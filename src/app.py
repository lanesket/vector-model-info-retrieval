from flask import Flask, render_template, request, redirect
from Preprocessor import Preprocessor
from VectorModel import VectorModel
from string import Template
import os

vm = VectorModel('assets/articles/processed')
# if not os.listdir('assets/articles/vectors'):
vm.generate_weights('assets/articles/vectors')
vectors = vm.load_vectors('assets/articles/vectors')
vm.create_inverted_index(vectors)
p = Preprocessor("assets/stop-words.txt")


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")



@app.route('/', methods=['POST', 'GET'])
def main_response():
    query = request.form['query']
    use_index = ""
    if request.method == "POST":
        use_index = request.form.get("use_index")
    processed_query = p.process(query)
    query_vector = vm.query_vectorize(processed_query)

    if ":" in query:
        pairs = query.split(" ")
        terms = []
        for pair in pairs:
            t, d, w = pair.partition(":")
            # vector_mapping returns position of a term in a vector
            # set only weights for the provided terms, since others are 0
            query_vector[vm.vector_mapping[t.lower()]] = int(w)
            terms.append(t)
        query = " ".join(terms)

    if use_index:
        res = vm.find_similar_with_index(vectors, query, query_vector)
    else:
        res = vm.find_similar(vectors, query_vector, 10)
    res = [ r.split("/")[-1] for r in res ]

    return render_template("index.html", qres=res)

@app.route("/article/<article_name>", methods=['POST'])
def full_article(article_name):
    text = ""
    try:
        with open("assets/articles/raw/" + article_name, "r") as f:
            text = f.read()
    except:
         text = "No such article found("
    return render_template("article.html", article_name=article_name, contents=text)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
