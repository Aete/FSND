# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

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

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## API Documentaion

### Getting Started
This API is organized around REST. <br>
If you run this backend flask app locally, the base url will be:
```bash
http://localhost:5000
```
### Errors
In general, a response status code 200 indicate success. However, status codes range 4xx mean an error that failed to perform tasks you required.
- 400 - bad request: The request was not acceptable. URI, parameters and methods should be rechecked.
- 404 - resource not found: The requested resource was not exist.
- 422 - unprocessable: The request was acceptable but it was unable to process the contained instructions 

### Endpoints
#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
#### GET '/questions'
- Fetches a list of questions with a page number 
- Request Argument: page number (default = 1)
- Returns: 1) An list of question object. 2) Number of total questions. 3) An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'questions': [[{"answer":"Apollo 13",
                 "category":5,
                 "difficulty":4,
                 "id":2,
                 "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"}],
  'total_questions': 1,
  'current_category': Null,
  'categories': {'1' : "Science",
                 '2' : "Art",
                 '3' : "Geography",
                 '4' : "History",
                 '5' : "Entertainment",
                 '6' : "Sports"}
}
```
#### DELETE '/questions/<int: question_id>'
- Delete a question by the given id.
- Returns: an id of the deleted question
```
{'deleted': 1}
```
#### POST '/questions'
- Create a new question with given information of JSON
- Request body: (JSON) An JSON object with 'question', 'answer', 'category', and 'difficulty' keys.
```
{"answer":"Apollo 13",
 "category":5,
 "difficulty":4,
 "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"}
```
- Returns: an id of the created question 
```
{'created': 20}
```
#### POST '/search'
- Fetch questions based on 'search term'
- Request body: (JSON) An JSON object with 'searchTerm' key.
```
{'searchTerm':'titie'}
```
- Returns: 1) An list of question object. 2) Number of total questions.
```
{'questions': [[{"answer":"Apollo 13",
                 "category":5,
                 "difficulty":4,
                 "id":2,
                 "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"}],
  'total_questions': 1,
  'current_category': Null,
}
```
#### GET '/categories/<int:category_id>/questions'
- Fetch questions based on the 'category'
- Returns: 1) category id (current_category), 2) An list of question object. 3) Number of total questions
```
{"current_category":1,
"questions":[{"answer":"The Liver",
              "category":1,
              "difficulty":4,
              "id":20,
              "question":"What is the heaviest organ in the human body?"}],
"total_questions":18}
```

#### POST '/quizzes'
- Fetch a random question based on a category id and a list of previous questions.
- Request body: (JSON) An JSON object with 'quiz_category' and 'previous_questions'
```
{'quiz_category':1,
'previous_questions':[1,2,5]}
```
- Returns: a question.
```
"question":{"answer":"The Liver",
            "category":1,
            "difficulty":4,
            "id":20,
            "question":"What is the heaviest organ in the human body?"},
```
