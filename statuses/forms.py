from django.forms import ModelForm
from statuses.models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = _("Name")
