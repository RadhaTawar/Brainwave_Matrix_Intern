from flask import Flask, render_template, request, jsonify
import re
import string
import math

app = Flask(__name__)

def analyze_password(password):
    if not password:  
        return {
            "strength": 0,
            "evaluation": "N/A",
            "properties": {
                "Password length": {"value": 0, "comment": "N/A"},
                "Numbers": {"value": 0, "comment": "N/A"},
                "Uppercase Letters": {"value": 0, "comment": "N/A"},
                "Lowercase Letters": {"value": 0, "comment": "N/A"},
                "Symbols": {"value": 0, "comment": "N/A"},
                "Letters": {"value": 0, "comment": "N/A"},
                "TOP 10000 password": {"value": "N/A", "comment": "N/A"},
                "Charset size": {"value": 0, "comment": "N/A"},
            },
            "cracking_times": {
                "Standard Desktop PC": "N/A",
                "Fast Desktop PC": "N/A",
                "GPU": "N/A",
                "Fast GPU": "N/A",
                "Parallel GPUs": "N/A",
                "Medium size botnet": "N/A",
            },
            "dictionary_check": {"safe": True, "message": "N/A"},
            "safe": True,
        }
        
    length = len(password)
    numbers = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    uppercase = sum(c.isupper() for c in password)
    lowercase = sum(c.islower() for c in password)
    symbols = length - letters - numbers
    top_10000 = False  

    dictionary = ["radha", "tawar", "123456"]  
    leet_replacements = {"a": "4", "e": "3", "o": "0", "@": "a"}

    dictionary_check = {
        "safe": True,
        "message": "",
    }

    words_in_password = re.findall(r'[a-zA-Z0-9]+', password.lower())
    
    found_words = []
    
    for word in words_in_password:
        if word in dictionary:
            found_words.append(word)
        else:
            leet_word = "".join(leet_replacements.get(c, c) for c in word)
            if leet_word in dictionary:
                found_words.append(word)

    if found_words:
        dictionary_check["safe"] = False
        message_parts = []
        for found_word in found_words:
            if found_word in dictionary:
                message_parts.append(f"'{found_word}' is a dictionary word.")
            else:
                original_word = next((w for w in words_in_password if "".join(leet_replacements.get(c, c) for c in w) == found_word), found_word)
                message_parts.append(f"'{original_word}' is a leet variation of a dictionary word.")

        dictionary_check["message"] = " ".join(message_parts)

    strength = min(100, length * 5 + numbers * 2 + letters * 2 + symbols * 3)  
    evaluation = "Excellent!" if strength >= 90 else "Good" if strength >= 70 else "Fair" if strength >= 50 else "Poor"

    # --- Updated Password Properties Logic ---
    properties = {}

    # Password length
    if length == 0:
        properties["Password length"] = {"value": length, "comment": "No password given"}
    elif length <= 4:
        properties["Password length"] = {"value": length, "comment": "Too short"}
    elif length <= 7:
        properties["Password length"] = {"value": length, "comment": "Short"}
    elif length == 8:
        properties["Password length"] = {"value": length, "comment": "Medium long"}
    else:
        properties["Password length"] = {"value": length, "comment": "OK"}

    # Numbers, Uppercase, Lowercase, Symbols
    properties["Numbers"] = {"value": numbers, "comment": "Used" if numbers > 0 else "Not used"}
    properties["Uppercase Letters"] = {"value": uppercase, "comment": "Used" if uppercase > 0 else "Not used"}
    properties["Lowercase Letters"] = {"value": lowercase, "comment": "Used" if lowercase > 0 else "Not used"}
    properties["Symbols"] = {"value": symbols, "comment": "Used" if symbols > 0 else "Not used"}
    properties["Letters"] = {"value": letters, "comment": "Used" if letters > 0 else "Not used"}
    properties["TOP 10000 password"] = {"value": "NO" if not top_10000 else "YES",
                                        "comment": "Password is NOT one of the most frequently used passwords." if not top_10000
                                        else "Password is one of the most frequently used passwords."}
    
    # Charset size
    charset = set(password)
    charset_size = len(charset)

    if charset_size == 0:
        properties["Charset size"] = {"value": charset_size, "comment": "Low"}
    elif charset <= set(string.digits):
        properties["Charset size"] = {"value": 10, "comment": "Low (0-9)"}
    elif charset <= set(string.ascii_lowercase):
        properties["Charset size"] = {"value": 26, "comment": "Low (a-z)"}
    elif charset <= set(string.ascii_uppercase):
        properties["Charset size"] = {"value": 26, "comment": "Low (A-Z)"}
    elif charset <= set(string.ascii_letters):
        properties["Charset size"] = {"value": 52, "comment": "Medium (a-z, A-Z)"}
    elif charset <= set(string.ascii_letters + string.digits):
        properties["Charset size"] = {"value": 62, "comment": "Medium (a-z, A-Z, 0-9)"}
    else:
        properties["Charset size"] = {"value": 94, "comment": "High (a-z, A-Z, 0-9, symbols)"}

    # --- Updated Cracking Time Logic ---
    if length == 0:
        cracking_times = {
            "Standard Desktop PC": "N/A",
            "Fast Desktop PC": "N/A",
            "GPU": "N/A",
            "Fast GPU": "N/A",
            "Parallel GPUs": "N/A",
            "Medium size botnet": "N/A",
        }
    else:

        if charset_size == 0:
            charset_size = 1

        combinations = charset_size ** length

        # Cracking speeds (guesses per second)
        cracking_speeds = {
            "Standard Desktop PC": 10**9,
            "Fast Desktop PC": 5 * 10**9,
            "GPU": 10**11,
            "Fast GPU": 10**12,
            "Parallel GPUs": 5 * 10**12,
            "Medium size botnet": 10**13,
        }

        cracking_times = {}
        for machine, speed in cracking_speeds.items():
            seconds = combinations / speed
            cracking_times[machine] = format_time(seconds)

    return {
        "strength": strength,
        "evaluation": evaluation,
        "properties": properties,
        "cracking_times": cracking_times,
        "dictionary_check": dictionary_check,
        "safe": dictionary_check["safe"],
    }

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{days:.2f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        analysis = analyze_password(password)
        return jsonify(analysis)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)