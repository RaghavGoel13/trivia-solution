# The Great Trivia Game

This project is a questionnaire where end user will be dealing with various categories. They can play out the quiz game
as a fun element that shuffles questions randomly to add a fun element.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
set FLASK_APP=app
set FLASK_DEBUG=True
py -m flask run
```

These commands put the application in development and directs our application to use the `app.py` file in our flaskr
folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever
changes are made. The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend
configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at
  the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable entity

### Endpoints

#### GET /questions?page=${integer}

- General:
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
    - Request Arguments: page - integer
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current
      category string
    - Sample: `curl http://127.0.0.1:5000/questions?page=2'

```
  {
      'questions': [
          {
              'id': 1,
              'question': 'This is a question',
              'answer': 'This is an answer', 
              'difficulty': 5,
              'category': 2
          },
      ],
      'totalQuestions': 100,
      'categories': { '1' : "Science",
      '2' : "Art",
      '3' : "Geography",
      '4' : "History",
      '5' : "Entertainment",
      '6' : "Sports" },
      'currentCategory': 'History'
  }
  ```

#### Errors CODES /questions?page=${9999}

-Errors are returned as JSON objects in the following format for invalid page numbers:

 ```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
 ```

#### GET /categories

- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the
      category.
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
    - Sample: `curl http://127.0.0.1:5000/categories'

```
    {
        'categories': { '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports" }
    }
```

#### Errors CODES /categories

-Errors are returned as JSON objects in the following format for no category present:

 ```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
 ```

#### GET /categories/${id}/questions

- General:
    - Fetch questions for a category specified by id request argument.
    - Request Arguments: id - integer
    - Returns: An object with questions for the specified category, total questions, and current category string
    - Sample: `curl http://127.0.0.1:5000/categories/1/questions'

```
    {
        'questions': [
            {
                'id': 1,
                'question': 'This is a question',
                'answer': 'This is an answer', 
                'difficulty': 5,
                'category': 4
            },
        ],
        'totalQuestions': 100,
        'currentCategory': 'History'
    }
```

#### Errors CODES /categories/1/questions

-Errors are returned as JSON objects in the following format for no question present for given category present:

 ```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
 ```

#### DELETE /questions/${id}'

- General:
    - Deletes a specified question using the id of the question.
    - Request Arguments: id - integer
    - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id
      of the question. If you are able to modify the frontend, you can have it remove the question using the id instead
      of fetching the questions.
    - Sample: `curl -x DELETE http://127.0.0.1:5000/questions/1'

```
    {
                'success': True,
                'deleted': "1"
    }
```

#### Errors CODES DELETE /questions/${id}

-Errors are returned as JSON objects in the following format when no question is present to be deleted for given id

 ```
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
 ```

-Errors are returned as JSON objects in the following format when invalid question id is passed

 ```
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
 ```

#### POST '/quizzes'

- General:
    - Sends a post request in order to get the next question.
    - Request Body: {'previous_questions':  an array of question id's such as [1, 4, 20, 15] 'quiz_category': a string
      of the current category }
    - Returns: a list of questions in random order to be played for quiz
    - Sample: `curl -x POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json -d '
      {'previous_questions':  [1, 4, 20, 15], 'quiz_category': 0}'

```
    {
        'question': {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        }
    }
```

#### Errors CODES POST /quizzes

-Errors are returned as JSON objects in the following format when category is None

 ```
{
    "success": False, 
    "error": 422,
    "message": "Unprocessable entity"
}
 ```

-Errors are returned as JSON objects in the following format when category is invalid

 ```
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
 ```

#### POST '/questions'

- General:
    - Sends a post request in order to add a new question
    - Request Body: All fields are required {
      'question':  'Heres a new question string',
      'answer':  'Heres a new answer string',
      'difficulty': 1,
      'category': 3, }
    - Returns: Does not return any new data
    - Sample: `curl -x POST http://127.0.0.1:5000/questions -H "Content-Type: application/json -d '{
      'question':  'Heres a new question string',
      'answer':  'Heres a new answer string',
      'difficulty': 1,
      'category': 3, }'

```
{
    'success': True,
    'created': id,
    'questions': Heres a new question string,
    'total_questions': len(all_questions)
}
```

#### Errors CODES POST /questions

-Errors are returned as JSON objects in the following format when question has an invalid/missing value

 ```
{
    "success": False, 
    "error": 422,
    "message": "Unprocessable entity"
}
 ```

#### POST '/questions/search'

- General:
    - Sends a post request in order to search for a specific question by search term
    - Request Body:
      { 'searchTerm': 'this is the term the user is looking for' }
    - Returns: any array of questions, a number of totalQuestions that met the search term and the current category
      string.
    - Sample: `curl -x POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json -d '{ '
      searchTerm': 'this is the term the user is looking for' }' {

 ```
{
'questions': [
      {
      'id': 1,
      'question': 'This is a question',
      'answer': 'This is an answer',
      'difficulty': 5,
      'category': 5 },
      ],
      'totalQuestions': 100,
      'currentCategory': 'Entertainment' 
}
```

#### Errors CODES POST /questions/search

-Errors are returned as JSON objects in the following format when searched question is not present

 ```

{
"success": False,
"error": 404,
"message": "Resource not found"
}

 ```

## Deployment N/A

## Authors

Yours truly, Raghav Goel
