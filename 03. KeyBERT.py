import os
import json 
from tqdm import tqdm
from keybert import KeyBERT
# You can select any model from sentence-transformers 
# (https://www.sbert.net/docs/pretrained_models.html) 
# and pass it through KeyBERT with model:
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')





# Data path
data_path = 'Data'

file_list = []
for root, dirs, files in os.walk(data_path):
	for file in files:
        # Append the file name to the list
		file_list.append(os.path.join(root, file))





d_keywords = dict()
for filename in tqdm(file_list):
    # Open file
    with open(filename, encoding="utf-8") as f:
        doc = f.read()	

    # Get keywords/keyphrases
    keywords = kw_model.extract_keywords(doc, 
                                     keyphrase_ngram_range=(1, 2), 
                                     stop_words='english', 
                                     highlight=False,
                                     top_n=20,
                                     use_maxsum=False,
                                     use_mmr=True, diversity=0.1);

    # Store keywords/keyphrases
    d_keywords[filename] = [x[0] for x in keywords]




# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    os.mkdir(output_dir)

with open(output_dir + "Keyphrases_KeyBERT.json", "w", encoding="utf-8") as outfile:
    json.dump(d_keywords, outfile, ensure_ascii=False)




