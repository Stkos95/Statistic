from django import forms
from statist.models import Type
from django.forms import inlineformset_factory, HiddenInput, ValidationError
from django.forms.models import BaseInlineFormSet
from statist.models import Actions, Players, Game, Type, Parts, RawResults, Teams


class PartsForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'type']


class CreateTypeGame(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'halfs']

class CreateTeam(forms.ModelForm):
    class Meta:
        model = Teams
        fields = ['name']

class BaseTypeFormset(BaseInlineFormSet):
    ordering_widget = HiddenInput

    def add_fields(self, form, index):
        super().add_fields(form, index)

        form.nested = PartsFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='parts-%s-%s' % (
                form.prefix,
                PartsFormset.get_default_prefix()),
        )

    def clean(self):
        for form in self.forms:

            for nested_form in form.nested:

                if nested_form.is_valid():
                    # nested_form.non_field_errors()
                    # nested_form.add_error()
                    name = nested_form.cleaned_data.get('name', None)
                    if not name:

                        raise ValidationError("Заполните или удалите пустые поля 'Действие'.")

    def save(self, commit=True):
        r = []
        result = super().save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    zz =form.nested.save(commit=False)
                    r.extend(zz)
        return r

class BasePartFormset(BaseInlineFormSet):
    ordering_widget = HiddenInput
    deletion_widget = HiddenInput

TypeFormset = inlineformset_factory(Type, Parts, fields=['name',], formset=BaseTypeFormset, extra=0, can_delete=False, can_order=True)
PartsFormset = inlineformset_factory(Parts, Actions, fields=['name'], min_num=1, formset=BasePartFormset, extra=0, can_delete=True, can_order=True)


PlayerCreationFormset = inlineformset_factory(Teams, Players, fields=['name', 'number'], extra=2)