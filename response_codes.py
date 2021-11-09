# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from enum import Enum


class Codes(Enum):
      ok = 200
      
      # error codes
      not_authorized = 401
      not_allowed = 403
      not_found = 404
      