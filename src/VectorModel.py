import os
import math


class VectorModel:
    def __init__(self, processed_path: str):
        self.processed_path = processed_path
        self.doc_count = len(os.listdir(processed_path))
        self.vector_mapping = self._vector_mapping()
        self.tfs, self.dfs = self._generate_tfs_dfs()

    def _vector_mapping(self):
        """
            Dict with word to its place in the vector
        """
        words = set()
        for file in os.listdir(self.processed_path):
            with open(f"{self.processed_path}/{file}", 'r') as f:
                text_words = f.readline().split(' ')
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
        return self.tf(term, doc_path) * self.idf(term)


if __name__ == "__main__":
    vm = VectorModel('assets/articles/processed')

    print(vm.tf('star',
                'assets/articles/processed/‘Hidden Figures’ Ties ‘Rogue One’ at Box Office - The New York Times'))

    print(vm.df('star'))
    print(vm.idf('star'))
    print(vm.tf_idf_weight(
        'star', 'assets/articles/processed/‘Hidden Figures’ Ties ‘Rogue One’ at Box Office - The New York Times'))
