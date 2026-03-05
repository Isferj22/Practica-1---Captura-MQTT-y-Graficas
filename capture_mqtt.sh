#!/bin/bash

archivo_log="mqtt_capture.log"
script_python="plot_mqtt.py"
programa="./mqtt_subscribe_emqx_linux"

echo "Introduce el tiempo máximo de captura (segundos):"
read tiempo_maximo

if ! [[ "$tiempo_maximo" =~ ^[0-9]+$ ]]; then
    echo "Error: debes introducir un número entero."
    exit 1
fi

if [ ! -f "$programa" ]; then
    echo "Error: no existe $programa"
    exit 1
fi

chmod +x "$programa"

echo "Iniciando captura MQTT durante $tiempo_maximo segundos..."

$programa > "$archivo_log" 2>&1 &
pid_proceso=$!

echo "Proceso lanzado con PID: $pid_proceso"

segundos_transcurridos=0

while kill -0 "$pid_proceso" 2>/dev/null && [ "$segundos_transcurridos" -lt "$tiempo_maximo" ]; do
    sleep 1
    segundos_transcurridos=$((segundos_transcurridos + 1))
done

if kill -0 "$pid_proceso" 2>/dev/null; then
    echo "Tiempo máximo alcanzado. Enviando señal SIGINT..."
    kill -SIGINT "$pid_proceso"
    sleep 2
fi

if kill -0 "$pid_proceso" 2>/dev/null; then
    echo "El proceso sigue activo. Enviando señal SIGTERM..."
    kill -SIGTERM "$pid_proceso"
    sleep 2
fi

if kill -0 "$pid_proceso" 2>/dev/null; then
    echo "El proceso no responde. Enviando señal SIGKILL..."
    kill -SIGKILL "$pid_proceso"
fi

wait "$pid_proceso" 2>/dev/null

echo "Captura finalizada."
echo "Ejecutando análisis en Python..."

python3 - <<'PY'
print("Hola mundo desde Python ejecutado dentro de Bash")
PY

python3 "$script_python"

echo "Proceso completo."
