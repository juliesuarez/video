from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def mind(request):
    return render(request, 'mychat/mind.html')

def room(request):
    return render(request, 'mychat/room.html')

# def generate_agora_key(request):
#     app_id = 'a6f9801aa6d44a72bb10511e25a749fc'  
#     app_certificate = '6daaa587816344fcbf0682be4c79498a'  
#     user_id = request.GET.get('1,230')  # Get user ID from the request parameters
#     role = RtcRole.PUBLISHER
#     channel_name = 'channel'
#     expiration_time_in_seconds = 3600  # Set the expiration time as needed

#     key = RtcTokenBuilder.build_token_with_uid(
#         app_id, app_certificate, channel_name, user_id, role, expiration_time_in_seconds
#     )

#     return JsonResponse({'agora_key': key})

def getToken(request):
    appId = "a6f9801aa6d44a72bb10511e25a749fc"
    appCertificate = "6daaa587816344fcbf0682be4c79498a"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)
