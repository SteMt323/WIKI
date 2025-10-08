# Django

Django is a web framework written using [Python](/wiki/Python) that allows for the design of web applications that generate [HTML](/wiki/HTML) dynamically.

### Activación de entorno virtual
```powershell
python -m venv venv
```

```powershell
.\venv\Scripts\activate
```

### Instalación de Django
```powershell
pip install django
```

### Creación del proyecto
```powershell
django-admin startproject nombre_del_proyecto .
```

### Correr el servidor local del proyecto
```powershell
python manage.py runserver
```

### Crear una aplicación
```powershell
django-admin startapp nombre_de_app
```

## Patrón de Arquitectura

### MTV - MODEL TEMPLATE VIEW
### MVC - MODEL VIEW CONTROLLER


## Estructura de Archivos

### manage.py
Permite gestionar el proyecto

### urls.py
Asocia las urls con las vistas que lo gestionan, es donde se escribiran
todas las rutas y vistas las cuales vamos a ir controlando, para controlarlos se usan
las "views" y para escribirlos / pintarlos se usan las "templates".

### settings.py
Se trata de establecer las configuraciones del paquete

## Modelo de Datos

### Migracines, modelo de datos
```powershell
python manage.py migrate
```

### Levantar servidor local
```powershell
python manage.py runserver
```



hola banda