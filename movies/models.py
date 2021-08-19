from django.db import models

from account.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(primary_key=True,max_length=100, null=False)

    def __str__(self):
        return self.name


class Actor(models.Model):
    # movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='movie')
    movie = models.CharField('фильм', max_length=100)
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    bio = models.TextField("биография")
    image = models.ImageField("Изображение", upload_to="images/actors")

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=500)
    imdb_score = models.FloatField()
    popularity = models.FloatField()
    # rating = models.ForeignKey('movies.Rating', on_delete=models.CASCADE, related_name='rating')
    director = models.CharField(max_length=500)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name='actor', default='')
    # actor = models.ManyToManyField(Actor, related_name="film_actor", default=None)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    trailer = models.CharField(max_length=500)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    value = models.SmallIntegerField("Значение")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rating")

    class Meta:
        ordering = ["-value"]

    def __str__(self):
        return f'{self.value}'






