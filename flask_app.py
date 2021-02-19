from flask import Flask, request
app = Flask(__name__)

import os
import sqlite3

def update_group(group_name, enabled):
  conn = sqlite3.connect("../pihole/etc-pihole/gravity.db")
  c = conn.cursor()
  c.execute("update 'group' set enabled = ? where name like ?;", (enabled, "%" + group_name + "%"))
  conn.commit()
  conn.close()

def update_pihole():
  os.system("docker exec pihole pihole restartdns reload-lists")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/enable/<int:flag>")
def enable(flag):
  update_group("Kids", flag)
  update_pihole()
  return "Success"

@app.route("/update_group", methods=["POST"])
def update():
  group_name = request.args.get('group', '')
  if group_name == '':
    return "No group name specified"
  enabled = int(request.args["enabled"])
  update_group(group_name, enabled)
  update_pihole()
  return "Success"
  

