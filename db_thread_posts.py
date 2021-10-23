# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from uuid import UUID, uuid4
import db_user
from datetime import datetime

def x():
      print("X")

def new_post(mongo, thread_id, token, content, title):
      db = mongo.db.posts
      if db_user.auth_user(mongo, token):
            user_id, username = db_user.auth_user(mongo, token)
            new_post = {"title": title, "content": content, "thread": UUID(thread_id), "created": datetime.now(), "author": user_id, "id": uuid4()}
            db.insert(new_post)
            print(new_post)
            return {"response code": 200, "msg": "post created"}
      else:
            return {"response code": 403}      
      return {"poof": "x"}

def get_specific_post(mongo, post_id):
      db = mongo.db.posts
      post = db.find_one({"id": UUID(post_id)})
      if post:
            return {"id": post["id"], "title": post["title"], "author": post["author"], "thread": post["thread"], "created": post["created"],"content": post["content"], "response code": 200}
      else:
            return {"response code": 404}


def get_all_posts(mongo, thread_id):
      db = mongo.db.posts
      posts = db.find({"thread": UUID(thread_id)})
      post_dict = {}
      index = 0

      if posts:
            for post in posts:
                  post_dict.update({f"{index}":{"title": post["title"],"id": post["id"], "content": post["content"], "author": post["author"], "created": post["created"]}})


            return post_dict
      else:
            return {"response code": 404, "msg": "there are currently no posts"}


def delete_post(mongo, post_id, token):
      db = mongo.db.posts
      post = db.find_one({"id": UUID(post_id)})
      author_id, username = db_user.auth_user(mongo, token)
      if post:
            if post["author"] == author_id:
                  db.delete_one(post)
                  return {"response code": 200, "msg": "post deleted"}
            else:
                  return {"response code": 403}
      else:
            return {"response code": 404}
            