#!/usr/bin/env python3
import json
import os
import matplotlib.pyplot as plt

archivo_log = "mqtt_capture.log"
carpeta_plots = "plots"

# Crear carpeta para gráficas si no existe
if not os.path.exists(carpeta_plots):
    os.makedirs(carpeta_plots)

# Listas para almacenar datos
datos_gas = []
datos_temperatura = []

# Leer el LOG
if os.path.exists(archivo_log):
    with open(archivo_log, "r") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        if "Payload:" in linea:
            partes = linea.split("Payload:")
            if len(partes) > 1:
                json_texto = partes[1].strip()
                if json_texto.startswith("{") and json_texto.endswith("}"):
                    datos = json.loads(json_texto)
                    # Para gas usamos co_ppm
                    if "co_ppm" in datos:
                        datos_gas.append(datos["co_ppm"])
                    # Para temperatura usamos temperature_c
                    if "temperature_c" in datos:
                        datos_temperatura.append(datos["temperature_c"])

# Graficas PNG
if len(datos_gas) > 0:
    plt.figure()
    plt.plot(datos_gas)
    plt.title("Gas CO (ppm)")
    plt.xlabel("Muestra")
    plt.ylabel("Valor")
    plt.savefig(os.path.join(carpeta_plots, "grafica_gas.png"))
    plt.close()

if len(datos_temperatura) > 0:
    plt.figure()
    plt.plot(datos_temperatura)
    plt.title("Temperatura Ambiente (°C)")
    plt.xlabel("Muestra")
    plt.ylabel("Valor")
    plt.savefig(os.path.join(carpeta_plots, "grafica_temperatura.png"))
    plt.close()

# Grafica ASCII
def graficar_ascii(datos, titulo):
    if len(datos) == 0:
        print(f"No hay datos para {titulo}")
        return

    ancho = 60
    alto = 15

    maximo = max(datos)
    minimo = min(datos)

    if maximo == minimo:
        maximo += 1
        minimo -= 1

    print("")
    print(f"GRAFICA ASCII - {titulo}")
    print("+" + "-" * ancho + "+")

    for fila in range(alto):
        linea = "|"
        for columna in range(min(len(datos), ancho)):
            valor = datos[columna]
            posicion = round((valor - minimo) / (maximo - minimo) * (alto - 1))
            linea += "*" if posicion == (alto - fila - 1) else " "
        linea += " " * max(0, ancho - len(datos)) + "|"
        print(linea)

    print("+" + "-" * ancho + "+")

    # Eje X con índices cada 5 caracteres
    eje_x = "".join(str(i % 10) if i % 5 == 0 else " " for i in range(min(len(datos), ancho)))
    print(eje_x)

    print("Min:", minimo, "Max:", maximo)

# Mostrar gráficas ASCII
graficar_ascii(datos_gas, "Gas CO (ppm)")
graficar_ascii(datos_temperatura, "Temperatura Ambiente (°C)")
