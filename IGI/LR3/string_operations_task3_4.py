# Module for string operations (Tasks 3 and 4)
# Lab Work #3
# Developer: Valiulin Konstantin
# Date: 24.04.2025

def is_hexadecimal(s):
    """
    Check if the string is a hexadecimal number.
    Args:
        s (str): Input string
    Returns:
        bool: True if hexadecimal, False otherwise
    """
    if not s:
        return False
    hex_digits = set("0123456789abcdefABCDEF")
    return all(char in hex_digits for char in s)

def analyze_text():
    """
    Analyze the predefined text string according to Task 4 requirements.
    Returns:
        None (prints results)
    """
    text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, "
            "whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, "
            "when suddenly a White Rabbit with pink eyes ran close by her.")
    
    # Split into words (removing commas)
    words = [word.strip(',') for word in text.split()]
    
    # a) Count words and list those with even letter count
    total_words = len(words)
    even_length_words = [word for word in words if len(word) % 2 == 0]
    print(f"a) Total number of words: {total_words}")
    print(f"Words with even number of letters: {', '.join(even_length_words)}")
    
    # b) Find shortest word starting with 'a'
    a_words = [word for word in words if word.lower().startswith('a')]
    shortest_a_word = min(a_words, key=len) if a_words else "None"
    print(f"b) Shortest word starting with 'a': {shortest_a_word}")
    
    # c) Find and print repeated words
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    repeated_words = [word for word, count in word_count.items() if count > 1]
    print(f"c) Repeated words: {', '.join(repeated_words) if repeated_words else 'None'}")