# Generated by Django 2.2.3 on 2019-07-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_lt', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=250)),
                ('stars', models.PositiveIntegerField()),
                ('country', models.CharField(max_length=30)),
                ('num_empty_rooms', models.IntegerField()),
                ('href', models.URLField()),
            ],
        ),
    ]
