# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")

# --- SQLite en ./instance/driftstereo.db ---
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "driftstereo.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    to_name    = db.Column(db.String(50), nullable=False)
    body       = db.Column(db.String(500), nullable=False)
    color      = db.Column(db.String(7),  nullable=False, default="#f0f0f0")
    created_at = db.Column(db.DateTime,   nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# (pasteles + negro)
# Texto blanco SOLO en negro.
ALLOWED_COLORS = {
    "Pink":         {"hex": "#FFD1DC", "text": "#000000"},
    "Baby Blue":    {"hex": "#ADD8E6", "text": "#000000"},
    "Pastel Yellow":{"hex": "#FDE68A", "text": "#000000"},  
    "Mint Green":   {"hex": "#A7F3D0", "text": "#000000"},  
    "Lila":        {"hex": "#E9D5FF", "text": "#000000"},
    "Light Brown":  {"hex": "#C8B6A6", "text": "#000000"},  
    "Black":        {"hex": "#000000", "text": "#FFFFFF"},
}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/gallery", endpoint="gallery")
def gallery_view():
    msgs = Message.query.order_by(Message.created_at.desc()).limit(100).all()
    # DEBUG: ver cuántos hay
    print(f"[GALLERY] mensajes: {len(msgs)} en {db_path}")
    return render_template("gallery.html", messages=msgs)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        to_name = (request.form.get("to_name") or "").strip()
        body    = (request.form.get("body") or "").strip()
        color   = (request.form.get("color") or "").strip()

        if not to_name or not body:
            flash("Please fill both 'To' and 'Message'.")
            return redirect(url_for("submit"))

        # Validación: solo colores permitidos
        allowed_hexes = {info["hex"] for info in ALLOWED_COLORS.values()}
        if color not in allowed_hexes:
            flash("Please choose a color from the list.")
            return redirect(url_for("submit"))

        db.session.add(Message(to_name=to_name, body=body, color=color))
        db.session.commit()
        return redirect(url_for("thanks"))

    return render_template("submit.html", colors=ALLOWED_COLORS)

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

# endpoint JSON
@app.route("/messages.json")
def messages_json():
    msgs = Message.query.order_by(Message.created_at.desc()).limit(100).all()
    return jsonify([
        {"id": m.id, "to": m.to_name, "body": m.body, "color": m.color, "created_at": m.created_at.isoformat()}
        for m in msgs
    ])

if __name__ == "__main__":
    app.run(debug=True)
