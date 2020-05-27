"""
:Author: PDT
:Since: 2020/05/24
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "TEST"


if __name__ == '__main__':
    app.run()
