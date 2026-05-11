import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class ErrorNota(Exception):
    pass


class ErrorEdad(Exception):
    pass


class Estudiante:
    def __init__(self, nombre, edad, nota):
        self.nombre = nombre
        self.edad = edad
        self.nota = nota

    def mostrar(self):
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Nota:", self.nota)


class SistemaAcademico:
    def __init__(self):
        self.estudiantes = []

    def registrar_estudiante(self):
        try:
            nombre = input("Ingrese nombre: ").strip()

            if nombre == "":
                raise ValueError("El nombre no puede estar vacío")

            edad = int(input("Ingrese edad: "))

            if edad <= 0:
                raise ErrorEdad("La edad debe ser mayor que cero")

            nota = float(input("Ingrese nota: "))

            if nota < 0 or nota > 5:
                raise ErrorNota("La nota debe estar entre 0 y 5")

        except ValueError as error:
            logging.error(error)
            print("Error:", error)

        except ErrorEdad as error:
            logging.error(error)
            print("Error:", error)

        except ErrorNota as error:
            logging.error(error)
            print("Error:", error)

        except Exception as error:
            logging.error(error)
            print("Ocurrió un error inesperado:", error)

        else:
            estudiante = Estudiante(nombre, edad, nota)
            self.estudiantes.append(estudiante)
            logging.info("Estudiante registrado correctamente")
            print("Estudiante registrado correctamente")

        finally:
            print("Proceso de registro finalizado")

    def mostrar_estudiantes(self):
        try:
            if len(self.estudiantes) == 0:
                raise Exception("No hay estudiantes registrados")

            print("\nListado de estudiantes")
            print("----------------------")

            for estudiante in self.estudiantes:
                estudiante.mostrar()
                print("----------------------")

            logging.info("Listado de estudiantes consultado")

        except Exception as error:
            logging.error(error)
            print("Aviso:", error)

    def buscar_estudiante(self):
        try:
            nombre = input("Ingrese nombre a buscar: ").strip()

            if nombre == "":
                raise ValueError("Debe ingresar un nombre")

            encontrado = False

            for estudiante in self.estudiantes:
                if estudiante.nombre.lower() == nombre.lower():
                    print("Estudiante encontrado")
                    estudiante.mostrar()
                    encontrado = True

            if not encontrado:
                raise Exception("Estudiante no encontrado")

        except Exception as error:
            logging.error(error)
            print("Aviso:", error)

    def eliminar_estudiante(self):
        try:
            nombre = input("Ingrese nombre a eliminar: ").strip()

            if nombre == "":
                raise ValueError("Debe ingresar un nombre")

            for estudiante in self.estudiantes:
                if estudiante.nombre.lower() == nombre.lower():
                    self.estudiantes.remove(estudiante)
                    logging.info("Estudiante eliminado correctamente")
                    print("Estudiante eliminado correctamente")
                    return

            raise Exception("No existe ese estudiante")

        except Exception as error:
            logging.error(error)
            print("Aviso:", error)


def menu():
    sistema = SistemaAcademico()

    while True:
        print("\nSISTEMA ACADÉMICO")
        print("1. Registrar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Buscar estudiante")
        print("4. Eliminar estudiante")
        print("5. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            sistema.registrar_estudiante()

        elif opcion == "2":
            sistema.mostrar_estudiantes()

        elif opcion == "3":
            sistema.buscar_estudiante()

        elif opcion == "4":
            sistema.eliminar_estudiante()

        elif opcion == "5":
            logging.info("Programa finalizado")
            print("Programa finalizado")
            break

        else:
            logging.error("Opción inválida ingresada")
            print("Opción inválida")


try:
    print("Bienvenido al sistema académico")
    menu()

except Exception as error:
    logging.error(error)
    print("Error general del sistema:", error)

finally:
    input("Presione Enter para cerrar...")
