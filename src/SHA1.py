#!/usr/bin/env python3

""" This module contains the SHA1 class
"""

from src._functions import rotl

class SHA1(object):
    """ SHA 1 hash algorithm implementation

        Attributes:
            block_size -- int -- block size, in bytes
            h -- list -- hash variables
    """

    def __init__(self):
        self.mask = 0xffffffff
        self._H = [0x67452301,
                   0xEFCDAB89,
                   0x98BADCFE,
                   0x10325476,
                   0xC3D2E1F0]

    @staticmethod
    def _padding(stream):
        """
            If the number of bits is not a multiple of 512, add some padding:
                - add '1' at the end of the text
                - fill with '0' (but let 64 bits available at the end)
                - the 64 last bits are the length of the original text

            Args:
                stream -- bytearray -- the stream to hash

            return stream, padded if needed
        """
        if len(stream) % 64 == 0:
            return stream

        # get the original length in hexadecimal and split it in 8 bytes (list of 8 bytes)
        original_length = [int((hex(len(stream)*8)[2:]).rjust(16, '0')[i:i+2], 16)
                           for i in range(0, 16, 2)]


        stream += bytes([0b10000000])
        # add k*'0', with len(stream) + k = 56 (mod 64)
        # to let 8 bytes (64 bits) for original length
        stream += bytes(((56 - len(stream)) % 64))
        stream += bytes(original_length)

        return stream

    @staticmethod
    def _prepare(stream):
        """
            Cut the stream in blocks of 64 bytes, and each block in 16 words
            of 4 bytes

            Args:
                stream -- bytearray -- the stream to hash

            return a list of blocks
        """
        blocks = []
        nb_blocks = len(stream) // 64

        for i in range(nb_blocks):
            temp = []
            for j in range(16):
                # Calculate the value of the word and append it
                value = 0
                for k in range(4):
                    value <<= 8
                    value += stream[i*64 + j*4 + k]
                temp.append(value)
            blocks.append(temp)

        return blocks

    def hash(self, stream):
        """
            Hash the given stream

            Args:
                stream -- string -- the text to hash

            return the 40 bytes digest
        """
        # convert stream to bytes if needed
        stream = bytes(stream, 'utf-8') if isinstance(stream, str) else stream
        # prepare the stream for hashing
        stream = self._prepare(self._padding(stream))

        for block in stream:
            self._process_block(block)

        return self.produce_digest()


    def _process_block(self, block):
        """
            Process the current block and update the hash variable

            Args:
                block -- list of int -- the block to hash
        """
        # => extend the block from 16 to 80 words
        w = block[:]
        for i in range(16, 80):
            w.append(rotl(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]) & self.mask)

        # initialize hash value for this block
        a, b, c, d, e = self._H[:]

        # main loop
        for i in range(80):
            if i <= 19:
                f = (b & c) ^ (~b & d)
                k = 0x5a827999
            elif i <= 39:
                f = b ^ c ^ d
                k = 0x6ed9eba1
            elif i <= 59:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8f1bbcdc
            else:
                f = b ^ c ^ d
                k = 0xca62c1d6

            T = ((rotl(a, 5) + f + e + k + w[i]) & self.mask)
            e = d
            d = c
            c = rotl(b, 30) & self.mask
            b = a
            a = T

        # add the block hash to the result
        self._H[0] = (a + self._H[0]) & self.mask
        self._H[1] = (b + self._H[1]) & self.mask
        self._H[2] = (c + self._H[2]) & self.mask
        self._H[3] = (d + self._H[3]) & self.mask
        self._H[4] = (e + self._H[4]) & self.mask

    def produce_digest(self):
        """ Combine the 5 hash variables to produce the final hash

            return the 160 bits length hash
        """
        # return 5 blocks of 8 hexadecimal digits
        return ''.join([('%08x' % h) for h in self._H])
