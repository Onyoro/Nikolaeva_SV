import pytest
from app.main import app, db
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_note(client):
    """Тест создания заметки"""
    response = client.post('/api/notes', 
        json={'title': 'Test Note', 'content': 'Test Content'})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Note'
    assert data['content'] == 'Test Content'

def test_get_notes(client):
    """Тест получения списка заметок"""
    # Создаем тестовую заметку
    client.post('/api/notes', 
        json={'title': 'Test Note', 'content': 'Test Content'})
    
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['items']) > 0

def test_update_note(client):
    """Тест обновления заметки"""
    # Создаем заметку
    create_resp = client.post('/api/notes', 
        json={'title': 'Old Title', 'content': 'Old Content'})
    note_id = json.loads(create_resp.data)['id']
    
    # Обновляем
    response = client.put(f'/api/notes/{note_id}',
        json={'title': 'New Title'})
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'New Title'

def test_delete_note(client):
    """Тест удаления заметки"""
    # Создаем заметку
    create_resp = client.post('/api/notes', 
        json={'title': 'To Delete', 'content': 'Delete me'})
    note_id = json.loads(create_resp.data)['id']
    
    # Удаляем
    response = client.delete(f'/api/notes/{note_id}')
    assert response.status_code == 200
    
    # Проверяем что заметка удалена
    get_resp = client.get(f'/api/notes/{note_id}')
    assert get_resp.status_code == 404