"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, abort, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [{"id": c.id, "flavor": c.flavor, "size": c.size, "rating": c.rating, "image": c.image} for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get data about a single cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake"""
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')
    )
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = {"id": new_cupcake.id, "flavor": new_cupcake.flavor, "size": new_cupcake.size, "rating": new_cupcake.rating, "image": new_cupcake.image}
    return jsonify(cupcake=serialized), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating, and image data from the body of the request."""
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    serialized_cupcake = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

    return jsonify(cupcake=serialized_cupcake)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="Deleted")


if __name__ == '__main__':
    app.run(debug=True)
