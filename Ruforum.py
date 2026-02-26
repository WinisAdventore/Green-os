import os
import hashlib
import uuid
import json
import base64
import re
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, send_file, jsonify
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'goteam-secret-key-2025'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['AVATAR_FOLDER'] = 'static/avatars'
app.config['INVENTORY_FOLDER'] = 'static/inventory'
app.config['STATUS_FOLDER'] = 'static/status'
app.config['GAMES_FOLDER'] = 'static/games'
app.config['GAME_SCREENSHOTS_FOLDER'] = 'static/games/screenshots'
app.config['GAME_ICONS_FOLDER'] = 'static/games/icons'
app.config['GAME_FILES_FOLDER'] = 'static/games/files'
app.config['ACHIEVEMENT_ICONS_FOLDER'] = 'static/achievements'
app.config['DATA_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'obj', 'fbx', 'stl', 'gltf', 'glb', 'blend', 'mtl', 'zip', 'rar', '7z', 'exe'}
app.config['IMAGE_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['AVATAR_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['INVENTORY_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'obj', 'fbx', 'stl', 'gltf', 'glb', 'blend', 'mtl', 'mp4', 'mp3'}
app.config['MODEL_EXTENSIONS'] = {'obj', 'fbx', 'stl', 'gltf', 'glb', 'blend'}
app.config['GAME_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z', 'exe'}

# Создаём все папки
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AVATAR_FOLDER'], exist_ok=True)
os.makedirs(app.config['INVENTORY_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATUS_FOLDER'], exist_ok=True)
os.makedirs(app.config['GAMES_FOLDER'], exist_ok=True)
os.makedirs(app.config['GAME_SCREENSHOTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['GAME_ICONS_FOLDER'], exist_ok=True)
os.makedirs(app.config['GAME_FILES_FOLDER'], exist_ok=True)
os.makedirs(app.config['ACHIEVEMENT_ICONS_FOLDER'], exist_ok=True)
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

# Файлы данных
USERS_FILE = os.path.join(app.config['DATA_FOLDER'], 'users.json')
POSTS_FILE = os.path.join(app.config['DATA_FOLDER'], 'posts.json')
COMMENTS_FILE = os.path.join(app.config['DATA_FOLDER'], 'comments.json')
INVENTORY_FILE = os.path.join(app.config['DATA_FOLDER'], 'inventory.json')
STATUSES_FILE = os.path.join(app.config['DATA_FOLDER'], 'statuses.json')
LIKES_FILE = os.path.join(app.config['DATA_FOLDER'], 'likes.json')
GAMES_FILE = os.path.join(app.config['DATA_FOLDER'], 'games.json')
GAME_ACHIEVEMENTS_FILE = os.path.join(app.config['DATA_FOLDER'], 'game_achievements.json')
USER_ACHIEVEMENTS_FILE = os.path.join(app.config['DATA_FOLDER'], 'user_achievements.json')

def init_data_files():
    default_data = {
        USERS_FILE: {},
        POSTS_FILE: [],
        COMMENTS_FILE: [],
        INVENTORY_FILE: {},
        STATUSES_FILE: [],
        LIKES_FILE: {},
        GAMES_FILE: [],
        GAME_ACHIEVEMENTS_FILE: {},
        USER_ACHIEVEMENTS_FILE: {}
    }
    for filepath, default in default_data.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default, f, ensure_ascii=False, indent=2)

def load_users():
    init_data_files()
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_posts():
    init_data_files()
    try:
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_posts(posts):
    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def load_comments():
    init_data_files()
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_comments(comments):
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

def load_inventory():
    init_data_files()
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

def load_statuses():
    init_data_files()
    try:
        with open(STATUSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_statuses(statuses):
    with open(STATUSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(statuses, f, ensure_ascii=False, indent=2)

def load_likes():
    init_data_files()
    try:
        with open(LIKES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_likes(likes):
    with open(LIKES_FILE, 'w', encoding='utf-8') as f:
        json.dump(likes, f, ensure_ascii=False, indent=2)

def load_games():
    init_data_files()
    try:
        with open(GAMES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_games(games):
    with open(GAMES_FILE, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

def load_game_achievements():
    init_data_files()
    try:
        with open(GAME_ACHIEVEMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_game_achievements(achievements):
    with open(GAME_ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(achievements, f, ensure_ascii=False, indent=2)

def load_user_achievements():
    init_data_files()
    try:
        with open(USER_ACHIEVEMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}

def save_user_achievements(achievements):
    with open(USER_ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(achievements, f, ensure_ascii=False, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed

def allowed_file(filename, file_type='file'):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'avatar':
        return ext in app.config['AVATAR_EXTENSIONS']
    elif file_type == 'image':
        return ext in app.config['IMAGE_EXTENSIONS']
    elif file_type == 'inventory':
        return ext in app.config['INVENTORY_EXTENSIONS']
    elif file_type == 'game':
        return ext in app.config['GAME_EXTENSIONS']
    else:
        return ext in app.config['ALLOWED_EXTENSIONS']

def is_image(filename):
    return allowed_file(filename, 'image')

def is_3d_model(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in app.config['MODEL_EXTENSIONS']

def is_admin_or_moderator(username):
    users = load_users()
    user = users.get(username, {})
    role = user.get('role', 'user') if isinstance(user, dict) else 'user'
    return role in ['admin', 'moderator']

def is_creator():
    if 'user_id' not in session:
        return False
    username = session['user_id']
    users = load_users()
    user = users.get(username, {})
    role = user.get('role', 'user') if isinstance(user, dict) else 'user'
    return role == 'admin'

def can_edit_user(target_username):
    if 'user_id' not in session:
        return False
    
    current_user = session['user_id']
    users = load_users()
    current_role = users.get(current_user, {}).get('role', 'user')
    
    if current_role == 'admin':
        return True
    
    if current_role == 'moderator':
        target_role = users.get(target_username, {}).get('role', 'user')
        if target_role == 'admin' or current_user == target_username:
            return False
        return True
    
    return False

def is_banned(username):
    users = load_users()
    user = users.get(username, {})
    if not user.get('banned'):
        return False
    
    ban_until = user.get('ban_until')
    if not ban_until:
        return False
    
    if ban_until == 'forever':
        return True
    
    try:
        ban_date = datetime.strptime(ban_until, '%Y-%m-%d %H:%M:%S')
        return ban_date > datetime.now()
    except:
        return False

def get_user_avatar_url(username):
    if not username:
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
            <rect width="100" height="100" fill="#333333"/>
            <text x="50" y="60" font-family="Arial" font-size="40" fill="white" text-anchor="middle">?</text>
        </svg>'''
        svg_encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return f"data:image/svg+xml;base64,{svg_encoded}"
    users = load_users()
    user = users.get(username, {})
    if isinstance(user, dict) and user.get('avatar'):
        avatar_filename = user['avatar']
        avatar_path = os.path.join(app.config['AVATAR_FOLDER'], avatar_filename)
        if os.path.exists(avatar_path):
            return f"/static/avatars/{avatar_filename}"
    colors = ['#333333', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#AAAAAA']
    color = '#333333'
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            color = user_data.get('avatar_color', '#333333')
    first_letter = username[0].upper() if username else "?"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <rect width="100" height="100" fill="{color}"/>
        <text x="50" y="60" font-family="Arial" font-size="40" fill="white" text-anchor="middle">{first_letter}</text>
    </svg>'''
    svg_encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_encoded}"

def get_user_status(username):
    users = load_users()
    user = users.get(username, {})
    status_id = user.get('active_status')
    if not status_id:
        return None
    
    statuses = load_statuses()
    for status in statuses:
        if status.get('id') == status_id:
            return status
    return None

def get_time_ago(dt_str):
    if not dt_str:
        return "давно"
    try:
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except:
        return dt_str
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "только что"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} мин. назад"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} ч. назад"
    elif seconds < 2592000:
        days = int(seconds // 86400)
        return f"{days} дн. назад"
    elif seconds < 31536000:
        months = int(seconds // 2592000)
        return f"{months} мес. назад"
    else:
        years = int(seconds // 31536000)
        return f"{years} г. назад"

def process_avatar(image_data, username):
    try:
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        filename = f"{username}_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(app.config['AVATAR_FOLDER'], filename)
        old_avatar = load_users().get(username, {}).get('avatar')
        if old_avatar:
            old_path = os.path.join(app.config['AVATAR_FOLDER'], old_avatar)
            if os.path.exists(old_path):
                os.remove(old_path)
        image.save(filepath, 'JPEG', quality=85)
        return filename
    except Exception as e:
        print(f"Ошибка обработки аватара: {e}")
        return None

def create_default_admins():
    users = load_users()
    default_users = [
        {
            'username': 'admin',
            'email': 'admin@goteam.com',
            'password': hash_password('admin123'),
            'role': 'admin',
            'avatar_color': '#444444',
            'bio': 'Главный администратор GoTeam',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'posts_count': 0,
            'comments_count': 0,
            'activity_score': 1000,
            'active_status': None,
            'banned': False,
            'ban_until': None
        },
        {
            'username': 'moderator',
            'email': 'moderator@goteam.com',
            'password': hash_password('admin123'),
            'role': 'moderator',
            'avatar_color': '#555555',
            'bio': 'Модератор GoTeam',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'posts_count': 0,
            'comments_count': 0,
            'activity_score': 800,
            'active_status': None,
            'banned': False,
            'ban_until': None
        }
    ]
    for user_data in default_users:
        username = user_data['username']
        if username not in users:
            users[username] = {
                'username': username,
                'email': user_data['email'],
                'password': user_data['password'],
                'created_at': user_data['created_at'],
                'role': user_data['role'],
                'avatar_color': user_data['avatar_color'],
                'avatar': None,
                'bio': user_data['bio'],
                'posts_count': user_data['posts_count'],
                'comments_count': user_data['comments_count'],
                'activity_score': user_data['activity_score'],
                'online': False,
                'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'active_status': user_data['active_status'],
                'banned': user_data['banned'],
                'ban_until': user_data['ban_until']
            }
    save_users(users)

def can_like_post(username, post_id, post_author):
    if username == post_author:
        return False, "Нельзя лайкнуть свой пост"
    
    likes = load_likes()
    if post_id in likes and username in likes[post_id]:
        return False, "Вы уже лайкнули этот пост"
    
    return True, ""

def add_like(username, post_id):
    likes = load_likes()
    if post_id not in likes:
        likes[post_id] = []
    
    if username not in likes[post_id]:
        likes[post_id].append(username)
        save_likes(likes)
        
        posts = load_posts()
        for post in posts:
            if post.get('id') == post_id:
                post['likes'] = len(likes[post_id])
                break
        save_posts(posts)
    
    return len(likes[post_id])

def remove_like(username, post_id):
    likes = load_likes()
    if post_id in likes and username in likes[post_id]:
        likes[post_id].remove(username)
        save_likes(likes)
        
        posts = load_posts()
        for post in posts:
            if post.get('id') == post_id:
                post['likes'] = len(likes[post_id])
                break
        save_posts(posts)
    
    return len(likes.get(post_id, []))

def get_post_likes_count(post_id):
    likes = load_likes()
    return len(likes.get(post_id, []))

def has_user_liked(username, post_id):
    likes = load_likes()
    return post_id in likes and username in likes[post_id]

def validate_cloud_link(link):
    if not link:
        return False
    allowed_domains = ['yandex.ru', 'yandex.com', 'disk.yandex.ru', 'drive.google.com', 'google.com', 'mail.ru', 'cloud.mail.ru']
    for domain in allowed_domains:
        if domain in link:
            return True
    return False

GOTEAM_ICON_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBT9Qh8QAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAHsSURBVDiNjZK9S5thFMV/972TpjWpgUgNWsRBBMFBF1d14iZ06uLkH1BHQYqDi4PgIuIoUqSgIu2k4mKHQge7iOBQoULs4FI6pA5pYixJm7w+dXgfNQ1tO3iXc84993DOH5hMhqsA1wF+wK/X+wZwr9cLgKZp3R6PZ1wQhElCyzRNjDHm7OxsLQgCDg4OUBQl7na7H7Tb7QkA0zRpNpucnZ0RBEG83W4z2+32HwO0223cbjcTExMkEgkURUEQBGzbxrZtJEkCwLZtcrkco6OjBEGAy+WqyrIcDwQBp9OJIAg0m01UVcW2bU6Pj1mcn+f88hLbtgFYmJ9nf3+fWq0GgM/nq8bj8UcP7z6fD1EUOTg4oFqtUiqV2N/fp1KpUCqVKBaLlEolKpUKtVoN27YRBIGnT5+yvLzM58+fGXg8HiRJwrIsEokELpeLcrnM1tYW29vbxONxkskk5XKZ7e1tEokE2WyW4eFhZmdn2d7eZmNjo38PQCAQYG9vj3K5zPj4OHt7e5RKJSKRCJlMBkVRWFhYIJvNkslkyGQyhEIh8vk80WiUYrHI/v4+Jycn/YMQBIFOp0M+n2dlZYXl5WXy+TydTgfbtrFtG13XMQyDdrtNp9Oh1WoxGAyYnp6mXC5TqVTo9XoAQqFw+H8HYJomhmF0i8Ui8/Pz5PN5Dg8Pu7Zt9/+7mZkZ4vE4kUiERCKBJEnEYrG+zP8C+AE8UibcKz5sBQAAAABJRU5ErkJggg=="

BASE_TEMPLATE = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-card: #333333;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --accent: #4a4a4a;
            --accent-hover: #5a5a5a;
            --border: #404040;
            --success: #28a745;
            --danger: #dc3545;
            --warning: #ffc107;
            --info: #17a2b8;
            --liked: #ff4d4d;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding-bottom: 70px;
            line-height: 1.6;
        }
        
        .top-navbar {
            background-color: var(--bg-secondary);
            padding: 15px 0;
            border-bottom: 2px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .top-nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }
        
        .forum-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            font-size: 24px;
            font-weight: bold;
            color: var(--text-primary);
        }
        
        .logo-icon {
            width: 32px;
            height: 32px;
            background-image: url('data:image/png;base64,{{ goteam_icon }}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            filter: invert(1);
        }
        
        .main-container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 20px;
        }
        
        .post-card {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid var(--border);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .post-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .post-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--border);
        }
        
        .post-author-info {
            flex-grow: 1;
        }
        
        .post-author-name {
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 18px;
            flex-wrap: wrap;
        }
        
        .status-container {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            max-width: 40px;
            max-height: 40px;
            overflow: hidden;
            border-radius: 4px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .status-container:hover {
            transform: scale(1.1);
        }
        
        .status-image {
            width: auto;
            height: auto;
            max-width: 40px;
            max-height: 40px;
            object-fit: contain;
            display: block;
        }
        
        .status-3d-icon {
            width: 40px;
            height: 40px;
            background: var(--accent);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: var(--text-primary);
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .status-3d-icon:hover {
            transform: scale(1.1);
        }
        
        .post-time {
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 5px;
        }
        
        .post-title {
            font-size: 24px;
            margin-bottom: 15px;
            color: var(--text-primary);
        }
        
        .post-content {
            line-height: 1.8;
            margin-bottom: 20px;
            font-size: 16px;
            color: var(--text-secondary);
        }
        
        .post-attachments {
            margin: 20px 0;
        }
        
        .attachment-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        
        .attachment-item {
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        
        .attachment-item img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            display: block;
        }
        
        .attachment-info {
            padding: 8px;
            background: var(--bg-secondary);
            font-size: 12px;
            color: var(--text-secondary);
            text-align: center;
        }
        
        .post-actions {
            display: flex;
            gap: 20px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }
        
        .action-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 16px;
            padding: 8px 15px;
            border-radius: 8px;
            transition: all 0.2s;
        }
        
        .action-btn:hover {
            background-color: var(--accent);
            color: var(--text-primary);
        }
        
        .action-btn.liked {
            color: var(--liked);
        }
        
        .action-btn.liked:hover {
            color: var(--danger);
        }
        
        .action-btn.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .action-btn.disabled:hover {
            background-color: transparent;
            color: var(--text-secondary);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-control {
            width: 100%;
            padding: 15px;
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 16px;
            transition: border-color 0.2s;
        }
        
        .form-control:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(74,74,74,0.1);
        }
        
        textarea.form-control {
            min-height: 150px;
            resize: vertical;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-decoration: none;
        }
        
        .btn-primary {
            background-color: var(--accent);
            color: var(--text-primary);
        }
        
        .btn-primary:hover {
            background-color: var(--accent-hover);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .btn-secondary {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        .btn-success {
            background-color: var(--success);
            color: white;
        }
        
        .btn-danger {
            background-color: var(--danger);
            color: white;
        }
        
        .btn-ban {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .btn-game {
            background-color: var(--accent);
            color: var(--text-primary);
            padding: 8px 16px;
            font-size: 14px;
        }
        
        .btn-game:hover {
            background-color: var(--accent-hover);
        }
        
        .btn-cloud {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .bottom-navbar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: var(--bg-secondary);
            border-top: 2px solid var(--border);
            padding: 12px 0;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
        }
        
        .bottom-nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-around;
            padding: 0 20px;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-decoration: none;
            color: var(--text-secondary);
            padding: 10px 15px;
            border-radius: 10px;
            transition: all 0.3s;
            min-width: 80px;
        }
        
        .nav-item:hover, .nav-item.active {
            background-color: var(--accent);
            color: var(--text-primary);
            transform: translateY(-3px);
        }
        
        .nav-item i {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .nav-item span {
            font-size: 12px;
            font-weight: 500;
        }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .alert-success {
            background-color: rgba(40,167,69,0.1);
            border-color: var(--success);
            color: var(--success);
        }
        
        .alert-danger {
            background-color: rgba(220,53,69,0.1);
            border-color: var(--danger);
            color: var(--danger);
        }
        
        .alert-info {
            background-color: rgba(23,162,184,0.1);
            border-color: var(--info);
            color: var(--info);
        }
        
        .badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .badge-admin {
            background-color: var(--danger);
            color: white;
        }
        
        .badge-moderator {
            background-color: var(--success);
            color: white;
        }
        
        .badge-user {
            background-color: var(--accent);
            color: var(--text-primary);
        }
        
        .badge-achievement {
            background-color: var(--warning);
            color: black;
            font-weight: bold;
        }
        
        .profile-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .profile-avatar {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid var(--border);
            margin-bottom: 20px;
        }
        
        .profile-name {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .profile-stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 28px;
            font-weight: bold;
            color: var(--text-primary);
        }
        
        .stat-label {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        
        .profile-logout-btn {
            margin-top: 20px;
            display: inline-block;
        }
        
        .inventory-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .inventory-item {
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: transform 0.2s;
            cursor: pointer;
        }
        
        .inventory-item:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }
        
        .inventory-item img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .inventory-3d-preview {
            width: 100px;
            height: 100px;
            background: var(--accent);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-primary);
            margin: 0 auto 10px;
            font-size: 24px;
        }
        
        .inventory-item .item-name {
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 5px;
        }
        
        .inventory-item .item-type {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }
        
        .inventory-item .item-actions {
            display: flex;
            gap: 5px;
            justify-content: center;
        }
        
        .inventory-item .btn-small {
            padding: 5px 10px;
            font-size: 12px;
        }
        
        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .game-card {
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }
        
        .game-header {
            display: flex;
            align-items: center;
            padding: 15px;
            background: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .game-icon {
            width: 60px;
            height: 60px;
            border-radius: 8px;
            margin-right: 15px;
            object-fit: cover;
            border: 2px solid var(--border);
        }
        
        .game-title-section {
            flex-grow: 1;
        }
        
        .game-name {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .game-version {
            font-size: 12px;
            opacity: 0.8;
            background: var(--bg-primary);
            padding: 2px 6px;
            border-radius: 4px;
        }
        
        .game-author {
            font-size: 12px;
            opacity: 0.8;
        }
        
        .game-screenshots {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 5px;
            padding: 15px;
            background: var(--bg-primary);
        }
        
        .game-screenshot {
            width: 100%;
            height: 80px;
            object-fit: cover;
            border-radius: 4px;
            border: 1px solid var(--border);
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .game-screenshot:hover {
            transform: scale(1.05);
        }
        
        .game-description {
            padding: 15px;
            color: var(--text-secondary);
            font-size: 14px;
            line-height: 1.6;
            min-height: 80px;
            flex-grow: 1;
        }
        
        .game-footer {
            padding: 15px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .game-info {
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: var(--text-secondary);
            flex-wrap: wrap;
        }
        
        .game-info-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .game-achievements {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        
        .achievement-badge {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: var(--warning);
            color: black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid var(--border);
        }
        
        .game-actions {
            display: flex;
            gap: 10px;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }
        
        .modal-content {
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90%;
            position: relative;
            top: 50%;
            transform: translateY(-50%);
        }
        
        .modal-content img {
            width: 100%;
            height: auto;
            max-height: 90vh;
            object-fit: contain;
        }
        
        .close-modal {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            z-index: 2001;
        }
        
        .close-modal:hover {
            color: var(--accent);
        }
        
        .game-page {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 30px;
            border: 2px solid var(--border);
        }
        
        .game-page-header {
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .game-page-icon {
            width: 150px;
            height: 150px;
            border-radius: 12px;
            object-fit: cover;
            border: 3px solid var(--border);
        }
        
        .game-page-title-section {
            flex-grow: 1;
        }
        
        .game-page-name {
            font-size: 36px;
            font-weight: bold;
            color: var(--text-primary);
            margin-bottom: 10px;
        }
        
        .game-page-meta {
            display: flex;
            gap: 20px;
            color: var(--text-secondary);
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .game-page-meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .game-page-description {
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 30px;
            padding: 20px;
            background: var(--bg-primary);
            border-radius: 8px;
            color: var(--text-secondary);
        }
        
        .game-page-screenshots {
            margin-bottom: 30px;
        }
        
        .game-page-screenshots h3 {
            margin-bottom: 15px;
        }
        
        .screenshots-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .screenshot-thumb {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid var(--border);
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .screenshot-thumb:hover {
            transform: scale(1.05);
        }
        
        .game-page-achievements {
            margin-bottom: 30px;
        }
        
        .achievements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .achievement-card {
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            border: 2px solid var(--border);
            transition: transform 0.2s;
        }
        
        .achievement-card.earned {
            background: linear-gradient(135deg, #444444, #555555);
            border-color: var(--warning);
        }
        
        .achievement-card:hover {
            transform: scale(1.05);
        }
        
        .achievement-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--bg-secondary);
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: var(--text-primary);
        }
        
        .achievement-name {
            font-weight: bold;
            margin-bottom: 5px;
            color: var(--text-primary);
        }
        
        .achievement-desc {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .game-page-download {
            text-align: center;
            padding: 20px;
            background: var(--bg-primary);
            border-radius: 8px;
        }
        
        .download-options {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .download-btn {
            padding: 15px 40px;
            font-size: 18px;
            background: var(--accent);
            color: var(--text-primary);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }
        
        .cloud-btn {
            background: var(--bg-secondary);
        }
        
        .status-preview {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: var(--bg-primary);
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .status-icon-preview {
            width: auto;
            height: auto;
            max-width: 40px;
            max-height: 40px;
            object-fit: contain;
            cursor: pointer;
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 768px) {
            .main-container {
                padding: 0 15px;
            }
            
            .post-card {
                padding: 20px;
            }
            
            .bottom-nav-container {
                padding: 0 10px;
            }
            
            .nav-item {
                min-width: 70px;
                padding: 8px 10px;
            }
            
            .nav-item i {
                font-size: 20px;
            }
            
            .profile-stats {
                gap: 20px;
            }
            
            .games-grid {
                grid-template-columns: 1fr;
            }
            
            .game-header {
                flex-direction: column;
                text-align: center;
            }
            
            .game-icon {
                margin-right: 0;
                margin-bottom: 10px;
            }
            
            .game-footer {
                flex-direction: column;
            }
            
            .game-page-header {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            
            .screenshots-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }
            
            .download-options {
                flex-direction: column;
            }
        }
        
        .comment {
            background-color: var(--bg-card);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid var(--border);
        }
        
        .comment-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .comment-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--border);
        }
        
        .comment-author {
            display: flex;
            align-items: center;
            gap: 5px;
            flex-wrap: wrap;
            color: var(--text-primary);
        }
        
        .comment-time {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        .role-admin {
            color: var(--danger);
        }
        
        .role-moderator {
            color: var(--success);
        }
        
        .role-user {
            color: var(--text-secondary);
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }
        
        .empty-state i {
            font-size: 48px;
            margin-bottom: 15px;
            color: var(--text-secondary);
            opacity: 0.5;
        }
        
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-hover);
        }
        
        a {
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        a:hover {
            color: var(--text-secondary);
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            margin-bottom: 15px;
        }
        
        p, ul, ol {
            margin-bottom: 15px;
            color: var(--text-secondary);
        }
        
        input, textarea, select {
            font-family: inherit;
            font-size: 16px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .text-center {
            text-align: center;
        }
        
        .text-right {
            text-align: right;
        }
        
        .mt-1 { margin-top: 5px; }
        .mt-2 { margin-top: 10px; }
        .mt-3 { margin-top: 15px; }
        .mt-4 { margin-top: 20px; }
        .mt-5 { margin-top: 25px; }
        
        .mb-1 { margin-bottom: 5px; }
        .mb-2 { margin-bottom: 10px; }
        .mb-3 { margin-bottom: 15px; }
        .mb-4 { margin-bottom: 20px; }
        .mb-5 { margin-bottom: 25px; }
        
        .d-flex { display: flex; }
        .d-block { display: block; }
        .d-none { display: none; }
        
        .align-items-center { align-items: center; }
        .justify-content-between { justify-content: space-between; }
        .justify-content-center { justify-content: center; }
        
        .preview-loader {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .preview-loader i {
            font-size: 24px;
            color: var(--text-primary);
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Стили для аватара в редакторе */
        .avatar-preview-container {
            text-align: center;
            margin-bottom: 30px;
        }
        
        #avatarPreview {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--border);
            margin-bottom: 15px;
        }
        
        .avatar-input-container {
            margin-top: 15px;
        }
        
        .avatar-input-container input[type="file"] {
            color: var(--text-primary);
        }
        
        .avatar-hint {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 5px;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <nav class="top-navbar">
        <div class="top-nav-container">
            <a href="/" class="forum-logo">
                <div class="logo-icon"></div>
                <span>GoTeam</span>
            </a>
            <div class="top-nav-right">
                {% if 'user_id' in session %}
                <a href="/inventory" class="btn btn-secondary" style="padding: 8px 15px;">
                    <i class="fas fa-box"></i> Инвентарь
                </a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <div id="imageModal" class="modal">
        <span class="close-modal" onclick="closeImageModal()">&times;</span>
        <div class="modal-content" id="modalImageContainer">
            <img id="modalImage" src="">
        </div>
    </div>
    
    <div id="modelModal" class="modal">
        <div class="modal-content" style="background: var(--bg-card); padding: 20px;">
            <span class="close-modal" onclick="closeModelViewer()">&times;</span>
            <div id="modelViewer" class="model-viewer"></div>
        </div>
    </div>
    
    <div class="main-container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}"><i class="fas fa-info-circle"></i> {{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {{ content|safe }}
    </div>
    
    <nav class="bottom-navbar">
        <div class="bottom-nav-container">
            {{ bottom_nav|safe }}
        </div>
    </nav>
    
    <script>
        let currentModelViewer = null;
        let currentScene = null;
        let currentCamera = null;
        let currentRenderer = null;
        let currentControls = null;
        
        function openImageModal(imageUrl) {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImage');
            modal.style.display = 'block';
            modalImg.src = imageUrl;
        }
        
        function closeImageModal() {
            const modal = document.getElementById('imageModal');
            modal.style.display = 'none';
        }
        
        function openModelViewer(modelUrl, modelType) {
            const modal = document.getElementById('modelModal');
            const container = document.getElementById('modelViewer');
            
            if (currentRenderer) {
                currentRenderer.dispose();
            }
            
            modal.style.display = 'block';
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x2d2d2d);
            
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 5;
            
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.innerHTML = '';
            container.appendChild(renderer.domElement);
            
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = true;
            
            const ambientLight = new THREE.AmbientLight(0x404040);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(1, 1, 1);
            scene.add(directionalLight);
            
            const backLight = new THREE.DirectionalLight(0xffffff, 0.5);
            backLight.position.set(-1, -1, -1);
            scene.add(backLight);
            
            const gridHelper = new THREE.GridHelper(10, 20, 0x666666, 0x444444);
            scene.add(gridHelper);
            
            const loader = modelType === 'gltf' || modelType === 'glb' ? new THREE.GLTFLoader() : new THREE.OBJLoader();
            
            loader.load(
                modelUrl,
                function (object) {
                    if (modelType === 'gltf' || modelType === 'glb') {
                        scene.add(object.scene);
                    } else {
                        scene.add(object);
                    }
                    
                    const box = new THREE.Box3().setFromObject(object);
                    const center = box.getCenter(new THREE.Vector3());
                    const size = box.getSize(new THREE.Vector3());
                    
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 2 / maxDim;
                    object.scale.set(scale, scale, scale);
                    
                    object.position.x = -center.x * scale;
                    object.position.y = -center.y * scale;
                    object.position.z = -center.z * scale;
                },
                function (xhr) {
                    console.log((xhr.loaded / xhr.total * 100) + '% loaded');
                },
                function (error) {
                    console.error('Ошибка загрузки модели:', error);
                    container.innerHTML = '<div style="color: red; padding: 20px;">Ошибка загрузки 3D модели</div>';
                }
            );
            
            function animate() {
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }
            animate();
            
            currentScene = scene;
            currentCamera = camera;
            currentRenderer = renderer;
            currentControls = controls;
            
            window.addEventListener('resize', function() {
                if (currentRenderer && currentCamera) {
                    const width = container.clientWidth;
                    const height = container.clientHeight;
                    currentRenderer.setSize(width, height);
                    currentCamera.aspect = width / height;
                    currentCamera.updateProjectionMatrix();
                }
            });
        }
        
        function closeModelViewer() {
            const modal = document.getElementById('modelModal');
            modal.style.display = 'none';
            if (currentRenderer) {
                currentRenderer.dispose();
            }
        }
        
        function confirmDelete(type, id) {
            if (confirm("Удалить " + type + "? Это действие нельзя отменить.")) {
                window.location.href = "/delete/" + type + "/" + id;
            }
        }
        
        function likePost(postId) {
            fetch("/like_post/" + postId, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const elem = document.getElementById("likes-" + postId);
                    if (elem) elem.textContent = data.likes;
                    
                    const btn = document.getElementById("like-btn-" + postId);
                    if (btn) {
                        if (data.liked) {
                            btn.classList.add('liked');
                        } else {
                            btn.classList.remove('liked');
                        }
                    }
                } else {
                    alert(data.error);
                }
            });
        }
        
        function changeUserRole(username, newRole) {
            if (confirm("Изменить роль пользователя " + username + " на " + newRole + "?")) {
                fetch("/change_role/" + username + "/" + newRole)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Роль успешно изменена!");
                            location.reload();
                        } else {
                            alert("Ошибка: " + data.error);
                        }
                    });
            }
        }
        
        function banUser(username, days) {
            let banDays = days;
            if (days === undefined) {
                banDays = prompt("Введите количество дней бана (0 - навсегда):", "7");
                if (banDays === null) return;
                banDays = parseInt(banDays);
                if (isNaN(banDays)) banDays = 7;
            }
            
            if (confirm("Забанить пользователя " + username + (banDays > 0 ? " на " + banDays + " дней?" : " навсегда?"))) {
                fetch("/ban_user/" + username + "/" + banDays)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Пользователь забанен!");
                            location.reload();
                        } else {
                            alert("Ошибка: " + data.error);
                        }
                    });
            }
        }
        
        function unbanUser(username) {
            if (confirm("Разбанить пользователя " + username + "?")) {
                fetch("/unban_user/" + username)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Пользователь разбанен!");
                            location.reload();
                        } else {
                            alert("Ошибка: " + data.error);
                        }
                    });
            }
        }
        
        function setActiveStatus(statusId) {
            fetch("/set_active_status/" + statusId)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Статус активирован!");
                        location.reload();
                    } else {
                        alert("Ошибка: " + data.error);
                    }
                });
        }
        
        function deleteInventoryItem(itemId) {
            if (confirm("Удалить предмет из инвентаря?")) {
                fetch("/delete_inventory_item/" + itemId)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Предмет удален!");
                            location.reload();
                        } else {
                            alert("Ошибка: " + data.error);
                        }
                    });
            }
        }
        
        function awardAchievement(username, gameId, achievementId) {
            if (confirm("Выдать достижение пользователю " + username + "?")) {
                fetch("/award_achievement/" + username + "/" + gameId + "/" + achievementId)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert("Достижение выдано!");
                            location.reload();
                        } else {
                            alert("Ошибка: " + data.error);
                        }
                    });
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            const currentPath = window.location.pathname;
            const navItems = document.querySelectorAll('.nav-item');
            
            navItems.forEach(item => {
                const href = item.getAttribute('href');
                if (href === currentPath) {
                    item.classList.add('active');
                }
            });
            
            const avatarInput = document.getElementById('avatarInput');
            if (avatarInput) {
                avatarInput.addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(event) {
                            const img = document.getElementById('avatarPreview');
                            if (img) {
                                img.src = event.target.result;
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                });
            }
        });
        
        function saveAvatar() {
            const img = document.getElementById('avatarPreview');
            const base64Image = img.src;
            
            fetch('/upload_avatar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: base64Image.split(',')[1]
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Аватар успешно обновлен!');
                    location.reload();
                } else {
                    alert('Ошибка: ' + data.error);
                }
            });
        }
    </script>
</body>
</html>'''

# Главная страница
@app.route('/')
def index():
    if 'user_id' in session and is_banned(session['user_id']):
        session.clear()
        flash('Вы были забанены. Доступ запрещён.', 'danger')
        return redirect('/login')
    
    posts = load_posts()
    users = load_users()
    
    content = '<h2 style="margin-bottom: 25px; font-size: 28px;"><i class="fas fa-newspaper"></i> Последние посты GoTeam</h2>'
    
    if posts:
        for post in reversed(posts):
            post_id = post.get('id', '')
            author = post.get('author', 'Гость')
            title = post.get('title', 'Без названия')
            post_content = post.get('content', '')
            created_at = post.get('created_at', '')
            likes = get_post_likes_count(post_id)
            comment_count = post.get('comment_count', 0)
            
            time_ago = get_time_ago(created_at)
            avatar_url = get_user_avatar_url(author)
            
            status = get_user_status(author)
            status_html = ''
            if status:
                if status.get('type') == 'image':
                    status_html = f'''
                    <div class="status-container" onclick="openImageModal('/static/status/{status.get("file")}')" title="{status.get("name")}">
                        <img src="/static/status/{status.get("file")}" class="status-image">
                    </div>
                    '''
                elif status.get('type') == '3d':
                    ext = status.get('file', '').split('.')[-1].lower()
                    model_type = 'gltf' if ext in ['gltf', 'glb'] else 'obj'
                    status_html = f'''
                    <div class="status-3d-icon" onclick="openModelViewer('/static/status/{status.get("file")}', '{model_type}')" title="{status.get("name")} (3D)">
                        3D
                    </div>
                    '''
            
            role = 'user'
            if author in users:
                user_data = users[author]
                if isinstance(user_data, dict):
                    role = user_data.get('role', 'user')
            
            is_author_banned = is_banned(author)
            ban_info = ''
            if is_author_banned:
                ban_info = '<span class="badge badge-ban">Забанен</span>'
                post_content = "[Пользователь забанен. Сообщение скрыто.]"
            
            like_btn_class = 'action-btn'
            if 'user_id' in session:
                if has_user_liked(session['user_id'], post_id):
                    like_btn_class += ' liked'
                if session['user_id'] == author:
                    like_btn_class += ' disabled'
            
            files_html = ''
            attachments = post.get('attachments', [])
            image_attachments = [att for att in attachments if is_image(att.get('original_name', ''))]
            
            if image_attachments:
                files_html = '<div class="post-attachments">'
                files_html += '<h4 style="margin-bottom: 10px; color: var(--text-secondary);"><i class="fas fa-images"></i> Прикрепленные изображения</h4>'
                files_html += '<div class="attachment-grid">'
                
                for att in image_attachments[:6]:
                    original_name = att.get('original_name', 'Файл')
                    filename = att.get('filename', '')
                    file_url = f"/download/{post_id}/{att.get('id', '')}"
                    
                    files_html += f'''
                    <div class="attachment-item">
                        <a href="#" onclick="openImageModal('{file_url}'); return false;">
                            <img src="{file_url}" alt="{original_name}" 
                                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIj48cmVjdCB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iIzJkMmQyZCIvPjx0ZXh0IHg9Ijc1IiB5PSI3NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5Gb3RvPC90ZXh0Pjwvc3ZnPg=='; this.onerror=null;">
                            <div class="attachment-info">
                                <i class="fas fa-image"></i> {original_name[:15]}{"..." if len(original_name) > 15 else ""}
                            </div>
                        </a>
                    </div>
                    '''
                
                files_html += '</div>'
                
                other_files = [att for att in attachments if not is_image(att.get('original_name', ''))]
                if other_files:
                    files_html += '<div style="margin-top: 15px; padding: 10px; background: var(--bg-primary); border-radius: 8px;">'
                    files_html += '<h5 style="margin-bottom: 8px; color: var(--text-secondary);"><i class="fas fa-file"></i> Другие файлы</h5>'
                    for att in other_files[:3]:
                        original_name = att.get('original_name', 'Файл')
                        files_html += f'''
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                            <i class="fas fa-file"></i>
                            <span style="flex-grow: 1;">{original_name}</span>
                            <a href="/download/{post_id}/{att.get('id', '')}" class="btn btn-primary" style="padding: 4px 8px; font-size: 12px;">
                                <i class="fas fa-download"></i>
                            </a>
                        </div>
                        '''
                    files_html += '</div>'
                
                files_html += '</div>'
            
            delete_button = ''
            if 'user_id' in session:
                current_user = session['user_id']
                user_role = users.get(current_user, {}).get('role', 'user') if current_user in users else 'user'
                
                if current_user == author or user_role in ['admin', 'moderator']:
                    delete_button = f'''
                    <button onclick="confirmDelete('post', '{post_id}')" class="btn btn-danger" style="margin-left: 10px;">
                        <i class="fas fa-trash"></i> Удалить
                    </button>
                    '''
            
            content += f'''
            <div class="post-card fade-in">
                <a href="/profile/{author}" style="text-decoration: none; color: inherit;">
                    <div class="post-header">
                        <img src="{avatar_url}" alt="{author}" class="user-avatar" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzJkMmQyZCIvPjx0ZXh0IHg9IjUwIiB5PSI2MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjQwIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj57eyBmaXJzdCBsZXR0ZXIgfX08L3RleHQ+PC9zdmc+'; this.onerror=null;">
                        <div class="post-author-info">
                            <div class="post-author-name">
                                {author}
                                {status_html}
                                <span class="badge {'badge-admin' if role == 'admin' else 'badge-moderator' if role == 'moderator' else 'badge-user'}">
                                    {role}
                                </span>
                                {ban_info}
                            </div>
                            <div class="post-time">
                                <i class="far fa-clock"></i> {time_ago}
                            </div>
                        </div>
                    </div>
                </a>
                
                <h3 class="post-title">{title}</h3>
                
                <div class="post-content">
                    {post_content.replace(chr(10), '<br>')}
                </div>
                
                {files_html}
                
                <div class="post-actions">
                    <button id="like-btn-{post_id}" onclick="likePost('{post_id}')" class="{like_btn_class}" {'disabled' if 'user_id' in session and session['user_id'] == author else ''}>
                        <i class="fas fa-heart"></i>
                        <span id="likes-{post_id}">{likes}</span>
                    </button>
                    
                    <a href="/post/{post_id}" class="action-btn">
                        <i class="fas fa-comment"></i>
                        <span>{comment_count}</span>
                    </a>
                    
                    {delete_button}
                </div>
            </div>
            '''
    else:
        content += '''
        <div class="empty-state">
            <i class="fas fa-users"></i>
            <h3>Пока нет постов в GoTeam</h3>
            <p>Будьте первым, кто создаст пост в нашем сообществе!</p>
            '''
        
        if 'user_id' in session:
            content += '''
            <a href="/create_post" class="btn btn-primary" style="margin-top: 20px;">
                <i class="fas fa-plus"></i> Создать первый пост
            </a>
            '''
        else:
            content += '''
            <a href="/login" class="btn btn-primary" style="margin-top: 20px;">
                <i class="fas fa-sign-in-alt"></i> Войти, чтобы создать пост
            </a>
            '''
        
        content += '</div>'
    
    bottom_nav = ''
    if 'user_id' in session:
        username = session['user_id']
        bottom_nav = f'''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/create_post" class="nav-item">
            <i class="fas fa-plus-square"></i>
            <span>Создать</span>
        </a>
        
        <a href="/inventory" class="nav-item">
            <i class="fas fa-box"></i>
            <span>Инвентарь</span>
        </a>
        
        <a href="/profile/{username}" class="nav-item">
            <i class="fas fa-user"></i>
            <span>Профиль</span>
        </a>
        
        <a href="/logout" class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Выйти</span>
        </a>
        '''
    else:
        bottom_nav = '''
        <a href="/" class="nav-item active">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/login" class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span>Войти</span>
        </a>
        
        <a href="/register" class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span>Регистрация</span>
        </a>
        '''
    
    return render_template_string(BASE_TEMPLATE,
        title="GoTeam - Главная",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not email or not password:
            flash('Все поля обязательны для заполнения', 'danger')
            return redirect('/register')
        
        if len(username) < 3:
            flash('Имя пользователя должно быть не менее 3 символов', 'danger')
            return redirect('/register')
        
        if len(password) < 6:
            flash('Пароль должен быть не менее 6 символов', 'danger')
            return redirect('/register')
        
        users = load_users()
        
        if username in users:
            flash('Имя пользователя уже занято', 'danger')
            return redirect('/register')
        
        import random
        colors = ['#333333', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#AAAAAA']
        
        users[username] = {
            'username': username,
            'email': email,
            'password': hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'role': 'user',
            'avatar_color': random.choice(colors),
            'avatar': None,
            'bio': 'Новый участник GoTeam',
            'posts_count': 0,
            'comments_count': 0,
            'activity_score': 0,
            'online': True,
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'active_status': None,
            'banned': False,
            'ban_until': None
        }
        
        save_users(users)
        
        inventory = load_inventory()
        inventory[username] = []
        save_inventory(inventory)
        
        session['user_id'] = username
        session['username'] = username
        
        flash(f'Регистрация успешна! Добро пожаловать в GoTeam, {username}! 🎉', 'success')
        return redirect('/')
    
    content = '''
    <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-user-plus"></i> Регистрация в GoTeam</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Имя пользователя</label>
                <input type="text" name="username" class="form-control" required 
                       placeholder="Введите имя пользователя (мин. 3 символа)">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Email</label>
                <input type="email" name="email" class="form-control" required 
                       placeholder="Введите ваш email">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Пароль</label>
                <input type="password" name="password" class="form-control" required 
                       placeholder="Введите пароль (мин. 6 символов)">
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 12px; margin-top: 20px;">
                <i class="fas fa-user-plus"></i> Зарегистрироваться и войти
            </button>
            
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: var(--text-secondary);">Уже есть аккаунт? <a href="/login" style="color: var(--text-primary); text-decoration: none;">Войти в GoTeam</a></p>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = '''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/login" class="nav-item">
        <i class="fas fa-sign-in-alt"></i>
        <span>Войти</span>
    </a>
    
    <a href="/register" class="nav-item active">
        <i class="fas fa-user-plus"></i>
        <span>Регистрация</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Регистрация - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Введите имя пользователя и пароль', 'danger')
            return redirect('/login')
        
        users = load_users()
        
        if username in users:
            user_data = users[username]
            
            if is_banned(username):
                ban_until = user_data.get('ban_until')
                if ban_until == 'forever':
                    flash('Вы забанены навсегда', 'danger')
                else:
                    try:
                        ban_date = datetime.strptime(ban_until, '%Y-%m-%d %H:%M:%S')
                        flash(f'Вы забанены до {ban_date.strftime("%d.%m.%Y %H:%M")}', 'danger')
                    except:
                        flash('Вы забанены', 'danger')
                return redirect('/login')
            
            if isinstance(user_data, dict) and check_password(password, user_data.get('password', '')):
                session['user_id'] = username
                session['username'] = username
                
                users[username]['online'] = True
                users[username]['last_seen'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_users(users)
                
                flash(f'Добро пожаловать в GoTeam, {username}!', 'success')
                return redirect('/')
        
        flash('Неверное имя пользователя или пароль', 'danger')
        return redirect('/login')
    
    content = '''
    <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-sign-in-alt"></i> Вход в GoTeam</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Имя пользователя</label>
                <input type="text" name="username" class="form-control" required 
                       placeholder="Введите имя пользователя">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Пароль</label>
                <input type="password" name="password" class="form-control" required 
                       placeholder="Введите пароль">
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%; padding: 12px; margin-top: 20px;">
                <i class="fas fa-sign-in-alt"></i> Войти
            </button>
            
            <div style="text-align: center; margin-top: 20px;">
                <p style="color: var(--text-secondary);">Нет аккаунта? <a href="/register" style="color: var(--text-primary); text-decoration: none;">Зарегистрироваться в GoTeam</a></p>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = '''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/login" class="nav-item active">
        <i class="fas fa-sign-in-alt"></i>
        <span>Войти</span>
    </a>
    
    <a href="/register" class="nav-item">
        <i class="fas fa-user-plus"></i>
        <span>Регистрация</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Вход - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Выход
@app.route('/logout')
def logout():
    if 'user_id' in session:
        users = load_users()
        username = session['user_id']
        if username in users:
            users[username]['online'] = False
            save_users(users)
    
    session.clear()
    flash('Вы успешно вышли из GoTeam', 'info')
    return redirect('/')

# Профиль пользователя
@app.route('/profile/<username>')
def profile(username):
    if 'user_id' in session and is_banned(session['user_id']):
        session.clear()
        flash('Вы забанены. Доступ запрещён.', 'danger')
        return redirect('/login')
    
    users = load_users()
    
    if username not in users:
        flash('Пользователь не найден', 'danger')
        return redirect('/')
    
    user_data = users[username]
    
    posts = load_posts()
    user_posts = [post for post in posts if post.get('author') == username]
    
    comments = load_comments()
    user_comments = [comment for comment in comments if comment.get('author') == username]
    
    avatar_url = get_user_avatar_url(username)
    
    status = get_user_status(username)
    status_html = ''
    if status:
        if status.get('type') == 'image':
            status_html = f'''
            <div class="status-container" onclick="openImageModal('/static/status/{status.get("file")}')" title="{status.get("name")}">
                <img src="/static/status/{status.get("file")}" class="status-image">
            </div>
            '''
        elif status.get('type') == '3d':
            ext = status.get('file', '').split('.')[-1].lower()
            model_type = 'gltf' if ext in ['gltf', 'glb'] else 'obj'
            status_html = f'''
            <div class="status-3d-icon" onclick="openModelViewer('/static/status/{status.get("file")}', '{model_type}')" title="{status.get("name")} (3D)">
                3D
            </div>
            '''
    
    role = user_data.get('role', 'user')
    
    is_user_banned = is_banned(username)
    ban_info = ''
    if is_user_banned:
        ban_until = user_data.get('ban_until')
        if ban_until == 'forever':
            ban_info = '<span class="badge badge-ban">Забанен навсегда</span>'
        elif ban_until:
            try:
                ban_date = datetime.strptime(ban_until, '%Y-%m-%d %H:%M:%S')
                ban_info = f'<span class="badge badge-ban">Забанен до {ban_date.strftime("%d.%m.%Y")}</span>'
            except:
                ban_info = '<span class="badge badge-ban">Забанен</span>'
    
    content = f'''
    <div class="profile-header">
        <div class="profile-avatar-container">
            <img src="{avatar_url}" alt="{username}" class="profile-avatar" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iIzJkMmQyZCIvPjx0ZXh0IHg9IjUwIiB5PSI2MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjQwIiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj57eyBmaXJzdCBsZXR0ZXIgfX08L3RleHQ+PC9zdmc+'; this.onerror=null;">
        </div>
        <h1 class="profile-name">
            {username}
            {status_html}
            {ban_info}
        </h1>
        <div class="profile-role">{role}</div>
        <p class="profile-bio">{user_data.get('bio', '')}</p>
        
        <div class="profile-stats">
            <div class="stat-item">
                <div class="stat-number">{len(user_posts)}</div>
                <div class="stat-label">Посты</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{len(user_comments)}</div>
                <div class="stat-label">Комментарии</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{user_data.get('activity_score', 0)}</div>
                <div class="stat-label">Активность</div>
            </div>
        </div>
    '''
    
    if 'user_id' in session:
        current_user = session['user_id']
        
        if current_user == username:
            content += f'''
            <div style="margin-top: 20px;">
                <a href="/edit_profile" class="btn btn-primary" style="margin-right: 10px;">
                    <i class="fas fa-edit"></i> Редактировать
                </a>
                <a href="/inventory" class="btn btn-success" style="margin-right: 10px;">
                    <i class="fas fa-box"></i> Инвентарь
                </a>
                <a href="/logout" class="btn btn-danger">
                    <i class="fas fa-sign-out-alt"></i> Выйти
                </a>
            </div>
            '''
    
    content += '</div>'
    
    content += '<h3 style="margin: 30px 0 20px 0;">Последние посты</h3>'
    
    if user_posts and not is_user_banned:
        for post in reversed(user_posts[-5:]):
            likes = get_post_likes_count(post.get('id'))
            content += f'''
            <div class="post-card" style="margin-bottom: 15px;">
                <h4><a href="/post/{post.get('id', '')}" style="color: var(--text-primary);">{post.get('title', 'Без названия')}</a></h4>
                <p style="color: var(--text-secondary); font-size: 14px;">
                    {get_time_ago(post.get('created_at', ''))} | ❤️ {likes} | 💬 {post.get('comment_count', 0)}
                </p>
            </div>
            '''
    elif is_user_banned:
        content += '<p>Пользователь забанен</p>'
    else:
        content += '<p>Нет постов</p>'
    
    bottom_nav = ''
    if 'user_id' in session:
        username = session['user_id']
        bottom_nav = f'''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/create_post" class="nav-item">
            <i class="fas fa-plus-square"></i>
            <span>Создать</span>
        </a>
        
        <a href="/inventory" class="nav-item">
            <i class="fas fa-box"></i>
            <span>Инвентарь</span>
        </a>
        
        <a href="/profile/{username}" class="nav-item active">
            <i class="fas fa-user"></i>
            <span>Профиль</span>
        </a>
        
        <a href="/logout" class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Выйти</span>
        </a>
        '''
    else:
        bottom_nav = '''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/login" class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span>Войти</span>
        </a>
        
        <a href="/register" class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span>Регистрация</span>
        </a>
        '''
    
    return render_template_string(BASE_TEMPLATE,
        title=f"Профиль {username} - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Редактирование профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    users = load_users()
    
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        email = request.form.get('email', '').strip()
        
        users[username]['bio'] = bio
        users[username]['email'] = email
        
        save_users(users)
        
        flash('Профиль обновлен!', 'success')
        return redirect(f'/profile/{username}')
    
    avatar_url = get_user_avatar_url(username)
    
    content = f'''
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-user-edit"></i> Редактирование профиля</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <div class="avatar-preview-container">
            <img id="avatarPreview" src="{avatar_url}" alt="Avatar" class="profile-avatar">
            
            <div class="avatar-input-container">
                <input type="file" id="avatarInput" accept="image/*">
                <p class="avatar-hint"><i class="fas fa-info-circle"></i> Выберите изображение для аватара (JPG, PNG, GIF)</p>
                <button onclick="saveAvatar()" class="btn btn-success" style="margin-top: 10px;">
                    <i class="fas fa-save"></i> Сохранить аватар
                </button>
            </div>
        </div>
        
        <form method="POST">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Имя пользователя</label>
                <input type="text" value="{username}" class="form-control" disabled>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Email</label>
                <input type="email" name="email" value="{users[username].get('email', '')}" class="form-control" required>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">О себе</label>
                <textarea name="bio" class="form-control" rows="4">{users[username].get('bio', '')}</textarea>
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-success" style="flex: 1;">
                    <i class="fas fa-save"></i> Сохранить изменения
                </button>
                <a href="/profile/{username}" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Отмена
                </a>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item active">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Редактирование профиля",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Загрузка аватара
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    username = session['user_id']
    
    if is_banned(username):
        return jsonify({'success': False, 'error': 'Забанен'}), 403
    
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'Нет данных'}), 400
        
        image_data = base64.b64decode(data['image'])
        filename = process_avatar(image_data, username)
        
        if filename:
            users = load_users()
            users[username]['avatar'] = filename
            save_users(users)
            return jsonify({'success': True, 'avatar_url': f"/static/avatars/{filename}"})
        
        return jsonify({'success': False, 'error': 'Ошибка обработки'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Инвентарь
@app.route('/inventory')
@app.route('/inventory/<username>')
def inventory(username=None):
    if 'user_id' not in session:
        flash('Войдите в систему', 'danger')
        return redirect('/login')
    
    current_user = session['user_id']
    
    if is_banned(current_user):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if not username:
        username = current_user
    
    users = load_users()
    if username not in users:
        flash('Пользователь не найден', 'danger')
        return redirect('/')
    
    inventory_data = load_inventory()
    user_inventory = inventory_data.get(username, [])
    
    content = f'<h2><i class="fas fa-box"></i> Инвентарь {username}</h2>'
    
    if current_user == username or is_admin_or_moderator(current_user):
        content += '<div style="margin: 20px 0;"><a href="/add_inventory_item" class="btn btn-primary"><i class="fas fa-plus"></i> Добавить предмет</a> '
        content += '<a href="/statuses" class="btn btn-secondary"><i class="fas fa-star"></i> Управление статусами</a></div>'
    
    if user_inventory:
        content += '<div class="inventory-grid">'
        for item in user_inventory:
            item_id = item.get('id')
            item_name = item.get('name', 'Без названия')
            item_type = item.get('type', 'image')
            item_file = item.get('file')
            
            preview_html = ''
            if item_type == 'image' and item_file:
                preview_html = f'<img src="/static/inventory/{item_file}" onclick="openImageModal(\'/static/inventory/{item_file}\')">'
            elif item_type == '3d':
                ext = item_file.split('.')[-1].lower() if item_file else ''
                model_type = 'gltf' if ext in ['gltf', 'glb'] else 'obj'
                preview_html = f'<div class="inventory-3d-preview" onclick="openModelViewer(\'/static/inventory/{item_file}\', \'{model_type}\')"><i class="fas fa-cube"></i></div>'
            else:
                preview_html = '<div class="inventory-3d-preview"><i class="fas fa-file"></i></div>'
            
            actions = ''
            if current_user == username or is_admin_or_moderator(current_user):
                actions = f'''
                <div class="item-actions">
                    <button onclick="setActiveStatus(\'{item_id}\')" class="btn btn-success btn-small" title="Использовать как статус">
                        <i class="fas fa-star"></i>
                    </button>
                    <button onclick="deleteInventoryItem(\'{item_id}\')" class="btn btn-danger btn-small" title="Удалить">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                '''
            
            content += f'''
            <div class="inventory-item">
                {preview_html}
                <div class="item-name">{item_name}</div>
                <div class="item-type">{item_type}</div>
                {actions}
            </div>
            '''
        content += '</div>'
    else:
        content += '<div class="empty-state"><i class="fas fa-box-open"></i><h3>Инвентарь пуст</h3><p>Добавьте предметы в инвентарь</p></div>'
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item active">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{current_user}" class="nav-item">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Инвентарь - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Добавление предмета в инвентарь
@app.route('/add_inventory_item', methods=['GET', 'POST'])
def add_inventory_item():
    if 'user_id' not in session:
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        item_name = request.form.get('name', '').strip()
        
        if not item_name:
            flash('Введите название', 'danger')
            return redirect('/add_inventory_item')
        
        if 'file' not in request.files:
            flash('Выберите файл', 'danger')
            return redirect('/add_inventory_item')
        
        file = request.files['file']
        if not file or not file.filename:
            flash('Выберите файл', 'danger')
            return redirect('/add_inventory_item')
        
        if not allowed_file(file.filename, 'inventory'):
            flash('Недопустимый формат', 'danger')
            return redirect('/add_inventory_item')
        
        try:
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{username}_{uuid.uuid4().hex[:8]}.{ext}"
            filepath = os.path.join(app.config['INVENTORY_FOLDER'], filename)
            file.save(filepath)
            
            if is_image(file.filename):
                actual_type = 'image'
            elif is_3d_model(file.filename):
                actual_type = '3d'
            else:
                actual_type = 'other'
            
            inventory = load_inventory()
            
            if username not in inventory:
                inventory[username] = []
            
            item = {
                'id': str(uuid.uuid4())[:8],
                'name': item_name,
                'type': actual_type,
                'file': filename,
                'original_name': file.filename,
                'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            inventory[username].append(item)
            save_inventory(inventory)
            
            flash('Предмет добавлен!', 'success')
            return redirect('/inventory')
            
        except Exception as e:
            flash('Ошибка загрузки', 'danger')
            return redirect('/add_inventory_item')
    
    content = '''
    <div style="max-width: 500px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-plus"></i> Добавить предмет в инвентарь</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Название предмета</label>
                <input type="text" name="name" class="form-control" required 
                       placeholder="Введите название предмета">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Файл</label>
                <input type="file" name="file" class="form-control" required 
                       accept=".png,.jpg,.jpeg,.gif,.obj,.fbx,.stl,.gltf,.glb,.blend,.mtl,.mp4,.mp3">
                <p class="avatar-hint"><i class="fas fa-info-circle"></i> Поддерживаются: изображения, 3D модели, видео, аудио</p>
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-success" style="flex: 1;">
                    <i class="fas fa-save"></i> Добавить
                </button>
                <a href="/inventory" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Отмена
                </a>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item active">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Добавление предмета",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Удаление предмета
@app.route('/delete_inventory_item/<item_id>')
def delete_inventory_item(item_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    username = session['user_id']
    
    if is_banned(username):
        return jsonify({'success': False, 'error': 'Забанен'}), 403
    
    inventory = load_inventory()
    
    if username not in inventory:
        return jsonify({'success': False, 'error': 'Не найден'}), 404
    
    user_items = inventory[username]
    new_items = []
    deleted_file = None
    
    for item in user_items:
        if item.get('id') == item_id:
            deleted_file = item.get('file')
        else:
            new_items.append(item)
    
    inventory[username] = new_items
    save_inventory(inventory)
    
    if deleted_file:
        filepath = os.path.join(app.config['INVENTORY_FOLDER'], deleted_file)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
    
    return jsonify({'success': True})

# Страница статусов
@app.route('/statuses')
def statuses():
    if 'user_id' not in session:
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    users = load_users()
    user_data = users.get(username, {})
    
    statuses_list = load_statuses()
    user_statuses = [s for s in statuses_list if s.get('owner') == username]
    
    content = f'<h2><i class="fas fa-star"></i> Мои статусы</h2>'
    content += '<div style="margin: 20px 0;"><a href="/add_status" class="btn btn-primary"><i class="fas fa-plus"></i> Создать статус</a></div>'
    
    if user_statuses:
        for status in user_statuses:
            status_id = status.get('id')
            status_name = status.get('name')
            status_type = status.get('type')
            status_file = status.get('file')
            is_active = user_data.get('active_status') == status_id
            
            preview_html = ''
            if status_type == 'image' and status_file:
                preview_html = f'<img src="/static/status/{status_file}" class="status-icon-preview" onclick="openImageModal(\'/static/status/{status_file}\')">'
            elif status_type == '3d':
                ext = status_file.split('.')[-1].lower() if status_file else ''
                model_type = 'gltf' if ext in ['gltf', 'glb'] else 'obj'
                preview_html = f'<div class="inventory-3d-preview" style="width: 40px; height: 40px;" onclick="openModelViewer(\'/static/status/{status_file}\', \'{model_type}\')"><i class="fas fa-cube"></i></div>'
            
            active_button = ''
            if is_active:
                active_button = '<span class="badge badge-success">Активен</span>'
            else:
                active_button = f'<button onclick="setActiveStatus(\'{status_id}\')" class="btn btn-success btn-small">Активировать</button>'
            
            content += f'''
            <div class="status-preview">
                {preview_html}
                <div style="flex-grow: 1;">
                    <div style="font-weight: bold;">{status_name}</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">Тип: {status_type}</div>
                </div>
                <div>
                    {active_button}
                </div>
            </div>
            '''
    else:
        content += '<div class="empty-state"><i class="fas fa-star"></i><h3>Нет статусов</h3><p>Создайте статус из предметов в инвентаре</p></div>'
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item active">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Статусы - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Добавление статуса
@app.route('/add_status', methods=['GET', 'POST'])
def add_status():
    if 'user_id' not in session:
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    inventory = load_inventory()
    user_inventory = inventory.get(username, [])
    
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        
        if not item_id:
            flash('Выберите предмет', 'danger')
            return redirect('/add_status')
        
        selected_item = None
        for item in user_inventory:
            if item.get('id') == item_id:
                selected_item = item
                break
        
        if not selected_item:
            flash('Предмет не найден', 'danger')
            return redirect('/add_status')
        
        try:
            source_file = os.path.join(app.config['INVENTORY_FOLDER'], selected_item['file'])
            if not os.path.exists(source_file):
                flash('Файл не найден', 'danger')
                return redirect('/add_status')
            
            ext = selected_item['file'].rsplit('.', 1)[1].lower()
            status_filename = f"status_{username}_{uuid.uuid4().hex[:8]}.{ext}"
            status_filepath = os.path.join(app.config['STATUS_FOLDER'], status_filename)
            
            import shutil
            shutil.copy2(source_file, status_filepath)
            
            statuses = load_statuses()
            status = {
                'id': str(uuid.uuid4())[:8],
                'name': selected_item['name'],
                'type': selected_item['type'],
                'file': status_filename,
                'owner': username,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            statuses.append(status)
            save_statuses(statuses)
            
            flash('Статус создан!', 'success')
            return redirect('/statuses')
            
        except Exception as e:
            flash('Ошибка создания статуса', 'danger')
            return redirect('/add_status')
    
    if not user_inventory:
        flash('Сначала добавьте предметы в инвентарь', 'warning')
        return redirect('/inventory')
    
    content = f'''
    <h2><i class="fas fa-plus"></i> Создать статус</h2>
    <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
    
    <form method="POST">
        <div class="form-group">
            <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Выберите предмет из инвентаря</label>
            <select name="item_id" class="form-control" required>
                <option value="">-- Выберите предмет --</option>
    '''
    
    for item in user_inventory:
        content += f'<option value="{item.get("id")}">{item.get("name")} ({item.get("type")})</option>'
    
    content += '''
            </select>
        </div>
        
        <div style="display: flex; gap: 10px; margin-top: 20px;">
            <button type="submit" class="btn btn-success" style="flex: 1;">
                <i class="fas fa-star"></i> Создать статус
            </button>
            <a href="/statuses" class="btn btn-secondary">
                <i class="fas fa-times"></i> Отмена
            </a>
        </div>
    </form>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item active">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Создание статуса",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Установка активного статуса
@app.route('/set_active_status/<status_id>')
def set_active_status(status_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    username = session['user_id']
    
    if is_banned(username):
        return jsonify({'success': False, 'error': 'Забанен'}), 403
    
    users = load_users()
    
    if username not in users:
        return jsonify({'success': False, 'error': 'Не найден'}), 404
    
    statuses = load_statuses()
    status_exists = False
    
    for status in statuses:
        if status.get('id') == status_id and status.get('owner') == username:
            status_exists = True
            break
    
    if not status_exists:
        return jsonify({'success': False, 'error': 'Статус не найден'}), 404
    
    users[username]['active_status'] = status_id
    save_users(users)
    
    return jsonify({'success': True})

# Страница игр
@app.route('/games')
def games():
    if 'user_id' in session and is_banned(session['user_id']):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    games_list = load_games()
    
    content = '<h2><i class="fas fa-gamepad"></i> Игры GoTeam</h2>'
    content += '<div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>'
    
    if 'user_id' in session:
        content += '<div style="margin: 20px 0;"><a href="/add_game" class="btn btn-primary"><i class="fas fa-plus"></i> Добавить игру</a></div>'
    
    if games_list:
        games_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        content += '<div class="games-grid">'
        for game in games_list:
            game_id = game.get('id')
            game_name = game.get('name', 'Без названия')
            game_icon = game.get('icon', '')
            game_version = game.get('version', '1.0')
            game_author = game.get('author', 'Неизвестен')
            game_description = game.get('description', '')
            game_screenshots = game.get('screenshots', [])
            game_language = game.get('language', 'Русский')
            game_size = game.get('size', '0 MB')
            game_downloads = game.get('downloads', 0)
            
            game_achs = load_game_achievements().get(game_id, [])
            
            if len(game_description) > 100:
                game_description = game_description[:97] + '...'
            
            icon_html = f'<img src="/static/games/icons/{game_icon}" class="game-icon">' if game_icon else '<div class="game-icon" style="background: var(--accent); display: flex; align-items: center; justify-content: center; color: var(--text-primary);">G</div>'
            
            screenshots_html = ''
            if game_screenshots:
                for i, ss in enumerate(game_screenshots[:3]):
                    screenshots_html += f'<img src="/static/games/screenshots/{ss}" class="game-screenshot" onclick="openImageModal(\'/static/games/screenshots/{ss}\')">'
                for i in range(3 - len(game_screenshots[:3])):
                    screenshots_html += '<div class="game-screenshot" style="background: var(--bg-primary);"></div>'
            else:
                for i in range(3):
                    screenshots_html += '<div class="game-screenshot" style="background: var(--bg-primary);"></div>'
            
            achievements_html = ''
            if game_achs:
                for ach in game_achs[:3]:
                    achievements_html += f'<div class="achievement-badge" title="{ach.get("name", "")}">{ach.get("icon", "🏆")}</div>'
            
            content += f'''
            <div class="game-card">
                <div class="game-header">
                    {icon_html}
                    <div class="game-title-section">
                        <div class="game-name">{game_name} <span class="game-version">v{game_version}</span></div>
                        <div class="game-author"><i class="fas fa-user"></i> {game_author}</div>
                    </div>
                </div>
                <div class="game-screenshots">{screenshots_html}</div>
                <div class="game-description">{game_description}</div>
                <div class="game-footer">
                    <div class="game-info">
                        <span class="game-info-item"><i class="fas fa-globe"></i> {game_language}</span>
                        <span class="game-info-item"><i class="fas fa-database"></i> {game_size}</span>
                        <span class="game-info-item"><i class="fas fa-download"></i> {game_downloads}</span>
                    </div>
                    <div class="game-achievements">{achievements_html}</div>
                    <a href="/game/{game_id}" class="btn btn-game">Подробнее</a>
                </div>
            </div>
            '''
        content += '</div>'
    else:
        content += '<div class="empty-state"><i class="fas fa-gamepad"></i><h3>Нет игр</h3><p>Будьте первым, кто добавит игру</p></div>'
    
    bottom_nav = ''
    if 'user_id' in session:
        username = session['user_id']
        bottom_nav = f'''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item active">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/create_post" class="nav-item">
            <i class="fas fa-plus-square"></i>
            <span>Создать</span>
        </a>
        
        <a href="/inventory" class="nav-item">
            <i class="fas fa-box"></i>
            <span>Инвентарь</span>
        </a>
        
        <a href="/profile/{username}" class="nav-item">
            <i class="fas fa-user"></i>
            <span>Профиль</span>
        </a>
        
        <a href="/logout" class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Выйти</span>
        </a>
        '''
    else:
        bottom_nav = '''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item active">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/login" class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span>Войти</span>
        </a>
        
        <a href="/register" class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span>Регистрация</span>
        </a>
        '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Игры - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Добавление игры
@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if 'user_id' not in session:
        flash('Войдите в систему', 'danger')
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        game_name = request.form.get('name', '').strip()
        game_version = request.form.get('version', '1.0').strip()
        game_description = request.form.get('description', '').strip()
        game_language = request.form.get('language', 'Русский').strip()
        game_size = request.form.get('size', '0 MB').strip()
        download_type = request.form.get('download_type', 'file')
        cloud_link = request.form.get('cloud_link', '').strip()
        
        if not game_name or not game_description:
            flash('Заполните обязательные поля', 'danger')
            return redirect('/add_game')
        
        if download_type == 'cloud':
            if not cloud_link:
                flash('Введите ссылку на облако', 'danger')
                return redirect('/add_game')
            if not validate_cloud_link(cloud_link):
                flash('Разрешены только Яндекс.Диск, Google Drive или Mail.ru Cloud', 'danger')
                return redirect('/add_game')
        
        game_id = str(uuid.uuid4())[:8]
        
        icon_file = request.files.get('icon')
        icon_filename = None
        if icon_file and icon_file.filename:
            ext = icon_file.filename.rsplit('.', 1)[1].lower()
            icon_filename = f"{game_id}_icon.{ext}"
            icon_path = os.path.join(app.config['GAME_ICONS_FOLDER'], icon_filename)
            icon_file.save(icon_path)
        
        screenshots = request.files.getlist('screenshots')
        screenshot_filenames = []
        for i, ss in enumerate(screenshots[:10]):
            if ss and ss.filename:
                ext = ss.filename.rsplit('.', 1)[1].lower()
                ss_filename = f"{game_id}_ss{i}_{uuid.uuid4().hex[:4]}.{ext}"
                ss_path = os.path.join(app.config['GAME_SCREENSHOTS_FOLDER'], ss_filename)
                ss.save(ss_path)
                screenshot_filenames.append(ss_filename)
        
        game_filename = None
        if download_type == 'file':
            game_file = request.files.get('game_file')
            if game_file and game_file.filename:
                ext = game_file.filename.rsplit('.', 1)[1].lower()
                game_filename = f"{game_id}_game.{ext}"
                game_path = os.path.join(app.config['GAME_FILES_FOLDER'], game_filename)
                game_file.save(game_path)
        
        game = {
            'id': game_id,
            'name': game_name,
            'version': game_version,
            'description': game_description,
            'language': game_language,
            'size': game_size,
            'author': username,
            'icon': icon_filename,
            'screenshots': screenshot_filenames,
            'download_type': download_type,
            'game_file': game_filename,
            'cloud_link': cloud_link if download_type == 'cloud' else None,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'downloads': 0
        }
        
        games = load_games()
        games.append(game)
        save_games(games)
        
        flash(f'Игра "{game_name}" добавлена!', 'success')
        return redirect(f'/game/{game_id}')
    
    content = '''
    <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-plus"></i> Добавить игру</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Название *</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Версия</label>
                <input type="text" name="version" class="form-control" value="1.0">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Описание *</label>
                <textarea name="description" class="form-control" required rows="8"></textarea>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Язык</label>
                <input type="text" name="language" class="form-control" value="Русский">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Размер</label>
                <input type="text" name="size" class="form-control" value="100 MB">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Иконка</label>
                <input type="file" name="icon" class="form-control" accept="image/*">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Скриншоты (до 10)</label>
                <input type="file" name="screenshots" multiple class="form-control" accept="image/*">
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Тип загрузки</label>
                <select name="download_type" id="download_type" class="form-control" onchange="toggleDownloadType()">
                    <option value="file">Файл</option>
                    <option value="cloud">Ссылка на облако</option>
                </select>
            </div>
            
            <div id="file_upload" class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Файл игры</label>
                <input type="file" name="game_file" class="form-control" accept=".zip,.rar,.7z,.exe,.apk">
            </div>
            
            <div id="cloud_link" class="form-group" style="display: none;">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Ссылка на облако</label>
                <input type="url" name="cloud_link" class="form-control" placeholder="https://disk.yandex.ru/...">
                <p class="avatar-hint"><i class="fas fa-info-circle"></i> Только Яндекс, Google, Mail.ru</p>
            </div>
            
            <script>
                function toggleDownloadType() {
                    const type = document.getElementById('download_type').value;
                    document.getElementById('file_upload').style.display = type === 'file' ? 'block' : 'none';
                    document.getElementById('cloud_link').style.display = type === 'cloud' ? 'block' : 'none';
                }
            </script>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-success" style="flex: 1;">
                    <i class="fas fa-save"></i> Добавить
                </button>
                <a href="/games" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Отмена
                </a>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item active">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Добавление игры",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Страница игры
@app.route('/game/<game_id>')
def game_page(game_id):
    if 'user_id' in session and is_banned(session['user_id']):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    games = load_games()
    game = None
    for g in games:
        if g.get('id') == game_id:
            game = g
            break
    
    if not game:
        flash('Игра не найдена', 'danger')
        return redirect('/games')
    
    users = load_users()
    game_achievements = load_game_achievements().get(game_id, [])
    user_achievements = load_user_achievements()
    current_user_achs = user_achievements.get(session.get('user_id', ''), {}).get(game_id, []) if 'user_id' in session else []
    
    game_name = game.get('name', 'Без названия')
    game_icon = game.get('icon', '')
    game_version = game.get('version', '1.0')
    game_author = game.get('author', 'Неизвестен')
    game_description = game.get('description', '')
    game_screenshots = game.get('screenshots', [])
    game_language = game.get('language', 'Русский')
    game_size = game.get('size', '0 MB')
    game_downloads = game.get('downloads', 0)
    download_type = game.get('download_type', 'file')
    game_file = game.get('game_file')
    cloud_link = game.get('cloud_link')
    
    icon_html = f'<img src="/static/games/icons/{game_icon}" class="game-page-icon">' if game_icon else '<div class="game-page-icon" style="background: var(--accent); display: flex; align-items: center; justify-content: center; color: var(--text-primary); font-size: 60px;">G</div>'
    
    screenshots_html = ''
    if game_screenshots:
        screenshots_html = '<div class="screenshots-grid">'
        for ss in game_screenshots:
            screenshots_html += f'<img src="/static/games/screenshots/{ss}" class="screenshot-thumb" onclick="openImageModal(\'/static/games/screenshots/{ss}\')">'
        screenshots_html += '</div>'
    else:
        screenshots_html = '<p class="text-secondary">Нет скриншотов</p>'
    
    achievements_html = ''
    if game_achievements:
        achievements_html = '<div class="achievements-grid">'
        for ach in game_achievements:
            earned = ach.get('id') in current_user_achs
            earned_class = 'earned' if earned else ''
            achievements_html += f'''
            <div class="achievement-card {earned_class}">
                <div class="achievement-icon">{ach.get('icon', '🏆')}</div>
                <div class="achievement-name">{ach.get('name', '')}</div>
                <div class="achievement-desc">{ach.get('description', '')}</div>
            </div>
            '''
        achievements_html += '</div>'
    else:
        achievements_html = '<p class="text-secondary">Нет достижений</p>'
    
    download_buttons = ''
    if download_type == 'file' and game_file:
        file_path = os.path.join(app.config['GAME_FILES_FOLDER'], game_file)
        if os.path.exists(file_path):
            download_buttons = f'<a href="/download_game/{game_id}" class="download-btn"><i class="fas fa-download"></i> Скачать ({game_size})</a>'
    elif download_type == 'cloud' and cloud_link:
        download_buttons = f'<a href="{cloud_link}" target="_blank" class="download-btn cloud-btn"><i class="fas fa-cloud"></i> Скачать с облака</a>'
    
    admin_actions = ''
    if 'user_id' in session:
        current_user = session['user_id']
        if current_user == game_author or is_creator() or is_admin_or_moderator(current_user):
            admin_actions = f'''
            <div style="margin-top: 30px; padding: 20px; background: var(--bg-primary); border-radius: 8px;">
                <h4><i class="fas fa-crown"></i> Управление</h4>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a href="/add_achievement/{game_id}" class="btn btn-primary"><i class="fas fa-plus"></i> Добавить достижение</a>
                    <button onclick="confirmDelete('game', '{game_id}')" class="btn btn-danger"><i class="fas fa-trash"></i> Удалить игру</button>
                </div>
            </div>
            '''
    
    content = f'''
    <div class="game-page">
        <a href="/games" class="btn btn-secondary" style="margin-bottom: 20px;"><i class="fas fa-arrow-left"></i> Назад</a>
        
        <div class="game-page-header">
            {icon_html}
            <div class="game-page-title-section">
                <h1 class="game-page-name">{game_name}</h1>
                <div class="game-page-meta">
                    <span class="game-page-meta-item"><i class="fas fa-tag"></i> v{game_version}</span>
                    <span class="game-page-meta-item"><i class="fas fa-user"></i> {game_author}</span>
                    <span class="game-page-meta-item"><i class="fas fa-globe"></i> {game_language}</span>
                    <span class="game-page-meta-item"><i class="fas fa-database"></i> {game_size}</span>
                    <span class="game-page-meta-item"><i class="fas fa-download"></i> {game_downloads}</span>
                </div>
            </div>
        </div>
        
        <div class="game-page-description">
            {game_description.replace(chr(10), '<br>')}
        </div>
        
        <div class="game-page-screenshots">
            <h3><i class="fas fa-images"></i> Скриншоты</h3>
            {screenshots_html}
        </div>
        
        <div class="game-page-achievements">
            <h3><i class="fas fa-trophy"></i> Достижения</h3>
            {achievements_html}
        </div>
        
        <div class="game-page-download">
            <h3><i class="fas fa-download"></i> Скачать</h3>
            <div class="download-options">
                {download_buttons}
            </div>
        </div>
        
        {admin_actions}
    </div>
    '''
    
    bottom_nav = ''
    if 'user_id' in session:
        username = session['user_id']
        bottom_nav = f'''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item active">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/create_post" class="nav-item">
            <i class="fas fa-plus-square"></i>
            <span>Создать</span>
        </a>
        
        <a href="/inventory" class="nav-item">
            <i class="fas fa-box"></i>
            <span>Инвентарь</span>
        </a>
        
        <a href="/profile/{username}" class="nav-item">
            <i class="fas fa-user"></i>
            <span>Профиль</span>
        </a>
        
        <a href="/logout" class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Выйти</span>
        </a>
        '''
    else:
        bottom_nav = '''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item active">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/login" class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span>Войти</span>
        </a>
        
        <a href="/register" class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span>Регистрация</span>
        </a>
        '''
    
    return render_template_string(BASE_TEMPLATE,
        title=f"{game_name} - GoTeam",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Скачивание игры
@app.route('/download_game/<game_id>')
def download_game(game_id):
    if 'user_id' in session and is_banned(session['user_id']):
        return "Доступ запрещён", 403
    
    games = load_games()
    game = None
    for g in games:
        if g.get('id') == game_id:
            game = g
            break
    
    if not game or game.get('download_type') != 'file' or not game.get('game_file'):
        flash('Файл не найден', 'danger')
        return redirect(f'/game/{game_id}')
    
    filepath = os.path.join(app.config['GAME_FILES_FOLDER'], game['game_file'])
    if not os.path.exists(filepath):
        flash('Файл не найден', 'danger')
        return redirect(f'/game/{game_id}')
    
    game['downloads'] = game.get('downloads', 0) + 1
    save_games(games)
    
    return send_file(
        filepath,
        as_attachment=True,
        download_name=f"{game['name']}_{game['version']}.{game['game_file'].split('.')[-1]}",
        mimetype='application/octet-stream'
    )

# Добавление достижения
@app.route('/add_achievement/<game_id>', methods=['GET', 'POST'])
def add_achievement(game_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    games = load_games()
    game = None
    for g in games:
        if g.get('id') == game_id:
            game = g
            break
    
    if not game:
        flash('Игра не найдена', 'danger')
        return redirect('/games')
    
    if not (username == game.get('author') or is_creator() or is_admin_or_moderator(username)):
        flash('Недостаточно прав', 'danger')
        return redirect(f'/game/{game_id}')
    
    if request.method == 'POST':
        ach_name = request.form.get('name', '').strip()
        ach_desc = request.form.get('description', '').strip()
        ach_icon = request.form.get('icon', '🏆').strip()
        
        if not ach_name or not ach_desc:
            flash('Заполните все поля', 'danger')
            return redirect(f'/add_achievement/{game_id}')
        
        achievements = load_game_achievements()
        if game_id not in achievements:
            achievements[game_id] = []
        
        achievement = {
            'id': str(uuid.uuid4())[:8],
            'name': ach_name,
            'description': ach_desc,
            'icon': ach_icon
        }
        
        achievements[game_id].append(achievement)
        save_game_achievements(achievements)
        
        flash('Достижение добавлено!', 'success')
        return redirect(f'/game/{game_id}')
    
    content = f'''
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-plus"></i> Добавить достижение</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Название</label>
                <input type="text" name="name" class="form-control" required>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Описание</label>
                <textarea name="description" class="form-control" required rows="4"></textarea>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Иконка (эмодзи)</label>
                <input type="text" name="icon" class="form-control" value="🏆">
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-success" style="flex: 1;">
                    <i class="fas fa-save"></i> Добавить
                </button>
                <a href="/game/{game_id}" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Отмена
                </a>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item active">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Добавление достижения",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Выдача достижения
@app.route('/award_achievement/<username>/<game_id>/<achievement_id>')
def award_achievement(username, game_id, achievement_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    current_user = session['user_id']
    
    if is_banned(current_user):
        return jsonify({'success': False, 'error': 'Забанен'}), 403
    
    games = load_games()
    game = None
    for g in games:
        if g.get('id') == game_id:
            game = g
            break
    
    if not game:
        return jsonify({'success': False, 'error': 'Игра не найдена'}), 404
    
    if not (current_user == game.get('author') or is_creator() or is_admin_or_moderator(current_user)):
        return jsonify({'success': False, 'error': 'Недостаточно прав'}), 403
    
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    achievements = load_game_achievements()
    if game_id not in achievements:
        return jsonify({'success': False, 'error': 'Достижения не найдены'}), 404
    
    ach_exists = any(a.get('id') == achievement_id for a in achievements[game_id])
    if not ach_exists:
        return jsonify({'success': False, 'error': 'Достижение не найдено'}), 404
    
    user_achs = load_user_achievements()
    if username not in user_achs:
        user_achs[username] = {}
    if game_id not in user_achs[username]:
        user_achs[username][game_id] = []
    
    if achievement_id not in user_achs[username][game_id]:
        user_achs[username][game_id].append(achievement_id)
        save_user_achievements(user_achs)
    
    return jsonify({'success': True})

# Удаление игры
@app.route('/delete/game/<game_id>')
def delete_game(game_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    current_user = session['user_id']
    
    if is_banned(current_user):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    games = load_games()
    game = None
    for g in games:
        if g.get('id') == game_id:
            game = g
            break
    
    if not game:
        flash('Игра не найдена', 'danger')
        return redirect('/games')
    
    if not (current_user == game.get('author') or is_creator() or is_admin_or_moderator(current_user)):
        flash('Недостаточно прав', 'danger')
        return redirect(f'/game/{game_id}')
    
    if game.get('icon'):
        icon_path = os.path.join(app.config['GAME_ICONS_FOLDER'], game['icon'])
        if os.path.exists(icon_path):
            os.remove(icon_path)
    
    for ss in game.get('screenshots', []):
        ss_path = os.path.join(app.config['GAME_SCREENSHOTS_FOLDER'], ss)
        if os.path.exists(ss_path):
            os.remove(ss_path)
    
    if game.get('game_file'):
        file_path = os.path.join(app.config['GAME_FILES_FOLDER'], game['game_file'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    games = [g for g in games if g.get('id') != game_id]
    save_games(games)
    
    flash('Игра удалена', 'success')
    return redirect('/games')

# Создание поста
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        flash('Войдите в систему', 'danger')
        return redirect('/login')
    
    username = session['user_id']
    
    if is_banned(username):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            flash('Заполните все поля', 'danger')
            return redirect('/create_post')
        
        posts = load_posts()
        post_id = str(uuid.uuid4())[:8]
        
        post = {
            'id': post_id,
            'title': title,
            'content': content,
            'author': username,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'likes': 0,
            'comment_count': 0,
            'attachments': []
        }
        
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    try:
                        filename = f"{uuid.uuid4().hex}_{file.filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        attachment = {
                            'id': str(uuid.uuid4())[:8],
                            'filename': filename,
                            'original_name': file.filename,
                            'size': os.path.getsize(filepath),
                            'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'type': 'image' if is_image(file.filename) else 'file'
                        }
                        post['attachments'].append(attachment)
                    except:
                        pass
        
        posts.append(post)
        save_posts(posts)
        
        users = load_users()
        users[username]['posts_count'] = users[username].get('posts_count', 0) + 1
        users[username]['activity_score'] = users[username].get('activity_score', 0) + 10
        save_users(users)
        
        flash('Пост создан!', 'success')
        return redirect(f'/post/{post_id}')
    
    content = '''
    <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
        <h2><i class="fas fa-plus"></i> Создать пост</h2>
        <div style="height: 2px; background: linear-gradient(90deg, transparent, #4a4a4a, transparent); margin: 20px 0;"></div>
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Заголовок</label>
                <input type="text" name="title" class="form-control" required>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Содержание</label>
                <textarea name="content" class="form-control" required rows="12"></textarea>
            </div>
            
            <div class="form-group">
                <label style="display: block; margin-bottom: 8px; color: var(--text-primary); font-weight: 600;">Файлы</label>
                <input type="file" name="files" multiple class="form-control">
                <p class="avatar-hint"><i class="fas fa-info-circle"></i> Можно прикрепить изображения, документы, видео</p>
            </div>
            
            <div style="display: flex; gap: 10px; margin-top: 20px;">
                <button type="submit" class="btn btn-success" style="flex: 1;">
                    <i class="fas fa-paper-plane"></i> Опубликовать
                </button>
                <a href="/" class="btn btn-secondary">
                    <i class="fas fa-times"></i> Отмена
                </a>
            </div>
        </form>
    </div>
    '''
    
    bottom_nav = f'''
    <a href="/" class="nav-item">
        <i class="fas fa-home"></i>
        <span>Главная</span>
    </a>
    
    <a href="/games" class="nav-item">
        <i class="fas fa-gamepad"></i>
        <span>Игры</span>
    </a>
    
    <a href="/create_post" class="nav-item active">
        <i class="fas fa-plus-square"></i>
        <span>Создать</span>
    </a>
    
    <a href="/inventory" class="nav-item">
        <i class="fas fa-box"></i>
        <span>Инвентарь</span>
    </a>
    
    <a href="/profile/{username}" class="nav-item">
        <i class="fas fa-user"></i>
        <span>Профиль</span>
    </a>
    
    <a href="/logout" class="nav-item">
        <i class="fas fa-sign-out-alt"></i>
        <span>Выйти</span>
    </a>
    '''
    
    return render_template_string(BASE_TEMPLATE,
        title="Создание поста",
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Просмотр поста
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    if 'user_id' in session and is_banned(session['user_id']):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if request.method == 'POST' and 'user_id' in session:
        username = session['user_id']
        comment_text = request.form.get('comment', '').strip()
        
        if comment_text:
            comments = load_comments()
            comment = {
                'id': str(uuid.uuid4())[:8],
                'post_id': post_id,
                'author': username,
                'text': comment_text,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'likes': 0
            }
            comments.append(comment)
            save_comments(comments)
            
            posts = load_posts()
            for post in posts:
                if post.get('id') == post_id:
                    post['comment_count'] = post.get('comment_count', 0) + 1
                    break
            save_posts(posts)
            
            return redirect(f'/post/{post_id}')
    
    posts = load_posts()
    post = None
    for p in posts:
        if p.get('id') == post_id:
            post = p
            break
    
    if not post:
        flash('Пост не найден', 'danger')
        return redirect('/')
    
    comments = load_comments()
    post_comments = [c for c in comments if c.get('post_id') == post_id]
    users = load_users()
    
    author = post.get('author')
    avatar_url = get_user_avatar_url(author)
    
    status = get_user_status(author)
    status_html = ''
    if status:
        if status.get('type') == 'image':
            status_html = f'<div class="status-container" onclick="openImageModal(\'/static/status/{status.get("file")}\')"><img src="/static/status/{status.get("file")}" class="status-image"></div>'
        elif status.get('type') == '3d':
            ext = status.get('file', '').split('.')[-1].lower()
            model_type = 'gltf' if ext in ['gltf', 'glb'] else 'obj'
            status_html = f'<div class="status-3d-icon" onclick="openModelViewer(\'/static/status/{status.get("file")}\', \'{model_type}\')">3D</div>'
    
    role = users.get(author, {}).get('role', 'user')
    
    content = f'''
    <a href="/" class="btn btn-secondary" style="margin-bottom: 20px;"><i class="fas fa-arrow-left"></i> Назад</a>
    
    <div class="post-card">
        <div class="post-header">
            <img src="{avatar_url}" class="user-avatar">
            <div class="post-author-info">
                <div class="post-author-name">
                    {author} {status_html}
                    <span class="badge badge-{role}">{role}</span>
                </div>
                <div class="post-time">{get_time_ago(post.get('created_at'))}</div>
            </div>
        </div>
        <h2 class="post-title">{post.get('title')}</h2>
        <div class="post-content">{post.get('content', '').replace(chr(10), '<br>')}</div>
    </div>
    
    <h3 style="margin: 30px 0 20px 0;"><i class="fas fa-comments"></i> Комментарии ({len(post_comments)})</h3>
    '''
    
    if 'user_id' in session and not is_banned(session['user_id']):
        content += '''
        <div style="margin-bottom: 30px;">
            <form method="POST">
                <div class="form-group">
                    <textarea name="comment" class="form-control" placeholder="Ваш комментарий..." required rows="4"></textarea>
                </div>
                <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> Отправить</button>
            </form>
        </div>
        '''
    elif 'user_id' in session and is_banned(session['user_id']):
        content += '<p class="text-secondary">Вы забанены и не можете писать комментарии</p>'
    else:
        content += '<p class="text-secondary"><a href="/login">Войдите</a> чтобы оставить комментарий</p>'
    
    if post_comments:
        for comment in post_comments:
            comment_author = comment.get('author')
            comment_avatar = get_user_avatar_url(comment_author)
            comment_role = users.get(comment_author, {}).get('role', 'user')
            
            comment_status = get_user_status(comment_author)
            comment_status_html = ''
            if comment_status:
                if comment_status.get('type') == 'image':
                    comment_status_html = f'<div class="status-container" style="width: 20px; height: 20px;" onclick="openImageModal(\'/static/status/{comment_status.get("file")}\')"><img src="/static/status/{comment_status.get("file")}" class="status-image"></div>'
                elif comment_status.get('type') == '3d':
                    comment_status_html = f'<div class="status-3d-icon" style="width: 20px; height: 20px; font-size: 10px;">3D</div>'
            
            content += f'''
            <div class="comment">
                <div class="comment-header">
                    <img src="{comment_avatar}" class="comment-avatar">
                    <div>
                        <div class="comment-author">
                            {comment_author} {comment_status_html}
                            <span class="badge badge-{comment_role}" style="font-size: 10px;">{comment_role}</span>
                        </div>
                        <div class="comment-time">{get_time_ago(comment.get('created_at'))}</div>
                    </div>
                </div>
                <div>{comment.get('text', '').replace(chr(10), '<br>')}</div>
            </div>
            '''
    else:
        content += '<div class="empty-state"><i class="fas fa-comment-slash"></i><p>Пока нет комментариев</p></div>'
    
    bottom_nav = ''
    if 'user_id' in session:
        username = session['user_id']
        bottom_nav = f'''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/create_post" class="nav-item">
            <i class="fas fa-plus-square"></i>
            <span>Создать</span>
        </a>
        
        <a href="/inventory" class="nav-item">
            <i class="fas fa-box"></i>
            <span>Инвентарь</span>
        </a>
        
        <a href="/profile/{username}" class="nav-item">
            <i class="fas fa-user"></i>
            <span>Профиль</span>
        </a>
        
        <a href="/logout" class="nav-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Выйти</span>
        </a>
        '''
    else:
        bottom_nav = '''
        <a href="/" class="nav-item">
            <i class="fas fa-home"></i>
            <span>Главная</span>
        </a>
        
        <a href="/games" class="nav-item">
            <i class="fas fa-gamepad"></i>
            <span>Игры</span>
        </a>
        
        <a href="/login" class="nav-item">
            <i class="fas fa-sign-in-alt"></i>
            <span>Войти</span>
        </a>
        
        <a href="/register" class="nav-item">
            <i class="fas fa-user-plus"></i>
            <span>Регистрация</span>
        </a>
        '''
    
    return render_template_string(BASE_TEMPLATE,
        title=post.get('title'),
        content=content,
        bottom_nav=bottom_nav,
        goteam_icon=GOTEAM_ICON_BASE64
    )

# Лайк поста
@app.route('/like_post/<post_id>', methods=['POST'])
def like_post(post_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Не авторизован'}), 401
    
    username = session['user_id']
    
    if is_banned(username):
        return jsonify({'success': False, 'error': 'Забанен'}), 403
    
    posts = load_posts()
    post = None
    for p in posts:
        if p.get('id') == post_id:
            post = p
            break
    
    if not post:
        return jsonify({'success': False, 'error': 'Пост не найден'}), 404
    
    can_like, error = can_like_post(username, post_id, post.get('author'))
    if not can_like:
        return jsonify({'success': False, 'error': error}), 400
    
    likes_count = add_like(username, post_id)
    
    return jsonify({'success': True, 'likes': likes_count, 'liked': True})

# Удаление
@app.route('/delete/<type>/<id>')
def delete_item(type, id):
    if 'user_id' not in session:
        return redirect('/login')
    
    current_user = session['user_id']
    
    if is_banned(current_user):
        session.clear()
        flash('Вы забанены', 'danger')
        return redirect('/login')
    
    if type == 'game':
        return delete_game(id)
    
    if type == 'post':
        posts = load_posts()
        new_posts = []
        for post in posts:
            if post.get('id') != id:
                new_posts.append(post)
        save_posts(new_posts)
        flash('Пост удален', 'success')
    
    return redirect('/')

# Скачивание файла из поста
@app.route('/download/<post_id>/<attachment_id>')
def download_attachment(post_id, attachment_id):
    posts = load_posts()
    for post in posts:
        if post.get('id') == post_id:
            for att in post.get('attachments', []):
                if att.get('id') == attachment_id:
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], att['filename'])
                    if os.path.exists(filepath):
                        return send_file(filepath, as_attachment=True, download_name=att['original_name'])
    return "Файл не найден", 404

# Статические файлы
@app.route('/static/uploads/<filename>')
def serve_uploaded_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return "Файл не найден", 404

# Заглушки для остальных маршрутов
@app.route('/change_role/<username>/<new_role>')
def change_role(username, new_role):
    return jsonify({'success': False, 'error': 'В разработке'})

@app.route('/ban_user/<username>/<int:days>')
def ban_user(username, days):
    return jsonify({'success': False, 'error': 'В разработке'})

@app.route('/unban_user/<username>')
def unban_user(username):
    return jsonify({'success': False, 'error': 'В разработке'})

if __name__ == '__main__':
    create_default_admins()
    
    print("=" * 70)
    print("🎮 GoTeam - ЧЕРНО-БЕЛАЯ ТЕМА")
    print("=" * 70)
    print("✅ ИСПРАВЛЕНО:")
    print("   • Редактирование профиля с аватаром")
    print("   • Достижения с иконками")
    print("   • Черно-белая тема оформления")
    print("=" * 70)
    print("✅ РАБОТАЮТ ВСЕ СТРАНИЦЫ:")
    print("   • / - Главная")
    print("   • /register - Регистрация")
    print("   • /login - Вход")
    print("   • /profile/username - Профиль")
    print("   • /edit_profile - Редактирование")
    print("   • /inventory - Инвентарь")
    print("   • /statuses - Статусы")
    print("   • /games - Игры")
    print("   • /game/id - Страница игры")
    print("   • /create_post - Создание поста")
    print("   • /post/id - Просмотр поста")
    print("=" * 70)
    print("👑 Админ: admin / admin123")
    print("👮 Модератор: moderator / admin123")
    print("=" * 70)
    print("Сервер запущен: http://127.0.0.1:5000")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)