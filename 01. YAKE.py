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




# Output directory
output_dir = 'Extracted_keyphrases/'
if (not os.path.exists(output_dir)):
    print(f'[INFO] Output directory ({output_dir}) created')
    os.mkdir(output_dir)


# Data path
data_path = 'Data'

# Get directories containing FEKs
directories_list = [f for f in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, f))]

# Setup keywords extractor
kw_extractor = yake.KeywordExtractor()


# Main loop
loop_directories = tqdm(directories_list, leave=True)
for directory in loop_directories:
    # Set path & output file
    path = f'{data_path}/{directory}'
    output_file = f'{output_dir}/Keyphrases-YAKE-{directory}.json'

    # Check if the file containing the keywords have been already created 
    if os.path.isfile(output_file):
        d_keywords = json.load(open(output_file, encoding="utf8")) 
    else:
        d_keywords = dict()

    # Get files
    files_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]



    loop_files = tqdm(files_list, leave=True)
    for idx, filename in enumerate(loop_files):
        # Check if the keywords have been already extracted for this document
        if (filename in d_keywords):
            continue
        
        # Open file
        with open(os.path.join(path, filename), encoding="utf-8") as f:
            doc = f.read()	

        # Get keywords/keyphrases
        keywords = kw_extractor.extract_keywords(doc)

        # Store keywords/keyphrases
        d_keywords[filename] = [x[0] for x in keywords if len(x[0]) > 3 and selected_keywords(x[0]) and percentage_upper_chars(x[0]) < 0.7]


        # Update TQDM
        loop_files.set_description(f"File: {filename} [{idx}/{len(files_list)}]")

       

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(d_keywords, outfile, ensure_ascii=False)

    # Update TQDM
    loop_files.set_description(f"Directory: {directory}")