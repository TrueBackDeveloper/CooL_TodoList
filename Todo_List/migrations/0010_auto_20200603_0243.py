# Generated by Django 3.0.3 on 2020-06-02 23:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Todo_List', '0009_auto_20200603_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='note_buffer',
            name='buf_d_line',
            field=models.DateField(default=datetime.datetime(2020, 6, 2, 23, 43, 59, 631272, tzinfo=utc), verbose_name='Dead Line'),
        ),
        migrations.AlterField(
            model_name='note',
            name='dead_line',
            field=models.DateField(default=datetime.datetime(2020, 6, 2, 23, 43, 59, 630214, tzinfo=utc), verbose_name='Dead Line'),
        ),
        migrations.AlterField(
            model_name='note',
            name='real_date',
            field=models.DateField(default=datetime.datetime(2020, 6, 2, 23, 43, 59, 630214, tzinfo=utc), verbose_name='Real date'),
        ),
        migrations.AlterField(
            model_name='note_buffer',
            name='buf_real_date',
            field=models.DateField(default=datetime.datetime(2020, 6, 2, 23, 43, 59, 631272, tzinfo=utc), verbose_name='Real date'),
        ),
    ]
