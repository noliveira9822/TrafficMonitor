from rest_framework import serializers

from .models import TrafficSegment

class TrafficSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficSegment
        fields = ['id', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length', 'speed']