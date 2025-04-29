import base64
import numpy as np
import cv2
import face_recognition
from flask import Flask, request, jsonify
from flask_cors import CORS
from model.model import initialize_resources, generate_response
from model.face_recognition_utils import (
    load_known_faces,
    known_face_encodings,
    known_face_names,
)

app = Flask(__name__)
CORS(app)

# — Initialize your QA model & FAISS index —
initialize_resources()

# — Load known faces from model/Faculty_images/ —
load_known_faces()
if not known_face_names:
    app.logger.warning("No known faces loaded. Check your 'model/Faculty_images/' folder.")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Zabiverse API is running"})

@app.route("/api/query", methods=["POST"])
def query_handler():
    data = request.get_json(force=True)
    query = data.get("query", "").strip()
    history = data.get("chat_history", [])
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    try:
        response_text, updated_history = generate_response(query, history)
        return jsonify({
            "status": "success",
            "response": response_text,
            "chat_history": updated_history
        })
    except Exception as e:
        app.logger.error("Error in generate_response", exc_info=True)
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username", "")
    password = data.get("password", "")
    if username == "admin" and password == "1234":
        return jsonify({"status": "success", "message": f"Welcome, {username}"})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/api/facial-recognition", methods=["POST"])
def facial_recognition():
    data = request.get_json(force=True)
    img_b64 = data.get("image", "")
    if not img_b64:
        return jsonify({"status": "error", "message": "No image provided"}), 400

    # Strip off the Data URI scheme if present
    if "," in img_b64:
        _, img_b64 = img_b64.split(",", 1)

    try:
        img_bytes = base64.b64decode(img_b64)
        arr = np.frombuffer(img_bytes, np.uint8)
        bgr_img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    except Exception as e:
        app.logger.error(f"Failed to decode image: {e}")
        return jsonify({"status": "error", "message": "Invalid image data"}), 400

    # Detect faces and compute encodings
    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    if not face_encodings:
        return jsonify({"status": "error", "message": "No face detected"}), 404

    # Compare against known faces
    matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
    if any(matches):
        idx = matches.index(True)
        name = known_face_names[idx]
        return jsonify({"status": "success", "message": f"Hello, {name}!"})

    return jsonify({"status": "error", "message": "Face not recognized"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
