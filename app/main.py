from flask import Flask, request, json
app = Flask(__name__, static_url_path='/static')

import os

@app.route("/")
def main():
  with file('index.html') as f:
    index = f.read() 
  return index

@app.route("/api/get")
def get():
  with file('votes.json') as f:
    votes = f.read() 
  return votes

@app.route("/api/post", methods = ['POST'])
def put():
  content = request.get_json()
  with file('votes.json', 'w') as f:
    f.write(json.dumps(content)) 
  return 'OK'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')