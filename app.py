from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
import sqlite3
from fpdf import FPDF
import requests
import cohere
import dropbox
import os
import datetime

app = Flask(__name__)

# Replace with your actual Cohere API key
cohere_api_key = 'YOUR API KEY'
co = cohere.Client(cohere_api_key)

TOKEN = "YOUR SECRET TOKEN"
dbx = dropbox.Dropbox(TOKEN)

@app.route('/add_vehicle')
def add_vehicle():
    return render_template('qr.html')

@app.route('/submit', methods=['POST'])
def submit():
    vehicle_id = request.form['vehicle-id']
    make = request.form['vehicle-make']
    model = request.form['vehicle-model']
    year = request.form['vehicle-year']
    color = request.form['vehicle-color']
    
    with sqlite3.connect('vehicles.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vehicle (vehicle_id, make, model, year, color) 
            VALUES (?, ?, ?, ?, ?)
        ''', (vehicle_id, make, model, year, color))
        conn.commit()
    
    return redirect(url_for('view'))

@app.route('/view')
def view():
    with sqlite3.connect('vehicles.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vehicle')
        records = cursor.fetchall()
    return render_template('view.html', records=records)

def init_db():
    conn = sqlite3.connect('response.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS SurveyResponse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rust_dents_damage TEXT,
            engine_oil_condition TEXT,
            engine_oil_color TEXT,
            brake_fluid_condition TEXT,
            brake_fluid_color TEXT,
            oil_leak TEXT
        )
    ''')
    conn.commit()
    conn.close()

    with sqlite3.connect('vehicles.db') as conn1:
        cursor = conn1.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id TEXT NOT NULL,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year TEXT NOT NULL,
                color TEXT NOT NULL
            )
        ''')
        conn1.commit()

@app.route('/')
def home():
    return render_template('indexmain.html')

@app.route('/login', methods=['GET', 'POST'])
def start_inspect():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Assuming a simple login check for demo purposes
        if email == 'test@example.com' and password == 'password':
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/save_voice_input', methods=['POST'])
def save_voice_input():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid input"}), 400

    rust_dents_damage = data.get('rust_dents_damage', '')
    engine_oil_condition = data.get('engine_oil_condition', '')
    engine_oil_color = data.get('engine_oil_color', '')
    brake_fluid_condition = data.get('brake_fluid_condition', '')
    brake_fluid_color = data.get('brake_fluid_color', '')
    oil_leak = data.get('oil_leak', '')

    try:
        conn = sqlite3.connect('response.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO SurveyResponse (
                rust_dents_damage,
                engine_oil_condition,
                engine_oil_color,
                brake_fluid_condition,
                brake_fluid_color,
                oil_leak
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (rust_dents_damage, engine_oil_condition, engine_oil_color, brake_fluid_condition, brake_fluid_color, oil_leak))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "data": data})

@app.route('/get_voice_inputs', methods=['GET'])
def get_voice_inputs():
    try:
        conn = sqlite3.connect('response.db')
        c = conn.cursor()
        c.execute('SELECT * FROM SurveyResponse')
        rows = c.fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
    voice_inputs = [{"id": row[0], "rust_dents_damage": row[1], "engine_oil_condition": row[2], "engine_oil_color": row[3], "brake_fluid_condition": row[4], "brake_fluid_color": row[5], "oil_leak": row[6]} for row in rows]

    # Generate recommendations using AI
    recommendations = generate_recommendations(voice_inputs)

    return jsonify({
        "status": "success",
        "data": voice_inputs,
        "recommendations": recommendations
    })

def generate_recommendations(responses):
    recommendations = []

    for response in responses:
        response_text = f"Rust/Dents/Damage: {response['rust_dents_damage']}, Engine Oil Condition: {response['engine_oil_condition']}, Engine Oil Color: {response['engine_oil_color']}, Brake Fluid Condition: {response['brake_fluid_condition']}, Brake Fluid Color: {response['brake_fluid_color']}, Oil Leak: {response['oil_leak']}"
        
        prompt = f"The following is a survey response about a car's condition. Provide recommendations for the car owner based on the response.\n\n{response_text}\n\nRecommendations:"

        try:
            ai_response = co.generate(
                model='command-xlarge-nightly',  # Use the appropriate model name
                prompt=prompt,
                max_tokens=150
            )
            recommendation = ai_response.generations[0].text.strip()
        except Exception as e:
            recommendation = f"Error generating recommendation: {str(e)}"

        recommendations.append({
            "id": response['id'],
            "recommendation": recommendation
        })

    return recommendations

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    content = data.get('content', '')

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        
        pdf_output = 'recommendation.pdf'
        pdf.output(pdf_output)
        
        return send_file(pdf_output, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text_to_translate = data.get('text', '')
    
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text_to_translate,
        'langpair': 'en|ta'  # English to Tamil (change 'ta' for other languages)
    }
    response = requests.get(url, params=params)
    
    if response.ok:
        translation = response.json().get('responseData', {}).get('translatedText', '')
        return jsonify({'translatedText': translation})
    else:
        return jsonify({'error': 'Translation failed'}), 500
    
@app.route('/add_image')
def add_image():
    return render_template('add_image.html', filename=None)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    
    # Save file locally
    file_path = os.path.join("local", filename)
    file.save(file_path)
    
    # Upload file to Dropbox
    with open(file_path, "rb") as f:
        data = f.read()
        dbx.files_upload(data, f"/{filename}")
    
    # Return to the main page with the filename
    return render_template('add_image.html', filename=filename)

@app.route('/uploads/<filename>')
def send_image(filename):
    local_directory = os.path.join(os.getcwd(), "local")
    file_path = os.path.join(local_directory, filename)
    print(f"Checking file existence at: {file_path}")  # Debugging statement
    if not os.path.exists(file_path):
        return "File not found", 404
    return send_file(file_path)

if __name__ == '__main__':
    init_db()
    if not os.path.exists('local'):
        os.makedirs('local')
    app.run(debug=True)
