#!/usr/bin/env python3
"""Builds the Sauna Sticker Pack: svg/*.svg and png/*.png (512 x 512, transparent, white die-cut outline), preview.png.

Steps per sticker: draw the art as SVG -> fit it into the 512 box -> render the alpha -> grow it by OUTLINE px
(distance transform, so corners stay round) -> trace that mask back into one vector path -> put the white path
behind the art. The SVG sources therefore carry a real vector outline, and the lettering is converted to paths.

Needs: pip install resvg-py fonttools pillow numpy scipy scikit-image
License: artwork CC BY 4.0, script MIT - DIVELUX, https://diveluxsaunahat.com
"""
import io
import math
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import measure

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfxlib as g
import scenes as sc            # the drawing functions of the Sauna Illustrations set

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = g.PAL
SIZE, OUTLINE, MARGIN = 512, 12, 16        # px; 16 px clear margin is what WhatsApp asks for, Telegram is fine with it
STEAM = '#c4beb4'                          # steam is light grey here: white would vanish into the outline


def T(text, x, y, size, color=P['ink'], anchor='middle', tracking=-0.01):
    return f'<path d="{g.text_path(text, x, y, size, anchor=anchor, tracking=tracking)}" fill="{color}"/>'


def scene(fn, drop_shadow=True):
    """An illustration scene without its round paper spot and floor shadow."""
    out = []
    for m in fn():
        if m == sc.spot() or (drop_shadow and 'fill="#dfd7ca"' in m and m.startswith('<ellipse')):
            continue
        out.append(m.replace('stroke="#ffffff"', f'stroke="{STEAM}"'))
    return ''.join(out)


def wisps(xs, y, h, color, w=16, amp=14):
    return ''.join(sc.wisp(x, y, h, amp, w, c=color, op=1) for x in xs)


def rot(markup, deg, cx=256, cy=256):
    return f'<g transform="rotate({deg} {cx} {cy})">{markup}</g>'


def snowflake(cx, cy, R, color, w):
    d = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        tip = (cx + R * math.cos(a), cy + R * math.sin(a))
        for frac, br in ((.62, .30), (.34, .2)):
            mid = (cx + R * frac * math.cos(a), cy + R * frac * math.sin(a))
            l = (mid[0] + R * br * math.cos(a - math.radians(55)), mid[1] + R * br * math.sin(a - math.radians(55)))
            r = (mid[0] + R * br * math.cos(a + math.radians(55)), mid[1] + R * br * math.sin(a + math.radians(55)))
            d.append(f'M{l[0]:.1f} {l[1]:.1f} {mid[0]:.1f} {mid[1]:.1f} {r[0]:.1f} {r[1]:.1f}')
        d.append(f'M{cx} {cy} {tip[0]:.1f} {tip[1]:.1f}')
    return sc.line(''.join(d), color, w)


# ---------------------------------------------------------------- stickers: each returns SVG markup in any coordinates
def s_bell_hat():
    return sc.bell_hat(300, 100, 1.6)


def s_bucket_hat():
    return ''.join([
        sc.ell(300, 408, 158, 30, P['felt3']), sc.ell(300, 402, 158, 28, P['felt2']),
        sc.path('M218 396C222 300 246 250 300 250s78 50 82 146c-26 14-138 14-164 0z', P['felt1']),
        sc.path('M300 250c54 0 78 50 82 146-10 5.5-30 9-52 10 2-70-4-120-30-156z', P['felt2'], ' opacity=".45"'),
        sc.line('M221 372c30 15 128 15 158 0', P['felt3'], 5),
        sc.rect(338, 380, 24, 15, P['ember'], 3, ' transform="rotate(-8 350 388)"')])


def s_good_steam():
    art = (wisps((176, 256, 336), 196, 112, P['ink'], 17, 15)
           + sc.rect(56, 204, 400, 196, P['ember'], 40)
           + T('Good', 256, 292, 96) + T('steam!', 256, 376, 96))
    return rot(art, -5)


def s_loyly_time():
    return ''.join([
        sc.circ(256, 256, 214, P['paper']), f'<circle cx="256" cy="256" r="196" fill="none" stroke="{P["ink"]}" stroke-width="7"/>',
        sc.path('M256 84c17 21 26 34 26 47a26 26 0 0 1-52 0c0-13 9-26 26-47z', P['ember']),
        T('Löyly', 256, 256, 96), T('time', 256, 352, 96),
        sc.stone(206, 408, 30, 19, P['stone2'], -6), sc.stone(258, 404, 34, 22, P['stone3'], 4), sc.stone(310, 408, 28, 18, P['stone1'], 6)])


def s_hat_on():
    return sc.bell_hat(256, 20, 1.25) + T('HAT ON', 256, 430, 118, tracking=0.01)


def s_stove():
    return scene(sc.stove)


def s_bucket():
    return scene(sc.bucket)


def s_cool_down():
    return snowflake(256, 190, 150, P['water2'], 20) + T('Cool down', 256, 452, 88)


def s_whisk():
    return scene(sc.whisk)


def s_sauna_time():
    hourglass = ''.join([
        sc.rect(152, 214, 102, 16, P['wood4'], 6), sc.rect(152, 392, 102, 16, P['wood4'], 6),
        sc.path('M166 230h74c0 44-28 52-28 73s28 29 28 89h-74c0-60 28-68 28-89s-28-29-28-73z', P['line']),
        sc.path('M174 258h58c-6 22-22 28-29 42-7-14-23-20-29-42z', P['ember']),
        sc.path('M203 352c12 10 28 18 34 40h-68c6-22 22-30 34-40z', P['ember']),
        sc.line('M203 304v44', P['ember'], 4)])
    return (f'<g transform="translate(-20 -150) scale(1.1)">{hourglass}</g>'
            + T('Sauna', 412, 176, 92) + T('time', 412, 262, 92))


def s_one_more_round():
    art = (sc.rect(40, 150, 432, 212, P['paper'], 46)
           + f'<rect x="56" y="166" width="400" height="180" rx="32" fill="none" stroke="{P["ink"]}" stroke-width="6"/>'
           + T('One more', 256, 246, 78) + T('round!', 256, 322, 78)
           + sc.line('M170 392c50-16 120-16 172 0', P['ember'], 14))
    return rot(art, 4)


def s_steam_team():
    art = (wisps((196, 256, 316), 176, 100, P['ember'], 16, 14)
           + sc.rect(66, 186, 380, 210, P['ink'], 40)
           + T('Steam', 256, 280, 96, P['paper']) + T('team', 256, 364, 96, P['paper']))
    return rot(art, -3)


def s_thermometer():
    return ''.join([
        sc.rect(330, 150, 130, 310, P['wood2'], 14), sc.circ(395, 172, 6, P['wood4']),
        sc.rect(374, 196, 24, 200, P['white'], 12), sc.circ(386, 408, 24, P['white']),
        sc.rect(380, 232, 12, 170, P['ember'], 6), sc.circ(386, 408, 16, P['ember'])]
        + [sc.line(f'M410 {216 + k * 21}h{22 if k % 2 == 0 else 12}', P['ink2'], 4) for k in range(9)])


def s_plunge():
    return scene(sc.plunge)


def s_cabin():
    return ''.join(sc.cabin()) + '<circle cx="300" cy="305" r="250" fill="none" stroke="#1b1512" stroke-width="0"/>'


STICKERS = [
    ('bell-hat', 'Bell sauna hat', s_bell_hat, '🧢'),
    ('good-steam', 'Good steam!', s_good_steam, '👍'),
    ('loyly-time', 'Löyly time', s_loyly_time, '💦'),
    ('hat-on', 'Hat on', s_hat_on, '🎩'),
    ('sauna-stove', 'Sauna stove', s_stove, '🔥'),
    ('bucket-and-ladle', 'Bucket and ladle', s_bucket, '🪣'),
    ('cool-down', 'Cool down', s_cool_down, '❄️'),
    ('bucket-hat', 'Bucket sauna hat', s_bucket_hat, '👒'),
    ('sauna-time', 'Sauna time', s_sauna_time, '⏳'),
    ('one-more-round', 'One more round!', s_one_more_round, '🔁'),
    ('steam-team', 'Steam team', s_steam_team, '🤝'),
    ('birch-whisk', 'Birch whisk', s_whisk, '🌿'),
    ('thermometer', 'Thermometer', s_thermometer, '🌡️'),
    ('cold-plunge', 'Cold plunge', s_plunge, '🥶'),
    ('lakeside-sauna', 'Sauna by the lake', s_cabin, '🏡'),
]


def alpha_of(svg, px):
    return np.asarray(Image.open(io.BytesIO(g.render(svg, width=px))).convert('RGBA'))[:, :, 3]


def fit(markup):
    """Scale and center the art in the 512 box, leaving room for the outline."""
    big = 1400
    probe = f'<svg xmlns="http://www.w3.org/2000/svg" width="{big}" height="{big}" viewBox="-400 -400 {big} {big}">{markup}</svg>'
    a = alpha_of(probe, big) > 8
    ys, xs = np.where(a)
    x0, x1, y0, y1 = xs.min() - 400, xs.max() + 1 - 400, ys.min() - 400, ys.max() + 1 - 400
    room = SIZE - 2 * (OUTLINE + MARGIN)
    s = room / max(x1 - x0, y1 - y0)
    tx = (SIZE - (x1 - x0) * s) / 2 - x0 * s
    ty = (SIZE - (y1 - y0) * s) / 2 - y0 * s
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{markup}</g>'


def outline_path(art):
    """White backing: the art's alpha grown by OUTLINE px, holes filled, traced to a path."""
    k = 2
    a = alpha_of(f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">{art}</svg>', SIZE * k) > 40
    pad = 8
    a = np.pad(a, pad)
    dist = ndimage.distance_transform_edt(~a)
    grown = ndimage.binary_fill_holes(dist <= OUTLINE * k)
    field = ndimage.gaussian_filter(grown.astype(float), 1.2)
    d = []
    for c in measure.find_contours(field, 0.5):
        if len(c) < 30:
            continue
        c = measure.approximate_polygon(c, 0.35)
        pts = ' '.join(f'{(x - pad) / k:.1f} {(y - pad) / k:.1f}' for y, x in c[:-1])
        d.append(f'M{pts}Z')
    return ''.join(d)


def build_one(name, title, fn):
    art = fit(fn())
    d = outline_path(art)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">'
           f'<title>{title}</title><path d="{d}" fill="#ffffff"/>{art}</svg>\n')
    open(os.path.join(ROOT, 'svg', name + '.svg'), 'w', encoding='utf-8').write(svg)
    png = g.render(svg, os.path.join(ROOT, 'png', name + '.png'), width=SIZE)
    im = Image.open(io.BytesIO(png))
    a = np.asarray(im.convert('RGBA'))[:, :, 3]
    ys, xs = np.where(a > 0)
    edge = min(xs.min(), ys.min(), SIZE - 1 - xs.max(), SIZE - 1 - ys.max()) + 1
    corners = [int(a[0, 0]), int(a[0, -1]), int(a[-1, 0]), int(a[-1, -1])]
    print(f'{name:18} {im.size} {im.mode}  clear edge {edge:3d}px  corners alpha {corners}  transparent {100 * (a == 0).mean():.0f}%  {len(png) // 1024} KB')
    assert im.size == (SIZE, SIZE) and im.mode == 'RGBA' and edge >= 15 and max(corners) == 0 and len(png) < 512 * 1024
    return svg


def main():
    for d in ('svg', 'png'):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    only = sys.argv[1:]
    cells_light, cells_dark = [], []
    for name, title, fn, emoji in STICKERS:
        if only and name not in only:
            continue
        svg = build_one(name, title, fn)
        inner = svg[svg.index('</title>') + 8:svg.rindex('</svg>')]
        cells_light.append((f'<g transform="translate(22 12) scale({250 / SIZE})">{inner}</g>', name))
    if only:
        return
    for dark in (False, True):
        sheet = g.contact_sheet(cells_light, 5, 294.4, 300, 'Sauna Sticker Pack',
                                f'{len(cells_light)} stickers · 512 px PNG, transparent, white outline · SVG sources · Telegram and WhatsApp ready · CC BY 4.0',
                                dark=dark, grid_lines=False, label_size=14)
        if not dark:   # a mid-tone backdrop so the white outline shows
            sheet = sheet.replace(f'fill="{P["paper"]}"', 'fill="#d9cfc0"', 1)
        g.render(sheet, os.path.join(ROOT, 'preview-dark.png' if dark else 'preview.png'))
    extras()
    print(len(cells_light), 'stickers')


def extras():
    """WhatsApp wants 512 x 512 WebP under 100 KB and a 96 x 96 tray icon under 50 KB; Telegram takes an optional 100 x 100 icon."""
    os.makedirs(os.path.join(ROOT, 'whatsapp'), exist_ok=True)
    for name, title, fn, emoji in STICKERS:
        im = Image.open(os.path.join(ROOT, 'png', name + '.png')).convert('RGBA')
        out = os.path.join(ROOT, 'whatsapp', name + '.webp')
        im.save(out, 'WEBP', quality=90, method=6)
        assert os.path.getsize(out) < 100 * 1024, out
    hat = Image.open(os.path.join(ROOT, 'png', 'bell-hat.png')).convert('RGBA')
    hat.resize((96, 96), Image.LANCZOS).save(os.path.join(ROOT, 'whatsapp', 'tray-icon.png'), optimize=True)
    hat.resize((100, 100), Image.LANCZOS).save(os.path.join(ROOT, 'telegram-icon-100.png'), optimize=True)


if __name__ == '__main__':
    main()
