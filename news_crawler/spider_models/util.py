import requests
import re
import os
from dotenv import load_dotenv
load_dotenv()

################################################ Corpus Creation ################################################

def fetch_articles(search_term, api_key, page=1):
    url = f"https://newsapi.org/v2/everything?q={search_term}&searchIn=title&sortBy=relevancy&language=en&pageSize=100&page={page}&apiKey={api_key}" #most accurate results possible lol
    response = requests.get(url)
    return response.json()

def clean_text(text):
    text = re.sub(r'\[\+\d+ chars\]', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'If you click \'Accept all\',.*?device', '', text)
    text = re.sub(r'\(in other words, use …', '', text)
    text = re.sub(r'\[Removed\]', '', text)
    text = re.sub(r'\[\+\]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_central_corpus(search_term):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    central_corpus = ""
    page = 1
    while True:
        data = fetch_articles(search_term, NEWS_API_KEY, page)
        articles = data.get("articles", [])
        if not articles:
            break
        for article in articles:
            content = article.get("content", "")
            if content:
                cleaned_content = clean_text(content)
                central_corpus += cleaned_content + " "
        page += 1
        if page > 5:  #limits to first 500 articles for practical purposes
            break
    write_corpus_to_file(central_corpus, search_term)
    return central_corpus

def write_corpus_to_file(corpus, search_term):
    output_file_path = f"data/{'_'.join(search_term.lower().split(' '))}_central_corpus.txt" #i want to be able to display this when i build out a frontend
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(corpus)    
    print(f"Central Corpus written to {output_file_path}")

##################################################### END ######################################################