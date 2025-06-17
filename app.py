from flask import Flask, request, render_template, jsonify
import os
import google.generativeai as genai
import magic
from datetime import datetime
import re

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    input_type = data.get('input_type')
    content = data.get('content')
    custom_prompt = data.get('custom_prompt', '').strip()

    if not input_type or not content:
        return jsonify({'error': 'Input type and content are required'}), 400

    try:
        if input_type == 'url':
            # For URL input, we would need to implement URL fetching
            # This is a placeholder
            code_content = content
        else:  # txt file
            code_content = content

        # Generate code review using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = """
You are a code review assistant specialized in Python and Apache Spark. Provide a comprehensive review of the code changes including:
1. Executive Summary
2. Syntax Review
3. Code Style (PEP8 compliance)
4. Performance Analysis (especially for Apache Spark)
Format the response in JSON with these sections, using keys: executive_summary, syntax_review, code_style, performance_analysis.
"""
        if custom_prompt:
            prompt = prompt + "\nCustom Reviewer Instructions: " + custom_prompt
        user_input = f"Please review the following code changes:\n{code_content}"
        full_prompt = prompt + "\n" + user_input
        response = model.generate_content(full_prompt)

        # Try to extract JSON from response.text
        import json
        import logging
        try:
            review = json.loads(response.text)
        except Exception as e:
            # Fallback: try to extract JSON substring and fix invalid escapes
            import re
            match = re.search(r'\{[\s\S]*\}', response.text)
            if match:
                json_str = match.group(0)
                # Fix invalid backslashes by replacing unescaped backslashes with double backslashes
                # This is a best-effort fix and may not work for all cases
                def fix_backslashes(s):
                    # Replace single backslash not followed by valid escape
                    return re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', s)
                try:
                    review = json.loads(json_str)
                except Exception as e2:
                    fixed_json_str = fix_backslashes(json_str)
                    try:
                        review = json.loads(fixed_json_str)
                    except Exception as e3:
                        logging.error(f"Failed to parse Gemini response after fixing backslashes: {e3}\nRaw: {response.text}")
                        log_entry = {
                            'timestamp': datetime.now().isoformat(),
                            'input_type': input_type,
                            'content': content,
                            'model_output': None,
                            'error': f'Failed to parse Gemini response as JSON after fixing backslashes: {e3}',
                            'raw': response.text,
                        }
                        log_path = os.path.join(os.path.dirname(__file__), 'review_logs.json')
                        import threading
                        lock = threading.Lock()
                        with lock:
                            try:
                                if os.path.exists(log_path):
                                    with open(log_path, 'r', encoding='utf-8') as f:
                                        logs = json.load(f)
                                else:
                                    logs = []
                            except Exception:
                                logs = []
                            logs.append(log_entry)
                            with open(log_path, 'w', encoding='utf-8') as f:
                                json.dump(logs, f, indent=2)
                        return jsonify({'error': 'Failed to parse Gemini response as JSON. Please check your code for unescaped backslashes or invalid characters.', 'raw': response.text}), 500
            else:
                # Log failure
                logging.error(f"Failed to parse Gemini response as JSON: {e}\nRaw: {response.text}")
                log_entry = {
                    'timestamp': datetime.now().isoformat(),
                    'input_type': input_type,
                    'content': content,
                    'model_output': None,
                    'error': f'Failed to parse Gemini response as JSON: {e}',
                    'raw': response.text,
                }
                log_path = os.path.join(os.path.dirname(__file__), 'review_logs.json')
                import threading
                lock = threading.Lock()
                with lock:
                    try:
                        if os.path.exists(log_path):
                            with open(log_path, 'r', encoding='utf-8') as f:
                                logs = json.load(f)
                        else:
                            logs = []
                    except Exception:
                        logs = []
                    logs.append(log_entry)
                    with open(log_path, 'w', encoding='utf-8') as f:
                        json.dump(logs, f, indent=2)
                return jsonify({'error': 'Failed to parse Gemini response as JSON. Please check your code for unescaped backslashes or invalid characters.', 'raw': response.text}), 500

        # Log successful review
        name = data.get('name', 'Unnamed Review')
        log_entry = {
            'name': name,
            'timestamp': '2025-06-15T11:38:08-07:00',
            'input_type': input_type,
            'content': content,
            'model_output': review,
            'error': None,
        }
        log_path = os.path.join(os.path.dirname(__file__), 'review_logs.json')
        import threading
        lock = threading.Lock()
        with lock:
            try:
                if os.path.exists(log_path):
                    with open(log_path, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                else:
                    logs = []
            except Exception:
                logs = []
            logs.append(log_entry)
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)

        return jsonify({'review': review})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

import signal

@app.route('/logs', methods=['GET'])
def get_logs():
    import json
    log_path = os.path.join(os.path.dirname(__file__), 'review_logs.json')
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
    except Exception:
        logs = []
    return jsonify(logs)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    import os
    import sys
    # Try to kill the current process
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({'message': 'Server shutting down...'}), 200

if __name__ == '__main__':
    app.run(debug=True)
