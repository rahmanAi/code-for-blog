import os
import subprocess
from math import log, sqrt
from collections import defaultdict
from string import ascii_lowercase


from process_word_lists.process_word_list import get_word_list
from utils import get_word_counts

VOWELS = 'aeiou'


def get_words_from_unix_dict():
    """ Get list of lowercase words with no hyphens from /usr/share/dict/words. """

    process = subprocess.Popen("cat /usr/share/dict/words".split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode("utf-8")

    words = set(word.lower() for word in output.splitlines() if "-" not in word)
    return words


def get_vowel_variants(words):
    variants = []

    for word in words:
        index = word.find('a')

        if index > -1:
            # Replace the first a with each vowel
            if all(word[:index] + vowel + word[index + 1:] in words for vowel in 'eiou'):
                variants.append(word)

    return variants


def print_longest_variants(variants, offset=0):
    max_length = max(len(word) for word in variants)
    print(max_length)
    print([word for word in variants if len(word) == max_length - offset])


def print_variant_counts(word, word_counts):
    index = word.find('a')
    if index > -1:
        for vowel in VOWELS:
            word = word[:index] + vowel + word[index + 1:]
            print("{}: {}".format(word, word_counts.get(word, 0)))


def get_all_variants_at_each_postion(words):
    variants = dict()
    letter_swaps = defaultdict(list)

    for word in words:
        best_word_list = []

        for index, letter in enumerate(word):
            word_list = []

            for new_letter in ascii_lowercase[ascii_lowercase.index(letter) + 1:]:
                new_word = word[:index] + new_letter + word[index + 1:]
                if new_word in words:
                    word_list.append(new_word)
                    letter_swaps[letter + new_letter].append((word, new_word))

            if len(word_list) > len(best_word_list):
                best_word_list = word_list

        if best_word_list:
            variants[word] = best_word_list

    return variants, letter_swaps


def find_most_swappable_letter(letter_swaps):
    letters = { letter: { 'total': 0} for letter in ascii_lowercase }
    
    for letter_pair, count in letter_swaps.items():
        letters[letter_pair[0]][letter_pair[1]] = count
        letters[letter_pair[1]][letter_pair[0]] = count
        letters[letter_pair[0]]['total'] += count
        letters[letter_pair[1]]['total'] += count

    return letters


def get_all_variants(words):
    variants = dict()

    for word in words:
        word_list = []

        for index, letter in enumerate(word):
            for new_letter in ascii_lowercase:
                if new_letter != letter:
                    new_word = word[:index] + new_letter + word[index + 1:]
                    if new_word in words:
                        word_list.append(new_word)

        variants[word] = word_list

    return variants


def print_most_variants(variants, max_count=-1):
    for index, item in enumerate(sorted(variants.items(), key=lambda item: -len(item[1]))):
        print("{} ({}): {}".format(item[0], len(item[1]), ', '.join(word[0] for word in item[1])))
        if index == max_count:
            break


def get_unswappable_pairs(letter_swaps):
    for i in range(25):
        for j in range(i + 1, 26):
            letter_pair = ascii_lowercase[i] + ascii_lowercase[j]
            if letter_pair not in letter_swaps:
                print(letter_pair)


def print_q_swap_words(letter_swaps):
    q_swaps = ["".join(sorted([letter, 'q'])) for letter in ascii_lowercase]

    for letter_pair in q_swaps:
        if letter_swaps.get(letter_pair):
            print(letter_swaps[letter_pair])


if __name__ == '__main__':
    # Get words
    # words = get_words_from_unix_dict()
    # words = set(get_word_list(os.path.join('word_lists', 'CROSSWD.TXT')))
    # words = set(get_word_list(os.path.join('word_lists', 'COMMON.TXT')))

    word_counts = get_word_counts(os.path.join('word_lists', 'filtered_word_counts.txt'))
    words = set(word_counts.keys())
    total_words = sum(word_counts.values())

    print(len(words))

    # Get vowel variants
    # variants = get_vowel_variants(words)
    # print(variants)
    # print(len(variants))
    # print_longest_variants(variants, 2)

    # print_variant_counts('blander', word_counts)
    # word_log_frequencies = { word: log(count / total_words) for word, count in word_counts.items() }

    # Get all variants
    variants, letter_swaps = get_all_variants_at_each_postion(words)
    # variants = get_all_variants(words)
    # print_most_variants(variants, 12)
    print(len(variants.keys()))
    print_longest_variants(variants)
    print(variants['counterterrorism'])

    #  TODO show longest variants
    #   show words with the most variants
    #   show longest words that have a variant at each of its positions

    # Number of letter pairs that can be swapped (out of a possible 325 (25 * 26  /2))
    # print(len(list(letter_swaps.keys())))

    # get_unswappable_pairs(letter_swaps.keys())
    # print_q_swap_words(letter_swaps)

    # Find most common letter swaps
    # for letter_pair, variants in sorted(letter_swaps.items(), key=lambda item: -len(item[1]))[:10]:
    #     variant_counts = { (word_1, word_2): word_counts[word_1] * word_counts[word_2] for word_1, word_2 in variants }
    #     most_common_count = max(variant_counts.values())
    #     most_common_variant = [word for word, count in variant_counts.items() if count == most_common_count][0]
    #     # freq = "{0:.2f}%".format(100 * sqrt(most_common_count) / total_words)
    #     freq = "{0:.2f}%, {1:.2f}%".format(100 * word_counts[most_common_variant[0]] / total_words,
    #                                        100 * word_counts[most_common_variant[1]] / total_words)

    #     print("<tr>")
    #     print(f"\t<td>{ letter_pair[0] } - { letter_pair[1] }</td>")
    #     print(f"\t<td>{ len(variants) }</td>")
    #     print(f"\t<td>{ ', '.join(most_common_variant) }</td>")
    #     print(f"\t<td>{ freq }</td>")
    #     print("</tr>")

    # Find letters that can be swapped most
    # letter_swap_counts = find_most_swappable_letter(letter_swaps)

    # for letter, counts in sorted(letter_swap_counts.items(), key=lambda item: -item[1]['total']):
    #     print(letter, counts['total'])
