import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {'question':'Who is the developer of this api?',
        'answer': 'Han',
        'difficulty': 1,
        'category': 4}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # (Done) TODO Write a test for successful operation with getting categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    # (Done) TODO write a test case for the failure
    def test_get_404_error_for_categories(self):
        res = self.client().get('/categories/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # (Done) TODO Write a test for successful operation with getting questions without any page number
    def test_get_questions_without_page(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # (Done) TODO Write a test for successful operation with getting questions with a page number
    def test_get_questions_with_page(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # (Done) TODO write a test case for the failure
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/27')
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == 27).one_or_none()
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(question,None)
    #     self.assertTrue(data['success'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))

    def test_get_404_error_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resource not found")


    # def test_create_question(self):
    #     res = self.client().post('/questions', json=self.new_question, content_type='application/json')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code,200)
    #     self.assertTrue(data['success'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(len(data['questions']))

    def test_get_422_error_create_question(self):
        res = self.client().post('/questions', json='', content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


    def test_search_question(self):
        res = self.client().post('/search', json={'searchTerm':'what'}, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        print(data['questions'])


    def test_get_422_error_search_question(self):
        res = self.client().post('/search', json='', content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()