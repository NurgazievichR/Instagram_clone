from django.contrib import admin
from django.utils import timezone

from apps.post.models import Post, PostImage



class PostImageInline(admin.TabularInline):
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'owner','create_at','update_at','slug')
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title','owner','id', 'create_at')
    list_display_links = ('title','owner')
    search_fields = ('owner',)
    readonly_fields = ('owner', 'update_at', 'create_at')
    inlines = (PostImageInline,)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.update_at = timezone.now()
        return super().save_model(request, obj, form, change)