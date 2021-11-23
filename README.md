# elixir-task

[![](https://github.com/bblodfon/elixir-task/actions/workflows/pytest-ci.yml/badge.svg)](https://github.com/bblodfon/elixir-task/actions)

Development task for Elixir.no position candidates.

## Inputs

Given two types of text files of genomic information, using the **SEGMENT** format and the **FUNCTION** format, as defined below:

### SEGMENT (file suffix: ".s")

2 columns tab-separated file containing the coordinates of a set of regions (or segments/intervals) located along the reference DNA of some creature.
The 1st column is the start coordinate (starting from 0) and the 2nd column is the end coordinate of the region (end-exclusive).
Example:
```
100	200
300	400
```

In this task, the regions within one SEGMENT file are not allowed to overlap. i.e.:

```
100	200
150	250
```

is not allowed in one file. But

```
100	200
200	300
```

is allowed (because of the end-exclusiveness of column 2). 

The SEGMENT files are also always in sorted order.

### FUNCTION (file suffix: ".f")

One floating point number per position along the genome (i.e. per genome base pair), starting at position 0. E.g.:

```
25.0
26.0
10.0
11.0
...
```

### The "genome"

The "genome" in this test is just a line of positions from 0 to 10.000.000 (end exclusive).
All FUNCTION files must be fully defined, with one value per position.
A FUNCTION file thus always has 10 million lines.
A SEGMENT file, on the other hand, may have varying number of lines.

## Task overview

The program should take two input files.
Based on the types of file (SEGMENT or FUNCTION), the program should calculate a value as follows:

- **2 SEGMENT files**: calculate the overlap (in number of positions) of the regions from file X.s with regions from file Y.s.

Example:

file X.s:
```
1	2
3	6
```

file Y.s:
```
0	1
1	5
```

has an overlap of 3 (i.e. for positions 1, 3 and 4).

Note that the example files shown here have a "genome" of length 7

- **2 FUNCTION files**: calculate the sample *Pearson correlation coefficient* of the two number lists ([see here](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#For_a_sample) for the formula)

Example: the two files

X.f
```
10.0
11.0
12.0
13.0
14.0
15.0
16.0
```

Y.f
```
10.5
11.5
12.0
13.0
13.5
15.0
14.0
```

Have a Pearson correlation of 0.9452853.

- **1 SEGMENT and 1 FUNCTION file**: The mean of the numbers in the FUNCTION file whose positions are covered by the regions in the SEGMENT file.
That is, the regions in the SEGMENT file refer to positions on the genome and hence to the index of the lines in the FUNCTION file.

Example: for files X.s and Y.f, the covered numbers are (11.5, 13.0, 13.5, 15.0), which are on lines with index 1,3,4 and 5, the ones covered by the SEGMENT regions.
These numbers have a mean of 13.25.

## Notes on Implementation

The program should be written in Python, with limited use of external libraries.
The goal is to write quick code that still tries to follow good programming practices as regards object-oriented programming, system architecture, unit testing, and such.
This is to be regarded as pilot code designed in such a way to support the possible expansion with other file types and analyses in a simple manner.
The code does not need to be fully polished, but please comment places where improvements may be made.

Performance is not an issue; a basic Python implementation is enough.
However, all combinations of the input files provided should be runnable.
Also some thought should be made on the algorithmic performance.
