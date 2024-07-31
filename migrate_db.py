import sqlite3

def migrate_db():
    conn = sqlite3.connect('voice_inputs.db')
    c = conn.cursor()
    # Check if the 'question' column exists
    c.execute("PRAGMA table_info(VoiceInput)")
    columns = [col[1] for col in c.fetchall()]
    if 'question' not in columns:
        # Add the 'question' column to the table
        c.execute("ALTER TABLE VoiceInput ADD COLUMN question TEXT NOT NULL DEFAULT ''")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_db()
