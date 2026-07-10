from flask import Flask, render_template, request, redirect, url_for, flash, session
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.job import Job
from models.interview import Interview
from datetime import datetime
from utils.validation import is_valid_password
from sqlalchemy import desc
#from flask_migrate import Migrate
from utils.job_status import sync_job_status
from utils.auth import get_current_user





app = Flask(__name__)
app.secret_key = "flask-dev-1029"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.context_processor
def inject_user():
    return {
        "current_user": get_current_user()
    }

with app.app_context():
   db.create_all()



#migrate = Migrate(app, db)




def login_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper

@app.route("/dashboard")
@login_required
def dashboard():
    current_user = get_current_user()

    user_jobs = Job.query.filter_by(user_id=current_user.id)
    
    total_jobs = user_jobs.count()
    total_applied = Job.query.filter_by(user_id=current_user.id,status="Applied").count()
    interview_pipeline = user_jobs.filter_by(status="Interview").count()
    total_offers = user_jobs.filter_by(status="Offer").count()
    total_rejected = user_jobs.filter_by(status="Rejected").count()

    today = datetime.now().date()
    
    upcoming_interviews = (
        Interview.query
        .join(Job)
        .filter(Job.user_id == current_user.id) 
        .filter(Interview.interview_date>= today)
        .filter(Interview.status == "Scheduled")
        .order_by(
            Interview.interview_date.asc(),
            Interview.interview_time.asc()
        )
        .limit(5)
        .all()


    )

    recent_jobs = (
        user_jobs
        .order_by(Job.date_applied.desc())
        .limit(5)
        .all()
    )




    return render_template("dashboard.html",
                           total_jobs=total_jobs,
                           Applied = total_applied,
                           active_interviews=interview_pipeline,
                           total_offers=total_offers,
                           total_rejected=total_rejected,
                           upcoming_interviews=upcoming_interviews,
                           recent_jobs = recent_jobs
                           )



@app.route("/signup", methods = ["Get","POST"])
def signup():
    """
    Register a new user.

    GET:
        Displays signup form.

    POST:
        Validates data,
        hashes password,
        stores user in database.
    """

    #If user already logged in -- Skip Signup page
    if "user_id" in session:
        flash("Already logged in!")
        return redirect(url_for("dashboard"))


    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        #Validation 1 - Password match validation
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("signup"))
        
        #Validation 2 - Password Strength Validation
        if not is_valid_password(password):
            flash("Passwords must be atleast 8 characters and contain letters and numbers.")
            return redirect(url_for("signup"))



        #Validation 3 - Unique Username Validation
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already taken. Please choose another one.")
            return redirect(url_for("signup"))
        
        #Validation 4 -- Unique Email Validation
        existing_user = User.query.filter_by(email = email).first()

        if existing_user:
            flash("Email already registered")
            return redirect(url_for("signup"))
        
        hashed_password = generate_password_hash(password)

        new_user = User(
            username = username,
            email = email,
            password_hash = hashed_password
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!")
            return redirect(url_for("login"))
        
        except Exception:
            db.session.rollback()

            flash("Something went wrong while creating your account.")
            return redirect(url_for("signup"))
        
    return render_template("signup.html")
                            


@app.route("/login", methods = ["GET", "POST"])
def login():
    '''
    Authenticate existing users.
    '''

    #If user already logged in -- Skip login page
    if "user_id" in session:
        flash("Already logged in!")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email = email).first()

        if not user:
            flash("Account not found.")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.password_hash, password):
            flash("Incorrect password")
            return redirect(url_for("login"))
        
        session["user_id"] = user.id
        print(session)

        flash("Login Successful")

        return redirect(url_for("dashboard"))
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


@app.route("/")
def home():

    # Already logged in?
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("index.html")

@app.route("/add-job", methods = ["GET", "POST"])
@login_required
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
            notes = notes,
            user_id = get_current_user().id
        )


        db.session.add(new_job)
        db.session.commit()

        return redirect(url_for("view_jobs"))
    return render_template("add_job.html")

@app.route("/view-jobs")
@login_required
def view_jobs():

    current_user = get_current_user()

    jobs = Job.query.filter_by(user_id = current_user.id).all()

    return render_template("view_jobs.html", jobs = jobs)

@app.route("/edit-job/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):

    job = Job.query.filter_by(
        id=job_id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":

        job.company = request.form["company"].strip()

        job.role = request.form["role"].strip()

        job.status = request.form["status"]

        date_str = request.form["date_applied"]
        job.date_applied = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        job.notes = request.form.get("notes")

        db.session.commit()

        flash("Job updated successfully.")

        return redirect(url_for("view_jobs"))

    return render_template(
        "edit_job.html",
        job=job
    )

@app.route("/delete-job/<int:job_id>", methods = ["POST"])
@login_required
def delete_job(job_id):

    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    return redirect(url_for("view_jobs"))


@app.route("/job/<int:job_id>/add-interview", methods = ["GET", "POST"])
@login_required
def add_interview(job_id):
    job = Job.query.filter_by(id = job_id, user_id = session["user_id"]).first()
    is_final = request.form.get("is_final_round") == "on"

    if is_final:
        Interview.query.filter_by(
            job_id=job.id,
            is_final_round=True
        ).update({"is_final_round": False})

    if not job:
        return "Unauthorized or Job not found", 403
    
    if request.method == "GET":
        return render_template("add_interview.html", job = job)
    
    if request.method == "POST":

        interview = Interview(
            job_id = job.id,
            interview_date = datetime.strptime(request.form["interview_date"], "%Y-%m-%d").date(),
            interview_time = datetime.strptime(request.form["interview_time"], "%H:%M").time(),
            interview_type = request.form["interview_type"],
            round_number = request.form["round_number"],
            status = request.form["status"],
            result = request.form["result"],
            is_final_round=is_final,
            notes = request.form.get("notes")

        )

        db.session.add(interview)

        db.session.commit()

        sync_job_status(job)
        db.session.commit()

        return redirect(url_for("home"))

@app.route("/edit-interview/<int:id>", methods = ["GET", "POST"])
@login_required
def edit_interview(id):

    interview = (
    Interview.query.join(Job).filter(
        Interview.id == id,
        Job.user_id == session["user_id"]
    ).first_or_404()
    )
    job = interview.job

    is_final = request.form.get("is_final_round") == "on"

    if is_final:
        Interview.query.filter(
            Interview.job_id == job.id,
            Interview.id != interview.id,
            Interview.is_final_round == True
        ).update(
            {"is_final_round": False},
            synchronize_session=False
        )

    if request.method == "POST":
        # Date
        date_str = request.form.get("interview_date")
        if date_str:
            interview.interview_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Time
        time_str = request.form.get("interview_time")
        if time_str:
            try:
                interview.interview_time = datetime.strptime(time_str, "%H:%M").time()
            except ValueError:
                interview.interview_time = datetime.strptime(time_str, "%H:%M:%S").time()

        intr_type= request.form.get("interview_type")
        if intr_type:
             interview.interview_type = intr_type
        round_num = request.form.get("round_number")
        if round_num:
            interview.round_number = int(round_num)
        int_status = request.form.get("status")
        if int_status:
            interview.status = int_status

        inter_result=request.form.get("result")
        if inter_result:
            interview.result = inter_result

        interview.is_final_round = is_final

        interview.notes = request.form.get("notes")


        db.session.commit()

        sync_job_status(interview.job)
        db.session.commit()

        return redirect(url_for("view_jobs"))
    return render_template("edit_interview.html", interview= interview)

@app.route("/delete-interview/<int:id>", methods=["POST"])
@login_required
def delete_interview(id):

    interview = Interview.query.get_or_404(id)

    job = interview.job          # Save the parent job first

    db.session.delete(interview)

    # Recalculate status based on remaining interviews
    sync_job_status(job)

    db.session.commit()

    flash("Interview deleted successfully.")

    return redirect(url_for("view_jobs"))



if __name__ == "__main__":
    app.run(debug=True)