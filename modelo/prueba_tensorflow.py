import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

##----------------------------------------------Funcion para llamar al modelo ya guardado
def modelo_cangrejo(respuestas= [1,0,1,0,0,1,1,0,1,0,1,0,1,0]):
    prueba = pd.read_csv("flask/modelo/cangrejos.csv")

    ruta_guardada = "flask/modelo/cangrejos_modelo_guardado.keras"
    try:
        saved_model = tf.keras.models.load_model(ruta_guardada)
    except Exception as e:
        print("fallo")
    test = np.array(respuestas, dtype=float)
    test = test.reshape(1, -1)

    le = LabelEncoder()
    le.fit(prueba['Especie'].astype(str))

    prediccion = saved_model.predict(test)

    clase_predicha = np.argmax(prediccion[0])
    especie_predicha = le.inverse_transform([clase_predicha])[0]

    print()
    print("\n----------------------------------------------")
    print(f"La especie de cangrejo clasificada es:"+  str(especie_predicha))
    print("----------------------------------------------")
    return str(especie_predicha)

#--------------------------------------------------------------Funcion para el entrenado del modelo
def entrenar_modelo_cangrejo(respuestas= [1,0,1,0,0,1,1,0,1,0,1,0,1,0]):
    #valor inicial neopisosoma neglectum
    #primero lee el csv
    prueba = pd.read_csv("flask/modelo/cangrejos.csv")
    #la convierte en una lista de tipo numpy
    test = np.array(respuestas, dtype=float)
    test = test.reshape(1, -1)

    y = prueba['Especie']
    x = prueba[['superficie_lisa','superficie_irregular','antena_lisa','antena_aserrado','maxilipedos_lisos','maxilipedos_con_surcos','quelipedos_desiguales','quelipedos_iguales','caparazon_cuadrado','caparazon_rectangular','telson_siete','telson_cinco','si_pleopodo','no_pleopodo']]

    x = x.apply(pd.to_numeric,errors='coerce').astype(float)

    le = LabelEncoder()
    y = le.fit_transform(y.astype(str))
    num_clases = len(le.classes_)

    oculta = tf.keras.layers.Dense(32, activation='relu', input_shape=[x.shape[1]])
    segundaOculta = tf.keras.layers.Dense(32, activation='relu')
    salida = tf.keras.layers.Dense(num_clases, activation='softmax')
    modelo = tf.keras.Sequential([oculta,segundaOculta, salida])

    modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    #modelo a las 300-500 iteraciones el entrenamiento no avanza 
    print("Comenzando entrenamiento...")
    historial = modelo.fit(x, y, epochs=600, verbose=False)
    print("Modelo entrenado!")
    ruta = "flask/modelo/cangrejos_modelo_guardado.keras"
    modelo.save(ruta)
    

    plt.xlabel('# Epoca')
    plt.ylabel('Magnitud de perdida') 
    plt.plot(historial.history['loss'])
    plt.show()


    prediccion = modelo.predict(test)

    clase_predicha = np.argmax(prediccion[0])
    especie_predicha = le.inverse_transform([clase_predicha])[0]

    print()
    print("\n----------------------------------------------")
    print(f"La especie de cangrejo clasificada es:"+  str(especie_predicha))
    print("----------------------------------------------")

