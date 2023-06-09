import spacy
from spacy.matcher import Matcher
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize

import re
pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')


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


def remove_stopping_words(text):
    '''
        Remove stopping words from text

        Parameters
        ----------
        text: input text

        Returns
        -------
        text with removed stopping words
    '''    
    return pattern.sub('', text)

def clean_keyword(keyword):
    parts = keyword.split(' ')

    if parts[0][-1] == '.' or parts[0][0] == '.': 
        keyword = ' '.join(parts[1:])
    elif parts[0][0] == ',':
        keyword = ' '.join(parts[2:])

    keyword = remove_stopping_words(keyword)

    return keyword


def match(nlp, keyword):
    """This function checks if a list of keywords match a certain POS pattern"""
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'VERB'}, {'POS': 'VERB'}],
        [{'POS': 'NOUN'}, {'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}],  
        # [{'POS': 'NOUN'}, {'POS': 'VERB'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'ADV'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'VERB'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'NOUN'}, {'POS': 'NOUN'}],
        [{'POS': 'ADJ'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'ADP'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'ADJ'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'VERB'}, {'POS': 'NOUN'}],
        [{'POS': 'NOUN'}, {'POS': 'ADP'}, {'POS': 'NOUN'}],
        [{'POS': 'PROPN'}, {'POS': 'NOUN'}, {'POS': 'PROPN'}],
        [{'POS': 'VERB'}, {'POS': 'ADV'}],
        [{'POS': 'PROPN'}, {'POS': 'NOUN'}],
        #
        [{'POS': 'ADJ'}, {'POS': 'NOUN'}],
        # [{'POS': 'NOUN'}], 
        # [{'POS': 'ADJ'}]
        ]
    
    matcher = Matcher(nlp.vocab)
    matcher.add("pos-matcher", patterns)
    # create spacy object
    doc = nlp(keyword)
    # iterate through the matches
    matches = matcher(doc)
    # if matches is not empty, it means that it has found at least a match
    if len(matches) > 0:
        return True
    return False