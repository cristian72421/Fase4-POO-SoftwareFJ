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
# 5. CLASE ABSTRACTA SERVICIO Y POLIMORFISMO
# ==========================================
class Servicio(EntidadGeneral):
    """
    Clase abstracta Servicio que hereda de EntidadGeneral.
    """
    def __init__(self, id_entidad, nombre_servicio, precio_base):
        super().__init__(id_entidad)
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abstractmethod
    def describir_servicio(self):
        """Método que debe ser sobrescrito (Polimorfismo)."""
        pass

    @abstractmethod
    def calcular_costo(self):
        pass

    def mostrar_detalles(self):
        return f"Servicio ID: {self._id_entidad} | {self.nombre_servicio} | Precio Base: ${self.precio_base}"

# ==========================================
# 6. SERVICIOS ESPECIALIZADOS (Clases Derivadas)
# ==========================================
class ReservaSala(Servicio):
    def __init__(self, id_entidad, capacidad_personas):
        # Según el caso, la empresa ofrece reservas de salas
        super().__init__(id_entidad, "Reserva de Sala de Reuniones", 50000) 
        self.capacidad_personas = capacidad_personas

    def describir_servicio(self):
        return f"Sala equipada para un máximo de {self.capacidad_personas} personas."

    # SOBRECARGA DE MÉTODOS: Se usan parámetros opcionales (horas, impuesto, descuento)
    def calcular_costo(self, horas=1, impuesto=0.0, descuento=0.0):
        try:
            if horas <= 0:
                raise DatoInvalidoError("Las horas de reserva deben ser mayores a cero.")
            subtotal = self.precio_base * horas
            total = subtotal + (subtotal * impuesto) - (subtotal * descuento)
            return total
        except DatoInvalidoError as e:
            logger.error(f"Error al calcular costo en {self.nombre_servicio}: {e}")
            raise

class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad, tipo_equipo):
        # La empresa también ofrece alquiler de equipos
        super().__init__(id_entidad, "Alquiler de Equipo Computacional", 120000)
        self.tipo_equipo = tipo_equipo

    def describir_servicio(self):
        return f"Equipo disponible: {self.tipo_equipo}."

    def calcular_costo(self, dias=1, seguro_danos=0.0):
        try:
            if dias <= 0:
                raise DatoInvalidoError("Los días de alquiler deben ser mayores a cero.")
            return (self.precio_base * dias) + seguro_danos
        except DatoInvalidoError as e:
            logger.error(f"Error al calcular costo en {self.nombre_servicio}: {e}")
            raise

class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad, area_experta):
        # Y finalmente, asesorías especializadas
        super().__init__(id_entidad, "Asesoría Técnica Especializada", 200000)
        self.area_experta = area_experta

    def describir_servicio(self):
        return f"Consultoría enfocada en el área de: {self.area_experta}."

    def calcular_costo(self, sesiones=1, impuesto=0.19):
        try:
            if sesiones <= 0:
                raise DatoInvalidoError("El número de sesiones debe ser mayor a cero.")
            subtotal = self.precio_base * sesiones
            return subtotal + (subtotal * impuesto)
        except DatoInvalidoError as e:
            logger.error(f"Error al calcular costo en {self.nombre_servicio}: {e}")
            raise


# ==========================================
# BLOQUE DE PRUEBA SECUENCIAL
# ==========================================
if __name__ == "__main__":
    print("--- INICIANDO PRUEBAS DEL SISTEMA ---")
    
    try:
        # 1. Prueba de Cliente
        cliente_valido = Cliente("C001", "Ana Gomez", "ana@ejemplo.com")
        print("[OK]", cliente_valido.mostrar_detalles())

        # 2. Prueba de Servicios (Polimorfismo)
        sala = ReservaSala("S001", 10)
        equipo = AlquilerEquipo("E001", "Proyector 4K")
        asesoria = AsesoriaEspecializada("A001", "Seguridad Informática")

        print("\n--- SERVICIOS DISPONIBLES ---")
        for servicio in [sala, equipo, asesoria]:
            print(f"- {servicio.describir_servicio()}")

        # 3. Prueba de Sobrecarga (Diferentes variantes de cálculo)
        print("\n--- CÁLCULO DE COSTOS SOBRECARGADOS ---")
        print(f"Costo Sala (3 horas, 19% IVA, 10% Descuento): ${sala.calcular_costo(horas=3, impuesto=0.19, descuento=0.10)}")
        print(f"Costo Alquiler Equipo (2 días, sin seguro): ${equipo.calcular_costo(dias=2)}")
        
        # 4. Error forzado para probar logs
        print("\n--- FORZANDO ERROR DE CÁLCULO ---")
        sala.calcular_costo(horas=-5) # Esto lanzará excepción

    except SistemaGestionError as error:
        print(f"[X] Excepción capturada en ejecución: {error}")
        print("    (Revisa 'sistema_errores.log')")
    finally:
        print("\n-> Ejecución de pruebas finalizada.")