from flask_restful import Resource, reqparse, request  #NOTE: Import from flask_restful, not python
from flask import jsonify
from api.swen610_db_utils import *
from api.club import *
import json


class Init(Resource):
    def post(self):
        rebuild_tables()

class Version(Resource):
    def get(self):
        return (exec_get_one('SELECT VERSION()'))

class ClubsInfo(Resource):
    def post(self, clubname):
        parser=reqparse.RequestParser()
        parser.add_argument('date', type=str, location='json')
        args=parser.parse_args()
        return jsonify(club_info(club_name=clubname, date = args['date']))

class ClubsFilter(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('population', type=str, location='json')
        parser.add_argument('income', type=str, location='json')
        args=parser.parse_args()
        return jsonify(club_filter( population = args['population'], income = args['income']))

class Clubs(Resource):
    def get(self):
        return jsonify(list_clubs())

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name', type=str, location = 'json')
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('opening_time', type=str, location='json')
        parser.add_argument('closing_time', type=str, location='json')
        args=parser.parse_args()
        return jsonify(insert_club(name=args['name'], capacity=args['capacity'], city=args['city'], 
                        opening_time=args['opening_time'],closing_time=args['closing_time'] ))

    def put(self,clubname):
        id = int(request.headers.get('session_id'))
        manager_name = request.headers.get('manager_name')
        parser=reqparse.RequestParser()
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('opening_time', type=str, location='json')
        parser.add_argument('closing_time', type=str, location='json')
        args=parser.parse_args()
        return jsonify(update_club(club_name=clubname, capacity=args['capacity'], city=args['city'], 
                        opening_time=args['opening_time'],closing_time=args['closing_time'], 
                        session_id=id, manager_name=manager_name))

    def delete(self,clubname):
        id = int(request.headers.get('session_id'))
        manager_name = request.headers.get('manager_name')
        return jsonify(del_club(club_name=clubname, session_id=id, manager_name=manager_name))

class Users(Resource):
    def get(self):
        return jsonify(list_users())

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name', type=str, location = 'json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('age', type=int, location='json')
        parser.add_argument('email', type=str, location='json')
        args=parser.parse_args()
        return jsonify(insert_user(name=args['name'], password=sha512(args['password'] ), age=args['age'] , email=args['email']))

    def put(self, username):
        id = int(request.headers.get('session_id'))
        parser=reqparse.RequestParser()
        parser.add_argument('age', type=int, location='json')
        parser.add_argument('email', type=str, location='json')
        args=parser.parse_args()
        return jsonify(update_user_info(name=username, age=args['age'] , email=args['email'], session_id=id))
        
    def delete(self, username):
        id = int(request.headers.get('session_id'))
        return jsonify(del_user(name=username, session_id=id))

class Reservation(Resource):
    def get(self):
        return (exec_get_one('SELECT VERSION()'))

class WaitList(Resource):
    def get(self):
        return (exec_get_one('SELECT VERSION()'))
        
class Entered(Resource):

    def post(self, clubname):
        id = int(request.headers.get('session_id'))
        bouncer_name = request.headers.get('bouncer_name')
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('enter_time', type=str, location='json')
        args=parser.parse_args()
        return jsonify(enter_club(bouncer_name=bouncer_name, session_id=id, user_name=args['username'], enter_time= args['enter_time'], club_name=clubname))

    
    def put(self, clubname):
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('amount_spent', type=int, location='json')
        parser.add_argument('left_time', type=str, location='json')
        args=parser.parse_args()
        return (leave_club(club_name=clubname, user_name=args['username'], amount_spent =args['amount_spent'], left_time=args['left_time']))
        
class Bouncers(Resource):
    def get(self):
        return jsonify(list_users())

    def post(self):
        id = int(request.headers.get('session_id'))
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str, location = 'json')
        parser.add_argument('clubname', type=str, location='json')
        parser.add_argument('manager_name', type=str, location='json')
        args=parser.parse_args()
        return jsonify(insert_bouncer(user_name=args['username'], club_name=args['clubname'], manager_name=args['manager_name'], session_id=id))
        
    def delete(self):
        id = int(request.headers.get('session_id'))
        username = request.headers.get('username')
        clubname = request.headers.get('clubname')
        manager_name = request.headers.get('manager_name')
        return jsonify(del_bouncer(user_name=username, club_name=clubname, manager_name=manager_name, session_id=id))

class Managers(Resource):
    def get(self):
        return jsonify(list_managers())

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str, location = 'json')
        parser.add_argument('clubname', type=str, location='json')
        args=parser.parse_args()
        return jsonify(insert_manager(user_name=args['username'], club_name=args['clubname']))

    def put(self):
        parser=reqparse.RequestParser()
        parser.add_argument('username', type=str, location = 'json')
        parser.add_argument('clubname', type=str, location='json')
        args=parser.parse_args()
        return jsonify(update_manager(user_name=args['username'], club_name=args['clubname']))
        
    def delete(self):
        username = request.headers.get('username')
        clubname = request.headers.get('clubname')
        return jsonify(del_manager(user_name=username, club_name=clubname))

class Login(Resource):

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('name', type=str, location = 'json')
        parser.add_argument('password', type=str, location='json')
        args=parser.parse_args()
        return jsonify(login_user(name=args['name'], password=sha512(args['password'])))
