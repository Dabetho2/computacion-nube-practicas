from flask import Flask
from flask_cors import CORS
from config import Config
from db.db import db
from products.controllers.product_controller import product_controller

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)
db.init_app(app)

app.register_blueprint(product_controller)

@app.get("/api/products/health")
def health():
    return {"status": "ok"}, 200
