from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Sheet
from django.utils import timezone


class Show_main_tests(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Todo_List/main.html')

    def test_view_url_correct_redirect(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('show_main'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index'))


class Index_tests(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_user2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user2.is_staff = True
        test_user2.save()

    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get('/Todolist/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sheet_list' in response.context)
        self.assertTemplateUsed(response, 'Todo_List/Page_main.html')
        self.assertTrue(list(response.context['sheet_list']) == list(Sheet.objects.all()))

    def test_view_for_client(self):
        response = self.client.get('/Todolist/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/Todolist/login/')

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get('/Todolist/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sheet_list' in response.context)
        self.assertTemplateUsed(response, 'Todo_List/Page_main.html')
        self.assertTrue(
            list(response.context['sheet_list']) == list(Sheet.objects.filter(user_sheet=response.context['user'])))


class Detail_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sheet' in response.context)
        self.assertTrue('all_note_list' in response.context)
        self.assertTrue(
            response.context['sheet'] == Sheet.objects.get(id=self.test_sheet_1.id))
        self.assertTrue(
            list(response.context['all_note_list']) == list(self.test_sheet_1.note_set.all()))
        self.assertTemplateUsed(response, 'Todo_List/detail.html')

    def test_view_for_user_wrong_sheet(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_2.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_2.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sheet' in response.context)
        self.assertTrue('all_note_list' in response.context)
        self.assertTrue(
            response.context['sheet'] == Sheet.objects.get(id=self.test_sheet_2.id))
        self.assertTrue(
            list(response.context['all_note_list']) == list(self.test_sheet_2.note_set.all()))

        response = self.client.get(reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('sheet' in response.context)
        self.assertTrue('all_note_list' in response.context)
        self.assertTrue(
            response.context['sheet'] == Sheet.objects.get(id=self.test_sheet_1.id))
        self.assertTrue(
            list(response.context['all_note_list']) == list(self.test_sheet_1.note_set.all()))
        self.assertTemplateUsed(response, 'Todo_List/detail.html')


class Create_note_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:create_note', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user_post(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note'
        some_task = 'Task Note'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:create_note', kwargs={'sheet_id': self.test_sheet_1.id}, ),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_user_post_wrong_note(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note'
        some_task = 'Task Note'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:create_note', kwargs={'sheet_id': self.test_sheet_2.id}, ),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff_post(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note for Staff'
        some_task = 'Task Note for Staff'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:create_note', kwargs={'sheet_id': self.test_sheet_1.id}, ),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class Create_sheet_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:create_sheet', ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:login', ))

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Sheet'
        hex_color = '#FFFFFF'

        response = self.client.post(reverse('Todo_List:create_sheet', ),
                                    {'name_': some_title, 'hex_color': hex_color, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index', ))



    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Sheet'
        hex_color = '#FFFAFF'

        response = self.client.post(reverse('Todo_List:create_sheet', ),
                                    {'name_': some_title, 'hex_color': hex_color, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index', ))


class Sheet_delete_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:sheet_delete', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:sheet_delete', kwargs={'sheet_id': self.test_sheet_1.id}, ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index', ))

    def test_view_for_user_post_wrong_sheet(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:sheet_delete', kwargs={'sheet_id': self.test_sheet_2.id}, ))
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:sheet_delete', kwargs={'sheet_id': self.test_sheet_2.id}, ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index', ))


class Note_delete(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

        self.test_sheet_1_note_1 = self.test_sheet_1.note_set.create(note_title='Note Title 1',
                                                                     task_text='Some Task 1',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

        self.test_sheet_2_note_2 = self.test_sheet_2.note_set.create(note_title='Note Title 2',
                                                                     task_text='Some Task 2',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:note_delete', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                            'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_delete', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                            'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_user_wrong_note(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_delete', kwargs={'sheet_id': self.test_sheet_2.id,
                                                                            'note_id': self.test_sheet_2_note_2.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_delete', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                            'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class Change_status_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

        self.test_sheet_1_note_1 = self.test_sheet_1.note_set.create(note_title='Note Title 1',
                                                                     task_text='Some Task 1',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

        self.test_sheet_2_note_2 = self.test_sheet_2.note_set.create(note_title='Note Title 2',
                                                                     task_text='Some Task 2',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:change_status', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                              'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:change_status', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                              'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_user_wrong_note(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:change_status', kwargs={'sheet_id': self.test_sheet_2.id,
                                                                              'note_id': self.test_sheet_2_note_2.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:change_status', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                              'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class Note_edit_tests(TestCase):

    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

        self.test_sheet_1_note_1 = self.test_sheet_1.note_set.create(note_title='Note Title 1',
                                                                     task_text='Some Task 1',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

        self.test_sheet_2_note_2 = self.test_sheet_2.note_set.create(note_title='Note Title 2',
                                                                     task_text='Some Task 2',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

    def test_view_for_client_get(self):
        response = self.client.get(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                          'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user_get(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                          'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Todo_List/note_edit.html')

    def test_view_for_user_wrong_note_get(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_2.id,
                                                                          'note_id': self.test_sheet_2_note_2.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_staff_get(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                          'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Todo_List/note_edit.html')

    def test_view_for_user_post(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note'
        some_task = 'Task Note'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_user_wrong_note_post(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note'
        some_task = 'Task Note'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_staff_post(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Note'
        some_task = 'Task Note'
        some_dl = timezone.localdate()

        response = self.client.post(reverse('Todo_List:note_edit', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}),
                                    {'title': some_title, 'task': some_task, 'dl': some_dl})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class Sheet_edit_tests(TestCase):

    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()
        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

    def test_view_for_client(self):
        response = self.client.get(reverse('Todo_List:sheet_edit', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user_get(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:sheet_edit', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Todo_List/sheet_edit.html')

    def test_view_for_staff_get(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.get(reverse('Todo_List:sheet_edit', kwargs={'sheet_id': self.test_sheet_1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Todo_List/sheet_edit.html')

    def test_view_for_user_post(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Sheet'
        hex_color = '#FFFFFF'

        response = self.client.post(reverse('Todo_List:sheet_edit', kwargs={'sheet_id': self.test_sheet_1.id}),
                                    {'name_': some_title, 'hex_color': hex_color, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_staff_post(self):
        login = self.client.login(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        some_title = 'Title Sheet'
        hex_color = '#FFFAFF'

        response = self.client.post(reverse('Todo_List:sheet_edit', kwargs={'sheet_id': self.test_sheet_1.id}),
                                    {'name_': some_title, 'hex_color': hex_color, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class Copy_Note_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()
        test_user_2 = User.objects.create_user(username='dogislav@mail.ru', password='1X<ISRUkw+tuK')
        test_user_2.is_staff = True
        test_user_2.save()

        self.test_sheet_1 = Sheet.objects.create(sheet_title="Some title", pub_date=timezone.now(), color='#FFFFFF',
                                                 user_sheet=User.objects.get(pk=test_user_1.pk))

        self.test_sheet_2 = Sheet.objects.create(sheet_title="Some title num 2", pub_date=timezone.now(),
                                                 color='#FFFAAA',
                                                 user_sheet=User.objects.get(pk=test_user_2.pk))

        self.test_sheet_1_note_1 = self.test_sheet_1.note_set.create(note_title='Note Title 1',
                                                                     task_text='Some Task 1',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

        self.test_sheet_2_note_2 = self.test_sheet_2.note_set.create(note_title='Note Title 2',
                                                                     task_text='Some Task 2',
                                                                     real_date=timezone.now(),
                                                                     dead_line=timezone.localdate())

    def test_view_for_client_get(self):
        response = self.client.get(reverse('Todo_List:copy_note', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                          'note_id': self.test_sheet_1_note_1.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_for_user(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse('Todo_List:copy_note', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}), )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_user_wrong_note(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse('Todo_List:copy_note', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}), )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))

    def test_view_for_staff(self):
        login = self.client.login(username='dog@mail.ru', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse('Todo_List:copy_note', kwargs={'sheet_id': self.test_sheet_1.id,
                                                                           'note_id': self.test_sheet_1_note_1.id}),
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:detail', kwargs={'sheet_id': self.test_sheet_1.id}, ))


class MyRegisterFormView_tests(TestCase):

    def test_view_client(self):
        response = self.client.get(reverse('Todo_List:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_view_client_signup(self):
        response = self.client.post(reverse('Todo_List:signup'),
                                    {'username': 'ddd@mail.ru', 'first_name': 'John',
                                     'password1': 'TipicalPassword5656',
                                     'password2': 'TipicalPassword5656'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:login', ))


class LoginFormView_tests(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='dog@mail.ru', password='1X<ISRUkw+tuK')
        test_user_1.save()

    def test_view_client(self):
        response = self.client.get(reverse('Todo_List:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_view_client_login(self):
        response = self.client.post(reverse('Todo_List:login'),
                                    {'username': 'dog@mail.ru', 'password': '1X<ISRUkw+tuK'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Todo_List:index', ))
