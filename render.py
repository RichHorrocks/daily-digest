#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import os
import sys
import fileinput
import constants as c
import create

app = Flask(__name__)

@app.route('/')
def render_index():
    return render_template(c.template)

@app.route('/goto')
def render_goto():
    line = request.args.get('line')
    direc = request.args.get('dir') 
    direc.replace('%26', '&')
    filename = c.feeds_dir + direc

    updated = False
    for x in fileinput.input(filename, inplace = 1):
        if int(x.split(' ', 1)[0]) == int(line):
            if 'NEW' in x:
                x = x.replace("NEW", "READ")
                updated = True
            url = x.rsplit(' ', 1)[1]
        print(x.rstrip())

    if updated:
        create.create_html()

    return redirect(url.rstrip(), 302)

if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader = False)