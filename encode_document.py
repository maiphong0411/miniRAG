import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def encode_document(document="data/movies_metadata.csv", name_db="movie_rag_test"):
    """
    A function to encode a document using SentenceTransformer and store the embeddings in a Vector database.

    Parameters:
    document (str): The path to the document to encode (default is "data/movies_metadata.csv").
    name_db (str): The name of the collection in the Vector database (default is "movie_rag_test").

    Returns:
    tuple: A tuple containing the Vector database object and the SentenceTransformer object.
    """

    SENTEMB = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    client = chromadb.Client()

    my_vectordb = client.create_collection(name=name_db, metadata={"hnsw:space": "cosine"})
    df = pd.read_csv(document)

    # drop the rows that contain nulls value in either title or overview
    df = df.dropna(subset = ["title", "overview"]).drop_duplicates(subset="id")

    # we can turn the dataframe to a list of dicts
    metadatas = list(df.to_dict('records'))[:]

    # create the embeddings

    # first we have to concatenate title and overview to get the text for embedding
    texts_to_embed = [f"{line['title']}\n{line['overview']}" for line in metadatas]

    embeddings = SENTEMB.encode(texts_to_embed, batch_size=16, show_progress_bar = True, normalize_embeddings = True)

    for i in tqdm(range(0, len(embeddings), 1000)):
        my_vectordb.add(
            embeddings=embeddings[i:i+1000],
            metadatas=metadatas[i:i+1000],
            ids = [str(line["id"]) for line in metadatas][i:i+1000]
        )

    return my_vectordb, SENTEMB