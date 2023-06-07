# Create your views here.
import os.path
from collections import OrderedDict
from datetime import datetime
from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import db, storage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from apps.news.serializers import NewsSerializer


@api_view(['POST'])
@parser_classes([MultiPartParser])
def create_news_view(request: Request):
    print(request.data)
    serializer = NewsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data: OrderedDict = serializer.validated_data

    ref = db.reference("news")
    ref = ref.push({
        "title": data.get("title"),
        "content": data.get("content"),
        "timestamp": datetime.timestamp(datetime.now())
    })
    key = ref.key
    print(key)

    temp_files: List[InMemoryUploadedFile] = data.get("attachments")
    for temp_file in temp_files:
        blob = storage.bucket().blob(f"news{key}/{temp_file.name}")
        blob.upload_from_file(temp_file.file)

    return Response()


@api_view(['GET'])
@parser_classes([JSONParser])
def list_news_view(request: Request):
    data = db.reference("news").get()
    return Response(data)