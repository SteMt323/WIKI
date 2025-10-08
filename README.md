![CS50 image](https://is1-ssl.mzstatic.com/image/thumb/Purple116/v4/37/a4/71/37a4710b-0d4d-4ced-a438-81c3e9dd1983/App_Icon-marketing.lsr/1200x630bb.png)

# CS50w-Project1

Repositorio con el segundo projecto (Project1) del módulo de web de cs50
## 📋 Características

- **Visualización de entradas:** Los usuarios pueden acceder a las páginas existentes y ver su contenido renderizado.
- **Búsqueda:** Permite buscar por título exacto o mostrar resultados parciales que coincidan con la consulta.
- **Creación de entradas:** Los usuarios pueden agregar nuevas páginas a la Wiki escribiendo el contenido en Markdown.
- **Edición de entradas:** Las páginas existentes pueden modificarse y actualizarse.
- **Entrada aleatoria:** Acceso rápido a una página aleatoria de la Wiki.


### Descripción de carpetas y archivos

- **encyclopedia/**: Contiene la aplicación principal de la Wiki con vistas, utilidades, formularios y plantillas HTML.
- **entries/**: Carpeta donde se almacenan las entradas en formato Markdown.
- **wiki/**: Configuración general del proyecto Django.
- **manage.py**: Script principal para la administración del proyecto (migraciones, servidor, etc.).
- **README.md**: Archivo de documentación del proyecto.

## ⚙️ Tecnologías utilizadas

- **Python 3**  
- **Django**  
- **Markdown**  
- **HTML5 / CSS3** 

    ```
       NOTA: Mire requirements.txt
    ```

## 🚀 Ejecución del proyecto

1. Clonar el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Descargar el entorno virtual:
   ```bash
   python -m venv venv
   ```
4. Activar el entorno virtual:
   ```bash
   ..\venv\Scripts\Activate
   ```
5. Correr el Servidor:
   ```bash
   python manage.py runserver
   ```


```
NOTA: Algunos estilos usados como las cartas o el diseño de los 
contenedores de code en los markdown, no son completamente de mi propiedad, créditos a sus respectivos autores.
```

## Colaboradores

### Cuenta Princippal
- [StvMt323](https://github.com/SteMt323)

### Cuenta Secundaria
- [IryuuStvM](https://github.com/IryuuStvM)

## 📦 Despliegue en Vercel (sitio estático)

Este repositorio incluye un script `build_static.py` que genera una carpeta `public/` con el sitio estático (index y páginas wiki) a partir de las entradas Markdown en `entries/` y copia los assets en `public/static/`.

Pasos rápidos para desplegar en Vercel:

1. Conecta tu repositorio a Vercel desde https://vercel.com/new.
2. En la configuración del proyecto en Vercel, asegúrate de que el framework/builder use `@vercel/python` y que el comando de build sea:

   npm run build

   (El `package.json` en la raíz tiene el script `build` que ejecuta `python build_static.py`).

3. Asegúrate de que `requirements.txt` esté presente en la raíz (Vercel instalará dependencias automáticamente usando pip).
4. Vercel detectará `vercel.json` y ejecutará el build. El proyecto está configurado para desplegar la carpeta `public/` como salida (`outputDirectory: "public"`).

Comandos útiles localmente:

```powershell
# activar entorno virtual en Windows PowerShell
.\venv\Scripts\Activate

# instalar dependencias (si no están instaladas)
pip install -r requirements.txt

# generar el sitio estático en public/
python build_static.py

# ver el index generado (ejemplo)
start public\index.html
```

Notas:
- Si ya ejecutaste `python build_static.py` localmente y `public/` está presente, Vercel desplegará esa salida tras ejecutar el mismo build en su entorno.
- He añadido `.vercelignore` para evitar subir entornos virtuales, bases de datos locales y la carpeta `public/` (si prefieres que Vercel use la `public/` existente, elimina esa línea de `.vercelignore`).

Si quieres, puedo preparar una rama lista para desplegar con `public/` incluida en el repo (git commit) o ayudarte a conectar GitHub y ajustar variables de entorno en Vercel.