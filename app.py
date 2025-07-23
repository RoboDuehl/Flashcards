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

@app.route('/api/flashcards/update', methods=['POST'])
def update_flashcard():
    data = request.get_json()
    word = data.get('word')
    meaning = data.get('meaning')
    example = data.get('example')

    if not word or not meaning or not example:
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE vocabulary SET meaning = ?, example = ? WHERE word = ?',
        (meaning, example, word)
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()

    if updated_rows == 0:
        return jsonify({'error': 'Word not found'}), 404

    return jsonify({'success': True})

