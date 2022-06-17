import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, User


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
            self.new_question = {
            'question': 'Hematology is a branch of medicine involving the study of what?',
            'answer': 'Blood',
            'difficulty': 4,
            'category': '1',
            'rating':3
        }
            self.new_category = {
            'type': 'Science',
        }
            self.new_user = {
            'user': 'Loval',
            'playscore': 0
        }
                    


    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_new_question(self):

        questions_before = Question.query.all()

        response = self.client().post("/questions", json=self.new_question)

        data = json.loads(response.data)

        questions_after = Question.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        
    def test_new_category(self):

        categories_before = Category.query.all()

        response = self.client().post("/categories", json=self.new_category)

        data = json.loads(response.data)

        categories_after = Category.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(categories_after) - len(categories_before) == 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()