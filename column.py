#!/usr/bin/env python

from __future__ import print_function
from functools import reduce

from sys import argv, stdin
from docopt import docopt
from collections import defaultdict
import re
import codecs

from signal import signal, SIGPIPE, SIG_DFL


doc = r"""
Usage: ./column.py [options] [<input> ...]

    -h,--help                    show this
    -s,--separator <sep>         specify the regex used for delimiting columns
    -r <right-align-mode>        Right align "all" columns, "numeric" columns,
                                    or "no" columns [default: numeric]
    -o --output-separator <ofs>  Delimiter to use between columns in the output
                                    table [default:   ]
"""
def main():
    ansi_escape = re.compile(r'(\x1B\[[0-?]*[ -/]*[@-~])')
    def removeAnsiEscape(s):
        return ansi_escape.sub('', s)

    # These three functions are meant to remove ansi escape sequences from
    # before and/or after a string, perform justification, and then re-add
    # escape sequences.
    def colorSafeJust(s, width, rightJust=True):
        parts = list(filter(None, ansi_escape.split(s)))
        for i in range(len(parts)):
            if ansi_escape.match(parts[i]): continue
            # NOTE: If there is more than one non-escape part, that implies
            # there was an escape sequence in the middle of the column,
            # which this tool does not support.
            parts[i] = parts[i].rjust(width) if rightJust else parts[i].ljust(width) 
            break
        return ''.join(parts)
    def colorSafeRjust(s, width):
        return colorSafeJust(s, width)
    def colorSafeLjust(s, width):
        return colorSafeJust(s, width, False)

    # Handle broken pipes when piping the output of this process to other
    # processes.
    signal(SIGPIPE,SIG_DFL)
    options = docopt(doc)
    def isValidLine(x):
        y = x.strip()
        if y.startswith("#") or len(y) == 0:
            return False
        return True

    def isNumericColumn(x):
        for item in x:
            if item in ("", "N/A", "NA"): continue
            try:
                float(removeAnsiEscape(item))
            except:
                return False
        return True

    lines = None
    if len(options["<input>"]) == 0:
      # read from stdin
      lines = [x.strip().encode("utf-8") for x in stdin.readlines() \
              if isValidLine(x)]
    else:
      linesList = []
      for name in options["<input>"]:
          with codecs.open(name, "r", "utf-8") as f:
              linesList.append([x.strip().encode("utf-8") \
                  for x in f.readlines() if isValidLine(x)])
      lines = reduce(lambda x, a: x + a, linesList, [])

    sep = re.compile(options['--separator'] if options['--separator'] else r'\s+')

    # Derive the number of columns from the header column
    headerLine = lines.pop(0)
    headerColumns = sep.split(headerLine.decode('utf-8'))

    columnLists = defaultdict(list)
    for line in lines:
        columns = sep.split(line.decode('utf-8'))
        for i in range(len(headerColumns)):
            if i < len(columns):
                columnLists[headerColumns[i]].append(columns[i])
            else:
                columnLists[headerColumns[i]].append("")
    for key in columnLists:
        maxWidth = max(len(removeAnsiEscape(x)) for x in (columnLists[key] + [key]))
        if options['-r'] == "all":
            columnLists[key] = [colorSafeRjust(key,maxWidth)] + \
            [colorSafeRjust(x,maxWidth) for x in columnLists[key]]
        elif options['-r'] == "no":
            columnLists[key] = [colorSafeLjust(key,maxWidth)] + \
            [colorSafeLjust(x,maxWidth) for x in columnLists[key]]
        else:
            if isNumericColumn(columnLists[key]):
                columnLists[key] = [colorSafeRjust(key,maxWidth)] + \
                [colorSafeRjust(x,maxWidth) for x in columnLists[key]]
            else:
                columnLists[key] = [colorSafeLjust(key,maxWidth)] + \
                [colorSafeLjust(x,maxWidth) for x in columnLists[key]]

    orderedColumns = \
        [columnLists[headerColumns[i]] for i in range(len(headerColumns))]
    for row in zip(*orderedColumns):
        print(options['--output-separator'].join(row))


if __name__ == '__main__':
    main()

