# Generated by Django 4.0.4 on 2022-06-21 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blogcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='discription',
            field=models.TextField(default=''),
        ),
    ]
