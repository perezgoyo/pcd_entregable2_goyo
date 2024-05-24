import pytest
from datetime import datetime
from implementacion_entregable_2 import Entorno, PublicadorDatosSensor

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

