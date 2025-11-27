from flask import Flask, request
import pandas as pd
import pickle
from sqlalchemy import create_engine

app = Flask(__name__)

churro = "postgresql://postgre_new_y2a5_user:eb6u0V5hfP0Yi0YWodHBTSVrgwjjVieM@dpg-d4k3bf6uk2gs73fjq940-a.oregon-postgres.render.com/postgre_new_y2a5"
engine = create_engine(churro)

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
    df = pd.DataFrame({"sex":[sex], "age":[age], "clase":[clase], "predicción":[survived]})
    df.to_sql("predictions", engine, if_exists = "append", index=False)
    return f"Para un pasajero de {age} años, sexo {sex} y clase {clase}, el modelo predice: {survived}"
if __name__ == '__main__':
    app.run(debug=True)