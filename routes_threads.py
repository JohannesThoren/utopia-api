from flask import Flask, blueprints
from flask_pymongo import PyMongo

import db, db_user, db_threads, db_thread_posts

api_threads = blueprints.Blueprint("api_threads", __name__)

@api_threads.route('/threads/all')
def threads_all():
      return

@api_threads.route('/threads/<thread_id>')
def threads_new(thread_id):
      return

@api_threads.route('/threads/<thread_id>/edit')
def threads_specific_modify(thread_id):
      return

@api_threads.route('/threads/<thread_id>/delete')      
def threads_specific_delete(thread_id):
      return
