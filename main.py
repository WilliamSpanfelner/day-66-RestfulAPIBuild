import random
from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/add", methods=['POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(name=request.form.get("name"),
                        map_url=request.form.get("map_url"),
                        img_url=request.form.get("img_url"),
                        location=request.form.get("location"),
                        seats=request.form.get("seats"),
                        has_toilet=bool(request.form.get("has_toilet")),
                        has_wifi=bool(request.form.get("has_wifi")),
                        has_sockets=bool(request.form.get("has_sockets")),
                        can_take_calls=bool(request.form.get("can_take_calls")),
                        coffee_price=request.form.get("coffee_price")
                        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/search")
def list_cafes_by_location():
    search_text = request.args.get('loc')
    cafes_at_location = Cafe.query.filter_by(location=search_text).all()
    cafes = [cafe.to_dict() for cafe in cafes_at_location]
    if cafes:
        return jsonify(cafes=cafes)
    cafes = {"Not Found": "Sorry, we don't have a cafe at that location."}
    return jsonify(error=cafes)


@app.route("/all")
def list_all_cafes():
    all_cafes = Cafe.query.all()
    cafes = [cafe.to_dict() for cafe in all_cafes]

    return jsonify(cafes=cafes)


@app.route("/random")
def select_random_cafe():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)

    return jsonify(cafe=random_cafe.to_dict())


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record

if __name__ == '__main__':
    app.run(debug=True)
