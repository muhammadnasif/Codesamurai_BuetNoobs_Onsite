from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Agency)
admin.site.register(Proposed_Project)
admin.site.register(Approved_Project)
admin.site.register(Location)
admin.site.register(Project_Core)
admin.site.register(User)
admin.site.register(UserTypes)
admin.site.register(Component)

# write code to register all 3 constraints
admin.site.register(Agency_Constraint)
admin.site.register(Location_Constraint)
admin.site.register(Yearly_Funding_Constraint)
