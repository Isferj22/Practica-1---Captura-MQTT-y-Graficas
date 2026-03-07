#!/bin/bash

# Archivo donde se guardará la captura MQTT
archivo_log="mqtt_capture.log"

# Script de Python que procesa los datos y genera gráficas
script_python="plot_mqtt.py"

# Programa que se conecta al broker MQTT y suscribe
programa="./mqtt_subscribe_emqx_linux"

# Pedir al usuario el tiempo máximo de captura en segundos
echo "Introduce el tiempo máximo de captura (segundos):"
read tiempo_maximo

# Validar que la entrada sea un número entero
if ! [[ "$tiempo_maximo" =~ ^[0-9]+$ ]]; then
    echo "Error: debes introducir un número entero."
    exit 1
fi

# Comprobar que el programa MQTT existe
if [ ! -f "$programa" ]; then
    echo "Error: no existe $programa"
    exit 1
fi

echo "Iniciando captura MQTT durante $tiempo_maximo segundos..."

# Ejecutar el programa en segundo plano y redirigir salida al log
$programa > "$archivo_log" 2>&1 &
pid_proceso=$!  # Guardar PID del proceso

echo "Proceso lanzado con PID: $pid_proceso"

# Contador de segundos transcurridos
segundos_transcurridos=0

# Bucle que espera hasta que se cumpla el tiempo máximo o el proceso termine
while kill -0 "$pid_proceso" 2>/dev/null && [ "$segundos_transcurridos" -lt "$tiempo_maximo" ]; do
    sleep 1
    segundos_transcurridos=$((segundos_transcurridos + 1))
done

# Enviar señales para detener el proceso si sigue activo
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

# Esperar a que el proceso termine completamente
wait "$pid_proceso" 2>/dev/null

echo "Captura finalizada."
echo "Ejecutando análisis en Python..."

#Hola Mundo
python3 - <<'PY'
print("Hola mundo desde Python ejecutado dentro de Bash")
PY

# Ejecuta el script que procesa el log y genera gráficas PNG y ASCII
python3 "$script_python"

echo "Proceso completo."
