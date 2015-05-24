import os
from uuid import uuid4


def unique_filename(path):
    def wrapper(instance, filename):
        ext = os.path.splitext(filename)[1]
        # get filename
        if instance.pk:
            filename = '%s%s' % (instance.pk, ext)
        else:
            # set filename as random string
            filename = '%s%s' % (uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper