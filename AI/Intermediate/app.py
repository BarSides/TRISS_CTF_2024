import os
import random
import string
import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nobody_cares')

# Configure Flask-Session with a server-side session store
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Get the CTF flag from the environment variable
CTF_FLAG = os.environ.get('CTF_FLAG')

# Define a list of words to choose from
WORDS = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'pear', 'quince', 'raspberry', 'strawberry', 'tangerine', 'watermelon', 'zucchini', 'tomato', 'potato', 'spinach']

# Store the solutions and captcha images in memory, associated with the session ID
solutions = {}
captcha_images = {}

# Define a helper function to generate a captcha image
def generate_captcha():
    # Choose two random words from the list
    word1, word2 = random.sample(WORDS, 2)

    # Create a new image
    width, height = 300, 200
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Draw the words on the image
    font = ImageFont.truetype('LiberationSans-Regular.ttf', 36)
    draw.text((10, 10), word1, font=font, fill='black')
    draw.text((10, 60), word2, font=font, fill='black')

    # Generate a random filename for the captcha image
    image_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=64)) + '.png'
    image_path = os.path.join('static', image_filename)
    image.save(image_path)

    return word1 + ' ' + word2, image_filename

# Route for generating a new session and captcha
@app.route('/', methods=['GET', 'POST'])
def index():
    informative_message = 'Solve 1000 captchas to get the flag.'
    if request.method == 'POST':
        time.sleep(0.5)
        # Verify the submitted captcha solution
        solution = request.form['solution']
        correct_solution = solutions.get(session.get('session_id'))
        if solution == correct_solution:
            session['solved'] = session.get('solved', 0) + 1
            if session['solved'] == 1000:
                # The user has solved 100 captchas, provide the flag
                return f'Congratulations! You have solved 1000 captchas. The flag is: {CTF_FLAG}'
            informative_message = 'Correct solution. Solved captchas: ' + str(session['solved'])
        else:
            session['attempts'] = session.get('attempts', 0) + 1
            if session['attempts'] > 100:
                # The user has exceeded the maximum number of attempts, expire the session
                session.clear()
                return 'Too many failed attempts. Your session has expired.'
            informative_message = 'Incorrect solution. Please try again.'

    # Generate a new captcha and store the solution and image in memory
    solution, image_filename = generate_captcha()

    # If we already have a session_id look for captcha_images[session_id] and solutions[session_id] and delete them from memory and the filesystem
    last_captcha = session.get('session_id')
    if last_captcha:
        rm_image_path = os.path.join('static', captcha_images[last_captcha])
        os.remove(rm_image_path)
        del captcha_images[last_captcha]
        del solutions[last_captcha]
    
    session_id = session.get('session_id', ''.join(random.choices(string.ascii_letters + string.digits, k=64)))
    session['session_id'] = session_id
    solutions[session_id] = solution
    captcha_images[session_id] = image_filename

    return render_template('index.html', informative_message=informative_message, image_filename=captcha_images[session_id])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")