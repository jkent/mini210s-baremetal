#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4 ai fenc=utf-8:

import sys
import struct

BLOCK_SIZE = 512
HEADER_FORMAT = '<IxxxxIxxxx'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s infile outfile' % sys.argv[0]
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    
    code = ''
    with open(in_path, 'rb') as f:
        code = f.read()
    
    header_len = struct.calcsize(HEADER_FORMAT)
    code_len = len(code)
    remainder = ((header_len + code_len) % BLOCK_SIZE)
    padding_len = 0
    if remainder:
        padding_len = BLOCK_SIZE - remainder

    size = header_len + code_len + padding_len

    sum = 0
    for c in code:
        sum += ord(c)
    
    header = struct.pack(HEADER_FORMAT, size, sum)

    padding = '\0' * padding_len

    with open(out_path, 'wb') as f:
        f.write(header)
        f.write(code)
        f.write(padding)
