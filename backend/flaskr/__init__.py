import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

SECRET_KEY = os.urandom(32)

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [q.format() for q in questions]
    return formatted_questions[start:end]

# returns categories in as an object with key = category id and value =
# category name


def _get_categories():
    categories = Category.query.order_by(Category.id).all()
    res = {}
    for c in categories:
        res[c.id] = c.type
    return res


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @DONE: Set up CORS. Allow '*' for origins.
  Delete the sample route after completing the DONEs
  '''
    # CORS(app, resources={r"*/api/*": {"origins": "*"}}) #?? unclear what the
    # r"*/api/*" part should be
    CORS(app)
    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        try:
            res = _get_categories()

            if not res:
                abort(404)

            return jsonify({
                'success': True,
                'categories': res
            })
        except BaseException:
            abort(404)

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom
  of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            curr_page_formatted_questions = paginate_questions(
                request, questions)

            res = _get_categories()

            if not curr_page_formatted_questions or not res:
                abort(404)

            return jsonify({
                'success': True,
                'questions': curr_page_formatted_questions,
                'total_questions': len(questions),
                'categories': res,
                'current_category': None
            })
        except BaseException:
            abort(404)

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(422)
            db.session.delete(question)
            db.session.commit()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except BaseException:
            abort(422)
        finally:
            db.session.close()

    '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def search_questions_or_add_question():
        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)
            search = body.get('searchTerm', None)

            if search is not None:
                matching_questions = Question.query.filter(
                    Question.question.ilike(
                        '%{}%'.format(search))).order_by(
                    Question.id).all()
                curr_page_formatted_questions = paginate_questions(
                    request, matching_questions)
                res = _get_categories()
                return jsonify({
                    'success': True,
                    'questions': curr_page_formatted_questions,
                    'total_questions': len(matching_questions)
                })

            else:
                if any(
                    field is None for field in [
                        question,
                        answer,
                        difficulty,
                        category]):
                    abort(422)
                newQuestion = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category)
                db.session.add(newQuestion)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'created': newQuestion.id
                })

        except BaseException:
            abort(422)
        finally:
            db.session.close()

    '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    # included in above, in:
    # @app.route('/questions', methods=['POST'])
    # def search_questions_or_add_question():

    '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).order_by(
                Question.id).all()
            curr_page_formatted_questions = paginate_questions(
                request, questions)

            categories = Category.query.order_by(Category.id).all()
            res = {}
            for c in categories:
                res[c.id] = c.type

            if not curr_page_formatted_questions or not res:
                # if not res: #<-- returns blank page if category does not
                # contain question
                abort(422)

            return jsonify({
                'success': True,
                'questions': curr_page_formatted_questions,
                'total_questions': len(questions),
                'categories': res,
                'current_category': category_id,
            })
        except Exception as e:
            app.logger.error(e)
            abort(422)

    '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        categories = _get_categories()

        if quiz_category is None:
            abort(400)
        quiz_category_id = int(quiz_category['id'])
        if quiz_category_id > 0 and quiz_category_id not in categories:
            abort(404)

        if quiz_category_id == 0:  # all categories
            questions = Question.query.filter(
                ~Question.id.in_(previous_questions)).all()
        else:
            questions = Question.query.filter(
                Question.category == quiz_category_id).filter(
                ~Question.id.in_(previous_questions)).all()

        n = len(questions)
        if n > 0:
            random_question = questions[random.randrange(0, n)].format()
        else:
            random_question = None

        return jsonify({
            'success': True,
            'question': random_question
        })

    '''
  BONUS - Add New Category in the "Add" page
  '''
    @app.route('/categories', methods=['POST'])
    def add_category():
        try:
            body = request.get_json()
            category = body.get('newCategory', None)

            if not category:
                abort(422)
            newCategory = Category(type=category)
            db.session.add(newCategory)
            db.session.commit()
            return jsonify({
                'success': True,
                'created': newCategory.id
            })

        except BaseException:
            abort(422)
        finally:
            db.session.close()

    '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_errors(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server errors"
        }), 500

    return app
