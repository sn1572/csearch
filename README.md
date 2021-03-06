# csearch
CLI tool for finding symbols in C source files.

A few examples:

It can be used to locate (obscure) symbols contained in (obscure) object files:

![Sample image 1](https://github.com/sn1572/csearch/blob/master/pics/csearch-3.PNG?raw=true)

It can be used to locate declarations in header files (ioctl is not declared in ioctl.h, it turns out):

![Sample image 2](https://github.com/sn1572/csearch/blob/master/pics/csearch-4.PNG?raw=true)

## Installation

```
git clone https://github.gatech.edu/mbolding3/csearch.git
```

No dependencies beyond the Python 3 standard libraries, `bash`, `cat`, `nm`, and `grep`.

## Example usage

### Object file mode

Let's say you're looking for a symbol named "glUniform1d". Try:
```
./csource -o -t /lib glUniform1d
```
**explanation**
`-o` indicates "object mode" which searches for symbols defined in .o, .so, and .a files. `-t /lib` specifies that the seach target is the directory /lib. `glUniform1d` is the pattern to grep for. The pattern follows all the rules of grep, so putting `glUniform` in this field will fill your screeen with all the various symbols whose name starts with glUniform (there are a lot).

### C source and header file mode

Now we want to know what header file declared "glUniform1d". This time we use:
```
./csource -he -t /usr/include glUniform
```
**explanation**
The only difference with the previous example is `-he` which uses header mode. `-c` searches through `.c`, `.cu`, and `.cpp` files. Note that you can use any combination of available modes, eg. `-c -h` is valid but might be a little confusing.

### Recursive mode

Just set the `-r`, `-R`, or `--recursive` flags.
