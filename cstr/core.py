import sys

RESET = '\033[0m'
WRAPPER = {'black': '\033[30m',
           'red': '\033[31m',
           'green': '\033[32m',
           'orange': '\033[33m',
           'blue': '\033[34m',
           'purple': '\033[35m',
           'cyan': '\033[36m',
           'lightgrey': '\033[37m',
           'darkgrey': '\033[90m',
           'lightred': '\033[91m',
           'lightgreen': '\033[92m',
           'yellow': '\033[93m',
           'lightblue': '\033[94m',
           'pink': '\033[95m',
           'lightcyan': '\033[96m', 
           'none': '\033[0m'}
ALIAS = {'blk': 'black', 'kuro': 'black', 'hei': 'black', 
         'r': 'red', 'aka': 'red', 'hong': 'red', 
         'g': 'green', 'grn': 'green', 'midori': 'green', 'lv': 'green',
         'lu': 'green', 
         'o': 'orange', 'cheng': 'orange', 'ju': 'orange', 
         'jv': 'orange',
         'b': 'blue', 'ao': 'blue', 'lan': 'blue',
         'p': 'purple', 'murasaki': 'purple', 'zi': 'purple',
         'qing': 'cyan',
         'y': 'yellow', 'ki': 'yellow', 'huang': 'yellow',
         'momo': 'pink', 'fen': 'pink',
         'w': 'none', 'white': 'none', 'null': 'none', 
         'wu': 'none', 'n': 'none'}
ALIAS.update({i: i for i in WRAPPER})

class cstrColor(object):
    def __init__(self, length, colors = None):
        if colors is None:
            self.names = ['none'] * length
            self.codes = [''] * length
        if isinstance(colors, cstrColor):
            colors = colors.names
        if isinstance(colors, str):
            if colors not in ALIAS:
                if len(colors) == length:
                    colors = list(colors)
                    self.names = [ALIAS[i] for i in colors]
                    self.codes = [WRAPPER[i] for i in self.names]
                else:
                    raise ValueError("Given color is not supported.")
            else:
                self.names = [ALIAS[colors]] * length
                self.codes = [WRAPPER[i] for i in self.names]
        elif isinstance(colors, list):
            if length != len(colors):
                raise ValueError("Given color list length does not match "
                                 "string length")
            self.names = [ALIAS[i] for i in colors]
            self.codes = [WRAPPER[i] for i in self.names]

    def __str__(self):
        return f'<cstrColor names: {str(self.names)}>'

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, key, value):
        toSub = self.names[key]
        if isinstance(toSub, str):
            if isinstance(value, str) and value not in ALIAS:
                raise ValueError("Given color is not supported.")
            elif isinstance(value, str) and value in ALIAS:
                value = ALIAS[value]
            elif isinstance(value, list) and len(value) != 1:
                raise ValueError("Given color list length does not match "
                                 "slice selection.")
            elif isinstance(value, list) and len(value) == 1:
                if value[0] not in ALIAS:
                    raise ValueError("Given color is not supported.")
                value = ALIAS[value[0]]
            self.names[key] = value
        
        elif isinstance(toSub, list):
            if isinstance(value, str) and value not in ALIAS:
                try:
                    value = [ALIAS[i] for i in value]
                except KeyError:
                    raise ValueError("Given color is not supported.")
            elif isinstance(value, str) and value in ALIAS:
                value = [ALIAS[value]] * len(toSub)
            if len(value) != len(toSub):
                raise ValueError("Given color list length does not match "
                                 "slice selection.")
            self.names[key] = value

        self.codes = [WRAPPER[i] for i in self.names]

    def __getitem__(self, key):
        newNames = self.names[key]
        if isinstance(newNames, str):
            newLength = 1
        else:
            newLength = len(newNames)
        return cstrColor(newLength, newNames)

    def tolist(self):
        return self.names

class cstr(str):
    '''
    str inherited object that can be displayed with color in command line 
    terminal.
    Arguments:
    ----------
    content - `object` with `.__str__()` method
    colors  - `str` or `list` of `str`, default `None`.
              1. If `list`, each element states the color of each character in 
              `str(content)`. 
                  `assert len(colors) == len(str(content))`
              2. If `str`, can be one of the keys of `cstr.ALIAS`, that 
              states all the color of the `cstr`
              3. If `str`, can also be a string sequence where each character
              states a color, e.g. `'rrgb'` states for `['red', 'red', 
              'green', 'blue']`. Note that choices for single-character key 
              word are limited.
                  `assert len(colors) == len(str(content))`
    Returns:
    ----------
    `cstr` object.
    '''

    def __new__(cls, content = None, colors = None):
        if isinstance(content, cstr):
            return cstr(content.str, colors = colors)
        elif content == None:
            obj = str.__new__(cls, '')
            obj.colorRecord = cstrColor(0, [])
            return obj
        else:
            obj = str.__new__(cls, content)
            obj.colorRecord = cstrColor(len(str(content)), colors)
            return obj

    def _getColor(self):
        return self.colorRecord

    def _setColor(self, color):
        self.colorRecord = cstrColor(len(str.__str__(self)), color)

    color = property(_getColor, _setColor)

    @property
    def str(self):
        '''
        Return the raw str content without color
        '''
        return str.__str__(self)

    def blockFormat(self, indentLen = 0, blockWidth = 78, 
                   indentFirstLine = False, color = None):
        '''
        Format long cstr to lines of text with fixed line length.
        Arguments:
        ----------
        indentLen       - `int`, default `0`
                          The number of spaces to add at the left of the text
                          block
        lenPerLine      - `int`, default `78`
                          The character number limit for each line, not 
                          including the indentation.
        indentFirstLine - `bool`, default `False`
                          Whether the first line follows the same indentation
                          scheme.
        color           - `str`, default `None`.
                          New color to display in the returned `cstr`. If 
                          NoneType, will follow the original color. If the 
                          coloring should be canceled, pass string `"none"`.
        Return:
        ----------
        `cstr`, with formatted string content and the same color
        ''' 
        if type(indentLen) != int:
            raise TypeError("indentLen should be an int.")
        if type(blockWidth) != int:
            raise TypeError("blockWidth should be an int.")
        wordList = self.split()
        wordLens = [len(i) for i in wordList]
        if blockWidth < max(wordLens):
            raise ValueError("Max word length larger than line length.")
        textBlock = ''
        lineLen = 0
        nLine = 0
        if indentFirstLine:
            textBlock = ' ' * indentLen
        while wordList:
            newWord = wordList.pop(0)
            if lineLen + len(newWord) > blockWidth:
                textBlock += '\n' + ' ' * indentLen + newWord + ' '
                lineLen = len(newWord) + 1
            else:
                textBlock += newWord + ' '
                lineLen += len(newWord) + 1
        return textBlock

    def __str__(self):
        output = ''
        lastColor = RESET
        if self.str == '':
            return ''
        for i in range(len(self)):
            if self.color.codes[i] != lastColor:
                output += self.color.codes[i]
            output += self.str[i]
            lastColor = self.color.codes[i]
        if lastColor != RESET:
            output += RESET
        return output

    def __repr__(self):
        return(f'<cstr: str = {self.str.__repr__()}, '
               f'color = {self.color.names}>')

    def __add__(self, other):
        if not isinstance(other, cstr):
            if other.split() == []:
                otherColor = [self.color.names[-1]]
            else:
                otherColor = ['n']
            return cstr(self.str + str(other), 
                        self.color.names + otherColor * len(str(other)))
        else:
            return cstr(self.str + other.str, 
                        self.color.names + other.color.names)

    def __mul__(self, value):
        valueType = str(type(value)).split("'")[1]
        if not isinstance(value, int):
            raise TypeError("can't multiply sequence by non-int of type "
                            f"'{valueType}'")
        return cstr(self.str * value, self.color.names * value)

    def __rmul__(self, value):
        valueType = str(type(value)).split("'")[1]
        if not isinstance(value, int):
            raise TypeError("can't multiply sequence by non-int of type "
                            f"'{valueType}'")
        return cstr(value * self.str, value * self.color.names)

    def __radd__(self, other):
        if not isinstance(other, cstr):
            if other.split() == []:
                otherColor = [self.color.names[0]]
            else:
                otherColor = ['n']
            return cstr(str(other) + self.str, 
                        otherColor * len(str(other)) + self.color.names)
        else:
            return cstr(other.str + self.str, 
                        other.color.names + self.color.names)

    def __iter__(self):
        self._iterI = -1
        return self

    def __next__(self):
        self._iterI += 1
        if self._iterI < len(self):
            return cstr(self.str[self._iterI], self.color.names[self._iterI])
        else:
            raise StopIteration

    def __getitem__(self, key):
        return cstr(self.str[key], self.color[key])

    def lower(self):
        return cstr(self.str.lower(), self.color)
    def upper(self):
        return cstr(self.str.upper(), self.color)

    def capitalize(self):
        return cstr(self.str.capitalize(), self.color)

    def swapcase(self):
        return cstr(self.str.swapcase(), self.color)

    def title(self):
        return cstr(self.str.title(), self.color)

    def zfill(self, width):
        if width <= len(self):
            return self
        else:
            newStr = cstr()
            if self[0] == '-' or self[0] == '+':
                newStr += self[0]
            nZero = width - len(self)
            newStr += cstr('0' * nZero, self.color.names[0])
            if self[0] == '-' or self[0] == '+':
                newStr += self[1:]
            else:
                newStr += self
            return newStr

    def lstrip(self, chars = None):
        remainingContent = self.str.lstrip(chars)
        remainingLen = len(remainingContent)
        return cstr(remainingContent, self.color.names[-remainingLen:])

    def rstrip(self, chars = None):
        remainingContent = self.str.rstrip(chars)
        remainingLen = len(remainingContent)
        return cstr(remainingContent, self.color.names[remainingLen:])

    def center(self, width, fillchar=' '):
        '''
        Return a centered string of length width.

        Padding is done using the specified fill character (default is a space).
        
        Colors of filled chars follows each end of the cstr
        '''
        if width <= len(self):
            return self
        elif (not isinstance(fillchar, str)) and len(fillchar) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            newStr = self.str.center(width, fillchar)
            width -= len(self)
            if width % 2 == 0:
                newColor = [self.color.names[0]] * (width // 2) \
                           + self.color.names \
                           + [self.color.names[-1]] * (width // 2)
            else:
                newColor = [self.color.names[0]] * ((width - 1) // 2) \
                           + self.color.names \
                           + [self.color.names[-1]] * ((width + 1) // 2)
            return cstr(newStr, newColor)

    def expandtabs(self, tabsize = 8):
        newStr = ''
        colWidth = 0
        for i in self:
            if colWidth == tabsize:
                colWidth = 0
            if i != '\t':
                newStr += i
                colWidth += 1
            else:
                newStr += cstr(' ' * (tabsize - colWidth), i.color.names[0])
                colWidth = 0
        return newStr

    def split(self, sep = None, maxsplit = -1):
        if maxsplit == 0:
            return [self]
        outList = []
        if sep == None:
            seps = {' ', '\t', '\r', '\n'} #TODO check if anymore default sep
            step = 1
        else:
            seps = {sep}
            step = len(sep)
        lastSplit = 0
        inDefaultGap = False
        wait = 0
        splitTime = 0
        i = 0
        while (maxsplit == -1 or splitTime < maxsplit) and i < len(self):
            if wait > 0:
                wait -= 1
                continue
            if self.str[i:i+step] in seps:
                if not inDefaultGap:
                    outList.append(self[lastSplit:i])
                    splitTime += 1
                    wait += step - 1
                if sep == None:
                    inDefaultGap = True
                lastSplit = i + step
            else:
                inDefaultGap = False
            i += 1

        if lastSplit <= len(self):
            outList.append(self[lastSplit:len(self)])
        return outList

    def splitlines(self, keepends = False):
        seps = {'\n', '\r'}
        outList = []
        line = cstr()
        for i in self:
            if i in seps:
                if keepends:
                    line += i
                outList.append(line)
                line = cstr()
            else:
                line += i
        if line != '':
            outList.append(line)
        return outList

    def join(self, iterable):
        newStr = ''
        for i in iterable[:-1]:
            newStr += i + self
        newStr += iterable[-1]
        return newStr

    def ljust(self, width, fillchar=' '):
        if width <= len(self):
            return self
        elif (not isinstance(fillchar, str)) and len(fillchar) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            width -= len(self)
            return self + cstr(fillchar * width, self.color.names[-1])

    def rjust(self, width, fillchar=' '):
        if width <= len(self):
            return self
        elif (not isinstance(fillchar, str)) and len(fillchar) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            width -= len(self)
            return cstr(fillchar * width, self.color.names[0]) + self
