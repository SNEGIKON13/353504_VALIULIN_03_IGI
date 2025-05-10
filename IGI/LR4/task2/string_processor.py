# Module for string processing (Task 2)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 24.10.2023

import re
from collections import Counter

def replace_v_patterns(text):
    """
    Replace all fragments of the form $v_(i)$ with v[i], where i is a single digit or letter.
    Args:
        text: Input text
    Returns:
        Modified text
    """
    pattern = r'\$v_\(([a-zA-Z0-9])\)\$'  # Corrected pattern with capturing group
    replacement = lambda m: f"v[{m.group(1)}]"
    modified_text = re.sub(pattern, replacement, text)
    return modified_text

def get_letters(word):
    """
    Extract only letters from a word.
    Args:
        word: Input word
    Returns:
        String containing only letters
    """
    return ''.join(c for c in word if c.isalpha())

def find_words_with_odd_letters(text):
    """
    Find words with an odd number of letters.
    Args:
        text: Input text
    Returns:
        List of words with odd letter counts
    """
    words = text.split()
    odd_words = [word for word in words if len(get_letters(word)) % 2 == 1]
    return odd_words

def find_shortest_word_starting_with_i(text):
    """
    Find the shortest word starting with 'i' (case-insensitive).
    Args:
        text: Input text
    Returns:
        Shortest word starting with 'i' or None if not found
    """
    words = text.split()
    i_words = [word for word in words if word.lower().startswith('i')]
    if not i_words:
        return None
    shortest = min(i_words, key=len)
    return shortest

def find_duplicate_words(text):
    """
    Find words that appear more than once in the text.
    Args:
        text: Input text
    Returns:
        List of duplicate words
    """
    words = text.split()
    word_counts = Counter(words)
    duplicates = [word for word, count in word_counts.items() if count > 1]
    return duplicates