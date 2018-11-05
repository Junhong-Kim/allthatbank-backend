# Generated by Django 2.0.2 on 2018-08-25 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('N', 'Notice'), ('F', 'FreeBoard'), ('Q', 'Question')], default='F', max_length=50),
        ),
    ]
