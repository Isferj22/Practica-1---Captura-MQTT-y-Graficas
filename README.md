# Practica-1---Captura-MQTT-y-Graficas
Practica 1 - SO: captura de datos MQTT usando un proceso en WSL, almacenamiento en log y generación de gráfica con Python.

## Descripcion
Esta practica consiste en ejecutar un cliente MQTT como un proceso en segundo plano, capturar los datos enviados por un sensor de gas, almacenarlos en un archivo log y generar una grafica con los valores obtenidos
Se utilizan:

- Script Bash para control de procesos
- Señales SIGINT, SIGTERM y SIGKILL
- Python para procesamiento de datos
- matplotlib para generacion de graficas
- Entorno WSL (Windows Subsystem for Linux)

## Estructura del proyecto
practica_mqtt/
│
├── capture_mqtt.sh
├── plot_mqtt.py
├── mqtt_subscribe_emqx_linux
├── README.md
├── mqtt_capture.log
│
└── plots/
└── GM102B.png

## Requisitos
Sistema Linux o WSL con:
- python3
- matplotlib

## Permisos de ejecucion
Dar permisos mediante chmod +x nombre_archivo a:
- capture_mqtt.sh
- mqtt_subscribe_emqx_linux
- plot_mqtt.py

## Ejecucion de la practica
1- Ejecucion principal: ejecutar capture_mqtt.sh (./capture_mqtt.sh)
2- Introducir el tiempo de captura en segundos cuando se solicite

## Funcionamiento
El script realiza las siguientes acciones:
- Ejecuta el MQTT como un proceso
- Guarda el PID del proceso
- Captura los datos en el archivo mqtt_capture.log
- Finaliza procesos usando señales (SIGINT, SIGTERM, SIGKILL)
- Ejecuta el script Python, generando una grafica en plots/GM102B.png

## Autor
Ismael Fernandez Jorreto
