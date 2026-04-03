"""
How to view webpage: 
  - run `python app.py` on Terminal.
  - There will be a link being printed out (usually http://127.0.0.1:5000)
  - Copy and paste the local host address to Safari.
  - To reflect the changes in code, I should refresh the Safari page.
  - To exit, press CTRL+C

The new version does not list the articles using database.
"""

import os, nbformat, json
from pathlib import Path
from nbconvert import HTMLExporter
from traitlets.config import Config
from flask import Flask, render_template # , send_from_directory, Response

app = Flask(__name__)
scriptPath = os.path.dirname(os.path.abspath(__file__)) # /Users/raymondkil/Desktop/raykil.github.io

def ipynb2html(ipynb_path):
    c = Config()
    c.HTMLExporter.embed_images = True
    c.HTMLExporter.exclude_input_prompt = True
    c.HTMLExporter.exclude_output_prompt = True
    nb = nbformat.read(ipynb_path, as_version=4)
    exporter = HTMLExporter(config=c, template_name="lab")
    body = exporter.from_notebook_node(nb)[0]
    return body

@app.route('/') # run the attached function when the URL in the arg is requested.
def index():
    # TODO: Let's animate some cool methematical animation at homepage.
    # Mandelbrot set
    # John Conway's Game of Life
    # Something related to coordinate transformation in gen rel
    # See animation_idea.txt for more.
    return render_template('index.html')

@app.route('/about')
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


@app.route('/articles/<dirname>/')
def get_articles_info(dirname):
    article_dir = f"{scriptPath}/articles/{dirname}"

    # Finding ipynb notebooks
    # TODO: change this so that I can display all ipynbs. Ipynbs should be named as 01_hello.ipynb, 02_my.ipynb, ... so that the order is manually specified.
    notebook_name = [ipynb for ipynb in os.listdir(article_dir) if '.ipynb' in ipynb]
    ipynb_path = os.path.join(article_dir, notebook_name[0])
    nb_html = ipynb2html(ipynb_path)

    # Pass in title in article page.
    # with open(f"{scriptPath}/articles/{dirname}/title.txt", 'r') as t: title = t.read().strip() or dirname
    return render_template("article.html", dirname=dirname, nb_html=nb_html)

@app.route('/omok')
def omok():
    return render_template('omok.html')

# @app.route('/particles')
# def particles():
#     return render_template('particles.html')


if __name__ == "__main__":
    app.run(debug=True)