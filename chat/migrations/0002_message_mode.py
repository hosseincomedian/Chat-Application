# Generated by Django 4.2 on 2023-05-05 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='mode',
            field=models.CharField(choices=[('s', 'set'), ('n', 'normal')], default='n', max_length=1),
        ),
    ]
