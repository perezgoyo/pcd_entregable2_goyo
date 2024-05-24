from abc import ABC, abstractmethod

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

# Clases Subscriptor y ManejadorTemperatura
class Subscriptor(ABC):
    @abstractmethod
    # Es un método abstracto porque luego la clase que hereda el método redefine el mismo(sobrecarga)
    def actualizar(self, evento):
        pass

class ManejadorTemperaturaAEstadistico(Subscriptor):
    def actualizar(self, evento):
        # Método que recibe la actualización del evento determinado por un Estadístico para A
        print("Manejador A Estadístico recibió:", evento)

class ManejadorTemperaturaAUmbral(Subscriptor):
    # Constructor de la clase
    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def actualizar(self, evento):
        # Método que recibe la actualización del evento determinado por un Umbral concreto para A
        timestamp, temperatura = evento
        umbral = 30.0 # Se recibe la notificación si la temperatura es mayor que el umbral determinado
        if temperatura > umbral:
            print("Temperatura supera el umbral:", temperatura)
        if self._siguiente:
            self._siguiente.actualizar(evento)

class ManejadorTemperaturaAAumento(Subscriptor):
    # Constructor de la clase
    def __init__(self, siguiente=None):
        self._siguiente = siguiente
        self.ultimas_temperaturas = []

    def actualizar(self, evento):
        # Método que recibe la actualización del evento determinado por un aumento de las temperaturas  para A
        self.ultimas_temperaturas.append(evento)
        if len(self.ultimas_temperaturas) > 6:  # asumiendo que se reciben datos cada 5 segundos
            self.ultimas_temperaturas.pop(0)

        if len(self.ultimas_temperaturas) == 6:
            # Recibe una notificación 
            temp_inicial = self.ultimas_temperaturas[0][1]
            temp_final = self.ultimas_temperaturas[-1][1]
            if temp_final - temp_inicial > 10:
                print("Temperatura aumentó más de 10 grados en los últimos 30 segundos.")

        if self._siguiente:
            self._siguiente.actualizar(evento)

class ManejadorTemperaturaBEstadistico(Subscriptor):
    # Método que recibe la actualización del evento determinado por un Estadístico para B
    def actualizar(self, evento):
        print("Manejador B Estadístico recibió:", evento)

class ManejadorTemperaturaBUmbral(Subscriptor):
    # Método que recibe la actualización del evento determinado por un Umbral concreto para B
    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def actualizar(self, evento):
        timestamp, temperatura = evento
        umbral = 22.0
        if temperatura > umbral:
            print("Temperatura supera el umbral:", temperatura)
        if self._siguiente:
            self._siguiente.actualizar(evento)

class ManejadorTemperaturaBAumento(Subscriptor):
    # Constructor de la clase
    def __init__(self, siguiente=None):
        self._siguiente = siguiente
        self.ultimas_temperaturas = []

    def actualizar(self, evento):
        # Método que recibe la actualización del evento determinado por un aumento de las temperaturas  para A
        self.ultimas_temperaturas.append(evento)
        if len(self.ultimas_temperaturas) > 4:
            self.ultimas_temperaturas.pop(0)

        if len(self.ultimas_temperaturas) == 4:
            temp_inicial = self.ultimas_temperaturas[0][1]
            temp_final = self.ultimas_temperaturas[-1][1]
            if temp_final - temp_inicial > 10:
                print("Temperatura aumentó más de 10 grados en los últimos 30 segundos.")

        if self._siguiente:
            self._siguiente.actualizar(evento)


