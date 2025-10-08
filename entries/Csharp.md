# Aprendiendo CSharp



Este repositorio contiene ejemplos, recursos y ejercicios practicos para aprender el lenguaje de programacion CSharp. Es ideal para principiantes que desean adquirir una base solida en el lenguaje y avanzar hacia el desarrollo de aplicaciones con .NET



---



## Que es CSharp



CSharp (pronunciado C Sharp) es un lenguaje de programacion moderno, orientado a objetos y desarrollado por Microsoft como parte de su plataforma .NET. Es utilizado para construir una amplia variedad de aplicaciones, incluyendo:



- Aplicaciones de escritorio  

- Aplicaciones web  

- Aplicaciones moviles (con Xamarin o MAUI)  

- Juegos (con Unity)  

- Servicios en la nube y APIs  



---



## Requisitos



Para poder ejecutar los ejemplos y proyectos incluidos en este repositorio necesitas:

- .NET SDK (version 6.0 o superior recomendada)  

- Un editor de codigo como Visual Studio o Visual Studio Code  

- Conocimientos basicos de programacion (no obligatorio, pero util)  



---



## Estructura del repositorio



```

/CSharp-Fundamentals

   |---- HelloWorld/           # Tu primer programa en CSharp

   |---- Variables/            # Uso de variables y tipos de datos

   |---- Condicionales/        # Estructuras if, else y switch

   |---- Bucles/               # while, for, foreach

   |---- Funciones/            # Metodos y paso de parametros

   |---- ClasesObjetos/        # Programacion orientada a objetos

   |---- Proyectos/            # Mini proyectos para practicar

```

---

## Como ejecutar un ejemplo



1. Abre una terminal o consola  

2. Navega al directorio del proyecto:  



```bash

cd CSharp-Fundamentals/HelloWorld

```



3. Ejecuta el programa con:  

```bash

dotnet run

```



---

## Temas cubiertos

- Sintaxis basica de CSharp  

- Tipos de datos y operadores  

- Control de flujo (condiciones y bucles)  

- Funciones y metodos  

- Clases y objetos  

- Herencia y polimorfismo  

- Colecciones (arrays, listas, diccionarios)  

- Manejo de errores (try-catch)  

- Archivos y entrada salida  

- LINQ basico  



---



## Ejemplo de C#



```csharp

using System;

class Program

{

    static void Main()

    {

        Random rnd = new Random();

        int numeroAleatorio = rnd.Next(1, 101); // Genera numero entre 1 y 100 (101 excluido)

        Console.WriteLine("Numero aleatorio generado: " + numeroAleatorio);

    }

}

```



---



## Recursos recomendados

- Documentacion oficial de CSharp: https://learn.microsoft.com/es-es/dotnet/csharp/  

- Microsoft Learn - CSharp para principiantes: https://learn.microsoft.com/es-es/training/paths/csharp-first-steps/  

- Curso gratuito en YouTube: https://www.youtube.com/results?search_query=curso+csharp+completo  



---



## Contribuciones

Las contribuciones son bienvenidas. Si tienes ejercicios, ejemplos o sugerencias para mejorar este repositorio, no dudes en hacer un pull request o abrir un issue.



---



## Autores:

- StvMt323

---



## Licencia



Este proyecto esta bajo la licencia MIT. Consulta el archivo LICENSE para mas informacion.