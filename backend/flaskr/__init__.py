import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Wrapper for pagenation
def paginate_questions(request, selection):
    # Gets the page argument if given.  If not, defaults page to 1
    page = request.args.get('page', 1, type=int)
    # get the range of objects to return.  In this case 10
    start = (page - 1) * QUESTIONS_PER_PAGE  # start index
    end = start + QUESTIONS_PER_PAGE  # ending index
    # formats the plants output using a format function declared in the Plant class
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

# Wrapper for getting all the categories since it's used >1 time
def category_list():
  selection = Category.query.order_by(Category.id).all()
  categories = [] #Create a blank array
  for category in selection: #Add each category to the array
    categories.append(category.type)
  return categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app,resouces={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
      return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
      categories = category_list() #Get category list using the function from above
      if len(categories) == 0:
        abort(404)
      else:
        return jsonify({
            'success': True,
            'categories': categories,
            'total_categories': len(categories)
        })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
      selection = Question.query.order_by(Question.id).all()
      # uses helper function above
      current_questions = paginate_questions(request, selection)
      categories = category_list() #Get category list using the function from above

      if len(current_questions) == 0 or len(categories) == 0:
          abort(404)
      else:
          return jsonify({
              'success': True,
              'questions': current_questions,
              'totalQuestions': len(selection),
              'categories':categories,
              'currentCategory':None
          })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
          abort(404)  # abort if question id is not found
      else:
          try:
              question.delete()

              selection = Question.query.order_by(Question.id).all()
              # uses helper function above
              current_questions = paginate_questions(request, selection)

              # return books from the same page so the page can refresh
              return jsonify({
                  'success': True,
                  'deleted': question_id,
                  'books': current_questions,
                  'total_books': len(selection)
              })
          except:
              abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():

    # get the body and put the needed parts into variables
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    search = body.get('searchTerm', None)
    print('testtttttttttt',search)
    try:  #If a search term was included, then return the search results
      if search:
        selection = Question.query.order_by(Question.id).filter(
            Question.question.ilike('%{}%'.format(search))).all()
        current_questions = paginate_questions(request, selection)
        print('testtttttttttt',current_questions)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(selection),
            'currentCategory': None
        })

      else: # No search term, add a new question
        question = Question(question=new_question, answer=new_answer,
                    difficulty=new_difficulty,category=new_category)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        # uses helper function above
        current_questions = paginate_questions(request, selection)
        # return books from the same page so the page can refresh
        return jsonify({
            'success': True,
            'created': question.id,
            'questions': current_questions,
            'total_questions': len(selection)
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  #See above

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found",
          "sys_error": str(error)
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable",
          "sys_error": str(error)
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request",
          "sys_error": str(error)
      }), 400

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Request not allowed",
          "sys_error": str(error)
      }), 405
  
  return app

    
