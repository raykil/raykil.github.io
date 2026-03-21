# Portfolio Website
The published website is [https://raykil.github.io](https://raykil.github.io).

## Webpage Development
For development, run `app.py` and use the localhost server `http://127.0.0.1:5000/` for quick iterations.

## Publish
Run `publish.py` to freeze and deploy the website in one step. It freezes the Flask app into static files in `build/`, then pushes them to the `static` branch on GitHub, which is what `raykil.github.io` serves.