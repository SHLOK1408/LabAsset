from flask import Flask, render_template

app = Flask(__name__)

equipment = [
    {
        "asset_id": "LAB001",
        "name": "Cisco Router",
        "category": "Networking",
        "status": "Available"
    },
    {
        "asset_id": "LAB002",
        "name": "Digital Oscilloscope",
        "category": "Electronics",
        "status": "Issued"
    },
    {
        "asset_id": "LAB003",
        "name": "Arduino Uno",
        "category": "Electronics",
        "status": "Maintenance"
    }
]


@app.route("/")
def home():
    total = len(equipment)
    available = sum(item["status"] == "Available" for item in equipment)
    issued = sum(item["status"] == "Issued" for item in equipment)
    maintenance = sum(
        item["status"] == "Maintenance" for item in equipment
    )

    return render_template(
        "index.html",
        equipment=equipment,
        total=total,
        available=available,
        issued=issued,
        maintenance=maintenance
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)