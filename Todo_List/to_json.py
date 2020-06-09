from rest_framework import serializers
from .models import Note


class Note_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('note_title', 'task_text', 'real_date', 'dead_line', 'status')

