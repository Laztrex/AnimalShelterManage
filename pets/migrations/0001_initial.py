# Generated by Django 3.1.1 on 2020-09-06 11:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breeds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название породы')),
                ('description', models.TextField(verbose_name='Особенности')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Порода',
                'verbose_name_plural': 'Породы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scientific_name', models.CharField(max_length=150, verbose_name='Научный вид')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Кличка')),
                ('age', models.PositiveSmallIntegerField(default=0, verbose_name='Возраст')),
                ('date_in_shelter', models.DateField(default=datetime.date.today, verbose_name='Дата поступления в приют')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='pets/', verbose_name='Фото')),
                ('url', models.SlugField(max_length=160, unique=True)),
                ('breed', models.ManyToManyField(to='pets.Breeds', verbose_name='породы')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pets.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Питомец',
                'verbose_name_plural': 'Питомцы',
            },
        ),
        migrations.CreateModel(
            name='ReviewWorkers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pets.reviewworkers', verbose_name='Родитель')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pets', verbose_name='Питомец')),
            ],
            options={
                'verbose_name': 'Комментарий работника приюта',
                'verbose_name_plural': 'Комментарии работников приюта',
            },
        ),
        migrations.CreateModel(
            name='PetShots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='pets_shots/', verbose_name='Фото')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pets', verbose_name='Питомец')),
            ],
            options={
                'verbose_name': 'Фото питомца',
                'verbose_name_plural': 'Фото питомцев',
            },
        ),
    ]
