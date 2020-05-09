from flask import Flask, render_template, request, redirect
from Preprocessor import Preprocessor
from VectorModel import VectorModel


vm = VectorModel('assets/articles/processed')
vectors = vm.load_vectors('assets/articles/vectors')
p = Preprocessor("assets/stop-words.txt")


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def main_response():
    query = request.form['query']
    processed_query = p.process(query)
    query_vector = vm.query_vectorize(processed_query)
    res = vm.find_similar(vectors, query_vector, 5)

    return render_template("index.html", qres=res)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
