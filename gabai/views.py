# Create your views here.
from dataclasses import dataclass

from django.http import JsonResponse
from firebase_admin import db


@dataclass
class FAQ:
    topic: str
    answer: str


def faqs(request):
    reference = db.reference("faq")

    def add_faq():
        new_faq = FAQ(topic, answer)
        reference.push(new_faq.__dict__)
        return JsonResponse({"success": True})

    def get_all_faq():
        faq_list = reference.get()
        return JsonResponse(faq_list)

    topic = request.GET.get("topic")
    answer = request.GET.get("answer")

    if topic and answer:
        return add_faq()
    else:
        return get_all_faq()