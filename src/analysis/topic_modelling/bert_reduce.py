import sys
from pathlib import Path

import pandas
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from loguru import logger


def get_topic_terms_with_probs(topic_id):
    return topic_model.get_topic(topic_id)


def get_topic_terms_oneline(topic_id):
    return ",".join([term[0] for term in topic_model.get_topic(topic_id)])


if __name__ == "__main__":
    target_folder = Path(sys.argv[1])
    model_name = sys.argv[2]
    model_path = target_folder / "models" / model_name
    reduced_model_dir = target_folder / "reduced_model"
    reduced_model_dir.mkdir(parents=True, exist_ok=True)
    step = 0.001
    df = pandas.read_excel(sys.argv[3])
    docs = df["cleaned_full_text"].tolist()
    representation_model = KeyBERTInspired()
    for i in range(51):
        logger.info(f"Reducing outliers with threshold {step*i}")
        topic_model = BERTopic.load(model_path)
        new_topics = topic_model.reduce_outliers(
            docs,
            topic_model.topics_,
            probabilities=topic_model.probabilities_,
            threshold=step * i,
            strategy="probabilities",
        )
        topic_model.update_topics(
            docs, topics=new_topics, representation_model=representation_model
        )
        topic_model.save(reduced_model_dir / f"{model_name}_threshold{step*i}")
        df[f"BERT_topic_reduced{step*i}"] = pandas.DataFrame(topic_model.topics_)
        df[f"BERT_topic_terms_reduced{step*i}"] = df[
            f"BERT_topic_reduced{step*i}"
        ].apply(get_topic_terms_oneline)
    df.to_excel(target_folder / f"{model_name}_reduced.xlsx")
