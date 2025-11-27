from flask import Flask, request
import pandas as pd
import pickle

app = Flask(__name__)

with open("model.pkl","rb") as f:
    read_rf = pickle.load(f)


@app.route('/', methods=['GET'])
def hola():
    return "Hola, Mundo!"

@app.route('/predict', methods=['GET'])
def predict():
    age = request.args.get("age", None)
    sex = request.args.get("sex", None)
    clase = request.args.get("clase", None)

    if age is None or sex is None or clase is None:
        "Faltan argumentos"

    if not(age.isnumeric() and sex.isnumeric() and clase.isnumeric()):
        return "¡Números enteros!"
    

    
    survived = "Sobrevive" if read_rf.predict([[age, sex, clase]])[0] == 1 else "No Sobrevive"
    return f"Para un pasajero de {age} años, sexo {sex} y clase {clase}, el modelo predice: {survived}"
if __name__ == '__main__':
    app.run(debug=True)