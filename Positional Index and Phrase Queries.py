import os
import pickle
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Preprocessing function
def preprocess_text(text):

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

    return tokens

# Create positional index
def create_positional_index(dataset_directory):
    positional_index = {}
    for file_name in os.listdir(dataset_directory):
        file_path = os.path.join(dataset_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = preprocess_text(file.read())
            for position, token in enumerate(tokens):
                if token not in positional_index:
                    positional_index[token] = {}
                if file_name not in positional_index[token]:
                    positional_index[token][file_name] = []
                positional_index[token][file_name].append(position)
    return positional_index

# Load positional index
def load_positional_index(file_path):
    with open(file_path, 'rb') as file:
        positional_index = pickle.load(file)
    return positional_index

# Save positional index
def save_positional_index(positional_index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(positional_index, file)

# Execute phrase queries
def execute_phrase_queries(positional_index, queries):
    results = []
    for query in queries:
        query_terms = preprocess_text(query)
        query_result = set(positional_index[query_terms[0]].keys())
        for term in query_terms[1:]:
            if term in positional_index:
                query_result = query_result.intersection(positional_index[term].keys())
            else:
                query_result = set()
                break
        if query_result:
            final_result = []
            for doc_id in query_result:
                positions = positional_index[query_terms[0]][doc_id]
                for pos in positions:
                    if all(pos + i + 1 in positional_index[term][doc_id] for i, term in enumerate(query_terms[1:])):
                        final_result.append(doc_id)
                        break
            results.append(final_result)
        else:
            results.append([])
    return results

#Preprocess query
def preprocess_query(query):
    # Lowercase the text
    query = query.lower()
    
    # Tokenization
    query_tokens = nltk.word_tokenize(query)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    query_tokens = [token for token in query_tokens if token not in stop_words]
    
    # Remove punctuations
    query_tokens = [re.sub(r'[^\w\s]', '', token) for token in query_tokens]
    
    # Remove blank space tokens
    query_tokens = [token for token in query_tokens if token.strip()]
    
    return ' '.join(query_tokens)

# Input format
def input_format():
    N = int(input("Enter the number of queries: "))
    queries = []
    for _ in range(N):
        query = input("Enter the query: ")
        cleaned_query = preprocess_query(query)
        queries.append(cleaned_query)
    return N, queries

# Output format
def output_format(N, queries, results):
    for i in range(N):
        print(f"Number of documents retrieved for query {i+1} using positional index: {len(results[i])}")
        print(f"Names of documents retrieved for query {i+1} using positional index: {' '.join(results[i])}\n")

# Main function
def main():
    dataset_directory = 'preprocessed_text_files'  # Specify the directory containing preprocessed files
    positional_index_file = 'positional_index.pkl'  # File to save the positional index

    # Create positional index if it doesn't exist, otherwise load it
    if not os.path.exists(positional_index_file):
        positional_index = create_positional_index(dataset_directory)
        save_positional_index(positional_index, positional_index_file)
    else:
        positional_index = load_positional_index(positional_index_file)

    # Input
    N, queries = input_format()

    # Execute phrase queries
    results = execute_phrase_queries(positional_index, queries)

    # Output
    output_format(N, queries, results)

if __name__ == "__main__":
    main()
