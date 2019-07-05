import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name") or not request.form.get("gender") or not request.form.get("exampleRadios"):
        return render_template("error.html")
    # writes form values into survey.csv
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("gender"), request.form.get("exampleRadios"), request.form.get("dietrestriction")))
    file.close()
    # redirects user to /sheet if validations
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    persons = list(reader)
    return render_template("table.html", persons=persons)
