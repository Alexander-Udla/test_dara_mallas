from validador import main as val
from validador import main_prerequisite as pr


import sys 

import logging
_logger = logging.getLogger(__name__)

if len(sys.argv) > 2:  # Asegurar que se reciben al menos 2 parámetros
    tipo = sys.argv[1]   # Primer parámetro (self.type)
    periodo = sys.argv[2]  # Segundo parámetro (self.period_id.name)
    
else:
    print("Faltan parámetros")


if __name__ == '__main__':
    try:
        if tipo == "1":
            print("INGRESO")
            validador = val.Validador_Homologaciones(periodo)
            validador.execute()
            
        else:
            validador = pr.Validar_Prerequisitos(periodo)
            validador.execute()

    except Exception as e:
        _logger.warning("NO EXISTE DATA")