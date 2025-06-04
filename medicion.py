import tkinter as tk
import serial
import threading
import datetime
import csv

# Configura el puerto según tu placa
arduino = serial.Serial('COM8', 9600, timeout=1)

def iniciar_medicion():
    boton.config(state="disabled", text="Midiendo...", bg="#AAAAAA")
    resultado_var.set("Midiendo...")

    arduino.write(b'\n')
    threading.Thread(target=leer_datos).start()

def leer_datos():
    buffer = ""
    while True:
        if arduino.in_waiting > 0:
            linea = arduino.readline().decode('utf-8').strip()
            print(linea)
            buffer += linea + '\n'
            if "MEDICIÓN FINALIZADA" in linea:
                final_line = arduino.readline().decode('utf-8').strip()
                buffer += final_line
                resultado_var.set(final_line)

                if "Distancia total recorrida:" in final_line:
                    distancia = final_line.split(":")[1].strip().replace(" cm", "")
                    guardar_medicion_en_csv(distancia)

                boton.config(state="normal", text="Iniciar Nueva Medición", bg="#4CAF50")
                break

def guardar_medicion_en_csv(distancia):
    with open("mediciones.csv", "a", newline="") as archivo_csv:
        writer = csv.writer(archivo_csv)
        # Si el archivo está vacío, escribe el encabezado
        if archivo_csv.tell() == 0:
            writer.writerow(["Fecha y   Hora",   "Distancia (cm)"])
        
        # Escribe la medición con la fecha y hora actual
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([fecha_hora, distancia])

# Crear ventana
ventana = tk.Tk()
ventana.title("Sistema de Medición - Encoder")
ventana.geometry("500x300")
ventana.configure(bg="#f1f1f1")

# Estilos
fuente_titulo = ("Helvetica", 14, "bold")
fuente_texto = ("Helvetica", 12)
fuente_boton = ("Helvetica", 12, "bold")

# Texto principal
resultado_var = tk.StringVar()
resultado_var.set("Presiona el botón para comenzar la medición")

etiqueta = tk.Label(ventana, textvariable=resultado_var, font=fuente_titulo,
                    bg="#f1f1f1", fg="#333", wraplength=480, justify="center")
etiqueta.pack(pady=40)

# Botón principal
boton = tk.Button(ventana, text="Iniciar Medición", command=iniciar_medicion,
                  height=2, width=30, font=fuente_boton,
                  bg="#4CAF50", fg="white", activebackground="#45A049",
                  relief="flat", bd=0)
boton.pack(pady=10)

ventana.mainloop()

