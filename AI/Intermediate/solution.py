from flask import Flask, request, render_template
import pickle
import subprocess
import torch  # Add PyTorch for model loading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_file = request.files['model']
        try:
            # Load the model using PyTorch
            model = torch.load(model_file)
            return 'Model loaded successfully!'
        except Exception as e:
            return f'Error: {e}'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)