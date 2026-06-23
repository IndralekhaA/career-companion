from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models.job import Job
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-job", methods = ["GET", "POST"])
def add_job():

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        date_str = request.form["date_applied"]
        date_applied = datetime.strptime(date_str, "%Y-%m-%d").date()
        notes = request.form["notes"]

        new_job = Job(
            company = company,
            role = role,
            status = status,
            date_applied = date_applied,
            notes = notes
        )
        print(date_applied)
        print(type(date_applied))

        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add_job.html")

@app.route("/jobs")
def view_jobs():

    jobs = Job.query.all()

    return render_template("jobs.html", jobs = jobs)

if __name__ == "__main__":
    app.run(debug=True)