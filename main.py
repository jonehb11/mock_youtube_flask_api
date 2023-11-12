from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "Video(name={},views={},liked={})".format(name,views,likes)


db.create_all()



Video_put_args = reqparse.RequestParser()
Video_put_args.add_argument("name", type=str, help="Name of video")
Video_put_args.add_argument("views", type=int, help="views of video")
Video_put_args.add_argument("likes", type=int, help="likes of video")

resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='video is not found')
        
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = Video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message='video id already taken')
        video = VideoModel(id=video_id,name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
        
    def delete(self, video_id):
        args = Video_put_args.parse_args()
        video = VideoModel(id=video_id,name = args['name'], views = args['views'], likes = args['likes'])
        db.session.delete(video)
        db.session.commit()
        return 204

        
         


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
