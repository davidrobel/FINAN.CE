# Generated by Django 4.2.3 on 2023-07-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrato', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mvalores',
            name='tipo',
            field=models.CharField(choices=[('E', 'Entrada'), ('S', 'Saída')], max_length=1),
        ),
    ]