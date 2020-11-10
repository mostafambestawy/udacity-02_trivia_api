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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_pagniated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['page'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])
        self.assertIsNotNone(data['current_category'])
    
    def test_get_questions_by_category(self):
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['page'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])
        self.assertIsNotNone(data['current_category'])

    def test_delete_question_succeeded(self):
        res=self.client().delete('/questions/19')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted')

    def test_delete_question_not_found(self):
        res=self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_post_question_succeeded(self):
        res=self.client().post('/questions',json={
            'question':'new question 1',
	        'answer':'answer of new question 1',
	        'difficulty':'2',
	        'category':'2'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Inserted')

    def test_post_question_unprocessable(self):
        res=self.client().post('/questions',json={
            'question':'new question 1',
	        'answer':'answer of new question 1',
	        'difficulty':'2',
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_questions_succeeded(self):
        res = self.client().post('/questions/search',json={
            'searchTerm':'which'
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['searchTerm'])
        self.assertIsNotNone(data['categories'])
        self.assertIsNotNone(data['current_category'])

    def test_search_questions_unprocessable(self):
        res=self.client().post('questions/search')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_play_quizzes_succeeded(self):
        res=self.client().post('/quizzes',json={
	        'previous_questions':[],
	        'quiz_category':{'id':0}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])

    def test_play_quizzes_sunprocessable(self):
        res=self.client().post('/quizzes',json={
	        'previous_questions':[],
	        
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        


    













# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()