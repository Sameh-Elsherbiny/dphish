import requests
from celery import shared_task
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def fetch_ip_info(task_id, ip):
    url = f"https://ipinfo.io/{ip}/json"
    headers = {"Authorization": f"Bearer {settings.IPINFO_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as e:
        result = {"error": str(e), "ip": ip}

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'task_{task_id}',
        {
            'type': 'ip.result',
            'task_id': task_id,
            'ip': ip,
            'result': result,
        }
    )
    return result