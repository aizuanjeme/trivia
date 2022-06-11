import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 2

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"*/api/*" : {"origins": '*'}})
    
    
    """ 
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    
    @app.route("/categories", methods=["GET"])
    def get_all_categories():
        categories= Category.query.all()
        category =[]
        for cat in categories:
            category.append({
                "id": cat.id,
                "type":cat.type
            })
            # category[cat.id] = cat.type
        return jsonify({
            "data":category,
            "totalCount": len(category)
        })    
        


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        # get paginated questions and categories
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        categories = Category.query.order_by(Category.id).all()

        # Get paginated questions
        current_questions = paginate_questions(request, questions)

        # return 404 if there are no questions for the page number
        # if (len(current_questions) == 0):
        #     abort(404)

        # categories_dict = {}
        # for category in categories:
        #     categories_dict[category.id] = category.type
        category =[]
        for cat in categories:
            category.append({
                "id": cat.id,
                "type":cat.type
            })

        # return values if there are no errors
        return jsonify({
            'success': True,
            'totalCount': total_questions,
            'categories': category,
            'data': current_questions,
            'limit': QUESTIONS_PER_PAGE
        }), 200


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        '''
        Handles DELETE requests for deleting a question by id.
        '''

        try:
            # get the question by id
            question = Question.query.filter_by(id=id).one_or_none()

            # abort 404 if no question found
            if question is None:
                abort(404)

            # delete the question
            question.delete()

            # return success response
            return jsonify({
                'success': True,
                'deleted': id
            })

        except:
            # abort if problem deleting question
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def post_question():
        data = request.json.get
        
        question = data("question")
        answer = data("answer")
        category = data("category")
        difficulty = data("difficulty")
        rating = data("rating")
        
        
        if not (question and answer and category and difficulty and rating):
            return abort(400)
        question_data = Question(question,answer,category,difficulty,rating)
        question_data.insert()
        return jsonify({
            "question": question_data.format(),
            "error": False,
            "success":True,
            "successMessage": "ok"
        })


    @app.route("/catergories", methods=["POST"])
    def post_category():
        data = request.json.get
        
        type = data("type")
        
        if not (type):
            return abort(400)
        category_data = Category(type)
        category_data.insert()
        return jsonify({
            "category": category_data.format(),
            "error": False,
            "success":True,
            "successMessage": "ok"
        })
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:categoryId>/questions")
    def get_questions_by_category(categoryId):
        category = Category.query.filter(Category.id  == categoryId).one_or_none()
        
        if category is None:
            abort(422)
            
        questions = Question.query.filter((Question.category) == str(category.id)).order_by(Question.id).all()
        paginated_questions= paginate_questions(request, questions)
        
        return jsonify({
            "success": True,
            "data": paginated_questions,
            "totalCount":len(questions),
            "current_category": category.type,
            "limit":QUESTIONS_PER_PAGE
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/questions/<int:question_id>", methods=["PATCH"])
    def update_question(question_id):
        data = request.get_json()
        
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            if "rating" in data:
                question.rating = int(data.get("rating"))
                
            question.update()
            return jsonify({
                "sucessMessage": "Success",
                "success": True,
                "id": question.id, 
                "categoryId": question.category                 
            })
        except:
            abort(400)     

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400
        
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    return app

