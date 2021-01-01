from flask import Flask
app = Flask(__name__)

import os
import sqlite3

def update_database(enabled):
  conn = sqlite3.connect("../pihole/etc-pihole/gravity.db")
  c = conn.cursor()
  c.execute("update 'group' set enabled = ? where id = 1;", (enabled,))
  conn.commit()
  conn.close()

def update_pihole():
  os.system("docker exec pihole pihole restartdns reload-lists")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/enable/<int:flag>")
def enable(flag):
  update_database(flag)
  update_pihole()
  return "Success"
