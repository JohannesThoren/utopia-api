from flask import Flask, blueprints, request, jsonify
from flask_pymongo import PyMongo

import json
import db, db_boards

api_boards = blueprints.Blueprint("api_boards", __name__)

# TODO All routess that should be a post request, should have all data in the body


@api_boards.route('/boards/get/all')
def boards_all():
      return db_boards.get_all_boards(db.mongo)

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


@api_boards.route('/board/<board_id>/edit/')
def board_specific_modify(board_id):
      return

# TODO this should be a post request
@api_boards.route('/board/<board_id>/delete/')      
def board_specific_delete(board_id):
      body = request.json
      return db_boards.delete_board(db.mongo, board_id, body["token"])