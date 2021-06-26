"""
Copyright 2020 IQuick 143

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so, subject
to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import re


class Generator(object):
    def __init__(self, generator):
        self.generator = generator

    def generate(self, join=" "):
        # 0 is the entry token
        stack = [0]
        result = []
        while len(stack) > 0:
            value = stack.pop()
            # None values are dropped
            if value is None:
                continue
            if isinstance(value, str):
                result.append(value)
            elif isinstance(value, int):
                # List reversion needed because the stack is backwards
                stack.extend(random.choice(self.generator[value])[::-1])
        return join.join(result).replace(" .", ".")


def loadGenerator(filename):
    main_re = re.compile(r'^\s*([A-Z0-9_]+)\s*=\s*((?:[A-Z0-9_]+|\s+|\||"(?:[^\\"]|\\\\|\\")+")+)')
    expr_re = re.compile(r'(?:[A-Z0-9_]+|\s+|"(?:[^\\"]|\\\\|\\")+")+')
    toke_re = re.compile(r'[A-Z0-9_]+|"(?:[^\\"]|\\\\|\\")+"')

    tokens = ["START"]
    needed_tokens = ["START"]
    defined_tokens = []

    generator = {}

    with open(filename, mode="r", encoding="UTF-8") as file:
        lnum = -1
        for line in file.readlines():
            lnum += 1
            striped = line.strip()
            # skip empty lines and comments
            if striped == "" or striped[0] == "#":
                continue
            match = main_re.match(striped)
            if match is None:
                raise ValueError("Line #%s has invalid formatting" % lnum)
            TOKEN = match.group(1)
            EXPRESS = match.group(2)
            if TOKEN in defined_tokens:
                raise ValueError("Token %s is defined multiple times" % TOKEN)
            else:
                defined_tokens.append(TOKEN)
            if TOKEN not in tokens:
                tokens.append(TOKEN)
            define_key = tokens.index(TOKEN)
            options = []
            for sub_expr_match in expr_re.finditer(EXPRESS):
                sub_expr = sub_expr_match.group(0).strip()
                option = []
                for token in toke_re.finditer(sub_expr):
                    token = token.group(0)
                    if token[0] == "\"":
                        token = token[1:-1].replace("\\\\", "\\").replace("\\\"", "\"")
                        option.append(token)
                    else:
                        if token == "NONE":
                            continue
                        if token not in needed_tokens:
                            needed_tokens.append(token)
                        if token not in tokens:
                            tokens.append(token)
                        option.append(tokens.index(token))
                options.append(option)
            generator[define_key] = options
    diff = set(needed_tokens).difference(set(defined_tokens))
    if len(diff) > 0:
        raise ValueError("Tokens %s are used but not defined" % list(diff))

    return Generator(generator)