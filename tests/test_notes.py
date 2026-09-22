import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, db, Note, Category

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_note(client):
    response = client.post('/api/notes', json={
        'title': 'Тестовая заметка',
        'content': 'Это содержимое тестовой заметки'
    })
    return response.get_json()

def test_get_empty_notes(client):
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert data['items'] == []
    assert data['total'] == 0


def test_create_note(client):
    response = client.post('/api/notes', json={
        'title': 'Моя заметка',
        'content': 'Текст'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Моя заметка'
    assert data['content'] == 'Текст'
    assert 'id' in data


def test_create_note_without_title(client):
    response = client.post('/api/notes', json={
        'content': 'Текст без заголовка'
    })
    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_create_note_without_content(client):
    response = client.post('/api/notes', json={
        'title': 'Заголовок без текста'
    })
    assert response.status_code == 400


def test_get_note_by_id(client, sample_note):
    note_id = sample_note['id']
    response = client.get(f'/api/notes/{note_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == note_id
    assert data['title'] == 'Тестовая заметка'


def test_get_note_not_found(client):
    response = client.get('/api/notes/9999')
    assert response.status_code == 404


def test_update_note(client, sample_note):
    note_id = sample_note['id']
    response = client.put(f'/api/notes/{note_id}', json={
        'title': 'Обновлённый заголовок',
        'content': 'Обновлённый текст'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Обновлённый заголовок'
    assert data['content'] == 'Обновлённый текст'


def test_delete_note(client, sample_note):
    note_id = sample_note['id']
    response = client.delete(f'/api/notes/{note_id}')
    assert response.status_code == 200

    response = client.get(f'/api/notes/{note_id}')
    assert response.status_code == 404


def test_pagination(client):
    for i in range(15):
        client.post('/api/notes', json={
            'title': f'Заметка {i}',
            'content': f'Текст {i}'
        })

    response = client.get('/api/notes?page=1&per_page=5')
    data = response.get_json()
    assert len(data['items']) == 5
    assert data['total'] == 15
    assert data['pages'] == 3

    response = client.get('/api/notes?page=2&per_page=5')
    data = response.get_json()
    assert len(data['items']) == 5

def test_create_category(client):
    response = client.post('/api/categories', json={
        'name': 'Работа',
        'description': 'Рабочие заметки'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Работа'
    assert data['description'] == 'Рабочие заметки'


def test_get_categories(client):
    client.post('/api/categories', json={'name': 'Работа'})
    client.post('/api/categories', json={'name': 'Личное'})

    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2


def test_create_category_without_name(client):
    response = client.post('/api/categories', json={
        'description': 'Без имени'
    })
    assert response.status_code == 400