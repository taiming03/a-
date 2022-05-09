from flask import Flask, render_template, make_response, request
from threading import Thread
from datetime import datetime

app = Flask('')

@app.route('/')
def main():
  #now = datetime.now()
  #return render_template('hello.html', **locals())
  return "✅   啟動成功!"
def run():
  try:
    app.run(host="0.0.0.0", port=8080)
  except OSError:
        pass

def keep_alive():
    server = Thread(target=run)
    server.start()
