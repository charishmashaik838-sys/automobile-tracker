import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Material
from sqlalchemy import func
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

# Database Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///automobile.db'

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables on startup
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    total_built = Material.query.filter_by(status='Built').count()
    total_assembled = Material.query.filter_by(status='Assembled').count()
    total_delivered = Material.query.filter_by(status='Delivered').count()

    today = date.today()

    daily_built = Material.query.filter(
        func.date(Material.updated_at) == today,
        Material.status == 'Built'
    ).count()

    daily_assembled = Material.query.filter(
        func.date(Material.updated_at) == today,
        Material.status == 'Assembled'
    ).count()

    daily_delivered = Material.query.filter(
        func.date(Material.updated_at) == today,
        Material.status == 'Delivered'
    ).count()

    type_counts = db.session.query(
        Material.material_type,
        func.count(Material.id)
    ).group_by(Material.material_type).all()

    materials = Material.query.order_by(
        Material.updated_at.desc()
    ).all()

    return render_template(
        'index.html',
        total_built=total_built,
        total_assembled=total_assembled,
        total_delivered=total_delivered,
        daily_built=daily_built,
        daily_assembled=daily_assembled,
        daily_delivered=daily_delivered,
        type_counts=type_counts,
        materials=materials
    )


@app.route('/add', methods=['POST'])
def add_material():
    name = request.form.get('name')
    material_type = request.form.get('type')
    status = request.form.get('status')

    if not name or not material_type or not status:
        flash('All fields are required!')
        return redirect(url_for('index'))

    new_material = Material(
        name=name,
        material_type=material_type,
        status=status
    )

    db.session.add(new_material)
    db.session.commit()

    flash('Material added successfully!')
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['POST'])
def update_status(id):
    material = Material.query.get_or_404(id)
    new_status = request.form.get('status')

    if new_status:
        material.status = new_status
        db.session.commit()
        flash(f'Updated {material.name} to {new_status}!')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)