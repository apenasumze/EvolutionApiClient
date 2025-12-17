import re

def validate_number(number: str | int) -> str | None: # <--- Ajuste na tipagem
    """
    Valida e normaliza um número de telefone para o formato internacional brasileiro
    ou um ID de grupo do WhatsApp.
    ... (docstring) ...
    """
    
    number_str = str(number) # <--- CONVERSÃO FEITA AQUI, NO INÍCIO

    # Validação para grupos.
    # Retorna o JID do grupo caso seja um formato válido.
    if number_str.endswith('@g.us'):
        return number_str if re.match(r'^\d+@g\.us$', number_str) else None

    # Validação para contatos.
    number = re.sub(r'\D', '', number_str)
    
    if not number.startswith('55'):
        number = '55' + number
    if len(number) not in [12, 13]:
        return None
    ddd = number[2:4]
    if not (1 <= int(ddd) <= 99):
        return None
    if len(number) == 13 and not number[4] == '9':
        return None
    return number


def calculate_send_delay(loop_index: int, delay_min: int = 5, delay_max: int = 30, delay_const: int = 10) -> int:
    """
    Calcula o delay dinamicamente de acordo com a volta atual do loop.

    - Para as primeiras `delay_const` voltas, retorna `delay_min`.
    - A partir da volta `delay_const`, o delay aumenta 1 por volta.
    - O valor final é limitado a `delay_max`.

    Args:
        loop_index (int): Índice da volta atual do loop (zero-based).
        delay_min (int): Delay mínimo (em segundos, por exemplo).
        delay_max (int): Delay máximo permitido.
        delay_const (int): Número de voltas fixas com delay mínimo antes de começar a aumentar.

    Returns:
        int: Delay calculado (em segundos).
    """
    if loop_index < delay_const:
        return delay_min
    delay = delay_min + (loop_index - delay_const + 1)
    return min(delay, delay_max)


