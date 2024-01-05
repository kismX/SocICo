from django import template

register = template.Library()

@register.filter(name='has_liked_post')
def has_liked_post(post, user):
    return post.likes.filter(id=user.id).exists()

@register.filter(name='has_liked_comment')
def has_liked_comment(comment, user):
    return comment.likes.filter(id=user.id).exists()