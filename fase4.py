class Estudiante:
    def __init__(self, nombre, edad, nota):
        self.nombre = nombre
        self.edad = edad
        self.nota = nota

    def mostrar(self):
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad}")
        print(f"Nota: {self.nota}")


class SistemaEstudiantes:
    def __init__(self):
        self.estudiantes = []

    def agregar_estudiante(self):
        try:
            nombre = input("Ingrese el nombre: ")

            edad = int(input("Ingrese la edad: "))
            if edad <= 0:
                raise ValueError("La edad debe ser positiva")

            nota = float(input("Ingrese la nota: "))
            if nota < 0 or nota > 5:
                raise ValueError("La nota debe estar entre 0 y 5")

            estudiante = Estudiante(nombre, edad, nota)
            self.estudiantes.append(estudiante)

            print("Estudiante agregado correctamente")

        except ValueError as error:
            print(f"Error: {error}")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

        finally:
            print("Proceso finalizado\n")

    def mostrar_estudiantes(self):
        if not self.estudiantes:
            print("No hay estudiantes registrados")
            return

        for estudiante in self.estudiantes:
            estudiante.mostrar()
            print("----------------")


sistema = SistemaEstudiantes()

while True:
    print("1. Agregar estudiante")
    print("2. Mostrar estudiantes")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        sistema.agregar_estudiante()

    elif opcion == "2":
        sistema.mostrar_estudiantes()

    elif opcion == "3":
        print("Programa finalizado")
        break

    else:
        print("Opción inválida")
