from django.contrib import admin
from django.utils import timezone

from apps.comment.models import Comment
from apps.post.models import Post, PostImage, Tag



class PostImageInline(admin.TabularInline):
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'owner','create_at','update_at','slug', 'views')
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title','owner','id', 'create_at', 'views')
    list_display_links = ('title','owner')
    search_fields = ('owner',)
    readonly_fields = ('owner', 'update_at', 'create_at', 'views')
    inlines = (PostImageInline,)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.update_at = timezone.now()
        return super().save_model(request, obj, form, change)


admin.site.register(Comment)
admin.site.register(Tag)