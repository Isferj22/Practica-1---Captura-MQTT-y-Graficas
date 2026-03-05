#!/usr/bin/env python3
import json
import os
import matplotlib.pyplot as plt

archivo_log = "mqtt_capture.log"
carpeta_plots = "plots"

# Crear carpeta de gráficas si no existe
if not os.path.exists(carpeta_plots):
    os.makedirs(carpeta_plots)

datos_gas = []
datos_temperatura = []

# ---------------- LEER EL LOG ----------------

if os.path.exists(archivo_log):

    archivo = open(archivo_log, "r")
    lineas = archivo.readlines()
    archivo.close()

    for linea in lineas:

        if "Payload:" in linea:

            partes = linea.split("Payload:")

            if len(partes) > 1:

                json_texto = partes[1].strip()

                if json_texto.startswith("{") and json_texto.endswith("}"):

                    datos = json.loads(json_texto)

                    if "GM102B" in datos:
                        datos_gas.append(datos["GM102B"])

                    if "AmbientTemperature" in datos:
                        datos_temperatura.append(datos["AmbientTemperature"])


# ---------------- GRAFICAS PNG ----------------

if len(datos_gas) > 0:

    plt.figure()
    plt.plot(datos_gas)
    plt.title("Gas GM102B")
    plt.xlabel("Muestra")
    plt.ylabel("Valor")
    plt.savefig("plots/grafica_gas.png")
    plt.close()

if len(datos_temperatura) > 0:

    plt.figure()
    plt.plot(datos_temperatura)
    plt.title("Temperatura Ambiente")
    plt.xlabel("Muestra")
    plt.ylabel("Valor")
    plt.savefig("plots/grafica_temperatura.png")
    plt.close()


# ---------------- GRAFICA ASCII ----------------

if len(datos_gas) > 0:

    ancho = 60
    alto = 15

    maximo = max(datos_gas)
    minimo = min(datos_gas)

    # Arreglo para cuando todos los valores son iguales
    if maximo == minimo:
        maximo = maximo + 1
        minimo = minimo - 1

    print("")
    print("GRAFICA ASCII - GAS GM102B")
    print("+" + "-" * ancho + "+")

    fila = 0

    while fila < alto:

        linea = "|"

        columna = 0

        while columna < len(datos_gas) and columna < ancho:

            valor = datos_gas[columna]

            posicion = round((valor - minimo) / (maximo - minimo) * (alto - 1))

            if posicion == (alto - fila - 1):
                linea = linea + "*"
            else:
                linea = linea + " "

            columna = columna + 1

        while columna < ancho:
            linea = linea + " "
            columna = columna + 1

        linea = linea + "|"

        print(linea)

        fila = fila + 1

    print("+" + "-" * ancho + "+")

    eje_x = " "

    indice = 0

    while indice < len(datos_gas) and indice < ancho:

        if indice % 5 == 0:
            eje_x = eje_x + str(indice % 10)
        else:
            eje_x = eje_x + " "

        indice = indice + 1

    print(eje_x)

    print("Min:", minimo, "Max:", maximo)
