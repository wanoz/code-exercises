from rest_framework import serializers

# Get all employees of given company
class Q1_serializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=264)

# Get all common friends of two given people
class Q2_serializer(serializers.Serializer):
    person_1_name = serializers.CharField(max_length=264)
    person_2_name = serializers.CharField(max_length=264)

# Get favourite fruits and vegetables of given person
class Q3_serializer(serializers.Serializer):
    person_name = serializers.CharField(max_length=264)