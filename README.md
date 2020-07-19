# Unix Terminal Colored str Object - cstr

Tested on the following environments:
- Windows Subsystem for Linux (Ubuntu)
- Mac OSX Terminal
- Windows MobaXterm connected to a Linux cluster server (CentOS)
- Windows Spyder editer console

## Installation

```
git clone https://github.com/mvfki/cstr.git
cd cstr
python setup.py install
```

## Usage

### str Operations
Just use it in the same way as you deal with normal `str` objects.

### Coloring
- Use `cstr()` to color text.
- Use `cstr.__str__()` to obtain the raw string with the Unix coloring prefix and suffix.
- Use `cstr.str` to get the raw string.

## Example
Run this example script in your terminal/command line to see Cstr in action!
```python
from cstr import cstr

s = cstr('Hello world!', 'rgbrgbrgbrgb')
print(s)
print(s.upper())
for word in s.split():
    print(word)
```

![Demo](https://github.com/mvfki/cstr/raw/master/docs/DEMO.png)
