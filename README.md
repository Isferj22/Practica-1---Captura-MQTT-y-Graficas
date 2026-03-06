# Práctica MQTT – Captura y Visualización de Datos de Sensores

## 1. Introducción

En esta práctica se realiza la captura de datos publicados en un broker MQTT, su almacenamiento en un fichero de registro y posteriormente su análisis y visualización mediante scripts en Bash y Python.


## 2. Descripción del problema y de lo que se hace

El objetivo de la práctica es construir un pequeño sistema que:

1. Se conecte a un broker MQTT público.
2. Se suscriba a varios topics de sensores.
3. Capture los mensajes recibidos durante un tiempo determinado.
4. Guarde esos mensajes en un archivo de log.
5. Procese los datos capturados mediante Python.
6. Genere:
   - Gráficas ASCII en la terminal
   - Gráficas PNG con los valores de los sensores.

El script de Bash controla la captura y el tiempo de ejecución, mientras que el script de Python se encarga del procesamiento y visualización de los datos.


## 3. Estructura del proyecto

El proyecto tiene la siguiente estructura de archivos:

practica_mqtt/
│
├── capture_mqtt.sh
├── plot_mqtt.py
├── mqtt_subscribe_emqx_linux
├── mqtt_capture.log
├── README.md
│
└── plots/
├── grafica_gas.png
└── grafica_temperatura.png

Descripción de los archivos:

- **capture_mqtt.sh**  
Script principal en Bash que lanza el programa MQTT, controla el tiempo de captura y ejecuta el análisis posterior.

- **plot_mqtt.py**  
Script en Python que analiza el archivo de log, extrae los datos de los sensores y genera las gráficas.

- **mqtt_subscribe_emqx_linux**  
Programa que se conecta al broker MQTT y recibe los mensajes de los topics.

- **mqtt_capture.log**  
Archivo donde se guardan todos los mensajes recibidos durante la captura.

- **plots/**  
Carpeta donde se guardan las gráficas generadas.


## 4. Requisitos del sistema y cómo instalarlo

Para ejecutar esta práctica se necesita:

Sistema operativo:
Linux o entorno Linux (por ejemplo WSL).

Software necesario:

- Bash
- Python 3
- Biblioteca matplotlib

Instalación de dependencias:

Instalar Python y matplotlib:

sudo apt update
sudo apt install python3 python3-pip
pip3 install matplotlib


### Permisos necesarios

- Dar permisos de ejecución al programa MQTT:
	chmod +x mqtt_subscribe_emqx_linux
- Dar permisos al script principal:
	chmod +x capture_mqtt.sh


## Ejecucion de la practica

Para ejecutar el sistema completo:
./capture_mqtt.sh

El programa pedirá introducir el tiempo máximo de captura en segundos.

Durante ese tiempo el programa capturará los mensajes MQTT y los guardará en el archivo:
mqtt_capture.log

Una vez finalizada la captura, se ejecutará automáticamente el script de Python que procesará los datos.


## Funcionamiento

El funcionamiento del sistema se divide en tres fases principales.

1. Captura de datos
El script capture_mqtt.sh:
	- Lanza el programa mqtt_subscribe_emqx_linux
	- Guarda su salido en mqtt_capture.log
	- Controla el tiempo maximo de ejecucion
	- Finaliza el proceso si se alcanza el tiempo indicado

2. Procesamiento de datos
El script plot_mqtt.py:
	- Lee el archivo mqtt_capture.log
	- Extrae los valores de los sensores
	- Almacena los datos en listas

3. Visualizacion
El script de python genera dos tipos de salida:
	- Grafica ACII en la terminal con una representacion grafica de los datosusando "*"
	- Graficas PNG guardadas en la carpeta "plots": grafica_gas.png y grafica_temperatura.png


## Autor

Ismael Fernandez Jorreto

