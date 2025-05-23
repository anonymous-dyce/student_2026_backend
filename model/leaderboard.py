from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
import logging

# leaderboard DATABASE
class LeaderboardEntry(db.Model):
    """
    LeaderboardEntry Model
    """
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.String(255), nullable=False)

    def __init__(self, player_name, score):
        self.player_name = player_name
        self.score = score

    def __repr__(self):
        return f"<LeaderboardEntry(id={self.id}, player_name='{self.player_name}', score='{self.score}')>"

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            "id": self.id,
            "player_name": self.player_name,
            "score": self.score,
        }

    def update(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error updating leaderboard entry: {e}")
            db.session.rollback()
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            logging.error(f"Error deleting leaderboard entry: {e}")
            db.session.rollback()
            return False

    @staticmethod
    def restore(data):
        with app.app_context():
            db.session.query(LeaderboardEntry).delete()
            db.session.commit()

            restored_entries = {}
            for entry_data in data:
                if 'player_name' in entry_data and 'score' in entry_data:
                    entry = LeaderboardEntry(
                        player_name=entry_data['player_name'],
                        score=entry_data['score']
                    )
                    entry.create()
                    restored_entries[entry_data['id']] = entry
                else:
                    print(f"Invalid data: {entry_data}")
            return restored_entries

def initLeaderboard():
    """
    Initializes the Leaderboard table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  
        
        entries = [
            LeaderboardEntry(player_name="Elon Musk", score=98),
        ]
        for entry in entries:
            try:
                entry.create()
                print(f"Created leaderboard entry: {repr(entry)}")
            except IntegrityError as e:
                db.session.rollback()
                print(f"Record already exists or error occurred: {str(e)}")
