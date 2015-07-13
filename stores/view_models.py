from .models import Person
from string import Template

class PersonAdminViewModel(Person):
    class Meta:
        proxy = True
