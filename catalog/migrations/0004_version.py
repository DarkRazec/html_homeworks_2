# Generated by Django 5.0.4 on 2024-06-01 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название версии')),
                ('num', models.IntegerField(default=0, verbose_name='номер версии')),
                ('is_active', models.BooleanField(default=True, verbose_name='актуальность')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version', to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
    ]