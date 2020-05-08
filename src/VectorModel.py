import os
import math
import numpy as np


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

    def tf_idf_weight(self, term: str, doc_path: str) -> float:
        """
            Calculates the tf-idf weight for `term` in document with `doc_path`
        """
        return self.tf(term, doc_path) * self.idf(term)

    def weights_for_doc(self, doc_path: str):
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

    def generate_weights(self, weights_path: str):
        """
            Saves the vectors for articles to `weights_path`
        """
        for file in os.listdir(self.processed_path):
            doc_path = f"{self.processed_path}/{file}"
            weights = self.weights_for_doc(doc_path)
            save_path = f"{weights_path}/{file}"
            np.save(save_path, weights)


if __name__ == "__main__":
    vm = VectorModel('assets/articles/processed')

    vm.generate_weights('assets/articles/vectors')
