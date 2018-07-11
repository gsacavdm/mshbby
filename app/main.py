from flask import Flask, request, json
app = Flask(__name__, static_url_path='/static')

import os
import uuid
import urllib2

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
def post():
  content = request.get_json()
  with file('votes.json', 'w') as f:
    f.write(json.dumps(content)) 
  return 'OK'

@app.route("/api/get2")
def get2():
  votes = "["
  for fn in os.listdir('/data/'):
    with file('/data/' + fn) as f:
      votes += f.read() + ","
  if (len(votes) != 1):
    votes = votes[:-1]
  votes += "]"
  return votes

@app.route("/api/post2", methods = ['POST'])
def post2():
  content = request.get_json()
  guid = uuid.uuid4().hex
  with file('/data/vote-' + guid + '.json', 'w') as f:
    f.write(json.dumps(content)) 

  try:
    email_url = os.getenv('EMAIL_URL')
    if (email_url != None):
      req = urllib2.Request(email_url)
      req.add_header('Content-Type', 'application/json')
      response = urllib2.urlopen(req, json.dumps(content))
  finally:
    app.logger.info("Unable to send email.")

  return 'OK'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')