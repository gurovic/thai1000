import json
from app import app, db, Technique, Category

def load_techniques_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with app.app_context():
        for technique_data in data.get('techniques', []):
            title = technique_data.get('title')
            content = technique_data.get('content')
            category_path = technique_data.get('category')
            if title and content and category_path: # Проверяем, что всё есть
                category = get_or_create_category_by_path(category_path)
                existing_technique = Technique.query.filter_by(title=title).first()
                if existing_technique:
                    existing_technique.content = content
                    existing_technique.category_id = category.id
                else:
                    technique = Technique(title=title, content=content, category_id=category.id)
                    db.session.add(technique)
                db.session.commit()

    print("Techniques loaded successfully!")
def get_or_create_category_by_path(path):
    parts = path.split('/')
    parent = None
    for part in parts:
        category = Category.query.filter_by(name=part, parent_id=parent.id if parent else None).first()
        if not category:
             category = Category(name=part,parent_id=parent.id if parent else None)
             db.session.add(category)
             db.session.commit()
        parent = category
    return category

if __name__ == '__main__':
    with app.app_context():
       load_techniques_from_json('techniques.json')
