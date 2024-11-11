import uuid
import bcrypt
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, redirect, url_for
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
import jwt
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for CSRF and JWT
app.config['WTF_CSRF_ENABLED'] = True  # 启用CSRF保护

# CSRF保护配置
csrf = CSRFProtect(app)

# 邮件配置（根据实际情况调整）
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your-email@example.com',
    MAIL_PASSWORD='your-email-password'
)
mail = Mail(app)

# JWT配置
JWT_SECRET = 'jwtsecretkey'
JWT_EXPIRATION_DELTA = timedelta(minutes=15)

# Limiter 设置（速率限制器）
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# CORS配置
CORS(app, resources={r"/api/*": {"origins": "https://trusted-client.com"}})

# HTTPS 配置（强制HTTPS）
@app.before_request
def before_request():
    if not request.is_secure:
        return redirect(url_for(request.endpoint, _scheme='https', _external=True))

# 用于将代理转发到正确的协议（适用于生产环境）
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        is_active BOOLEAN NOT NULL DEFAULT 1,
                        email TEXT NOT NULL UNIQUE,
                        mfa_code TEXT,
                        login_attempts INTEGER DEFAULT 0,
                        last_attempt_time TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_logs (
                        log_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        action TEXT,
                        ip TEXT,
                        user_agent TEXT,
                        timestamp TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                    )''')
    conn.commit()
    conn.close()

# 注册新用户，密码使用bcrypt加密
@app.route('/api/register', methods=['POST'])
@csrf.exempt  # 这里可以通过API Token机制或CORS限制控制
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    role = data.get('role', 'user')
    
    # bcrypt加密密码
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, password, role, email) VALUES (?, ?, ?, ?, ?)",
                       (uuid.uuid4().hex, username, hashed_password, role, email))
        conn.commit()
        return jsonify({"message": f"User '{username}' registered successfully."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists."}), 400
    finally:
        conn.close()

# 登录并进行二次验证
@app.route('/api/login', methods=['POST'])
@csrf.exempt  # 登录请求不需要CSRF，但可以考虑进一步的安全策略
@limiter.limit("10 per minute")  # 设置登录接口速率限制
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password, role, is_active, email, login_attempts, last_attempt_time FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        user_id, stored_password, role, is_active, email, login_attempts, last_attempt_time = user
        
        # 账户锁定检查
        if login_attempts >= 5 and datetime.now() - datetime.fromisoformat(last_attempt_time) < timedelta(minutes=5):
            return jsonify({"error": "Account is temporarily locked due to multiple failed login attempts."}), 403
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            if not is_active:
                return jsonify({"error": "Account is disabled."}), 403

            cursor.execute("UPDATE users SET login_attempts = 0 WHERE user_id = ?", (user_id,))
            conn.commit()

            # 生成并发送验证码
            mfa_code = str(uuid.uuid4().int)[:6]
            cursor.execute("UPDATE users SET mfa_code = ? WHERE user_id = ?", (mfa_code, user_id))
            conn.commit()
            send_mfa_code(email, mfa_code)
            conn.close()
            return jsonify({"message": "Verification code sent to your email."}), 200
        else:
            cursor.execute("UPDATE users SET login_attempts = login_attempts + 1, last_attempt_time = ? WHERE user_id = ?", (datetime.now().isoformat(), user_id))
            conn.commit()
            return jsonify({"error": "Invalid password."}), 401
    else:
        return jsonify({"error": "User does not exist."}), 404

# 发送验证码邮件
def send_mfa_code(email, code):
    msg = Message(subject="Your Verification Code",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email])
    msg.body = f"Your verification code is: {code}"
    mail.send(msg)

# 验证二次验证代码并生成 JWT
@app.route('/api/verify_mfa', methods=['POST'])
@csrf.exempt
def verify_mfa():
    data = request.json
    username = data['username']
    mfa_code = data['mfa_code']
    
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, role, mfa_code FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_id, role, stored_mfa_code = user
        if mfa_code == stored_mfa_code:
            conn = sqlite3.connect('accounts.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET mfa_code = NULL WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            
            token = jwt.encode({
                'user_id': user_id,
                'role': role,
                'exp': datetime.utcnow() + JWT_EXPIRATION_DELTA
            }, JWT_SECRET, algorithm='HS256')
            
            log_user_action(user_id, 'login')
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid MFA code."}), 401
    else:
        return jsonify({"error": "User does not exist."}), 404

# 日志记录
def log_user_action(user_id, action):
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_logs (log_id, user_id, action, ip, user_agent, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                   (uuid.uuid4().hex, user_id, action, ip, user_agent, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# 权限装饰器
def requires_role(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"error": "Unauthorized access. Token missing."}), 401
            try:
                decoded_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                if decoded_token['role'] != role:
                    return jsonify({"error": f"Access denied. '{role}' role required."}), 403
                request.user_id = decoded_token['user_id']
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token."}), 401
        return decorated_function
    return wrapper

# 管理员操作
@app.route('/api/admin_action', methods=['POST'])
@requires_role('admin')
@csrf.exempt  # 在需要时考虑如何更好地处理API端点的CSRF
@cross_origin(origins=["https://trusted-client.com"])  # CORS 限制
def admin_action():
    log_user_action(request.user_id, 'admin_action')
    return jsonify({"message": "Admin action performed successfully."}), 200

# 初始化数据库
init_db()

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)  # 使用HTTPS
