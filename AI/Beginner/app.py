from flask import Flask, request, render_template, jsonify
import torch
import os
import logging

app = Flask(__name__)

# Configure logging
# logging.basicConfig(filename='app.log', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s: %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')
# Log to stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Set a maximum file size of 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 10

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'model' not in request.files:
            logging.error('No model file uploaded')
            return jsonify({'error': 'No model file uploaded'}), 400

        model_file = request.files['model']
        if model_file.filename == '':
            logging.error('No selected file')
            return jsonify({'error': 'No file selected'}), 400

        if model_file and allowed_file(model_file.filename):
            try:
                # Load the model using PyTorch
                model = torch.load(model_file, weights_only=False)
                logging.info('Model loaded successfully')
                return jsonify({'message': 'Model loaded successfully'})
            except Exception as e:
                logging.error(f'Error loading model: {e}')
                return jsonify({'error': f'Error loading model: {e}'}), 500
        else:
            logging.error('Invalid file type')
            return jsonify({'error': 'Invalid file type'}), 400

    return render_template('index.html')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pt', 'pth'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8893)