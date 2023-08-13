# Generated by Django 4.2.1 on 2023-08-11 23:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0011_websitemeta"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="bookmarks",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                related_name="bookmarks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]