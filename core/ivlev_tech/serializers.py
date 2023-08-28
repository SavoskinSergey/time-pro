from core.account.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from .models import Question
# from .utils import average_rating


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']


class QuestionSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['pk', 'name', 'body',
                  'date_created', 'date_edited', 'creator']

    def create(self, validated_data):
        request = self.context["request"]
        creator = request.user
        if not creator.is_authenticated:
            raise NotAuthenticated('Authentication required.')
        return Question.objects.create(
                    content=validated_data['content'], creator=creator
                    )

    def update(self, instance, validated_data):
        request = self.context['request']
        creator = request.user
        if not creator.is_authenticated or instance.creator_id != creator.pk:
            raise PermissionDenied('Permission denied, you are \
                                    not the creator of this question')
        instance.name = validated_data['name']
        instance.body = validated_data['body']
        instance.date_edited = timezone.now()
        instance.save()
        return instance
