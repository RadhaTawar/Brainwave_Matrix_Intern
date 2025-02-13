from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__, template_folder='templates')


# Phishing Keywords & Suspicious Indicators
PHISHING_KEYWORDS = {
    "login", "secure", "update", "password", "bank", "free", "gift", "win", "prize", 
    "discount", "offer", "urgent", "limited", "actnow", "verify", "account", 
    "information", "credit", "card", "billing"
}
SUSPICIOUS_SUBDOMAINS = {
    "login", "signin", "verify", "account", "update", "secure", "bank", "paypal", 
    "admin", "cpanel", "webmail"
}
SUSPICIOUS_TLDS = {".xyz", ".top", ".club", ".online", ".site", ".bid", ".loan", ".vip", ".icu"}
SUSPICIOUS_CHARACTERS = {"~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+",
                         "{", "}", "[", "]", ";", "<", ">", ",", "?", "\\", "|", "-"}

def phishing_url(url):
    """Analyzes a URL for potential phishing indicators."""
    try:
        parsed_url = urllib.parse.urlparse(url)

        # URL Validation and Checks
        if not parsed_url.scheme or not parsed_url.netloc:
            return "Invalid URL: Missing scheme or domain"
        
        if any(keyword in url.lower() for keyword in PHISHING_KEYWORDS):
            return "Suspicious URL: Contains phishing keywords"
        
        if any(subdomain in parsed_url.netloc.split('.') for subdomain in SUSPICIOUS_SUBDOMAINS):
            return "Suspicious URL: Contains a known phishing subdomain"
        
        if any(parsed_url.netloc.endswith(tld) for tld in SUSPICIOUS_TLDS):
            return "Suspicious URL: Uses a known phishing TLD"
        
        if len(url) > 100:
            return "Suspicious URL: URL is very long"
        
        # Check for suspicious characters in path, query, or fragment (exclude valid URL characters like / and :)
        suspicious_url_parts = parsed_url.path + parsed_url.query + parsed_url.fragment
        if any(char in SUSPICIOUS_CHARACTERS for char in suspicious_url_parts):
            return "Suspicious URL: Contains unusual characters"
        
        if parsed_url.scheme == "http":
            return "Suspicious URL: Uses HTTP (not HTTPS)"
        return "Safe URL (No obvious threats detected)"
    
    except Exception as e:
        return f"Error analyzing URL: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        result = phishing_url(url)
        return render_template('index.html', result=result)
    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)
