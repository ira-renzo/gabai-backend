# Create your views here.
import base64
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import List

from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import db, storage
from google.cloud.storage import Blob
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from app.serializers import NewsSerializer


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


@api_view(['GET'])
@parser_classes([MultiPartParser])
def get_news_view(request: Request, news_id: str):
    data = db.reference("news").child(news_id).get()

    assert isinstance(data, dict)

    attachments = []
    for blob in storage.bucket().list_blobs(prefix=f"news{news_id}"):
        blob: Blob
        attachment = base64.b64encode(blob.download_as_bytes()).decode()
        attachments.append({
            "name": Path(blob.name).name,
            "data": attachment
        })
    data["attachments"] = attachments

    return Response(data)


@api_view(['POST'])
@parser_classes([JSONParser])
def get_chat_view(request: Request):
    print(request.data)
    reference = db.reference("chat").child("-NXPB7P57nHrp1mKrtn3")

    if "author" not in request.data or "content" not in request.data:
        return Response(reference.get())

    messages = reference.get()
    assert isinstance(messages, List)
    messages.append(request.data)

    content = request.data["content"].lower()
    bot_response = gabai_bot.get_response(content)

    if request.data["author"] != "Employee":
        messages.append({"author": "Auto Mode", "content": str(bot_response)})
        print(messages)

    reference.set(messages)
    return Response(messages)


@api_view(['POST'])
@parser_classes([JSONParser])
def topic_view(request: Request):
    reference = db.reference("topics")

    if request.data == {}:
        messages = reference.get()
        return Response(messages)

    if "conversation" in request.data:
        conversation = request.data["conversation"]
        reference.push(conversation)

    return Response()


gabai_bot = ChatBot(
    "Gabai",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
    ],
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        },
        'chatterbot.logic.MathematicalEvaluation',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry. I do not understand. Please wait for an actual employee to reply.',
            'maximum_similarity_threshold': 0.50,
            "statement_comparison_function": LevenshteinDistance,
            "response_selection_method": get_first_response,
        }
    ]
)