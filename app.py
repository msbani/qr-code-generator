from flask import Flask, render_template, request, jsonify
import qrcode
import io
import base64

app = Flask(__name__)

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
def generate():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"eoor": "No URL provided"}), 400
    
    qr_image = generate_qr_image(url)
    return jsonify({"qr_image": qr_image})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
