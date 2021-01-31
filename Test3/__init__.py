
from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)



#with open('index.html') as f:
#        html_source_code = f.read()


@app.route("/")
def home(): 
    return render_template("index.html")


@app.route('/js/<path:filename>')
def serve_static(filename):

    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'js'), filename)


if __name__ == "__main__":
        app.run(host = "0.0.0.0", port = 80)
