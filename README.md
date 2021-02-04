# csearch
CLI tool for finding symbols in C source files.

## Installation

```
git clone https://github.gatech.edu/mbolding3/csearch.git
```

No dependencies beyond the Python 3 standard libraries.

## Example usage

### Object file mode

Let's say you're looking for a symbol named "glUniform1d". Try:
```
./csource -o -d /lib glUniform1d
```
**explanation**
`-o` indicates "object mode" which searches for symbols defined in .o, .so, and .a files. `-d /lib` specifies that the seach directory is /lib. `glUniform1d` is the pattern to grep for. The pattern follows all the rules of grep, so putting `glUniform` in this field will fill your screeen with all the various symbols whose name starts with glUniform (there are a lot).

### C source and header file mode

Now we want to know what header file declared "glUniform1d". This time we use:
```
./csource -h -d /usr/include glUniform
```
The only difference with the previous example is `-h` which uses header mode. `-c` has a similar effect. Note that you can use any combination of available modes, eg. `-c -h` is valid but might be a little confusing.
