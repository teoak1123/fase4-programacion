# Sistema académico desarrollado en Python
import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
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
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad}")
        print(f"Nota: {self.nota}")


class SistemaAcademico:
    def __init__(self):
        self.estudiantes = []

    def registrar_estudiante(self):

        try:
            nombre = input("Ingrese nombre: ").strip()

            if nombre == "":
                raise ValueError("El nombre está vacío")

            edad = int(input("Ingrese edad: "))

            if edad <= 0:
                raise ErrorEdad("La edad debe ser positiva")

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
            print("Ocurrió un error inesperado")

        else:
            estudiante = Estudiante(nombre, edad, nota)
            self.estudiantes.append(estudiante)
            print("Estudiante registrado correctamente")

        finally:
            print("Proceso finalizado\n")

    def mostrar_estudiantes(self):

        try:

            if len(self.estudiantes) == 0:
                raise Exception("No hay estudiantes registrados")

            for estudiante in self.estudiantes:
                print("----------------")
                estudiante.mostrar()

        except Exception as error:
            logging.error(error)
            print(error)

    def buscar_estudiante(self):

        try:
            nombre = input("Ingrese nombre a buscar: ")

            encontrado = False

            for estudiante in self.estudiantes:

                if estudiante.nombre.lower() == nombre.lower():
                    estudiante.mostrar()
                    encontrado = True

            if not encontrado:
                raise Exception("Estudiante no encontrado")

        except Exception as error:
            logging.error(error)
            print(error)

    def eliminar_estudiante(self):

        try:
            nombre = input("Ingrese nombre a eliminar: ")

            for estudiante in self.estudiantes:

                if estudiante.nombre.lower() == nombre.lower():
                    self.estudiantes.remove(estudiante)
                    print("Estudiante eliminado")
                    return

            raise Exception("No existe ese estudiante")

        except Exception as error:
            logging.error(error)
            print(error)


print("Bienvenido al sistema académico")

sistema = SistemaAcademico()

while True:

    print("\n1. Registrar estudiante")
    print("2. Mostrar estudiantes")
    print("3. Buscar estudiante")
    print("4. Eliminar estudiante")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        sistema.registrar_estudiante()

    elif opcion == "2":
        sistema.mostrar_estudiantes()

    elif opcion == "3":
        sistema.buscar_estudiante()

    elif opcion == "4":
        sistema.eliminar_estudiante()

    elif opcion == "5":
        print("Programa finalizado")
        break

    else:
        print("Opción inválida")
        print("Opción inválida. Intente nuevamente")
