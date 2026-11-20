#!/usr/bin/env python3
"""Builds the Sauna Illustrations set: svg/*.svg (600 x 600), png/*.png (1200 x 1200, transparent), preview.png.

Every scene is a plain Python function that returns SVG shapes; no tracing, no raster effects.
Needs: pip install resvg-py fonttools (fonts only for the preview sheet, see gfxlib.py)
License: artwork CC BY 4.0, script MIT - DIVELUX, https://diveluxsaunahat.com
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfxlib as g

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = g.PAL
SPOT = P['paper2']


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def spot(r=250, cy=305):
    return f'<circle cx="300" cy="{cy}" r="{r}" fill="{SPOT}"/>'


def shadow(cx, cy, rx, ry=14, c='#dfd7ca'):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}"/>'


def rect(x, y, w, h, c, rx=0, extra=''):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{c}"{extra}/>'


def ell(cx, cy, rx, ry, c, extra=''):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{c}"{extra}/>'


def circ(cx, cy, r, c, extra=''):
    return f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{c}"{extra}/>'


def path(d, c, extra=''):
    return f'<path d="{d}" fill="{c}"{extra}/>'


def line(d, c, w=5, extra=''):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def wisp(x, y, h, amp=14, w=14, c='#ffffff', op=0.9, n=3):
    """A rising steam wisp: a soft S-curve that starts at (x, y) and goes up by h."""
    seg = h / n
    d = f'M{f(x)} {f(y)}'
    s = 1
    for i in range(n):
        y0 = y - i * seg
        d += f' C{f(x + s * amp)} {f(y0 - seg * .33)} {f(x - s * amp)} {f(y0 - seg * .66)} {f(x)} {f(y0 - seg)}'
    return line(d, c, w, f' opacity="{op}"')


def stone(cx, cy, rx, ry, c, rot=0):
    return f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="{c}" transform="rotate({rot} {f(cx)} {f(cy)})"/>'


def stones(cx, base, scale=1.0):
    """A pile of stones centered on cx, resting on y=base."""
    S1, S2, S3 = P['stone1'], P['stone2'], P['stone3']
    rows = [
        [(-88, -20, 32, 22, S2, -6), (-30, -24, 38, 26, S1, 4), (32, -22, 34, 24, S3, -3), (86, -19, 30, 21, S2, 8)],
        [(-58, -58, 30, 21, S1, 6), (0, -64, 34, 23, S2, -4), (58, -58, 29, 20, S1, 3)],
        [(-26, -94, 26, 18, S3, -8), (26, -96, 25, 17, S1, 6)],
    ]
    out = []
    for row in rows:
        for dx, dy, rx, ry, c, rot in row:
            out.append(stone(cx + dx * scale, base + dy * scale, rx * scale, ry * scale, c, rot))
    return ''.join(out)


# ---------------------------------------------------------------- scenes
def stove():
    o = [spot(), shadow(300, 524, 170)]
    o.append(wisp(250, 190, 120, 16, 15))
    o.append(wisp(305, 170, 130, 18, 17))
    o.append(wisp(360, 195, 110, 14, 13))
    o.append(stones(300, 312))
    o.append(rect(205, 500, 20, 26, P['ink'], 4) + rect(375, 500, 20, 26, P['ink'], 4))
    o.append(rect(186, 306, 228, 200, P['ink'], 16))
    o.append(rect(174, 294, 252, 30, P['ink2'], 10))
    o.append(rect(232, 360, 136, 104, P['ink2'], 10))
    o.append(rect(250, 378, 100, 68, P['ember'], 7))
    o.append(path('M300 388c4 14 22 22 22 40a22 22 0 0 1-44 0c0-8 4-14 9-19 1 7 4 10 8 12-3-13-1-24 5-33z', P['glow']))
    o.append(line('M214 344h172', P['ink2'], 6))
    o.append(circ(385, 412, 6, P['wood2']))
    return o


def bucket():
    o = [spot(), shadow(300, 500, 150)]
    # tall grip stave behind the rim
    o.append(rect(196, 176, 40, 110, P['wood2'], 10))
    o.append(ell(216, 206, 8, 12, SPOT))
    # body
    o.append(path('M190 262h220l-22 216a14 14 0 0 1-14 12H226a14 14 0 0 1-14-12z', P['wood2']))
    for x1, x2 in ((238, 246), (300, 300), (362, 354)):
        o.append(line(f'M{x1} 286 {x2} 486', P['wood3'], 4))
    o.append(path('M193 300h214l-2.2 22H195.200z', P['ink2']))
    o.append(path('M206 424h188l-2.2 22H208.200z', P['ink2']))
    # rim and water
    o.append(ell(300, 262, 110, 26, P['wood3']))
    o.append(ell(300, 266, 97, 19, P['water']))
    o.append(line('M250 268c14-5 28-5 40 0', P['white'], 4, ' opacity=".8"'))
    # ladle: bowl in the water, long handle to the upper right
    o.append(line('M318 262 452 140', P['wood4'], 15))
    o.append(line('M318 262 452 140', P['wood3'], 7))
    o.append(path('M270 262a44 16 0 0 0 88 0z', P['water2'], ' opacity=".55"'))
    # drops
    for x, y, s in ((470, 215, 1), (492, 262, .75), (455, 290, .6)):
        o.append(path(f'M{x} {y}c{f(9*s)} {f(11*s)} {f(13*s)} {f(18*s)} {f(13*s)} {f(25*s)}a{f(13*s)} {f(13*s)} 0 0 1-{f(26*s)} 0c0-{f(7*s)} {f(4*s)}-{f(14*s)} {f(13*s)}-{f(25*s)}z', P['water2']))
    return o


def bell_hat(cx, top, s=1.0, tag=True):
    """Classic bell sauna hat. cx = center, top = y of the crown top."""
    o = []
    q = lambda x, y: f'{f(cx + x * s)} {f(top + y * s)}'
    o.append(path(f'M{q(0, 0)}C{q(-64, 6)} {q(-84, 96)} {q(-108, 196)}H{f(cx + 108 * s)}C{q(84, 96)} {q(64, 6)} {q(0, 0)}z', P['felt1']))
    o.append(path(f'M{q(0, 0)}C{q(64, 6)} {q(84, 96)} {q(108, 196)}H{f(cx + 30 * s)}C{q(30, 120)} {q(22, 60)} {q(0, 0)}z', P['felt2'], ' opacity=".45"'))
    o.append(line(f'M{q(0, 2)}C{q(-22, 60)} {q(-34, 120)} {q(-36, 190)}', P['felt2'], 4 * s))
    o.append(line(f'M{q(0, 2)}C{q(22, 60)} {q(30, 120)} {q(30, 190)}', P['felt3'], 4 * s, ' opacity=".7"'))
    o.append(rect(cx - 120 * s, top + 184 * s, 240 * s, 34 * s, P['felt3'], 17 * s))
    if tag:
        o.append(rect(cx + 62 * s, top + 193 * s, 26 * s, 16 * s, P['ember'], 3 * s))
    return ''.join(o)


def hat_hook():
    o = [spot()]
    # peg rail
    o.append(rect(96, 150, 408, 58, P['wood2'], 12))
    o.append(line('M120 170h150M330 190h150M150 192h70', P['wood3'], 3))
    for x in (176, 300, 424):
        o.append(circ(x, 181, 17, P['wood4']))
        o.append(circ(x - 4, 177, 6, P['wood3']))
    # loop and hat
    o.append(line('M300 186c-16 22-14 44 0 62 14-18 16-40 0-62z', P['felt3'], 7))
    o.append(bell_hat(300, 244, 1.05))
    o.append(circ(300, 181, 17, P['wood4']) + circ(296, 177, 6, P['wood3']))
    # ladle on the right peg
    o.append(line('M424 196v150', P['wood3'], 11))
    o.append(path('M392 346h64a32 32 0 0 1-64 0z', P['wood4']))
    o.append(circ(424, 181, 17, P['wood4']) + circ(420, 177, 6, P['wood3']))
    # towel on the left peg
    o.append(path('M150 190h52v180a8 8 0 0 1-8 8h-36a8 8 0 0 1-8-8z', P['white']))
    o.append(rect(150, 330, 52, 10, P['ember']))
    o.append(rect(150, 346, 52, 5, P['felt1']))
    o.append(circ(176, 181, 17, P['wood4']) + circ(172, 177, 6, P['wood3']))
    return o


def bucket_hat():
    o = [spot()]
    o.append(wisp(170, 250, 110, 14, 13))
    o.append(wisp(440, 230, 120, 16, 15))
    # bench
    o.append(rect(70, 420, 460, 30, P['wood2'], 6))
    o.append(rect(70, 456, 460, 22, P['wood3'], 6))
    o.append(rect(120, 478, 26, 62, P['wood4'], 4) + rect(454, 478, 26, 62, P['wood4'], 4))
    o.append(line('M100 435h120M300 435h190', P['wood3'], 3))
    # hat: brim, crown, band
    o.append(ell(300, 408, 158, 30, P['felt3']))
    o.append(ell(300, 402, 158, 28, P['felt2']))
    o.append(path('M218 396C222 300 246 250 300 250s78 50 82 146c-26 14-138 14-164 0z', P['felt1']))
    o.append(path('M300 250c54 0 78 50 82 146-10 5.5-30 9-52 10 2-70-4-120-30-156z', P['felt2'], ' opacity=".45"'))
    o.append(line('M221 372c30 15 128 15 158 0', P['felt3'], 5))
    o.append(rect(338, 380, 24, 15, P['ember'], 3, ' transform="rotate(-8 350 388)"'))
    return o


def leaf(x, y, rot, s, c, vein):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(s)})">'
            f'<path d="M0 -34C20 -22 22 10 0 34C-22 10 -20 -22 0 -34z" fill="{c}"/>'
            f'<path d="M0 -24V30" fill="none" stroke="{vein}" stroke-width="2.5" stroke-linecap="round"/></g>')


def whisk():
    o = [spot()]
    rnd = random.Random(7)
    # handle: bound twigs
    for dx in (-12, 0, 12):
        o.append(line(f'M{268 + dx} {372 + dx * .6} {150 + dx} {492 + dx * .6}', P['wood4'], 11))
    o.append(line('M152 494 268 374', P['wood3'], 4))
    # leaves, back to front
    leaves = []
    for i in range(64):
        a = rnd.uniform(-1, 1)
        r = 40 + 190 * rnd.random() ** .8
        spread = 62 * (1 - .45 * r / 230)                 # the fan narrows a little toward the tips
        ang = math.radians(-47 + a * spread)
        x = 250 + r * math.cos(ang)
        y = 392 + r * math.sin(ang)
        rot = math.degrees(ang) + 90 + rnd.uniform(-40, 40)
        leaves.append((r, x, y, rot, rnd.uniform(1.15, 1.6)))
    leaves.sort(key=lambda t: -t[0])
    for k, (r, x, y, rot, s) in enumerate(leaves):
        c, v = ((P['leaf'], P['leaf2']) if k % 3 else (P['leaf2'], '#3f5a35'))
        if k % 7 == 3:
            c, v = '#8aa871', P['leaf']
        o.append(leaf(x, y, rot, s, c, v))
    # twine
    o.append(line('M236 372l36 36', P['ink2'], 12))
    o.append(line('M226 384l34 34', P['ink2'], 12))
    o.append(line('M246 420c10 14 6 30-8 40', P['ink2'], 5))
    return o


def cabin():
    cid = 'cabin-clip'
    o = [f'<clipPath id="{cid}"><circle cx="300" cy="305" r="250"/></clipPath>', f'<g clip-path="url(#{cid})">']
    o.append(rect(40, 40, 520, 520, SPOT))
    o.append(circ(462, 176, 38, P['ember']))
    # far hills
    o.append(path('M40 372c70-58 150-66 232-30 80-52 190-52 288 8v70H40z', P['felt1']))
    # pines
    def pine(x, base, h, c):
        w = h * .42
        return (path(f'M{x} {base - h}l{f(w * .55)} {f(h * .42)}h-{f(w * .2)}l{f(w * .5)} {f(h * .36)}h-{f(w * 1.7)}l{f(w * .5)}-{f(h * .36)}h-{f(w * .2)}z', c)
                + rect(x - 5, base - h * .24, 10, h * .24, P['wood4']))
    for x, b, h, c in ((92, 404, 150, P['leaf2']), (140, 406, 110, P['leaf']), (488, 404, 130, P['leaf2']), (530, 406, 96, P['leaf']), (404, 404, 84, P['leaf'])):
        o.append(pine(x, b, h, c))
    # ground and lake
    o.append(rect(40, 398, 520, 14, P['wood3']))
    o.append(rect(40, 410, 520, 160, P['water']))
    o.append(path('M432 452h60v10h-60zM418 476h88v10h-88zM438 500h48v10h-48z', P['ember'], ' opacity=".55"'))
    o.append(line('M90 440h70M210 470h90M120 500h60M300 520h80', P['white'], 5, ' opacity=".7"'))
    # smoke
    o.append(wisp(318, 232, 110, 14, 13))
    # cabin
    o.append(rect(306, 232, 26, 50, P['ink2'], 3))
    o.append(rect(176, 296, 190, 104, P['wood2']))
    for y in (322, 348, 374):
        o.append(line(f'M176 {y}h190', P['wood3'], 3))
    o.append(path('M150 304 271 214l121 90h-26l-95-70-95 70z', P['ink']))
    o.append(path('M176 304l95-70 95 70z', P['wood3']))
    o.append(rect(204, 330, 48, 70, P['wood4'], 4))
    o.append(circ(243, 368, 4, P['wood1']))
    o.append(rect(286, 334, 50, 40, P['ink2'], 4))
    o.append(rect(292, 340, 38, 28, P['glow'], 2))
    o.append(line('M311 340v28', P['ink2'], 4))
    # dock
    o.append(rect(352, 400, 120, 13, P['wood2'], 2))
    for x in (372, 416, 460):
        o.append(rect(x, 400, 9, 40, P['wood4'], 2))
    o.append('</g>')
    return o


def plunge():
    o = [spot(), shadow(300, 506, 170)]
    # snowflake
    sf = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        cx, cy, R = 300, 150, 52
        tip = (cx + R * math.cos(a), cy + R * math.sin(a))
        mid = (cx + R * .62 * math.cos(a), cy + R * .62 * math.sin(a))
        l = (mid[0] + 17 * math.cos(a - math.radians(50)), mid[1] + 17 * math.sin(a - math.radians(50)))
        r = (mid[0] + 17 * math.cos(a + math.radians(50)), mid[1] + 17 * math.sin(a + math.radians(50)))
        sf.append(f'M{cx} {cy} {f(tip[0])} {f(tip[1])}M{f(l[0])} {f(l[1])} {f(mid[0])} {f(mid[1])} {f(r[0])} {f(r[1])}')
    o.append(line(''.join(sf), P['water2'], 9))
    # ladder behind the tub
    o.append(line('M430 250v250M474 290v210', P['wood4'], 12))
    for y in (330, 380, 430):
        o.append(line(f'M430 {y}h44', P['wood4'], 9))
    # tub
    o.append(path('M150 290h300l-16 196a16 16 0 0 1-16 14H182a16 16 0 0 1-16-14z', P['wood2']))
    for x1, x2 in ((205, 212), (252, 256), (300, 300), (348, 344), (395, 388)):
        o.append(line(f'M{x1} 318 {x2} 494', P['wood3'], 4))
    o.append(path('M153 330h294l-1.8 22H154.800z', P['ink2']))
    o.append(path('M162 440h276l-1.8 22H163.800z', P['ink2']))
    o.append(ell(300, 290, 150, 34, P['wood3']))
    o.append(ell(300, 295, 135, 26, P['water']))
    o.append(line('M215 296c16-6 32-6 46 0M330 304c14-5 28-5 40 0', P['white'], 4, ' opacity=".8"'))
    # ice
    o.append(rect(262, 272, 34, 30, P['white'], 6, ' transform="rotate(-12 279 287)"'))
    o.append(rect(326, 266, 30, 27, P['white'], 6, ' transform="rotate(14 341 280)"'))
    o.append(rect(378, 284, 24, 21, P['white'], 5, ' transform="rotate(-6 390 294)"'))
    return o


def towels():
    o = [spot(), shadow(300, 500, 190)]
    # folded stack
    cols = [(P['wood1'], P['wood2']), (P['felt1'], P['felt2']), (P['white'], P['line'])]
    for k, (c, c2) in enumerate(cols):
        y = 420 - k * 64
        w = 300 - k * 14
        x = 300 - w / 2 - 20
        o.append(rect(x, y, w, 62, c, 22))
        o.append(line(f'M{f(x + 18)} {y + 31}h{f(w - 40)}', c2, 4))
        o.append(path(f'M{f(x + w - 26)} {y + 8}a23 23 0 0 1 0 46', c2, ' opacity=".6"'))
    o.append(rect(232, 300, 22, 54, P['ember'], 0))
    o.append(rect(262, 300, 7, 54, P['ember'], 0))
    # rolled towel on top
    o.append(rect(170, 232, 200, 62, P['felt2'], 31))
    o.append(circ(339, 263, 31, P['felt1']))
    pts = []
    for i in range(0, 61):
        t = i / 60 * 2.4 * 2 * math.pi
        r = 3 + 19 * i / 60
        pts.append(f'{f(339 + r * math.cos(t))} {f(263 + r * math.sin(t))}')
    o.append(line('M' + ' '.join(pts), P['felt3'], 4))
    # slippers, seen from the front
    for cx, cy in ((418, 474), (500, 482)):
        o.append(ell(cx, cy + 4, 46, 13, P['wood4']))
        o.append(ell(cx, cy, 46, 13, P['wood2']))
        o.append(path(f'M{cx - 40} {cy + 3}c0-52 80-52 80 0c-22 9-58 9-80 0z', P['felt3']))
        o.append(line(f'M{cx - 31} {cy - 8}c14 8 48 8 62 0', P['felt1'], 4))
    return o


def timer_thermo():
    o = [spot()]
    # sand timer on a board
    o.append(rect(128, 150, 150, 310, P['wood2'], 14))
    o.append(line('M150 180v250M256 190v240', P['wood3'], 3))
    o.append(circ(203, 172, 6, P['wood4']))
    o.append(rect(152, 214, 102, 16, P['wood4'], 6) + rect(152, 392, 102, 16, P['wood4'], 6))
    o.append(path('M166 230h74c0 44-28 52-28 73s28 29 28 89h-74c0-60 28-68 28-89s-28-29-28-73z', P['white'], ' opacity=".85"'))
    o.append(path('M174 258h58c-6 22-22 28-29 42-7-14-23-20-29-42z', P['ember']))
    o.append(path('M203 352c12 10 28 18 34 40h-68c6-22 22-30 34-40z', P['ember']))
    o.append(line('M203 304v44', P['ember'], 4))
    for k in range(4):
        o.append(line(f'M140 {250 + k * 42}h8', P['ink2'], 4))
    # thermometer
    o.append(rect(330, 150, 130, 310, P['wood2'], 14))
    o.append(circ(395, 172, 6, P['wood4']))
    o.append(rect(374, 196, 24, 200, P['white'], 12))
    o.append(circ(386, 408, 24, P['white']))
    o.append(rect(380, 262, 12, 140, P['ember'], 6))
    o.append(circ(386, 408, 16, P['ember']))
    for k in range(9):
        y = 216 + k * 21
        o.append(line(f'M410 {y}h{22 if k % 2 == 0 else 12}', P['ink2'], 4))
    return o


def interior():
    cid = 'interior-clip'
    o = [f'<clipPath id="{cid}"><circle cx="300" cy="305" r="250"/></clipPath>', f'<g clip-path="url(#{cid})">']
    o.append(rect(40, 40, 520, 520, P['wood1']))
    for x in range(60, 560, 44):
        o.append(line(f'M{x} 40v520', P['wood2'], 3))
    # window with evening light
    o.append(rect(340, 104, 110, 90, P['ink2'], 8))
    o.append(rect(348, 112, 94, 74, P['glow'], 4))
    o.append(circ(416, 146, 16, P['ember']))
    o.append(line('M395 112v74', P['ink2'], 5))
    # backrest
    o.append(rect(40, 236, 520, 22, P['wood2'], 4))
    o.append(rect(40, 258, 520, 6, P['wood3']))
    # upper bench
    o.append(rect(40, 318, 520, 26, P['wood2']))
    o.append(rect(40, 344, 520, 12, P['wood3']))
    for x in (130, 440):
        o.append(rect(x, 356, 22, 220, P['wood4']))
    # lower bench
    o.append(rect(40, 432, 520, 28, P['wood2']))
    o.append(rect(40, 460, 520, 12, P['wood3']))
    o.append(rect(40, 472, 520, 100, P['wood4'], 0, ' opacity=".35"'))
    for x in (130, 440):
        o.append(rect(x, 472, 22, 100, P['wood4']))
    # hat on the upper bench
    o.append(bell_hat(206, 216, .5, tag=True))
    # bucket on the lower bench
    o.append(path('M330 372h84l-8 60h-68z', P['wood3']))
    o.append(path('M332 386h80l-1.3 10h-77.400z', P['ink2']))
    o.append(path('M336 414h72l-1.3 10h-69.400z', P['ink2']))
    o.append(ell(372, 372, 42, 9, P['wood4']))
    o.append(line('M384 370 430 318', P['wood4'], 8))
    # steam
    o.append(wisp(100, 300, 150, 16, 15, op=.75))
    o.append(wisp(262, 216, 130, 16, 14, op=.7))
    o.append(wisp(520, 420, 150, 16, 15, op=.75))
    o.append('</g>')
    return o


SCENES = [
    ('sauna-stove', 'Sauna stove with stones and steam', stove),
    ('bucket-and-ladle', 'Wooden bucket and ladle', bucket),
    ('bell-hat-on-peg', 'Bell sauna hat on a peg rail', hat_hook),
    ('bucket-hat-on-bench', 'Bucket sauna hat on a bench', bucket_hat),
    ('birch-whisk', 'Birch whisk', whisk),
    ('lakeside-sauna', 'Sauna cabin by the lake', cabin),
    ('cold-plunge', 'Cold plunge tub', plunge),
    ('towels-and-slippers', 'Towels and slippers', towels),
    ('timer-and-thermometer', 'Sand timer and thermometer', timer_thermo),
    ('sauna-bench', 'Inside the sauna', interior),
]


def svg_doc(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">'
            f'<title>{title}</title>{"".join(body)}</svg>\n')


def main():
    os.makedirs(os.path.join(ROOT, 'svg'), exist_ok=True)
    os.makedirs(os.path.join(ROOT, 'png'), exist_ok=True)
    only = sys.argv[1:] 
    cells = []
    for name, title, fn in SCENES:
        body = fn()
        doc = svg_doc(title, body)
        open(os.path.join(ROOT, 'svg', name + '.svg'), 'w', encoding='utf-8').write(doc)
        if not only or name in only:
            g.render(doc, os.path.join(ROOT, 'png', name + '.png'), width=1200)
        cells.append((f'<g transform="translate(24 16) scale({320 / 600})">{"".join(body)}</g>', name))
    sheet = g.contact_sheet(cells, 4, 368, 386, 'Sauna Illustrations', f'{len(cells)} flat vector scenes · SVG + PNG 1200 px · free under CC BY 4.0',
                            grid_lines=True, label_size=15)
    g.render(sheet, os.path.join(ROOT, 'preview.png'))
    print(len(cells), 'illustrations')


if __name__ == '__main__':
    main()
