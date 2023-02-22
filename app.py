from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Toddo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id}"


@app.route('/', methods=['GET', 'POST'])
def create_data():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        todo = Toddo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    data = Toddo.query.all()
    return render_template('index.html', data=data)


@app.route('/update/<int:pk>/', methods=['GET', 'POST'])
def update_data(pk):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        todo = Toddo.query.filter_by(id=pk).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    data = Toddo.query.filter_by(id=pk).first()
    return render_template('edit.html', data=data)


@app.route('/delete/<int:pk>')
def delete_data(pk):
    data = Toddo.query.filter_by(id=pk).first()
    db.session.delete(data)
    db.session.commit()
    return redirect("/")


@app.route('/search/<str>')
def search_data(str=None):
    data_list = []
    data = Toddo.query.filter(Toddo.title.startswith(str)).all()
    if data:
        for i in data:
            context = {
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "created_date": i.created_date
            }
            data_list.append(context)
        return data_list
    else:
        return data_list


@app.route('/search/')
def search_alldata():
    data_list = []
    data = Toddo.query.all()
    if data:
        for i in data:
            context = {
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "created_date": i.created_date
            }
            data_list.append(context)
        return data_list


if __name__ == "__main__":
    app.run(debug=True, port=5000)
