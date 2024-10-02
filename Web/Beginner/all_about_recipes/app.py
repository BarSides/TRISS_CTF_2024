from flask import Flask, render_template, make_response
from random import randint, random

app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


def random_flag():
    return ("Not this food.", "Maybe another one.", "Still hungry, keep clicking.")[randint(0, 2)]


@app.route('/food/<name>')
def food(name):
    r = make_response(render_template("food.html", name=name))
    if name == "cookie":
        r.set_cookie("flag", "Barsides{792e24bc-749f-4587-aeb7-a526a928f898}")
    else:
        r.set_cookie("flag", random_flag())
    return r


if __name__ == '__main__':
    app.run(port=8002, debug=True)
