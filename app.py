from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from constantes.preguntas import PREGUNTAS
from modelo.prueba_tensorflow import modelo_cangrejo

app = Flask(__name__)
#secret key para la sesion y el guardado de la informacion
app.secret_key = '1234566789'

#ruta principal
@app.route('/')
def index():
    if 'pregunta_actual' in session:
        session['pregunta_actual'] = 0
        session['respuestas'] = []
    return render_template('index.html')

#ruta de quiz para las preguntas
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    #si es la primera pregunta crea la sesion e inicializa la preguntas
    if 'pregunta_actual' not in session:
        session['pregunta_actual'] = 0
        session['respuestas'] = []
        
    #toma la posicion de la pregunta actual
    indice = session['pregunta_actual']

    if request.method == 'POST':
        #toma el valor de la seleccion
        seleccion = request.form.get('seleccionado')
        
        try:
            #lo intenta convertir en int para la comparacion
            recibido = int(seleccion)
            if recibido == 1:
                #si presiona el primer boton el csv se guarda 1,0
                session['respuestas'].append(0)
                session['respuestas'].append(1)
            else:
                #si presiona el segundo guarda un registro 0,1
                session['respuestas'].append(1)
                session['respuestas'].append(0)
            session['pregunta_actual'] = indice + 1
        except(ValueError, TypeError):
            print("error" + str(ValueError) + str(TypeError))
            return redirect(url_for('quiz'))
                
                
            
        #condicional para ultima pregunta
        if indice < len(PREGUNTAS):
            return redirect(url_for('quiz'))
        else:
            session.pop('pregunta_actual')
            return redirect(url_for('resultados'))
    else:

        if indice < len(PREGUNTAS):
            
            actual = PREGUNTAS[indice]
            return render_template('quiz.html', pregunta=actual, num_pregunta=indice + 1, total_preguntas=len(PREGUNTAS))

        else:
            session.pop('pregunta_actual')
            return redirect(url_for('resultados'))

#ruta para mostrar el resultado
@app.route('/resultados')
def resultados():
    #primero toma las respuestas guardadas en la sesion en una lista
    respuestas_guardadas = session.get('respuestas', [])
    #luego las para a una variable resultado y hace la llamada al modelo
    resultado = modelo_cangrejo(respuestas_guardadas)
    return render_template('result.html', resultado = resultado)

@app.route('/cangrejos', methods=['POST'])
def cangrejos():
    if request.is_json:
        try:
            data = request.get_json()
            arrayToModel = data.get('elementos')
            cangrejo_encontrado = modelo_cangrejo(arrayToModel)

            return jsonify({"mensaje": "Array procesado",
                        "cangrejo":cangrejo_encontrado}),200
        except Exception:
            return jsonify({"error":"error en json"}),500
    else:
        return jsonify({"error":"error al detectar"}),400




if __name__ == '__main__':
    app.run(debug=True)