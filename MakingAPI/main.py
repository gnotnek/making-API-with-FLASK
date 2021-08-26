from flask import Flask
from flask_restful import  Api, Resource,reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class videoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {views})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="name of the videos is required", required=True)
video_put_args.add_argument("views", type=int, help="views of the videos is required", required=True)
video_put_args.add_argument("likes", type=int, help="likes of the videos is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="name of the videos is required")
video_update_args.add_argument("views", type=int, help="views of the videos is required")
video_update_args.add_argument("likes", type=int, help="likes of the videos is required")

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        res = videoModel.query.filter_by(id=video_id).first()
        if not res:
            abort(404, "Couldn't find video with that id")
        return res

    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        res = videoModel.query.filter_by(id=video_id).first()
        if res:
            abort(409, message="Video already exist...")
        video = videoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        res = videoModel.query.filter_by(id=video_id).first()
        if not res:
            abort(404, message="Video doesn't exist...")
        if args['name']:
            res.name = args['name']
        if args['views']:
            res.views = args['views']
        if args['likes']:
            res.likes = args['likes']

        db.session.commit()
        return res

    def delete(self, video_id):
        res = videoModel.query.filter_by(id=video_id).first()
        if not res:
            abort(404, message="Video don't exist...")
        db.session.delete(res)
        db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)