
from flask import Flask, request, send_from_directory, render_template, jsonify, make_response
import os
from hashlib import sha256
import json
import random
import requests

app = Flask(__name__)

prizes = ("Chocolate", "Starburst")
probabilities = (0.5, 0.5)
assert sum(probabilities) == 1
assert len(prizes) == len(probabilities)


GITHUB_TOKEN = "a5e19f669cb256593788a27b1995f0e61dcee83e"


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

def get_used_codes():
    url = "https://gist.githubusercontent.com/EricWu2003/9099922858882e94fdb16ca3c9293dfa/raw/gashapon_used_codes"
    used_codes = json.loads(requests.get(url).text)
    return used_codes


used_codes = get_used_codes()





@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/getcode", methods = ["POST"])
def handle_code():
    global used_codes
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
        print(repr(code))
        print(repr(used_codes))
        if code not in used_codes.keys():
            result = random.randint(1, len(prizes))

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