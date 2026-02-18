from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    
    #Consumo del ENDPOINT DEL PUERTO 8000 EN DOCKER 
    response = requests.get("http://localhost:8000/v1/Usuarios")
    json_response = response.json()
    

    usuarios = json_response["data"]

    return render_template("index.html", usuarios=usuarios)

if __name__ == '__main__':
    app.run(port=5020, debug=True)
    
    
#CORRE EL PROGRMA
#cd frontFlask
#python3 app.py
#http://localhost:5020