import logging
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
# Todo error se guardará en "sistema_errores.log" para mantener la aplicación activa
logging.basicConfig(
    filename='sistema_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
class SistemaGestionError(Exception):
    """Excepción base para todos los errores de Software FJ."""
    pass

class DatoInvalidoError(SistemaGestionError):
    """Se lanza cuando un dato ingresado no cumple con las validaciones."""
    pass

class OperacionNoPermitidaError(SistemaGestionError):
    """Se lanza cuando se intenta una acción inválida."""
    pass

# ==========================================
# 3. CLASES ABSTRACTAS
# ==========================================
class EntidadGeneral(ABC):
    """
    Clase abstracta que representa entidades generales del sistema.
    """
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad  # Atributo protegido
        self._fecha_creacion = datetime.now()

    @abstractmethod
    def mostrar_detalles(self):
        """Método abstracto que deben implementar las clases hijas."""
        pass

# ==========================================
# 4. CLASE CLIENTE (Encapsulación Estricta)
# ==========================================
class Cliente(EntidadGeneral):
    """
    Clase Cliente con encapsulación de datos personales y validaciones.
    """
    def __init__(self, id_entidad, nombre, correo):
        super().__init__(id_entidad)
        # Atributos privados (encapsulados)
        self.__nombre = None
        self.__correo = None
        
        # Validación desde la creación
        self.asignar_nombre(nombre)
        self.asignar_correo(correo)

    # --- Getters ---
    def obtener_nombre(self):
        return self.__nombre

    def obtener_correo(self):
        return self.__correo

    # --- Setters (con validación de errores) ---
    def asignar_nombre(self, nombre):
        try:
            if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 3:
                raise DatoInvalidoError("El nombre debe ser un texto de al menos 3 caracteres.")
            self.__nombre = nombre.strip()
        except DatoInvalidoError as e:
            logger.error(f"Error al asignar nombre al cliente {self._id_entidad}: {e}")
            raise # Relanzamos la excepción

    def asignar_correo(self, correo):
        try:
            if not correo or "@" not in correo or "." not in correo:
                raise DatoInvalidoError("El correo proporcionado no tiene un formato válido.")
            self.__correo = correo.strip()
        except DatoInvalidoError as e:
            logger.error(f"Error al asignar correo al cliente {self._id_entidad}: {e}")
            raise

    def mostrar_detalles(self):
        return f"Cliente ID: {self._id_entidad} | Nombre: {self.__nombre} | Correo: {self.__correo}"

# ==========================================
# 5. BLOQUE DE PRUEBA SECUENCIAL
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL SISTEMA DE CLIENTES ---")
    
    # Prueba 1: Cliente válido
    try:
        cliente_valido = Cliente(id_entidad="C001", nombre="Ana Gomez", correo="ana@ejemplo.com")
    except DatoInvalidoError as error:
        print(f"[X] No se pudo crear el cliente: {error}")
    else:
        print("[OK] Éxito:", cliente_valido.mostrar_detalles())
    finally:
        print("-> Intento de creación de Cliente 1 finalizado.\n")

    # Prueba 2: Cliente con error intencional (Correo inválido)
    try:
        cliente_invalido = Cliente(id_entidad="C002", nombre="Lu", correo="correo_invalido")
    except DatoInvalidoError as error:
        print(f"[X] Error controlado correctamente: {error}")
        print("    (Revisa el archivo 'sistema_errores.log' para ver el registro interno).")
    else:
        print("[OK] Éxito:", cliente_invalido.mostrar_detalles())
    finally:
        print("-> Intento de creación de Cliente 2 finalizado.\n")