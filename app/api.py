from flask import Flask, jsonify, request
from tag import Model, tag_text, output

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '<p>Our udpipe api</p>'


@app.route('/processing', methods=['GET', 'POST'])
def get_json():
    req_data = request.get_json()
    text = req_data['input_text']
    toks = req_data['tokenization']
    lemmas = req_data['lemmatisation']


    processed_text = tag_text(text, model1, model2, toks, lemmas)
    return jsonify({'output_text': processed_text})


if __name__ == '__main__':
    model1 = Model('rnc6,5.udpipe')
    model2 = Model('lemma_midrus.udpipe')
    app.run(host='0.0.0.0', port=7000, debug=True)
