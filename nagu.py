# -*- coding: utf-8 -*-

CONTROL_CODES = {
    0: "reset",
    1: "bold",
    2: "dim",
    4: "underline",
    5: "blink",
    7: "reverse",
    8: "hidden",
    21: "reset-bold",
    22: "reset-dim",
    24: "reset-underline",
    25: "reset-blink",
    27: "reverse-off",
    28: "reset-hidden",
}

FG_COLORS = {
    30: "#000", # black
    31: "#c00", # red
    32: "#0c0", # green
    33: "#cc0", # yellow
    34: "#28f", # blue
    35: "#c0c", # magenta
    36: "#0cc", # cyan
    37: "#eee", # gray
    90: "#444", # dark gray
    91: "#f00", # light red
    92: "#0f0", # light green
    93: "#ff0", # light yellow
    94: "#48b", # light blue
    95: "#f0f", # light magenta
    96: "#0ff", # light cyan
    97: "#fff", # white
}

BG_COLORS = dict((c+10, n) for c, n in FG_COLORS.items())
DEFAULT_COLORS = {39: 0, 49: 1}
COLORS = dict(FG_COLORS.items() + BG_COLORS.items()
        + DEFAULT_COLORS.items())
COLORS_INDEX = (dict(enumerate(FG_COLORS.keys())), dict(enumerate(BG_COLORS.keys())))
COLORS_INDEX_R = {}
for b in COLORS_INDEX:
    COLORS_INDEX_R.update(dict((v, k) for k, v in b.items()))

STYLES = (
    "color: {0};",
    "background-color: {0};",
    "font-weight: bold;",
    "",
    "text-decoration: underline;",
    "",
    "direction: rtl; unicode-bidi: bidi-override;",
    "visibility: hidden;",
)

MODS = {
     1: 1,   2: 2,   4: 3,   5: 4,   7: 5,   8: 6,
    21: -1, 22: -2, 24: -3, 25: -4, 27: -5, 28: -6,
}
COLOR_SHIFT = 4
COLOR_SIZE = 1 << COLOR_SHIFT
COLOR_LEN = COLOR_SIZE - 1
COLORS_DATA = COLOR_SIZE * 2
FIRST_MOD = COLOR_SHIFT * 2
for k in MODS.keys():
    offset = FIRST_MOD - 1
    if MODS[k] < 0:
        MODS[k] -= offset
    elif MODS[k] > 0:
        MODS[k] += offset
LAST_MOD = max(MODS.values())+1

def get_color(num):
    fg, bg = num & COLOR_LEN, (num >> COLOR_SHIFT) & COLOR_LEN
    out = ''
    for i, c in enumerate((fg, bg)):
        idx = COLORS_INDEX[i][c]
        if idx not in DEFAULT_COLORS and c:
            out += STYLES[i].format(COLORS[idx])
    return out

def pack_color(c, mod):
    if c in DEFAULT_COLORS:
        mod &= ~(COLOR_LEN << (DEFAULT_COLORS[c] * COLOR_SHIFT))
    elif c in COLORS_INDEX_R:
        shift = 0 if c in FG_COLORS else COLOR_SHIFT
        mod &= ~(COLOR_LEN << shift)
        mod |= (COLORS_INDEX_R[c] & COLOR_LEN) << shift
    return mod

def pack(m, mod):
    if m in COLORS:
        return pack_color(m, mod)
    shift = MODS.get(m, 0)
    if shift > 0:
        mod |= 1 << shift
    elif shift < 0:
        mod &= ~(1 << -shift)
    return mod

MOD = 0
def reset(r=None):
    global MOD
    MOD = 0
    return r

def sequence(seq):
    global MOD
    seqs = list(set(unicode(seq).split(';')))
    mods = [int(x) for x in seqs if x.isdigit()]
    if not len(mods):
        return ''
    if 0 in mods:
        return reset('</span>' if MOD else '')
    styles = []
    if MOD:
        styles.append('</span>')
    for m in mods:
        MOD = pack(m, MOD)
    styles.append('<span style="')
    for shift in range(FIRST_MOD, LAST_MOD):
        if MOD & (1 << shift):
            styles.append(STYLES[shift - FIRST_MOD + 2])
    styles.extend([get_color(MOD), '">'])
    return ''.join(styles)

def parse_line(text):
    char = 0
    length = len(text)
    while char < length:
       if text[char] == '\033':
           char += 2
           esc = ''
           while text[char] != 'm' and char < length:
               if len(esc) > 20:
                   break
               esc += text[char]
               char += 1
           char += 1
           yield sequence(esc)
       else:
           char += 1
           yield text[char-1]

def html(text):
    lines = text.splitlines()
    out = '<br />'.join([''.join([s for s in parse_line(l)]) \
            for l in lines])
    return out+sequence('0');

__all__ = ['html']

