from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('vocab.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flashcards')
def flashcards():
    conn = get_db_connection()
    words = conn.execute('SELECT * FROM vocabulary').fetchall()
    conn.close()
    return jsonify([dict(word) for word in words])

if __name__ == '__main__':
    app.run(debug=True)



