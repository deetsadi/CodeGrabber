import base64
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from get_text import get_ocr_text

app = Flask(__name__)
CORS(app)


@app.route('/getText', methods=['POST'])
def get_javascript_data():
    img_url = "../screenshot_info/image_to_decode.jpeg"

    encoded = request.get_json(force=True)["data"]
    decoded = base64.b64decode(encoded[23:])
    result=None
    with open(img_url, "wb") as f:
        f.write(decoded)
    
    result = get_ocr_text(img_url)
    return jsonify({"result":result})

app.run(port = 5000)