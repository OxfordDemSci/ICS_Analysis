import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Union

import markdown
import numpy
import pandas
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer
from bs4 import BeautifulSoup
from loguru import logger
from sentence_transformers import SentenceTransformer
from sklearn.metrics import silhouette_score

try:
    from cuml.cluster import HDBSCAN
except ImportError:
    from hdbscan import HDBSCAN
try:
    from cuml.manifold import UMAP
except ImportError:
    from umap import UMAP

columns_for_analysis = [
    "1. Summary of the impact",
    "2. Underpinning research",
    "3. References to the research",
    "4. Details of the impact",
    "5. Sources to corroborate the impact",
]


def clean_free_text(s: str):
    content = markdown.markdown(s)
    soup = BeautifulSoup(content, "html.parser")
    s = soup.get_text()
    s = re.sub(r"http\S+", "", s)
    s = re.sub("[^a-zA-Z]+", " ", s)
    s = s.replace("Summary of the impact indicative maximum 100 words ", "")
    s = s.replace("Summary of the impact ", "")
    s = s.replace("Underpinning research indicative maximum 500 words ", "")
    s = s.replace("Underpinning research ", "")
    s = s.replace(
        "References to the research indicative maximum of six references ", ""
    )
    s = s.replace("References to the research ", "")
    s = s.replace("Details of the impact indicative maximum 750 words ", "")
    s = s.replace("Details of the impact  ", "")
    s = s.replace(
        "Sources to corroborate the impact indicative maximum of 10 references ", ""
    )
    s = s.replace("Sources to corroborate the impact ", "")
    return s.strip()


def prepare_full_texts(excel_path: Union[str, Path]):
    df = pandas.read_excel(excel_path)
    df["full_text"] = df.apply(
        lambda row: "\n".join(str(row[col]) for col in columns_for_analysis), axis=1
    )
    df["cleaned_full_text"] = df["full_text"].apply(clean_free_text)
    return df


def run_bert(
    df: pandas.DataFrame,
    docs: List[str],
    embedding_model: SentenceTransformer,
    embeddings: numpy.ndarray,
    target_dir: Union[str, Path],
    n_neighbors: int = 15,
    nr_topics: Union[None, str, int] = "auto",
    random_state: int = 77,
):
    logger.info(f"Running BERTopic on {len(docs)} documents")
    model_dir = Path(target_dir) / "models"
    output_dir = Path(target_dir) / "output"
    fig_dir = Path(target_dir) / "figures"
    model_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created model directory at: {model_dir.absolute()}")
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory at: {output_dir.absolute()}")
    fig_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created figure directory at: {fig_dir.absolute()}")
    model_name = f'nn{n_neighbors}{f"_nr{nr_topics}" if nr_topics is not None else ""}'
    path_metadata_csv = target_dir / "metadata.csv"
    representation_model = KeyBERTInspired()
    umap_model = UMAP(
        n_neighbors=n_neighbors,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=random_state,
    )
    hsdb_model = HDBSCAN(
        min_cluster_size=10,
        metric="euclidean",
        prediction_data=True,
    )
    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
    topic_model = BERTopic(
        language="english",
        verbose=True,
        calculate_probabilities=True,
        n_gram_range=(1, 2),
        representation_model=representation_model,
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hsdb_model,
        ctfidf_model=ctfidf_model,
        nr_topics=nr_topics,
    )
    topics, probs = topic_model.fit_transform(docs, embeddings)
    topic_model.save(model_dir / model_name)
    topics_counter = Counter(topics)
    outliers_count = topics_counter.get(-1, 0)
    topics_count = (
        len(topics_counter) - 1 if outliers_count > 0 else len(topics_counter)
    )
    logger.info(f"Found {topics_count} topics and {outliers_count} outliers")
    df_topic_info = topic_model.get_topic_info()
    df_topic_info.to_excel(
        Path(target_dir) / "output" / f"{model_name}_topic_info.xlsx"
    )
    df["BERT_topic"] = topic_model.topics_
    df["BERT_prob"] = [max(i) for i in topic_model.probabilities_]
    df.to_excel(Path(target_dir) / "output" / f"{model_name}.xlsx")
    fig_topic = topic_model.visualize_documents(
        docs, hide_document_hover=True, hide_annotations=True
    )
    fig_topic.write_html(fig_dir.joinpath(f"{model_name}.html"))
    fig_topic_hierarchy = topic_model.visualize_hierarchy()
    fig_topic_hierarchy.write_html(fig_dir.joinpath(f"{model_name}_hierarchy.html"))
    metadata = {
        "random_state": random_state,
        "n_neighbors": n_neighbors,
        "nr_topics": nr_topics,
        "topics_count": topics_count,
        "outliers_count": outliers_count,
    }
    logger.info(metadata)
    pandas.DataFrame([metadata]).to_csv(
        path_metadata_csv,
        mode="a",
        header=not path_metadata_csv.exists(),
        index=False,
    )


def get_model(target_dir, n_neighbors, nr_topics=None):
    model_name = f'nn{n_neighbors}{f"_nr{nr_topics}" if nr_topics is not None else ""}'
    model_path = Path(target_dir) / "models" / f"{model_name}"
    return BERTopic.load(str(model_path.absolute())), model_name


def calculate_silhouette_score(topic_model, embeddings, topics):
    umap_embeddings = topic_model.umap_model.transform(embeddings)
    indices = [index for index, topic in enumerate(topics) if topic != -1]
    X = umap_embeddings[numpy.array(indices)]
    labels = [topic for topic in topics if topic != -1]
    return silhouette_score(X, labels)


if __name__ == "__main__":
    df = prepare_full_texts(sys.argv[1])
    docs = df["cleaned_full_text"].tolist()
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(docs, show_progress_bar=True)
    for i in range(2, 20):
        logger.info(f"Running neighbors: {i}")
        run_bert(
            df,
            docs,
            embedding_model,
            embeddings,
            sys.argv[2],
            n_neighbors=i,
            nr_topics=None,
        )
    logger.info("Finished running BERTopic")
    path_evaluation_csv = Path(sys.argv[2]) / "evaluation.csv"
    logger.info("Calculating coherence scores")
    for i in range(2, 20):
        topic_model, model_name = get_model(sys.argv[2], i)
        silhouette = calculate_silhouette_score(
            topic_model, embeddings, topic_model.topics_
        )
        metadata = {
            "n_neighbors": i,
            "silhouette_score": silhouette,
        }
        pandas.DataFrame([metadata]).to_csv(
            path_evaluation_csv,
            mode="a",
            header=not path_evaluation_csv.exists(),
            index=False,
        )
    logger.info("Finished calculating silhouette scores")
