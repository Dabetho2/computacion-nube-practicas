from flask import Flask
from flask_cors import CORS
from config import Config
from db.db import db
from users.controllers.user_controller import user_controller

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "dev"
CORS(app, supports_credentials=True)

db.init_app(app)
app.register_blueprint(user_controller)

# opcional
@app.get("/api/users/health")
def health():
    return {"status": "ok"}, 200

#if __name__ == '__main__':
    #app.run()
