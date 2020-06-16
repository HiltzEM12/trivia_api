# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

On Windows, run the following:
    py -m pip install --user virtualenv
    py -m venv env
The last variable above is the name of the virtual environment.  In this case 'env'
Then add the env folder to the gitignore
Then activate the virtual environment by running:
    .\env\Scripts\activate
If the above doesn't work, use:
    source env/Scripts/activate
Check to see if its running, run:
    where python
It should display something allong the lines of (...env\Scripts\python.exe) if it's running.
To leave the virtual environment, run:
    deactivate


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
***NOTE:  Some of these are not working.  psycopg2-binary needs to be installed manually via (pip install psycopg2-binary)

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
**Note:  Must create the db 1st using:
    CREATE DATABASE trivia
**Note:  Also might need to create a role with your user name.  I did this via the GUI.
**Note:  Must change the role used in the trivia.psql file to the one created above.

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

***NOTE: there is a known error of module 'time' has no attribute 'clock'.  This is a depricated feature in SQLAlchemy that needs to be changed manualy.


Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
In the virtual environment folder (env in this case), edit the file Lib\site_packages->sqlalchemy->util->compat.py
Comment out the following:
```bash
import time

if win32 or jython:
    time_func = time.clock
else:
    time_func = time.time
```

After that, you might need to update the Werkzeug via:
    pip install --upgrade Werkzeug
For more info see: https://knowledge.udacity.com/questions/132762


Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Endpoints
```
GET /categories
GET /categories/${id}/questions
GET /questions
POST /questions
POST /quizzes
DELETE /questions/${id}
```

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{
    'success': True, 
    'categories': ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports'], 
    'total_categories': 6
}
```


### GET '/categories/{id}/questions'
- Fetches a page of questions that are in the given category id given in the uri.
- Request Arguments:
    - page: page of questions requested.  Questions are separated into 10 per page.
- Returns response 404 if no questions were found
- Returns json object with the questions to be displayed: 
```
{
    'success': True, 
    'questions': [
        {
            'id': 10, 
            'question': 'Which is the only team to play in every soccer World Cup tournament?', 
            'answer': 'Brazil', 
            'category': 5, 
            'difficulty': 3
        }, 
        {
            'id': 11, 
            'question': 'Which country won the first ever soccer World Cup in 1930?', 
            'answer': 'Uruguay', 
            'category': 5, 
            'difficulty': 4
        }
    ], 
    'totalQuestions': 2, 
    'currentCategory': 'Sports'
}
``` 

### GET '/questions'
- Fetches a page of question of any category.
- Request Arguments:
    - page: page of questions requested.  Questions are separated into 10 per page.
- Returns response 404 if no questions were found
- Returns json object with the questions to be displayed: 
```
{
    'success': True, 
    'questions': [
        {
            'id': 5, 
            'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 
            'answer': 'Maya Angelou', 
            'category': 3, 
            'difficulty': 2
        }, 
        {
            'id': 6, 
            'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
            'answer': 'Edward Scissorhands', 
            'category': 4, 'difficulty': 3
        }
    ], 
    'totalQuestions': 22, 
    'categories': ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports'], 
    'currentCategory': None
}
``` 

### POST '/questions'
- Fetches a json file containing the question that meet the searc criteria
- Creates a new question
- Request Arguments:
    - page: page of questions requested.  Questions are separated into 10 per page.  Only applicable when searching.
- Returns 422 if not all required fields are present (question, answer, difficulty, category)
- On search returns json object contianing the questions that match the search criteria: 
```
{
    'success': True, 
    'questions': [{'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 'answer': 'Edward Scissorhands', 'category': 4, 'difficulty': 3}, {'id': 18, 'question': 'How many paintings did Van Gogh sell in his lifetime?', 'answer': 'One', 'category': 1, 'difficulty': 4}], 'totalQuestions': 2, 'currentCategory': None}
``` 
- On add new returns json object with status, id of newly created question, new count of questions: 
```
{
    'success': True, 
    'created': 29, 
    'total_questions': 21
}
```

### POST '/quizzes'
- Fetches a random question for the quiz.  
- Request Arguments: 
    - In the request body: 
    - previous_questions: list of ids of questions already asked during this quiz attempt.
    - quiz_category: json object containing the category type and id.  If all categories are chosen, then type should be 'click'.
```
{
    'previous_questions': [17, 16], 
    'quiz_category': {
        'type': 'Art', 
        'id': '1'
    }
}
```
- Returns: 
```
{
    'success': True, 
    'question': {
        'id': 19, 
        'question': 'Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?', 
        'answer': 'Jackson Pollock', 
        'category': 1, 
        'difficulty': 2
    }
}
``` 

### DELETE '/questions/{id}'
- Deletes the question with the unique id given in the uri 
- Request Arguments:
    - page: page of questions requested.  Questions are separated into 10 per page
- Returns response 404 if question doesn't exist
--Returns response 422 if there was a problem deleting the question
- Returns a json object with the id of the question deleted as well as the a list of the remaining questions: 
```
{
    'success': True, 
    'deleted': 5, 
    'books': [
        {
            'id': 6, 
            'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
            'answer': 'Edward Scissorhands', 
            'category': 4, 
            'difficulty': 3
        }, 
        {
            'id': 9, 
            'question': "What boxer's original name is Cassius Clay?", 
            'answer': 'Muhammad Ali', 
            'category': 3, 
            'difficulty': 1}
    ], 
    'total_books': 21
}
``` 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```