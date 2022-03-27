from flask import Flask, render_template, request, redirect, flash
from errors import DownloadError
from downloader import download_link

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route("/")
def index():
    return render_template("index.html")
    

@app.route("/download", methods=["POST"])
def download():
    data = request.form
    series = data.get('series')
    season = data.get('season')
    episode = data.get('episode')
    
    try:
        link = download_link(series, int(season), int(episode))
        return redirect(link)
    except DownloadError as e:
        flash(f"{e}", category='error')
        return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0')