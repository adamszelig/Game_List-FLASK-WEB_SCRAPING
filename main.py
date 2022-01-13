from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from game_scraping import get_game_data
import pandas as pd

app = Flask(__name__)

# CREATE  DYNAMIC FOOTER DATE
@app.context_processor
def inject_now():
    return {'footer_year': datetime.now().year}


@app.route('/')
def home():
    get_game_data()
    df = pd.read_csv("game.csv")
    return render_template("index.html", data=df, len=len(df))


if __name__ == '__main__':
    app.run(debug=True)

# <h5 class="card-title"><a href={{game['link'}}>{{game['title'}}</a></h5>
# genre