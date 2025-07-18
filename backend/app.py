from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.pdf_parser import extract_text_from_pdf, split_text_into_chunks
from utils.embedder import embed_and_save
from utils.retriever import retrieve_answer
from utils.ai_responder import generate_response
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload PDF and process it
# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            # Step 1: Extract text
            text = extract_text_from_pdf(filepath)
            # Step 2: Split into chunks
            chunks = split_text_into_chunks(text)
            # Step 3: Embed and save
            embed_and_save(chunks)
        except Exception as e:
            return jsonify({'error': f'Processing failed: {str(e)}'}), 500

        return jsonify({'message': 'PDF uploaded and processed successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/chat', methods=['POST'])
def chat_with_pdf():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({'error': 'Query is required.'}), 400

        user_query = data["query"]

        # Step 1: Load embedder
        try:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            return jsonify({'error': f'Embedder load failed: {str(e)}'}), 500

        # Step 2: Retrieve matched context
        try:
            result = retrieve_answer(user_query, embedder)
        except Exception as e:
            return jsonify({'error': f'Retrieve answer failed: {str(e)}'}), 500

        # Step 3: Generate response
        try:
            context = result.get("context", "")
            if not context:
                return jsonify({'error': 'No relevant context found for your query.'}), 404

            response = generate_response(user_query, context)
        except Exception as e:
            return jsonify({'error': f'Generate response failed: {str(e)}'}), 500

        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
