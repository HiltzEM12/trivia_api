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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #question for succeful add
        self.new_question ={
            'question': "Hey there", 
            'answer': 'What', 
            'difficulty': '2', 
            'category': '2'
        }

        #question for unsucessful add
        self.bad_question ={
            'question': "Hey there", 
            'answer': None, 
            'difficulty': '2', 
            'category': '2'
        }

        #appropriate json for getting a quiz
        self.good_quiz = {
            'previous_questions': [17, 16], 
            'quiz_category': {
                'type': 'Art', 
                'id': '1'
            }
        }

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

    # GET /categories
    def test_categories(self):
        """Test that categories returns 200"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # GET /categories FAIL due unallowed method
    def test_categories_bad_method(self):
        """Test that categories returns 405"""
        res = self.client().delete('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request not allowed')

    # GET /categories/${id}/questions
    def test_questions_by_category(self):
        """Test that getting questions by category returns 200"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'],'Art')
        self.assertTrue(len(data['questions']))

    # GET /categories/${id}/questions FAIL due to bad category id
    def test_questions_by_category_bad_id(self):
        """Test that getting questions by a non-existent category returns 404"""
        res = self.client().get('/categories/99999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # GET /questions
    def test_questions(self):
        """Test that getting questions 200"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'],None)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # GET /questions FAIL due to bad page
    def test_questions_bad_page(self):
        """Test that getting questions with bad page number returns 404"""
        res = self.client().get('/questions?page=99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # POST /questions
    def test_post_question(self):
        """Test to make sure a question can be added"""
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    # POST /questions FAIL due to bad question (no answer)
    def test_post_question_no_answer(self):
        """Test to make sure a question is rejected if it doesn't have an answer"""
        res = self.client().post('/questions',json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # POST /quizzes
    def test_post_quizzes(self):
        """Test to make sure a random quiz can be retrieved"""
        res = self.client().post('/quizzes',json=self.good_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    # POST /quizzes FAIL due to tring to delete
    def test_post_quizzes_bad_category(self):
        """Test to make sure delete is not allowed on /quizzes"""
        res = self.client().delete('/quizzes',json=self.good_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request not allowed')


    # DELETE /questions/${id}
    # must refresh db for this to pass
    def test_delete_question(self):
        """Test to make sure a question can be deleted"""
        book_id = 13
        res = self.client().delete('/questions/'+str(book_id))
        data = json.loads(res.data)
        book = Question.query.filter(Question.id == book_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], book_id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(book,None)

    # DELETE /questions/${id} FAIL due to invalid id
    def test_delete_question_bad_id(self):
        """Test to make sure a question with an invalid id will return an error"""
        res = self.client().delete('/questions/999999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()