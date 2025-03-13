import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime
import json

class PhoneNumberSearcher:
    def __init__(self):
        self.search_history = []
        self.current_user = "ThiagoBranas"  # Agregado el usuario actual
        self.current_datetime = "2025-03-13 01:43:10"  # Fecha y hora actual

    def search_phone_info(self, phone_number):
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number)
            
            # Validate the number
            if not phonenumbers.is_valid_number(parsed_number):
                return {"error": "Número de teléfono no válido"}

            # Get basic information
            info = {
                "número_original": phone_number,
                "número_internacional": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "número_nacional": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "país": geocoder.description_for_number(parsed_number, "es"),
                "código_país": parsed_number.country_code,
                "operador": carrier.name_for_number(parsed_number, "es"),
                "zona_horaria": timezone.time_zones_for_number(parsed_number),
                "tipo_línea": "Móvil" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fijo",
                "es_válido": phonenumbers.is_valid_number(parsed_number),
                "es_posible": phonenumbers.is_possible_number(parsed_number),
                "timestamp_búsqueda": self.current_datetime,
                "usuario": self.current_user
            }

            # Save to search history
            self.search_history.append(info)
            return info

        except Exception as e:
            return {"error": f"Error al procesar el número: {str(e)}"}

    def save_history(self, filename="search_history.json"):
        """Guarda el historial de búsquedas en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.search_history, f, ensure_ascii=False, indent=4)

    def get_history(self):
        """Retorna el historial de búsquedas"""
        return self.search_history

def main():
    searcher = PhoneNumberSearcher()
    
    while True:
        print("\n=== Buscador de Información de Números de Teléfono ===")
        print(f"Usuario actual: {searcher.current_user}")
        print(f"Fecha y hora: {searcher.current_datetime}")
        print("\n1. Buscar información de un número")
        print("2. Ver historial de búsquedas")
        print("3. Guardar historial")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == "1":
            numero = input("\nIngrese el número de teléfono (con código de país, ej: +34612345678): ")
            resultado = searcher.search_phone_info(numero)
            print("\nResultado de la búsqueda:")
            print(json.dumps(resultado, indent=4, ensure_ascii=False))
            
        elif opcion == "2":
            historial = searcher.get_history()
            if historial:
                print("\nHistorial de búsquedas:")
                print(json.dumps(historial, indent=4, ensure_ascii=False))
            else:
                print("\nNo hay búsquedas en el historial.")
                
        elif opcion == "3":
            searcher.save_history()
            print("\nHistorial guardado correctamente en 'search_history.json'")
            
        elif opcion == "4":
            print("\n¡Gracias por usar el buscador!")
            break
            
        else:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
