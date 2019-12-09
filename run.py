from mdblog.app import flask_app, db

import sys

def start():
    debug = True
    host = "0.0.0.0"
    flask_app.run(host, debug=debug)

def init():
    with flask_app.app_context():
        db.create_all()
        print("Database inicialized")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        commad = sys.argv[1]
        if commad == "start":
            start()
        elif commad == "init":
            init()
        else:
            print("usage: start or init")
    else:
        print("usage: start or init")