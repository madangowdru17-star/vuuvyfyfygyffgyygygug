from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from flask_cors import CORS
import json
import os
import hashlib
import secrets
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
CORS(app)

CONFIG_FILE = 'config.json'
ADMIN_CREDENTIALS_FILE = 'admin_credentials.json'

DEFAULT_CONFIG = {
    "maintenance": False,
    "freefire_maintenance": False,
    "freefire_max_maintenance": False,
    "master_key": "HEXPROXY999",
    "master_key_expiry": "2026-12-31T23:59:59.000000",
    "login_name": "HEX PROXY XOS V6",
    "app_name": "HEX PROXY XOS V6",
    "maintenance_message": "We are performing scheduled maintenance. Please join our Telegram for updates.",
    "telegram_link": "https://t.me/+_s4OBzblpi0zNzE1",
    "get_key_link": "https://t.me/+_s4OBzblpi0zNzE1",
    "logo_url": "https://i.ibb.co/Wpcb6Ydy/IMG-20260313-030403-360.jpg",
    "shizuku_logo_url": "https://i.ibb.co/JRjy2ZpC/20260808-044938.png",
    "freefire_logo_url": "https://i.ibb.co/nsqT2bjJ/Garena-Free-Fire-Icon.jpg",
    "freefire_max_logo_url": "https://i.ibb.co/Wv5pthbL/unnamed.webp",
    "api_base_url": "https://key-system-production-1bc5.up.railway.app",
    "update_available": False,
    "update_version": "2.1.0",
    "update_changelog": "- Fixed AimBot\n- Added new features\n- Performance improvements",
    "update_url": "https://github.com/madangowdru17-star/Apk/raw/refs/heads/main/generated_sign.apk",
    "assets_version": "9.9",
    "assets": [
        {
            "name": "bg.mp4",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/bg.mp4"
        }
    ],
    "freefire_buttons": [
        {
            "id": "ff_drag",
            "name": "Chest HS 95%-Sensi",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "ff_antenna",
            "name": "DRAG HS + ANITENA SPEED 2x",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/DARG-HS-1000/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": True
        },
        {
            "id": "ff_headshot",
            "name": "HEADSHOT 99%",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_aimbot",
            "name": "AIMBOT PRO",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_wallhack",
            "name": "WALLHACK XRAY",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        },
        {
            "id": "ff_esp",
            "name": "ESP PLAYER",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/Assistant/refs/heads/main/localconfig.json",
            "enabled": False,
            "maintenance": False
        }
    ],
    "freefire_max_buttons": [
        {
            "id": "max_drag_safe",
            "name": "DRAG HS 85% SAFE",
            "url": "https://raw.githubusercontent.com/madangowdru17-star/HS-ANTENA/refs/heads/main/localconfig.json",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_nick",
            "name": "NICK HS 95%",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_body",
            "name": "BODY HS 99%",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_aimbot",
            "name": "AIMBOT MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_wallhack",
            "name": "WALLHACK MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "max_esp",
            "name": "ESP MAX",
            "url": "",
            "enabled": True,
            "maintenance": False
        }
    ],
    "root_libs": [
        {
            "id": "root_max64",
            "name": "FF MAX 64-BIT",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libcrashlytics_arm64.so",
            "lib_path": "lib/arm64-v8a/libcrashlytics.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_max32",
            "name": "FF MAX 32-BIT",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libcrashlytics_arm.so",
            "lib_path": "lib/armeabi-v7a/libcrashlytics.so",
            "arch": "arm",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_aimbot",
            "name": "AIMBOT MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libaimbot.so",
            "lib_path": "lib/arm64-v8a/libaimbot.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_esp",
            "name": "ESP MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libesp.so",
            "lib_path": "lib/arm64-v8a/libesp.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_headshot",
            "name": "HEADSHOT MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libheadshot.so",
            "lib_path": "lib/arm64-v8a/libheadshot.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        },
        {
            "id": "root_wallhack",
            "name": "WALLHACK MODULE",
            "url": "https://github.com/madangowdru17-star/Assistant/raw/refs/heads/main/libwallhack.so",
            "lib_path": "lib/arm64-v8a/libwallhack.so",
            "arch": "arm64",
            "enabled": True,
            "maintenance": False
        }
    ]
}

def load_admin_credentials():
    if os.path.exists(ADMIN_CREDENTIALS_FILE):
        with open(ADMIN_CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return {"admins": []}

def save_admin_credentials(credentials):
    with open(ADMIN_CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin(username, password):
    credentials = load_admin_credentials()
    for admin in credentials['admins']:
        if admin['username'] == username:
            return False
    
    hashed_pw = hash_password(password)
    credentials['admins'].append({
        'username': username,
        'password': hashed_pw,
        'created_at': datetime.now().isoformat()
    })
    save_admin_credentials(credentials)
    return True

def verify_admin(username, password):
    credentials = load_admin_credentials()
    hashed_pw = hash_password(password)
    for admin in credentials['admins']:
        if admin['username'] == username and admin['password'] == hashed_pw:
            return True
    return False

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/config', methods=['GET'])
def get_config():
    config = load_config()
    return jsonify(config)

@app.route('/api/config/update', methods=['POST'])
@login_required
def update_config():
    try:
        data = request.json
        config = load_config()
        for key, value in data.items():
            if key in config:
                config[key] = value
        save_config(config)
        return jsonify({"success": True, "message": "Configuration updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/button/update/<button_type>/<button_id>', methods=['POST'])
@login_required
def update_button(button_type, button_id):
    try:
        data = request.json
        config = load_config()
        
        if button_type == 'freefire':
            buttons = config.get('freefire_buttons', [])
        elif button_type == 'freefire_max':
            buttons = config.get('freefire_max_buttons', [])
        elif button_type == 'root_libs':
            buttons = config.get('root_libs', [])
        else:
            return jsonify({"success": False, "message": "Invalid button type"}), 400
        
        for button in buttons:
            if button.get('id') == button_id:
                for key, value in data.items():
                    if key in button:
                        button[key] = value
                
                if button_type == 'freefire':
                    config['freefire_buttons'] = buttons
                elif button_type == 'freefire_max':
                    config['freefire_max_buttons'] = buttons
                elif button_type == 'root_libs':
                    config['root_libs'] = buttons
                
                save_config(config)
                return jsonify({"success": True, "message": "Button updated successfully"})
        
        return jsonify({"success": False, "message": "Button not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/button/toggle/<button_type>/<button_id>', methods=['POST'])
@login_required
def toggle_button(button_type, button_id):
    try:
        data = request.json
        enabled = data.get('enabled', False)
        maintenance = data.get('maintenance', False)
        
        config = load_config()
        
        if button_type == 'freefire':
            buttons = config.get('freefire_buttons', [])
        elif button_type == 'freefire_max':
            buttons = config.get('freefire_max_buttons', [])
        elif button_type == 'root_libs':
            buttons = config.get('root_libs', [])
        else:
            return jsonify({"success": False, "message": "Invalid button type"}), 400
        
        for button in buttons:
            if button.get('id') == button_id:
                button['enabled'] = enabled
                button['maintenance'] = maintenance
                
                if button_type == 'freefire':
                    config['freefire_buttons'] = buttons
                elif button_type == 'freefire_max':
                    config['freefire_max_buttons'] = buttons
                elif button_type == 'root_libs':
                    config['root_libs'] = buttons
                
                save_config(config)
                return jsonify({"success": True, "message": "Button toggled successfully"})
        
        return jsonify({"success": False, "message": "Button not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/maintenance/toggle', methods=['POST'])
@login_required
def toggle_maintenance():
    try:
        data = request.json
        config = load_config()
        
        if 'maintenance' in data:
            config['maintenance'] = data['maintenance']
        if 'freefire_maintenance' in data:
            config['freefire_maintenance'] = data['freefire_maintenance']
        if 'freefire_max_maintenance' in data:
            config['freefire_max_maintenance'] = data['freefire_max_maintenance']
        
        save_config(config)
        return jsonify({"success": True, "message": "Maintenance status updated"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/asset/update', methods=['POST'])
@login_required
def update_asset():
    try:
        data = request.json
        asset_name = data.get('name')
        asset_url = data.get('url')
        
        if not asset_name or not asset_url:
            return jsonify({"success": False, "message": "Missing asset name or URL"}), 400
        
        config = load_config()
        assets = config.get('assets', [])
        
        for asset in assets:
            if asset.get('name') == asset_name:
                asset['url'] = asset_url
                config['assets'] = assets
                save_config(config)
                return jsonify({"success": True, "message": "Asset updated successfully"})
        
        assets.append({"name": asset_name, "url": asset_url})
        config['assets'] = assets
        save_config(config)
        return jsonify({"success": True, "message": "Asset added successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/update/app', methods=['POST'])
@login_required
def update_app_info():
    try:
        data = request.json
        config = load_config()
        
        if 'update_available' in data:
            config['update_available'] = data['update_available']
        if 'update_version' in data:
            config['update_version'] = data['update_version']
        if 'update_changelog' in data:
            config['update_changelog'] = data['update_changelog']
        if 'update_url' in data:
            config['update_url'] = data['update_url']
        
        save_config(config)
        return jsonify({"success": True, "message": "App info updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if verify_admin(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error='Invalid credentials')
    
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route('/dashboard')
@login_required
def dashboard():
    config = load_config()
    username = session.get('username', 'Admin')
    return render_template_string(DASHBOARD_TEMPLATE, config=config, username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def init_admin():
    credentials = load_admin_credentials()
    if not credentials['admins']:
        create_admin('admin', 'admin123')
        print("Default admin created: username='admin', password='admin123'")

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .login-container {
            background: white;
            padding: 3rem 2.5rem;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 420px;
            transition: transform 0.3s ease;
        }
        .login-container:hover {
            transform: translateY(-5px);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            font-size: 2rem;
            color: #2d3748;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        .login-header p {
            color: #718096;
            margin-top: 0.5rem;
            font-size: 0.95rem;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #2d3748;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .form-group input {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #f7fafc;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .login-btn {
            width: 100%;
            padding: 0.875rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .login-btn:active {
            transform: translateY(0);
        }
        .error-message {
            background: #fed7d7;
            color: #c53030;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-weight: 500;
            border-left: 4px solid #fc8181;
        }
        .login-footer {
            margin-top: 1.5rem;
            text-align: center;
            color: #a0aec0;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>Admin Panel</h1>
            <p>Secure access to configuration management</p>
        </div>
        {% if error %}
        <div class="error-message">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Enter username" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="login-btn">Sign In</button>
        </form>
        <div class="login-footer">
            <p>Secure Administration Interface</p>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Admin Panel</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }
        body {
            background: #f7fafc;
            padding: 20px;
        }
        .container {
            max-width: 1440px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            color: #2d3748;
            font-size: 1.75rem;
            font-weight: 700;
        }
        .header-user {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .header-user span {
            color: #4a5568;
            font-weight: 500;
        }
        .logout-btn {
            padding: 0.5rem 1.25rem;
            background: #fc8181;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .logout-btn:hover {
            background: #f56565;
            transform: translateY(-1px);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            color: #718096;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        .stat-card .value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #2d3748;
        }
        .section {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
        }
        .section h2 {
            color: #2d3748;
            font-size: 1.25rem;
            margin-bottom: 1.25rem;
            font-weight: 600;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }
        .button-card {
            background: #f7fafc;
            padding: 1rem 1.25rem;
            border-radius: 10px;
            border-left: 4px solid #48bb78;
            transition: all 0.3s ease;
        }
        .button-card:hover {
            background: #edf2f7;
            transform: translateX(4px);
        }
        .button-card .name {
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.25rem;
        }
        .button-card .id {
            font-size: 0.8rem;
            color: #a0aec0;
            margin-bottom: 0.5rem;
            font-family: monospace;
        }
        .button-card .status {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }
        .badge {
            padding: 0.2rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
        .badge-success {
            background: #c6f6d5;
            color: #22543d;
        }
        .badge-danger {
            background: #fed7d7;
            color: #742a2a;
        }
        .badge-warning {
            background: #fefcbf;
            color: #744210;
        }
        .badge-info {
            background: #bee3f8;
            color: #2a4365;
        }
        .control-group {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        .toggle-btn {
            padding: 0.3rem 0.75rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .toggle-btn.enable {
            background: #48bb78;
            color: white;
        }
        .toggle-btn.enable:hover {
            background: #38a169;
        }
        .toggle-btn.disable {
            background: #fc8181;
            color: white;
        }
        .toggle-btn.disable:hover {
            background: #f56565;
        }
        .maintenance-toggle {
            background: #edf2f7;
            border: 2px solid #e2e8f0;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            color: #2d3748;
        }
        .maintenance-toggle:hover {
            background: #e2e8f0;
            border-color: #cbd5e0;
        }
        .config-input {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            margin-top: 0.5rem;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            background: #f7fafc;
        }
        .config-input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .save-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 0.5rem;
            transition: all 0.3s ease;
        }
        .save-btn:hover {
            background: #5a67d8;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        .json-view {
            background: #2d3748;
            padding: 1.25rem;
            border-radius: 8px;
            overflow: auto;
            max-height: 500px;
            font-size: 0.8rem;
            color: #f7fafc;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
        }
        .refresh-btn {
            background: #48bb78;
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        .refresh-btn:hover {
            background: #38a169;
            transform: translateY(-1px);
        }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }
        .status-dot.online {
            background: #48bb78;
        }
        .status-dot.maintenance {
            background: #fc8181;
        }
        .status-dot.active {
            background: #48bb78;
        }
        .status-dot.inactive {
            background: #a0aec0;
        }
        .flex-row {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 1rem;
                align-items: stretch;
            }
            .header-user {
                justify-content: space-between;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Administration Dashboard</h1>
            <div class="header-user">
                <span>Welcome, {{ username }}</span>
                <a href="/logout" class="logout-btn">Sign Out</a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>FreeFire Buttons</h3>
                <div class="value">{{ config.freefire_buttons|length }}</div>
            </div>
            <div class="stat-card">
                <h3>FreeFire Max Buttons</h3>
                <div class="value">{{ config.freefire_max_buttons|length }}</div>
            </div>
            <div class="stat-card">
                <h3>Root Libraries</h3>
                <div class="value">{{ config.root_libs|length }}</div>
            </div>
            <div class="stat-card">
                <h3>Assets</h3>
                <div class="value">{{ config.assets|length }}</div>
            </div>
        </div>

        <div class="section">
            <h2>Maintenance Controls</h2>
            <div class="flex-row">
                <button class="maintenance-toggle" onclick="toggleMaintenance('maintenance', {{ config.maintenance|lower }})">
                    <span class="status-dot {{ 'online' if not config.maintenance else 'maintenance' }}"></span>
                    Application: {{ 'Online' if not config.maintenance else 'Maintenance' }}
                </button>
                <button class="maintenance-toggle" onclick="toggleMaintenance('freefire_maintenance', {{ config.freefire_maintenance|lower }})">
                    <span class="status-dot {{ 'online' if not config.freefire_maintenance else 'maintenance' }}"></span>
                    FreeFire: {{ 'Online' if not config.freefire_maintenance else 'Maintenance' }}
                </button>
                <button class="maintenance-toggle" onclick="toggleMaintenance('freefire_max_maintenance', {{ config.freefire_max_maintenance|lower }})">
                    <span class="status-dot {{ 'online' if not config.freefire_max_maintenance else 'maintenance' }}"></span>
                    FreeFire Max: {{ 'Online' if not config.freefire_max_maintenance else 'Maintenance' }}
                </button>
            </div>
        </div>

        <div class="section">
            <h2>FreeFire Buttons</h2>
            <div class="button-grid">
                {% for button in config.freefire_buttons %}
                <div class="button-card">
                    <div class="name">{{ button.name }}</div>
                    <div class="id">{{ button.id }}</div>
                    <div class="status">
                        <span class="badge {{ 'badge-success' if button.enabled else 'badge-danger' }}">
                            <span class="status-dot {{ 'active' if button.enabled else 'inactive' }}"></span>
                            {{ 'Enabled' if button.enabled else 'Disabled' }}
                        </span>
                        <span class="badge {{ 'badge-warning' if button.maintenance else 'badge-info' }}">
                            <span class="status-dot {{ 'maintenance' if button.maintenance else 'active' }}"></span>
                            {{ 'Maintenance' if button.maintenance else 'Active' }}
                        </span>
                    </div>
                    <div class="control-group">
                        <button class="toggle-btn {{ 'enable' if not button.enabled else 'disable' }}" 
                                onclick="toggleButton('freefire', '{{ button.id }}', {{ not button.enabled|lower }}, {{ button.maintenance|lower }})">
                            {{ 'Enable' if not button.enabled else 'Disable' }}
                        </button>
                        <button class="toggle-btn {{ 'enable' if button.maintenance else 'disable' }}"
                                onclick="toggleMaintenanceButton('freefire', '{{ button.id }}', {{ not button.maintenance|lower }}, {{ button.enabled|lower }})">
                            {{ 'Set Active' if button.maintenance else 'Set Maintenance' }}
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section">
            <h2>FreeFire Max Buttons</h2>
            <div class="button-grid">
                {% for button in config.freefire_max_buttons %}
                <div class="button-card">
                    <div class="name">{{ button.name }}</div>
                    <div class="id">{{ button.id }}</div>
                    <div class="status">
                        <span class="badge {{ 'badge-success' if button.enabled else 'badge-danger' }}">
                            <span class="status-dot {{ 'active' if button.enabled else 'inactive' }}"></span>
                            {{ 'Enabled' if button.enabled else 'Disabled' }}
                        </span>
                        <span class="badge {{ 'badge-warning' if button.maintenance else 'badge-info' }}">
                            <span class="status-dot {{ 'maintenance' if button.maintenance else 'active' }}"></span>
                            {{ 'Maintenance' if button.maintenance else 'Active' }}
                        </span>
                    </div>
                    <div class="control-group">
                        <button class="toggle-btn {{ 'enable' if not button.enabled else 'disable' }}" 
                                onclick="toggleButton('freefire_max', '{{ button.id }}', {{ not button.enabled|lower }}, {{ button.maintenance|lower }})">
                            {{ 'Enable' if not button.enabled else 'Disable' }}
                        </button>
                        <button class="toggle-btn {{ 'enable' if button.maintenance else 'disable' }}"
                                onclick="toggleMaintenanceButton('freefire_max', '{{ button.id }}', {{ not button.maintenance|lower }}, {{ button.enabled|lower }})">
                            {{ 'Set Active' if button.maintenance else 'Set Maintenance' }}
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section">
            <h2>Root Libraries</h2>
            <div class="button-grid">
                {% for lib in config.root_libs %}
                <div class="button-card">
                    <div class="name">{{ lib.name }}</div>
                    <div class="id">{{ lib.id }}</div>
                    <div class="status">
                        <span class="badge {{ 'badge-success' if lib.enabled else 'badge-danger' }}">
                            <span class="status-dot {{ 'active' if lib.enabled else 'inactive' }}"></span>
                            {{ 'Enabled' if lib.enabled else 'Disabled' }}
                        </span>
                        <span class="badge {{ 'badge-warning' if lib.maintenance else 'badge-info' }}">
                            <span class="status-dot {{ 'maintenance' if lib.maintenance else 'active' }}"></span>
                            {{ 'Maintenance' if lib.maintenance else 'Active' }}
                        </span>
                    </div>
                    <div class="control-group">
                        <button class="toggle-btn {{ 'enable' if not lib.enabled else 'disable' }}" 
                                onclick="toggleButton('root_libs', '{{ lib.id }}', {{ not lib.enabled|lower }}, {{ lib.maintenance|lower }})">
                            {{ 'Enable' if not lib.enabled else 'Disable' }}
                        </button>
                        <button class="toggle-btn {{ 'enable' if lib.maintenance else 'disable' }}"
                                onclick="toggleMaintenanceButton('root_libs', '{{ lib.id }}', {{ not lib.maintenance|lower }}, {{ lib.enabled|lower }})">
                            {{ 'Set Active' if lib.maintenance else 'Set Maintenance' }}
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="section">
            <h2>Application Update Controls</h2>
            <div class="flex-row" style="margin-bottom: 1rem;">
                <button class="maintenance-toggle" onclick="toggleUpdate()">
                    <span class="status-dot {{ 'online' if config.update_available else 'inactive' }}"></span>
                    Update: {{ 'Available' if config.update_available else 'Not Available' }}
                </button>
            </div>
            <input class="config-input" id="update_version" placeholder="Update Version (e.g. 2.1.0)" value="{{ config.update_version }}">
            <input class="config-input" id="update_url" placeholder="Update URL" value="{{ config.update_url }}">
            <textarea class="config-input" id="update_changelog" rows="3" placeholder="Update Changelog">{{ config.update_changelog }}</textarea>
            <button class="save-btn" onclick="saveUpdateInfo()">Save Update Information</button>
        </div>

        <div class="section">
            <h2>Configuration Viewer</h2>
            <button class="refresh-btn" onclick="refreshConfig()">Refresh Configuration</button>
            <div class="json-view" id="configView">{{ config|tojson|safe }}</div>
        </div>
    </div>

    <script>
        async function toggleButton(type, id, enabled, maintenance) {
            try {
                const response = await fetch(`/api/button/toggle/${type}/${id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({enabled: enabled, maintenance: maintenance})
                });
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function toggleMaintenanceButton(type, id, maintenance, enabled) {
            try {
                const response = await fetch(`/api/button/toggle/${type}/${id}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({enabled: enabled, maintenance: maintenance})
                });
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function toggleMaintenance(type, current) {
            try {
                const response = await fetch('/api/maintenance/toggle', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({[type]: !current})
                });
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function toggleUpdate() {
            try {
                const current = {{ config.update_available|lower }};
                const response = await fetch('/api/update/app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({update_available: !current})
                });
                const data = await response.json();
                if (data.success) {
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function saveUpdateInfo() {
            const version = document.getElementById('update_version').value;
            const url = document.getElementById('update_url').value;
            const changelog = document.getElementById('update_changelog').value;
            
            try {
                const response = await fetch('/api/update/app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        update_version: version,
                        update_url: url,
                        update_changelog: changelog
                    })
                });
                const data = await response.json();
                if (data.success) {
                    alert('Update information saved successfully!');
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        async function refreshConfig() {
            try {
                const response = await fetch('/api/config');
                const data = await response.json();
                document.getElementById('configView').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        setInterval(refreshConfig, 30000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    init_admin()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
