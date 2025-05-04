from flask import Flask, render_template, request, redirect, url_for, session
import random
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'abc3xyz'

IMAGE_FOLDER = 'static/images'
IMAGE_FILES = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png','.jpg','.jpeg'))]

def gri():
    return random.choice(IMAGE_FILES)

def cd():
    conn = sqlite3.connect('words.db')
    curson = conn.cursor()
    curson.execute('''
        CREATE TABLE IF NOT EXISTS user_word (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

cd()

def we(word):
    conn = sqlite3.connect('words.db')
    curson = conn.cursor()
    curson.execute('SELECT id FROM user_word WHERE WORD = ?',(word,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_word(word):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_words (word) VALUES (?)', (word,))
    conn.commit()
    conn.close()
@app.route('/')
def index():
    if 'image' not in session:
        session['image'] = gri()
    return render_template('index.html', image=session['image'])

@app.route('/new_image')
def ni():
    session['image'] = gri()
    return redirect(url_for('index'))

@app.route('/learn', methods=['POST'])
def l():
    words = [request.form.get(f'word{i}') for i in range(1, 6)]
    words = [word.strip() for word in words if word.strip()]
    if len(words) < 1 or len(words) > 5:
        return "Please enter between 1 and 5 words.", 400
    for word in words:
        save_word(word)
    return render_template('learn.html', words=words, image=session['image'])

@app.route('/my_words')
def mw():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM user_words')
    words = cursor.fetchall()
    conn.close()
    return render_template('my_words.html',words=words)

if __name__=='__main__':
    app.run(debug=True, port=5005)