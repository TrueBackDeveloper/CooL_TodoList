# Generated by Django 3.0.3 on 2020-06-01 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_List', '0005_note_task_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note_buffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buf_titel', models.CharField(default='Note_Titel', help_text='N_Titel', max_length=20, verbose_name='____Note Titlel')),
                ('buf_task', models.CharField(default='Task_Text', help_text='Task', max_length=600, verbose_name='____Task Text')),
            ],
        ),
    ]