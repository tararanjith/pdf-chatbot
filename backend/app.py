from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from utils.pdf_parser import extract_text_from_pdf
from utils.embedder import embed_text_chunks, embedder  # Import embedder model instance
from utils.retriever import retrieve_answer
from utils.ai_responder import generate_response

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

session_embeddings = {}

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('pdf')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    chunks = extract_text_from_pdf(filepath)
    embeddings = embed_text_chunks(chunks)

    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    session_embeddings[session_id] = {
        'chunks': chunks,
        'embeddings': embeddings,
        'history': []
    }

    return jsonify({'message': 'File uploaded and processed successfully'})


@app.route('/chat', methods=['POST'])
def chat():
    print("Raw request data:", request.data)
    data = request.get_json()
    print("Parsed JSON:", data)

    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    query = data.get('query')
    history = data.get('history', [])

    if not query:
        return jsonify({'error': 'Missing query'}), 400

    session_id = session.get('session_id')
    if not session_id or session_id not in session_embeddings:
        return jsonify({'error': 'No document uploaded yet'}), 400

    chunks = session_embeddings[session_id]['chunks']
    embeddings = session_embeddings[session_id]['embeddings']

    matched_chunks = retrieve_answer(query, chunks, embeddings, embedder)
    response = generate_response(query, matched_chunks, history)

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": response})
    session_embeddings[session_id]['history'] = history

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
