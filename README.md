# Full Stack API Final Project

## Full Stack Trivia

This Trivia App can:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that users include question and answer text.
4. Add categories.
5. Search for questions based on a text query string.
6. Play the quiz game, randomizing either all questions or within a specific category.



### Backend

API endpoints, the following documentation, and tests are written by me. 

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

### POST /categories
- General
  - Creates a new category using the parameters passed. 
  - Returns the id of the newly created category.
- Sample
  ```bash
  curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"newCategory":"Pop Culture"}'
  ```
  ```
  {
  "created": 9, 
  "success": true
  }
  ```



### Frontend 

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. This was mostly provided by Udacity. I added a bonus feature to add question categories.

[View the README.md within ./frontend for more details.](./frontend/README.md)
