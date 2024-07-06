from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets'
app.config['SECRET_KEY'] = 'your_secret_key'
connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=form.available.data
        )
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} has been added to the adoption list.", "success")
        return redirect(url_for('show_pet', pet_id=new_pet.id))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=["GET"])
def show_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('show_pet.html', pet=pet)

@app.route('/<int:pet_id>/edit', methods=["GET", "POST"])
def show_edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data or None
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()
        flash(f"{pet.name} has been updated.", "success")
        return redirect(url_for('homepage'))

    return render_template('edit_pet.html', pet=pet, form=form)

@app.route('/<int:pet_id>/delete', methods=["POST"])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    flash(f"{pet.name} has been deleted.", "success")
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
