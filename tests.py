#!/usr/bin/python
# -*- coding: utf-8 -*-

from nagu import (get_color, pack_color, pack,
        sequence, parse_line, html)

def test_get_colors():
    """
    >>> assert get_color(0) == ""
    >>> assert get_color(13) == "color: #ff0;"
    >>> bg = 13 << 4
    >>> assert get_color(bg) == 'background-color: #ff0;'
    >>> assert get_color(13 + bg) == 'color: #ff0;background-color: #ff0;'
    """
    pass

def pack_color():
    """
    """
    pass

def test_pack():
    """
    """
    pass

def test_sequence():
    """
    Must return nothing on init
    >>> assert sequence(0) == ""

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
    >>> result = 'This is <span style="font-weigth: bold;color #c00">'+ \
        'yellow</span><span style="font-weight: bold;> bold'
    >>> line = ''.join([x for x in parse_line(string)])
    >>> assert line == result
    """
    pass

def test_html():
    """
    >>> text = '''This text is \033[4;34mblue \033[42mwith green background \
        have \033[1;39mtwo\033[21m lines\033[49m and still underlined\033[0m or not'''
    >>> result = '''This text is <span style="text-decoration: underline; \
        color: #28f;">blue </span><span style="text-decoration: underline; \
        color: #28f; background-color: #0c0;">with green background<br /> \
        have </span><span style="font-weight: bold;text-decoration: underline; \
        color: #28f; background-color: #0c0;">two</span><span style=" \
        text-decoration: underline; color: #28f; background-color: #0c0;"> \
        lines</span><span style="text-decoration: underline; color: #28f;> \
        and still underlined</span> or not'''
    >>> assert html(text) == result
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
