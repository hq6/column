#!/usr/bin/python

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
			            [default: \\s+]
    -r <right-align-mode>        Right align "all" columns, "numeric" columns,
                                    or "no" columns [default: numeric]
    -o --output-separator <ofs>  Delimiter to use between columns in the output
                                    table [default:   ]
"""
def main():
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
                float(item)
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

    sep = re.compile(options['--separator'])

    # Derive the number of columns from the header column
    headerLine = lines.pop(0)
    headerColumns = sep.split(headerLine)

    columnLists = defaultdict(list)
    for line in lines:
        columns = sep.split(line)
        for i in xrange(len(headerColumns)):
            if i < len(columns):
                columnLists[headerColumns[i]].append(columns[i])
            else:
                columnLists[headerColumns[i]].append("")
    for key in columnLists:
        maxWidth = max(len(x) for x in (columnLists[key] + [key]))
        if options['-r'] == "all":
            columnLists[key] = [key.rjust(maxWidth)] + \
            [x.rjust(maxWidth) for x in columnLists[key]]
        elif options['-r'] == "no":
            columnLists[key] = [key.ljust(maxWidth)] + \
            [x.ljust(maxWidth) for x in columnLists[key]]
        else:
            if isNumericColumn(columnLists[key]):
                columnLists[key] = [key.rjust(maxWidth)] + \
                [x.rjust(maxWidth) for x in columnLists[key]]
            else:
                columnLists[key] = [key.ljust(maxWidth)] + \
                [x.ljust(maxWidth) for x in columnLists[key]]

    orderedColumns = \
        [columnLists[headerColumns[i]] for i in xrange(len(headerColumns))]
    for row in zip(*orderedColumns):
        print options['--output-separator'].join(row)


if __name__ == '__main__':
    main()

