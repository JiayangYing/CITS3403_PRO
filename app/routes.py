from flask import render_template, request, jsonify
from app import app
import os

@app.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@app.route('/')
@app.route('/login')
def login():
    return render_template("/users/login.html", title="Home", hideNav=True)

@app.route('/home')
def home():
    return render_template('/home/home.html')

@app.route('/sdg_img_dirs', methods=['POST'])
def test():
    is_dark_mode = request.json.get('isDarkMode')
    path = 'web-inverted'
    if is_dark_mode:
        path = 'web'
    img_dir = os.path.join(app.root_path, 'static', 'img', 'sdg', path)
    sdg_images = [path+'/'+img for img in os.listdir(img_dir) if img.endswith('png')]
    return jsonify({'sdg_images': sdg_images})

@app.route('/signup')
def signup():
    return render_template('/users/signup.html', hideNav=True)
