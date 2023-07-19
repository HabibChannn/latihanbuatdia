import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI= os.environ.get("mongodb+srv://AyangFreya:AyangElla@projectayang.c1mw30u.mongodb.net/")
DB_NAME = os.environ.get("Ayang_freya")

client = MongoClient("mongodb+srv://AyangFreya:AyangElla@projectayang.c1mw30u.mongodb.net/?retryWrites=true&w=majority")
                         
db = client['Ayang_freya']

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")

    profile_image = request.files.get("profile_image")
    cover_image = request.files.get("cover_image")

    profile_image_filename = None
    if profile_image:
        profile_image_filename = os.path.join(app.config['UPLOAD_FOLDER'], profile_image.filename)
        profile_image.save(profile_image_filename)

    cover_image_filename = None
    if cover_image:
        cover_image_filename = os.path.join(app.config['UPLOAD_FOLDER'], cover_image.filename)
        cover_image.save(cover_image_filename)

    doc = {
        'profile_image': profile_image_filename if profile_image_filename else '',
        'cover_image': cover_image_filename if cover_image_filename else '',
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'Menulis Cerita Berhasil!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
