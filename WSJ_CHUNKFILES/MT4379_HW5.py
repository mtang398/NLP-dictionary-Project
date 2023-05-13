import os
import sys
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Define paths for data files
current_directory = os.getcwd()
train_file_path = os.path.join(current_directory, "WSJ_02-21.pos-chunk")
dev_file_path = os.path.join(current_directory, "WSJ_24.pos")
answer_key_path = os.path.join(current_directory, "WSJ_24.pos-chunk")
test_input_path = os.path.join(current_directory, "WSJ_23.pos")

# Initialize variables for storing previous words and their POS tags
prev_word = ""
prev_pos = ""
prev_bio = "@@"
pre_prev_word = ""
pre_prev_pos = ""

# Function to write test output with features
def write_test_output(output, word, pos, prev_word, prev_pos, prev_bio,
                      pre_prev_word, pre_prev_pos, next_word, next_pos,
                      next_next_word, next_next_pos):
    output.write(f"{word}\tPOS={pos}")
    if prev_pos:
        output.write(f"\tPrevious_Pos={prev_pos}")
    if prev_word:
        output.write(f"\tPrevious_Word={prev_word}")
    if prev_bio:
        output.write(f"\tPrevious_Bio={prev_bio}")
    if pre_prev_word:
        output.write(f"\tPrevious_two_word={pre_prev_word}")
    if pre_prev_pos:
        output.write(f"\tPrevious_two_pos={pre_prev_pos}")
    if next_word:
        output.write(f"\tNext_word={next_word}")
    if next_pos:
        output.write(f"\tNext_pos={next_pos}")
    if next_next_word:
        output.write(f"\tNext_two_word={next_next_word}")
    if next_next_pos:
        output.write(f"\tNext_two_pos={next_next_pos}")
    output.write("\n")
    
# Function to write output with features and BIO tags
def write_output(output, word, pos, bio, prev_word, prev_pos, prev_bio,
                 pre_prev_word, pre_prev_pos, next_word, next_pos,
                 next_next_word, next_next_pos):
    output.write(f"{word}\tPOS={pos}")
    if prev_pos:
        output.write(f"\tPrevious_Pos={prev_pos}")
    if prev_word:
        output.write(f"\tPrevious_Word={prev_word}")
    if prev_bio:
        output.write(f"\tPrevious_Bio={prev_bio}")
    if pre_prev_word:
        output.write(f"\tPrevious_two_word={pre_prev_word}")
    if pre_prev_pos:
        output.write(f"\tPrevious_two_pos={pre_prev_pos}")
    if next_word:
        output.write(f"\tNext_word={next_word}")
    if next_pos:
        output.write(f"\tNext_pos={next_pos}")
    if next_next_word:
        output.write(f"\tNext_two_word={next_next_word}")
    if next_next_pos:
        output.write(f"\tNext_two_pos={next_next_pos}")
    if bio:
        output.write(f"\t{bio}")
    output.write("\n")

#__________________________________________________________________________

def write_features(input_path, output_path, mode):
    # Initialize variables for storing previous words and their POS tags
    prev_word = ""
    prev_pos = ""
    prev_bio = "@@"
    pre_prev_word = ""
    pre_prev_pos = ""

    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        lines = input_file.readlines()

        for i in range(len(lines)):
            if lines[i] == '\n':
                output_file.write('\n')
                prev_word = 'empty'
                prev_pos = 'empty'
                if mode == 'train':
                    prev_bio = '@@'
            else:
                # Get current word, POS tag, and BIO tag (if in 'train' mode)
                if mode == 'train':
                    curr_word, curr_pos, curr_bio = lines[i].strip().split('\t')[:3]
                elif mode == 'test':
                    curr_word, curr_pos = lines[i].strip().split('\t')[:2]

                # Get next word and its POS tag
                if i >= len(lines) - 1 or lines[i + 1] == '\n':
                    next_word, next_pos = ('empty', 'empty')
                else:
                    next_word, next_pos = lines[i + 1].strip().split('\t')[:2]

                # Get previous to previous word and its POS tag
                if i < 2 or lines[i - 2] == '\n':
                    pre_prev_word, pre_prev_pos = ('empty', 'empty')
                else:
                    pre_prev_word, pre_prev_pos = lines[i - 2].strip().split('\t')[:2]

                # Get next to next word and its POS tag
                if i >= len(lines) - 2 or lines[i + 2] == '\n':
                    next_next_word, next_next_pos = ('empty', 'empty')
                else:
                    next_next_word, next_next_pos = lines[i + 2].strip().split('\t')[:2]

                if mode == 'train':
                    write_output(output_file, curr_word, curr_pos, curr_bio, prev_word, prev_pos, prev_bio,
                                 pre_prev_word, pre_prev_pos, next_word, next_pos, next_next_word, next_next_pos)
                    prev_bio = curr_bio
                elif mode == 'test':
                    write_test_output(output_file, curr_word, curr_pos, prev_word, prev_pos, prev_bio,
                                      pre_prev_word, pre_prev_pos, next_word, next_pos, next_next_word, next_next_pos)

                prev_word = curr_word
                prev_pos = curr_pos

# Call the function with appropriate input_path, output_path, and mode
write_features(train_file_path, 'training.feature', 'train')
write_features(test_input_path, 'test.feature', 'test')
