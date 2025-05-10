# Module for text statistics (Task 2)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 24.10.2023

import re

def get_letters(word):
    """
    Extract only letters from a word.
    Args:
        word: Input word
    Returns:
        String containing only letters
    """
    return ''.join(c for c in word if c.isalpha())

def count_sentences(text):
    """
    Count total sentences and classify them by type.
    Args:
        text: Input text
    Returns:
        Tuple of (total, narrative, interrogative, imperative)
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    total = len(sentences)
    narrative = sum(1 for s in sentences if s.endswith('.'))
    interrogative = sum(1 for s in sentences if s.endswith('?'))
    imperative = sum(1 for s in sentences if s.endswith('!'))
    return total, narrative, interrogative, imperative

def average_sentence_length(text):
    """
    Calculate average sentence length in characters (only words).
    Args:
        text: Input text
    Returns:
        Average length as float
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 0
    lengths = []
    for sentence in sentences:
        words = sentence.split()
        total_letters = sum(len(get_letters(word)) for word in words)
        lengths.append(total_letters)
    return sum(lengths) / len(lengths)

def average_word_length(text):
    """
    Calculate average word length in characters (only letters).
    Args:
        text: Input text
    Returns:
        Average length as float
    """
    words = text.split()
    letter_lengths = [len(get_letters(word)) for word in words if get_letters(word)]
    if not letter_lengths:
        return 0
    return sum(letter_lengths) / len(letter_lengths)

def count_smileys(text):
    """
    Count smileys in the text based on the defined pattern.
    Args:
        text: Input text
    Returns:
        Number of smileys
    """
    smiley_pattern = r'[;:]-*\(+|[;:]-*\)+|[;:]-*\[+|[;:]-*\]+'
    smileys = re.findall(smiley_pattern, text)
    return len(smileys)