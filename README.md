# Keyword extraction GR

This repository parses a series of documents and extracts their keywords. The keywords of each document is stored in a JSON file

<br/>

## Methodologies
---

- **YAKE**: Keywords extraction using YAKE package
- **Spacy**: Keywords extraction using Spacy package by excluding the top-ranked phrases in the document
- **KeyBERT**: Keyword extraction using KeyBERT and two Greek LLM models
- **LMRank**: Keywords extraction using LMRank methodology
- **Hybrid**: Keywods extraction using (i) KeyBERT and two Greek LLM models and (ii) Spacy by excluding the top-ranked phrases

<br/>


## Data
---

The Greek legislation dataset consists of randomly selected)legal documents of Greek Government Gazette. 
Every issue contains multiple legal texts.

<br/>


## Get started
--- 

1. Create a virtual environment 
```
    conda create -n myEnv python=3.8
```

2. Activate the virtual environment 
```
    conda activate myEnv
```

3. Install requirements 
```
    pip install -r requirements.txt
```

4. Run
```
    python '.\01. YAKE.py'
    python '.\02. Spacy.py'
    python '.\03. KeyBERT.py'
    python '.\04. LMRank.py'
    python '.\05. Hybrid.py'
```

<br/>

## Requirements
---

- python>=3.8
- tqdm==4.61.0
- spacy==3.2.4
- yake==0.4.8
- faiss==1.7.2

<br/>

## :mailbox: Contact
---

Ioannis E. Livieris (livieris@novelcore.eu)