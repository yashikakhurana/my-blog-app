# Generated by Django 4.2.4 on 2023-08-07 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_tag_post_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="view_count",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
