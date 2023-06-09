import os
import json 
from tqdm import tqdm
from LMRank.model import LMRank
# You can select any model from sentence-transformers 
# (https://www.sbert.net/docs/pretrained_models.html) 
# and pass it through KeyBERT with model:
model = LMRank(model_name='lighteternal/stsb-xlm-r-greek-transfer', 
               spacy_model_name='el_core_news_lg')


# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    print(f'[INFO] Output directory ({output_dir}) created')
    os.mkdir(output_dir)


# Data path
data_path = 'Data'

# Get directories containing FEKs
directories_list = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]




# Main loop
loop_directories = tqdm(directories_list, leave=True)
for directory in loop_directories:
    # Update TQDM
    loop_directories.set_description(f"Directory: {directory}")

    # Set path & output file
    path = f'{data_path}/{directory}'
    output_file = f'{output_dir}/Keyphrases-LMRank-{directory}.json'

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
        try:
            keywords = kw_model.extract_keywords(doc,
                                                 top_n=20)
            # Store keywords/keyphrases
            d_keywords[filename] = [x[0] for x in keywords]
        except Exception as e:
            print(f'[ERROR] {e}')

        if idx%300 == 0:
            with open(output_file, "w", encoding="utf-8") as outfile:
                json.dump(d_keywords, outfile, ensure_ascii=False)
       

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(d_keywords, outfile, ensure_ascii=False)







