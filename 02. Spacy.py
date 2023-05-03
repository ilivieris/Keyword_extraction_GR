import os
import spacy
import pytextrank
import json 
from tqdm import tqdm
# Installation: python -m spacy download el_core_news_sm


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

def extract_keywords(nlp=None, doc:str=None, max_number_of_keywords:int=20):
    '''
        Given a text, returns the keywords

        Parameters
        ----------
        nlp: spacy functionality
        doc: Text
        max_number_of_keywords: maximum number of keywords

        Returns:
        --------
        A list with keywords
    '''
    doc = doc.replace('\n', ' ')
    result = nlp(doc)
    
    # examine the top-ranked phrases in the document
    keywords = list()
    for phrase in result._.phrases:
        if len(phrase.text) > 3 and percentage_upper_chars(phrase.text) < 0.2:
            keywords.append(phrase.text) 

    return keywords[:max_number_of_keywords]






# Data path
data_path = 'Data'

file_list = []
for root, dirs, files in os.walk(data_path):
	for file in files:
        # Append the file name to the list
		file_list.append(os.path.join(root, file))





# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("el_core_news_sm")
# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")


d_keywords = dict()
for filename in tqdm(file_list):
    # Open file
    with open(filename, encoding="utf-8") as f:
        doc = f.read()	

    # Get keywords/keyphrases
    keywords = extract_keywords(nlp=nlp, doc=doc, max_number_of_keywords=10)

    d_keywords[filename] = keywords
    print(keywords)


with open("Keyphrases_Spacy.json", "w", encoding="utf-8") as outfile:
    json.dump(d_keywords, outfile, ensure_ascii=False)



