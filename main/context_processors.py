import os

def image_tag(request):
    return {
        'IMAGE_TAG': os.environ.get('IMAGE_TAG', '')
    }
