from flask import Flask, render_template, request, redirect, url_for, session
from metodos.metodo_grafico.metodografico import metodo_grafico
from constantes.preguntas import PREGUNTAS

app = Flask(__name__)
app.secret_key = '1234566789'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    respuestas = []
    if 'pregunta_actual' not in session:
        session['pregunta_actual'] = 0
        session['respuestas'] = []
        
    
    indice = session['pregunta_actual']

    if request.method == 'POST':
        seleccion = request.form.get('seleccionado')
        try:
            recibido = int(seleccion)
            if recibido == 1:
                session['respuestas'].append(0)
                session['respuestas'].append(1)
            else:
                session['respuestas'].append(1)
                session['respuestas'].append(0)
        except (ValueError, TypeError):
            print("Error al convertir la selección a entero.")
        if indice < len(PREGUNTAS):
            session['pregunta_actual'] = indice + 1
            actual = PREGUNTAS[indice]
            return render_template('quiz.html', pregunta=actual, num_pregunta=indice + 1, total_preguntas=len(PREGUNTAS))

        else:
            session.pop('pregunta_actual')
            return redirect(url_for('resultados'))
    return render_template('quiz.html', pregunta=PREGUNTAS[indice], num_pregunta=indice + 1, total_preguntas=len(PREGUNTAS))

@app.route('/resultados')
def resultados():
    respuestas_guardadas = session.get('respuestas', [])
    # Aquí puedes calcular y mostrar los resultados usando session['respuestas']
    return render_template('result.html', respuestas=respuestas_guardadas)

@app.route('/grafico', methods=['POST'])
def graphic_method():
    metodo_grafico()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)