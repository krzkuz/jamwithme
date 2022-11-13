from django.urls import reverse
from django.db.models.signals import post_save, m2m_changed

from .models import JamRequest, Notification
from chat.models import Message
from posts.models import Post, Comment
from users.models import Follow

# somebody liked post
def post_like_notification(sender, instance, action, **kwargs):
    if action == 'post_add':
        post = instance
        if post.author != post.likes.first():
            notification = Notification.objects.create(
                type = 1,
                from_user = post.likes.first(),  
                link = reverse('post', args=[post.id])     
            )
            notification.to_users.add(post.author)
            notification.save()      
m2m_changed.connect(post_like_notification, sender=Post.likes.through)

# somebody disliked post
def post_dislike_notification(sender, instance, action, **kwargs): 
    if action == 'post_add':
        post = instance
        if post.author != post.dislikes.first():
            notification = Notification.objects.create(
                type = 1,
                from_user = post.dislikes.first(),  
                link = reverse('post', args=[post.id])     
            )
            notification.to_users.add(post.author)
            notification.save() 
m2m_changed.connect(post_dislike_notification, sender=Post.dislikes.through)

#somebody commented post
def comment_to_post_notification(sender, instance, created, **kwargs):
    if created:
        comment = instance
        if comment.author != comment.post.author:
            notification = Notification.objects.create(
                type = 3,
                from_user = comment.author,
                link = reverse('post', args=[comment.post.id]),         
            )
            notification.to_users.add(comment.post.author)
            notification.save()
post_save.connect(comment_to_post_notification, sender=Comment)

#somebody liked comment
def comment_like_notification(sender, instance, action, **kwargs): 
    if action == 'post_add':
        comment = instance
        if comment.author != comment.likes.first():
            notification = Notification.objects.create(
                type = 2,
                from_user = comment.likes.first(),  
                link = reverse('post', args=[comment.post.id])     
            )
            notification.to_users.add(comment.author)
            notification.save() 
m2m_changed.connect(comment_like_notification, sender=Comment.likes.through)

#somebody disliked comment
def comment_dislike_notification(sender, instance, action, **kwargs): 
    if action == 'post_add':
        comment = instance
        if comment.author != comment.dislikes.first():
            notification = Notification.objects.create(
                type = 2,
                from_user = comment.dislikes.first(),  
                link = reverse('post', args=[comment.post.id])     
            )
            notification.to_users.add(comment.author)
            notification.save() 
m2m_changed.connect(comment_dislike_notification, sender=Comment.dislikes.through)

#somebody followed
def follow_notification(sender, instance, action, **kwargs):
    if action == 'post_add':
        follow = instance
        notification = Notification.objects.create(
            type = 5,
            from_user = follow.follower.first(),
            link = reverse('profile', args=[follow.follower.first().id])         
        )
        notification.to_users.add(follow.user)
        notification.save()
m2m_changed.connect(follow_notification, sender=Follow.follower.through)

#somebody sent jam request
def jam_request_notification(sender, instance, created, **kwargs):
    if created:
        jam_request = instance
        notification = Notification.objects.create(
            type = 4,
            from_user = jam_request.sender,
            link = reverse('profile', args=[jam_request.sender.id])         
        )
        notification.to_users.add(jam_request.recipient)
        notification.save()
post_save.connect(jam_request_notification, sender=JamRequest)

#somebody sent message
def message_notification(sender, instance, created, **kwargs):
    if created:
        message = instance
        notification = Notification.objects.create(
            type = 6,
            from_user = message.sender,  
            link = reverse('messages', args=[message.conversation.id])     
        )
        participants = message.conversation.participants.exclude(id=message.sender.id)
        for participant in participants:
            notification.to_users.add(participant)
        notification.save()  
post_save.connect(message_notification, sender=Message)