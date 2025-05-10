# Module for email parsing (Task 2)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 24.10.2023

import re

def extract_emails_and_names(text):
    """
    Extract email addresses and corresponding names from the text.
    Args:
        text: Input text
    Returns:
        List of tuples containing (name, email)
    """
    pattern = r'([^<]+)\s<([^>]+)>'
    matches = re.findall(pattern, text)
    return matches