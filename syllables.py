# python2

from hyphen.dictools import *
from hyphen import Hyphenator
import nltk
import re
import string
import numpy as np
import matplotlib.pyplot as plt

# lines enjambed vs stanzas enjambed - done
# enjambment over the course of the poem, so a graph,
# say, of where enjambment tends to occur. done
# a sense of where enjambment tends to happen in each stanza, which i can
# measure by doing that for each stanza and averaging the findings.
# the last two done for each particular punctuation mark


def get_text():
    """Read in a text from a filename."""
    filename = text = 'omeros.txt'
    with open(filename, 'r') as fin:
        text = fin.read()
    return text


def install_stuff_for_hyphenator():
    for lang in ['de_DE', 'en_US']:
        if not is_installed(lang): install(lang)


def remove_header_and_backmatter(text):
    """removes the header information and pre-text stuff"""
    return text[181:-78]


def get_chapter_indices(raw_text):
    chapter_indices = []
    for index, line in enumerate(raw_text):
        text_search = re.search(
            'Chapter M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})',
            line)
        # print(text_search)
        if text_search:
            chapter_indices.append(index)
    return chapter_indices


def get_text_by_chapters(raw_text, chapter_indices):
    text_broken_by_chapters = []
    for index, _ in enumerate(chapter_indices):
        if index < 63:
            start = chapter_indices[index]
            end = chapter_indices[index + 1]
            new_text = raw_text[start:end]
            text_broken_by_chapters.append(new_text)
        else:
            text_broken_by_chapters.append(raw_text[chapter_indices[index]:])
    return text_broken_by_chapters


def chunk_text(raw_text):
    """"take a text that has been split into lines and return chunks,
    so preserving the cantos and the"""
    # first regex to break at Chapter Number, second at I II or III

    chapter_indices = get_chapter_indices(raw_text)
    text_broken_by_chapters = get_text_by_chapters(raw_text, chapter_indices)
    cleaned_segmented_text = []
    chapter_split_indices = []
    for chapter in text_broken_by_chapters:
        indices = []
        for index, line in enumerate(chapter):
            if line in ['I', 'II', 'III']:
                indices.append(index)
        chapter_split_indices.append(indices)
    for index, list_of_indices in enumerate(chapter_split_indices):
        first_chunk = text_broken_by_chapters[index][
            list_of_indices[0]:list_of_indices[1]]
        second_chunk = text_broken_by_chapters[index][
            list_of_indices[1]:list_of_indices[2]]
        third_chunk = text_broken_by_chapters[index][list_of_indices[2]:]
        cleaned_segmented_text.append([first_chunk,
                                       second_chunk, third_chunk])
    return cleaned_segmented_text


def clean_empty_cells(text):
    """Takes a text and cleans the empty cells."""
    result = []
    for line in text:
        if line:
            result.append(line)
    return result


def count_enjambment(chunked_text):
    endstopped_lines_count = 0
    enjambed_lines_count = 0
    endstopped_cantos_count = 0
    enjambed_cantos_count = 0
    total_lines = 0
    total_cantos = 0
    line_endings_dict = {}
    canto_endings_dict = {}
    for chapter in chunked_text:
        for canto_index, canto in enumerate(chapter):
            for line_index, line in enumerate(canto):
                if line[-1] not in string.punctuation:
                    enjambed_lines_count += 1
                else:
                    if line[-1] in line_endings_dict:
                        line_endings_dict[line[-1]] += 1
                    else:
                        line_endings_dict[line[-1]] = 1
                    endstopped_lines_count += 1
                if line_index == len(canto) - 1 and line[-1] \
                        not in string.punctuation:
                    enjambed_cantos_count += 1
                elif line_index == len(canto) - 1:
                    if line[-1] in canto_endings_dict:
                        canto_endings_dict[line[-1]] += 1
                    else:
                        canto_endings_dict[line[-1]] = 1
                    endstopped_cantos_count += 1
                total_lines += 1
            total_cantos += 1
    print('Note - these are the things the script is recognizing as counting as an endstop. Would need to massage based on what Caleb wants: ' + str(string.punctuation))
    print('Endstopped lines: ' + str(endstopped_lines_count) +
          '/' + str(total_lines))
    print('Enjambed lines: ' + str(enjambed_lines_count) + '/' +
          str(total_lines))
    print('"Endstopped" Line endings count by punctuation: ')
    for key in line_endings_dict:
        print(key + ': ' + str(line_endings_dict[key]))
    print('Endstopped cantos: ' + str(endstopped_cantos_count) +
          '/' + str(total_cantos))
    print('Enjambed cantos: ' + str(enjambed_cantos_count) +
          '/' + str(total_cantos))
    print('Endstopped Canto endings count by punctuation: ')
    for key in canto_endings_dict:
        print(key + ': ' + str(canto_endings_dict[key]))


def reduce_text_to_line_endings(chunked_text):
    text_with_only_line_endings = []
    canto_endings = []
    for chapter in chunked_text:
        for canto_index, canto in enumerate(chapter):
            for line_index, line in enumerate(canto):
                if line[-1] in string.punctuation:
                    # it must end in punctuation, so build up a list of only the line endings.
                    text_with_only_line_endings.append(line[-1])
                else:
                    # if enjambed, just put a space
                    text_with_only_line_endings.append(" ")
                if line_index == len(canto) - 1 and line[-1] \
                        in string.punctuation:
                        canto_endings.append(line[-1])
                elif line_index == len(canto) - 1 and line[-1] \
                        not in string.punctuation:
                        canto_endings.append(" ")
    return text_with_only_line_endings, canto_endings


def graph_punctuation_endings_whole_poem():
    pass


def graph_punctuation_endings_for_internal_cantos():
    pass


def count_syllables(chunked_text):
    h_en = Hyphenator()
    for chapter in chunked_text:
        for canto in chapter:
            for line in canto:
                syllables = []
                for word in nltk.word_tokenize(unicode(line, 'utf-8')):
                    count = h_en.syllables(word)
                    syllables.append(len(count))
                print('=====')
                print(line)
                print(sum(syllables))


def get_frequencies_of_a_punctuation(line_endings, punct):
    """Takes a list of line endings and a single punctuation character. returns 0's if the character is not in that index position. 1 if it is."""
    np_array = np.array(line_endings)
    as_num = np_array == punct
    return list(as_num.astype(int))


def bin_data(frequencies, bin_count):
    bins = range(1, bin_count)
    total_words = len(frequencies)
    bin_size = total_words / bin_count
    binned_frequencies = []
    for current_bin in bins:
        start = bin_size * (current_bin - 1)
        end = bin_size * current_bin
        binned_frequencies.append(sum(frequencies[start:end]))
    return binned_frequencies


def plot_the_thing(data, punct):
    fig = plt.figure()
    ax = plt.axes()
    y = data
    x = range(0, len(data))
    ax.set(title="Frequencies of cantos ending in " + punct + " over time in Omeros")
    ax.plot(x, y)
    plt.savefig('results/' + punct + '.png')

    # plt.savefig('results/1.png')

def average_by_stanza(data):
    # average data is wonky - try to copy bin_data above
    """take the data that we have, and average it."""
    averaged_data = []
    total_stanzas = 192
    bins = range(1, total_stanzas)
    bin_size = len(data) / total_stanzas
    for chunk in bins:
        start = bin_size * (chunk - 1)
        end = bin_size * chunk
        this_chunk = data[start:end]
        print(start)
        print(end)
        print(this_chunk)
        print(len(this_chunk))

        average_for_this_chunk = sum(this_chunk) / len(this_chunk)
        averaged_data.append(average_for_this_chunk)
    print(averaged_data)


def main():
    # install_stuff_for_hyphenator()
    text = remove_header_and_backmatter(get_text().split('\n'))
    text = clean_empty_cells(text)
    chunked_text = chunk_text(text)
    # count_syllables(chunked_text)
    line_endings, canto_endings = reduce_text_to_line_endings(chunked_text)

    potential_endings = string.punctuation + ' '
    print(potential_endings)
    print(len(canto_endings))
    for punct in potential_endings:
        print(punct)
        np_array = get_frequencies_of_a_punctuation(line_endings, punct)
        binned_data = bin_data(np_array, 192)
        print(average_by_stanza(binned_data))
        # plot_the_thing(binned_data, punct)
    # fd.plot()


if __name__ == "__main__":
    main()
