"""
How to view webpage: 
  - run `python app.py` on Terminal.
  - There will be a link being printed out (usually http://127.0.0.1:5000)
  - Copy and paste the local host address to Safari.
  - To reflect the changes in code, I should refresh the Safari page.
  - To exit, press CTRL+C

The new version does not list the articles using database.
"""

import os, nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config
from flask import Flask, render_template, send_from_directory, Response

app = Flask(__name__)
scriptPath = os.path.dirname(os.path.abspath(__file__)) # /Users/raymondkil/Desktop/raykil.github.io

def ipynb2html(ipynb_path):
    Config().HTMLExporter.embed_images = True
    nb = nbformat.read(ipynb_path, as_version=4)
    exporter = HTMLExporter(config=Config(), template_name="lab")
    body = exporter.from_notebook_node(nb)[0]
    return body

@app.route('/')
def index():
    # TODO: Let's animate some cool methematical animation at homepage.
    # Mandelbrot set
    # John Conway's Game of Life
    # Something related to coordinate transformation in gen rel
    # See animation_idea.txt for more.
    return render_template('index.html')

@app.route('/articles')
def articles():
    slugs = [n for n in os.listdir(f"{scriptPath}/articles") if '.' not in n] # Ex) special_relativity
    articles_info = []
    for slug in slugs:
        with open(f"{scriptPath}/articles/{slug}/title.txt", 'r') as t: title = t.read().strip() or slug
        articles_info.append({'slug': slug, 'title': title})
    return render_template('articles.html', articles=articles_info)

@app.route('/articles/<slug>') # Ex) /articles/entropy
def get_articles_info(slug): # slug is a string, the name of article directory. Ex) special_relativity
    article_dir = f"{scriptPath}/articles/{slug}"

    # Finding ipynb notebooks
    # TODO: change this so that I can display all ipynbs. Ipynbs should be named as 01_hello.ipynb, 02_my.ipynb, ... so that the order is manually specified.
    notebook_name = [ipynb for ipynb in os.listdir(article_dir) if '.ipynb' in ipynb]
    ipynb_path = os.path.join(article_dir, notebook_name[0])
    nb_html = ipynb2html(ipynb_path)
    return render_template("article.html", slug=slug, nb_html=nb_html)

@app.route('/particles')
def particles():
    return render_template('particles.html')


if __name__ == "__main__":
    app.run(debug=True)