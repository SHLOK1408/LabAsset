from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

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
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()

    filtered_equipment = equipment

    if search:
        search_lower = search.lower()

        filtered_equipment = [
            item for item in filtered_equipment
            if search_lower in item["asset_id"].lower()
            or search_lower in item["name"].lower()
        ]

    if status_filter:
        filtered_equipment = [
            item for item in filtered_equipment
            if item["status"] == status_filter
        ]

    total = len(equipment)

    available = sum(
        item["status"] == "Available"
        for item in equipment
    )

    issued = sum(
        item["status"] == "Issued"
        for item in equipment
    )

    maintenance = sum(
        item["status"] == "Maintenance"
        for item in equipment
    )

    return render_template(
        "index.html",
        equipment=filtered_equipment,
        total=total,
        available=available,
        issued=issued,
        maintenance=maintenance,
        search=search,
        status_filter=status_filter
    )


@app.route("/add", methods=["POST"])
def add_equipment():
    asset_id = request.form.get(
        "asset_id", ""
    ).strip().upper()

    name = request.form.get(
        "name", ""
    ).strip()

    category = request.form.get(
        "category", ""
    ).strip()

    if not asset_id or not name or not category:
        flash("All fields are required.", "error")
        return redirect(url_for("home"))

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

    duplicate = any(
        item["asset_id"] == asset_id
        for item in equipment
    )

    if duplicate:
        flash("Asset ID already exists.", "error")
        return redirect(url_for("home"))

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

    flash(
        "Equipment added successfully.",
        "success"
    )

    return redirect(url_for("home"))


@app.route("/issue/<asset_id>", methods=["POST"])
def issue_equipment(asset_id):
    for item in equipment:
        if item["asset_id"] == asset_id:

            if item["status"] != "Available":
                flash(
                    "Only available equipment can be issued.",
                    "error"
                )
                return redirect(url_for("home"))

            item["status"] = "Issued"

            flash(
                f"{asset_id} issued successfully.",
                "success"
            )

            return redirect(url_for("home"))

    flash("Equipment not found.", "error")
    return redirect(url_for("home"))


@app.route("/return/<asset_id>", methods=["POST"])
def return_equipment(asset_id):
    for item in equipment:
        if item["asset_id"] == asset_id:

            if item["status"] != "Issued":
                flash(
                    "Only issued equipment can be returned.",
                    "error"
                )
                return redirect(url_for("home"))

            item["status"] = "Available"

            flash(
                f"{asset_id} returned successfully.",
                "success"
            )

            return redirect(url_for("home"))

    flash("Equipment not found.", "error")
    return redirect(url_for("home"))


@app.route("/maintenance/<asset_id>", methods=["POST"])
def send_to_maintenance(asset_id):
    for item in equipment:
        if item["asset_id"] == asset_id:

            if item["status"] != "Available":
                flash(
                    "Only available equipment can be sent to maintenance.",
                    "error"
                )
                return redirect(url_for("home"))

            item["status"] = "Maintenance"

            flash(
                f"{asset_id} sent to maintenance.",
                "success"
            )

            return redirect(url_for("home"))

    flash("Equipment not found.", "error")
    return redirect(url_for("home"))


@app.route("/restore/<asset_id>", methods=["POST"])
def restore_equipment(asset_id):
    for item in equipment:
        if item["asset_id"] == asset_id:

            if item["status"] != "Maintenance":
                flash(
                    "Only equipment under maintenance can be restored.",
                    "error"
                )
                return redirect(url_for("home"))

            item["status"] = "Available"

            flash(
                f"{asset_id} is available again.",
                "success"
            )

            return redirect(url_for("home"))

    flash("Equipment not found.", "error")
    return redirect(url_for("home"))


@app.route("/api/equipment")
def equipment_api():
    return jsonify(equipment)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )
