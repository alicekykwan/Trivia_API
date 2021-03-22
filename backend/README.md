# Full Stack Trivia API Backend
## Description
This Trivia API allows users to create questions and retrieve randomized questions to run a trivia quiz. Users may view questions and play the quiz based on a specified category (or all categories combined). Users may also search and delete questions. 
The code adheres to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started
### Base URL and Authentication
- Base URL: 
  - At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: 
  - This version of the application does not require authentication or API keys.


### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

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
Username and password (if any) for your database user can be stored as environmental variables in a python terminal shell or alternatively, create a file named ".env" in the `backend` directory to store them. 

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 



## Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": False,
  "error": 400,
  "message": "bad request"
}
```
The API will return three error types when requests fail: - 400: Bad Request - 404: Resource Not Found - 422: Not Processable

## Endpoint Library
### GET /categories
- General
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
- Sample
  ```bash
  curl http://127.0.0.1:5000/categories
  ```

  ```
  {
    "categories": {
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports"
    }
    "success": True
  }
  ```

### GET /questions
- General
  - Fetches a list of questions objects for the current page, an integer of total number of questions, dictionary of categories, and current category of value None.
  - Results are paginated in groups of 10. Optionally include a request argument to choose page number, default as 1. 
- Sample
  ```bash
  curl http://127.0.0.1:5000/questions?page=2
  ```
  ```
  {
    "questions": [
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }
    ],
    "total_questions": 12,
    "categories": {
      '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports"
    },
    "current_category": None,
    "success": True 
  }

  ```

### DELETE /questions/{question_id}
- General
  - Deletes the question of the given ID if it exists. 
  - Returns the id of the deleted book
- Sample
  ```bash
  curl -X DELETE http://127.0.0.1:5000/questions/5
  ```
  ```
  {
    "deleted": 5,
    "success": True
  }
  ```

### POST /questions
#### Supports Search or Create depending on the parameters passed
SEARCH:
- General
    - Returns a list of questions objects matching the search terms (case insensitive).
    - Results are paginated in groups of 10. Optionally include a request argument to choose page number, default as 1. 
    
- Sample
  ```bash
  curl http://127.0.0.1:5000/questions?page=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'
  ```
  ```
  {
    "questions": [
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ],
    "total_questions": 2,
    "success": True
  }
  ```
CREATE:
- General
  - Creates a new question using the parameters passed. 
  - Returns the id of the newly created question.
- Sample
  ```bash
  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the symbol of the element with the lowest atomic mass?","answer":"H","difficulty":"2","category":1}'
  ```
  ```
  {
  "created": 25, 
  "success": true
  }
  ```

### GET /categories/{category_id}/questions
- General
  - Fetches a list of questions objects for the given category id, an integer of total number of questions, dictionary of categories, and the id of the current category.
  - Results are paginated in groups of 10. Optionally include a request argument to choose page number, default as 1. 
- Sample 
  ```bash
  curl http://127.0.0.1:5000/categories/6/questions
  ```
  ```
  {
    "questions": [
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ], 
    "total_questions": 2,
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "current_category": 6, 
    "success": true
  } 
  ```
### POST /quizzes
- General
  - Returns one question belonging to the quiz category id passed in, or id of 0 if question category of "all" is requested. A "previous_questions" parameter is passed in to ensure a question that has not previously appeared in the current quiz is returned.
  - Response object contains value "None" for the key "question" if there are no available questions left.
- Sample
  ```bash
  curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"id":5}}'
  ```
  ```
  {
    "question": {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    "success": true
  }
  ```


## Testing
To run the tests, navigate to the backend folder and run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Authors
- Front End: Udacity Full Stack Nanodegree Program Staff
- Back End: Alice Kwan and Udacity Full Stack Nanodegree Program Staff

## Acknowledgements
- Coach Caryn at Udacity