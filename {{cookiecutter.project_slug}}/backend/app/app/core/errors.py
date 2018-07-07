# -*- coding: utf-8 -*-

from flask import jsonify
from ..main import app


# 400 Bad Request
@app.errorhandler(400)
def custom400(error):
    return jsonify({"msg": error.description}), 400


# 401 Unauthorized
@app.errorhandler(401)
def custom401(error):
    return jsonify({"msg": error.description}), 401


# 403 Forbidden
@app.errorhandler(403)
def custom403(error):
    return jsonify({"msg": error.description}), 403


# 404 Not Found
@app.errorhandler(404)
def custom404(error):
    return jsonify({"msg": error.description}), 404


# 405 Method Not Allowed
@app.errorhandler(405)
def custom405(error):
    return jsonify({"msg": error.description}), 405


# 406 Not Acceptable
@app.errorhandler(406)
def custom406(error):
    return jsonify({"msg": error.description}), 406


# 422 Unprocessable Entity, for flask-apispec, webargs
@app.errorhandler(422)
def custom422(error):
    return jsonify({"msg": error.description, "errors": error.exc.messages}), 422


# 500 Internal Server Error
@app.errorhandler(500)
def custom500(error):
    return jsonify({"msg": error.description}), 500
