from datetime import date
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from smartmin.views import SmartCRUDL, SmartCreateView, SmartReadView, SmartUpdateView, SmartListView
from phoenix.apps.finances.views import TransactionCRUDL
from phoenix.apps.records.views import AnimalNoteCRUDL
from phoenix.apps.health.views import TreatmentCRUDL
from .models import Animal, Breed, Service, PregnancyCheck, MilkProduction
from .forms import AnimalForm, ServiceForm, PregnancyCheckForm


class ServiceCRUDL(SmartCRUDL):
    model = Service
    actions = ('create', 'read', 'update', 'list')

    class Create(SmartCreateView):
        form_class = ServiceForm
        fields = ('method', 'sire', 'date', 'notes',)

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)

            if animal_id:
                try:
                    Animal.objects.get(id=animal_id)
                except Animal.DoesNotExist:
                    messages.warning(request, 'Animal Id is required')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            else:
                messages.error(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            return super(ServiceCRUDL.Create, self).get(request, *args, **kwargs)

        def pre_save(self, obj):
            animal = Animal.objects.get(id=self.request.GET.get('animal'))
            obj.animal = animal
            return super(ServiceCRUDL.Create, self).pre_save(obj)

        def post_save(self, obj):
            obj.animal.served()
            obj.animal.save()
            return super(ServiceCRUDL.Create, self).post_save(obj)

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal')])

    class Read(SmartReadView):
        fields = ('id', 'method', 'sire', 'date', 'status', 'notes', 'created', 'modified')

        def get_context_data(self, **kwargs):  # pragma: no cover
            context_data = super(ServiceCRUDL.Read, self).get_context_data(**kwargs)
            self.request.service = self.get_object()

            pregnancychecks_response = PregnancyCheckCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(pregnancychecks_response, 'context_data'):
                context_data['pregnancychecks'] = render_to_string('animals/pregnancycheck_related_list.html', pregnancychecks_response.context_data, RequestContext(self.request))
            return context_data

    class List(SmartListView):
        fields = ('id', 'method', 'sire', 'date', 'status', 'notes')
        default_order = '-id'

        def get_status(self, obj):
            if obj.pregnancy_checks.all():
                return PregnancyCheck.RESULT_CHOICES[obj.pregnancy_checks.latest('created_on').result]
            return ''

        def get_queryset(self, **kwargs):
            queryset = super(ServiceCRUDL.List, self).get_queryset(**kwargs)
            if hasattr(self.request, 'animal'):
                queryset = queryset.filter(animal=self.request.animal)
            return queryset

        def get_context_data(self, **kwargs):
            context_data = super(ServiceCRUDL.List, self).get_context_data(**kwargs)
            if hasattr(self.request, 'animal'):
                context_data['animal'] = self.request.animal
            return context_data

        def get_method(self, obj):
            if obj.method:
                return Service.METHOD_CHOICES[obj.method]
            return ''


class PregnancyCheckCRUDL(SmartCRUDL):
    model = PregnancyCheck

    class Create(SmartCreateView):
        form_class = PregnancyCheckForm
        fields = ('result', 'check_method', 'date')

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)

            if animal_id:
                try:
                    Animal.objects.get(id=animal_id)
                except Animal.DoesNotExist:
                    messages.warning(request, 'Animal Id is required')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            else:
                messages.error(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            return super(PregnancyCheckCRUDL.Create, self).get(request, *args, **kwargs)

        def pre_save(self, obj):
            animal = Animal.objects.get(id=self.request.GET.get('animal'))
            obj.animal = animal

            # Getting the last service for the animal
            obj.service = animal.animal_services.latest('created_on')
            return super(PregnancyCheckCRUDL.Create, self).pre_save(obj)

        def post_save(self, obj):
            if obj.result == PregnancyCheck.RESULT_CHOICES.pregnant:
                obj.animal.pregnant()
            elif obj.result == PregnancyCheck.RESULT_CHOICES.open:
                obj.animal.open()
            obj.animal.save()
            return super(PregnancyCheckCRUDL.Create, self).post_save(obj)

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal')])

    class Read(SmartReadView):
        fields = ('id', 'check_method', 'result', 'date', 'created', 'modified')

    class List(SmartListView):
        fields = ('id', 'check_method', 'result', 'date')
        default_order = '-id'

        def get_check_method(self, obj):
            if obj.check_method:
                return PregnancyCheck.CHECK_METHOD_CHOICES[obj.check_method]
            return ''

        def get_result(self, obj):
            return PregnancyCheck.RESULT_CHOICES[obj.result]

        def get_queryset(self, **kwargs):
            queryset = super(PregnancyCheckCRUDL.List, self).get_queryset(**kwargs)
            if hasattr(self.request, 'animal'):
                queryset = queryset.filter(animal=self.request.animal)
            if hasattr(self.request, 'service'):
                queryset = queryset.filter(service=self.request.service)
            return queryset

        def get_context_data(self, **kwargs):
            context_data = super(PregnancyCheckCRUDL.List, self).get_context_data(**kwargs)
            if hasattr(self.request, 'animal'):
                context_data['animal'] = self.request.animal
            return context_data


class AnimalTransactionCRUDL(TransactionCRUDL):
    class Create(TransactionCRUDL.Create):
        fields = ('date', 'category', 'amount')

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)
            if animal_id:
                try:
                    Animal.objects.get(id=animal_id)
                except Animal.DoesNotExist:
                    messages.error(request, 'Animal Id is required')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            else:
                messages.error(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            return super(AnimalTransactionCRUDL.Create, self).get(request, *args, **kwargs)

        def post_save(self, obj):  # pragma: no cover
            animal_id = self.request.GET.get('animal', None)
            animal = Animal.objects.get(id=animal_id)
            obj.animals.add(animal)
            return obj

        def get_success_url(self):  # pragma: no cover
            return reverse('animals.animal_read', args=[self.request.GET.get('animal')])

    class List(TransactionCRUDL.List):
        fields = ('id', 'date', 'category', 'amount')

        def get_queryset(self, **kwargs):
            queryset = super(AnimalTransactionCRUDL.List, self).get_queryset(**kwargs)
            queryset = queryset.filter(animals=self.request.animal)
            return queryset

        def get_context_data(self, **kwargs):
            context_data = super(AnimalTransactionCRUDL.List, self).get_context_data(**kwargs)
            context_data['animal'] = self.request.animal
            return context_data


class AnimalTreatmentCRUDL(TreatmentCRUDL):

    class Create(TreatmentCRUDL.Create):
        fields = ('date', 'description', 'notes')

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)
            if animal_id:
                try:
                    Animal.objects.get(id=animal_id)
                except Animal.DoesNotExist:
                    messages.error(request, 'Animal Id is required')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            else:
                messages.error(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('animals.animal_list')))
            return super(AnimalTreatmentCRUDL.Create, self).get(request, *args, **kwargs)

        def post_save(self, obj):
            obj = super(AnimalTreatmentCRUDL.Create, self).post_save(obj)
            animal_id = self.request.GET.get('animal', None)
            animal = Animal.objects.get(id=animal_id)
            obj.animals.add(animal)
            return obj

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal', None)])

    class Update(TreatmentCRUDL.Update):
        fields = ('date', 'description', 'notes',)

        def get_success_url(self):
            animal_id = self.object.animals.all()[0].id
            return reverse('animals.animal_read', args=[animal_id])

    class List(TreatmentCRUDL.List):
        fields = ('id', 'type', 'date', 'description', 'notes')

        def get_queryset(self, **kwargs):
            queryset = super(AnimalTreatmentCRUDL.List, self).get_queryset(**kwargs)
            queryset = queryset.filter(animals=self.request.animal)
            return queryset


class BreedCRUDL(SmartCRUDL):
    model = Breed


class MilkProductionCRUDL(SmartCRUDL):
    model = MilkProduction

    class Create(SmartCreateView):
        fields = ('time', 'amount', 'butterfat_ratio')

        def pre_save(self, obj):
            obj = super(MilkProductionCRUDL.Create, self).pre_save(obj)
            animal_id = self.request.GET.get('animal')
            obj.animal = Animal.objects.get(id=animal_id)
            return obj

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal', None)])

    class List(SmartListView):
        fields = ('id', 'time', 'amount', 'butterfat_ratio')
        default_order = '-id'

        def get_context_data(self, **kwargs):
            context_data = super(MilkProductionCRUDL.List, self).get_context_data(**kwargs)
            if hasattr(self.request, 'animal'):
                context_data['animal'] = self.request.animal
            return context_data


class AnimalCRUDL(SmartCRUDL):
    model = Animal
    actions = ('create', 'read', 'update', 'list', 'add_offspring')

    class FormMixin(object):

        def __init__(self, **kwargs):
            self.form_class = AnimalForm
            super(AnimalCRUDL.FormMixin, self).__init__(**kwargs)

    class Create(FormMixin, SmartCreateView):
        pass

    class AddOffspring(FormMixin, SmartCreateView):

        def get(self, request, *args, **kwargs):
            animal_id = request.GET.get('animal', None)
            if animal_id:
                try:
                    Animal.objects.get(id=animal_id)
                except Animal.DoesNotExist:
                    messages.error(request, 'Animal Id is required')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, 'Animal Id is required')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return super(AnimalCRUDL.AddOffspring, self).get(request, *args, **kwargs)

        def customize_form_field(self, name, field):
            field = super(AnimalCRUDL.AddOffspring, self).customize_form_field(name, field)
            animal_id = self.request.GET.get('animal')
            animal = Animal.objects.get(id=animal_id)

            if name == 'birth_date':
                    field.initial = date.today()

            try:
                service = animal.animal_services.latest('created_on')
            except Service.DoesNotExist:
                pass
            else:
                if name == 'sire':
                    field.initial = service.sire
                if name == 'dam':
                    field.initial = animal

            return field

        def pre_save(self, obj):
            obj = super(AnimalCRUDL.AddOffspring, self).pre_save(obj)
            animal_id = self.request.GET.get('animal')
            obj.dam = Animal.objects.get(id=animal_id)
            return obj

        def post_save(self, obj):
            obj.lactating()
            obj.save()
            return super(AnimalCRUDL.AddOffspring, self).post_save(obj)

        def get_success_url(self):
            return reverse('animals.animal_read', args=[self.request.GET.get('animal')])

    class Read(SmartReadView):
        fields = ('animal_id', 'alt_id', 'electronic_id', 'ear_tag', 'name', 'color', 'gender', 'breed', 'sire', 'dam',
                  'status', 'birth_date', 'birth_weight', 'weaning_date', 'weaning_weight', 'yearling_date',
                  'yearling_weight')

        def get_context_data(self, **kwargs):
            context_data = super(AnimalCRUDL.Read, self).get_context_data(**kwargs)

            # Add related lists
            self.request.animal = self.object

            # fertile
            context_data['fertile'] = False
            if self.object.gender != Animal.GENDER_CHOICES.bull:
                context_data['fertile'] = True

            service_response = ServiceCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(service_response, 'context_data'):
                context_data['services'] = render_to_string('animals/service_related_list.html', service_response.context_data, RequestContext(self.request))

            pregnancy_response = PregnancyCheckCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(pregnancy_response, 'context_data'):
                context_data['pregnancies'] = render_to_string('animals/pregnancycheck_related_list.html', pregnancy_response.context_data, RequestContext(self.request))

            treatment_response = AnimalTreatmentCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(treatment_response, 'context_data'):
                treatment_response.context_data['add_url'] = reverse('animals.treatment_create') + '?animal=' + str(self.request.animal.id)
                context_data['treatment'] = render_to_string('health/treatment_related_list.html', treatment_response.context_data, RequestContext(self.request))

            note_response = AnimalNoteCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(note_response, 'context_data'):
                context_data['notes'] = render_to_string('records/animalnote_related_list.html', note_response.context_data, RequestContext(self.request))

            context_data['animal_documents'] = render_to_string('records/animaldocument_form.html', {'animal': self.request.animal}, RequestContext(self.request))

            transaction_response = AnimalTransactionCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(transaction_response, 'context_data'):
                context_data['transactions'] = render_to_string('animals/transaction_related_list.html', transaction_response.context_data, RequestContext(self.request))

            milkproduction_response = MilkProductionCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(milkproduction_response, 'context_data'):
                context_data['milkproduction'] = render_to_string('animals/milkproduction_related_list.html', milkproduction_response.context_data, RequestContext(self.request))

            self.request.offsprings = True
            offspring_response = AnimalCRUDL().view_for_action('list').as_view()(self.request)
            if hasattr(offspring_response, 'context_data'):
                context_data['offsprings'] = render_to_string('animals/offspring_related_list.html', offspring_response.context_data, RequestContext(self.request))

            return context_data

    class Update(FormMixin, SmartUpdateView):
        pass

    class List(SmartListView):
        fields = ('id', 'name', 'color', 'breed', 'gender', 'sire', 'dam')

        def get_queryset(self, **kwargs):
            queryset = super(AnimalCRUDL.List, self).get_queryset(**kwargs)
            if hasattr(self.request, 'offsprings') and self.request.offsprings:
                queryset = queryset.filter(Q(sire=self.request.animal) | Q(dam=self.request.animal))
            return queryset

        def get_context_data(self, **kwargs):
            context_data = super(AnimalCRUDL.List, self).get_context_data(**kwargs)
            if hasattr(self.request, 'animal'):
                context_data['animal'] = self.request.animal
            return context_data


