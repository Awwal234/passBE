from ..utils import db

class Inventory(db.Model):
    __tablename__ = 'inventoryTable'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    productName = db.Column(db.String(40), unique=True, nullable=False)
    price = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.String(4), nullable=False)
    
    def __repr__(self):
        return f"Inventory('{self.id}')"
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        