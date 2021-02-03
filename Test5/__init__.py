
from flask import Flask, request, send_from_directory, render_template, jsonify, make_response
import os
from hashlib import sha256
import json
from random import random
import requests

app = Flask(__name__)

prizes = ("Chocolate", "Strawberry Starburst", "Cherry Starburst", "Orange Starburst", "Lemon Starburst")
probabilities = (0.4, 0.15, 0.15, 0.15, 0.15)
assert sum(probabilities) == 1
assert len(prizes) == len(probabilities)


GITHUB_TOKEN = "secret token here"
USED_CODES_PATH = "static/used_codes.json"


hashes = requests.get("https://pastebin.com/raw/DUV5ztr1").text.split("\n")
hashes = [x.strip('\r') for x in hashes]
#print(hashes)



def save_used_codes(used_codes):
    #this uses github gists to save our used codes file

    gist_id="9099922858882e94fdb16ca3c9293dfa"

    content=json.dumps(used_codes, indent = 4, sort_keys=True)
    filename = "gashapon_used_codes"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    r = requests.patch('https://api.github.com/gists/' + gist_id, data=json.dumps({'files':{filename:{"content":content}}}),headers=headers) 
    #print(r.json())
    with open(USED_CODES_PATH, 'w') as f:
        f.write(content)

def get_used_codes():
    with open(USED_CODES_PATH) as f:
        return json.load(f)


def pick_randomly():
    #this number randomly picks a number from 1 to n inclusive (assuming there are n different types of prizes) according the the weighted probabilities
    num = random()
    for i in range(len(prizes)):
        num -= probabilities[i]
        if num < 0:
            return i + 1
    print("this should never really happen")
    return len(prizes) + 1



@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/getcode", methods = ["POST"])
def handle_code():
    used_codes = get_used_codes()
    
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
            result = pick_randomly()
            

            used_codes[code] = prizes[result - 1]

            save_used_codes(used_codes)

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