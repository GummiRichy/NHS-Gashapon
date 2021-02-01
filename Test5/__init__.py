
from flask import Flask, request, send_from_directory, render_template, jsonify, make_response
import os

app = Flask(__name__)



#with open('index.html') as f:
#        html_source_code = f.read()


@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/getcode", methods = ["POST"])
def handle_code(): 
    req = request.get_json()
    
    print(req)
    print(type(req))

    if not type(req) == type(""):
        res = make_response(jsonify(4), 200)
        return res

    if not req.isdigit():
        res = make_response(jsonify(4), 200)
        return res

    code = int(req)


    
    if code %17 == 0:
        res = make_response(jsonify(1), 200)
        return res
    else:
        res = make_response(jsonify(4), 200)
        return res




    




if __name__ == "__main__":
        app.run(host = "0.0.0.0", port = 80)