import os

def image_tag_timestamp(request):
    return {
        'IMAGE_TAG_TIMESTAMP': os.environ.get('IMAGE_TAG_TIMESTAMP', '')
    }
