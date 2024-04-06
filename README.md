# RAG a movie

A mini project I learn and develop RAG - Retrieval Augmented Generation which I am learnt by [VietAI](https://vietai.org/). Based on the tutorial, I learnt to answer 3 questions.

1. Does every question of user need context ?
2. Should we trust retrieval model 100% ?
3. What should the model do when the user's query is ambiguous ?

In the repo, I am using a dataset about movie to demonstrate a RAG pipeline

<img title="a RAG pipeline" alt="Alt text" src="/assets/rag.png">

## Dataset
adult,belongs_to_collection,budget,genres,homepage,id,imdb_id,original_language,original_title,overview,popularity,poster_path,production_companies,production_countries,release_date,revenue,runtime,spoken_languages,status,tagline,title,video,vote_average,vote_count

The main features which are encoded in database:
1. Title : the name of movie
2. Overview: the shortcut of movie

## How to install 

``` bash
pip install -r requirements.txt 
```
You need to create a file ```.env``` and set GEMINI key in this ```GEMINI_API_KEY=your_api_key```

## Ready to chat
```
python chat.py
```

## Future Development
In the mini project, I will develop some features: 
1. Evaluate RAG's performance using RAGA framework
2. Integrate some LLM api