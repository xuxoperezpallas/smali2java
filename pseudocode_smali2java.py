import os
import re
import sys
import openai


def create_directories(path):
    try:
        os.makedirs(path)
        print("Se crearon los directorios con éxito en", path)
    except OSError as e:
        print("Error al crear los directorios:", e)

def split_methods(filename):
    with open(filename, 'r') as f:
        smali = f.read()
        methods = smali.split('.method')
        # Eliminar el primer elemento, que es la cabecera del archivo
        methods.pop(0)
        # Agregar '.method' al principio de cada método
        methods = [f".method{method}" for method in methods]
        # Agregar la etiqueta de fin del archivo al final de la lista
        methods.append('.end file')
    return methods

def escape_special_characters(text):
    return re.escape(text)

def access_directory(path):
    try:
        os.chdir(path)
        print("Se accedió a la ruta", path, "con éxito")
    except OSError as e:
        print("Error al acceder a la ruta:", e)


var1 = split_methods(sys.argv[1])


openai.api_key = os.getenv("OPENAI_API_KEY")

posicion_barra = sys.argv[1].rfind("/")
nueva_cadena = "./sources/" + sys.argv[1][:posicion_barra]

create_directories(nueva_cadena)

open("./sources/" + sys.argv[1], "w")

for i, part in enumerate(var1):
    var2 = escape_special_characters(part)
    response = openai.Completion.create(
  model="code-davinci-002",
  prompt="##### Translate this function  from Smali into Java  and removed the endFile method\n### Smali\n    \n" + var2 + "\n  \n### Java",
  temperature=0,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["###"]
)
    with open("./sources/" + sys.argv[1], "a") as archivo:
        # Agregar el texto al final del archivo
        archivo.write(response.choices[0].text)
