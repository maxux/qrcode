import os
import sys
import json
import git
import hashlib
import qrcode
import qrcode.image.svg
from config import config
from flask import Flask, request, jsonify, render_template, abort, make_response

app = Flask(__name__, static_url_path='/static')
app.url_map.strict_slashes = False

repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha
gitsha = sha[0:8]

@app.route('/download', methods=['POST'])
def download():
    message = request.form.get("message")

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 25,
        border = 4,
        image_factory = qrcode.image.svg.SvgPathImage
    )

    qr.add_data(message)
    img = qr.make_image()

    response = make_response(img.to_string())
    response.headers["Content-Type"] = "image/svg+xml"
    response.headers['Content-Disposition'] = 'inline; filename=qrcode.svg'

    return response

@app.route('/generate', methods=['POST'])
def generate():
    payload = request.get_json()
    message = payload["message"]

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 25,
        border = 4,
        image_factory = qrcode.image.svg.SvgPathImage
    )

    qr.add_data(message)
    img = qr.make_image()

    response = make_response(img.to_string())
    # response.headers["Content-Type"] = "image/svg+xml"

    return response

@app.route('/', methods=['GET'])
def index():
    content = {"revision": gitsha}
    return render_template("create.html", **content)

print("[+] listening")
app.run(host=config['listen'], port=config['port'], debug=config['debug'], threaded=True)

