# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask, blueprints
from flask_pymongo import PyMongo
from werkzeug.wrappers import request

api_thread_posts = blueprints.Blueprint('api_thread_posts', __name__)

@api_thread_posts.route('/<thread_id>/posts/get/<post_id>/comments')
def thread_posts_get_specific_get_comments(thread_id, post_id):
      return

@api_thread_posts.route('/<thread_id>/posts/get/<post_id>/comments/new')
def thread_posts_get_specific_get_comments_new(thread_id, post_id):
      return

@api_thread_posts.route('/<thread_id>/posts/get/<post_id>/comments/<comment_id>')
def thread_posts_get_specific_get_comments_specific(thread_id, post_id, comment_id):
      return
