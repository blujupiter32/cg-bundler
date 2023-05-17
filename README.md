# CG Bundler
A language-agnostic bundler created for use with complex CodinGame solutions.

[CodinGame](https://www.codingame.com) uses a single source file for each
submission. As a complex solution is developed, navigating this file can become
tedious due to its length.

This script enables a solution to be split into multiple source files and
directories, which are concatenated together before submission. Only files with
the same extension as the specified output file are included in the bundling
process.

By specifying a separator, the modular import and export features of the chosen
programming language may be used without including bogus imports in the output
file. This separator must be commented out as it is replaced with the path to
the source file in the output file.

Source files are concatenated in alphabetical order of their paths, with the
exception of a specified "main" file which is always included last.
