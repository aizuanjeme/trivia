import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import User, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

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
    
    @app.route('/categories')
    def get_categories():
        '''
        Handles GET requests for getting all categories.
        '''

                # get paginated questions and categories
        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        categories = Category.query.order_by(Category.id).all()

        # Get paginated questions
        current_questions = paginate_questions(request, questions)

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



    @app.route('/questions')
    def get_questions():
        '''
        Handles GET requests for getting all questions.
        '''

        # get all questions and paginate
        selection = Question.query.all()
        total_questions = len(selection)
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        category =[]
        for cat in categories:
            category.append({
                "id": cat.id,
                "type":cat.type
            })
        # abort 404 if no questions
        if (len(current_questions) == 0):
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': category
        })

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

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.json.get
        
        search_term = data('searchTerm')

            # query the database using search term
        selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # 404 if no results found
        if (len(selection) == 0):
                abort(404)

            # paginate the results
        paginated = paginate_questions(request, selection)

            # return results
        return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })

    
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
        

    @app.route('/categories/<int:id>/questions', methods=["GET"])
    def get_questions_by_category(id):
        '''
        Handles GET requests for getting questions based on category.
        '''
        category = Category.query.filter(Category.id  == id).one_or_none()
        
        if category is None:
            abort(422)
            
        questions = Question.query.filter((Question.category) == str(category.id)).order_by(Question.id).all()
        paginated_questions= paginate_questions(request, questions)
        
        # return the results
        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        '''
        Handles POST requests for playing quiz.
        '''
        
        # process the request data and get the values
        data = request.json.get
        previous_questions = data('previous_questions')
        category = data('quiz_category')

        # abort 400 if category or previous questions isn't found
        if ((category is None) or (previous_questions is None)):
            abort(400)

        # load questions all questions if "ALL" is selected
        if (category['id'] == 0):
            questions = Question.query.all()
        # load questions for given category
        else:
            questions = Question.query.filter(Question.category == str(category['id'])).all()

        # get total number of questions
        total = len(questions)

        # picks a random question
        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        # checks to see if question has already been used
        def check_if_answered(question):
            answered = False
            for q in previous_questions:
                if (q == question.id):
                    answered = True

            return answered

        # get random question
        question = get_random_question()

        # check if used, execute until unused question found
        while (check_if_answered(question)):
            question = get_random_question()

            # if all questions have been tried, return without question
            # necessary if category has <5 questions
            if (len(previous_questions) == total):
                return jsonify({
                    'success': True
                })

        # return the question
        return jsonify({
            'success': True,
            'question': question.format()
        })
        
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
    
    @app.route("/categories", methods=["POST"])
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
        
        
    @app.route("/users", methods=["POST"])
    def post_user():
        data = request.json.get
        
        user = data("user")
        playscore = 0
        
        if not (user):
            return abort(400)
        user_data = User(user,playscore)
        user_data.insert()
        return jsonify({
            "user": user_data.format(),
            "error": False,
            "success":True,
            "successMessage": "ok"
        })

    @app.route("/users/<int:user_id>", methods=["PATCH"])
    def update_user(user_id):
        data = request.get_json()
        
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            if user is None:
                abort(404)
            if "playscore" in data:
                user.playscore = int(data.get("playscore"))
                
            user.update()
            return jsonify({
                "sucessMessage": "Success",
                "success": True,
                "id": user.id, 
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

