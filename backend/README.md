# Backend - Trivia API

# Setting up the Backend

# Install Dependencies

1. ** Python 3.7 ** - Follow instructions to install the latest version of python for your platform in the[python docs](https: // docs.python.org/3/using/unix.html  # getting-and-installing-the-latest-version-of-python)

2. ** Virtual Environment ** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the[python docs](https: // packaging.python.org/guides/installing-using-pip-and-virtual-environments /)

3. ** PIP Dependencies ** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/ backend` directory and running:

```bash
pip install - r requirements.txt
```

# Key Pip Dependencies

- [Flask](http: // flask.pocoo.org /) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https: // www.sqlalchemy.org /) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https: // flask-cors.readthedocs.io/en/latest /  # ) is the extension we'll use to handle cross-origin requests from our frontend server.

# Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

# Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run - -reload
```

The `- -reload` flag will detect file changes and restart the server automatically.

# To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination(every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

# Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

# Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
[
  {
    "id": 1,
    "type": "Science"
  }
  {
    "id": 2,
    "type": "Art"
  }
  {
    "id": 3,
    "type": "Geography"
  }
  {
    "id": 4,
    "type": "History"
  }
  {
    "id": 5,
    "type": "Entertainment"
  }
  {
    "id": 6,
    "type": "Sports"
  }
]
```
`GET '/api/v1.0/questions'`

- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: page
- Returns: An Array of object, `questions`,

```json
{
"success": true,
"questions": [
{
  "question": "What is Science",
  "answer": "Science is what it is",
  "difficulty": 2,
  "catergory": 1,
  "rating": 4
}
{
  "question": "What is Technology",
  "answer": "Technology is what it is",
  "difficulty": 2,
  "catergory": 2,
  "rating": 2
}
{
  "question": "What is Art",
  "answer": "Art is what it is",
  "difficulty": 4,
  "catergory": 5,
  "rating": 3
}
],
"total_question": 4,
"limit": 10
}
```

`GET '/api/v1.0/categories/<int:id>/questions'`

- Fetches a dictionary of question based on there category in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: page
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
```json
{
  "success": true,
  "questions": [
    {
  "question": "What is Science",
  "answer": "Science is what it is",
  "difficulty": 2,
  "catergory": 1,
  "rating": 4
    }
  ],
  "total_questions": 4,
  "current_category": "Science"
}
```
`DELETE '/api/v1.0/questions/<int:id>'`

- Delete a question from the database of question based on the id passes
- Request Arguments: None
- Returns: An object of a success message and the deleted id

```json
{
  "success": true,
  "deleted": 1
}
```
`POST '/api/v1.0/quizzes'`

- Takes the category and array of previous questions in the request.
- Request Arguments: None
- Returns: An object of random question not in previous questions.

```json
{
  "question": {
    "id": 1,
    "question": "What is Science",
    "answer": "Science is what it is",
    "category": 4,
    "difficulty": 2,
    "rating": 2
  },
  "success": true
}

```
`POST '/api/v1.0/questions/search'`

- Takes the object of value that is been passed in the search form i.e `'{"searchTerm": "science"}'`.
- Request Arguments: page
- Returns: An array of object that matches the searchTerm.
```json
{
  "question": [{
    "id": 1,
    "question": "What is Science",
    "answer": "Science is what it is",
    "category": 4,
    "difficulty": 2,
    "rating": 2
  }],
  "success": true,
  "total_questions": 20
}

```
`POST '/api/v1.0/questions'`

- Takes the object of value that is been passed i.e `'{
            "question": "Where is Nigeria?",
            "answer": "Africa",
            "difficulty": 3,
            "category": "3",
            "rating": 4
        }'`.
- Request Arguments: None
- Returns: An object of success message.
```json
{
  "question": {
            "question": "Where is Nigeria?",
            "answer": "Africa",
            "difficulty": 3,
            "category": "3",
            "rating": 4
        },
  "successMessage": "ok",
  "success": true,
  "error": false,
}
```
`POST '/api/v1.0/category'`

- Takes the object of value that is been passed i.e `'{
            "type": "Art",
        }'`.
- Request Arguments: None
- Returns: An object of success message.
```json
{
  "category": {
            "type": "Art",
        },
  "successMessage": "ok",
  "success": true,
  "error": false,
}
```
`POST '/api/v1.0/user'`

- Takes the object of value that is been passed i.e `'{
            "user": "Steph",
            "playscore": "0",
        }'`.
- Request Arguments: None
- Returns: An object of success message.
```json
{
  "category": {
            "user": "Steph",
            "playscore": 0,
        },
  "successMessage": "ok",
  "success": true,
  "error": false,
}
```

`PATCH '/api/v1.0/users/<int:id>'`

- Takes the id of the user
- Request Arguments: None
- Returns: An object of success message.

```json
{
                "sucessMessage": "Success",
                "success": true,
                "id": "id",
            }
```
`PATCH '/api/v1.0/questions/<int:id>'`

- Takes the id of the questions
- Request Arguments: None
- Returns: An object of success message.

```json
{
                "sucessMessage": "Success",
                "success": true,
                "id": 3,
                "categoryId": 4
            }
```

# Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
