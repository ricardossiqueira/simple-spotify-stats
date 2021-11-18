from flask import Flask, render_template, Response
from spotify import get_current_song


app = Flask(__name__)


@app.route('/')
def index():
    render_data = get_current_song()
    svg = render_template('index.html.j2', **render_data)
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp
