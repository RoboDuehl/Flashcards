from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('vocab.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_table_names():
    conn = sqlite3.connect('vocab.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

@app.route('/')
def index():
    categories = get_table_names()
    print("Available tables:", categories)  # Debug print
    return render_template('index.html', categories=categories)

@app.route('/api/flashcards')
def flashcards():
    conn = get_db_connection()
    words = conn.execute('SELECT * FROM vocabulary').fetchall()
    conn.close()
    return jsonify([dict(word) for word in words])



@app.route('/api/flashcards/update', methods=['POST'])
def update_flashcard():
    data = request.get_json()
    print("Full received data:", data)  # Debug print
    word = data.get('word')
    meaning = data.get('meaning')
    example = data.get('example')

    print("Received update for word:", word)  # Debug print

    if not word or not meaning or not example:
        return jsonify({'error': 'Missing data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE vocabulary SET meaning = ?, example = ? WHERE LOWER(word) = LOWER(?)',
        (meaning, example, word)
    )
    conn.commit()
    updated_rows = cursor.rowcount
    print("Rows updated:", updated_rows)  # Debug print
    conn.close()

    if updated_rows == 0:
        return jsonify({'error': 'Word not found'}), 404

    return jsonify({'success': True})


@app.route('/api/flashcards/add', methods=['POST'])
def add_flashcard_api():
    data = request.get_json()
    word = data.get('word')
    meaning = data.get('meaning')
    example = data.get('example')
    category = data.get('category')  # This is the table name

    if not word or not meaning or not category:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    # SECURITY CHECK: validate the table name
    allowed_tables = get_table_names()  # You define this function
    if category not in allowed_tables:
        return jsonify({'success': False, 'error': 'Invalid category (table name)'}), 400

    try:
        conn = sqlite3.connect('vocab.db')
        cursor = conn.cursor()
        
        # Use string formatting carefully; table names can't be parameterized
        sql = f"INSERT INTO {category} (word, meaning, example) VALUES (?, ?, ?)"
        cursor.execute(sql, (word, meaning, example))
        conn.commit()
        conn.close()

        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


