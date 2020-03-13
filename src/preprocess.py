import pandas as pd
from Preprocessor import Preprocessor
from Article import Article

csv_name = 'assets/articles/articles1.csv'
data = pd.read_csv(csv_name)

p = Preprocessor("assets/stop-words.txt")

for index, row in data.iterrows():
    processed = ' '.join(p.process(row['content']))
    raw_path = f"assets/articles/raw/{row['title']}"
    pr_path = f"assets/articles/processed/{row['title']}"
    f = open(raw_path, "w+")
    f.write(row['content'])
    f.close()
    f = open(pr_path, "w+")
    f.write(processed)
    f.close()

    if index > 200:
        break