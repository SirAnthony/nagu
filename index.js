'use strict'; /*jslint node:true, browser:true, esversion:6*/
/* jshint -W033 */
(function(){
var define;
if (!(typeof module=='object' && module.exports && module.children))
    define = self.define;
else
{
    define = function(name, req, setup){
        module.exports = setup.apply(this, req.map(function(dep){
            return require(dep) })) }
}

define('nagu', [], function(){
const E = {};

E.ESCAPE_CHAR = '\u001b' // \033

const CONTROL_CODES = {
    0: 'reset',
    1: 'bold',
    2: 'dim',
    4: 'underline',
    5: 'blink',
    7: 'reverse',
    8: 'hidden',
    21: 'reset-bold',
    22: 'reset-dim',
    24: 'reset-underline',
    25: 'reset-blink',
    27: 'reverse-off',
    28: 'reset-hidden',
}

const FG_COLORS = {
    30: '#000', // black
    31: '#c00', // red
    32: '#0c0', // green
    33: '#cc0', // yellow
    34: '#28f', // blue
    35: '#c0c', // magenta
    36: '#0cc', // cyan
    37: '#eee', // gray
    90: '#444', // dark gray
    91: '#f00', // light red
    92: '#0f0', // light green
    93: '#ff0', // light yellow
    94: '#48b', // light blue
    95: '#f0f', // light magenta
    96: '#0ff', // light cyan
    97: '#fff', // white
}

const BG_COLORS = {}
for (let c in FG_COLORS)
    BG_COLORS[(c|0)+10] = FG_COLORS[c]
const DEFAULT_COLORS = {39: 0, 49: 1}
const COLORS = Object.assign({}, FG_COLORS, BG_COLORS, DEFAULT_COLORS)
const COLOR_INDEX = [enumerate(Object.keys(FG_COLORS)),
    enumerate(Object.keys(BG_COLORS))]
const COLOR_INDEX_R = {}
COLOR_INDEX.map(function(b){
    for (let k in b)
        COLOR_INDEX_R[b[k]] = k
})

const STYLES = [
    'color: {COLOR};',
    'background-color: {COLOR};',
    'font-weight: bold;',
    '',
    'text-decoration: underline;',
    '',
    'direction: rtl; unicode-bidi: bidi-override;',
    'visibility: hidden;',
]

const MODS = {
     1: 1,   2: 2,   4: 3,   5: 4,   7: 5,   8: 6,
    21: -1, 22: -2, 24: -3, 25: -4, 27: -5, 28: -6,
}
const COLOR_SHIFT = 4
const COLOR_SIZE = 1 << COLOR_SHIFT
const COLOR_LEN = COLOR_SIZE - 1
const FIRST_MOD = COLOR_SHIFT * 2
for (let k in MODS)
{
    let offset = FIRST_MOD - 1
    if (MODS[k] < 0)
        MODS[k] -= offset
    else if (MODS[k] > 0)
        MODS[k] += offset
}
const LAST_MOD = Math.max.apply(Math, Object.values(MODS))+1

function enumerate(obj){
    let ret = {}
    for (let i=0; i<obj.length; i++)
        ret[i] = obj[i];
    return ret;
}

function get_color(num){
    // fg, bg
    let col = [num & COLOR_LEN, (num >> COLOR_SHIFT) & COLOR_LEN]
    return col.map(function(c, i){
        let idx = COLOR_INDEX[i][c]
        if (c && !(idx in DEFAULT_COLORS))
            return STYLES[i].replace(/\{COLOR\}/, COLORS[idx])
    }).filter(Boolean).join('')
}

function pack_color(c, mod){
    if (c in DEFAULT_COLORS)
        mod &= ~(COLOR_LEN << (DEFAULT_COLORS[c] * COLOR_SHIFT))
    else if (c in COLOR_INDEX_R)
    {
        let shift = c in FG_COLORS ? 0 : COLOR_SHIFT
        mod &= ~(COLOR_LEN << shift)
        mod |= (COLOR_INDEX_R[c] & COLOR_LEN) << shift
    }
    return mod
}

function pack(m, mod){
    if (m in COLORS)
        return pack_color(m, mod)
    let shift = MODS[m]||0
    if (shift > 0)
        mod |= 1 << shift
    else if (shift < 0)
        mod &= ~(1 << -shift)
    return mod
}

let MOD = 0
function reset(r){
    MOD = 0
    return r
}

function sequence(seq){
    const seqs = seq.toString().split(';')
    const mods = seqs.filter(function(x){ return /[0-9]+/.test(x) })
        .map(function(x){ return x|0 });
    if (!mods.length)
        return ''
    if (mods.includes(0))
        return reset(MOD ? '</span>' : '')
    let styles = []
    if (MOD)
        styles.push('</span>')
    for (let m of mods)
        MOD = pack(m, MOD)
    styles.push('<span style="')
    for (let shift = FIRST_MOD; shift<LAST_MOD; shift++)
    {
        if (MOD & (1 << shift))
            styles.push(STYLES[shift - FIRST_MOD + 2])
    }
    styles.push(get_color(MOD), '">')
    return styles.join('')
}


E.parse_line = function(text){
    let char = 0
    let length = text.length
    let ret = [];
    while (char < length)
    {
       if (text[char] == E.ESCAPE_CHAR)
       {
           char += 2
           let esc = ''
           while (char < length && text[char] != 'm')
           {
               if (esc.length > 20)
                   break;
               esc += text[char]
               char += 1
           }
           char += 1
           ret.push(sequence(esc))
       }
       else
       {
           char += 1
           ret.push(text[char-1])
       }
    }
    return ret
}
E.html = function(text){
    let lines = text
    if (typeof lines==='string')
        lines = lines.split('\n')
    return lines.map(function(l){ return E.parse_line(l).join('') })
        .join('<br />')+sequence('')
}

E.t = {
    get_color,
    pack_color,
    pack,
    reset,
    sequence,
}

return E }) })()
