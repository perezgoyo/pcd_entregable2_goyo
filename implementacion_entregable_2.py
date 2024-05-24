# Clase Entorno
class Entorno:
    _instancia = None # Variable de clase para almacenar la única instancia

    def __init__(self):
        # Esta clase solo debe ser instanciada una vez
        if Entorno._instancia is not None:
            raise Exception("Esta clase es un singleton!") 
        else:
            self.sistema = "Sistema IoT" # Fijamos este sistema ya que es el que se pide en el enunciado
            self.datos = []
            self.publicador = PublicadorDatosSensor()
            Entorno._instancia = self # En el caso de no existir la instancia Singleton se crea con los atributos que debe tener

    @staticmethod
    def obtener_instancia():
        # Método estático para obtener la instancia única de la clase ConexionBD
        if Entorno._instancia is None:
            Entorno()
        return Entorno._instancia 

# Clase PublicadorDatosSensor
class PublicadorDatosSensor:
    def __init__(self):
        self._subscriptores = []
        self._datos = []

    def agregar(self, subscriptor):
        # Método para añadir subscriptores a la lista subscriptores
        if subscriptor not in self._subscriptores:
            self._subscriptores.append(subscriptor)

    def eliminar(self, subscriptor):
        # Método para eliminar subscriptores de la lista subscriptores
        if subscriptor in self._subscriptores:
            self._subscriptores.remove(subscriptor)

    def notificar_subscriptores(self):
        #Método para notificar a los subcriptores de los cambios que han sucedido
        for subscriptor in self._subscriptores:
            subscriptor.actualizar(self._datos[-1])

    def set_datos(self, timestamp, temperatura):
        # Método que asume que el sensor de temperatura envía, en cada mensaje una tupla (timestamp, t) donde timestamp es la fecha y hora en la que el sensor reportó la temperatura 
        self._datos.append((timestamp, temperatura))
        self.notificar_subscriptores()

    def obtener_datos(self, n=60):
        # Método para obtener los datos de los últimos 60 segundos para el cálculo de estadísticas
        return self._datos[-n:]



