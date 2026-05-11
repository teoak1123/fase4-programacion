# Sistema académico desarrollado en Python
class Estudiante:
    def __init__(self, nombre, edad, nota):
        self.nombre = nombre
        self.edad = edad
        self.nota = nota

    def mostrar_informacion(self):
        print("Nombre:", self.nombre)
        print("Edad:", self.edad)
        print("Nota:", self.nota)


class SistemaAcademico:
    def __init__(self):
        self.estudiantes = []

    def registrar_estudiante(self):
        try:
            nombre = input("Ingrese el nombre del estudiante: ").strip()

            if nombre == "":
                raise ValueError("El nombre no puede estar vacío")

            edad = int(input("Ingrese la edad del estudiante: "))

            if edad <= 0:
                raise ValueError("La edad debe ser mayor que cero")

            nota = float(input("Ingrese la nota final del estudiante: "))

            if nota < 0 or nota > 5:
                raise ValueError("La nota debe estar entre 0 y 5")

            estudiante = Estudiante(nombre, edad, nota)
            self.estudiantes.append(estudiante)

            print("Estudiante registrado correctamente")

        except ValueError as error:
            print("Error en los datos ingresados:", error)

        except Exception as error:
            print("Ocurrió un error inesperado:", error)

        finally:
            print("Proceso de registro finalizado\n")

    def mostrar_estudiantes(self):
        try:
            if len(self.estudiantes) == 0:
                raise Exception("No hay estudiantes registrados")

            print("\nListado de estudiantes")
            print("----------------------")

            for estudiante in self.estudiantes:
                estudiante.mostrar_informacion()
                print("----------------------")

        except Exception as error:
            print("Aviso:", error)

    def buscar_estudiante(self):
        try:
            nombre_buscar = input("Ingrese el nombre a buscar: ").strip()

            if nombre_buscar == "":
                raise ValueError("Debe ingresar un nombre para buscar")

            encontrado = False

            for estudiante in self.estudiantes:
                if estudiante.nombre.lower() == nombre_buscar.lower():
                    print("Estudiante encontrado:")
                    estudiante.mostrar_informacion()
                    encontrado = True

            if not encontrado:
                raise Exception("No se encontró un estudiante con ese nombre")

        except ValueError as error:
            print("Error:", error)

        except Exception as error:
            print("Aviso:", error)

    def eliminar_estudiante(self):
        try:
            nombre_eliminar = input("Ingrese el nombre del estudiante a eliminar: ").strip()

            if nombre_eliminar == "":
                raise ValueError("Debe ingresar un nombre válido")

            for estudiante in self.estudiantes:
                if estudiante.nombre.lower() == nombre_eliminar.lower():
                    self.estudiantes.remove(estudiante)
                    print("Estudiante eliminado correctamente")
                    return

            raise Exception("No se encontró el estudiante para eliminar")

        except ValueError as error:
            print("Error:", error)

        except Exception as error:
            print("Aviso:", error)


sistema = SistemaAcademico()

while True:
    print("\nSISTEMA ACADÉMICO")
    print("1. Registrar estudiante")
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
        print("Opción inválida. Intente nuevamente")
