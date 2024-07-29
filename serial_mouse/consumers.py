import json
from channels.generic.websocket import AsyncWebsocketConsumer
import cv2
import time
import os
from channels.db import database_sync_to_async
from .models import MouseData, Capture
from django.conf import settings


class SerialConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connection established."}))

    async def disconnect(self, close_code):
        print("WebSocket connection closed cleanly, code=", close_code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'mouse_move':
            await self.save_mouse_data(data['x'], data['y'])
        elif data['action'] == 'capture':
            await self.capture_image()

    @database_sync_to_async
    def save_mouse_data(self, x, y):
        MouseData.objects.create(x=x, y=y)

    @database_sync_to_async
    def capture_image(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            filename = f"captures/capture_{int(time.time())}.jpg"
            full_path = os.path.join(settings.MEDIA_ROOT, filename)
            cv2.imwrite(full_path, frame)
            Capture.objects.create(image=filename)
        cap.release()