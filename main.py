from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
from data import users, orders, offers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))



def insert_data():
    new_users = []
    for i in users:
        new_users.append(
            User(
                id=i['id'],
                first_name=i['first_name'],
                last_name=i['last_name'],
                age=i['age'],
                email=i['email'],
                role=i['role'],
                phone=i['phone'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_users)

    new_order = []
    for i in orders:
        new_order.append(
            Order(
                id=i['id'],
                name=i['name'],
                description=i['description'],
                start_date=datetime.strptime(i['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(i['end_date'], '%m/%d/%Y'),
                address=i['address'],
                price=i['price'],
                customer_id=i['customer_id'],
                executor_id=i['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_order)

    new_offer = []
    for i in offers:
        new_offer.append(
            Offer(
                id=i['id'],
                order_id=i['order_id'],
                executor_id=i['executor_id'],

            )
        )
        with db.session.begin():
            db.session.add_all(new_offer)




@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        data = []
        for i in Order.query.all():
            data.append({
                'id': i.id,
                'name': i.name,
                'description': i.description,
                'start_date': i.start_date,
                'end_date': i.end_date,
                'address': i.address,
                'price': i.price,
                'customer_id': i.customer_id,
                'executor_id': i.executor_id,
            })
        return jsonify(data)
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        new_order = Order(
                name=data['name'],
                description=data['description'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                address=data['address'],
                price=data['price'],
                customer_id=data['customer_id'],
                executor_id=data['executor_id'],
        )
        with db.session.begin():
            db.session.add(new_order)



@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def orders_id(id):
    if request.method == 'GET':
        i = Order.query.get(id)
        data = {
                'id': i.id,
                'name': i.name,
                'description': i.description,
                'start_date': i.start_date,
                'end_date': i.end_date,
                'address': i.address,
                'price': i.price,
                'customer_id': i.customer_id,
                'executor_id': i.executor_id,
        }
        return jsonify(data)
    elif request.method == 'PUT':
        data = request.get_json()
        i = Order.guery.get(id)
        i.id = data['id']
        i.name = data['name']
        i.description = data['description']
        i.start_date = data['start_date']
        i.end_date = data['end_date']
        i.address = data['address']
        i.price = data['price']
        i.customer_id = data['customer_id']
        i.executor_id = data['executor_id']

        with db.session.begin():
            db.session.add_all(i)


if __name__ == '__main__':
    app.run(debug=True)

