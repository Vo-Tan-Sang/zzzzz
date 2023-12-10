from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.


class CustomUser(AbstractUser): 
     
    created_at = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True, default=None)
    GENDER_CHOICES = (
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
    )
    gender = models.CharField(
        max_length=3, choices=GENDER_CHOICES, blank=True, null=True, default=None)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    website = models.TextField(
        max_length=255, default='https://mincute2205.pythonanywhere.com/')
    lives = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.username

    def blocked_friends(self):
        blocked_by_self_ids = Friendship.objects.filter(
            blocked=True,
            user1=self
        ).values('user2')
        blocked_by_self = CustomUser.objects.filter(id__in=blocked_by_self_ids)
        return blocked_by_self
    def is_friend_with(self, other_user):
        # Add your logic here to determine if the current user is a friend of the `other_user`.
        # Return True or False based on your criteria.
        pass

class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)

class Video(models.Model):
    video = models.FileField(upload_to='videos/', blank=True, null=True)
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    images = models.ManyToManyField(Image, blank=True)
    video = models.ManyToManyField(Video, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(
        CustomUser, related_name='liked_posts', blank=True)
    liked = models.TextField(default=False)
    profile = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='posts',null=True)
    def __str__(self):
        return f"{self.author.username} - {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} thích bài viết của {self.post.author.username}"


class Friendship(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='friends')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user1.username} và {self.user2.username} là bạn"

    def unfriend(self):
        self.delete()

    def block(self):
        self.blocked = True
        self.save()

    def unblock(self):
        self.blocked = False
        self.save()


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(
        CustomUser, related_name='groups_joined', blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='groups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    group_picture = models.ImageField(upload_to='group_pics/', blank=True)

    def __str__(self):
        return self.name

    def leave_group(self, user):
        if user in self.members.all():
            self.members.remove(user)
            return True
        return False


class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
    CustomUser, related_name='liked_Groupposts', blank=True)
    liked = models.TextField(default=False)
    images = models.ManyToManyField(Image, blank=True)
    video = models.ManyToManyField(Video, blank=True)
    def __str__(self):
        return f"Post by {self.author.username} in {self.group}"


class Comment(models.Model):
    post = models.ForeignKey(
        GroupPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyComment(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ['follower', 'following']


class CommentPost(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='commentsPost')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyCommentPost(models.Model):
    comment = models.ForeignKey(
        CommentPost, on_delete=models.CASCADE, related_name='repliesPost')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"

class Fanpage(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='fanpage_joined', blank=True)
    name = models.TextField()
    description = models.TextField()
    imgFanpage = models.ImageField(upload_to='fanpage/', blank=True, null=True)
    imgFanpageCover = models.ImageField(upload_to='fanpageCover/', blank=True, null=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_fanpage', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fanpage: {self.name} - {self.author.username}"

class ImageFanpage(models.Model):
    image = models.ImageField(upload_to='images_post_fanpage/', blank=True, null=True)

class VideoFanpage(models.Model):
    video = models.FileField(upload_to='videos_post_fanpage/',blank=True, null=True)

class Post_Fanpage(models.Model):
    fanpage = models.ForeignKey(Fanpage, on_delete=models.CASCADE,blank=True,null=True)
    content = models.TextField()
    images = models.ManyToManyField(ImageFanpage, blank=True)
    video = models.ManyToManyField(VideoFanpage, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    likes = models.ManyToManyField(
    CustomUser, related_name='liked_posts_fanpage', blank=True)
    liked = models.TextField(default=False)

    def __str__(self):
        return f"Fanpage {self.fanpage.author.username} - {self.created_at}"

class CommentFanpage(models.Model):
    post = models.ForeignKey(Post_Fanpage, on_delete=models.CASCADE, related_name='commentsPostFanpage')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


class ReplyCommentFanpage(models.Model):
    comment = models.ForeignKey(CommentFanpage, on_delete=models.CASCADE, related_name='repliesPostFanpage')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment}"