import pytest
from datetime import datetime
import random
from implementacion_entregable_2 import Entorno, PublicadorDatosSensor, ManejadorTemperaturaAEstadistico, ManejadorTemperaturaAUmbral, ManejadorTemperaturaAAumento, ProductorKafka, ConsumidorKafka, ComputarEstadisticoMediaSd, ComputarEstadisticoCuantiles, ComputarEstadisticoMaxMin, Contexto

class MockSubscriptor:
    def __init__(self):
        self.evento = None

    def actualizar(self, evento):
        self.evento = evento

@pytest.fixture
def publicador():
    return PublicadorDatosSensor()

@pytest.fixture
def entorno():
    return Entorno.obtener_instancia()

@pytest.fixture
def productor():
    return ProductorKafka()

@pytest.fixture
def consumidor(publicador):
    return ConsumidorKafka(publicador)

def test_singleton_entorno():
    entorno1 = Entorno.obtener_instancia()
    entorno2 = Entorno.obtener_instancia()
    assert entorno1 is entorno2

def test_publicador_notifica_subscriptor(publicador):
    subscriptor = MockSubscriptor()
    publicador.agregar(subscriptor)
    timestamp = datetime.now()
    temperatura = 25.0
    publicador.set_datos(timestamp, temperatura)
    assert subscriptor.evento == (timestamp, temperatura)

def test_manejador_temperatura_a_estadistico():
    manejador = ManejadorTemperaturaAEstadistico()
    assert manejador is not None

def test_productor_kafka(productor):
    timestamp, temperatura = productor.producir()
    assert isinstance(timestamp, datetime)
    assert 15.0 <= temperatura <= 35.0

def test_consumidor_kafka(consumidor, publicador):
    subscriptor = MockSubscriptor()
    publicador.agregar(subscriptor)
    mensaje = (datetime.now(), 22.5)
    consumidor.consumir(mensaje)
    assert subscriptor.evento == mensaje

def test_strategy():
    contexto = Contexto(ComputarEstadisticoMediaSd())
    datos = [(datetime.now(), random.uniform(15.0, 35.0)) for _ in range(60)]
    resultado = contexto.hacer_algo(datos)
    assert "media" in resultado and "desviacion_tipica" in resultado

    contexto.establecer_estrategia(ComputarEstadisticoCuantiles())
    resultado = contexto.hacer_algo(datos)
    assert "q1" in resultado and "mediana" in resultado and "q3" in resultado

    contexto.establecer_estrategia(ComputarEstadisticoMaxMin())
    resultado = contexto.hacer_algo(datos)
    assert "maximo" in resultado and "minimo" in resultado

def test_cadena_de_responsabilidad(publicador):
    manejador_estadistico_a = ManejadorTemperaturaAEstadistico()
    manejador_umbral_a = ManejadorTemperaturaAUmbral(manejador_estadistico_a)
    manejador_aumento_a = ManejadorTemperaturaAAumento(manejador_umbral_a)
    publicador.agregar(manejador_aumento_a)

    timestamp = datetime.now()
    temperatura = 25.0
    publicador.set_datos(timestamp, temperatura)

