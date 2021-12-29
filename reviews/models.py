from django.contrib.auth.models import AbstractUser
from django.db import models

REVIEW_ERROR = 'У Вас уже есть ревью к этому произведению'


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    )
    email = models.EmailField(
        verbose_name='Еmail адрес',
        max_length=254, unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max([len(role[0]) for role in ROLES]),
        choices=ROLES,
        default=USER
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return (
            f'{self.username}, '
            f'{self.email}, '
            f'{self.role}, '
            f'{self.bio[:15]}'
        )


class Genre(models.Model):

    name = models.TextField(verbose_name='Название',
                            max_length=256)
    slug = models.SlugField(verbose_name='Ключ',
                            unique=True, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (f'{self.name}, '
                f'{self.slug}')


class Category(models.Model):
    name = models.TextField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Ключ',
        unique=True, max_length=50
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (f'{self.name}, '
                f'{self.slug}')


class Title(models.Model):

    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True, related_name="titles")
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        through='GenreTitle'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (
            f'{self.name[:10]}, '
            f'{self.year}, '
            f'{self.category.name}, '
            f'{self.genre.name}, '
            f'{self.description[:10]}'
        )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,)


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка', help_text="Введите оценку от 1 до 10"
    )
    title = models.ForeignKey(
        Title, verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return (
            f'{self.title.name}, '
            f'{self.pub_date}, '
            f'{self.author.username}, '
            f'{self.score}, '
            f'{self.text[:10]},'
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review(), verbose_name='Ревью',
        on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(verbose_name='Дата добавления',
                                    auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return (
            f'{self.author.username}, '
            f'{self.pub_date}, '
            f'{self.text[:10]}'
        )
