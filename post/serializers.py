from rest_framework import serializers
from .models import Snack

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ('id','title','purchaser','description','created_at')