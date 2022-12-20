from django.forms import ModelForm
from observer.models import Project_Core, Proposed_Project

class ProjectCoreForm(ModelForm):
    class Meta:
        model = Project_Core
        fields = []
