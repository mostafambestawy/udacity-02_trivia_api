import os
from flask import Flask, request, abort, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    @app.route('/categories', methods=['GET'])
    def get_catogries():
        CATEGORIES = {}
        categories = Category.query.all()
        for c in categories:
            CATEGORIES.update(c.format())
        return jsonify({
            "categories": CATEGORIES,
        })

    @app.route('/', methods=['GET'])
    def index():
        qeustions = Question.query.order_by(
            func.random()).paginate(1, per_page=QUESTIONS_PER_PAGE)
        qs = []
        current_cats = []
        for i in qeustions.items:
            qs.append(i.format())
            current_cats.append(i.format().get('category'))
        CATEGORIES = {}
        categories = Category.query.all()
        for c in categories:
            CATEGORIES.update(c.format())
        return jsonify({
            "questions": qs,
            "page": 1,
            "total_questions": qeustions.total,
            "categories": CATEGORIES,
            "currentCategory": current_cats,
        })

    @app.route('/questions')
    def get_questions():
        try:
            page = request.headers.get('page', 1, type=int)
            qeustions = Question.query.order_by(func.random()).paginate(
                page, per_page=QUESTIONS_PER_PAGE)
            qs = []
            current_cats = []
            for _question in qeustions.items:
                qs.append(_question.format())
                current_cats.append(_question.format().get('category'))
            CATEGORIES = {}
            categories = Category.query.all()
            for c in categories:
                CATEGORIES.update(c.format())
            return jsonify({
                "questions": qs,
                "page": 1,
                "total_questions": qeustions.total,
                "categories": CATEGORIES,
                "current_category": current_cats,
            })
        except:
            abort(422)

    @app.route('/categories/<id>/questions')
    def get_by_cat(id):
        page = request.headers.get('page', 1, type=int)
        qeustions = Question.query.filter(Question.category == id).paginate(
            page, per_page=QUESTIONS_PER_PAGE)
        qs = []
        current_cats = []
        for _question in qeustions.items:
            qs.append(_question.format())
            current_cats.append(_question.format().get('category'))
        CATEGORIES = {}
        categories = Category.query.all()
        for c in categories:
            CATEGORIES.update(c.format())
        return jsonify({
            "questions": qs,
            "page": page,
            "total_questions": qeustions.total,
            "categories": CATEGORIES,
            "current_category": current_cats,
        })

    @app.route('/questions/<id>', methods=['DELETE'])
    def delete__q_by_id(id):
        q = Question.query.filter(Question.id == id).first()
        if q is None:
            abort(404)
        else:
            q.delete()
            return jsonify({
                "success": True,
                "message": "Deleted",
            })

    @app.route('/questions', methods=['POST'])
    def add_q():
        try:
            question = request.get_json()['question']
            answer = request.get_json()['answer']
            category = request.get_json()['category']
            difficulty = request.get_json()['difficulty']
            q = Question(question=question, answer=answer,
                         category=category, difficulty=difficulty)
            q.insert()
            return jsonify({
                "success": True,
                "message": "Inserted",
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            searchTerm = request.get_json()['searchTerm']
            qeustions = Question.query.filter(
                (func.lower(Question.question)).like('%'+searchTerm+'%')).all()
            categories = Category.query.all()
            qs = []
            current_cats = []
            for i in qeustions:
                qs.append(i.format())
                current_cats.append(i.format().get('category'))
            cs = []
            for c in categories:
                cs.append(c.format())
            CATEGORIES = {}
            categories = Category.query.all()
            for c in categories:
                CATEGORIES.update(c.format())
            return jsonify({
                "searchTerm": searchTerm,
                "questions": qs,
                "categories": CATEGORIES,
                "current_category": current_cats,
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        try:
            previous_questions = request.get_json()['previous_questions']
            quiz_category = request.get_json()['quiz_category']
            question = None
            if quiz_category['id'] != 0:
                question = Question.query.filter(Question.id.notin_(previous_questions)).filter(
                    Question.category == quiz_category['id']).order_by(func.random()).first()
            else:
                question = Question.query.filter(Question.id.notin_(
                    previous_questions)).order_by(func.random()).first()
            result = {}
            if question is not None:
                result.update({"question": question.format()})
            return jsonify(result)
        except:
            abort(422)

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

    return app
