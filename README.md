# suffixtree
Suffix Tree implementation in pure Python

Implementation of a [Suffix tree](http://en.wikipedia.org/wiki/Suffix_tree). 
There are probably better implementations out there; this was just a learning exercise.

## Why is it useful?

The main advantage is that for an up-front linear time cost, to build the tree, plus linear space to hold it,
you can then do substring matches that are linear in the length of the query string, 
and are *independent of the size of the source string*! That's pretty cool.

Applications include looking for known sequences in a human genome, or searching for words and
phrases in a currently-open document.

Other neat applications include finding the longest repeated substring, or the longest palindrome,
in a given string in linear time.

## Are you allergic to code comments?

No, just busy. I plan on tidying up the code at an unspecified future date.

## Are you planning on adding functionality?

In an ideal world I'd like to add:

* Support for Generalized Suffix Trees (i.e. multiple strings in one tree).
* Palindrome and longest-substring implementations.
* An ASCII-art vizualizer
* Tests
* More whitespace
