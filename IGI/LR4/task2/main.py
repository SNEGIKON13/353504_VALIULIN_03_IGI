# Main module for testing (Task 2)
# Lab Work #4
# Developer: Valiulin Konstantin
# Date: 10.05.2025

import os
from file_utils import read_file, write_results
from email_parser import extract_emails_and_names
from string_processor import replace_v_patterns, find_words_with_odd_letters, find_shortest_word_starting_with_i, \
    find_duplicate_words
from text_stats import count_sentences, average_sentence_length, average_word_length, count_smileys
from archiver import create_archive, display_archive_info


def main():
    """
    Main function to orchestrate text analysis and processing.
    """
    while True:
        path = input("Enter the path to the text file: ")
        content = read_file(path)
        if content is None:
            continue

        # Process the text
        emails_and_names = extract_emails_and_names(content)
        modified_content = replace_v_patterns(content)
        odd_words = find_words_with_odd_letters(modified_content)
        shortest_i_word = find_shortest_word_starting_with_i(modified_content)
        duplicates = find_duplicate_words(modified_content)
        total_sentences, narrative, interrogative, imperative = count_sentences(modified_content)
        avg_sent_len = average_sentence_length(modified_content)
        avg_word_len = average_word_length(modified_content)
        smileys = count_smileys(modified_content)

        # Collect individual results
        individual_results = ["Emails and Names:"]
        for name, email in emails_and_names:
            individual_results.append(f"{name} <{email}>")
        individual_results.append("\nModified Text:")
        individual_results.append(modified_content)
        individual_results.append("\nWords with odd letter counts:")
        individual_results.append(', '.join(odd_words) if odd_words else "None")
        individual_results.append(f"\nShortest word starting with 'i': {shortest_i_word if shortest_i_word else 'None'}")
        individual_results.append("\nDuplicate words:")
        individual_results.append(', '.join(duplicates) if duplicates else "None")

        # Collect general results
        general_results = [f"Number of sentences: {total_sentences}", f"Narrative sentences: {narrative}",
                           f"Interrogative sentences: {interrogative}", f"Imperative sentences: {imperative}",
                           f"Average sentence length: {avg_sent_len:.2f}", f"Average word length: {avg_word_len:.2f}",
                           f"Number of smileys: {smileys}"]

        # Display individual results
        for line in individual_results:
            print(line)

        # Save results
        base_name = os.path.splitext(os.path.basename(path))[0]
        individual_results_file = f"individual_results_{base_name}.txt"
        general_results_file = f"general_results_{base_name}.txt"
        write_results(individual_results, individual_results_file)
        write_results(general_results, general_results_file)

        # Archive individual results
        archive_name = f"archive_{base_name}.zip"
        create_archive(individual_results_file, archive_name)
        display_archive_info(archive_name)

        # Ask to repeat
        repeat = input("Do you want to process another file? (yes/no): ").lower()
        if repeat != 'yes':
            break


if __name__ == "__main__":
    main()