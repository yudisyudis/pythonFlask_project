# Import modul-modul yang diperlukan:
# Flask sebagai framework, render_template untuk templarting, request dan redirect untuk request yang dilakukan
# SQL untuk database

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# deklarasi framework dan database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# deklarasi model database sebagai Objek
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id

# deklarasi route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        konten = request.form['content']
        input_task = Todo(content = konten)

        try:
            db.session.add(input_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ada masalah'
    else:
        show_task = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = show_task)

@app.route('/delete/<int:id>')
def delete(id):
    menghapus = Todo.query.get_or_404(id)

    try:
        db.session.delete(menghapus)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ada Masalah'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ada masalah'
    else:
        return render_template('update.html', task=task)
    return 'tes'

if __name__ == "__main__":
    app.run(debug=True)

