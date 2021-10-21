# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import bcrypt
from uuid import uuid4

def create_user(mongo, username, password, email):
      db = mongo.db.users
      
      if not db.find_one({"username":username}):
            password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
            new_user = {"username": username, "email": email ,"password": password, "token": uuid4()}
            db.insert(new_user)
            return True
      else:
            return False

def get_user_by_name(mongo, name):
      return
