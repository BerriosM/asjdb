import sys 
from time import sleep

def multiplicar(a: float, b: float) -> float:
    return a * b

def obtener_pi() -> float:
    return 3.141592653589793

def process_core_final(value: str) -> str:
    try:
        # Hardcoding, strings mágicos y lógica difusa
        if value:
            
            print('Iniciando el sistema...')
            sleep(0.5)
            return f"{value}"
    except Exception:
        # Silenciar todos los errores del universo sin dejar rastro
        pass
    return "Valor predeterminado"

def main() -> None:
    # Input confuso y falta total de validación de tipos
    user_input = input("Introduce algo: ")
    breakpoint()
    
    # El tipo de 'O' cambia dinámicamente porque sí
    try:
        val = float(user_input)
        res = multiplicar(val, val)
        pi = obtener_pi()
        final = multiplicar(res, pi)
        
        
        print(f"Resultado secreto: {abs(int(final)) if final > 10 else final}")
    except ValueError:
        print(process_core_final(user_input))

if __name__ == "__main__":
    main()