# Linux Terminal Colored str Object - cstr

Tested on Windows Subsystem Linux - Ubuntu

## Installation

```
git clone https://github.com/mvfki/cstr.git
cd cstr
python setup.py install
```

## Usage

### str Operations
Just use it in the same way as you deal with `str` object.  
> **TODO** say more

### Coloring
`cstr.__str__()` method returns the raw string with terminal understandable prefix and suffix so that it automatically turns out to be colored. To fetch the raw string only, use `cstr.str`.

## Example
Run the example script in your command line terminal. 
```
from cstr import cstr
s = cstr('Hello world!', 'rgbrgbrgbrgb')
print(s)
print(s.upper())
for word in s.split():
    print(word)
```
![Demo](https://github.com/mvfki/cstr/raw/master/DEMO.png)
