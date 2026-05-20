from abc import ABC, abstractmethod
from datetime import datetime
import os

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_LOG = os.path.join(CARPETA_ACTUAL, "logs.txt")


def guardar_log(tipo, mensaje):
    with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"{fecha} - {tipo} - {mensaje}\n")


class ErrorDatoInvalido(Exception):
    pass


class ErrorServicioNoDisponible(Exception):
    pass


class ErrorReserva(Exception):
    pass


class EntidadSistema(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


class Cliente(EntidadSistema):

    def __init__(self, nombre, documento, correo):

        if not nombre.strip():
            raise ErrorDatoInvalido("El nombre no puede estar vacío")

        if not documento.strip():
            raise ErrorDatoInvalido("El documento no puede estar vacío")

        if "@" not in correo:
            raise ErrorDatoInvalido("Correo electrónico inválido")

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

    def mostrar_info(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo}"
        )

    def get_nombre(self):
        return self.__nombre


class Servicio(ABC):

    def __init__(self, nombre, precio_base, disponible=True):

        if precio_base <= 0:
            raise ErrorDatoInvalido("El precio base debe ser mayor que cero")

        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def validar_disponibilidad(self):

        if not self.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio {self.nombre} no está disponible"
            )


class ReservaSala(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        return (self.precio_base * duracion - descuento) + impuesto

    def describir_servicio(self):
        return "Reserva de salas empresariales"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        return (self.precio_base * duracion - descuento) + impuesto

    def describir_servicio(self):
        return "Alquiler de equipos tecnológicos"


class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        costo = self.precio_base * duracion
        recargo = costo * 0.20

        return (costo + recargo - descuento) + impuesto

    def describir_servicio(self):
        return "Asesoría especializada profesional"


class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ErrorReserva(
                "La duración de la reserva debe ser mayor que cero"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):

        try:
            self.servicio.validar_disponibilidad()

        except ErrorServicioNoDisponible as error:
            raise ErrorReserva(
                "No fue posible confirmar la reserva"
            ) from error

        else:
            self.estado = "Confirmada"
            guardar_log("INFO", "Reserva confirmada correctamente")

    def cancelar(self):

        self.estado = "Cancelada"

        guardar_log("INFO", "Reserva cancelada")

    def procesar(self):

        try:
            self.confirmar()

            costo = self.servicio.calcular_costo(
                self.duracion,
                descuento=5000,
                impuesto=3000
            )

        except ErrorReserva as error:

            guardar_log("ERROR", error)

            print("Error en la reserva:", error)

        except Exception as error:

            guardar_log("ERROR", error)

            print("Error inesperado:", error)

        else:

            print("\n===== RESERVA PROCESADA =====")
            print(self.cliente.mostrar_info())
            print("Servicio:", self.servicio.nombre)
            print("Descripción:", self.servicio.describir_servicio())
            print("Duración:", self.duracion, "horas")
            print("Costo total:", costo)
            print("Estado:", self.estado)

            guardar_log("INFO", "Reserva procesada correctamente")

        finally:

            print("Proceso finalizado")


clientes = []
servicios = []
reservas = []


try:

    guardar_log("INFO", "Inicio del sistema Software FJ")

    print("\n===== SOFTWARE FJ =====")

    cliente1 = Cliente(
        "Carlos Pérez",
        "1001",
        "carlos@email.com"
    )

    clientes.append(cliente1)

    guardar_log("INFO", "Cliente válido registrado")

    try:
        cliente2 = Cliente("", "1002", "correo@email.com")

    except Exception as error:
        guardar_log("ERROR", error)
        print("Cliente inválido:", error)

    try:
        cliente3 = Cliente("Ana", "1003", "correo_invalido")

    except Exception as error:
        guardar_log("ERROR", error)
        print("Correo inválido:", error)

    servicio1 = ReservaSala(
        "Sala Ejecutiva",
        30000,
        True
    )

    servicios.append(servicio1)

    guardar_log("INFO", "Servicio de sala creado")

    servicio2 = AlquilerEquipo(
        "Video Beam",
        20000,
        True
    )

    servicios.append(servicio2)

    guardar_log("INFO", "Servicio de equipo creado")

    servicio3 = AsesoriaEspecializada(
        "Asesoría Software",
        50000,
        False
    )

    servicios.append(servicio3)

    guardar_log("INFO", "Servicio no disponible registrado")

    try:
        servicio4 = ReservaSala(
            "Sala Básica",
            -10000,
            True
        )

    except Exception as error:
        guardar_log("ERROR", error)
        print("Servicio inválido:", error)

    reserva1 = Reserva(cliente1, servicio1, 2)

    reservas.append(reserva1)

    reserva1.procesar()

    try:
        reserva2 = Reserva(cliente1, servicio2, 0)

    except Exception as error:
        guardar_log("ERROR", error)
        print("Reserva inválida:", error)

    reserva3 = Reserva(cliente1, servicio3, 3)

    reservas.append(reserva3)

    reserva3.procesar()

    reserva1.cancelar()

    print("\nReserva cancelada correctamente")

    reserva4 = Reserva(cliente1, servicio2, 5)

    reservas.append(reserva4)

    reserva4.procesar()

except Exception as error:

    guardar_log("ERROR", error)

    print("Error general del sistema:", error)

finally:

    guardar_log("INFO", "Fin de ejecución del sistema")

    input("\nPresione Enter para cerrar...")
