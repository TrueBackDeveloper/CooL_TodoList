# Generated by Django 3.0.3 on 2020-06-04 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_List', '0015_auto_20200604_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='json_sheet',
            name='json_file',
            field=models.FileField(upload_to=models.CharField(default='JSON_Title', help_text='JSON', max_length=600, verbose_name='JSON')),
        ),
        migrations.AlterField(
            model_name='json_sheet',
            name='json_path',
            field=models.CharField(default='JSON_Title', help_text='JSON', max_length=600, verbose_name='JSON'),
        ),
    ]
