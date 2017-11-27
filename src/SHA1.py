#!/usr/bin/env python3
# -*-coding: utf-8 -*-

""" This module contains the SHA1 class
"""

import struct
from src.functions import bytearray_xor, rotl

class SHA1(object):
    """ SHA 1 hash algorithm implementation

        Attributes:
            block_size -- int -- block size, in bytes
            h -- list -- hash variables
    """

    def __init__(self):
        self.block_size = 64
        self.h = [0x67452301,
                  0xEFCDAB89,
                  0x98BADCFE,
                  0x10325476,
                  0xC3D2E1F0]

    def final_hash(self):
        """ Combine the 5 hash variables to produce the final hash
            return the 160 bits length hash
        """
        #return ''.join([str(h) for h in self.h])
        return rotl(self.h[0], 128) or rotl(self.h[1], 96) or rotl(self.h[2], 64) or rotl(self.h[3], 32) or self.h[4]

    def pad(self, arr):
        """
            SHA-1 works with blocks of 64 bytes (512 bits). If the number of bits
            in the text is not a multiple of 512, add some padding:
                - add '1' at the end of the text
                - fill with '0' (but let 64 bits available at the end)
                - the 64 last bits are the length of the original text

            Args:
                arr -- bytearray -- the text to hash in bytes

            return arr, padded if needed
        """
        original_length = len(arr)

        if len(arr) % self.block_size == 0:
            return arr

        # append the bit 1
        arr.append(0x80)

        # add k*'0', with len(arr) + k = 56 (mod 64)
        # => to let 8 bytes (64 bits) for original text length
        nb_zero_to_add = ((7*self.block_size)//8 - len(arr)) % self.block_size
        for _ in range(nb_zero_to_add):
            arr.append(0)

        # add the length of the original text
        arr += struct.pack(b'>Q', original_length)

        return arr

    def hash(self, text):
        # transform the string to an array of bytes
        bytes_text = bytearray(text, 'utf-8')
        # SHA-1 works with 512 bits blocks.
        # add some padding if needed
        bytes_text = self.pad(bytes_text)

        # process the text in blocks of 64 bits
        for i in range(0, len(bytes_text), self.block_size):
            w = []
            # cut the block in 16 chunks of 4 bytes
            for t in range(16):
                w.append(bytes_text[i*self.block_size: (i+1)*self.block_size][t*4:(t+1)*4])
            # => extend it to 80 chunks
            for t in range(16, 80):
                # w[t] = w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16]
                w.append(bytearray_xor(bytearray_xor(bytearray_xor(w[t-3], w[t-8]), w[t-14]), w[t-16]))

            # initialize hash value for this block
            a = self.h[0]
            b = self.h[1]
            c = self.h[2]
            d = self.h[3]
            e = self.h[4]

            # main loop
            for i in range(80):
                if i <= 19:
                    f = (b and c) or ((not b) and d)
                    k = 0x5A827999
                elif i <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif i <= 59:
                    f = (b and c) or (b and d) or (c and d)
                    k = 0x8F1BBCDC
                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = (rotl(a, 5)) + f + e + k + int.from_bytes(w[i], byteorder='big')
                e = d
                d = c
                c = rotl(b, 30)
                b = a
                a = temp

            # add the block hash to the result
            self.h[0] += a
            self.h[1] += b
            self.h[2] += c
            self.h[3] += d
            self.h[4] += e
