import random
import time
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import json

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_generator.log'),
        logging.StreamHandler()
    ]
)

# Colores ANSI para la consola
class Colors:
    YELLOW = "\033[93m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

@dataclass
class CountryCode:
    prefix: str
    area_codes: List[int]
    phone_length: int = 8  # Longitud predeterminada del número local

class PhoneNumberGenerator:
    def __init__(self, countries_file: str = 'countries_data.json'):
        self.countries_data = self._load_countries_data(countries_file)
        self.generated_numbers: set = set()
        self.start_time = datetime.now()

    def _load_countries_data(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # Si el archivo no existe, usar datos predeterminados
            return {
                "Argentina": {
                    "prefix": "+54",
                    "area_codes": [92325],  # Solo área de San Andrés de Giles
                    "phone_length": 8
                },
                "México": {
                    "prefix": "+52",
                    "area_codes": [55, 33, 81, 777, 662, 999, 222, 333, 442],
                    "phone_length": 8
                },
                "España": {
                    "prefix": "+34",
                    "area_codes": [91, 93, 95, 96, 98, 81, 82, 91, 92],
                    "phone_length": 8
                },
                "Colombia": {
                    "prefix": "+57",
                    "area_codes": [1, 2, 3, 4, 5, 7, 8, 9],
                    "phone_length": 8
                }
            }

    def generate_whatsapp_number(self, country: str) -> Optional[str]:
        """
        Genera un número de WhatsApp único para el país especificado.
        """
        try:
            country_data = self.countries_data.get(country)
            if not country_data:
                raise ValueError(f"País no soportado: {country}")

            prefix = country_data["prefix"]
            area_code = random.choice(country_data["area_codes"])
            phone_length = country_data.get("phone_length", 8)

            while True:
                local_number = random.randint(
                    10 ** (phone_length - 1),
                    (10 ** phone_length) - 1
                )
                
                full_number = f"{prefix} {area_code} {local_number}"
                if full_number not in self.generated_numbers:
                    self.generated_numbers.add(full_number)
                    return full_number

        except Exception as e:
            logging.error(f"Error generando número: {str(e)}")
            return None

    def verify_number(self, number: str) -> bool:
        """
        Simula la verificación de la existencia del número con una probabilidad más realista.
        """
        # Simulación más realista: 30% de probabilidad de que el número exista
        return random.random() < 0.3

    def generate_batch(self, country: str, batch_size: int = 1000, delay: float = 1.0):
        """
        Genera un lote de números de WhatsApp con estadísticas.
        """
        valid_numbers = 0
        invalid_numbers = 0
        
        print(f"\n{Colors.BLUE}Generando números para {country}...{Colors.RESET}\n")

        try:
            for i in range(batch_size):
                number = self.generate_whatsapp_number(country)
                if not number:
                    continue

                exists = self.verify_number(number)
                if exists:
                    print(f"{Colors.GREEN}{number} ✓{Colors.RESET}")
                    valid_numbers += 1
                else:
                    print(f"{Colors.RED}{number} ✗{Colors.RESET}")
                    invalid_numbers += 1

                # Mostrar progreso
                progress = (i + 1) / batch_size * 100
                sys.stdout.write(f"\rProgreso: {progress:.1f}% ")
                sys.stdout.flush()

                time.sleep(delay)

        except KeyboardInterrupt:
            print("\n\nGeneración interrumpida por el usuario.")
        finally:
            self._show_statistics(valid_numbers, invalid_numbers)

    def _show_statistics(self, valid: int, invalid: int):
        """
        Muestra estadísticas de la generación de números.
        """
        total = valid + invalid
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n{Colors.BLUE}Estadísticas:{Colors.RESET}")
        print(f"Total números generados: {total}")
        print(f"Números válidos: {valid} ({(valid/total*100 if total else 0):.1f}%)")
        print(f"Números inválidos: {invalid} ({(invalid/total*100 if total else 0):.1f}%)")
        print(f"Tiempo total: {duration:.2f} segundos")
        print(f"Velocidad: {total/duration if duration else 0:.2f} números/segundo")

def main():
    generator = PhoneNumberGenerator()
    
    # Mostrar países disponibles
    print(f"{Colors.BLUE}Países disponibles:{Colors.RESET}")
    for country in generator.countries_data.keys():
        print(f"- {country}")

    # Solicitar país al usuario
    while True:
        country = input("\nIntroduce el país para generar números de WhatsApp: ").strip()
        if country in generator.countries_data:
            break
        print(f"{Colors.RED}País no válido. Por favor, elige uno de la lista.{Colors.RESET}")

    # Solicitar cantidad de números
    while True:
        try:
            batch_size = int(input("Cantidad de números a generar (máximo 1000): "))
            if 1 <= batch_size <= 1000:
                break
            print(f"{Colors.RED}Por favor, introduce un número entre 1 y 1000.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Por favor, introduce un número válido.{Colors.RESET}")

    # Solicitar delay entre generaciones
    while True:
        try:
            delay = float(input("Tiempo de espera entre números (en segundos, 0-5): "))
            if 0 <= delay <= 5:
                break
            print(f"{Colors.RED}Por favor, introduce un número entre 0 y 5.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Por favor, introduce un número válido.{Colors.RESET}")

    # Iniciar generación
    generator.generate_batch(country, batch_size, delay)

if __name__ == "__main__":
    main()
