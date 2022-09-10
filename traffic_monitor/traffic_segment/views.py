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


"""
Get all traffic segments.
"""
@api_view(["GET"])
@csrf_exempt
def get_traffic_segments(request):
    segments = TrafficSegment.objects.all()
    serializer = TrafficSegmentSerializer(segments, many = True)
    return JsonResponse({'TrafficSegments': serializer.data}, safe = False, status = status.HTTP_200_OK)


"""
Add a new segment to DB.
Request body has the object.
"""
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


"""
Update traffic record.
Request body has new values to update the record.
"""
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


"""
Delete traffic segment record.
"""
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


"""
Get a segment matching given segment_id.
"""
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


"""
Get all segments matching characterization
0 - speed between 0 and 20 (inclusive)
1 - speed between 20 (exclusive) and 50 (inclusive)
2 - speed higher than 50 (exclusive) 
"""
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


"""
Manipulate speed on traffic segment record.
Depending on request method, different operations are made.

GET -> retrieve speed attribute from record.
POST/PUT -> change speed attribute from record.
DELETE -> delete speed attribute from record (empty value). 
"""
@api_view(["GET", "POST", "PUT", "DELETE"])
@csrf_exempt
def speed_operation_on_segment(request, segment_id):
    payload = json.loads(request.body)
    try:
        if request.method == "GET":
            segment_item = TrafficSegment.objects.get(id = segment_id)
            serializer = TrafficSegmentSerializer(segment_item)
            return JsonResponse({'Speed':serializer.data['speed']}, safe = False, status = status.HTTP_200_OK)
        
        elif request.method == "POST":
            segment_item = TrafficSegment.objects.get(id = segment_id)
            segment_item.speed = payload["speed"]
            segment_item.save()
            segment = TrafficSegment.objects.get(id = segment_id)
            serializer = TrafficSegmentSerializer(segment)
            return JsonResponse({'Speed':serializer.data['speed']}, safe = False, status = status.HTTP_200_OK)

        elif request.method == "PUT":
            try:   
                segment_item = TrafficSegment.objects.get(id = segment_id)
                segment_item.update(**payload)
                segment = TrafficSegment.objects.get(id = segment_id)
                serializer = TrafficSegmentSerializer(segment)
                return JsonResponse({'Speed':serializer.data['speed']}, safe = False, status = status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return JsonResponse({'error': 'Something went wrong ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR) 

        elif request.method == "DELETE":
            try:
                segment_item = TrafficSegment.objects.get(id = segment_id)
                segment_item.speed = ""
                segment_item.save()
                segment = TrafficSegment.objects.get(id = segment_id)
                serializer = TrafficSegmentSerializer(segment)
                return JsonResponse({'Speed':serializer.data['speed']}, safe = False, status = status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': str(e)}, safe = False, status = status.HTTP_404_NOT_FOUND)
            except Exception as ex:
                return JsonResponse({'error': 'Something went wrong ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(safe = False, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as ex:
        return JsonResponse({'error ' + str(ex)}, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)