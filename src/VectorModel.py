import os
import math


class VectorModel:
    @staticmethod
    def vector_mapping(processed_path: str):
        """
            Dict with word to its place in the vector
        """
        words = set()
        for file in os.listdir(processed_path):
            with open(f"{processed_path}/{file}", 'r') as f:
                text_words = f.readline().split(' ')
                words = words.union(set(text_words))

        return dict(zip(words, range(len(words))))

    @staticmethod
    def tf(term: str, doc_path: str) -> int:
        """
            Term frequency
            Number of times term (word) occured in doc
        """
        with open(doc_path, 'r') as f:
            text = f.readline()
            return text.count(term)

    @staticmethod
    def df(term: str, processed_path: str) -> int:
        """
            Document frequency
            Number of documents containing a term (word)
        """
        count = 0
        for file in os.listdir(processed_path):
            with open(f"{processed_path}/{file}", 'r') as f:
                if term in f.readline():
                    count += 1

        return count

    @staticmethod
    def idf(term: str, processed_path: str) -> float:
        """
            Inverse document frequency
        """
        doc_count = len(os.listdir(processed_path))

        return math.log(doc_count / VectorModel.df(term, processed_path))


if __name__ == "__main__":
    # print(VectorModel.vector_mapping('assets/articles/processed'))
    # print(VectorModel.tf('star',
    #                      'assets/articles/processed/‘Hidden Figures’ Ties ‘Rogue One’ at Box Office - The New York Times'))
    # print(VectorModel.df('star', 'assets/articles/processed'))
    # print(VectorModel.idf('star', 'assets/articles/processed'))
