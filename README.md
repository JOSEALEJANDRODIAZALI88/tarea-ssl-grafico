1. Descripcion general del proyecto

Este proyecto implementa un pequeño panel de tipo de cambio del dolar:

La base de datos datos.db contiene alrededor de 20 registros con:

fecha (cadena)

tipo_cambio (real)

El backend Flask:

Lee la tabla tipo_cambio.

Expone una API simple en /data que devuelve JSON.

Renderiza una vista en / con un grafico de lineas.

Todo funciona sin acceso a internet, porque:

La base de datos esta embebida (SQLite).

Chart.js se sirve desde static/chart.min.js.

HTTPS se habilita mediante certificados autofirmados generados con OpenSSL.

2. Tecnologias utilizadas

Python 3

Flask (servidor web)

SQLite (base de datos local)

Chart.js (graficos en JavaScript usando archivo local static/chart.min.js)

OpenSSL (generacion de server.key y server.crt)

Git / GitHub (control de versiones y repositorio remoto)

3. Requisitos previos (Windows)

Antes de replicar el proyecto en otra maquina se necesita:

Python 3

Descargar desde la pagina oficial.

En el instalador marcar: Add Python to PATH.

Git for Windows

Provee git, Git Bash y openssl.

(Opcional) IDE

PyCharm o VS Code para editar el proyecto.

Verificaciones rapidas:

python --version
git --version


En Git Bash:

openssl version

4. Clonado del repositorio

En la maquina de destino:

cd C:\Users\TU_USUARIO
git clone https://github.com/JOSEALEJANDRODIAZALI88/tarea-ssl-grafico.git
cd tarea-ssl-grafico


Estructura esperada:

tarea-ssl-grafico/
  app.py (o main.py segun la version)
  init_db.py
  templates/
    index.html
  static/
    chart.min.js
  .gitignore
  README.md
  ...

5. Entorno virtual e instalacion de dependencias

Para aislar las dependencias en la maquina de destino:

cd C:\Users\TU_USUARIO\tarea-ssl-grafico
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask


El prompt mostrara (venv) cuando el entorno virtual este activo.

Para desactivar el entorno virtual:

deactivate

6. Generacion y estructura de la base de datos

El archivo init_db.py crea y rellena la base SQLite datos.db.

Desde la raiz del proyecto:

.\venv\Scripts\Activate.ps1
python init_db.py


Logica principal del script:

Eliminar la tabla tipo_cambio si existe.

Crear la tabla:

CREATE TABLE tipo_cambio (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fecha TEXT NOT NULL,
  tipo_cambio REAL NOT NULL
);


Insertar aproximadamente 20 filas con fechas consecutivas y valores de tipo de cambio simulados.

Resultado: archivo datos.db en la raiz del proyecto, listo para ser usado por Flask.

7. Logica del backend (Flask + SQLite)
7.1. Funcion de acceso a datos

En el archivo principal (app.py o main.py) se usa una funcion de este estilo:

def get_data():
    conn = sqlite3.connect("datos.db")
    cur = conn.cursor()
    cur.execute("SELECT fecha, tipo_cambio FROM tipo_cambio ORDER BY fecha")
    rows = cur.fetchall()
    conn.close()
    puntos = []
    for fecha, valor in rows:
        puntos.append({"x": fecha, "y": valor})
    return puntos


Comportamiento:

Abre la base de datos datos.db.

Ejecuta una consulta ordenando por fecha.

Construye una lista de objetos con claves x (fecha) e y (tipo de cambio) para poder serializar en JSON.

7.2. Rutas principales de Flask

Rutas expuestas por la aplicacion:

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(get_data())


GET / entrega la plantilla HTML con el grafico.

GET /data entrega los datos en JSON, consumidos desde el frontend mediante fetch.

8. Frontend y grafico con Chart.js
8.1. Plantilla HTML (index.html)

El archivo templates/index.html define:

Un diseño tipo dashboard:

Titulo general del panel.

Subtitulo explicativo.

Una tarjeta central donde se incrusta el grafico.

Un <canvas id="grafico"> donde se dibuja la serie.

Estilos CSS integrados que dan:

Fondo oscuro.

Tarjeta con bordes redondeados y sombras.

Tipografia clara y jerarquia visual.

Ejemplo de inclusion de Chart.js y logica basica:

<script src="/static/chart.min.js"></script>
<script>
  fetch("/data")
    .then(function(r){ return r.json(); })
    .then(function(puntos){
      var etiquetas = puntos.map(function(p){ return p.x; });
      var valores = puntos.map(function(p){ return p.y; });

      var ctx = document.getElementById("grafico").getContext("2d");
      new Chart(ctx, {
        type: "line",
        data: {
          labels: etiquetas,
          datasets: [{
            label: "Tipo de cambio del dolar",
            data: valores
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    });
</script>

8.2. Carga local de Chart.js

Chart.js se almacena localmente en:

static/chart.min.js


y se referencia en la plantilla con:

<script src="/static/chart.min.js"></script>


De esta forma, la aplicacion no necesita acceder a ningun CDN en internet para renderizar el grafico; todo se sirve desde el propio servidor Flask.

9. Ejecucion en HTTP (modo basico)

Con entorno virtual activo y base de datos creada:

cd C:\Users\TU_USUARIO\tarea-ssl-grafico
.\venv\Scripts\Activate.ps1
python app.py


o

python main.py


(segun el nombre del archivo principal del proyecto).

Por defecto, Flask escucha en:

http://127.0.0.1:5000

http://localhost:5000

Comprobaciones:

Vista principal
http://localhost:5000/
→ Se debe mostrar el panel con el grafico de tipo de cambio (linea sobre el tiempo).

API de datos
http://localhost:5000/data
→ Se debe mostrar JSON con listas de objetos, por ejemplo:

[
  {"x": "2025-01-01", "y": 6.9},
  {"x": "2025-01-02", "y": 6.91}
]


Si ambas rutas funcionan, la parte funcional de la aplicacion (sin SSL) ya esta replicada correctamente.

10. Habilitacion de HTTPS con OpenSSL

Para cumplir con la parte de SSL/TLS, se usan certificados autofirmados generados con openssl (incluido en Git Bash).

10.1. Generar certificados autofirmados

Desde Git Bash, en la carpeta del proyecto:

cd /c/Users/TU_USUARIO/tarea-ssl-grafico
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt


Durante el asistente de openssl completar:

Country Name: por ejemplo BO.

State or Province Name, Locality Name, Organization Name: opcionales.

Common Name: escribir localhost (importante para pruebas locales).

Email Address: opcional.

Esto generara dos archivos en la raiz:

server.key → clave privada del servidor.

server.crt → certificado autofirmado del servidor.

10.2. Ejecutar Flask en HTTPS

En el archivo principal (app.py o main.py) se debe configurar:

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8443, ssl_context=("server.crt", "server.key"))


Con esto:

El servidor expone HTTPS en el puerto 8443.

Usa server.crt y server.key para establecer el canal cifrado.

Para levantar la aplicacion en HTTPS:

cd C:\Users\TU_USUARIO\tarea-ssl-grafico
.\venv\Scripts\Activate.ps1
python app.py


Luego, en el navegador:

https://localhost:8443/


El navegador mostrara una advertencia de seguridad porque el certificado es autofirmado y no proviene de una autoridad certificadora.
En un entorno de laboratorio se puede continuar pulsando “Avanzado / Continuar”.

La pagina que se muestra es el mismo panel con el grafico, ahora servido sobre HTTPS.

11. Resumen general para replicacion

Para replicar completamente el proyecto en cualquier maquina Windows:

Clonar el repositorio desde GitHub:

git clone https://github.com/JOSEALEJANDRODIAZALI88/tarea-ssl-grafico.git


Crear y activar un entorno virtual, e instalar Flask:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install flask


Generar la base de datos local ejecutando:

python init_db.py


Ejecutar en HTTP con:

python app.py


y verificar:

http://localhost:5000/ (vista)

http://localhost:5000/data (JSON)

Generar certificados SSL con OpenSSL en Git Bash:

openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt


Configurar Flask para HTTPS:

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8443, ssl_context=("server.crt", "server.key"))


Ejecutar en HTTPS y acceder a:

https://localhost:8443/


Explicar al docente que:

El grafico se alimenta de una tabla local con aproximadamente 20 registros de tipo de cambio.

El proyecto no depende de internet (base de datos y libreria de graficos son locales).

La comunicacion entre cliente y servidor esta cifrada usando SSL/TLS, con certificados generados mediante OpenSSL.

Con estos pasos, cualquier persona puede replicar el entorno y comprobar el funcionamiento completo de la aplicacion tal como fue diseñada para la tarea