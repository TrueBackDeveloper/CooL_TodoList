from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Sheet, Note_buffer
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import FormView
from .forms import SignUpForm, LoginForm, ColorCheckForm
from django.contrib.auth import login, logout
from django.shortcuts import render
from Todo_List.to_json import Note_Serializer
import zipfile, json, os, mimetypes, glob
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper


def show_main(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Todo_List:index', ))
    else:
        return render(request, 'Todo_List/main.html', )


def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            sheet_list = Sheet.objects.all()
            return render(request, 'Todo_List/Page_main.html', {'sheet_list': sheet_list})
        else:
            sheet_list = Sheet.objects.filter(user_sheet=request.user)
            return render(request, 'Todo_List/Page_main.html', {'sheet_list': sheet_list})
    else:
        return HttpResponseRedirect(reverse('Todo_List:login', ))


def detail(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        try:
            sheet = Sheet.objects.get(id=sheet_id)
        except:
            raise Http404("Листа нет :( Программист не виноват в код пробрались враги!")

        all_note_list = sheet.note_set.all()
        for note in all_note_list:
            note.real_date = timezone.now()

        return render(request, 'Todo_List/detail.html', {'sheet': sheet, 'all_note_list': all_note_list})
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def create_note(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        try:
            sheet = Sheet.objects.get(id=sheet_id)
        except:
            raise Http404("Листа нет :( Программист не виноват в код пробрались враги!")

        sheet.note_set.create(note_title=request.POST.get('title', False), task_text=request.POST.get('task', False),
                              real_date=timezone.now(), dead_line=request.POST.get('dl', False))

        return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def create_sheet(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ColorCheckForm(request.POST)
            sheet = Sheet(sheet_title=request.POST.get('name_', False), pub_date=timezone.now())
            sheet.user_sheet = User.objects.get(pk=request.user.pk)

            if form.is_valid():
                sheet.color = form.cleaned_data['hex_color']
                sheet.save()

            return HttpResponseRedirect(reverse('Todo_List:index', ))
    else:
        return HttpResponseRedirect(reverse('Todo_List:login', ))


def sheet_delete(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        sheet = Sheet.objects.get(id=sheet_id)
        sheet.delete()
        return HttpResponseRedirect(reverse('Todo_List:index', ))
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def note_delete(request, sheet_id, note_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        sheet = Sheet.objects.get(id=sheet_id)
        note = sheet.note_set.get(id=note_id)
        note.delete()
        return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def change_status(request, sheet_id, note_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        sheet = Sheet.objects.get(id=sheet_id)
        note = sheet.note_set.get(id=note_id)
        if note.status == 'Not Performed':
            note.status = 'In progress'
        elif note.status == 'In progress':
            note.status = 'Performed'
        else:
            note.status = 'Not Performed'

        note.save()

        return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def note_edit(request, sheet_id, note_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        try:
            sheet = Sheet.objects.get(id=sheet_id)
            note = sheet.note_set.get(id=note_id)
            if request.method == "POST":

                note.note_title = request.POST.get('title')
                note.task_text = request.POST.get('task')
                note.real_date = timezone.now()
                note.save()
                return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
            else:
                return render(request, 'Todo_List/note_edit.html', {'sheet': sheet, 'note': note})
        except Sheet.DoesNotExist:
            raise Http404("Note not found")
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def sheet_edit(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        try:
            sheet = Sheet.objects.get(id=sheet_id)

            if request.method == "POST":
                form = ColorCheckForm(request.POST)
                sheet.sheet_title = request.POST.get('name_')
                sheet.pub_date = timezone.now()
                if form.is_valid():
                    sheet.color = form.cleaned_data['hex_color']
                    sheet.save()

                return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
            else:
                return render(request, 'Todo_List/sheet_edit.html', {'sheet': sheet})
        except Sheet.DoesNotExist:
            raise Http404("<h2>Note not found</h2>")
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


class MyRegisterFormView(FormView):
    form_class = SignUpForm

    success_url = "/Todolist/login/"

    template_name = "registration/signup.html"

    def form_valid(self, form):
        form.save()
        
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):
    form_class = LoginForm

    template_name = "registration/login.html"

    success_url = "/Todolist/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Todo_List:login', ))


def copy_note(request, sheet_id, note_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        sheet = Sheet.objects.get(id=sheet_id)
        note = sheet.note_set.get(id=note_id)
        if not Note_buffer.objects.filter(id=1).exists():
            buffer = Note_buffer(buf_title=note.note_title, buf_task=note.task_text,
                                 buf_d_line=note.dead_line, buf_real_date=timezone.now(),
                                 buf_status=note.status)
            buffer.save()
            return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
        else:
            buffer = Note_buffer.objects.get(id=1)
            buffer.buf_title = note.note_title
            buffer.buf_task = note.task_text
            buffer.buf_d_line = note.dead_line
            buffer.buf_real_date = timezone.now()
            buffer.buf_status = note.status
            buffer.save()
            return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def paste_note(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        try:
            sheet = Sheet.objects.get(id=sheet_id)
            buffer = Note_buffer.objects.get(id=1)
            sheet.note_set.create(note_title=buffer.buf_title, task_text=buffer.buf_task,
                                  real_date=timezone.now(), dead_line=buffer.buf_d_line,
                                  status=buffer.buf_status)

            return HttpResponseRedirect(reverse('Todo_List:detail', args=(sheet.id,)))
        except Note_buffer.DoesNotExist:
            raise Http404("<h2>Buffer is empty</h2>")
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def download_json(request, sheet_id):
    if Sheet.objects.get(id=sheet_id).user_sheet == request.user or request.user.is_staff:
        sheet = Sheet.objects.get(id=sheet_id)
        note_list = sheet.note_set.all()
        file_name = str(sheet.sheet_title) + '.json'
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)))

        path += '\\files\\'
        files_ = glob.glob(path + '/**/*.json', recursive=True)

        for f in files_:
            try:
                os.remove(f)
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))

        path += file_name
        open(path, 'w')
        f = open(path, 'a')

        for note in note_list:
            dict_note = Note_Serializer(note)
            json.dump(dict_note.data, f)

        f.close()

        file_name = os.path.basename(path)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(path)[0])
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name

        return response
    else:
        raise Http404("Это не твой лист!!! (N_N) Я звоню в полицию!!!")


def download_all_json(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            sheet_list = Sheet.objects.all()
        else:
            sheet_list = Sheet.objects.filter(user_sheet=request.user)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        path += '\\files\\All_json.zip'
        zip_file = zipfile.ZipFile(path, 'w')
        for sheet in sheet_list:
            note_list = sheet.note_set.all()
            file_name = str(sheet.sheet_title) + '.json'
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
            path += '\\files\\'
            path += file_name
            open(path, 'w')
            file = open(path, 'a')
            for note in note_list:
                dict_note = Note_Serializer(note)
                json.dump(dict_note.data, file)
                zip_file.write(path)
            file.close()

        zip_file.close()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        path += '\\files\\All_json.zip'
        filename = os.path.basename(path)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(path, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(path)[0])
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)))

        path += '\\files\\'
        files_ = glob.glob(path + '/**/*.json', recursive=True)
        for file in files_:
            try:
                os.remove(file)
            except OSError as e:
                print("Error: %s : %s" % (file, e.strerror))

        return response
    else:
        return HttpResponseRedirect(reverse('Todo_List:login', ))
