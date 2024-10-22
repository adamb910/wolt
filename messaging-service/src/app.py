from flask import Flask
from routes import api

app = Flask(__name__)
app.register_blueprint(api)

# initialize DB
from repository import engine

engine.connect()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)