import fileinput
import os
from collections import defaultdict
import re
import numpy as np
from collections import Counter

cwd = os.getcwd()
train_file = os.path.join(cwd, 'WSJ_02-21.pos')
development_file = os.path.join(cwd, 'WSJ_24.pos')
development_test_file = os.path.join(cwd, 'WSJ_24.words')
test_file = os.path.join(cwd, "WSJ_23.words")
scoring_file = os.path.join(cwd, "score.py")
output_file = os.path.join(cwd, "submission.pos")

# Open and merge the POS tagged files
with open(train_file, "r") as f1, open(development_file, "r") as f2, open("corpus.pos", "w") as out_file:
    out_file.writelines(line for file in (f1, f2) for line in file)

train_set = ("corpus.pos")
test_set = open(test_file, "r").readlines()

word_count = {}
# Count the occurrences of each word in the training set
for line in fileinput.input(files=train_set):
    if not (split := line.split()):
        continue
    word, tag = split[0], split[1]
    word_count[word] = word_count.get(word, 0) + 1

single_word = {}
multiple_words = {}
# Separate words into single_word and multiple_words dictionaries
single_word = {word: {} for word, count in word_count.items() if count == 1}
multiple_words = {word: {} for word, count in word_count.items() if count > 1}

def fill_likelihood_table(train_set, single_word):
    likelihood_table = defaultdict(lambda: defaultdict(int))
    for line in fileinput.input(files=train_set):
        if not (split := line.split()):
            continue
        word, tag = split[0], split[1]
        likelihood_table[tag]['UNKNOWN_WORD' if word in single_word else word] += 1
    return likelihood_table


def create_transition_table(train_set):
    transition_table = defaultdict(lambda: defaultdict(int))
    prev_tag = 'Begin_Sent'
    for line in fileinput.input(files=train_set):
        if not (split := line.split()):
            transition_table[prev_tag]['End_Sent'] += 1
            prev_tag = 'Begin_Sent'
        else:
            tag = split[1]
            transition_table[prev_tag][tag] += 1
            prev_tag = tag
    return transition_table


def calculate_probabilities(table):
    prob_table = {}
    for key, sub_dict in table.items():
        total = sum(sub_dict.values())
        prob_table[key] = {sub_key: float(value) / total for sub_key, value in sub_dict.items()}
    return prob_table


def split_test_set(test_set):
    sentence = []
    sentences = []
    for line in test_set:
        split = line.split()
        if not split:
            sentences.append(sentence)
            sentence = []
        else:
            sentence.append(split[0])
    return sentences

# Call the functions
likelihood_table = fill_likelihood_table(train_set, single_word)
transition_table = create_transition_table(train_set)
likelihood_prob_table = calculate_probabilities(likelihood_table)
transition_prob_table = calculate_probabilities(transition_table)
sentences = split_test_set(test_set)

#----------------------------------------------------------------------------------------------

all_tags_of_all_sentences = []


def oov_prob(tag, word):
    if tag in likelihood_prob_table and 'UNKNOWN_WORD' in likelihood_prob_table[tag]:
        return likelihood_prob_table[tag]['UNKNOWN_WORD']
    else:
        return 0


def viterbi_algo(sentence):
    test_sentence = sentence
    num_of_cols = len(test_sentence) + 2
    num_of_rows = len(likelihood_table.keys()) + 2
    viterbi = [[0 for i in range(num_of_cols)] for i in range(num_of_rows)]
    viterbi[0][0] = 1
    all_keys = list(likelihood_table)
    all_keys.insert(0, 'Begin_Sent')
    all_keys.append('End_Sent')

    # Initialize the first column of the Viterbi table
    for i in range(0, num_of_rows):
        current_word = test_sentence[0]
        current_tag = all_keys[i]
        if current_word in multiple_words and current_tag in transition_prob_table['Begin_Sent'] and current_word in likelihood_prob_table[current_tag]:
            prob = transition_prob_table['Begin_Sent'][current_tag] * likelihood_prob_table[current_tag][current_word]
            viterbi[i][1] = prob
        elif current_word not in multiple_words and current_tag in transition_prob_table['Begin_Sent'] and 'UNKNOWN_WORD' in likelihood_prob_table[current_tag]:
            prob = transition_prob_table['Begin_Sent'][current_tag] * likelihood_prob_table[current_tag]['UNKNOWN_WORD']
            viterbi[i][1] = prob

    # Fill in the rest of the Viterbi table
    for i in range(2, num_of_cols - 1):
        current_word = test_sentence[i - 1]
        for j in range(1, num_of_rows):
            current_col_tag = all_keys[j]
            likelihood_in_state = 0
            if current_word in multiple_words:
                if current_col_tag != 'End_Sent' and current_word in likelihood_prob_table[current_col_tag]:
                    likelihood_in_state = likelihood_prob_table[current_col_tag][current_word]
            else:
                likelihood_in_state = oov_prob(current_col_tag, word)
            max_probability = 0
            for jj in range(1, num_of_rows):
                prev_col_tag = all_keys[jj]
                tp = transition_prob_table[prev_col_tag][current_col_tag] if prev_col_tag != 'End_Sent' and current_col_tag in transition_prob_table[prev_col_tag] else 0
                prev_score = viterbi[jj][i - 1]
                total_prob = likelihood_in_state * tp * prev_score
                if total_prob > max_probability:
                    max_probability = total_prob
            viterbi[j][i] = max_probability

    # Extract the most likely sequence of tags
    tag_sequence = []
    for c in range(num_of_cols - 1):
        max_probability = 0
        max_probability_tag = ''
        for r in range(num_of_rows):
            if viterbi[r][c] > max_probability:
                max_probability = viterbi[r][c]
                max_probability_tag = all_keys[r]
        tag_sequence.append(max_probability_tag)
    tag_sequence.append('End_Sent')
    return tag_sequence

submission = open("submission.pos", "w")
temp = []
counter = 0

# Apply the Viterbi algorithm to each sentence and write the results to the submission file
for s in sentences:
    tags = viterbi_algo(s)
    for i in range(len(s)):
        line = s[i] + "\t" + tags[i + 1] + '\n'
        submission.write(line)
    submission.write("\n")

