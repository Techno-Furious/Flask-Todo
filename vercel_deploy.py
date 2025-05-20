import os
from app import app as flask_app

# Add memory-only db initialization if needed
if os.environ.get('VERCEL_REGION'):
    from app import db
    with flask_app.app_context():
        db.create_all()

# Export the Flask app for Vercel
app = flask_app