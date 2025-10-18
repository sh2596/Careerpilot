import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Resume
from app.utils.resume_parser import parse_resume
from flask_jwt_extended import jwt_required, get_jwt_identity

resumes_bp = Blueprint('resumes', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resumes_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({"msg": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        ext = os.path.splitext(filename)[1].lower()
        try:
            parsed = parse_resume(filepath, ext)
        except Exception as e:
            return jsonify({"msg": f"Parsing failed: {str(e)}"}), 500
        resume = Resume(
            filename=filename,
            user_id=user_id,
            raw_text=parsed['raw_text'],
            parsed_data={
                "name": parsed["name"],
                "email": parsed["email"],
                "phone": parsed["phone"],
                "skills": parsed["skills"]
            }
        )
        db.session.add(resume)
        db.session.commit()
        return jsonify({"id": resume.id, "parsed": resume.parsed_data}), 201
    return jsonify({"msg": "Invalid file type. Use .pdf or .docx"}), 400