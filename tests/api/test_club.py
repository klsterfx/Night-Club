import unittest
from tests.test_utils import *
import json

class TestNightClub(unittest.TestCase):

    def setUp(self):  
        """Initialize DB using API call"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
    
    # databse tests
    def test_get_clubs(self):  
        """test list all clubs"""
        result = get_rest_call(self, 'http://localhost:5000/clubs')
        self.assertEqual(len(result), 4)
   
    def test_get_all_users(self):  
        """Itest list all users"""
        result= get_rest_call(self, 'http://localhost:5000/users')
        self.assertEqual(len(result), 5)

    # login tests
    def test_login_successful(self):
        """login the user"""
        # insert user
        data = dict(name='user', password='ali123ali', age =10, email='ali@rit.edu', city='Rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        #login user
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        self.assertEqual(type(result[0]), int, "user is not logged in")

    def test_incorrect_password_fails_login(self):
        """login the user"""
        # insert user
        data = dict(name='user', password='ali123ali', age =10, email='ali@rit.edu', city='Rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        #login user
        login_data = dict(email='ali@rit.edu', password='ali123ali123')
        jdata = json.dumps(login_data)
        result = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        self.assertEqual(result, 'email or password is incorrect', "user is not logged in")

    ########################################################
     # user tests
    ########################################################

    # add users

    def test_insert_user(self):
        """insert a user"""
        data = dict(name='user', password='ali123ali', age =10, email='ali@rit.edu', city='Rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        self.assertEqual(result,'Account is created successfully', "user is not inserted")
    
    def test_insert_fail_user_already_exists(self):
        """doesn't inser a user if it already exists"""
        data = dict(name='user', password='ali123ali', age =10, email='ali@rit.edu', city='Rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        self.assertEqual(result, 'ali@rit.edu already exists', "user is not logged in")

   
    ########################################################
    #  managers test 
    ########################################################

    # add manager

    def test_add_maneger(self):
        """add manager to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        self.assertEqual(result,'manager added successfully', "manager is not added")

    def test_add_maneger_fails_if_user_doesnt_exist(self):
        """add manager to a club"""
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        self.assertEqual(result,'ali@rit.edu doesnot exists', "manager is not added")

    def test_add_maneger_fails_if_club_doesnt_exist(self):
        """add manager to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        self.assertEqual(result,'club-rochester doesnot exists', "manager is not added")

    def test_add_maneger_fails_if_club_alredy_has_manager(self):
        """add manager to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        self.assertEqual(result,'club-rochester already has a manager', "manager is not added")

    def test_add_maneger_fails_if_user_is_alredy_a_manager(self):
        """add manager to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert a club
        data = dict(name='club-nyc', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # insert manager 
        data = dict(club='club-nyc', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        self.assertEqual(result,'ali@rit.edu is a manager of another club', "manager is not added")

    # delete manager

    def test_delete_maneger(self):
        """delete manager to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # delete manager
        hdr = {'content-type':'application/json', 'clubname':'club-rochester'}
        result = delete_rest_call(self, 'http://localhost:5000/managers', hdr)
        self.assertEqual(result,'manager deleted successfully', "manager is not delted")

    def test_delete_maneger_fails_if_club_not_exist(self):
        """delete manager to a club"""
        # delete manager
        hdr = {'content-type':'application/json', 'clubname':'club-rochester'}
        result = delete_rest_call(self, 'http://localhost:5000/managers', hdr)
        self.assertEqual(result,'club-rochester doesnot exists', "manager is not delted")

    def test_delete_maneger_fails_if_club_has_no_manager(self):
        """delete manager to a club"""
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # delete manager
        hdr = {'content-type':'application/json', 'clubname':'club-rochester'}
        result = delete_rest_call(self, 'http://localhost:5000/managers', hdr)
        self.assertEqual(result,'club-rochester has no manager', "manager is not delted")



    ########################################################
    #  bouncers test 
    ########################################################

    # add bouncer
    def test_add_bouncer(self):
        """add bouncer to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'bouncer added successfully', "bouncer is not added")

    def test_add_bouncer_fail_if_club_doesnt_exist(self):
        """add bouncer to a club"""
        id = 2000
         # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'club-rochester doesnot exists', "bouncer is not added")

    def test_add_bouncer_fail_if_user_doesnt_exist(self):
        """add bouncer to a club"""
       # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'alib@rit.edu doesnot exists', "bouncer is not added")


    def test_add_bouncer_fail_if_user_is_already_a_bouncer_of_another_club(self):
        """add bouncer to a club"""

        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert a club
        data = dict(name='club-nyc', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # insert manager 
        data = dict(club='club-nyc', email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login manager
        login_data = dict(email='ali1@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-nyc', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali1@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'alib@rit.edu is already a bouncer of another club', "bouncer is not added")

    def test_add_bouncer_fail_if_manager_is_wrong(self):
        """add bouncer to a club"""


        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login manager
        login_data = dict(email='ali1@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali1@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'ali1@rit.edu is not the manager of club-rochester', "bouncer is not added")

    def test_add_multiple_bouncer(self):
        """add bouncer to a club"""


        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        self.assertEqual(result,'bouncer added successfully', "bouncer is not added")

    
#     # delete bouncers

    def test_del_bouncers(self):
        """del bouncer from a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # del bouncer
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'email':'alib@rit.edu', 'manager_email':'ali@rit.edu'}
        result = delete_rest_call(self, 'http://localhost:5000/bouncers', hdr)
        self.assertEqual(result,'bouncer deleted successfully', "bouncer is not added")


    def test_del_bouncer_fail_if_user_doesnt_exist(self):
        """del bouncer to a club"""
        id =2000
        # delete bouncer
        hdr = {'content-type':'application/json', 'session_id': str(id), 'email':'alib@rit.edu', 'manager_email':'ali@rit.edu'}
        result = delete_rest_call(self, 'http://localhost:5000/bouncers', hdr)
        self.assertEqual(result,'alib@rit.edu is not a bouncer', "bouncer is not added")

   
    def test_del_bouncer_fail_if_manager_is_not_logged_in(self):
        """del bouncer to a club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # del bouncer
        hdr = {'content-type':'application/json', 'session_id': str(id[0]+1), 'email':'alib@rit.edu', 'manager_email':'ali@rit.edu'}
        result = delete_rest_call(self, 'http://localhost:5000/bouncers', hdr)
        self.assertEqual(result,'manager needs to login to modify club details', "bouncer is not added")

    def test_del_bouncer_fail_if_manager_is_wrong(self):
        """add bouncer to a club"""

         # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login manager
        login_data = dict(email='ali1@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # del bouncer
        hdr = {'content-type':'application/json', 'session_id': str(id[0]+1), 'email':'alib@rit.edu', 'manager_email':'ali1@rit.edu'}
        result = delete_rest_call(self, 'http://localhost:5000/bouncers', hdr)
        self.assertEqual(result,'ali1@rit.edu is not the manager of club-rochester', "bouncer is not added")



    ########################################################
    #  club test 
    ########################################################
     
    # Add club 
    
    def test_insert_club(self):
        """insert a club"""
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        self.assertEqual(result,'club added successfully', "club is not inserted")

    def test_insert_fail_club_already_exists(self):
        """insert a club"""
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        self.assertEqual(result, 'club-rochester already exists. select different name.', "user is not logged in")

#     # modify club

    def test_modify_club(self):
        """modify club"""
        #insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # update club 
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/club-rochester', jdata, hdr)
        self.assertEqual(result,'information modified successfully', "club is not inserted")

    def test_modify_club_fails_if_club_not_exist(self):
        """modify club"""
        # update club 
        id=2000
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id), 'manager_email':'ali@rit.edu'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/club-rochester', jdata, hdr)
        self.assertEqual(result,'club-rochester doesnot exists', "club is not inserted")

    def test_modify_club_fails_if_manager_not_exist(self):
        """modify club"""
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # update club 
        id=2000
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id), 'manager_email':'ali@rit.edu'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/club-rochester', jdata, hdr)
        self.assertEqual(result,'ali@rit.edu is not the manager of club-rochester', "club is not inserted")

    def test_modify_club_fails_if_manager_is_not_logged_in(self):
        """modify club"""
        #insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # update club 
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]+1), 'manager_email':'ali@rit.edu'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/club-rochester', jdata, hdr)
        self.assertEqual(result,'manager needs to login to modify club details', "club is not inserted")


    # delete club

    def test_del_club(self):
        """delete club"""
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # del club
        hdr = {'content-type':'application/json'}
        result = delete_rest_call(self, 'http://localhost:5000/clubs/club-rochester', hdr)
        self.assertEqual(result,'club is deleted successfully', "club is not deleted")

    def test_del_club_fails_if_club_not_exist(self):
        """delete club"""
        # del club 
        hdr = {'content-type':'application/json'}
        result = delete_rest_call(self, 'http://localhost:5000/clubs/club-rochester', hdr)
        self.assertEqual(result,'club-rochester doesnot exists', "club is not deleted")



    #######################################################
    # Club Entry test 
    #######################################################

    def test_enter_club(self):
        """enter club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'added customer successfully', "club is not inserted")

    def test_enter_club_fail_if_bouncer_is_not_logged_in(self):
        """enter club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=100, city='Rochester', yellow_threshold=70, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]+1), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'bouncer needs to login to allow entry to club', "club is not inserted")
    
   
   
    def test_enter_club_fail_if_capacity_is_full(self):
        """enter club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali2', password='ali123ali', age=25, email='ali2@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=1, city='Rochester', yellow_threshold=1, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        # enter club 
        data = dict(email='ali2@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'full capacity, cant enter', "club is not inserted")

    def test_enter_club_fail_if_user_is_already_entered(self):
        """enter club"""
        # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=1, city='Rochester', yellow_threshold=1, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'ali1@rit.edu is already in the club', "club is not inserted")

    ########################################################
    #  Club Leave test 
    ########################################################

    def test_leave_club(self):
        """leave club"""
         # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=1, city='Rochester', yellow_threshold=1, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # enter club 
        data = dict(email='ali1@rit.edu', club='club-rochester')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'bouncer_email':'alib@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        # leave club 
        data = dict(email='ali1@rit.edu', club='club-rochester', amount_spent = 50)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'removed customer susscessfully', "club is not inserted")

    def test_leave_club_fails_if_user_is_not_present_in_club(self):
        """leave club"""
         # insert user
        data = dict(name='ali', password='ali123ali', age=25, email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali1', password='ali123ali', age=25, email='ali1@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert user
        data = dict(name='ali-bouncer', password='ali123ali', age=25, email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/users', jdata, hdr)
        # insert a club
        data = dict(name='club-rochester', music='pop', capacity=1, city='Rochester', yellow_threshold=1, current_count=0, increment=False, decrement=False)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/clubs', jdata, hdr)
        # insert manager 
        data = dict(club='club-rochester', email='ali@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = post_rest_call(self, 'http://localhost:5000/managers', jdata, hdr)
        # login manager
        login_data = dict(email='ali@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # insert bouncer
        data = dict(club='club-rochester', email='alib@rit.edu')
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json', 'session_id': str(id[0]), 'manager_email':'ali@rit.edu'}
        result = post_rest_call(self, 'http://localhost:5000/bouncers', jdata, hdr)
        # login bouncer
        login_data = dict(email='alib@rit.edu', password='ali123ali')
        jdata = json.dumps(login_data)
        id = post_rest_call(self, 'http://localhost:5000/login', jdata, hdr)
        # leave club 
        data = dict(email='ali1@rit.edu', club='club-rochester', amount_spent = 50)
        jdata = json.dumps(data)
        hdr = {'content-type':'application/json'}
        result = put_rest_call(self, 'http://localhost:5000/clubs/entry', jdata, hdr)
        self.assertEqual(result,'ali1@rit.edu is not present in the club', "club is not inserted")