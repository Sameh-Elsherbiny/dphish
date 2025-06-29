from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid
import ipaddress
from .tasks import fetch_ip_info


def index(request):
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def process_ips(request):
    try:
        data = json.loads(request.body)
        ip_list = data.get('ips', [])
        if len(ip_list) > 15 :
            return  JsonResponse({'error': 'Your maximum num of ips is 15 '},status=400)

        for ip in ip_list:
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                return JsonResponse({'error': f'Invalid IP: {ip}'}, status=400)

        task_id = str(uuid.uuid4())

        for ip in ip_list:
            fetch_ip_info.delay(task_id, ip)

        return JsonResponse({'task_id': task_id, 'status': 'Tasks submitted'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)