'use strict'; /*jslint node:true*/ /* jshint -W033 */
const nagu = require('./index.js')
debugger

test('get_color', ()=>{
    expect(nagu.t.get_color(0)).toBe('')
    expect(nagu.t.get_color(13)).toBe('color: #f0f;')
    expect(nagu.t.get_color(64)).toBe('background-color: #28f;')
    expect(nagu.t.get_color(13+64)).toBe('color: #f0f;background-color: #28f;')
})

test('pack_color', ()=>{
    expect(nagu.t.pack_color(0, 0)).toBe(0)
    expect(nagu.t.pack_color(95, 0)).toBe(13)
    expect(nagu.t.pack_color(44, 14)).toBe(78)
    expect(nagu.t.pack_color(36, 158)).toBe(150)
    expect(nagu.t.pack_color(39, 148)).toBe(144)
    expect(nagu.t.pack_color(49, 144)).toBe(0)
})

test('pack', ()=>{
    expect(nagu.t.pack(0, 0)).toBe(0)
    expect(nagu.t.pack(95, 0)).toBe(13)
    expect(nagu.t.pack(1, 14)).toBe(270)
    expect(nagu.t.pack(4, 270)).toBe(1294)
    expect(nagu.t.pack(21, 1294)).toBe(1038)
    expect(nagu.t.pack(39, 1038)).toBe(1024)
    expect(nagu.t.pack(24, 1024)).toBe(0)
})

describe('sequence', ()=>{
    const seq = nagu.t.sequence
    test('Must return nothing on init', ()=>expect(seq(0))
         .toBe(''))
    test('Set to something', ()=>expect(seq(1))
         .toBe('<span style="font-weight: bold;">'))
    test('Update', ()=>expect(seq(93))
         .toBe('</span><span style="font-weight: bold;color: #ff0;">'))
    test('Not enabled modifier changes nothing', ()=>expect(seq(22))
        .toBe('</span><span style="font-weight: bold;color: #ff0;">'))
    test('Disable one', ()=>expect(seq(21))
         .toBe('</span><span style="color: #ff0;">'))
    test('Disable', ()=>expect(seq(0)).toBe('</span>'))
})

const b = '\u001b'
test('parse_line', ()=>{
    /* jshint -W115 */
    const string = `This is ${b}[1;33myellow${b}[39m bold`
    const result = 'This is <span style="font-weight: bold;color: #cc0;">'+
        'yellow</span><span style="font-weight: bold;"> bold'
    expect(nagu.parse_line(string).join('')).toBe(result)
    nagu.t.reset()
})

test('html', ()=>{
    /* jshint -W115 */
    const html = `This text is ${b}[4;34mblue ${b}[42mwith green background
have ${b}[1;39mtwo${b}[21m lines${b}[49m and still underlined${b}[0m or not`
    const result= 'This text is <span style="text-decoration: underline;'+
        'color: #28f;">blue </span><span style="text-decoration: underline;'+
        'color: #28f;background-color: #0c0;">with green background<br />'+
        'have </span><span style="font-weight: bold;text-decoration: underline;'+
        'background-color: #0c0;">two</span><span style="text-decoration: '+
        'underline;background-color: #0c0;"> lines</span><span '+
        'style="text-decoration: underline;"> and still underlined'+
        '</span> or not'
    expect(nagu.html(html)).toBe(result)
    nagu.t.reset()
})
