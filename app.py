from flask import Flask, render_template, request, jsonify, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import qrcode
import io
import base64
import validators
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)
limiter.init_app(app)

def generate_qr_image(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    encoded = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
@limiter.limit("10 per minute")  # Limit per IP
def generate():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    logging.info(f"QR generation requested for URL: {url}")

    if not url:
        logging.warning("No URL provided")
        return jsonify({"error": "No URL provided"}), 400

    if not validators.url(url):
        logging.warning(f"Invalid URL format: {url}")
        return jsonify({"error": "Invalid URL format"}), 400

    # Generate QR code
    qr_image = generate_qr_image(url)
    logging.info(f"QR code generated successfully for URL: {url}")
    return jsonify({"qr_image": qr_image})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
