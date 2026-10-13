from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub'
    )
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        allow_unicode=True,
        unique=True,
        null=True,
        blank=True
    )
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='category',
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "home:category",
            args=[self.slug]
        )


class Product(models.Model):

    VARIENT = (
        ("None", "None"),
        ("Size", "Size"),
        ("Color", "Color"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    amount = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    unit_price = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    information = RichTextUploadingField(
        blank=True,
        null=True
    )
    update = models.DateTimeField(auto_now=True)
    create = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product')
    tags = TaggableManager(blank=True)
    status = models.CharField(
        max_length=200,
        choices=VARIENT,
        null=True,
        blank=True
    )
    like = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_products'
    )
    dislike = models.ManyToManyField(
        User,
        blank=True,
        related_name='disliked_products'
    )

    def total_likes(self):
        return self.like.count()

    def total_dislikes(self):
        return self.dislike.count()

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price

        discount_price = self.unit_price * self.discount / 100
        return int(self.unit_price - discount_price)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=200)
    product_variant = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    size_varient = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='variants'
    )
    color_varient = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='variants'
    )
    amount = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    unit_price = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price

        discount_price = self.unit_price * self.discount / 100
        return int(self.unit_price - discount_price)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.TextField()
    rate = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='comment_reply',
        blank=True,
        null=True
    )
    is_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create']

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment', 'rate']

class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']



        