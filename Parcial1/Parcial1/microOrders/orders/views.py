from flask import Flask
from flask_cors import CORS

from config import Config
from db.db import init_app as db_init
from orders.controllers.order_controller import order_controller

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True)
db_init(app)

app.register_blueprint(order_controller)

@app.get("/api/orders/health")
def health():
    return {"status": "ok"}, 200
