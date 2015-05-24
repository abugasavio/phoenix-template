# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse
from django.conf import settings


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize1(instance, delete_url, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.url)[0] or 'image/png',
        'thumbnailUrl': get_icon(obj),
        'size': obj.size,
        'deleteUrl': reverse(delete_url, args=[instance.pk]),
        'isImage': is_image(obj.url),
        'deleteType': 'DELETE',
    }

def serialize(instance, delete_url, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    """
    obj = getattr(instance, file_attr)
    return {
        'url': obj.url,
        'name': order_name(obj.name),
        'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        'thumbnailUrl': obj.url,
        'size': obj.size,
        'deleteUrl': reverse(delete_url, args=[instance.pk]),
        'deleteType': 'DELETE',
    }




def is_image(url):
    if mimetypes.guess_type(url)[0].split('/')[0] == 'image':
        return True
    return False


def get_icon(obj):
    mimetype = mimetypes.guess_type(obj.url)[0]
    upload_icons_url = settings.STATIC_URL + 'img/'
    if is_image(obj.url):
        icon = obj.url
    elif mimetype == 'application/pdf':
        icon = upload_icons_url + 'pdf-icon.png'
    elif mimetype in ('application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        icon = upload_icons_url + 'word-icon.png'
    elif mimetype == 'application/excel':
        icon = upload_icons_url + 'excel-icon.png'
    else:
        icon = upload_icons_url + 'unknown-icon.png'
    return icon
