#!env/bin/python
"""
    Web Application main file (for future use)
"""

import flask

# Create flask application
app = flask.Flask(__name__)

@app.route('/')
def index():
    """ Index """
    return flask.render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

