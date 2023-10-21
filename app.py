from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

abs_path = os.path.abspath(__file__)
current_directory = os.path.dirname(abs_path)
db_path = current_directory + '/instance/test.db'
db_config = 'sqlite:////' + db_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_config#/// for rel path, //// for absolute path to db
db=SQLAlchemy(app)#to set up, open interactive python sell in terminal via python3 command, then "from app import db", then "db.create_all()"
#But first you need to import your app into the python session, from <my_app> import app, then with app.app_context(): from app import db, then db.create_all()

#Create your models here
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)#nullable=False means that the content cannot be empty
    date_created = db.Column(db.DateTime, default=datetime.utcnow)#default=datetime.utcnow means that the date will be set automatically
    def __repr__(self):
        return '<Task %r>' % self.id#self.id goes into %r


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']#content is the name of the input field in the form, or ID?
        new_task=Todo(content=task_content)#create new task object
        try:
            db.session.add(new_task)#add new task to db
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        
    else:
        try:
            tasks=Todo.query.order_by(Todo.date_created).all()
        except:
            return render_template('index.html', tasks=[])    
        return render_template('index.html', tasks=tasks)#pass tasks to index.html
    



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    

    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html',task=task)



if __name__ == '__main__':
    app.run(debug=True)

