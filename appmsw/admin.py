from django.contrib import admin
from appmsw.models import Param, Comment, SysOption, DbConnection

admin.site.register(Param)
admin.site.register(Comment)
admin.site.register(DbConnection)
admin.site.register(SysOption)
