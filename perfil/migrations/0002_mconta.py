# Generated by Django 4.2.3 on 2023-07-04 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mConta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apelido', models.CharField(max_length=50)),
                ('banco', models.CharField(choices=[('NU', 'Nubank'), ('CE', 'Caixa economica')], max_length=2)),
                ('tipo', models.CharField(choices=[('pf', 'Pessoa fisica'), ('pj', 'Pessoa juridica')], max_length=2)),
                ('valor', models.FloatField(default=0)),
                ('icone', models.ImageField(upload_to='icones')),
            ],
        ),
    ]
