from db.db import db

class Products(db.Model):
    __tablename__ = 'products'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(255))
    price    = db.Column(db.Numeric(10, 2))
    quantity = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price) if self.price is not None else None,
            "quantity": self.quantity
        }
