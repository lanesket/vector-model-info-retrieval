import pandas as pd
from Preprocessor import Preprocessor


# data from kaggle dataset https://www.kaggle.com/snapcrack/all-the-news
# csv to concrete number of article text files
def parse_csv_data(csv_path: str, limit: int):
    data = pd.read_csv(csv_path)
    p = Preprocessor("assets/stop-words.txt")

    for index, row in data.iterrows():
        if index > limit - 1:
            return

        print(f"Status: {index + 1} / {limit} \r", end="")

        processed = ' '.join(p.process(row['content']))
        raw_path = f"assets/articles/raw/{row['title'].replace('/', '')}"
        pr_path = f"assets/articles/processed/{row['title'].replace('/', '')}"

        f = open(raw_path, "w+")
        f.write(row['content'])
        f.close()

        f = open(pr_path, "w+")
        f.write(processed)
        f.close()
    print("Done.")


if __name__ == "__main__":
    parse_csv_data('assets/articles/articles1.csv', 200)
