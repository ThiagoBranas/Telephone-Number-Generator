import random
from time import sleep

# Diccionario con prefijos internacionales y códigos de área para algunos países
pais_codigos = {
    "Argentina": {
        "prefijo": "+54",
        "codigos_de_area": [
            11, 221, 223, 261, 264, 291, 297, 341, 342, 343, 345, 351, 353, 381, 383, 385, 387, 388, 2325, 2324, 2323
        ]
    },
    "México": {
        "prefijo": "+52",
        "codigos_de_area": [
            55, 33, 81, 777, 662, 999, 222, 333, 442, 634, 667
        ]
    },
    "España": {
        "prefijo": "+34",
        "codigos_de_area": [
            91, 93, 95, 96, 98, 81, 82, 91, 92
        ]
    },
    "Colombia": {
        "prefijo": "+57",
        "codigos_de_area": [
            1, 2, 3, 4, 5, 7, 8, 9
        ]
    }
    # Puedes agregar más países aquí
}

def generar_numero_whatsapp(pais):
    """Genera un número de WhatsApp ficticio para el país especificado."""
    if pais not in pais_codigos:
        raise ValueError(f"No se tiene información para el país {pais}.")
    
    # Extraemos el prefijo internacional y los códigos de área
    prefijo_internacional = pais_codigos[pais]["prefijo"]
    codigos_de_area = pais_codigos[pais]["codigos_de_area"]
    
    # Seleccionamos un código de área aleatorio
    codigo_de_area = random.choice(codigos_de_area)
    
    # Generamos un número de teléfono de 8 dígitos (sin el 15 inicial)
    numero_telefono = random.randint(10000000, 99999999)
    
    # Formateamos el número completo
    numero_completo = f"{prefijo_internacional} {codigo_de_area} {numero_telefono}"
    
    return numero_completo

def verificar_numero(numero):
    """Simula la verificación de la existencia del número."""
    return random.choice([True, False])

# Código ANSI para texto amarillo y rojo
COLOR_AMARILLO = "\033[93m"
COLOR_ROJO = "\033[91m"
FIN_COLOR = "\033[0m"

# Solicitar al usuario el país para generar números
pais_usuario = input("Introduce el país para generar números de WhatsApp (por ejemplo, Argentina, México, España): ")

# Generamos 1000 números de ejemplo para el país elegido
for _ in range(1000):
    try:
        numero = generar_numero_whatsapp(pais_usuario)
        existe = verificar_numero(numero)

        if existe:
            print(f"{COLOR_AMARILLO}{numero}{FIN_COLOR}")
        else:
            print(f"{COLOR_ROJO}{numero}{FIN_COLOR}")

        sleep(1)
    except ValueError as e:
        print(e)
        break
