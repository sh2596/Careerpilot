# backend/app/routes/jobs.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Job

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()
    jobs = Job.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'description': job.description,
        'status': job.status,
        'created_at': job.created_at.isoformat()
    } for job in jobs])

@jobs_bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ['title', 'company']
    if not all(k in data for k in required):
        return jsonify({"msg": "Title and company required"}), 400

    job = Job(
        title=data['title'],
        company=data['company'],
        description=data.get('description', ''),
        status=data.get('status', 'Applied'),
        user_id=user_id
    )
    db.session.add(job)
    db.session.commit()

    return jsonify({
        "id": job.id,
        "msg": "Job created"
    }), 201