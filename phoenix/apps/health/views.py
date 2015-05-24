from django.core.urlresolvers import reverse
from smartmin.views import SmartCRUDL, SmartCreateView, SmartReadView, SmartUpdateView, SmartListView
from .models import Treatment
from .forms import TreatmentForm


class TreatmentCRUDL(SmartCRUDL):
    model = Treatment
    actions = ('create', 'read', 'update', 'list')

    class Create(SmartCreateView):
        form_class = TreatmentForm
        fields = ('date', 'description', 'animals', 'notes')

    class Read(SmartReadView):
        fields = ('date', 'description', 'notes', 'animals')

        def get_animals(self, obj):
            animals = ''
            for animal in obj.animals.all():
                animals += '<a href=' + reverse('animals.animal_read', args=[animal.id]) + '>' + str(animal) + '</a>, '
            return animals[:-2]

    class Update(SmartUpdateView):
        form_class = TreatmentForm

        def customize_form_field(self, name, field):
            field = super(TreatmentCRUDL.Update, self).customize_form_field(name, field)

            if name == 'animals':
                # Force the minimumInputLength to 0, so that it shows all the contacts by default
                field.widget.options['minimumInputLength'] = 0
                treatment = self.get_object()
                animals = treatment.animals
                field.widget.choices = [(animal.id, str(animal)) for animal in animals.order_by('name').all()]
                field.initial = [animal.id for animal in animals.order_by('name').all()]

            return field

    class List(SmartListView):
        fields = ('id', 'date', 'description', 'notes')

        def get_queryset(self, **kwargs):
            queryset = super(TreatmentCRUDL.List, self).get_queryset(**kwargs)
            return queryset