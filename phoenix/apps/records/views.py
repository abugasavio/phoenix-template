from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from smartmin.views import SmartCRUDL, SmartCreateView, SmartReadView, SmartListView
from phoenix.apps.animals.models import Animal
from phoenix.apps.utils.upload.views import UploadView, UploadListView, UploadDeleteView
from .models import AnimalNote, AnimalDocument


class AnimalDocumentUploadView(UploadView):
    model = AnimalDocument
    delete_url = 'records.animaldocument_delete'

    def get_context_data(self, **kwargs):
        context = super(AnimalDocumentUploadView, self).get_context_data(**kwargs)
        #context['animal'] = self.request.animal
        return context


class AnimalDocumentListView(UploadListView):
    model = AnimalDocument
    delete_url = 'records.animaldocument_delete'

    def get_queryset(self):
        return AnimalDocument.objects.all()# filter(animal=self.kwargs['animal_id']).filter(deleted=False)


class AnimalDocumentDeleteView(UploadDeleteView):
    model = AnimalDocument


class AnimalNoteCRUDL(SmartCRUDL):
    model = AnimalNote

    class FormMixin(object):

        def __init__(self, **kwargs):
            # Prevent cyclic import errors
            from .forms import AnimalNoteForm
            self.form_class = AnimalNoteForm
            super(AnimalNoteCRUDL.FormMixin, self).__init__(**kwargs)

    class Create(FormMixin, SmartCreateView):

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)
            if not animal_id:
                messages.warning(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return super(AnimalNoteCRUDL.Create, self).get(request, *args, **kwargs)

        def pre_save(self, obj):
            animal_id = self.request.GET.get('animal', None)
            try:
                animal = Animal.objects.get(id=animal_id)
            except AnimalNote.DoesNotExist:
                messages.error(self.request, 'Animal Id is required')
            else:
                obj.animal = animal
            return obj

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal', None)])

    class Read(SmartReadView):
        fields = ('id', 'date', 'file', 'details', 'created', 'modified')

        def get_file(self, obj):
            return '<a href=' + obj.file.url + '>' + obj.file.name + '</a>'

    class List(SmartListView):
        fields = ('id', 'date', 'file', 'details')

        def get_file(self, obj):
            if obj.file:
                return '<a href=' + obj.file.url + '>' + obj.file.name + '</a>'
            return ''

        def get_queryset(self, **kwargs):
            queryset = super(AnimalNoteCRUDL.List, self).get_queryset(**kwargs)
            queryset = queryset.filter(animal=self.request.animal)
            return queryset


# class AnimalGroupNoteCRUDL(SmartCRUDL):
#     model = AnimalGroupNote
#
#     class FormMixin(object):
#
#         def __init__(self, **kwargs):
#             # Prevent cyclic import errors
#             from .forms import AnimalGroupNoteForm
#             self.form_class = AnimalGroupNoteForm
#             super(AnimalGroupNoteCRUDL.FormMixin, self).__init__(**kwargs)
#
#     class Create(FormMixin, SmartCreateView):
#
#         def get(self, request, *args, **kwargs):
#             animalgroup_id = request.GET.get('group', None)
#             if not animalgroup_id:
#                 messages.warning(request, 'Animal Group Id is required')
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#             return super(AnimalGroupNoteCRUDL.Create, self).get(request, *args, **kwargs)
#
#         def pre_save(self, obj):
#             animalgroup_id = self.request.GET.get('group', None)
#             try:
#                 animalgroup = AnimalGroup.objects.get(id=animalgroup_id)
#             except AnimalGroup.DoesNotExist:
#                 messages.error(self.request, 'Animal Id is required')
#             else:
#                 obj.animalgroup = animalgroup
#             return obj
#
#         def get_success_url(self):
#             return reverse('groups.animalgroup_read', args=[self.request.GET.get('group', None)])
#
#     class Read(SmartReadView):
#         fields = ('id', 'date', 'file', 'details', 'created', 'modified')
#
#         def get_file(self, obj):
#             if obj.file:
#                 return '<a href=' + obj.file.url + '>' + obj.file.name + '</a>'
#             return ''
#
#     class List(SmartListView):
#         fields = ('id', 'date', 'file', 'details')
#
#         def get_file(self, obj):
#             if obj.file:
#                 return '<a href=' + obj.file.url + '>' + obj.file.name + '</a>'
#             return ''
#
#         def get_queryset(self, **kwargs):
#             queryset = super(AnimalGroupNoteCRUDL.List, self).get_queryset(**kwargs)
#             queryset = queryset.filter(animalgroup=self.request.animalgroup)
#             return queryset