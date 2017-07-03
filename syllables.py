# python2

from hyphen.dictools import *
from hyphen import Hyphenator
import nltk
import re
import string

# preserve the chapter chunks as well as the cantos, so should be 192 segments

# count the number of lines that end with punctuation
# and the kinds they end with.


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
    line_enjamb_dict = {}
    canto_enjamb_dict = {}
    for chapter in chunked_text:
        for canto_index, canto in enumerate(chapter):
            for line_index, line in enumerate(canto):
                if line[-1] not in string.punctuation:
                    if line_enjamb_dict
                    line_enjamb_dict[line[-1]] += 1
                    enjambed_lines_count += 1
                else:
                    endstopped_lines_count += 1
                if line_index == len(canto) - 1 and line[-1] \
                        not in string.punctuation:
                    print('====')
                    print(canto_index)
                    print(line_index)
                    print(line)
                    enjambed_cantos_count += 1
                elif line_index == len(canto) - 1:
                    endstopped_cantos_count += 1
                total_lines += 1
            total_cantos += 1
    print('Endstopped lines: ' + str(endstopped_lines_count) +
          '/' + str(total_lines))
    print('Enjambed lines: ' + str(enjambed_lines_count) + '/' +
          str(total_lines))
    print('Endstopped cantos: ' + str(endstopped_cantos_count) +
          '/' + str(total_cantos))
    print('Enjambed cantos: ' + str(enjambed_cantos_count) +
          '/' + str(total_cantos))


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


def main():
    install_stuff_for_hyphenator()
    text = remove_header_and_backmatter(get_text().split('\n'))
    text = clean_empty_cells(text)
    chunked_text = chunk_text(text)
    # count_syllables(chunked_text)
    count_enjambment(chunked_text)


if __name__ == "__main__":
    main()
