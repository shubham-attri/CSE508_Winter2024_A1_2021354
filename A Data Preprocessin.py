import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Lowercasing
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Remove punctuations
    tokens = [token for token in tokens if token not in string.punctuation]

    # Remove blank space tokens
    tokens = [token for token in tokens if token.strip()]

    # Save preprocessed text
    preprocessed_text = ' '.join(tokens)
    preprocessed_file_path = file_path.replace(dataset_directory, preprocessed_directory)
    os.makedirs(os.path.dirname(preprocessed_file_path), exist_ok=True)

    with open(preprocessed_file_path, 'w', encoding='utf-8') as preprocessed_file:
        preprocessed_file.write(preprocessed_text)

    return preprocessed_text

# List all text files in the dataset directory
dataset_directory = 'text_files'
preprocessed_directory = 'preprocessed_text_files'
text_files = [file for file in os.listdir(dataset_directory) if file.endswith('.txt')]

# Print contents of all files before and after preprocessing
for file_name in text_files:
    file_path = os.path.join(dataset_directory, file_name)
    print(f"\nOriginal content of file: {file_name}")
    with open(file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()
        print(original_text)

    preprocessed_text = preprocess_text(file_path)

    print(f"\nContent of file after preprocessing: {file_name}")
    print(preprocessed_text)



