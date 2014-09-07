#!/usr/bin/python
# -*- coding: utf-8 -*-

from nagu import (get_color, pack_color, pack, reset,
        sequence, parse_line, html)

def test_get_color():
    """
    >>> assert get_color(0) == ""
    >>> assert get_color(13) == "color: #ff0;"
    >>> assert get_color(64) == 'background-color: #ff0;'
    >>> assert get_color(13 + 64) == 'color: #ff0;background-color: #ff0;'
    """
    pass

def test_pack_color():
    """
    >>> assert pack_color(0, 0) == 0
    >>> assert pack_color(30, 0) == 14
    >>> assert pack_color(44, 14) == 158
    >>> assert pack_color(36, 158) == 148
    >>> assert pack_color(39, 148) == 144
    >>> assert pack_color(49, 144) == 0
    """
    pass

def test_pack():
    """
    >>> assert pack(0, 0) == 0
    >>> assert pack(30, 0) == 14
    >>> assert pack(1, 14) == 270
    >>> assert pack(4, 270) == 1294
    >>> assert pack(21, 1294) == 1038
    >>> assert pack(39, 1038) == 1024
    >>> assert pack(24, 1024) == 0
    """
    pass

def test_reset():
    """
    >>> assert reset() is None
    >>> assert reset(1) == 1
    """
    pass

def test_sequence():
    """
    Must return nothing on init
    >>> assert sequence(0) == ''

    Set to something
    >>> assert sequence(1) == '<span style="font-weight: bold;">'

    Update
    >>> assert sequence(93) == '</span><span style="font-weight: bold;color: #ff0;">'

    Not enabled modifier changes nothing
    >>> assert sequence(22) == '</span><span style="font-weight: bold;color: #ff0;">'

    Disable one
    >>> assert sequence(21) == '</span><span style="color: #ff0;">'

    Disable
    >>> assert sequence(0) == '</span>'
    """
    pass

def test_parse_line():
    """
    >>> string = "This is \033[1;33myellow\033[39m bold"
    >>> result = 'This is <span style="font-weight: bold;color: #cc0;">'+ \
        'yellow</span><span style="font-weight: bold;"> bold'
    >>> line = ''.join([x for x in parse_line(string)])
    >>> assert line == result
    >>> reset()
    """
    pass

html_text = '''This text is \033[4;34mblue \033[42mwith green background
have \033[1;39mtwo\033[21m lines\033[49m and still underlined\033[0m or not'''

def ts(s, r):
    for i in range(0, len(s)):
        if s[i] != r[i]:
            print i, s[i], r[i]

def test_html():
    """
    >>> result = 'This text is <span style="text-decoration: underline;'+ \
        'color: #28f;">blue </span><span style="text-decoration: underline;'+ \
        'color: #28f;background-color: #0c0;">with green background<br />'+ \
        'have </span><span style="font-weight: bold;text-decoration: underline;'+ \
        'background-color: #0c0;">two</span><span style="text-decoration: '+ \
        'underline;background-color: #0c0;"> lines</span><span '+ \
        'style="text-decoration: underline;"> and still underlined'+ \
        '</span> or not'
    >>> assert html(html_text) == result
    >>> reset()
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
