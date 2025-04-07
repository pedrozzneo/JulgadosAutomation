import re

def extract_numbers(texto):
    padrao = r"resultades (\d+) a (\d+) de (\d+)"
    match = re.search(padrao, texto)
    
    if match:
        primeiro_numero = int(match.group(1))
        ultimo_numero = int(match.group(3))
        return primeiro_numero, ultimo_numero
    else:
        return None, None  # Return a tuple with None values if no match is found
    
texto = "resultades 1 a 10 de 100"
numbers = extract_numbers(texto)
print(numbers[0], numbers[1])  