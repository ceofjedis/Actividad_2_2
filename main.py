# Autor: Valentin Arzola Angel
# Contacto: https://github.com/ceofjedis
# Fecha: 2023-10-16
# Descripción: Desplegar temperatura en OLED Display con bitArray imagen
#La PicoW y Pico, tienen un sensor interno de temperatura, debemos probarlo y asi finalmente liberar el hardware de algún defecto que desde el 2020 no ha sucedido; el fabricante el SONY U.K, con licencia de RaspberryPi Foundation.
#Alternativa de desplegar la  Temperatura e incluir un bitArray imagen temàtica de esta pràctica (Frio, Càlido, Caliente)
#Puede ser una versiòn 2 donde una imagen fija  con la temperatura formato local e internacional 

# Importar las bibliotecas necesarias
import machine
import utime
from ssd1306 import SSD1306_I2C

# Configuración del sensor de temperatura interno
sensor_temp = machine.ADC(4)

# Configuración de la pantalla OLED SSD1306 a través de I2C
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
oled = SSD1306_I2C(128, 64, i2c)

# Función para leer la temperatura en grados Celsius
def get_temperatura():
    lectura = sensor_temp.read_u16() * 3.3 / (65535)
    temperatura = 27 - (lectura - 0.706) / 0.001721
    return temperatura

# Función para mostrar imágenes temáticas según la temperatura
def mostrar_imagen(temperatura):
    if temperatura < 10:
        # Mostrar imagen de frío
        imagen = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
    elif 10 <= temperatura < 30:
        # Mostrar imagen de cálido
        imagen = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff')
    else:
        # Mostrar imagen de caliente
        imagen = bytearray(b'\x00\xff\x00\xff\x00\xff\x00\xff')
    oled.fill(0)
    oled.framebuf.blit_buffer(imagen, 0, 0, 8, 1)
    oled.show()

# Bucle principal para medir la temperatura y mostrar la imagen

while True:
    temp = get_temperatura()
    print('Temperatura actual: {} °C'.format(temp))
    mostrar_imagen(temp)
    utime.sleep(5)  # Pausa de 5 segundos entre las mediciones
