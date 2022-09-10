import json
from typing import Any
from xml.dom.minidom import CharacterData
from .models import TrafficSegment
from .serializers import TrafficSegmentSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


@api_view(["GET"])
@csrf_exempt
def get_traffic_segments(request):
    segments = TrafficSegment.objects.all()
    serializer = TrafficSegmentSerializer(segments, many = True)
    return JsonResponse({'TrafficSegments': serializer.data}, safe = False, status = status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
def add_segment(request):
    payload = json.loads(request.body)
    try:
        segment = TrafficSegment.objects.create(
            id = payload["id"],
            long_start = payload["long_start"],
            lat_start = payload["lat_start"],
            long_end = payload["long_end"],
            lat_end = payload["lat_end"],
            length = payload["length"],
            speed = payload["speed"]
        )
        serializer = TrafficSegmentSerializer(segment)
        return JsonResponse({'TrafficSegment': serializer.data}, safe = False, status = status.HTTP_201_CREATED)

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)

    except Exception as ex:
        return JsonResponse({'error': 'Something went wrong ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@csrf_exempt
def update_segment(request, segment_id):
    payload = json.loads(request.body)
    try:
        segment_item = TrafficSegment.objects.filter(id = segment_id)
        segment_item.update(**payload)
        segment = TrafficSegment.objects.get(id = segment_id)
        serializer = TrafficSegmentSerializer(segment)
        return JsonResponse({'TrafficSegment': serializer.data}, safe = False, status = status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'error': 'Something went wrong ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@csrf_exempt
def delete_segment(request, segment_id):
    #payload = json.loads(request.body)
    try:
        segment = TrafficSegment.objects.get(id = segment_id)
        segment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'error': 'Something went wrong ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
def get_segment_by_id(request, segment_id):
    try:
        segment_item = TrafficSegment.objects.get(id = segment_id)
        serializer = TrafficSegmentSerializer(segment_item)
        return JsonResponse({'TrafficSegment': serializer.data}, safe = False, status = status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return JsonResponse({'error': str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
def get_segments_by_characterization(request, characterization):
    try:
        if characterization == 0:
            segment_items = TrafficSegment.objects.filter(speed__lte = 20)
        elif characterization == 1:
            segment_items = TrafficSegment.objects.filter(speed__gt = 20, speed__lte = 50)
        elif characterization == 2:
            segment_items = TrafficSegment.objects.filter(speed__gt = 50)
        else:
            return JsonResponse({'error: charaterization value not found.'}, safe = False, status = status.HTTP_404_NOT_FOUND)
        
        serializer = TrafficSegmentSerializer(segment_items, many = True)
        return JsonResponse({'TrafficSegments' : serializer.data}, safe = True, status = status.HTTP_200_OK)

    except Exception as ex:
        return JsonResponse({'error': str(ex)}, safe = False, status = status.HTTP_404_NOT_FOUND)