from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>LabAsset</h1>
    <h2>Laboratory Equipment Tracking System</h2>
    <p>LabAsset is running successfully.</p>
    """


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)