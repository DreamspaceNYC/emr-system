
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.auth import verify_admin_email, authenticate_pin
from utils.qr import generate_qr, fetch_patient_by_qr
from db.database import db, get_patient_by_id, save_patient
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/api/generate-qr', methods=['POST'])
def generate_qr_code():
    data = request.json
    patient_id = str(uuid.uuid4())
    data["id"] = patient_id
    save_patient(data)
    qr_token = generate_qr(patient_id)
    return jsonify({"status": "success", "qr_token": qr_token, "patient_id": patient_id})

@app.route('/api/scan-qr/<token>', methods=['GET'])
def scan_qr(token):
    patient = fetch_patient_by_qr(token)
    if not patient:
        return jsonify({"status": "error", "message": "QR not found"}), 404
    return jsonify({"status": "success", "patient": patient})

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    if verify_admin_email(data.get("email")):
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Unauthorized"}), 401

@app.route('/api/patient-login', methods=['POST'])
def patient_login():
    data = request.json
    success = authenticate_pin(data.get("hospital_number"), data.get("pin"))
    if success:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid PIN"}), 403

if __name__ == '__main__':
    app.run(debug=True)
