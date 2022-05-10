from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
import csv
from datetime import datetime
import os


now = datetime.now()
date = now.date()
hour = now.hour
minute = now.minute
tiden = f"{hour}:{minute}"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asgthgtrhtrw34dt45y452d4q245y52zsty46yu357du35ud3t5ryu56ud5e'
Bootstrap(app)


class ReportingData(FlaskForm):
    original_email = TextAreaField("email", validators=[DataRequired()])
    customer = StringField("Kund", validators=[DataRequired()])
    client = StringField("Beställare", validators=[DataRequired()])
    hardware = StringField("Hårdvara")
    service = StringField("Tjänst", validators=[DataRequired()])
    time_spent = StringField("Tid", validators=[DataRequired()])
    worker = SelectField("Utförare", choices=[("Lars Eriksson", "Lars Eriksson"), ("Jan Tolshagen", "Jan Tolshagen"),
                                              ("Jens Åberg", "Jens Åberg")])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    try:
        with open(f"static/data/{date}.csv") as file:

                csv_data = csv.reader(file, delimiter=',')
                number_of_rows = 0
                for row in csv_data:
                    number_of_rows += 1
    except FileNotFoundError:
        return render_template("start_index.html")
    return render_template("index.html", number_of_rows=number_of_rows)


@app.route("/submit", methods=["POST", "GET"])
def data_submission():
    form = ReportingData()
    if request.method == "POST" and form.validate_on_submit():
        print("True")
        data_gathered = [tiden, form.original_email.data, form.customer.data, form.client.data, form.hardware.data,
                         form.service.data, form.time_spent.data, form.worker.data]
        with open(f"static/data/{date}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_gathered)


        return redirect("data")
    return render_template('submit.html', form=form)


@app.route("/data")
def data_viewing():
    try:
        with open(f"static/data/{date}.csv") as file:

                csv_data = csv.reader(file, delimiter=',')
                list_of_rows = []
                for row in csv_data:
                    list_of_rows.append(row)
    except FileNotFoundError:
        return render_template("data_not_found.html")

    return render_template("data.html", rows=list_of_rows)

@app.route("/download")
def download():
    try:
        with open(f"static/data/{date}.csv") as file:

                csv_data = csv.reader(file, delimiter=',')
                data = []
                for row in csv_data:
                    data.append(f"Registrerat: {row[0]}\n\nFöretag: {row[2]}\nBeställare: {row[3]}\nHårdvara: {row[4]}\nTjänst: {row[5]}\nTid: {row[6]} \nUtförare: {row[7]}\n\n##\n\n")
                try:
                    return send_file(f"static/data/{date}_result.txt", as_attachment=True)
                except FileNotFoundError:
                    with open(f"static/data/{date}_result.txt", 'a') as data_file:
                        for d in data:
                            data_file.write(d)
        return send_file(f"static/data/{date}_result.txt", as_attachment=True)

    except FileNotFoundError:
        return render_template("data_not_found.html")


if __name__ == "__main__":
    app.run(debug=True)
