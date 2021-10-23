from flask import Flask, blueprints, request, jsonify
from flask_pymongo import PyMongo

import db, db_user, db_threads, db_thread_posts

api_threads = blueprints.Blueprint("api_threads", __name__)

@api_threads.route('/threads/get/all')
def threads_all():
      return db_threads.get_all_threads(db.mongo)

@api_threads.route('/thread/new')
def thread_new():
      body = request.json
      return db_threads.create_thread(db.mongo, body["name"], body["description"], body["token"])

@api_threads.route('/thread/<thread_id>/get/id/')
def thread_get_specific_by_id(thread_id):
      return db_threads.get_specific_thread_by_id(db.mongo, thread_id)

@api_threads.route('/thread/<thread_name>/get/name/')
def thread_get_specific_by_name(thread_name):
      return db_threads.get_specific_thread_by_name(db.mongo, thread_name)


@api_threads.route('/thread/<thread_id>/edit/')
def thread_specific_modify(thread_id):
      return

@api_threads.route('/thread/<thread_id>/delete/')      
def thread_specific_delete(thread_id):
      body = request.json
      return db_threads.delete_thread(db.mongo, thread_id, body["token"])