# Generated by Django 3.2 on 2021-05-23 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0010_auto_20210523_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.PositiveSmallIntegerField(choices=[(4, 'action'), (6, 'rom-coms'), (7, 'adventure'), (5, 'romantic'), (8, 'musicals'), (0, 'Undefined'), (1, 'Comedy'), (2, 'Drama'), (3, 'Sci-fi')], default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profilepic.jpg', upload_to='profiles'),
        ),
    ]
