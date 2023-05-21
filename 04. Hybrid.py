import os
import json 
from tqdm import tqdm
import spacy
from keybert import KeyBERT
from utils.utils import clean_keyword, match
from utils.extract_keywords_spacy import extract_keywords_spacy
# You can select any model from sentence-transformers 
# (https://www.sbert.net/docs/pretrained_models.html) 
# and pass it through KeyBERT with model:
kw_model_1 = KeyBERT(model='lighteternal/stsb-xlm-r-greek-transfer')
kw_model_2 = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')

print('[INFO] Model loaded')

# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    print(f'[INFO] Output directory ({output_dir}) created')
    os.mkdir(output_dir)


# Data path
data_path = 'Data'

# Get directories containing FEKs
directories_list = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

# Spacy model
nlp = spacy.load("el_core_news_lg")
# Add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")


# Main loop
loop_directories = tqdm(directories_list[:1], leave=True)
for directory in loop_directories:
    # Update TQDM
    loop_directories.set_description(f"Directory: {directory}")

    # Set path & output file
    path = f'{data_path}/{directory}'
    output_file = f'{output_dir}/Keyphrases-Hybrid-{directory}.json'

    # Check if the file containing the keywords have been already created 
    if os.path.isfile(output_file):
        d_keywords = json.load(open(output_file, encoding="utf8")) 
    else:
        d_keywords = dict()

    # Get files
    files_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]



    loop_files = tqdm(files_list[:5], leave=True)
    for idx, filename in enumerate(loop_files):

        # Update TQDM
        loop_files.set_description(f"File: {filename} [{idx}/{len(files_list)}]")
                
        # Check if the keywords have been already extracted for this document
        if (filename in d_keywords):
            continue
        
        # Open file
        with open(os.path.join(path, filename), encoding="utf-8") as f:
            text = f.read()	

        # Preprocess text
        text = text.replace('\n', '. ')
        text = text.replace('\t', '. ')


        # nlpaueb/bert-base-greek-uncased-v1
        # Get keywords/keyphrases
        try:
            keywords = kw_model_1.extract_keywords(text, 
                                                   keyphrase_ngram_range=(1, 2), 
                                                   stop_words='english', 
                                                   highlight=False,
                                                   top_n=50,
                                                   use_maxsum=False,
                                                   use_mmr=True, diversity=0.3);

            # Keyword cleaning (1)
            keywords = [(clean_keyword(item[0]), item[1]) for item in keywords]
            # Keyword cleaning (2)
            keywords = [keyword for keyword in keywords if match(nlp, keyword[0])]
            # Keyword clearning (3)
            keywords = [(' '.join(keyword.split(' ')[1:]), keyword[1]) if nlp(keyword[0])[0].pos_ in ['DET','ADP'] else keyword for keyword in keywords]

            # Store keywords/keyphrases
            d_keywords[filename] = [{'keyword':x[0], 'score_1':x[1]} for x in keywords]
        except Exception as e:
            print(f'[ERROR] Approach 1 - Filename: {filename}')
            print(f'{e}')



        # paraphrase-multilingual-MiniLM-L12-v2
        # Get keywords/keyphrases
        try:
            keywords = kw_model_2.extract_keywords(text, 
                                                   keyphrase_ngram_range=(1, 2), 
                                                   stop_words='english', 
                                                   highlight=False,
                                                   top_n=50,
                                                   use_maxsum=False,
                                                   use_mmr=True, diversity=0.3);

            # Keyword cleaning (1)
            keywords = [(clean_keyword(item[0]), item[1]) for item in keywords]
            # Keyword cleaning (2)
            keywords = [keyword for keyword in keywords if match(nlp, keyword[0])]
            # Keyword clearning (3)
            keywords = [(' '.join(keyword.split(' ')[1:]), keyword[1]) if nlp(keyword[0])[0].pos_ in ['DET','ADP'] else keyword for keyword in keywords]

            # Store keywords/keyphrases
            d_keywords[filename] += [{'keyword':x[0], 'score_2':x[1]} for x in keywords]
        except Exception as e:
            print(f'[ERROR] Approach 2 - Filename: {filename}')
            print(f'{e}')


        # Spacy
        # Get keywords/keyphrases
        try:
            keywords = extract_keywords_spacy(nlp=nlp, doc=text, max_number_of_keywords=30)

            # Keyword cleaning (1)
            keywords = [clean_keyword(item) for item in keywords]
            # Keyword cleaning (2)
            keywords = [keyword for keyword in keywords if match(nlp, keyword)]
            # Keyword cleaning (3) - Two times!
            keywords = [' '.join(keyword.split(' ')[1:]) if nlp(keyword)[0].pos_ in ['DET','ADP'] else keyword for keyword in keywords]
            keywords = [' '.join(keyword.split(' ')[1:]) if nlp(keyword)[0].pos_ in ['DET','ADP'] else keyword for keyword in keywords]

            # Store keywords/keyphrases
            d_keywords[filename] += [{'keyword':x, 'score_3':'NaN'} for x in keywords]
        except Exception as e:
            print(f'[ERROR] Approach 3 - Filename: {filename}')
            print(f'{e}')



        if idx%100 == 0:
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(d_keywords, outfile, ensure_ascii=False)

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(d_keywords, outfile, ensure_ascii=False)






