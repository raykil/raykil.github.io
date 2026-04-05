"""
Run `python app.py` on Terminal, and paste http://127.0.0.1:5000 (printed when the command is run) on Safari.
Use -q / --quarto to run `quarto render` before starting the server.
Raymond Kil, April 2026
"""

import os, json, argparse, subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
scriptPath = os.path.dirname(os.path.abspath(__file__))

def quarto2html(dirname):
    path = Path(scriptPath) / "quarto_articles" / "articles" / dirname / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return soup.find("main", id="quarto-document-content")

@app.route('/') # run the attached function when the URL in the arg is requested.
def index():
    # TODO: Let's animate some cool methematical animation at homepage.
    # Mandelbrot set
    # John Conway's Game of Life
    # Something related to coordinate transformation in gen rel
    # See animation_idea.txt for more.
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

def load_summaries() -> dict:
    p = Path(scriptPath) / "static" / "summaries.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_articles() -> dict:
    p = Path(scriptPath) / "articles" / "index.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.route('/articles/')
def articles():
    articles_to_show = load_articles()
    summaries = load_summaries()
    return render_template('articles.html', articles=articles_to_show, summaries=summaries)


@app.route('/articles/<dirname>/index_files/<path:filename>')
def article_files(dirname, filename):
    directory = Path(scriptPath) / "quarto_articles" / "articles" / dirname / "index_files"
    return send_from_directory(directory, filename)

@app.route('/articles/<dirname>/')
def get_articles_info(dirname):
    nb_html = quarto2html(dirname)
    return render_template("article.html", dirname=dirname, nb_html=nb_html)

@app.route('/omok/')
def omok():
    return render_template('omok.html')

# @app.route('/particles')
# def particles():
#     return render_template('particles.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quarto", action="store_true", help="If True, generates article page with Quarto, and saves to quarto_articles dir.")
    args = parser.parse_args()

    if args.quarto:
        subprocess.run(["quarto", "render"], cwd=scriptPath, check=True)

    app.run(debug=True)