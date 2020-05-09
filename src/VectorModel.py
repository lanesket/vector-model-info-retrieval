from typing import List
import os
import math
import numpy as np
import re
from Preprocessor import Preprocessor
from sklearn.metrics.pairwise import cosine_similarity


class VectorModel:
    def __init__(self, processed_path: str):
        self.processed_path = processed_path

        self.doc_count = len(os.listdir(processed_path))

        self.vector_mapping = self._vector_mapping()

        self.num_terms = len(self.vector_mapping.keys())

        self.tfs, self.dfs = self._generate_tfs_dfs()

    def _vector_mapping(self) -> dict:
        """
            Dict with word to its place in the vector
        """
        # problem
        words = set()
        for file in os.listdir(self.processed_path):
            doc_path = f"{self.processed_path}/{file}"
            with open(doc_path, 'r') as f:
                text_words = f.readline().split()
                words = words.union(set(text_words))

        return dict(zip(words, range(len(words))))

    def _generate_tfs_dfs(self) -> dict:
        """
            Generates the dictionaries for tf and df
        """
        tfs, dfs = {}, {}

        for file in os.listdir(self.processed_path):
            doc_path = f"{self.processed_path}/{file}"
            if doc_path not in tfs:
                tfs[doc_path] = {}
            with open(doc_path, 'r') as f:
                text = f.readline()
                terms = set(text.split())
                for term in terms:
                    tfs[doc_path][term] = text.count(term)

                    if term not in dfs:
                        dfs[term] = 1
                    else:
                        dfs[term] += 1

        return tfs, dfs

    def tf(self, term: str, doc_path: str) -> int:
        """
            Term frequency
            Number of times term (word) occured in doc
        """
        return self.tfs[doc_path][term]

    def df(self, term: str) -> int:
        """
            Document frequency
            Number of documents containing a term (word)
        """
        return self.dfs[term]

    def idf(self, term: str) -> float:
        """
            Inverse document frequency
        """
        return math.log(self.doc_count / self.df(term))

    def tf_query(self, term: str, query_words: List) -> int:
        """
            Term frequency for query
            Number of times term occured in query
        """
        return query_words.count(term)

    def tf_idf_weight(self, term: str, doc_path: str) -> float:
        """
            Calculates the tf-idf weight for `term` in document with `doc_path`
        """
        return self.tf(term, doc_path) * self.idf(term)

    def tf_idf_weight_query(self, term: str, query_words: List) -> float:
        """
            Calculates the tf-idf weight for `term` in query consisting of `query_words`
        """
        return self.tf_query(term, query_words) * self.idf(term)

    def weights_for_doc(self, doc_path: str) -> np.ndarray:
        """
            Creates the vector of tf-idf weights for document with `doc_path`
        """
        weights = np.zeros(shape=self.num_terms)
        with open(doc_path, 'r') as f:
            text = f.readline()
            terms = set(text.split())
            for term in terms:
                index = self.vector_mapping[term]
                weights[index] = self.tf_idf_weight(term, doc_path)

        return weights

    def generate_weights(self, weights_path: str) -> None:
        """
            Saves the vectors for articles to `weights_path`
        """
        for file in os.listdir(self.processed_path):
            doc_path = f"{self.processed_path}/{file}"
            weights = self.weights_for_doc(doc_path)
            save_path = f"{weights_path}/{file}"
            np.save(save_path, weights)

    def load_vectors(self, weights_path: str) -> dict:
        """
            Loads the vectors from `weights_path` and saves the to dict
        """
        vectors = {}
        for file in os.listdir(weights_path):
            v_path = f"{weights_path}/{file}"
            res = re.search("(.+).npy", v_path)
            # filename without extension
            if res:
                filename = res.group(1)

                vectors[filename] = np.load(v_path)

        return vectors

    def query_vectorize(self, query_words: List) -> np.ndarray:
        """
            Takes the list of query words and created the vector from without explicitly provided weights
        """
        weights = np.zeros(shape=self.num_terms)
        terms = set(query_words)

        for term in terms:
            index = self.vector_mapping[term]
            weights[index] = self.tf_idf_weight_query(term, query_words)

        return weights

    def cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
            Calculates the angle between 2 vectors
        """
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        # return cosine_similarity(v1, v2)[0][0]

    def find_similar(self, vectors: dict, q_v: np.ndarray) -> str:
        """
            Find the similar document using cosine similarity
        """
        max_sim = 0
        sim_doc_name = ""

        for fname, f_v in vectors.items():
            r = self.cosine_similarity(f_v, q_v)

            if r > max_sim:
                max_sim = r
                sim_doc_name = fname

        return sim_doc_name


if __name__ == "__main__":
    vm = VectorModel('assets/articles/processed')

    vm.generate_weights('assets/articles/vectors')

    vectors = vm.load_vectors('assets/articles/vectors')

    p = Preprocessor("assets/stop-words.txt")
    query = "Benjamin Netanyahu "
    processed_query = p.process(query)

    query_vector = vm.query_vectorize(processed_query)

    print(vm.find_similar(vectors, query_vector))
