from curate import curate, db

with curate.app_context():
    db.create_all()