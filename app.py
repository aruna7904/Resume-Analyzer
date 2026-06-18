from flask import Flask, render_template, request, jsonify
import json
from config import Config
from database import init_db, get_db_connection
from utils.pdf_parser import extract_text_from_pdf
from models.agent import ResumeAgent

app = Flask(__name__)
app.config.from_object(Config)

init_db()
agent_engine = ResumeAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Payload items missing."}), 400
    
    file = request.files['resume']
    jd_text = request.form['job_description'].strip()
    
    if file.filename == '' or not jd_text:
        return jsonify({"error": "Empty values supplied."}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "System supports PDF extension sets only."}), 400

    try:
        resume_text = extract_text_from_pdf(file)
        analysis_result = agent_engine.analyze(resume_text, jd_text)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analysis_history 
            (user_id, job_title, ats_score, skills_found, missing_skills, suggestions, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            1,
            analysis_result['job_title'],
            analysis_result['ats_score'],
            json.dumps(analysis_result['skills_found']),
            json.dumps(analysis_result['missing_skills']),
            analysis_result['suggestions'],
            analysis_result['summary']
        ))
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "analysis_id": analysis_id})
        
    except Exception as e:
        error_message = str(e)
        
        # Catch Google API Quota limitations cleanly
        if "429" in error_message or "quota" in error_message.lower():
            return jsonify({
                "error": "The AI Agent is currently cooling down due to Google API free-tier traffic rules. Please wait 30 seconds and click 'Run Analysis Pipeline' again."
            }), 429
            
        return jsonify({"error": error_message}), 500

@app.route('/dashboard/<int:analysis_id>')
def dashboard(analysis_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM analysis_history WHERE analysis_id = ?', (analysis_id,)).fetchone()
    conn.close()
    
    if not row:
        return "Requested Evaluation Logs Are Missing.", 404
        
    report = dict(row)
    report['skills_found'] = json.loads(report['skills_found'])
    report['missing_skills'] = json.loads(report['missing_skills'])
    
    return render_template('dashboard.html', report=report)

@app.route('/history')
def history():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM analysis_history WHERE user_id = 1 ORDER BY analyzed_at DESC').fetchall()
    conn.close()
    return render_template('history.html', history=rows)

if __name__ == '__main__':
    app.run(debug=True, port=5001, use_reloader=True)