from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Task, UserSchema, TaskSchema

class Signup(Resource):
    def post(self):
        data = request.get_json()

        try:
            user = User(
                username=data.get('username')
            )

            user.password_hash = data.get('password')

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            user_json = UserSchema().dump(user)

            return user_json, 201
        except Exception as error:
            db.session.rollback()

            return {
                'errors': [str(error)]
            }, 422


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = db.session.get(User, user_id)

        if not user:
            session.pop("user_id", None)
            return {"error": "Unauthorized"}, 401

        return UserSchema().dump(user), 200


class Login(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(
            username=data.get('username')
        ).first()

        if user and user.authenticate(data.get('password')):
            session['user_id'] = user.id

            user_json = UserSchema().dump(user)

            return user_json, 200
        
        return {"error": "Unauthorized"}, 401

class Logout(Resource):
    def delete(self):
        user_id = session.get("user_id")

        if user_id:
            session.pop('user_id', None)
            return "", 204
    
        return {"error": "Unauthorized"}, 401



class TaskIndex(Resource):

    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401


        #
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        pagination = Task.query.filter_by(
            user_id=user_id
            ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
            )

        tasks_json = TaskSchema(many=True).dump(pagination.items)

        return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "items": tasks_json
        }, 200

    #both check save session to see if auth
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        #

        data = request.get_json() or {}

        try:
            task = Task(
            title=data.get("title"),
            description=data.get("description"),
            completed=data.get("completed", False),
            user_id=user_id
            )

            db.session.add(task)
            db.session.commit()

            return TaskSchema().dump(task), 201

        except Exception as error:
            db.session.rollback()

            return {
                "errors": [str(error)]
            }, 422



class TaskByID(Resource):
    #checks save session to see if auth
    def patch(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401


        #sql to filter, py to logic
        task = Task.query.filter_by(
            id=id,
            user_id=user_id
        ).first()

        if not task:
            return {"error": "Task not found"}, 404

        #
        data = request.get_json() or {}

        try:
            if "title" in data:
                task.title = data["title"]

            if "description" in data:
                task.description = data["description"]

            if "completed" in data:
                task.completed = data["completed"]

            db.session.commit()

            return TaskSchema().dump(task), 200

        except Exception as error:
            db.session.rollback()

            return {
                "errors": [str(error)]
            }, 422



    def delete(self, id):
        #checks save session to see if auth
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        #SQL to filter py to logic
        task = Task.query.filter_by(
            id=id,
            user_id=user_id
        ).first()

        #
        if not task:
            return {"error": "Task not found"}, 404

        db.session.delete(task)
        db.session.commit()

        return "", 204



            









api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TaskIndex, "/tasks", endpoint="tasks")
api.add_resource(TaskByID, "/tasks/<int:id>", endpoint="task_by_id")

if __name__ == '__main__':
    app.run(port=5555, debug=True)