from django.contrib import admin
from .models import Post, CustomUser,Comment,Like,Group,Friendship,GroupPost,ReplyComment,FriendRequest,Image,Follow,CommentPost,ReplyCommentPost

# Register your models here.
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Group)
admin.site.register(Friendship)
admin.site.register(GroupPost)
admin.site.register(ReplyComment)   
admin.site.register(FriendRequest)
admin.site.register(Image)
admin.site.register(Follow)
admin.site.register(CommentPost)
admin.site.register(ReplyCommentPost)



