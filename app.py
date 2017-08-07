# -*- coding: utf-8 -*-

from flask import jsonify

from flask import Flask, request, abort

from bible import get_bible

app = Flask(__name__)

# For Kakao


@app.route('/message', methods=['POST'])
def message():
    data = request.json
    bible_verse = get_bible(script=data['content'])
    output = {"message": {"text": bible_verse}}
    return jsonify(output)


@app.route('/keyboard')
def keyboard():
    # return jsonify({
    #    "type": "buttons",
    #    "buttons": ["John3:16", "Ps119", "Acts3:1-3"]
    #})
    return jsonify({'type': 'text'})


@app.route('/')
def index():
    return get_bible(), 200

# We only need this for local development.
if __name__ == '__main__':
    app.run()
