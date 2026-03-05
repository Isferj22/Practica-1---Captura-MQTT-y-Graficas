#!/bin/bash

LOG_FILE="mqtt_capture.log"
PYTHON_SCRIPT="plot_mqtt.py"
PROGRAM="./mqtt_subscribe_emqx_linux"

echo "Introduce el tiempo máximo de captura (segundos):"
read MAX_TIME

if ! [[ "$MAX_TIME" =~ ^[0-9]+$ ]]; then
    echo "Error: debes introducir un número entero."
    exit 1
fi

if [ ! -f "$PROGRAM" ]; then
    echo "Error: no existe $PROGRAM"
    exit 1
fi

chmod +x "$PROGRAM"

echo "Iniciando captura MQTT durante $MAX_TIME segundos..."

$PROGRAM > "$LOG_FILE" 2>&1 &
PID=$!

echo "Proceso lanzado con PID: $PID"

SECONDS_PASSED=0

while kill -0 "$PID" 2>/dev/null && [ "$SECONDS_PASSED" -lt "$MAX_TIME" ]; do
    sleep 1
    SECONDS_PASSED=$((SECONDS_PASSED + 1))
done

if kill -0 "$PID" 2>/dev/null; then
    echo "Tiempo máximo alcanzado. Enviando SIGINT..."
    kill -SIGINT "$PID"
    sleep 2
fi

if kill -0 "$PID" 2>/dev/null; then
    echo "Proceso aún activo. Enviando SIGTERM..."
    kill -SIGTERM "$PID"
    sleep 2
fi

if kill -0 "$PID" 2>/dev/null; then
    echo "Proceso no responde. Enviando SIGKILL..."
    kill -SIGKILL "$PID"
fi

wait "$PID" 2>/dev/null

echo "Captura finalizada."
echo "Ejecutando análisis en Python..."

python3 - <<'PY'
print("Hola mundo desde Python ejecutado dentro de Bash")
PY

python3 "$PYTHON_SCRIPT"

echo "Proceso completo."
