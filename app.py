# up
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, re

# folders
app = Flask(__name__, template_folder="templates", static_folder="static")

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, re

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///driftstereo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_name = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    color = db.Column(db.String(7), nullable=False, default="#f0f0f0")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    msgs = Message.query.order_by(Message.created_at.desc()).limit(100).all()
    return render_template("index.html", messages=msgs)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        to_name = (request.form.get("to_name") or "").strip()
        body = (request.form.get("body") or "").strip()
        color = (request.form.get("color") or "#f0f0f0").strip()

        if not to_name or not body:
            flash("Completa 'To' y 'Mensaje'."); return redirect(url_for("submit"))
        if len(to_name) > 50:
            flash("‘Para’ máx. 50 caracteres."); return redirect(url_for("submit"))
        if len(body) > 500:
            flash("Mensaje máx. 500 caracteres."); return redirect(url_for("submit"))
        if not re.match(r"^#[0-9A-Fa-f]{6}$", color):
            color = "#f0f0f0"

        db.session.add(Message(to_name=to_name, body=body, color=color))
        db.session.commit()
        return redirect(url_for("thanks"))
    return render_template("submit.html")

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@app.route("/messages.json")
def messages_json():
    msgs = Message.query.order_by(Message.created_at.desc()).limit(100).all()
    return jsonify([{
        "id": m.id, "to": m.to_name, "body": m.body,
        "color": m.color, "created_at": m.created_at.isoformat()
    } for m in msgs])

if __name__ == "__main__":
    app.run(debug=True)  # host/port por defecto: 127.0.0.1:5000
