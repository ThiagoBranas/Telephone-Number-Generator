import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import sys
from typing import Dict, Optional
from dataclasses import dataclass
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phone_info.log'),
        logging.StreamHandler()
    ]
)

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class PhoneInfo:
    """Clase para almacenar la información del número telefónico"""
    number: str
    country: str
    carrier: str
    time_zones: list
    valid: bool
    possible: bool
    type: str
    format_national: str
    format_international: str

class PhoneAnalyzer:
    def __init__(self):
        self.history: Dict[str, PhoneInfo] = {}
        self.start_time = datetime.now()

    def analyze_number(self, phone_number: str) -> Optional[PhoneInfo]:
        """Analiza un número telefónico y retorna su información"""
        try:
            # Si el número ya fue analizado, retornamos la información guardada
            if phone_number in self.history:
                logging.info(f"Recuperando información guardada para {phone_number}")
                return self.history[phone_number]

            # Parsear el número
            parsed_number = phonenumbers.parse(phone_number)

            # Obtener información
            info = PhoneInfo(
                number=phone_number,
                country=geocoder.description_for_number(parsed_number, "es"),
                carrier=carrier.name_for_number(parsed_number, "es"),
                time_zones=timezone.time_zones_for_number(parsed_number),
                valid=phonenumbers.is_valid_number(parsed_number),
                possible=phonenumbers.is_possible_number(parsed_number),
                type=self._get_number_type(parsed_number),
                format_national=phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                format_international=phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            )

            # Guardar en el historial
            self.history[phone_number] = info
            return info

        except Exception as e:
            logging.error(f"Error al analizar el número {phone_number}: {str(e)}")
            return None

    def _get_number_type(self, parsed_number) -> str:
        """Determina el tipo de número telefónico"""
        number_type = phonenumbers.number_type(parsed_number)
        types = {
            phonenumbers.PhoneNumberType.MOBILE: "Móvil",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fijo",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fijo o Móvil",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Gratuito",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium",
            phonenumbers.PhoneNumberType.SHARED_COST: "Costo Compartido",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal",
            phonenumbers.PhoneNumberType.PAGER: "Localizador",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.UNKNOWN: "Desconocido"
        }
        return types.get(number_type, "Desconocido")

    def display_info(self, info: PhoneInfo) -> None:
        """Muestra la información del número de manera formateada"""
        print(f"\n{Colors.HEADER}{'='*50}{Colors.RESET}")
        print(f"{Colors.BOLD}Información del número telefónico{Colors.RESET}")
        print(f"{Colors.HEADER}{'='*50}{Colors.RESET}\n")

        # Información básica
        print(f"{Colors.BLUE}Número analizado:{Colors.RESET}")
        print(f"  Nacional: {Colors.GREEN}{info.format_national}{Colors.RESET}")
        print(f"  Internacional: {Colors.GREEN}{info.format_international}{Colors.RESET}")

        # Validez
        valid_status = f"{Colors.GREEN}✓ Válido{Colors.RESET}" if info.valid else f"{Colors.RED}✗ No válido{Colors.RESET}"
        possible_status = f"{Colors.GREEN}✓ Posible{Colors.RESET}" if info.possible else f"{Colors.RED}✗ No posible{Colors.RESET}"
        print(f"\n{Colors.BLUE}Estado:{Colors.RESET}")
        print(f"  Validez: {valid_status}")
        print(f"  Posibilidad: {possible_status}")

        # Ubicación y tipo
        print(f"\n{Colors.BLUE}Detalles:{Colors.RESET}")
        print(f"  País: {Colors.YELLOW}{info.country or 'Desconocido'}{Colors.RESET}")
        print(f"  Operador: {Colors.YELLOW}{info.carrier or 'Desconocido'}{Colors.RESET}")
        print(f"  Tipo: {Colors.YELLOW}{info.type}{Colors.RESET}")

        # Zonas horarias
        print(f"\n{Colors.BLUE}Zonas horarias:{Colors.RESET}")
        for zone in info.time_zones:
            print(f"  • {Colors.YELLOW}{zone}{Colors.RESET}")

def main():
    analyzer = PhoneAnalyzer()
    
    print(f"{Colors.HEADER}Analizador de Números Telefónicos{Colors.RESET}")
    print("Para salir, escribe 'salir' o presiona Ctrl+C\n")

    while True:
        try:
            number = input(f"\n{Colors.BOLD}Ingresa un número telefónico (con código de país, ej: +34612345678): {Colors.RESET}")
            
            if number.lower() in ['salir', 'exit', 'quit']:
                print(f"\n{Colors.GREEN}¡Hasta luego!{Colors.RESET}")
                break

            info = analyzer.analyze_number(number)
            if info:
                analyzer.display_info(info)
            else:
                print(f"\n{Colors.RED}Error: No se pudo analizar el número. Asegúrate de incluir el código de país.{Colors.RESET}")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}¡Hasta luego!{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    main()
