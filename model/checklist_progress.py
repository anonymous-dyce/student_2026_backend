from __init__ import db, app
from sqlalchemy.exc import SQLAlchemyError
import logging
import json

class ChecklistProgress(db.Model):
    __tablename__ = 'checklist_progress'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), nullable=False, unique=True)
    progress = db.Column(db.Text, nullable=False)  # Will store JSON string

    def __init__(self, user, progress):
        self.user = user
        self.progress = json.dumps(progress)  # store as string

    def __repr__(self):
        return f"ChecklistProgress(id={self.id}, user={self.user})"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        return self

    def read(self):
        return {
            "id": self.id,
            "user": self.user,
            "progress": json.loads(self.progress)
        }

    def update(self, new_progress):
        try:
            self.progress = json.dumps(new_progress)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            logging.error(f"Error updating checklist: {e}")
            db.session.rollback()
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initChecklists():
    """
    Initialize the ChecklistProgress table with a few users and default progress.
    """
    with app.app_context():
        db.create_all()

        example_checklists = [
            ChecklistProgress(user='student1', progress={
                "Install Python": True,
                "Download VS Code": False,
                "Clone GitHub Repo": False,
                "Set Up Linter": False
            }),
            ChecklistProgress(user='student2', progress={
                "Install Python": True,
                "Download VS Code": True,
                "Clone GitHub Repo": False,
                "Set Up Linter": False
            })
        ]

        for checklist in example_checklists:
            try:
                checklist.create()
                print(f"Added checklist for user: {checklist.user}")
            except Exception as e:
                db.session.remove()
                print(f"Error adding checklist for {checklist.user}: {e}")
