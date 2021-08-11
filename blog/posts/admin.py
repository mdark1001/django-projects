from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post) # equal to admin.site.register
class PostAdmin(admin.ModelAdmin):
    """ Modelo admin para los post """

    list_display =('title','author','publish','status')
    list_filter = ('status','created','publish','author') # Filter 
    search_fields = ('title','body')  # search
    prepopulated_fields = {'slug':('title',)}  # buscar más del prepopulated_fields
    raw_id_fields =('author',) # Choose an author 
    date_hierarchy = 'publish'
    ordering = ('status','publish')

