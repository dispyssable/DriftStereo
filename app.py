# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "dev-key"   # para flash()

# ---- HOME (/) ----
@app.route("/", endpoint="home")
def home():
    return render_template("home.html")

# ---- GALLERY (/gallery) ----
@app.route("/gallery", endpoint="gallery")
def gallery():
    # si no usas BD aún, pasa una lista vacía
    messages = []
    return render_template("gallery.html", messages=messages)

# Alias en español si quieres /galeria → redirige a /gallery
@app.route("/galeria")
def galeria_alias():
    return redirect(url_for("gallery"))

# ---- FORM (/submit) ----
@app.route("/submit", methods=["GET", "POST"], endpoint="submit")
def submit():
    if request.method == "POST":
        to_name = (request.form.get("to_name") or "").strip()
        body    = (request.form.get("body") or "").strip()
        color   = (request.form.get("color") or "#f0f0f0").strip()
        if not to_name or not body:
            flash("Please fill in both 'To' and 'Message'.")
            return redirect(url_for("submit"))
        flash("Saved!")                     # aquí guardarías en la BD
        return redirect(url_for("thanks"))
    return render_template("submit.html")

# ---- THANKS (/thanks) ----
@app.route("/thanks", endpoint="thanks")
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)
