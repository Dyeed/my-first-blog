# Generated by Django 2.0.5 on 2018-06-21 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date']},
        ),
    ]