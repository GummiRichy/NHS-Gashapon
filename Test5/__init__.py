
from flask import Flask, request, send_from_directory, render_template, jsonify, make_response
import os
from hashlib import sha256
import json
import random

app = Flask(__name__)

prizes = ("Chocolate", "Starburst")
probabilities = (0.5, 0.5)
assert sum(probabilities) == 1
assert len(prizes) == len(probabilities)


with open('static/hashes.txt') as f:
    hashes = f.readlines()
    hashes = [x.strip() for x in hashes]
with open('static/used_codes.json') as f:
    used_codes = json.load(f)


@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/getcode", methods = ["POST"])
def handle_code(): 
    code = request.get_json()
    
    #print(req)
    #print(type(req))

    if not type(code) == type(""):
        res = make_response(jsonify(0), 200)
        return res

    if not code.isdigit():
        res = make_response(jsonify(0), 200)
        return res

    


    if sha256(code.encode('utf-8')).hexdigest() in hashes:
        if code not in used_codes.keys():
            result = random.randint(1, len(prizes))

            used_codes[code] = prizes[result - 1]

            with open("static/used_codes.json", 'w') as f:
                f.write(json.dumps(used_codes))

            res = make_response(jsonify(result), 200)
            return res
        else:
            result = prizes.index(used_codes[code]) + 1
            result = -result
            res = make_response(jsonify(result), 200)
            return res
    else:
        res = make_response(jsonify(0), 200)
        return res




    




if __name__ == "__main__":
        app.run(host = "0.0.0.0", port = 80)