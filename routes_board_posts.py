from flask import Flask, blueprints, request
from flask_pymongo import PyMongo

import json

import db
import db_user
import db_boards
import db_board_posts
import db_comment

api_board_posts = blueprints.Blueprint('api_board_posts', __name__)

# TODO All routess that should be a post request, should have all data in the body


# TODO this should be a post request
@api_board_posts.route('/board/<board_id>/post/new', methods=['POST'])
def board_posts_new(board_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_board_posts.new_post(db.mongo, board_id, body["token"],
                                   body["content"], body["title"],
                                   body["flag"])


@api_board_posts.route('/board/<board_id>/posts/get/all')
def board_posts_all(board_id):
    return db_board_posts.get_all_posts(db.mongo, board_id)


@api_board_posts.route('/get/<n>/global/posts')
def get_n_global_posts(n):
    return db_board_posts.get_n_amount_of_latest_posts(db.mongo, n)


@api_board_posts.route('/post/<post_id>')
def board_posts_get_specific(post_id):
    return db_board_posts.get_specific_post(db.mongo, post_id)


# TODO this should be a post request
@api_board_posts.route('/post/<post_id>/edit')
def board_posts_specific_edit(board_id, post_id):
    body = request.json
    return

# TODO this should be a post request


@api_board_posts.route('/post/<post_id>/delete', methods=['POST'])
def board_posts_specific_delete(post_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_board_posts.delete_post(db.mongo, post_id, body["token"])


@api_board_posts.route('/post/<post_id>/comment', methods=['POST'])
def comment(post_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_comment.new_comment(db.mongo, body["comment"], post_id, body["token"])


@api_board_posts.route('/post/<post_id>/comment/<comment_id>/delete', methods=['POST'])
def delete_comment(post_id, comment_id):
    body = json.loads(request.get_data().decode("UTF-8"))
    return db_comment.delete_comment(db.mongo, comment_id, post_id, body["roken"],)


@api_board_posts.route('/post/<post_id>/get/comments')
def get_comments(post_id):
    return db_comment.get_comments_for_post(db.mongo, post_id)
