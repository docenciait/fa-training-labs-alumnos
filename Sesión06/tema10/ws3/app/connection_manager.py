from fastapi import WebSocket
from typing import List, Set, Dict
import logging

logger = logging.getLogger("connection_manager")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []  # guarda las conexiones vivas
        self.rooms: Dict[str, Set[WebSocket]] = {} # rooms identificadas por un id str y un conjunto de clientes
        logger.info("✅ ConnectionManager inicializado.")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"🔌 Conexión aceptada: {self._client_id(websocket)}. Total activos: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        client_id = self._client_id(websocket)
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"❌ Cliente desconectado: {client_id}. Activos restantes: {len(self.active_connections)}")
        
        rooms_to_clean = []
        for room_id, members in self.rooms.items():
            if websocket in members:
                members.remove(websocket)
                logger.info(f"🚪 Cliente {client_id} eliminado de sala '{room_id}'")
                if not members:
                    rooms_to_clean.append(room_id)
        
        for room_id in rooms_to_clean:
            del self.rooms[room_id]
            logger.info(f"🧹 Sala vacía eliminada: '{room_id}'")

    async def broadcast_to_all(self, message: str):
        logger.info(f"📢 Enviando a todos los clientes ({len(self.active_connections)}): {message}")
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"⚠️ Error al enviar a {self._client_id(connection)}: {e}")
                self.disconnect(connection)

    async def join_room(self, room_id: str, websocket: WebSocket):
        # join_room: crea la sala si no existe y añade el cliente.
        client_id = self._client_id(websocket)
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
            logger.info(f"🆕 Sala creada: '{room_id}'")
        
        if websocket not in self.rooms[room_id]:
            self.rooms[room_id].add(websocket)
            logger.info(f"➕ {client_id} se unió a sala '{room_id}'. Total en sala: {len(self.rooms[room_id])}")
            await self.send_to_room(room_id, f"👤 {client_id} se ha unido a la sala.", exclude_sender=None)

    async def leave_room(self, room_id: str, websocket: WebSocket):
        # leave_room: lo elimina de la sala y borra la sala si queda vacía.
        client_id = self._client_id(websocket)
        if room_id in self.rooms and websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
            logger.info(f"➖ {client_id} salió de la sala '{room_id}'")
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                logger.info(f"🧹 Sala '{room_id}' eliminada (vacía)")
            await self.send_to_room(room_id, f"🚪 {client_id} salió de la sala.", exclude_sender=None)

    async def send_to_room(self, room_id: str, message: str, exclude_sender: WebSocket = None):
        # Envía un mensaje a todos los miembros de la sala, excepto quien lo envió.
        
        if room_id not in self.rooms:
            logger.warning(f"⚠️ Intento de enviar a sala inexistente: '{room_id}'")
            return
        logger.info(f"📨 Enviando mensaje a sala '{room_id}': {message}")
        for ws in list(self.rooms[room_id]):
            if ws != exclude_sender:
                try:
                    await ws.send_text(message)
                except Exception as e:
                    logger.error(f"⚠️ Error enviando a cliente en '{room_id}': {e}")
                    self.disconnect(ws)

    def _client_id(self, websocket: WebSocket) -> str:
        return f"{websocket.client.host}:{websocket.client.port}"
