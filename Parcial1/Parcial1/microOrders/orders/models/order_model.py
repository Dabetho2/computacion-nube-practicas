from db.db import db
from sqlalchemy.sql import func

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    userEmail = db.Column(db.String(255), nullable=False)
    saleTotal = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "userName": self.userName,
            "userEmail": self.userEmail,
            "saleTotal": float(self.saleTotal),
            "date": self.date.isoformat(sep=" ", timespec="seconds") if self.date else None,
        }
