from rest_framework import serializers
from .models import Lecturer, Document, PastQues, GenPastQues


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["file_url", "user", "created_at"]


class PastQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastQues
        fields = ["file_url", "lecturer", "created_at"]


class GeneratedPastQuestion(serializers.ModelSerializer):
    class Meta:
        model = GenPastQues
        fields = ["content", "lecturer", "created_at"]


class LecturerSerializer(serializers.ModelSerializer):
    past_ques = PastQuestionSerializer(read_only=True, many=True)
    gen_pq = GeneratedPastQuestion(read_only=True, many=True)

    class Meta:
        model = Lecturer
        fields = [
            "name",
            "image",
            "email",
            "user",
            "created_at",
            "past_ques",
            "gen_pq",
        ]
