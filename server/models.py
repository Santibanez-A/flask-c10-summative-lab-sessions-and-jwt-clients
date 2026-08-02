from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=True)

    tasks = db.relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("Username is required.")

        return username

    @hybrid_property
    def password_hash(self):
        raise AttributeError(
            "Password hashes may not be viewed."
        )

    #bcrypt hashes the password
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    #authenticating the password in db to one passed
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password
        )



class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="tasks"
    )

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title is required.")

        return title


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()


class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    completed = fields.Bool()
    user_id = fields.Int()

    
