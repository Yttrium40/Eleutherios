import json
import random

import punctuation


markov_dictionary_path = "markov_dictionary.json"
training_file_path = "markov_training.txt"

def load_dictionary():
    try:
        with open(markov_dictionary_path, "r", encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        with open(markov_dictionary_path, "w+", encoding="utf-8") as fp:
            fp.write("{}")
        return {}

def save_dictionary(dictionary):
    with open(markov_dictionary_path, "w", encoding="utf-8") as fp:
        json.dump(dictionary, fp, sort_keys=True, indent=4)

def get_next_block(block, dictionary):
    """Randomly get the next block given the previous block"""
    if dictionary.get(block) is None:
        return ""
    max_rand = 0
    for key in dictionary[block].keys():
        max_rand += dictionary[block][key]
    num = random.uniform(0, max_rand)
    for key in dictionary[block].keys():
        if num < dictionary[block][key]:
            return key
        else:
            num -= dictionary[block][key]

def get_phrase(start, end, append_start, dictionary):
    """Make a phrase with the Markov chain with start and end appended"""
    phrase = ""
    next_block = ""

    # append the start
    if start is not None and start != "":
        if append_start:
            phrase = start

        next_block = start.split(" ")[-1]

    # build the middle
    while True:
        next_block = get_next_block(next_block, dictionary)

        # if end is reached
        if next_block == "" and not phrase == "":
            break
        phrase += " " + next_block

    # append the end
    if end is not None:
        phrase += " " + end

    return phrase.strip()

def learn_phrase(phrase, dictionary):
    def update_block(left, right, dictionary):
        if left == "" and right == "":
            return
        if dictionary.get(left) is None:
            dictionary[left] = {right: 1}
        elif dictionary[left].get(right) is None:
            dictionary[left][right] = 1
        else:
            dictionary[left][right] += 1

    blocks = phrase.split(" ")
    if len(blocks) == 0:
        return

    left_block = ""
    right_block = ""
    length = len(blocks)
    for i in range(length+1):
        if i == length:
            right_block = ""
        else:
            right_block = blocks[i].strip()
        update_block(left_block, right_block, dictionary)
        left_block = right_block

def train_from_file():
    dictionary = load_dictionary()
    with open(training_file_path, "r", encoding="utf-8") as fp:
        for l in fp:
            learn_phrase(l, dictionary)
    save_dictionary(dictionary)

if __name__ == "__main__":
    train_from_file()
