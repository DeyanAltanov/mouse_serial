import os
import json
import cv2
import time
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .models import Capture, MouseData


def index(request):
    return render(request, 'serial_mouse/index.html')


def view_data(request):
    captures = Capture.objects.all()
    mouse_data = MouseData.objects.all()
    return render(request, 'serial_mouse/view_data.html', {
        'captures': captures,
        'mouse_data': mouse_data
    })


def mouse_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        MouseData.objects.create(x=data['x'], y=data['y'])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'}, status=400)


def capture_image(request):
    if request.method == 'POST':
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            captures_dir = os.path.join(settings.BASE_DIR, 'static', 'captures')
            if not os.path.exists(captures_dir):
                os.makedirs(captures_dir)
            filename = f'capture_{int(time.time())}.jpg'
            filepath = os.path.join(captures_dir, filename)
            cv2.imwrite(filepath, frame)
            Capture.objects.create(filename=f'captures/{filename}')
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure'}, status=400)