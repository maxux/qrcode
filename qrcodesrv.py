import os
import sys
import json
import hashlib
import qrcode
import qrcode.image.svg
from datetime import datetime
from flask import Flask, request, jsonify, render_template, abort, make_response

class QRCodeServer:
    def __init__(self):
        self.app = Flask(__name__, static_url_path='/static')
        self.app.url_map.strict_slashes = False

        self.gitsha = self.gitsharoot()
        print(f"[+] running code revision: {self.gitsha}")

    def gitsharoot(self):
        try:
            ref = ""

            with open(".git/HEAD", "r") as f:
                head = f.read()
                if not head.startswith("ref:"):
                    return None

                ref = head[5:].strip()

            with open(f".git/{ref}", "r") as f:
                sha = f.read()
                return sha[:8]

        except Exception as e:
            print(e)
            return None

    def routes(self):
        @self.app.context_processor
        def inject_now():
            return {'now': datetime.utcnow()}

        @self.app.route('/download', methods=['POST'])
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

        @self.app.route('/generate', methods=['POST'])
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

        @self.app.route('/', methods=['GET'])
        def index():
            content = {"revision": self.gitsha}
            return render_template("create.html", **content)

if __name__ == "qrcodesrv":
    root = QRCodeServer()
    root.routes()
    app = root.app
