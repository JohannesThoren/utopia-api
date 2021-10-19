# Copyright (c) 2021 Johannes Thorén
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import jsonify, Flask

app = Flask(__name__)

@app.route('/api')
def api_main():
      return "api"


if __name__ == "__main__":
      app.run(host='localhost', port=8001)