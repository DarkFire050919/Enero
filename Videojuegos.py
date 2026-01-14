import ZODB
import ZODB.FileStorage
import persistent
import BTrees.OOBTree
import re
from typing import List, Optional

class Videojuego(persistent.Persistent):
    """Clase que representa un videojuego en la base de datos"""
    
    def __init__(self, nombre: str, edad: str, dificultad: str, horas_aprox: float, 
                 plataforma: str, precio: float):
        self.nombre = nombre
        self.edad = edad
        self.dificultad = dificultad
        self.horas_aprox = horas_aprox
        self.plataforma = plataforma
        self.precio = precio
    
    def __str__(self):
        return (f"Nombre: {self.nombre}\n"
                f"Edad: {self.edad}\n"
                f"Dificultad: {self.dificultad}\n"
                f"Horas aprox: {self.horas_aprox}\n"
                f"Plataforma: {self.plataforma}\n"
                f"Precio: ${self.precio:.2f}")
    
    def contiene_texto(self, texto: str) -> bool:
        """Verifica si el videojuego contiene el texto en alguno de sus campos"""
        texto = texto.lower()
        return (texto in self.nombre.lower() or
                texto in self.edad.lower() or
                texto in self.dificultad.lower() or
                texto in str(self.horas_aprox).lower() or
                texto in self.plataforma.lower() or
                texto in str(self.precio).lower())

class SistemaVideojuegos:
    """Sistema principal para gestionar videojuegos"""
    
    def __init__(self, db_path: str = "videojuegos.db"):
        self.db_path = db_path
        self.storage = None
        self.db = None
        self.connection = None
        self.videojuegos = None
        self._inicializar_db()
    
    def _inicializar_db(self):
        """Inicializa la base de datos y la conexión"""
        try:
            self.storage = ZODB.FileStorage.FileStorage(self.db_path)
            self.db = ZODB.DB(self.storage)
            self.connection = self.db.open()
            self.videojuegos = self.connection.root().get('videojuegos')
            
            if self.videojuegos is None:
                self.videojuegos = BTrees.OOBTree.BTree()
                self.connection.root().videojuegos = self.videojuegos
                print("Base de datos inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
    
    def agregar_videojuego(self):
        """Agrega un nuevo videojuego a la base de datos"""
        print("\n--- AGREGAR VIDEOJUEGO ---")
        
        try:
            nombre = input("Nombre: ")
            edad = input("Clasificación por edad (Ej: E, T, M, A): ")
            dificultad = input("Dificultad (Ej: Fácil, Medio, Difícil): ")
            
            try:
                horas_aprox = float(input("Horas aproximadas de juego: "))
            except ValueError:
                print("Error: Las horas deben ser un número.")
                return
            
            plataforma = input("Plataforma (Ej: PC, PS5, Xbox, Switch): ")
            
            try:
                precio = float(input("Precio: $"))
            except ValueError:
                print("Error: El precio debe ser un número.")
                return
            
            # Crear ID único
            juego_id = len(self.videojuegos) + 1
            videojuego = Videojuego(nombre, edad, dificultad, horas_aprox, plataforma, precio)
            self.videojuegos[juego_id] = videojuego
            
            # Guardar cambios
            import transaction
            transaction.commit()
            
            print(f"Videojuego '{nombre}' agregado con ID: {juego_id}")
            
        except Exception as e:
            print(f"Error al agregar videojuego: {e}")
    
    def editar_videojuego(self):
        """Edita un videojuego existente"""
        print("\n--- EDITAR VIDEOJUEGO ---")
        self.mostrar_todos()
        
        try:
            juego_id = int(input("ID del videojuego a editar: "))
            
            if juego_id not in self.videojuegos:
                print("Error: ID no encontrado.")
                return
            
            juego = self.videojuegos[juego_id]
            print(f"\nEditando: {juego.nombre}")
            print("(Deja en blanco para mantener el valor actual)")
            
            nombre = input(f"Nombre [{juego.nombre}]: ") or juego.nombre
            edad = input(f"Edad [{juego.edad}]: ") or juego.edad
            dificultad = input(f"Dificultad [{juego.dificultad}]: ") or juego.dificultad
            
            horas_input = input(f"Horas aprox [{juego.horas_aprox}]: ")
            horas_aprox = float(horas_input) if horas_input else juego.horas_aprox
            
            plataforma = input(f"Plataforma [{juego.plataforma}]: ") or juego.plataforma
            
            precio_input = input(f"Precio [${juego.precio:.2f}]: $")
            precio = float(precio_input) if precio_input else juego.precio
            
            # Actualizar el objeto
            juego.nombre = nombre
            juego.edad = edad
            juego.dificultad = dificultad
            juego.horas_aprox = horas_aprox
            juego.plataforma = plataforma
            juego.precio = precio
            
            # Marcar como modificado
            juego._p_changed = True
            
            # Guardar cambios
            import transaction
            transaction.commit()
            
            print(f"Videojuego '{nombre}' actualizado correctamente.")
            
        except ValueError:
            print("Error: ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al editar videojuego: {e}")
    
    def eliminar_videojuego(self):
        """Elimina un videojuego de la base de datos"""
        print("\n--- ELIMINAR VIDEOJUEGO ---")
        self.mostrar_todos()
        
        try:
            juego_id = int(input("ID del videojuego a eliminar: "))
            
            if juego_id not in self.videojuegos:
                print("Error: ID no encontrado.")
                return
            
            juego = self.videojuegos[juego_id]
            confirmacion = input(f"¿Estás seguro de eliminar '{juego.nombre}'? (s/n): ")
            
            if confirmacion.lower() == 's':
                del self.videojuegos[juego_id]
                
                # Guardar cambios
                import transaction
                transaction.commit()
                
                print(f"Videojuego '{juego.nombre}' eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
                
        except ValueError:
            print("Error: ID debe ser un número entero.")
        except Exception as e:
            print(f"Error al eliminar videojuego: {e}")
    
    def buscar_videojuegos(self):
        """Busca videojuegos por cualquier campo usando texto libre"""
        print("\n--- BUSCAR VIDEOJUEGOS ---")
        
        if not self.videojuegos:
            print("No hay videojuegos en la base de datos.")
            return
        
        texto_busqueda = input("Texto a buscar (en nombre, edad, dificultad, horas, plataforma o precio): ").strip()
        
        if not texto_busqueda:
            print("Por favor ingresa un texto para buscar.")
            return
        
        resultados = []
        
        for juego_id, juego in self.videojuegos.items():
            if juego.contiene_texto(texto_busqueda):
                resultados.append((juego_id, juego))
        
        if resultados:
            print(f"\nSe encontraron {len(resultados)} resultado(s):")
            print("-" * 50)
            for juego_id, juego in resultados:
                print(f"ID: {juego_id}")
                print(juego)
                print("-" * 30)
        else:
            print("No se encontraron videojuegos que coincidan con la búsqueda.")
    
    def mostrar_todos(self):
        """Muestra todos los videojuegos en la base de datos"""
        print("\n--- TODOS LOS VIDEOJUEGOS ---")
        
        if not self.videojuegos:
            print("No hay videojuegos en la base de datos.")
            return
        
        for juego_id, juego in self.videojuegos.items():
            print(f"ID: {juego_id}")
            print(juego)
            print("-" * 30)
    
    def menu_principal(self):
        """Muestra el menú principal del sistema"""
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE BÚSQUEDA DE VIDEOJUEGOS")
            print("="*50)
            print("1. Agregar videojuego")
            print("2. Editar videojuego")
            print("3. Eliminar videojuego")
            print("4. Buscar videojuegos")
            print("5. Mostrar todos los videojuegos")
            print("6. Salir")
            print("-"*50)
            
            opcion = input("Selecciona una opción (1-6): ").strip()
            
            if opcion == '1':
                self.agregar_videojuego()
            elif opcion == '2':
                self.editar_videojuego()
            elif opcion == '3':
                self.eliminar_videojuego()
            elif opcion == '4':
                self.buscar_videojuegos()
            elif opcion == '5':
                self.mostrar_todos()
            elif opcion == '6':
                print("¡Hasta luego!")
                self.cerrar()
                break
            else:
                print("Opción no válida. Por favor selecciona 1-6.")
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
        if self.db:
            self.db.close()

def main():
    """Función principal"""
    sistema = SistemaVideojuegos()
    
    try:
        sistema.menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sistema.cerrar()
    except Exception as e:
        print(f"Error inesperado: {e}")
        sistema.cerrar()

if __name__ == "__main__":
    main()