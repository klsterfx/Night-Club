from flask_restful import Resource, reqparse, request  # Import from flask_restful, not python
from flask import jsonify
from .swen610_db_utils import *
from .club import *
import json

# This class handles the initialization of the database
class Init(Resource):
    def post(self):
        rebuild_tables()

# This class returns the database version
class Version(Resource):
    def get(self):
        return exec_get_one('SELECT VERSION()')

# This class handles the retrieval of club information
class ClubsInfo(Resource):
    def post(self, clubname):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, location='json')
        args = parser.parse_args()
        return jsonify(club_info(club_name=clubname, date=args['date']))
# This class handles filtered information about clubs based on certain criteria
class ClubsFilteredInfo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, location='json')
        parser.add_argument('population', type=str, location='json')
        parser.add_argument('earning', type=str, location='json')
        args = parser.parse_args()
        # Returns filtered club information based on population, earning, and date
        return jsonify(filterClubsInfo(population=args['population'], earning=args['earning'], date=args['date']))

# This class manages filtering options for clubs
class ClubsFilter(Resource):
    def get(self):
        # Retrieves available club locations
        return jsonify(get_club_locations())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('population', type=str, location='json')
        parser.add_argument('income', type=str, location='json')
        args = parser.parse_args()
        # Filters clubs based on population and income criteria
        return jsonify(club_filter(population=args['population'], income=args['income']))

# This class is used for operations related to clubs
class Clubs(Resource):
    def get(self):
        # Lists all clubs
        return jsonify(list_clubs())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('music', type=str, location='json')
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('yellow_threshold', type=str, location='json')
        parser.add_argument('count', type=int, location='json')
        parser.add_argument('increment', type=bool, location='json')
        parser.add_argument('decrement', type=bool, location='json')
        args = parser.parse_args()
        # Inserts a new club with the provided details
        return jsonify(insert_club(name=args['name'], city=args['city'], music=args['music'], capacity=args['capacity'], 
                                  yellow_threshold=args['yellow_threshold'], count=args['count'], increment=args['increment'],
                                  decrement=args['decrement']))

    def put(self, clubname):
        id = int(request.headers.get('session_id'))
        manager_email = request.headers.get('manager_email')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('music', type=str, location='json')
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('yellow_threshold', type=str, location='json')
        parser.add_argument('count', type=int, location='json')
        parser.add_argument('increment', type=bool, location='json')
        parser.add_argument('decrement', type=bool, location='json')
        args = parser.parse_args()
        # Updates a club's information based on the given data
        return jsonify(update_club(oldname=clubname, name=args['name'], city=args['city'], music=args['music'], capacity=args['capacity'], 
                                  yellow_threshold=args['yellow_threshold'], count=args['count'], increment=args['increment'],
                                  decrement=args['decrement'], session_id=id, manager_email=manager_email))

    def delete(self, clubname):
        # Deletes a club based on the provided name
        return jsonify(del_club(club_name=clubname))

# This class is responsible for handling user-related operations
class Users(Resource):
    def get(self):
        # Lists all users
        return jsonify(list_users())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('age', type=int, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('city', type=str, location='json')
        args = parser.parse_args()
        # Inserts a new user with encrypted password and provided details
        return jsonify(insert_user(name=args['name'], password=sha512(args['password']), age=args['age'], email=args['email'], city=args['city']))

    def put(self, username):
        id = int(request.headers.get('session_id'))
        parser = reqparse.RequestParser()
        parser.add_argument('age', type=int, location='json')
        parser.add_argument('email', type=str, location='json')
        args = parser.parse_args()
        # Updates user information based on provided details
        return jsonify(update_user_info(name=username, age=args['age'], email=args['email'], session_id=id))
        
    def delete(self, username):
        id = int(request.headers.get('session_id'))
        # Deletes a user based on username
        return jsonify(del_user(name=username, session_id=id))

# This class manages reservations for clubs
class Reservation(Resource):
    def get(self, clubname):
        # Lists reservations for a specified club
        return jsonify(list_reservaion(clubname))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('club', type=str, location='json')
        parser.add_argument('date', type=str, location='json')
        args = parser.parse_args()
        # Creates a new reservation with the provided details
        return jsonify(insert_reservation(email=args['email'], club=args['club'], date=args['date']))

    def delete(self):
        email = request.headers.get('email')
        club = request.headers.get('club')
        date = request.headers.get('date1')
        # Deletes a reservation based on email, club, and date
        return jsonify(del_reservation(email=email, club=club, date=date))

# This class is used to get specific system information
class WaitList(Resource):
    def get(self):
        # Retrieves and returns the database version
        return exec_get_one('SELECT VERSION()')
# This class manages entries into clubs
class Entered(Resource):

    def get(self, clubname):
        # Returns the current number of entries in a specified club
        return jsonify(current_entries_in_club(clubname))

    def post(self):
        id = int(request.headers.get('session_id'))
        bouncer_email = request.headers.get('bouncer_email')
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('club', type=str, location='json')
        args = parser.parse_args()
        # Records entry of a customer into a club
        return jsonify(enter_club(email=args['email'], club=args['club'], bouncer_email=bouncer_email, session_id=id))

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('club', type=str, location='json')
        parser.add_argument('amount_spent', type=int, location='json')
        args = parser.parse_args()
        # Records customer's departure from a club and their spending
        return leave_club(club=args['club'], email=args['email'], amount_spent=args['amount_spent'])

# This class handles customer related information
class Customers(Resource):

    def get(self, email):
        # Retrieves current club details for a specific customer
        return jsonify(current_club_customer(email))
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('music', type=str, location='json')
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('yellow_threshold', type=str, location='json')
        parser.add_argument('count', type=int, location='json')
        parser.add_argument('increment', type=bool, location='json')
        parser.add_argument('decrement', type=bool, location='json')
        args = parser.parse_args()
        # Updates club information based on customer preferences
        return jsonify(update_club_customer(oldname=args['name'], name=args['name'], city=args['city'], music=args['music'], capacity=args['capacity'], 
                                  yellow_threshold=args['yellow_threshold'], count=args['count'], increment=args['increment'],
                                  decrement=args['decrement']))

# This class is responsible for managing bouncers in clubs
class Bouncers(Resource):
    def get(self, clubname):
        # Lists all bouncers associated with a specific club
        return jsonify(list_bouncers(clubname))

    def post(self):
        id = int(request.headers.get('session_id'))
        manager_email = request.headers.get('manager_email')
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('club', type=str, location='json')
        args = parser.parse_args()
        # Assigns a bouncer to a club
        return jsonify(insert_bouncer(email=args['email'], club=args['club'], manager_email=manager_email, session_id=id))
        
    def delete(self):
        id = int(request.headers.get('session_id'))
        manager_email = request.headers.get('manager_email')
        email = request.headers.get('email')
        # Removes a bouncer from a club
        return jsonify(del_bouncer(email=email, manager_email=manager_email, session_id=id))
# This class manages operations related to club managers
class Managers(Resource):
    def get(self):
        # Retrieves a list of all managers
        return jsonify(list_managers())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('club', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        args = parser.parse_args()
        # Inserts a new manager for a specified club
        return jsonify(insert_manager(email=args['email'], club=args['club']))

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('clubname', type=str, location='json')
        args = parser.parse_args()
        # Updates manager details for a club
        return jsonify(update_manager(user_name=args['username'], club_name=args['clubname']))
        
    def delete(self):
        clubname = request.headers.get('clubname')
        # Deletes a manager from a specified club
        return jsonify(del_manager(club_name=clubname))

# This class retrieves information about clubs managed by a specific manager
class Manager_Club(Resource):
    def get(self, email):
        # Returns the club details managed by the given manager's email
        return jsonify(get_managers_club(email))

# This class retrieves information about clubs associated with a specific bouncer
class Bouncer_Club(Resource):
    def get(self, email):
        # Returns the club details where the given bouncer's email is associated
        return jsonify(get_bouncers_club(email))

# This class is responsible for updating the count of various aspects of clubs
class ClubCount(Resource):
    def put(self):
        id = int(request.headers.get('session_id'))
        bouncer_email = request.headers.get('bouncer_email')
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('city', type=str, location='json')
        parser.add_argument('music', type=str, location='json')
        parser.add_argument('capacity', type=int, location='json')
        parser.add_argument('yellow_threshold', type=str, location='json')
        parser.add_argument('count', type=int, location='json')
        parser.add_argument('increment', type=bool, location='json')
        parser.add_argument('decrement', type=bool, location='json')
        args = parser.parse_args()
        # Updates club count and other details based on provided information
        return jsonify(update_club_count(oldname=args['name'], name=args['name'], city=args['city'], music=args['music'], capacity=args['capacity'], 
                                  yellow_threshold=args['yellow_threshold'], count=args['count'], increment=args['increment'],
                                  decrement=args['decrement'], session_id=id, bouncer_email=bouncer_email))

# This class manages user login functionality
class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        args = parser.parse_args()
        # Validates user login using email and encrypted password
        return jsonify(login_user(email=args['email'], password=sha512(args['password'])))

# This class handles the retrieval of users who have not entered a club
class NotEnterend(Resource):
    def get(self):
        # Returns a list of users who have not entered any club
        return jsonify(list_not_entered())
