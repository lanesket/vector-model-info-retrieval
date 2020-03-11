import pandas as pd
from Preprocessor import Preprocessor
from Article import Article

csv_name = 'assets/articles/articles1.csv'
data = pd.read_csv(csv_name)

p = Preprocessor("assets/stop-words.txt")

for index, row in data.iterrows():
    print(index)
    processed = ' '.join(p.process(row['content']))
    a = Article(row['title'], row['content'], processed)
    a.insert()
