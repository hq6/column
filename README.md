# Column.py

This is a more re-implementation of the venerable old `column` application
available on most Unix / Linux systems today.

## Why re-implement this ancient tool?

BSD `column` has been, for many, the tool that *almost* works for every
situation where we want to pretty-print a delimited table in textual form.
Unfortunately, it lacks two highly desirable features.

1. It has no option to right-justify columns instead of left-justifying them.
2. It has no option to specify the output delimiter, and has two spaces
   hardcoded.

## Why not just modify the original code?

The original code is over 20 years old, is written in a cryptic C style which
does not lend itself to easy modification, and uses the  compiler-dependent
`wchar_t` type is not actually wide enough for Unicode.
