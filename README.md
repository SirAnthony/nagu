Nagu
====

Nagu is simple library to convert ANSI/VT100 formatted text to html
representation. The main library use case to save colored cli output
for latest representation in browser.

Usage
------

Javascript:

```javascript
const nagu = require('nagu');
nagu.html(`This text is \033[4;34mblue \033[42mwith green background
have \033[1;39mtwo\033[21m lines\033[49m and still underlined\033[0m or not`);
'This text is <span style="text-decoration: underline;color: #28f;">blue </span><span style="text-decoration: underline;color: #28f;background-color: #0c0;">with green background<br />have </span><span style="font-weight: bold;text-decoration: underline;background-color: #0c0;">two</span><span style="text-decoration: underline;background-color: #0c0;"> lines</span><span style="text-decoration: underline;"> and still underlined</span> or not'
```

Python:

```python
>>> import nagu
>>> html_text = '''This text is \033[4;34mblue \033[42mwith green background
... have \033[1;39mtwo\033[21m lines\033[49m and still underlined\033[0m or not'''
>>>
>>> nagu.html(html_text)
'This text is <span style="text-decoration: underline;color: #28f;">blue </span><span style="text-decoration: underline;color: #28f;background-color: #0c0;">with green background<br />have </span><span style="font-weight: bold;text-decoration: underline;background-color: #0c0;">two</span><span style="text-decoration: underline;background-color: #0c0;"> lines</span><span style="text-decoration: underline;"> and still underlined</span> or not'
```

Rendered html (markdown strip styles):
<p>This text is <span style="text-decoration: underline;color: #28f;">blue </span><span style="text-decoration: underline;color: #28f;background-color: #0c0;">with green background<br />have </span><span style="font-weight: bold;text-decoration: underline;background-color: #0c0;">two</span><span style="text-decoration: underline;background-color: #0c0;"> lines</span><span style="text-decoration: underline;"> and still underlined</span> or not</p>

nagu-pipe
------
small 3-lines utility to use in cli with pipes.
Typical usage:

    grep -R --color=always 'na' . | ./nagu-pipe.py

