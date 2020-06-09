from django.db import models
from django.contrib.auth.models import User


class Sheet(models.Model):
    sheet_title = models.CharField('Main Title', default='Sheet_Title', max_length=20, help_text="M_Title")
    color = models.CharField('Color', default='Sheet_Color', max_length=25, help_text="Color Sheet")
    pub_date = models.DateField('Pub date')
    user_sheet = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):

        return self.sheet_title


class Note(models.Model):
    note_title = models.CharField('Note Title', default='Note_Title', max_length=20, help_text="Title")

    task_text = models.CharField('Note Task Text', default='Task Text', max_length=3000, help_text="Task")
    real_date = models.DateField('Real date')
    dead_line = models.DateField('Dead Line')
    status = models.CharField('status', default='Not Performed', max_length=20, help_text="N_Status")

    main = models.ForeignKey(Sheet, on_delete=models.CASCADE)

    def __str__(self):
        return self.note_title


class Note_buffer(models.Model):
    buf_title = models.CharField('Buffer Title', default='Buffer_Title', max_length=20, help_text="Buf_Title")
    buf_task = models.CharField('Buffer Task Text', default='Buffer_Task_Text', max_length=3000, help_text="Buffer Task")
    buf_real_date = models.DateField('Real date')
    buf_d_line = models.DateField('Dead Line')
    buf_status = models.CharField('status', default='Not Performed', max_length=20, help_text="N_Status")

    def __str__(self):
        return 'Buffer'
