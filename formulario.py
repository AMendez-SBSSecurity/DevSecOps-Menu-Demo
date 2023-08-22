from flask import Flask, render_template, request
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
        
        # Abrir el archivo CSV en modo de escritura
        with open('datos.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Escribir los datos en el archivo CSV
            writer.writerow(data)
        
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