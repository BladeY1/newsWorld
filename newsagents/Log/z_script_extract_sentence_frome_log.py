import os

def extract_sentences_with_phrase(input_file, phrase, output_file):
    # Ensure the input file exists
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        return

    sentences = []
    
    # Read the input file and extract sentences with the specified phrase
    with open(input_file, 'r') as file:
        for line in file:
            if phrase in line:
                sentences.append(line.strip())

    # Write the extracted sentences to the output file
    with open(output_file, 'w') as file:
        for sentence in sentences:
            file.write(f"{sentence}\n")

    print(f"Extracted {len(sentences)} sentences containing the phrase '{phrase}'.")

# Specify the file paths and the phrase to search for
input_file = '/home/newsworld/newsagents/Log/us_election_2_log2'
output_file = 'us_election_forecast_result2.txt'
phrase = "to win the election"

# Run the extraction function
extract_sentences_with_phrase(input_file, phrase, output_file)
