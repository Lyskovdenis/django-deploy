from django.contrib import admin

from .models import Article, Author, Category, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'pub_date')
    list_select_related = ('author', 'category')
    list_filter = ('category', 'tags')
    search_fields = ('title', 'author__name')
    filter_horizontal = ('tags',)