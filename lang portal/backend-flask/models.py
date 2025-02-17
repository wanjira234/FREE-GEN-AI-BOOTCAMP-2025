from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kanji = db.Column(db.String(255), nullable=False)
    romaji = db.Column(db.String(255), nullable=False)
    english = db.Column(db.String(255), nullable=False)
    parts = db.Column(db.JSON, nullable=False)
    correct_count = db.Column(db.Integer, default=0)
    wrong_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'kanji': self.kanji,
            'romaji': self.romaji,
            'english': self.english,
            'parts': self.parts,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count
        }

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    words_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'words_count': self.words_count
        }

class WordGroup(db.Model):
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)

class StudyActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    study_activity_id = db.Column(db.Integer, db.ForeignKey('study_activity.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class WordReviewItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    study_session_id = db.Column(db.Integer, db.ForeignKey('study_session.id'), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())