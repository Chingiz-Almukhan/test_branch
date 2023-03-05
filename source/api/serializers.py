from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from applications.models import Application
from education.models import Subject


class ApplicationCreateSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(required=True, max_length=20, allow_blank=False)
    applicant_surname = serializers.CharField(required=True, max_length=20, allow_blank=False)
    email = serializers.CharField(required=True, max_length=164, allow_blank=False, allow_null=False)
    subjects = PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, allow_empty=False)

    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_surname', 'email', 'phone', 'subjects']


class ApplicationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'
