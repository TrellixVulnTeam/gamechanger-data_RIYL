from txtai.embeddings import Embeddings
from os.path import join
from numpy import interp
from pandas import read_csv

from gamechangerml.api.utils.logger import logger
from gamechangerml.src.text_handling.process import preprocess
from .similarity_ranker import SimilarityRanker

# Metadata for the model these scores were derived from
# {"user": null, "date_started": "2022-04-29 16:06:06", "date_finished": "2022-04-29 19:52:52", "doc_id_count": 1495122, "corpus_name": "/opt/app-root/src/gamechangerml/corpus", "encoder_model": "multi-qa-MiniLM-L6-cos-v1"}
DEFAULT_SCORES = [
    [0.8, "High"],
    [0.5, "Medium"],
    [0.4, "Low"],
    [0.0, "Very Low"],
]
DEFAULT_CUTOFF = 0.25


class DocCompareSentenceSearcher:
    """
    Imports the text index generated by the DocCompareSentenceEncoder and
    performs the search functionality. Initial set of documents
    are first retrieved through an Annoy index then re-ranked with
    the similarity model.

    Args:
        index_path (str): Path to index directory generated by the
            DocCompareSentenceEncoder
        encoder_model (str): Model name supported by huggingface
            and txtai to generate the document embeddings
        sim_model (str): Model name supported by huggingface
            and txtai to calculate similarity between query and document
    """

    def __init__(
        self, sim_model_name, index_path, transformer_path, sim_model=None
    ):
        self.embedder = Embeddings()
        self.embedder.load(index_path)
        # replace this with looking up ES
        self.data = read_csv(
            join(index_path, "data.csv"), dtype={"paragraph_id": str}
        )
        if sim_model:
            self.similarity = sim_model
        else:
            self.similarity = SimilarityRanker(
                sim_model_name, transformer_path
            )

        self.default_score_mapper = self.score_mapper_creator(DEFAULT_SCORES)

    def retrieve_topn(self, query, num_results, score_mapper, cutoff) -> dict:
        results = []
        retrieved = self.embedder.search(query, limit=num_results)
        for doc_id, score in retrieved:
            if score < cutoff:
                continue

            text = self.data[self.data["paragraph_id"] == str(doc_id)].iloc[0][
                "text"
            ]

            results.append(
                {
                    "id": doc_id,
                    "text": text,
                    "text_length": len(text),
                    "score": score,
                    "score_display": score_mapper(score),
                }
            )

        return results

    def score_mapper_creator(self, scores_map):
        """
        Returns a function that maps a score to display text based on scores_map
        if score > threshold -> display, else -> None
        """
        scores_map.sort(key=lambda x: x[0], reverse=True)

        def mapper(score):
            for threshold, display in scores_map:
                if score > threshold:
                    return display

            return None

        return mapper

    def search(
        self, query, num_results, body, process=False, externalSim=True,
    ):
        """
        Search the index and perform a similarity scoring reranker at
        the topn returned documents
        Args:
            query (str): Query text to search in documents
        Returns:
            rerank (list): List of tuples following a (score, paragraph_id,
                paragraph_text) format ranked based on similarity with query
        """
        if process:
            query = " ".join(preprocess(query))
        logger.info(f"Doc Compare Sentence searching for: {query}")
        if not len(query) > 2:
            return []

        cutoff = body.get("cutoff", DEFAULT_CUTOFF)
        score_display_mapping = body.get("score_display_mapping", None)
        if score_display_mapping is None:
            score_mapper = self.default_score_mapper
        else:
            score_mapper = self.score_mapper_creator(score_display_mapping)

        top_results = self.retrieve_topn(
            query, num_results, score_mapper, cutoff
        )

        if not top_results:
            return []

        if externalSim:
            return self.similarity.re_rank(query, top_results)
        else:
            # adding normalize text length to score and sorting
            finalResults = []
            result_text = [len(x["text"]) for x in top_results]
            length_scores = interp(
                result_text, (min(result_text), max(result_text)), (0, 0.2)
            )
            for idx, doc in enumerate(top_results):
                doc["text_length"] = length_scores[idx]
                doc["score"] = doc["score"]
                finalResults.append(doc)

            finalResults.sort(key=lambda i: i["score"], reverse=True)
            return finalResults
