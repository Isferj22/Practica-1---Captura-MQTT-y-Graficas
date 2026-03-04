#!/bin/bash

LOG_FILE="mqtt_capture.log"

echo "====================================="
echo " PRACTICA MQTT - SISTEMAS OPERATIVOS"
echo "====================================="

echo "Introduce el tiempo de captura en segundos:"
read tiempo

echo ""
echo "Iniciando cliente MQTT..."

# Ejecutar cliente MQTT en background
./mqtt_subscribe_emqx_linux > "$LOG_FILE" 2>&1 &

PID=$!

echo "Proceso iniciado con PID: $PID"

# Esperar el tiempo indicado
sleep "$tiempo"

echo ""
echo "Finalizando proceso..."

# Enviar señales
kill -SIGINT $PID 2>/dev/null
sleep 1

kill -SIGTERM $PID 2>/dev/null
sleep 1

kill -SIGKILL $PID 2>/dev/null

echo "Proceso detenido."

echo ""
echo "Ejecutando script Python..."

python3 plot_mqtt.py

echo ""
echo "Practica finalizada."
