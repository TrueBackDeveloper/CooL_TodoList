# Generated by Django 3.0.3 on 2020-05-18 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_List', '0003_auto_20200518_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note_titel',
            field=models.CharField(default='Note_Titel', help_text='N_Titel', max_length=20, verbose_name='____Note Titlel'),
        ),
    ]
