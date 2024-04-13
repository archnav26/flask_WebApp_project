
from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #creates a Flask application instance.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) # intialize the database

#create a model class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __ref__(self):
        return '<Task %r>' % self.id
'''
to create the database and tables inside the sqllite follow the below steps
    1. activate enviornment if not active
    2. type python3 
    3. Import your Flask app and the necessary modules: from app import app, db
    4. Activate the application context: app.app_context().push()
    5. Now you can interact with your database, for example, by creating all tables: db.create_all()
    6. exit()

'''

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except request.requestException as e:
             return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task =  Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":  #is a common construct used to determine whether the script is being run directly by the Python interpreter or if it is being imported as a module into another script.
   app.run(debug=True)  # this line will start the Flask development server.