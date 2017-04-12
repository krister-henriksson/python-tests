#! /usr/bin/python3

"""

Script for counting words in file(s). A word is defined as a contiguous
sequence of non-whitespace characters. A word ends when a whitespace
character is encountered.


"""

import sys;

def main():
    if len(sys.argv)<=1:
        print("");
        print("Usage:");
        print("    {:s} file1 [file2 [file3 [...]]]".format(sys.argv[0]));
        print("Arguments:");
        print("  file1        Text file whose word count is desired.");
        print("  file2        Text file whose word count is desired.");
        print("  ...          ...");
        print("");
        sys.exit();
    
    for st in sys.argv[1:]:
        n = 0;
        try:
            f = open(st, "r");
        except FileNotFoundError as e:
            print("{:20s}  {:10d}  (file not found)".format(st, 0));
        else:
            for line in f:
                n += len(line.split());
            f.close();
            print("{:20s}  {:10d}".format(st, n));


if __name__ == '__main__':
    main()

