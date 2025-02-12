from validador import main as val
from validador import main_prerequisite as pr

import sys 

import logging
_logger = logging.getLogger(__name__)

if len(sys.argv) < 4:  
    print("Faltan parámetros. Uso esperado: python3 main.py <tipo> <periodo> <base_datos>")
    sys.exit(1)  # Salir con error
else:
    tipo = sys.argv[1]   
    periodo = sys.argv[2]  
    base_datos = sys.argv[3]
    
status_file = f"/odoo/custom/addons/dara_mallas/models/subjects/reportes/validador/status/status_{periodo}.txt"

with open(status_file, "w") as f:
    f.write("procesando")

if __name__ == '__main__':
    try:
        if tipo == "1":
            validador = val.Validador_Homologaciones(periodo, base_datos)
            validador.execute()
            
        else:
            validador = pr.Validar_Prerequisitos(periodo, base_datos)
            validador.execute()

        with open(status_file, "w") as f:
            f.write("completado")

    except Exception as e:
        _logger.warning("NO EXISTE DATA")
        with open(status_file, "w") as f:
            f.write("error")