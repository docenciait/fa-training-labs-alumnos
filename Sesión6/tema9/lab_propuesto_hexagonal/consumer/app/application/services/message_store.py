from app.domain.entities import Evento

class MessageStore:
    mensajes: list[Evento] = []

    @classmethod
    def store(cls, evento: Evento):
        cls.mensajes.append(evento)

    @classmethod
    def list(cls):
        return [m.dict() for m in cls.mensajes]