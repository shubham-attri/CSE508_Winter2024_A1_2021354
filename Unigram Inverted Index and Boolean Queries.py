import os
import pickle
from collections import defaultdict
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

# Create unigram inverted index
def create_inverted_index(dataset_directory):
    inverted_index = defaultdict(set)
    for file_name in os.listdir(dataset_directory):
        file_path = os.path.join(dataset_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = preprocess_text(file.read())
            for token in tokens:
                inverted_index[token].add(file_name)
    return inverted_index

# Function to perform AND operation
def perform_AND(op1, op2):
    return op1.intersection(op2)

# Function to perform OR operation
def perform_OR(op1, op2):
    return op1.union(op2)

# Function to perform AND NOT operation
def perform_AND_NOT(op1, op2):
    return op1.difference(op2)

# Function to perform OR NOT operation
def perform_OR_NOT(op1, op2, all_files):
    return all_files.difference(op2).union(op1)

# Load inverted index
def load_inverted_index(file_path):
    with open(file_path, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index

# Save inverted index
def save_inverted_index(inverted_index, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(inverted_index, file)

# Execute queries
def execute_queries(inverted_index, queries):
    results = []
    for query in queries:
        operations = query.split(', ')
        result = inverted_index[operations[0]]
        for i in range(1, len(operations), 2):
            operator = operations[i]
            operand = operations[i+1]
            if operator == 'AND':
                result = perform_AND(result, inverted_index[operand])
            elif operator == 'OR':
                result = perform_OR(result, inverted_index[operand])
            elif operator == 'AND NOT':
                result = perform_AND_NOT(result, inverted_index[operand])
            elif operator == 'OR NOT':
                result = perform_OR_NOT(result, inverted_index[operand], set(inverted_index.keys()))
        results.append(result)
    return results

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
    N = int(input())
    queries = []
    for _ in range(N):
        query = input()
        cleaneed_query = preprocess_query(query)
        queries.append(cleaneed_query)
    return N, queries

# Output format
def output_format(N, queries, results):
    for i in range(N):
        print(f"Query {i+1}: {queries[i]}")
        print(f"Number of documents retrieved for query {i+1}: {len(results[i])}")
        print(f"Names of the documents retrieved for query {i+1}: {' '.join(results[i])}\n")

# Main function
def main():
    dataset_directory = 'preprocessed_text_files'  # Specify the directory containing preprocessed files
    inverted_index_file = 'inverted_index.pkl'  # File to save the inverted index

    # Create inverted index if it doesn't exist, otherwise load it
    if not os.path.exists(inverted_index_file):
        inverted_index = create_inverted_index(dataset_directory)
        save_inverted_index(inverted_index, inverted_index_file)
    else:
        inverted_index = load_inverted_index(inverted_index_file)

    # Input
    N, queries = input_format()

    # Execute queries
    results = execute_queries(inverted_index, queries)

    # Output
    output_format(N, queries, results)

if __name__ == "__main__":
    main()
