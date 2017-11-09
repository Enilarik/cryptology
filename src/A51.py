from LFSR import LFSR
import os
import utils

class A51:

    def __init__(self, key):
        self.key_length = 64
        self.key = [int(b) for b in key]

    def init_lfsr(self):
        """ Init the 3 LFSR with:
            key : 64-bit key
        """

        # create the 3 LFSR
        self.r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
        self.r2 = LFSR(name="R2", length=22, taps=[20, 21], clocking_bit_index=10)
        self.r3 = LFSR(name="R3", length=23, taps=[7, 20, 21, 22], clocking_bit_index=10)

        # introduce the key in the system
        for i in range(self.key_length):
            self.r1.shift(self.r1.feedback() ^ self.key[i])
            self.r2.shift(self.r2.feedback() ^ self.key[i])
            self.r3.shift(self.r3.feedback() ^ self.key[i])

    def output_bit(self):
        """ XOR the ouput bits of the 3 registers
        """
        return self.r1.output_bit() ^ self.r2.output_bit() ^ self.r3.output_bit()

    def gen_sequence(self, l = 114):
        """ Generate a sequence of 'l' bits
            By default, l is 114
        """
        sequence = []
        for i in range(l):
            # check the clocking bit of each register
            # to determine the majority bit
            c = {0:0, 1:0}
            c[self.r1.clocking_bit()] += 1
            c[self.r2.clocking_bit()] += 1
            c[self.r3.clocking_bit()] += 1

            majority_bit = 0 if c[0] > c[1] else 1

            # update LFSR where clocking_bit = majority_bit
            if self.r1.clocking_bit() == majority_bit:
                self.r1.shift()
            if self.r2.clocking_bit() == majority_bit:
                self.r2.shift()
            if self.r3.clocking_bit() == majority_bit:
                self.r3.shift()

            sequence.append(self.output_bit())

        return ''.join([str(b) for b in sequence])

    def run(self, m):
        """ Encrypt/Decrypt an utf-8 encoded string
        """
        # init the 3 lfsr
        self.init_lfsr()
        # use them to encrypt generate a sequence
        # and XOR the generated sequence with the message
        binary_m = utils.utf8_to_binary(m)
        binary_c = utils.binary_xor(binary_m, self.gen_sequence(len(binary_m)))
        return utils.binary_to_utf8(binary_c)

    def encrypt_pgm_asset(self, asset_name, output_name=None):
        if not output_name:
            output_name = 'encrypted_' + asset_name

        input_path = os.path.abspath('assets') + '/'
        input_file = open(input_path + asset_name + '.pgm', 'rb')
        lines = input_file.readlines()

        # file content (to encrypt)
        for i in range(3, len(lines)):
            binary_line = ''.join([utils.decimal_to_binary(n, 8) for n in lines[i]])
            lines[i] = utils.binary_xor(binary_line, self.gen_sequence(len(binary_line)))
            utils.print_loading(i, len(lines) - 3)

        # write result in file
        output_path = os.path.abspath('outputs') + '/'
        output_file = open(output_path + output_name + '.pgm', 'w')
        for i in range(3):
            output_file.write(lines[i].decode("utf-8"))
        for i in range(3, len(lines)):
            line = ''.join([chr(utils.binary_to_decimal(lines[i][j:j+8])) for j in range(0, len(lines[i]), 8)])
            output_file.write(line)

k = "1111000011110000111100001111000011110000111100001111000011110000"
a51 = A51(k)
#alg.encrypt_pgm_asset('lena')
c = a51.run('prudywsh66')
print(c)
m = a51.run(c)
print(m)
