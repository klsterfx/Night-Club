from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from api.swen610_db_utils import *
from api.club_api import *
import coverage

def main(coverage_tracer_obj: coverage.Coverage = None):
    """
    Main function to start the Flask server. Initializes the Flask app, sets up CORS,
    and creates routes for the RESTful API. Optionally integrates with a coverage tracer object
    for code coverage analysis.
    """
    app = Flask(__name__)  # Create Flask instance
    CORS(app)  # Enable CORS on Flask server to work with Node.js pages
    api = Api(app)  # API router

    # Management APIs
    api.add_resource(Init, '/manage/init')  # Management API for initializing the DB
    api.add_resource(Version, '/manage/version')  # Management API for checking DB version

    # User-related APIs
    api.add_resource(Login, '/login')  # User login API
    api.add_resource(Users, '/users', '/users/<string:username>')  # User management API

    # Club-related APIs
    api.add_resource(Clubs, '/clubs', '/clubs/<string:clubname>')  # API for club management
    api.add_resource(Entered, '/clubs/entry', '/clubs/entry/<string:clubname>')  # API for club entries
    api.add_resource(NotEnterend, '/clubs/noentry')  # API for non-entered club users

    # Detailed club information APIs
    api.add_resource(ClubsInfo, '/clubs/<string:clubname>/info')  # API for specific club information
    api.add_resource(ClubsFilter, '/clubs/filter')  # API for filtering clubs
    api.add_resource(ClubCount, '/clubs/count')  # API for club count management
    api.add_resource(ClubsFilteredInfo, '/clubs/filterAll')  # API for comprehensive club filtering

    # Manager and bouncer related APIs
    api.add_resource(Managers, '/managers')  # API for managing club managers
    api.add_resource(Bouncers, '/bouncers', '/bouncers/<string:clubname>')  # API for managing club bouncers

    # APIs to get club information for bouncers and managers
    api.add_resource(Bouncer_Club, '/bouncers/clubs/<string:email>')  # API to get clubs associated with a bouncer
    api.add_resource(Manager_Club, '/managers/<string:email>')  # API to get clubs managed by a manager
    api.add_resource(Customers, '/customers/<string:email>', '/customers/leave')  # API for customer management

    # Reservation and waiting list APIs
    api.add_resource(Reservation, '/clubs/reservations', '/clubs/reservations/<string:clubname>')  # API for club reservations
    api.add_resource(WaitList, '/clubs/<int:id>/waiting-list')  # API for club waiting list

    # Optional route for stopping coverage tracing
    if coverage_tracer_obj is not None:
        @app.route("/stopcoverage")
        def stopCoverage():
            coverage_tracer_obj.get_data().write()
            return ""

    # Initialize and start the Flask application
    print("Loading db")
    exec_sql_file('club.sql')
    print("Starting flask")
    app.run(debug=True)

# Entry point for the application
if __name__ == '__main__':
    print("Starting react app")
    main()
