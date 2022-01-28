Lucas Moyle
README file for bloom.py and bloom_sha1.py

1. Use requirements.txt to install the necessary modules, bitarray and pycryptodome.

2. Ensure the provided dictionary.txt file is in the same directory with the python scripts.

3. The program can be used in 2 ways (no input file or with an input file)-

Method 1 - Run with the command 'python3 bloom.py' (no arguments) for the program to run in interface mode. The program will ask the user
for a desired false positive rate. There is no input validation here so the input is a float the corresponds to the
probability of a false positive (example- 0.05 = 5% false positive rate)
The program will prompt the user to input individual test words and use the bloom filter to see if they are already 
in the dictionary.txt list. Output of 'maybe' for a word that is likely in the list, 'no' for a string that is
guaranteed to not be in the list. Type 'q' to exit.

Method 2 - Run the program with an additional command line argument. Use the command 'python3 bloom.py "input_file"' 
where input_file is the path to a list of words to test, formatted with each word to test on a new line. 
The program will generate an output file in the same directory with each line of the output file corresponding to
a line from the input file that will either say 'maybe' or 'no'.

4. If a different dictionary file is desired, it can be changed in the __init__ function in bloom.py. 
Ensure that encoding is also specified. As it is written for submission, the program will always use a file
name 'dictionary.txt' in the same directory encoded in the iso-8859-1 format.
 

