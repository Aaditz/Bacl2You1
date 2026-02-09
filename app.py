from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from config import (
    MAIL_SERVER,
    MAIL_PORT,
    MAIL_USE_TLS,
    MAIL_USERNAME,
    MAIL_PASSWORD,
    UNIVERSITY_EMAIL_DOMAIN
)
from models import create_user, verify_user, user_exists
from db import init_db, get_db_connection

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret123"

# =========================
# MAIL CONFIG
# =========================
app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_TLS"] = MAIL_USE_TLS
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

mail = Mail(app)

# =========================
# EMAIL VERIFICATION MAIL
# =========================
def send_verification_email(email, token):
    verify_link = url_for("verify_email", token=token, _external=True)

    msg = Message(
        subject="Back2You – Verify Your Email",
        sender=MAIL_USERNAME,
        recipients=[email]
    )

    msg.body = f"""
Hello,

Thank you for registering on Back2You.

Please verify your email by clicking the link below:
{verify_link}

If you did not register, please ignore this email.

Regards,
Back2You Team
"""
    mail.send(msg)

# =========================
# REGISTER
# =========================
@app.route("/", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # University email check
        if not email.endswith(UNIVERSITY_EMAIL_DOMAIN):
            flash("Only university email allowed", "error")
            return redirect(url_for("register_page"))

        # User exists check
        if user_exists(email):
            flash("User already exists. Please login.", "error")
            return redirect(url_for("login"))

        hashed_password = generate_password_hash(password)

        token = create_user(email, hashed_password)
        send_verification_email(email, token)

        flash("Registration successful! Please verify your email.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in → dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        result = verify_user(email, password)

        if result == "NOT_VERIFIED":
            flash("Please verify your email before logging in", "error")

        elif result is not None:
            session["user_id"] = result["id"]
            session["user_email"] = result["email"]

            # USERNAME = EMAIL PREFIX IN CAPS
            session["username"] = result["email"].split("@")[0].upper()

            return redirect(url_for("dashboard"))

        else:
            flash("Invalid email or password", "error")

    return render_template("login.html")

# =========================
# DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        email=session["user_email"]
    )

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# EMAIL VERIFICATION
# =========================
@app.route("/verify/<token>")
def verify_email(token):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE verification_token = ?",
        (token,)
    )
    user = cursor.fetchone()

    if not user:
        flash("Invalid or expired verification link", "error")
        conn.close()
        return redirect(url_for("login"))

    cursor.execute(
        "UPDATE users SET verified = 1, verification_token = NULL WHERE id = ?",
        (user["id"],)
    )

    conn.commit()
    conn.close()

    flash("Email verified successfully. You can now login.", "success")
    return redirect(url_for("login"))

# =========================
# APP START
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
