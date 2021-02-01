
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

PASTEBIN_API_USER_KEY = "999a799fd183b4c140d4c0fafdd91448"
PASTEBIN_API_DEV_KEY = "d114f27662bc159b55db39b96dc050f8"


hashes = requests.get("https://pastebin.com/raw/DUV5ztr1").text.split("\n")
hashes = [x.strip('\r') for x in hashes]
#print(hashes)




def save_used_codes(used_codes):
    data = {
        'api_option': 'paste',
        'api_dev_key':PASTEBIN_API_DEV_KEY,
        'api_paste_code': json.dumps(used_codes, indent = 4, sort_keys=True),
        'api_paste_name': "used_codes",
        'api_paste_expire_date': 'N',
        'api_user_key': PASTEBIN_API_USER_KEY,
        'api_paste_format': 'json'
    }
  
    r = requests.post("https://pastebin.com/api/api_post.php", data=data)
    print("Paste send: ", r.status_code if r.status_code != 200 else "OK/200")
    print("Paste URL: ", r.text)
def get_used_codes():
    data = {
        'api_option': 'list',
        'api_dev_key':PASTEBIN_API_DEV_KEY,
        'api_user_key': PASTEBIN_API_USER_KEY,
        'api_results_limit': "1000"
    }
    r = requests.post("https://pastebin.com/api/api_post.php", data=data)
    url = r.text.split('paste_url')[-2].strip(">").strip("/").strip("<")
    
    url = "https://pastebin.com/raw/" + url.split('/')[-1]
    used_codes = json.loads(requests.get(url).text)
    return used_codes


used_codes = get_used_codes()


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