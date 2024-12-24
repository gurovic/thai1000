from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techniques.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy=True)
    techniques = db.relationship('Technique', backref='category_rel', lazy=True) # Связь с таблицей техник


class Technique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)


# Создание админ-панели
admin = Admin(app, name='Thai Cooking Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Technique, db.session)) # Добавляем технику в админку

def get_all_categories():
  categories = Category.query.all()
  return categories
def get_nested_categories(categories, parent_id=None, level=0, result=None):
  if result is None:
    result = []
  for category in categories:
        if category.parent_id == parent_id:
          result.append({"id":category.id,"name":category.name, "level": level, "children": get_nested_categories(categories,category.id,level +1)})
  return result

@app.route("/")
def home():
    category_id = request.args.get('category')
    categories = get_all_categories()
    nested_categories = get_nested_categories(categories)
    if category_id:
      techniques = Technique.query.filter_by(category_id=category_id).all()
    else:
      techniques = Technique.query.all()
    return render_template('index.html', techniques=techniques, categories = nested_categories)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
