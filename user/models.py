from flask import Flask, jsonify
class User:
    def signup():
        user={
        "__id":"",
        "firstname":"",
        "lastname":"",
        "username":"",
        "signup":" "
        }
        return jsonify(user),200

