from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = "carsweb.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ensure tbcars table exists."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tbcars (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            carname  TEXT NOT NULL,
            carbrand TEXT NOT NULL,
            carmodel TEXT NOT NULL,
            carprice TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ── GET  /api/cars  — list all ─────────────────────────────────────────────────
@app.route("/api/cars", methods=["GET"])
def list_cars():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tbcars ORDER BY id").fetchall()
    conn.close()
    return jsonify({"status": "success", "count": len(rows), "data": [dict(r) for r in rows]}), 200


# ── GET  /api/cars/<id>  — detail ─────────────────────────────────────────────
@app.route("/api/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tbcars WHERE id = ?", (car_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"status": "error", "message": "Car not found"}), 404
    return jsonify({"status": "success", "data": dict(row)}), 200


# ── POST /api/cars  — create ───────────────────────────────────────────────────
@app.route("/api/cars", methods=["POST"])
def create_car():
    data = request.get_json(silent=True) or {}
    name  = str(data.get("carname", "")).strip()
    brand = str(data.get("carbrand", "")).strip()
    model = str(data.get("carmodel", "")).strip()
    price = str(data.get("carprice", "")).strip()
    if not all([name, brand, model, price]):
        return jsonify({"status": "error", "message": "Fields carname, carbrand, carmodel, carprice are required"}), 400
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO tbcars (carname, carbrand, carmodel, carprice) VALUES (?, ?, ?, ?)",
        (name, brand, model, price),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"status": "success", "message": "Car created", "id": new_id}), 201


# ── PUT  /api/cars/<id>  — update ─────────────────────────────────────────────
@app.route("/api/cars/<int:car_id>", methods=["PUT"])
def update_car(car_id):
    data = request.get_json(silent=True) or {}
    conn = get_db()
    row = conn.execute("SELECT * FROM tbcars WHERE id = ?", (car_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"status": "error", "message": "Car not found"}), 404

    name  = str(data.get("carname",  row["carname"])).strip()
    brand = str(data.get("carbrand", row["carbrand"])).strip()
    model = str(data.get("carmodel", row["carmodel"])).strip()
    price = str(data.get("carprice", row["carprice"])).strip()

    conn.execute(
        "UPDATE tbcars SET carname=?, carbrand=?, carmodel=?, carprice=? WHERE id=?",
        (name, brand, model, price, car_id),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Car updated"}), 200


# ── DELETE /api/cars/<id>  — delete ───────────────────────────────────────────
@app.route("/api/cars/<int:car_id>", methods=["DELETE"])
def delete_car(car_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM tbcars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"status": "error", "message": "Car not found"}), 404
    return jsonify({"status": "success", "message": "Car deleted"}), 200


# ── GET  /api/cars/search?q=  — search ────────────────────────────────────────
@app.route("/api/cars/search", methods=["GET"])
def search_cars():
    keyword = request.args.get("q", "").strip()
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM tbcars WHERE carbrand LIKE ? OR carmodel LIKE ? OR carname LIKE ?",
        (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
    ).fetchall()
    conn.close()
    return jsonify({"status": "success", "count": len(rows), "data": [dict(r) for r in rows]}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002)
