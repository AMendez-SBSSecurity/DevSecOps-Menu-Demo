import os
from flask import Flask, render_template, request
import git_operations
import csv


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        item = request.form['item']
        notes = request.form['notes']
        
        # Crear una lista con los datos a guardar
        data = [name, item, notes]
        # Git Actions
        if os.path.exists("./web_app"):
            os.system('cmd /c "rmdir /s /Q web_app"')
        git_operations.clone_repo( "web_app", "github.com/AMendez-SBSSecurity/DevSecOps-WebApp-Demo.git")
        # Abrir el archivo CSV en modo de escritura
        with open('./web_app/static/data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Verificar si esta vacio y si lo está, lo setea en none
            for i in range(len(data)):
                if data[i] == '':
                    data[i] = None
            # Escribir los datos en el archivo CSV
            writer.writerow(data)
        git_operations.push_changes("web_app")
        if os.path.exists("./web_app"):
            os.system('cmd /c "rmdir /s /Q web_app"')
        # Aquí puedes hacer lo que necesites con los datos del formulario
        
    return render_template('form.html')
@app.route('/results')
def show_results():
    with open('datos.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    return render_template('results.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)