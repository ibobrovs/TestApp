python manage.py shell

from django.contrib.auth.models import User

from testapp.models import Author, Category, Post, Comment

user1 = User.objects.create("user1")
user2 = User.objects.create("user2")

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

category1 = Category.objects.create(name="category1")
category2 = Category.objects.create(name="category2")
category3 = Category.objects.create(name="category3")
category4 = Category.objects.create(name="category4")

post1 = Post.objects.create(author=author1, post_type=Post.ARTICLE, title="article 1", content="content_article 1 ", rating=0)
post2 = Post.objects.create(author=author2, post_type=Post.ARTICLE, title="article 2", content="content_article 2 ", rating=0)
post3 = Post.objects.create(author=author2, post_type=Post.NEWS, title="new 1", content="content_new 1", rating=0)

post1.categories.add(category1, category2)
post2.categories.add(category2)
post3.categories.add(category3)

comment1 = Comment.objects.create(post=post1, user=user1, text="comment 1", rating=0)
comment2 = Comment.objects.create(post=post2, user=user2, text="comment 2", rating=0)
comment3 = Comment.objects.create(post=post3, user=user1, text="comment 3", rating=0)
comment4 = Comment.objects.create(post=post1, user=user2, text="comment 4", rating=0)

post1.like()
post2.dislike()
comment1.like()
comment2.dislike()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by("-rating").first()
    print("Лучший автор: {}, Рейтинг: {}".format(best_author.user.username, best_author.rating))

best_post = Post.objects.order_by("-rating").first()
    print()"Дата поста: {}, Автор: {}, Рейтинг: {}, Заголовок: {}, Превью: {}".format(best_post.created.date, best_post.author.username, best_post.rating, best_post.title, best_post.preview())

print("Все комментарии к статье '{}':".format(best_post.title))
for comment in best_post.comment_set.all():
    print("Дата: {}, Пользователь: {}, Рейтинг: {}, Текст: {}".format(comment.created.date, comment.user.username, comment.rating, comment.text))