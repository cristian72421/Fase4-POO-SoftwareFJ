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
# 7. CLASE RESERVA (Integración)
# ==========================================
class Reserva(EntidadGeneral):
    """
    Integra cliente, servicio, duración y maneja el estado de la reserva.
    """
    def __init__(self, id_entidad, cliente, servicio, duracion_medida):
        super().__init__(id_entidad)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_medida = duracion_medida  # Horas, días o sesiones, dependiendo del servicio
        self.estado = "Pendiente" # Estados posibles: Pendiente, Confirmada, Cancelada

    def confirmar(self):
        try:
            if self.estado == "Confirmada":
                raise OperacionNoPermitidaError("La reserva ya se encuentra confirmada.")
            if self.estado == "Cancelada":
                raise OperacionNoPermitidaError("No se puede confirmar una reserva que fue cancelada.")
            self.estado = "Confirmada"
            return f"Reserva {self._id_entidad} confirmada con éxito."
        except OperacionNoPermitidaError as e:
            logger.error(f"Error al confirmar reserva {self._id_entidad}: {e}")
            raise

    def cancelar(self):
        try:
            if self.estado == "Cancelada":
                raise OperacionNoPermitidaError("La reserva ya se encontraba cancelada.")
            self.estado = "Cancelada"
            return f"Reserva {self._id_entidad} cancelada con éxito."
        except OperacionNoPermitidaError as e:
            logger.error(f"Error al cancelar reserva {self._id_entidad}: {e}")
            raise

    def mostrar_detalles(self):
        # Usamos la abstracción de la clase Servicio para calcular el costo base
        try:
            costo = self.servicio.calcular_costo(self.duracion_medida)
            return (f"--- Detalles Reserva ID: {self._id_entidad} ---\n"
                    f"Estado: {self.estado}\n"
                    f"Cliente: {self.cliente.obtener_nombre()} ({self.cliente.obtener_correo()})\n"
                    f"Servicio: {self.servicio.nombre_servicio}\n"
                    f"Costo Total: ${costo}\n"
                    f"----------------------------------")
        except DatoInvalidoError:
            return f"Reserva {self._id_entidad}: Error al calcular el costo por datos inválidos en la duración."

# ==========================================
# BLOQUE DE PRUEBA SECUENCIAL
# ==========================================
# ==========================================
# 8. SIMULACIÓN DE 10 OPERACIONES (Requisito Fase 4)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("INICIANDO SIMULACIÓN DE 10 OPERACIONES")
    print("="*50 + "\n")

    # Listas para simular nuestra "Base de Datos" en memoria sin usar motores externos
    clientes_db = []
    servicios_db = []
    reservas_db = []

    # Op 1: Registro válido de cliente
    try:
        c1 = Cliente("C001", "Carlos Perez", "carlos@mail.com")
        clientes_db.append(c1)
        print("Op 1 [Éxito]: Cliente registrado ->", c1.obtener_nombre())
    except Exception as e:
        print("Op 1 [Error no controlado]:", e)

    # Op 2: Registro inválido de cliente (Falta el arroba en el correo)
    try:
        c2 = Cliente("C002", "Ana", "correo_sin_arroba.com")
        clientes_db.append(c2)
    except DatoInvalidoError as e:
        print("Op 2 [Fallo Controlado]: No se pudo crear cliente ->", e)

    # Op 3: Creación correcta de servicio de sala
    try:
        s1 = ReservaSala("S001", capacidad_personas=20)
        servicios_db.append(s1)
        print("Op 3 [Éxito]: Servicio creado ->", s1.nombre_servicio)
    except Exception as e:
        print("Op 3 [Error no controlado]:", e)

    # Op 4: Creación correcta de servicio de equipo
    try:
        s2 = AlquilerEquipo("E001", tipo_equipo="Proyector 4K y Sonido")
        servicios_db.append(s2)
        print("Op 4 [Éxito]: Servicio creado ->", s2.nombre_servicio)
    except Exception as e:
        print("Op 4 [Error no controlado]:", e)

    # Op 5: Reserva exitosa (Carlos alquila la sala por 4 horas)
    try:
        r1 = Reserva("R001", clientes_db[0], servicios_db[0], duracion_medida=4)
        reservas_db.append(r1)
        print("Op 5 [Éxito]: Reserva creada en estado ->", r1.estado)
    except Exception as e:
        print("Op 5 [Error no controlado]:", e)

    # Op 6: Reserva fallida en cálculo (se envía una duración negativa)
    try:
        r2 = Reserva("R002", clientes_db[0], servicios_db[1], duracion_medida=-2)
        # El error detonará al intentar calcular el costo con días negativos
        print("Op 6 [Fallo Controlado]:", r2.mostrar_detalles())
    except Exception as e:
        print("Op 6 [Error]:", e)

    # Op 7: Confirmación exitosa de reserva
    try:
        msg = reservas_db[0].confirmar()
        print("Op 7 [Éxito]:", msg)
    except Exception as e:
        print("Op 7 [Error no controlado]:", e)

    # Op 8: Confirmación fallida (Se intenta confirmar la reserva que YA está confirmada)
    try:
        msg = reservas_db[0].confirmar()
        print("Op 8 [Éxito]:", msg)
    except OperacionNoPermitidaError as e:
        print("Op 8 [Fallo Controlado]:", e)

    # Op 9: Cancelación exitosa (Creamos una nueva reserva rápida solo para cancelarla)
    try:
        r3 = Reserva("R003", clientes_db[0], servicios_db[0], duracion_medida=1)
        reservas_db.append(r3)
        msg = r3.cancelar()
        print("Op 9 [Éxito]:", msg)
    except Exception as e:
        print("Op 9 [Error no controlado]:", e)

    # Op 10: Cancelación fallida (Se intenta cancelar la reserva que YA está cancelada)
    try:
        msg = r3.cancelar()
        print("Op 10 [Éxito]:", msg)
    except OperacionNoPermitidaError as e:
        print("Op 10 [Fallo Controlado]:", e)

    print("\n" + "="*50)
    print("RESUMEN DE DATOS EN MEMORIA")
    print("="*50)
    print(f"Total Clientes válidos en lista: {len(clientes_db)}")
    print(f"Total Servicios válidos en lista: {len(servicios_db)}")
    print(f"Total Reservas creadas en lista: {len(reservas_db)}")
    print("\nEl programa ejecutó todas las operaciones y manejó los errores sin detenerse.")