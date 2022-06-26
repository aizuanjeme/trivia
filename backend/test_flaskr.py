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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "!pass4sure", "localhost:5432", self.database_name)
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
                'rating': 3
            }
            self.new_category = {
                'type': 'Science',
            }
            self.new_user = {
                'user': 'Loval',
                'playscore': 0
            }
            self.rate = {
                'rating': 4
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

    def test_new_user(self):

        users_before = User.query.all()

        response = self.client().post("/users", json=self.new_user)

        data = json.loads(response.data)

        users_after = User.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(users_after) - len(users_before) == 1)

    def test_get_questions(self):

        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_categories(self):

        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertTrue(data['categories'])

    def test_get_questions_category(self):

        response = self.client().get("/categories/3/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_search_questions(self):

        response = self.client().post("/questions/search",
                                      json={"searchTerm": "dna"})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["questions"][0]["id"], 6)

    def test_no_data_for_search(self):
        """Test for the case where no data is sent"""

        # process response from request without sending data
        response = self.client().post('/questions/search',
                                      json={"searchTerm": "dna"})
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_rating_question(self):

        question = Question.query.filter_by(id=6).one_or_none()
        question_rate_before = question.rating

        response = self.client().patch("/questions/5", json=self.rate)
        question_rate_after = question.rating

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(question_rate_after != question_rate_before)

    def test_no_rating(self):
        """Test for the case where id is not found"""

        # process response from request without sending data
        response = self.client().patch('/questions/5')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_question(self):
        """Tests question deletion success"""

        response = self.client().delete('/questions/8')

        questions_before = Question.query.all()

        question = Question.query.filter(Question.id == 8).one_or_none()

        data = json.loads(response.data)

        questions_after = Question.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 8)

        self.assertTrue(len(questions_before) - len(questions_after) == 1)

        self.assertEqual(question, None)

    def test_no_id(self):
        """Test for the case where id is not found"""

        # process response from request without sending data
        response = self.client().delete('/questions/8')
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_quiz(self):
        response = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [10],
                "quiz_category": {"type": "Science", "id": "3"},
            },
        )

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["question"])

    def test_no_data_to_play_quiz(self):
        """Test for the case where no data is sent"""

        # process response from request without sending data
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
