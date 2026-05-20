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
            raise ErrorDatoInvalido("El nombre del cliente no puede estar vacío")

        if not documento.strip():
            raise ErrorDatoInvalido("El documento del cliente no puede estar vacío")

        if "@" not in correo or "." not in correo:
            raise ErrorDatoInvalido("El correo electrónico del cliente no es válido")

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} | Documento: {self.__documento} | Correo: {self.__correo}"

    def get_nombre(self):
        return self.__nombre


class Servicio(ABC):
    def __init__(self, nombre, precio_base, disponible=True):
        if not nombre.strip():
            raise ErrorDatoInvalido("El nombre del servicio no puede estar vacío")

        if precio_base <= 0:
            raise ErrorDatoInvalido("El precio base del servicio debe ser mayor que cero")

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
            raise ErrorServicioNoDisponible(f"El servicio {self.nombre} no está disponible")


class ReservaSala(Servicio):
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        return (self.precio_base * duracion - descuento) + impuesto

    def describir_servicio(self):
        return "Reserva de salas para reuniones empresariales"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        seguro = 10000
        return (self.precio_base * duracion + seguro - descuento) + impuesto

    def describir_servicio(self):
        return "Alquiler de equipos tecnológicos"


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        costo_base = self.precio_base * duracion
        recargo_especializado = costo_base * 0.20
        return (costo_base + recargo_especializado - descuento) + impuesto

    def describir_servicio(self):
        return "Asesoría especializada profesional"


class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if cliente is None:
            raise ErrorReserva("La reserva debe tener un cliente asociado")

        if servicio is None:
            raise ErrorReserva("La reserva debe tener un servicio asociado")

        if duracion <= 0:
            raise ErrorReserva("La duración de la reserva debe ser mayor que cero")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            self.servicio.validar_disponibilidad()

        except ErrorServicioNoDisponible as error:
            raise ErrorReserva("No fue posible confirmar la reserva") from error

        else:
            self.estado = "Confirmada"
            guardar_log("INFO", "Reserva confirmada correctamente")

    def cancelar(self):
        try:
            if self.estado == "Cancelada":
                raise ErrorReserva("La reserva ya se encuentra cancelada")

            self.estado = "Cancelada"

        except ErrorReserva as error:
            guardar_log("ERROR", error)
            print("Error al cancelar:", error)

        else:
            guardar_log("INFO", "Reserva cancelada correctamente")
            print("Reserva cancelada correctamente")

        finally:
            print("Proceso de cancelación finalizado")

    def procesar(self):
        try:
            self.confirmar()

            costo = self.servicio.calcular_costo(
                self.duracion,
                descuento=5000,
                impuesto=3000
            )

            if costo <= 0:
                raise ErrorReserva("El cálculo del costo no es válido")

        except ErrorReserva as error:
            guardar_log("ERROR", error)
            print("Error en la reserva:", error)

        except Exception as error:
            guardar_log("ERROR", error)
            print("Error inesperado:", error)

        else:
            print("Reserva procesada correctamente")
            print(self.cliente.mostrar_info())
            print("Servicio:", self.servicio.nombre)
            print("Descripción:", self.servicio.describir_servicio())
            print("Duración:", self.duracion, "horas")
            print("Costo total:", costo)
            print("Estado:", self.estado)

            guardar_log("INFO", "Reserva procesada correctamente")

        finally:
            print("Proceso de reserva finalizado")


def ejecutar_simulaciones():
    clientes = []
    servicios = []
    reservas = []

    guardar_log("INFO", "Inicio del sistema Software FJ")

    print("\n===== SOFTWARE FJ =====")
    print("Sistema Integral de Gestión de Clientes, Servicios y Reservas")
    print("Simulaciones válidas e inválidas para evidenciar excepciones, logs y estabilidad.\n")

    print("Operación 1: Registro de cliente válido")
    try:
        cliente1 = Cliente("Carlos Pérez", "1001", "carlos@email.com")
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        clientes.append(cliente1)
        guardar_log("INFO", "Cliente Carlos Pérez registrado")
        print("Cliente registrado correctamente")

    print("\nOperación 2: Registro de segundo cliente válido")
    try:
        cliente2 = Cliente("Laura Gómez", "1002", "laura@email.com")
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        clientes.append(cliente2)
        guardar_log("INFO", "Cliente Laura Gómez registrado")
        print("Cliente registrado correctamente")

    print("\nOperación 3: Registro inválido de cliente sin nombre")
    try:
        Cliente("", "1003", "cliente@email.com")
    except Exception as error:
        guardar_log("ERROR", error)
        print("Cliente inválido:", error)

    print("\nOperación 4: Registro inválido de cliente sin documento")
    try:
        Cliente("Ana Torres", "", "ana@email.com")
    except Exception as error:
        guardar_log("ERROR", error)
        print("Documento inválido:", error)

    print("\nOperación 5: Registro inválido de cliente con correo incorrecto")
    try:
        Cliente("Pedro Ruiz", "1005", "correo_invalido")
    except Exception as error:
        guardar_log("ERROR", error)
        print("Correo inválido:", error)

    print("\nOperación 6: Creación de servicio válido de reserva de sala")
    try:
        servicio1 = ReservaSala("Sala Ejecutiva", 30000, True)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        servicios.append(servicio1)
        guardar_log("INFO", "Servicio Sala Ejecutiva creado")
        print("Servicio creado correctamente")

    print("\nOperación 7: Creación de servicio válido de alquiler de equipo")
    try:
        servicio2 = AlquilerEquipo("Video Beam", 20000, True)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        servicios.append(servicio2)
        guardar_log("INFO", "Servicio Video Beam creado")
        print("Servicio creado correctamente")

    print("\nOperación 8: Creación de servicio de asesoría no disponible")
    try:
        servicio3 = AsesoriaEspecializada("Asesoría en Software", 50000, False)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        servicios.append(servicio3)
        guardar_log("INFO", "Servicio Asesoría en Software creado como no disponible")
        print("Servicio creado correctamente, pero no disponible")

    print("\nOperación 9: Creación de servicio válido de asesoría empresarial")
    try:
        servicio4 = AsesoriaEspecializada("Asesoría Empresarial", 60000, True)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        servicios.append(servicio4)
        guardar_log("INFO", "Servicio Asesoría Empresarial creado")
        print("Servicio creado correctamente")

    print("\nOperación 10: Creación inválida de servicio con precio negativo")
    try:
        ReservaSala("Sala Básica", -10000, True)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Servicio inválido:", error)

    print("\nOperación 11: Creación inválida de servicio sin nombre")
    try:
        AlquilerEquipo("", 20000, True)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Nombre de servicio inválido:", error)

    print("\nOperación 12: Reserva exitosa de sala ejecutiva")
    try:
        reserva1 = Reserva(clientes[0], servicios[0], 2)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva1)
        reserva1.procesar()

    print("\nOperación 13: Reserva exitosa de alquiler de equipo")
    try:
        reserva2 = Reserva(clientes[1], servicios[1], 5)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva2)
        reserva2.procesar()

    print("\nOperación 14: Reserva exitosa de asesoría empresarial")
    try:
        reserva3 = Reserva(clientes[0], servicios[3], 3)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva3)
        reserva3.procesar()

    print("\nOperación 15: Reserva inválida con duración cero")
    try:
        Reserva(clientes[0], servicios[1], 0)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Reserva inválida:", error)

    print("\nOperación 16: Reserva inválida con duración negativa")
    try:
        Reserva(clientes[1], servicios[0], -4)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Reserva con duración negativa:", error)

    print("\nOperación 17: Reserva fallida por servicio no disponible")
    try:
        reserva4 = Reserva(clientes[0], servicios[2], 3)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva4)
        reserva4.procesar()

    print("\nOperación 18: Reserva inválida sin cliente")
    try:
        Reserva(None, servicios[0], 2)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Reserva sin cliente:", error)

    print("\nOperación 19: Reserva inválida sin servicio")
    try:
        Reserva(clientes[0], None, 2)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Reserva sin servicio:", error)

    print("\nOperación 20: Cancelación de reserva existente")
    if reservas:
        reservas[0].cancelar()

    print("\nOperación 21: Nueva reserva exitosa de sala")
    try:
        reserva5 = Reserva(clientes[1], servicios[0], 4)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva5)
        reserva5.procesar()

    print("\nOperación 22: Nueva reserva exitosa de equipo")
    try:
        reserva6 = Reserva(clientes[0], servicios[1], 1)
    except Exception as error:
        guardar_log("ERROR", error)
        print("Error:", error)
    else:
        reservas.append(reserva6)
        reserva6.procesar()

    print("\nOperación 23: Intento de cancelar nuevamente una reserva cancelada")
    if reservas:
        reservas[0].cancelar()

    guardar_log("INFO", "Total de clientes válidos registrados: " + str(len(clientes)))
    guardar_log("INFO", "Total de servicios válidos creados: " + str(len(servicios)))
    guardar_log("INFO", "Total de reservas creadas: " + str(len(reservas)))
    guardar_log("INFO", "Fin de simulaciones del sistema")

    print("\n===== RESUMEN FINAL =====")
    print("Operaciones simuladas: 23")
    print("Clientes válidos registrados:", len(clientes))
    print("Servicios válidos creados:", len(servicios))
    print("Reservas creadas:", len(reservas))
    print("Archivo de logs generado en:", RUTA_LOG)


try:
    ejecutar_simulaciones()

except Exception as error:
    guardar_log("ERROR", error)
    print("Error general del sistema:", error)

finally:
    guardar_log("INFO", "Fin de ejecución del programa")
    input("\nPresione Enter para cerrar...")
