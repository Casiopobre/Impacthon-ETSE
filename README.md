# CuidaMed
Proyecto desarrollado durante **[IMPACT-THON USC](https://pasoinfousc.com/hackathon.html)**

**CuidaMed** es un sistema de **seguimiento de medicación** diseñado para ayudar al usuario a gestionar su toma de medicamentos y realizar un seguimiento de los síntomas. SU interfaz sencilla está diseñada para ser accesible a un amplio público, incluyendo personas mayores, reduciendo la confusión y facilitando su uso. El sistema busca mejorar la adherencia a los tratamientos y brindar un mejor control sobre la evolución de la salud del paciente.

## Funcionalidades
+ **Compatibilidad multiplataforma**: Disponible tanto en versión web como en Android.
+ **Inicio de sesión diferenciado**: Existen dos tipos de cuentas, una para pacientes y otra para profesionales sanitarios, permitiendo así un acceso adecuado a las funciones según el rol del usuario.
+ **Seguimiento diario de síntomas**: Los usuarios pueden registrar sus síntomas y cambios en su estado de salud de manera diaria para un mejor control médico.
+ **Calendario de medicamentos y síntomas**: Un sistema de calendario donde se visualizan las fechas y horas de toma de medicamentos, así como los registros de los síntomas.
+ **Lista de medicamentos previstos para hoy**: Una lista que muestra los medicamentos programados para el día actual, ayudando a los usuarios a no olvidar ningúna dosis.

!CAPTURA DE PANTALLA DE LA WEB!

## Como funciona?
La aplicación está desarrollada en el framework de cliente Flet, lo que permite exportarla a diferentes plataformas como web, Android y Windows.
### Arquitectura del sistema
1. **Interfaz de usuario**: La interfaz está diseñada con Flet para proporcionar una experiencia intuitiva y accesible en múltiples dispositivos.
2. **API backend**: La aplicación se conecta a una API desarrollada en NodeJS que gestiona la lógica de negocio y la comunicacion con la base de datos.
3. **Base de datos**: Se utiliza MySQL para almacenar los datos de los usuarios, sus medicamentos, síntomas y registros médicos.
4. **Consulta de medicamentos**: La aplicación emplea la CIMA REST API de la AEMPS para obtener información actualizada sobre los medicamentos disponibles en España.
5. **Autenticación y seguridad**: Se implementa autenticación segura para proteger los datos de los usuarios, con encriptación y permisos diferenciados entre pacientes y profesionales sanitarios.
6. **Notificaciones y recordatorios**: El sistema envía notificaciones a los usuarios para recordarles la toma de medicamentos y el registro de síntomas diarios.

## Instalación
Para poder utilizar la aplicación necesitas un entorno con Python 3.12.3 o superior y [Flet](https://flet.dev/) 0.27.5.
1. Clona este repositorio
2. En en directorio "frontend" ejecuta el comando `flet run --web` para la versión web y `flet run --android` para Android.
   > Nota: para Android es necesario tener instalada la app de Flet y que el ordenador esté conectado a la misma red que el teléfono

## Despliegue
### Instrucciones para ejecutar la app
Para que cualquier usuario pueda ejecutar la aplicacion, tiene que seguir estos pasos:
1. **Clonar el repositorio** del proyecto desde la plataforma correspondiente (GitHub, GitLab, etc.).
2. **Instalar las dependencias necesarias** con el comando correspondiente según el sistema (ej, `npm install` para Node.js o `pip install -r requirements.txt` para Python).
3. **Configurar el entorno**. Necesitas un entorno con Python 3.12.3 o superior y [Flet](https://flet.dev/) 0.27.5.
4. **Ejecutar la aplicación** con los comandos especificos según la plataforma:
   -Para web: `npm start` o `python app.py`
   -Para Android: Compilar la app con Android Studio y desplegar en un dispositivo o emulador.
      >Nota: es imprescindible tener la app de Flet y que el ordenador esté conectado a la misma red que el teléfono.

## Instrucciones de uso
### ¿Cómo se usa la app?
1. **Registro e inicio de sesión**
   + Los pacientes crean una cuenta y configuran su perfil de salud.
   + Los profesionales sanitarios puede registrarse y vincularse a pacientes para hacer seguimiento.
2. **Gestión de medicamentos**
    + Los usuarios ingresan los medicamentos que están tomando y establecen horarios.
    + La app envía recordatorios cuando es el momento de tomar un medicamento.
3. **Seguimiento de síntomas**
   + Los pacientes pueden registrar síntomas y cambios en su salud.
   + La información se almacena para su consulta posterior y para ser analizada por médicos.
4. **Interacción con el calendario**
   Se pueden visualizar las fechas de toma de medicamentos y el historial de síntomas en un calendario interactivo.
5. **Acceso de profesionales sanitarios**
   Los médicos pueden acceder a los datos del paciente y proporcionar recomendaciones basadas en la evolución de sus síntomas. Además, basándose en los datos recopilados, la aplicacion puede generar reportes y gráficos para facilitar la toma de decisiones médicas.
   
## Licencias
+ Código fuete: Este software está licenciado bajo una licencia de código abierto, permitiendo su uso, modificación y distribución bajo ciertas condiciones.
+ Iconos de síntomas: SeungJun for TheNounProject (_Creative Commons Attribution License (CC BY 3.0)_)
+ Datos de medicamentos: La información sobre medicamentos se obtiene a través de la CIMA REST API de la AEMPS, cuyos datos están sujetos a los términos y condiciones establecidos por la Agencia Española de Medicamentos y Productos Sanitarios.
+ Bibiotecas y frameworks: Se utilizan diversas tecnologías de terceros, cada una con sus propias licencias. Entre ellas:
     + FLET
     + NodeJS (licencia MIT)
     + MySQL (licencia GPL)

