import random
from time import sleep

def generar_numero_whatsapp_argentino():
    # Prefijo internacional para Argentina
    prefijo_internacional = "+54"
    
    # Códigos de área sin el 0 inicial
    codigos_de_area = [
        11, 221, 223, 261, 264, 291, 297, 341, 342, 343, 345, 351, 353, 381, 383, 385, 387, 388, 11, 2325, 2324, 2323
    ]
    
    # Seleccionamos un código de área aleatorio
    codigo_de_area = random.choice(codigos_de_area)
    
    # Generamos un número de teléfono de 8 dígitos (sin el 15 inicial)
    numero_telefono = random.randint(10000000, 99999999)
    
    # Formateamos el número completo
    numero_completo = f"{prefijo_internacional} {codigo_de_area} {numero_telefono}"
    
    return numero_completo

def verificar_numero(numero):
    # Simula la verificación de la existencia del número
    # En un caso real, aquí se llamaría a la API de WhatsApp o a un servicio que lo permita
    return random.choice([True, False])

# Código ANSI para texto amarillo y rojo
COLOR_AMARILLO = "\033[93m"
COLOR_ROJO = "\033[91m"
FIN_COLOR = "\033[0m"

# Generamos 1000 números de ejemplo
for _ in range(1000):
    numero = generar_numero_whatsapp_argentino()
    existe = verificar_numero(numero)
    
    if existe:
        print(f"{COLOR_AMARILLO}{numero}{FIN_COLOR}")
    else:
        print(f"{COLOR_ROJO}{numero}{FIN_COLOR}") 
    
    sleep(1)
