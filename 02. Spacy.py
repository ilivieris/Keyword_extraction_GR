import os
import spacy
import pytextrank
import json 
from tqdm import tqdm
# Installation: python -m spacy download el_core_news_sm
from utils.extract_keywords_spacy import extract_keywords_spacy
from utils.utils import percentage_upper_chars




# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    print(f'[INFO] Output directory ({output_dir}) created')
    os.mkdir(output_dir)


# Data path
data_path = 'Data'

# Get directories containing FEKs
directories_list = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

# Load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("el_core_news_sm")
# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")





# Main loop
loop_directories = tqdm(directories_list, leave=True)
for directory in loop_directories:
    # Update TQDM
    loop_directories.set_description(f"Directory: {directory}")

    # Set path & output file
    path = f'{data_path}/{directory}'
    output_file = f'{output_dir}/Keyphrases-Spacy-{directory}.json'

    # Check if the file containing the keywords have been already created 
    if os.path.isfile(output_file):
        d_keywords = json.load(open(output_file, encoding="utf8")) 
    else:
        d_keywords = dict()

    # Get files
    files_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]



    loop_files = tqdm(files_list, leave=True)
    for idx, filename in enumerate(loop_files):
        # Update TQDM
        loop_files.set_description(f"File: {filename} [{idx}/{len(files_list)}]")

        # Check if the keywords have been already extracted for this document
        if (filename in d_keywords):
            continue
        
        # Open file
        with open(os.path.join(path, filename), encoding="utf-8") as f:
            doc = f.read()	

        # Get keywords/keyphrases
        keywords = extract_keywords(nlp=nlp, doc=doc, max_number_of_keywords=10)

        # Store keywords/keyphrases
        d_keywords[filename] = keywords


    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(d_keywords, outfile, ensure_ascii=False)