from flask import Flask, jsonify, request, render_template, send_file
import requests
from markup import for_markup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html', hidden_state = 'hidden')


@app.route('/upload_text', methods = ['POST', 'GET'])
def upload_text():
    url = 'http://host.docker.internal:7000/processing'
    text = request.form['text_input']
    toks = False
    lemmas = False
    if 'tokenization' in request.form:
        toks = True
    if 'lemmatisation' in request.form:
        lemmas = True
    json_text = {'input_text': text, 'tokenization': toks, 'lemmatisation': lemmas}
    
    response = requests.post(url, json=json_text)
    markup_text = for_markup(response.json()['output_text'])

    with open('data/doc.txt', 'w', encoding = 'utf-8') as f:
        f.write(response.json()['output_text'])


    return render_template('main.html', hidden_state = '', markup_text = markup_text, output_text = response.json()['output_text'])



@app.route('/upload_file', methods = ['POST', 'GET'])
def upload_file():
    url = 'http://host.docker.internal:7000/processing'
    uploaded_file = request.files['file_input']
    text = uploaded_file.read().decode('utf-8')
    toks = False
    lemmas = False
    if 'tokenization' in request.form:
        toks = True
    if 'lemmatisation' in request.form:
        lemmas = True
    json_text = {'input_text': text, 'tokenization': toks, 'lemmatisation': lemmas}
    
    response = requests.post(url, json=json_text)
    try:
        markup_text = for_markup(response.json()['output_text'])
    except:
        markup_text = response.json()['output_text']

    with open('data/doc.txt', 'w', encoding = 'utf-8') as f:
        f.write(response.json()['output_text'])

    return render_template('main.html', hidden_state = '', markup_text = markup_text, output_text = response.json()['output_text'])


@app.route('/download_file')
def download_file():
    return send_file('data/doc.txt')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api_docs')
def api_docs():
    return render_template('api.html')


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)