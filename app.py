from flask import Flask, render_template
from sysinfo import get_system_info
from gemini import generate_story

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sysinfo')
def sysinfo_page():
    system_info = get_system_info()
    return render_template("sysinfo.html", info=system_info)

@app.route("/gemini")
def story_page():
    title, story, moral= generate_story()
    return render_template('gemini.html', title=title, moral=moral, story=story)

if __name__ == "__main__":
    app.run(host="192.168.20.95", port=5000)
