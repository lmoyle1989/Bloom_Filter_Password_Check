# Program:      Bloom Filter Demonstration
# Author:       Lucas Moyle
# Date:         10/31/2021
# Description:  This program demonstrates a basic bloom filter for the use of determining if a given word/password
#               is present in the provided dictionary file. The user can selected a desired false positive rate and
#               the program will calculate the other necessary parameters for the filter to achieve that.
#               The program can be used to test individual words input at the command line by running it with no
#               other command line arguments. The program can also be used to check a list of input words and
#               generate and output file by adding the input file path as the first and only argument.
#               Any other hash functions can be used but they will make it very slow.

import sys
import bitarray
import math

class BloomFilter:
    
    # Our constructor, takes the desired false positive rate from the user and then calculates the number of
    # hashes and bit array size necessary to achieve a false positive rate as close as possible to the input.
    # Math was found here: https://corte.si/posts/code/bloom-filter-rules-of-thumb/
    def __init__(self, fp_rate):
        # If you want to use a different input set, the file and encoding will need to be set here.
        self.input_file_name = './dictionary.txt'
        self.input_file_encoding = 'iso-8859-1'
        self.bits_per_word = max(1, int(math.log(1 / fp_rate) / ((math.log(2)) ** 2)))
        self.no_of_hashes = max(1, int(0.7 * self.bits_per_word))
        self.actual_fp_rate = 1 / (math.e ** (self.bits_per_word * ((math.log(2)) ** 2)))
        self.bit_array = self.build_bit_array()
        self.bit_array_size = len(self.bit_array)

        print('bloom filter created')
        print('desired false positive rate: ' + str(fp_rate))
        print('bits per input word: ' + str(self.bits_per_word))
        print('hashes: ' + str(self.no_of_hashes))
        print('actual false positive rate: ' + str(self.actual_fp_rate))
        

    # Returns the position in the bit array of size 'array_size' by hashing the input and then modding it to
    # the array size.
    def get_bit_position(self, input, array_size):
        bit_position = hash(input) % array_size
        return bit_position


    # Sets up the bit array when the BloomFilter object is instantiated. Simulates multiple hash functions
    # by appending a increasing integer to the front of the string before hashing. So if we are using 3
    # hashes and the input string is 'Hello World', it would get hashed 3 times using the same hash function
    # as '0Hello World', '1Hello World', '2Hello World' and the bit positive of each added to the bit array.
    def build_bit_array(self):
        input_file = open(self.input_file_name, 'r', encoding = self.input_file_encoding)
        input_lines = input_file.readlines()
        no_of_lines = len(input_lines)
        array_size = self.bits_per_word * no_of_lines
        my_array = bitarray.bitarray(array_size)
        my_array.setall(0)
        for word in input_lines:
            for i in range(self.no_of_hashes):
                salted_input = str(i) + word.rstrip('\n')
                bit_position = self.get_bit_position(salted_input, array_size)
                my_array[bit_position] = 1
        input_file.close()
        return my_array


    # Checks if the generated bits for a test word are in the bit array of the BloomFilter class.
    # Appends an increasing integer to the front of the test word for each hash, the same way as
    # the build_bit_array function above. If any of the bits are 0, we know that the word is not
    # in the list. If all the bits are 1, we have a candidate that is most likely in the list, but
    # could be a false positive.
    def check_word(self, input_word):
        bit_list = []
        for i in range(self.no_of_hashes):
            salted_word = str(i) + input_word.rstrip('\n')
            bit_position = self.get_bit_position(salted_word, self.bit_array_size)
            bit_list.append(self.bit_array[bit_position])
        if 0 in bit_list:
            return 'no'
        else:
            return 'maybe'


    # Using the check_word function, takes an input file with a test word on each line and creates
    # an output file with 'no' and 'maybe' on corresponding lines.
    def check_list_of_words(self, test_file_name):
        test_file = open(test_file_name, 'r', encoding = self.input_file_encoding)
        output_file_name = "output_" + test_file_name
        output_file = open(output_file_name, 'w')
        test_file_lines = test_file.readlines()
        for word in test_file_lines:
            output_file.write(self.check_word(word.rstrip('\n')) + '\n')
        output_file.close()
        test_file.close()


if __name__ == '__main__':

    fp_rate = input('enter desired false positive rate (e.g. "0.05" = 5%): ')
    print('generating bloom filter...')
    my_bloom = BloomFilter(float(fp_rate))
    
    if len(sys.argv) >= 2:
        print('generating output file...')
        my_bloom.check_list_of_words(sys.argv[1])
        print('done')
    else:
        while True:
            test_word = input('enter word to test ("q" to exit): ')
            if test_word == 'q':
                print("goodbye")
                break
            print(my_bloom.check_word(test_word))
