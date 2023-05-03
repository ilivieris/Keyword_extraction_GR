import os
import yake
import json 
from tqdm import tqdm


def selected_keywords(word:str=None) -> bool:
      '''
        Gets a word and returns if it should be usef as a keyword

        Parameters
        ----------
        word: Word

        Returns
        -------
        True/False (dhould be removed or not)
      '''
      
      for x in ['ΤΕΥΧΟΣ', 'ΕΦΗΜΕΡΙΣ', 'ΚΥΒΕΡΝΗΣΕΩΣ', 'ΕΛΛΗΝΙΚΗΣ', 'ΔΗΜΟΚΡΑΤΙΑΣ', 'στην', 'στον', 'από την', 'από τον', 'από το', 'ΑΡΙΘΜΟΣ ΦΥΛΛΟΥ', 'ΠΡΟΕΔΡΟΣ', 'ΠΕΡΙΕΧΟΜΕΝΑ']:
            if x in word:
                return False
      return True

def percentage_upper_chars(string):
    '''
        Counts the percentage of upper characters in a word

        Parameters
        ----------
        string: Word

        Returns
        -------
        percentage of upper characters in a word
    '''
    return sum(map(str.isupper, string))/len(string)






# Data path
data_path = 'Data'

file_list = []
for root, dirs, files in os.walk(data_path):
	for file in files:
        # Append the file name to the list
		file_list.append(os.path.join(root, file))

# Setup keywords extractor
kw_extractor = yake.KeywordExtractor()

d_keywords = dict()
for filename in tqdm(file_list):
    # Open file
    with open(filename, encoding="utf-8") as f:
        doc = f.read()	

    # Get keywords/keyphrases
    keywords = kw_extractor.extract_keywords(doc)

    # Store keywords/keyphrases
    d_keywords[filename] = [x[0] for x in keywords if len(x[0]) > 3 and selected_keywords(x[0]) and percentage_upper_chars(x[0]) < 0.7]


# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    os.mkdir(output_dir)

with open(output_dir + "Keyphrases_YAKE.json", "w", encoding="utf-8") as outfile:
    json.dump(d_keywords, outfile, ensure_ascii=False)



