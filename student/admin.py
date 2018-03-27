from django.contrib import admin
from student.models import Student, Team, Writeup, Solve, Evsolv
# Register your models here.
admin.site.register(Student)
admin.site.register(Team)
admin.site.register(Writeup)
admin.site.register(Solve)
admin.site.register(Evsolv)