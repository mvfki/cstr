import sys

RESET = '\033[0m'
WRAPPER = {
    'black': '\033[30m',
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
    'none': '\033[0m'
}
ALIAS = {
    'blk': 'black', 'kuro': 'black', 'hei': 'black',
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
    'wu': 'none', 'n': 'none'
}

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
        to_sub = self.names[key]
        if isinstance(to_sub, str):
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
        
        elif isinstance(to_sub, list):
            if isinstance(value, str) and value not in ALIAS:
                try:
                    value = [ALIAS[i] for i in value]
                except KeyError:
                    raise ValueError("Given color is not supported.")
            elif isinstance(value, str) and value in ALIAS:
                value = [ALIAS[value]] * len(to_sub)
            if len(value) != len(to_sub):
                raise ValueError("Given color list length does not match "
                                 "slice selection.")
            self.names[key] = value

        self.codes = [WRAPPER[i] for i in self.names]

    def __getitem__(self, key):
        new_names = self.names[key]
        if isinstance(new_names, str):
            new_length = 1
        else:
            new_length = len(new_names)
        return cstrColor(new_length, new_names)

    def tolist(self):
        return self.names


class cstr(str):
    """
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
    """

    def __new__(cls, content=None, colors=None):
        if isinstance(content, cstr):
            return cstr(content.str, colors=colors)
        elif content is None:
            obj = str.__new__(cls, '')
            obj.colorRecord = cstrColor(0, [])
            return obj
        else:
            obj = str.__new__(cls, content)
            obj.colorRecord = cstrColor(len(str(content)), colors)
            return obj

    def _get_color(self):
        return self.colorRecord

    def _set_color(self, color):
        self.colorRecord = cstrColor(len(str.__str__(self)), color)

    color = property(_get_color, _set_color)

    @property
    def str(self):
        """
        Return the raw str content without color
        """
        return str.__str__(self)

    def block_format(self, indent_len=0, block_width=78,
                     indent_first_line=False, color=None):
        """
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
        """
        if type(indent_len) != int:
            raise TypeError("indentLen should be an int.")
        if type(block_width) != int:
            raise TypeError("blockWidth should be an int.")
        word_list = self.split()
        word_lens = [len(i) for i in word_list]
        if block_width < max(word_lens):
            raise ValueError("Max word length larger than line length.")
        text_block = ''
        line_len = 0
        if indent_first_line:
            text_block = ' ' * indent_len
        while word_list:
            new_word = word_list.pop(0)
            if line_len + len(new_word) > block_width:
                text_block += '\n' + ' ' * indent_len + new_word + ' '
                line_len = len(new_word) + 1
            else:
                text_block += new_word + ' '
                line_len += len(new_word) + 1
        return text_block

    def __str__(self):
        output = ''
        last_color = RESET
        if self.str == '':
            return ''
        for i in range(len(self)):
            if self.color.codes[i] != last_color:
                output += self.color.codes[i]
            output += self.str[i]
            last_color = self.color.codes[i]
        if last_color != RESET:
            output += RESET
        return output

    def __repr__(self):
        return(f'<cstr: str = {self.str.__repr__()}, '
               f'color = {self.color.names}>')

    def __add__(self, other):
        if not isinstance(other, cstr):
            if not other.split():
                other_color = [self.color.names[-1]]
            else:
                other_color = ['n']
            return cstr(self.str + str(other), 
                        self.color.names + other_color * len(str(other)))
        else:
            return cstr(self.str + other.str, 
                        self.color.names + other.color.names)

    def __mul__(self, value):
        value_type = str(type(value)).split("'")[1]
        if not isinstance(value, int):
            raise TypeError("can't multiply sequence by non-int of type "
                            f"'{value_type}'")
        return cstr(self.str * value, self.color.names * value)

    def __rmul__(self, value):
        value_type = str(type(value)).split("'")[1]
        if not isinstance(value, int):
            raise TypeError("can't multiply sequence by non-int of type "
                            f"'{value_type}'")
        return cstr(value * self.str, value * self.color.names)

    def __radd__(self, other):
        if not isinstance(other, cstr):
            if not other.split():
                other_color = [self.color.names[0]]
            else:
                other_color = ['n']
            return cstr(str(other) + self.str, 
                        other_color * len(str(other)) + self.color.names)
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
            new_str = cstr()
            if self[0] == '-' or self[0] == '+':
                new_str += self[0]
            n_zero = width - len(self)
            new_str += cstr('0' * n_zero, self.color.names[0])
            if self[0] == '-' or self[0] == '+':
                new_str += self[1:]
            else:
                new_str += self
            return new_str

    def lstrip(self, chars = None):
        remaining_content = self.str.lstrip(chars)
        remaining_len = len(remaining_content)
        return cstr(remaining_content, self.color.names[-remaining_len:])

    def rstrip(self, chars = None):
        remaining_content = self.str.rstrip(chars)
        remaining_len = len(remaining_content)
        return cstr(remaining_content, self.color.names[remaining_len:])

    def center(self, width, fill_char=' '):
        """
        Return a centered string of length width.

        Padding is done using the specified fill character (default is a space).

        Colors of filled chars follows each end of the cstr
        """
        if width <= len(self):
            return self
        elif (not isinstance(fill_char, str)) and len(fill_char) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            new_str = self.str.center(width, fill_char)
            width -= len(self)
            if width % 2 == 0:
                new_color = [self.color.names[0]] * (width // 2) \
                           + self.color.names \
                           + [self.color.names[-1]] * (width // 2)
            else:
                new_color = [self.color.names[0]] * ((width - 1) // 2) \
                           + self.color.names \
                           + [self.color.names[-1]] * ((width + 1) // 2)
            return cstr(new_str, new_color)

    def expandtabs(self, tabsize = 8):
        new_str = ''
        col_width = 0
        for i in self:
            if col_width == tabsize:
                col_width = 0
            if i != '\t':
                new_str += i
                col_width += 1
            else:
                new_str += cstr(' ' * (tabsize - col_width), i.color.names[0])
                col_width = 0
        return new_str

    def split(self, sep=None, max_split=-1):
        if max_split == 0:
            return [self]
        out_list = []
        if sep is None:
            seps = {' ', '\t', '\r', '\n'}  # TODO check if anymore default sep
            step = 1
        else:
            seps = {sep}
            step = len(sep)
        last_split = 0
        in_default_gap = False
        wait = 0
        split_time = 0
        i = 0
        while (max_split == -1 or split_time < max_split) and i < len(self):
            if wait > 0:
                wait -= 1
                continue
            if self.str[i:i+step] in seps:
                if not in_default_gap:
                    out_list.append(self[last_split:i])
                    split_time += 1
                    wait += step - 1
                if sep is None:
                    in_default_gap = True
                last_split = i + step
            else:
                in_default_gap = False
            i += 1

        if last_split <= len(self):
            out_list.append(self[last_split:len(self)])
        return out_list

    def splitlines(self, keepends=False):
        seps = {'\n', '\r'}
        out_list = []
        line = cstr()
        for i in self:
            if i in seps:
                if keepends:
                    line += i
                out_list.append(line)
                line = cstr()
            else:
                line += i
        if line != '':
            out_list.append(line)
        return out_list

    def join(self, iterable):
        new_str = ''
        for i in iterable[:-1]:
            new_str += i + self
        new_str += iterable[-1]
        return new_str

    def ljust(self, width, fill_char=' '):
        if width <= len(self):
            return self
        elif (not isinstance(fill_char, str)) and len(fill_char) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            width -= len(self)
            return self + cstr(fill_char * width, self.color.names[-1])

    def rjust(self, width, fill_char=' '):
        if width <= len(self):
            return self
        elif (not isinstance(fill_char, str)) and len(fill_char) != 1:
            raise TypeError("The fill character must be exactly "
                            "one character long")
        else:
            width -= len(self)
            return cstr(fill_char * width, self.color.names[0]) + self
