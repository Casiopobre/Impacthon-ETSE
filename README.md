# CuidaMed
Proyecto desarrollado durante **[IMPACT-THON USC](https://pasoinfousc.com/hackathon.html)**

**CuidaMed** es un sistema de **seguimiento de medicación** diseñado para ayudar al usuario a gestionar su toma de medicamentos y a mantener un [**?seguimiento?**] de sus síntomas. 
Presenta una interfaz sencilla con el objetivo de llegar al mayor público posible y resultar poco confuso para personas mayores.

## Funcionalidades
+ Soporte tanto para **web** como para **android**
+ Sistema de **inicio de sesión** diferenciado para profesionales sanitarios y para pacientes
+ Sistema diario de **seguimiento de síntomas**
+ **Calendario** de medicamentos y síntomas
+ Lista de **medicamentos** previstos para hoy

!CAPTURA DE PANTALLA DE LA WEB!

## Como funciona?
La aplicación está desarrollada en el framework de cliente flet, para permitirnos exportarlo a diferentes plataformas. \
La aplicación se conecta a nuestra API desarrollada en NodeJS que se conecta a la base de datos MySQL. \
Para la base de datos utilizamos la CIMA REST API de la AEMPS para obtener la información sobre los medicamentos.

## Instalación
Para poder utilizar la aplicación necesitas un entorno con Python 3.12.3 o superior y [Flet](https://flet.dev/) 0.27.5. \
1. Clona este repositorio
2. En en directorio "frontend" ejecuta el comando `flet run --web` para la versión web y `flet run --android` para Android.
   > Nota: para Android es necesario tener instalada la app de Flet y que el ordenador esté conectado a la misma red que el teléfono

## Instrucciones de uso

### Paciente
Primero inicia sesión o regístrate en la pantalla de login como paciente. \
Para añadir un medicamento, presiona el día en el que lo quieres añadir en el calendario y completa los campos. \
Para añadir un síntoma pulsa el botón superior ("¿Cómo te sientes hoy?") y añade un síntoma predefinido o dale al botón "+" para añadir un nuevo síntoma. 

### Personal sanitario
Primero inicia sesión como presonal sanitario. \
. . . . . . . . . . . . FAÑLTASN 

## Licencias
Iconos de síntomas: SeungJun for TheNounProject (_Creative Commons Attribution License (CC BY 3.0)_) 

