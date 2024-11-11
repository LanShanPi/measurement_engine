import tkinter as tk
from tkinter import messagebox
import requests

# 配置API基本地址和默认的headers
API_BASE = "https://localhost:5000/api"  # 替换为你的服务器地址
headers = {"Content-Type": "application/json"}
jwt_token = ""

# 初始化主窗口
root = tk.Tk()
root.title("Account System Test Interface")
root.geometry("400x600")

# 显示消息
def show_message(msg):
    messagebox.showinfo("Information", msg)

# 注册功能
def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    email = register_email_entry.get()
    
    payload = {"username": username, "password": password, "email": email}
    
    try:
        response = requests.post(f"{API_BASE}/register", json=payload, headers=headers, verify=False)
        data = response.json()
        show_message(data.get("message", data.get("error", "Unknown Error")))
    except requests.RequestException as e:
        show_message(f"Request failed: {e}")

# 登录功能
def login():
    global username
    username = login_username_entry.get()
    password = login_password_entry.get()
    
    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(f"{API_BASE}/login", json=payload, headers=headers, verify=False)
        data = response.json()
        
        if data.get("message") == "Verification code sent to your email.":
            show_message("Login successful, verification code sent to your email.")
            mfa_frame.pack(pady=10)  # 显示二次验证框
        else:
            show_message(data.get("error", "Unknown Error"))
    except requests.RequestException as e:
        show_message(f"Request failed: {e}")

# 二次验证功能
def verify_mfa():
    global jwt_token
    mfa_code = mfa_code_entry.get()
    
    payload = {"username": username, "mfa_code": mfa_code}
    
    try:
        response = requests.post(f"{API_BASE}/verify_mfa", json=payload, headers=headers, verify=False)
        data = response.json()
        
        if "token" in data:
            jwt_token = data["token"]
            show_message("Verification successful! You are now authenticated.")
            mfa_frame.pack_forget()  # 隐藏二次验证框
            auth_action_frame.pack(pady=10)  # 显示管理员操作框
        else:
            show_message(data.get("error", "Unknown Error"))
    except requests.RequestException as e:
        show_message(f"Request failed: {e}")

# 管理员操作功能
def admin_action():
    try:
        auth_headers = headers.copy()
        auth_headers["Authorization"] = jwt_token
        
        response = requests.post(f"{API_BASE}/admin_action", headers=auth_headers, verify=False)
        data = response.json()
        
        show_message(data.get("message", data.get("error", "Unknown Error")))
    except requests.RequestException as e:
        show_message(f"Request failed: {e}")

# 注册框
register_frame = tk.LabelFrame(root, text="Register", padx=10, pady=10)
register_frame.pack(pady=10)

register_username_entry = tk.Entry(register_frame, width=30)
register_username_entry.insert(0, "Username")
register_username_entry.pack(pady=5)

register_password_entry = tk.Entry(register_frame, show="*", width=30)
register_password_entry.insert(0, "Password")
register_password_entry.pack(pady=5)

register_email_entry = tk.Entry(register_frame, width=30)
register_email_entry.insert(0, "Email")
register_email_entry.pack(pady=5)

register_button = tk.Button(register_frame, text="Register", command=register)
register_button.pack(pady=5)

# 登录框
login_frame = tk.LabelFrame(root, text="Login", padx=10, pady=10)
login_frame.pack(pady=10)

login_username_entry = tk.Entry(login_frame, width=30)
login_username_entry.insert(0, "Username")
login_username_entry.pack(pady=5)

login_password_entry = tk.Entry(login_frame, show="*", width=30)
login_password_entry.insert(0, "Password")
login_password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(pady=5)

# 二次验证框
mfa_frame = tk.LabelFrame(root, text="MFA Verification", padx=10, pady=10)
mfa_code_entry = tk.Entry(mfa_frame, width=30)
mfa_code_entry.insert(0, "Verification Code")
mfa_code_entry.pack(pady=5)

mfa_button = tk.Button(mfa_frame, text="Verify MFA", command=verify_mfa)
mfa_button.pack(pady=5)

# 管理员操作框
auth_action_frame = tk.LabelFrame(root, text="Authenticated Actions", padx=10, pady=10)
admin_action_button = tk.Button(auth_action_frame, text="Perform Admin Action", command=admin_action)
admin_action_button.pack(pady=5)

root.mainloop()
