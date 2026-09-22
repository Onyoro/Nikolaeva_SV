from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///notes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def init_db():
    """Создаёт таблицы с несколькими попытками (для Render)."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("Таблицы созданы")
            return
        except Exception as e:
            print(f"Попытка {attempt + 1}/{max_retries} не удалась: {e}")
            time.sleep(3)
    print("Не удалось создать таблицы")

init_db()

# Модели данных
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    notes = db.relationship('Note', backref='category', lazy=True)

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'category': self.category.name if self.category else None,
            'category_id': self.category_id
        }

# Вызываем функцию инициализации при запуске
init_db()

# Роуты для заметок
@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Получение всех заметок с пагинацией и фильтрацией"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', type=int)
    
    query = Note.query
    if category:
        query = query.filter_by(category_id=category)
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [note.to_dict() for note in paginated.items],
        'total': paginated.total,
        'page': page,
        'per_page': per_page,
        'pages': paginated.pages
    })

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Получение заметки по ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Создание новой заметки"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400
    
    note = Note(
        title=data['title'],
        content=data['content'],
        category_id=data.get('category_id')
    )
    
    db.session.add(note)
    db.session.commit()
    
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Обновление заметки"""
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    if 'category_id' in data:
        note.category_id = data['category_id']
    
    note.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(note.to_dict())

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Удаление заметки"""
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({'message': 'Note deleted successfully'}), 200

# Роуты для категорий
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Получение всех категорий"""
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'notes_count': len(c.notes)
    } for c in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Создание категории"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    }), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)