import os
from flask import Flask, render_template, request
import git_operations
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import conf

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        item = request.form['item']
        notes = request.form['notes']
        if notes == '':
            notes = "None"
        print(f"La variable notes es: {notes}")
        email = request.form['email']
        
        body =f'Hi {name},\n\nYour order of: {item} Has been successfully registered. Here are some places recomendations near you: \n' + "\n".join(conf.food[item])
        send_email(email,name + "Order Summary", body)
    
        # Crear una lista con los datos a guardar
        data = [name, item, notes, email]
        # Git Actions
        if os.path.exists("..\\web_app"):
            os.system('cmd /c "rmdir /s /Q ..\\web_app"')
        git_operations.clone_repo( "../web_app", "github.com/AMendez-SBSSecurity/DevSecOps-WebApp-Demo.git")
        # Abrir el archivo CSV en modo de escritura
        with open('..\\web_app\\static\\data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Escribir los datos en el archivo CSV
            writer.writerow(data)
        git_operations.push_changes("..\\web_app")
        if os.path.exists("..\\web_app"):
            os.system('cmd /c "rmdir /s /Q ..\\web_app"')
        # Aquí puedes hacer lo que necesites con los datos del formulario
        
    return render_template('form.html')
@app.route('/results')
def show_results():
    with open('datos.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    return render_template('results.html', data=data)

EMAIL_FROM = "andresmendez9896@gmail.com"
EMAIL_TO_1 = "andresmendez9896@gmail.com"

def send_email(email, subject, body):
    receivers = [EMAIL_TO_1, email]
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = ', '.join(receivers)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Use your SMTP server and port
        server.starttls()
        server.login("andresmendez9896@gmail.com","habwnknmrartdvuf")
        server.sendmail(EMAIL_FROM, receivers, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


if __name__ == '__main__':
    app.run(debug=True)