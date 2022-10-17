# Generated by Django 4.1 on 2022-10-11 10:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0002_post_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="post_like", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
