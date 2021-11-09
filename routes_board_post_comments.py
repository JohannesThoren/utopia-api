# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask, blueprints
from flask_pymongo import PyMongo
from werkzeug.wrappers import request

api_board_posts = blueprints.Blueprint('api_board_posts', __name__)

@api_board_posts.route('/<board_id>/posts/get/<post_id>/comments')
def board_posts_get_specific_get_comments(board_id, post_id):
      return

@api_board_posts.route('/<board_id>/posts/get/<post_id>/comments/new')
def board_posts_get_specific_get_comments_new(board_id, post_id):
      return

@api_board_posts.route('/<board_id>/posts/get/<post_id>/comments/<comment_id>')
def board_posts_get_specific_get_comments_specific(board_id, post_id, comment_id):
      return
