import tkinter as tk
import serial
import time

# Configuración de la comunicación serial con Arduino
ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' por el puerto correcto en tu sistema

def iniciar_medicion():
    # Envía un comando al Arduino para iniciar la medición
    ser.write(b'INICIAR')  # Ajusta según lo que envíes desde Arduino
    
    # Mostrar mensaje de advertencia al usuario
    label_instrucciones.config(text="Iniciando medición... Por favor, espere.")
    
    # Espera a que se presione Enter para comenzar
    label_instrucciones.config(text="Parta desde el punto cero y presione ENTER para comenzar")
    
    while True:
        if ser.in_waiting > 0:
            distancia = ser.readline().decode('utf-8').strip()
            label_distancia.config(text=f"Distancia Total: {distancia} cm")
            root.update()

        # Para finalizar la medición si no se reciben pulsos durante 2 segundos
        time.sleep(2)  # Este tiempo se puede ajustar según el comportamiento de Arduino
        label_instrucciones.config(text="Medición finalizada. Distancia total recorrida.")
        break


# Crear la ventana principal
root = tk.Tk()
root.title("Medición de Distancia con Encoder")
root.geometry("600x500")
root.config(bg='#f0f8ff')  # Fondo de color claro para hacerlo más atractivo

# Crear un título
titulo = tk.Label(root, text="Medición de Distancia con Encoder", font=('Helvetica', 16, 'bold'), bg='#f0f8ff')
titulo.pack(pady=20)

# Instrucciones iniciales
label_instrucciones = tk.Label(root, text="Por favor, asegúrese de que el encoder esté en el punto cero.", font=('Arial', 12), bg='#f0f8ff')
label_instrucciones.pack(pady=10)

# Crear el botón de inicio con estilo
boton_iniciar = tk.Button(root, text="Iniciar Medición", font=('Arial', 14), fg='white', bg="#2E5998", command=iniciar_medicion)
boton_iniciar.pack(pady=20)

# Crear el label para mostrar la distancia
label_distancia = tk.Label(root, text="Distancia Total: 0 cm", font=('Arial', 14), bg='#f0f8ff')
label_distancia.pack(pady=10)

# Ejecutar la ventana principal
root.mainloop()
