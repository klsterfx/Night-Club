from flask import Flask
from flask_restful import Resource, Api
from api.club_api import *

app = Flask(__name__)
api = Api(app)

api.add_resource(Init, '/manage/init') #Management API for initializing the DB
api.add_resource(Version, '/manage/version') #Management API for checking DB version
api.add_resource(Login, '/login') 
api.add_resource(Users, '/users', '/users/<string:username>') 

api.add_resource(Clubs, '/clubs', '/clubs/<string:clubname>')  
api.add_resource(Entered, '/clubs/<string:clubname>/entry') 

api.add_resource(ClubsInfo, '/clubs/<string:clubname>/info')
api.add_resource(ClubsFilter, '/clubs/filter')

api.add_resource(Managers, '/managers') 
api.add_resource(Bouncers, '/bouncers') 

api.add_resource(Reservation, '/clubs/<int:id>/reservation') 
api.add_resource(WaitList, '/clubs/<int:id>/waiting-list') 

if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True)
