from flask import Flask, blueprints, request, jsonify
from flask_pymongo import PyMongo

import json
import db
import db_boards

api_boards = blueprints.Blueprint("api_boards", __name__)

# TODO All routess that should be a post request, should have all data in the body


@api_boards.route('/boards/get/all')
def boards_all():
    return db_boards.get_all_boards(db.mongo)


@api_boards.route('/boards/<n>/top')
def board_n_top_followed(n):
    return db_boards.get_n_most_followed_boards(db.mongo, n)

# TODO this should be a post request


@api_boards.route('/board/new', methods=["POST"])
def board_new():
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_boards.create_board(db.mongo, body["name"], body["description"], body["token"])


@api_boards.route('/board/get/id/<board_id>')
def board_get_specific_by_id(board_id):
    return db_boards.get_specific_board_by_id(db.mongo, board_id)


@api_boards.route('/board/get/name/<board_name>')
def board_get_specific_by_name(board_name):
    return db_boards.get_specific_board_by_name(db.mongo, board_name)



@api_boards.route('/board/<board_id>/update/', methods=['POST'])
def update_board(board_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_boards.update_board_settings(db.mongo, body["token"], body["settings"], board_id)

@api_boards.route('/board/<board_id>/delete/', methods=['POST'])
def board_specific_delete(board_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_boards.delete_board(db.mongo, board_id, body["token"])


@api_boards.route('/board/<board_id>/follow', methods=["POST"])
def user_follow_board(board_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_boards.user_follow_board(db.mongo, body["token"], board_id)


@api_boards.route('/board/<board_id>/unfollow', methods=["POST"])
def user_unfollow_board(board_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_boards.user_unfollow_board(db.mongo, body["token"], board_id)
