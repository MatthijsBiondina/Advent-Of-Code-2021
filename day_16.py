import time
from copy import copy, deepcopy

import numpy as np
from aocd.models import Puzzle
from tqdm import tqdm
import sys

from tools import pyout

puzzle = Puzzle(day=16, year=2021)

# data = "9C0141080250320F1802104A08"
data = puzzle.input_data

hex2binary = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101',
              '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
              'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
bin2dec = lambda x: int(x, 2)

hex = data
bin = ''.join([hex2binary[h] for h in hex])

version_sum = 0


def decode_packet(binary, read_nr_of_packets=None):
    global version_sum
    literal_values = []
    ii = 0
    packets_found = 0
    while True:
        # the first three bits encode the packet version
        V, ii = bin2dec(binary[ii:ii + 3]), ii + 3
        version_sum += V
        # the next three bits encode the packet type ID
        T, ii = bin2dec(binary[ii:ii + 3]), ii + 3
        if T == 4:
            nrstr = ''
            while True:
                # the binary number is padded with leading zeroes until its length is a multiple of four bits,
                # and then it is broken into groups of four bits.
                five_bits, ii = binary[ii:ii + 5], ii + 5
                nrstr += five_bits[1:]
                # Each group is prefixed by a 1 bit except the last group, which is prefixed by a 0 bit
                if five_bits[0] == '0':
                    break
            literal_value = bin2dec(nrstr)
            literal_values.append(literal_value)
        else:
            # Every other type of packet (any packet with a type ID other than 4) represent an operator
            I, ii = binary[ii], ii + 1
            # An operator packet contains one or more packets. To indicate which subsequent binary data
            # represents its sub-packets, an operator packet can use one of two modes indicated by the
            # bit immediately after the packet header; this is called the length type ID
            if I == '0':
                # If the length type ID is 0, then the next 15 bits are a number that represents the total
                # length in bits of the sub-packets contained by this packet.
                total_length, ii = bin2dec(binary[ii:ii + 15]), ii + 15
                # Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets
                # appear.
                sub_packet, ii = binary[ii:ii + total_length], ii + total_length
                value = decode_packet(sub_packet)
            else:
                # If the length type ID is 1, then the next 11 bits are a number that represents the
                # number of sub-packets immediately contained by this packet.
                nr_of_contained_packets, ii = bin2dec(binary[ii:ii + 11]), ii + 11
                value, bit_read = decode_packet(binary[ii:], nr_of_contained_packets)
                ii += bit_read

            if T == 0:
                literal_values.append(sum(value))
            elif T == 1:
                product = 1
                for v in value:
                    product *= v
                literal_values.append(product)
            elif T == 2:
                literal_values.append(min(value))
            elif T == 3:
                literal_values.append(max(value))
            elif T == 5:
                literal_values.append(int(value[0] > value[1]))
            elif T == 6:
                literal_values.append(int(value[0] < value[1]))
            elif T == 7:
                literal_values.append(int(value[0] == value[1]))



            # pyout()

        packets_found += 1
        if read_nr_of_packets is not None and packets_found == read_nr_of_packets:
            return literal_values, ii

        remainder = binary[ii:]
        if remainder == '0' * len(remainder):
            return literal_values
    return literal_values, ii


output = decode_packet(bin)[0]
puzzle.answer_b = output
pyout(version_sum)

puzzle.answer_a = version_sum

pyout()
