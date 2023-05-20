import pytextrank
import spacy

def extract_keywords_spacy(nlp=None, doc:str=None, max_number_of_keywords:int=20):
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
        if len(phrase.text) > 3: #and percentage_upper_chars(phrase.text) < 0.2:
            keywords.append(phrase.text) 

    return keywords[:max_number_of_keywords]