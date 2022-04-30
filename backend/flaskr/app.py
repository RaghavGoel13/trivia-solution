# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import random
from logging import FileHandler, Formatter

from flask import Flask, abort, jsonify, logging, request
from flask_cors import CORS

from models import setup_db, Category, Question

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
QUES_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUES_PER_PAGE
    end = start + QUES_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


app = Flask(__name__)
setup_db(app)
# CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/categories', methods=['GET'])
def retrieve_categories():
    categories = Category.query.order_by(Category.type).all()
    if len(categories) == 0:
        abort(404)
    else:
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict
        })


@app.route('/questions')
def get_questions():
    try:
        all_questions = Question.query.order_by(Question.id).all()
        total_questions = len(all_questions)
        pagenated_questions = paginate_questions(request, all_questions)

        if (len(pagenated_questions) == 0):
            abort(404)

        categories = Category.query.all()
        categoriesDict = {}
        for category in categories:
            categoriesDict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': pagenated_questions,
            'total_questions': total_questions,
            'categories': categoriesDict
        })
    except Exception as e:
        print(e)
        abort(400)


'''
@TODO: 
Create an endpoint to DELETE question using a question ID. 

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page. 
'''


@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_questions(id):
    try:
        question_to_be_deleted = Question.query.filter_by(id=id).one_or_none()
        if question_to_be_deleted is None:
            abort(404)
        else:
            question_to_be_deleted.delete()

            return jsonify({
                'success': True,
            })
    except Exception as e:
        print(e)
        abort(400)


'''
@TODO: 
Create an endpoint to POST a new question, 
which will require the question and answer text, 
category, and difficulty score.

TEST: When you submit a question on the "Add" tab, 
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.  
'''


@app.route("/questions", methods=['POST'])
def add_question():
    body = request.get_json()
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    try:
        added_question = Question(question=new_question, answer=new_answer, category=new_category,
                                  difficulty=new_difficulty)
        added_question.insert()

        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, all_questions)
        return jsonify({
            'success': True,
            'created': added_question.id,
            'questions': current_questions,
            'total_questions': len(all_questions)
        })

    except Exception as e:
        print(e)
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


@app.route("/search", methods=['POST'])
def search_question():
    body = request.get_json()
    search = body.get('searchTerm')
    searched_question = Question.query.filter(Question.question.ilike('%' + search + '%')).all()

    if searched_question:
        current_questions = paginate_questions(request, searched_question)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(searched_question)
        })
    else:
        abort(404)


'''
@TODO: 
Create a GET endpoint to get questions based on category. 

TEST: In the "List" tab / main screen, clicking on one of the 
categories in the left column will cause only questions of that 
category to be shown. 
'''


@app.route("/categories/<int:id>/questions")
def questions_by_category(id):
    searched_category = Category.query.filter_by(id=id).one_or_none()
    if searched_category:
        questions_in_category = Question.query.filter_by(category=str(id)).all()
        current_questions = paginate_questions(request, questions_in_category)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions_in_category),
            'current_category': searched_category.type
        })
    else:
        abort(404)


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


@app.route('/quizzes', methods=['POST'])
def get_quiz():
    body = request.get_json()
    quiz_category = body.get('quiz_category')
    previous_question = body.get('previous_questions')

    try:
        if (quiz_category['id'] == 0):
            # To handle all categories
            questions_query = Question.query.all()
        else:
            questions_query = Question.query.filter_by(category=quiz_category['id']).all()
        random_ques_index = random.randint(0, len(questions_query) - 1)

        next_question = questions_query[random_ques_index]
        while next_question.id not in previous_question:
            next_question = questions_query[random_ques_index]
            return jsonify({
                'success': True,
                'question': {
                    "answer": next_question.answer,
                    "category": next_question.category,
                    "difficulty": next_question.difficulty,
                    "id": next_question.id,
                    "question": next_question.question
                },
                'previousQuestion': previous_question
            })
    except Exception as e:
        print(e)
        abort(404)


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
        "message": "Resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
