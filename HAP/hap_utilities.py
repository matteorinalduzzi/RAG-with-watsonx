# hap_utilities.py>

# Helper functions
import nltk
from nltk.tokenize import sent_tokenize, regexp_tokenize

# Ensure you have the required NLTK data
nltk.download('punkt')

def split_text_preserve_newlines(text):
    """
    Split the given text into sentences while preserving newlines.
    1. Splits the text into paragraphs based on double newlines (\n\n).
    2. Tokenizes each paragraph separately into sentences.
    3. Reassembles the sentences while inserting double newlines between paragraphs.
    
    Args:
    text (str): The input text to split.
    
    Returns:
    List[str]: A list of sentences with preserved newlines.
    """
    # Split text by newline characters first
    paragraphs = text.split('\n\n')
    
    # Tokenize each paragraph separately
    sentences_with_newlines = []
    for para in paragraphs:
        sentences = sent_tokenize(para)
        if sentences:
            # Add newline between paragraphs
            sentences_with_newlines.extend(sentences)
            sentences_with_newlines.append('')  # This will add a '\n\n' in the final text
    
    # Remove the last extra newline added
    if sentences_with_newlines and sentences_with_newlines[-1] == '':
        sentences_with_newlines.pop()
    
    return sentences_with_newlines

def rebuild_text_with_newlines(sentences):
    """
    Rebuild the text from a list of sentences with preserved newlines. Joins sentences back into text, inserting double newlines where appropriate.
    
    Args:
    sentences (List[str]): A list of sentences to join.
    
    Returns:
    str: The rebuilt text with preserved newlines.
    """
    rebuilt_text = ''
    for sentence in sentences:
        if sentence == '':
            rebuilt_text += '\n\n'
        else:
            rebuilt_text += sentence + ' '
    
    return rebuilt_text.strip()


def find_substring_indices(full_strings, substrings):
    """
    Find the indices of substrings within a list of full strings.

    Parameters:
    full_strings (list[str]): A list of full strings to search for substrings.
    substrings (list[str]): A list of substrings to search for within the full strings.

    Returns:
    list[int]: A list of indices corresponding to the full strings that contain at least one substring.
    """
    indices = []
    
    # Iterate through each full string
    for i, full_string in enumerate(full_strings):
        # Check if any of the substrings is found in the current full string
        if any(sub in full_string for sub in substrings):
            indices.append(i)
    
    return indices



# function
def clean_hap_content():
    print( "Geeks 4 Geeks !")