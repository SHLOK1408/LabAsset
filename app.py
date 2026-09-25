from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "labasset-secret-key"

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

VALID_CATEGORIES = [
    "Networking",
    "Electronics",
    "Computer Accessories",
    "Other"
]


@app.route("/")
def home():
    total = len(equipment)

    available = sum(
        item["status"] == "Available" for item in equipment
    )

    issued = sum(
        item["status"] == "Issued" for item in equipment
    )

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


@app.route("/add", methods=["POST"])
def add_equipment():
    asset_id = request.form.get("asset_id", "").strip().upper()
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()

    # Check empty fields
    if not asset_id or not name or not category:
        flash("All fields are required.", "error")
        return redirect(url_for("home"))

    # Check Asset ID format
    if not (
        asset_id.startswith("LAB")
        and len(asset_id) == 6
        and asset_id[3:].isdigit()
    ):
        flash(
            "Asset ID must use the format LAB followed by 3 digits.",
            "error"
        )
        return redirect(url_for("home"))

    # Check duplicate Asset ID
    duplicate = any(
        item["asset_id"] == asset_id
        for item in equipment
    )

    if duplicate:
        flash("Asset ID already exists.", "error")
        return redirect(url_for("home"))

    # Check category
    if category not in VALID_CATEGORIES:
        flash("Invalid equipment category.", "error")
        return redirect(url_for("home"))

    new_equipment = {
        "asset_id": asset_id,
        "name": name,
        "category": category,
        "status": "Available"
    }

    equipment.append(new_equipment)

    flash("Equipment added successfully.", "success")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)