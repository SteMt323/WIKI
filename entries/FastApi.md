# Backend con Python y FastAPI



Este repositorio contiene un proyecto de backend desarrollado en Python utilizando el framework FastAPI. A continuacion, se detallan los pasos para configurar un servidor local con un entorno virtual.



## Documentaciones



Se presentara sitios con la documentacion necesaria



### FastApi Documentation 

- [FastApi - Main Page](https://fastapi.tiangolo.com/)

- [FastApi - Primeros Pasos](https://fastapi.tiangolo.com/es/tutorial/first-steps/)



### AutoDocumentation APIS 

- [Swagger](https://github.com/swagger-api/swagger-ui)

- [ReDocs](https://github.com/Redocly/redoc)



### HTTP status code

- [Mozilla - Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)



## Configuracion del Entorno Virtual



Para levantar el servidor local, se necesita crear y activar un entorno virtual. Sigue los pasos a continuacion:



### Paso 1: Crear el entorno virtual



Ejecute el siguiente comando dentro del directorio de su proyecto:



```bash

python -m venv venv

```



Esto creara una carpeta llamada `venv` dentro del directorio donde se ejecuto el comando, que servira como el entorno virtual.



### Paso 2: Activar el entorno virtual



Dependiendo del sistema operativo y la terminal que estas utilizando, usa uno de los siguientes comandos:



- **PowerShell (Windows):**

  ```powershell

  .\venv\Scripts\Activate

  ```

- **CMD (Windows):**

  ```cmd

  venv\Scripts\activate

  ```



Cuando el entorno virtual esta activado, el prompt de la terminal cambiara para reflejarlo, por ejemplo:



```

(venv) PS C:\Users\username\OneDrive\Desktop\Python-Web>

```



### Paso 3: Instalar las dependencias



Ejecute el siguiente comando para instalar FastAPI y Uvicorn:



```bash

pip install fastapi uvicorn

```



### Paso 4: Verificar la estructura del archivo `main.py`



Asegurese de que el archivo `main.py` esta correctamente estructurado y contiene la configuracion necesaria para FastAPI.



### Paso 5: Levantar el servidor con Uvicorn



Ejecute el siguiente comando para iniciar el servidor:



```bash

uvicorn main:app --reload

```



Si el archivo `main.py` esta dentro de una subcarpeta, use el siguiente formato:



```bash

uvicorn main_folder.main:app --reload

```



### Paso 6: Verificar que el servidor esta corriendo



Si todo se ejecuto correctamente, deberias ver el siguiente output en la terminal:



```

INFO:     Will watch for changes in these directories: ['C:\Users\username\OneDrive\Desktop\Python-Web']

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

INFO:     Started reloader process [15752] using StatReload

```



## Nota



Para desactivar el entorno virtual, simplemente ejecute en la terminal:



```bash

deactivate

```



Ahora ya puedes trabajar en tu backend con FastAPI!