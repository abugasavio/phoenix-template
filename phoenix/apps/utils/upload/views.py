import json
from django.views.generic import CreateView, ListView, DeleteView
from django.http import HttpResponse
from .response import JSONResponse, response_mimetype
from .serialize import serialize


class UploadView(CreateView):

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object, self.delete_url)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class UploadListView(ListView):

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(f, self.delete_url) for f in self.get_queryset()]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class UploadDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
