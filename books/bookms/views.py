from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext
from . import models
import time
from . import forms

# Create your views here.
#未登录界面
def ShowIndex(request):
    context = {}
    overdue_rec = []
    new_books = []
    borrow_list = models.Borrows.objects.all()
    book_list = models.Books.objects.all()

    if request.user.is_authenticated:
        context['is_login'] = True
        context['user'] = request.user
    else:
        context['is_login'] = False

    # 匹配有过期书籍的用户
    for borrow_rec in  borrow_list:
        if borrow_rec.is_overdue():
            overdue_rec.append(borrow_rec)

    for book in book_list:
        if book.is_included_recently():
            new_books.append(book)

    context['overdue_rec'] = overdue_rec
    context['new_books'] = new_books
    return render(request, 'bookms/Index.html', context)


#找书
@csrf_exempt
def SearchBooks(req):
    book_list = models.Books.objects.all()
    context={
        'book_list': book_list,
        'is_login': False,
    }
    if req.method == 'POST':
        name = req.POST.get('name', '')
        author = req.POST.get('author', '')
        publisher = req.POST.get('publisher', '')
        category = req.POST.get('category', '')

        book_list = models.Books.objects.filter(
            name__contains=name,
            author__name__contains=author,
            publisher__name__contains=publisher,
            category__name__contains=category
        )
        context['book_list'] = book_list

    if req.user.is_authenticated:
        context['is_login'] = True
        context['user'] = req.user
    return render(req, 'bookms/SearchBooks.html', context)


#登陆
@csrf_exempt
def SignIn(req, context= {}):
    context = context
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            context['login_success'] = True
            return HttpResponseRedirect('/home/%d'%(user.id))
        else:
            if models.Readers.objects.filter(user__username=username).count() == 0:
                context['message'] = '不存在此用户'
                context['state'] = 'user_name_not_exist'
            else:
                context['message'] = '密码错误'
                context['state'] = 'password_error'
            return render(req, 'bookms/SignIn.html', context)

    return render(req, 'bookms/SignIn.html', context)


#注册
@csrf_exempt
def SignUp(req):
    context = {
        'userExist': False,
        'usernameExist': False,
        'sign_up_success': False,
        'invalid_username': False,
    }
    error_flag = False
    if req.method =='POST':
        username = req.POST['username']
        password = req.POST['password']
        password_re = req.POST['password_re']
        age = req.POST['age']

        #检查用户名
        username = username.strip()
        if username == '':
            context['invalid_username'] = True
            error_flag = True

        #检查密码
        if password == '':
            context['invalid_password'] = True
            error_flag = True
        elif password != password_re:
            context['match_error'] = True
            error_flag = True

        #判断用户是否已注册
        user = authenticate(username=username, password=password)
        if user:
            context['userExist'] = True
            error_flag = True

        # 判断用户名是否已被注册
        user = User.objects.filter(username=username)
        if user:
            context['usernameExist'] = True
            context['registered_username'] = username
            error_flag = True

        if error_flag:
            return render(req, 'bookms/SignUp.html', context)

        #在数据库中创建新用户
        user = User.objects.create_user(username=username, password=password)
        user.save()
        reader = models.Readers(user=user, reader_identity=user.id, reg_date=datetime.datetime.now(), age=age)
        reader.save()
        context['sign_up_success'] = True
        return HttpResponseRedirect('/SignIn')
    else:
        return render(req, 'bookms/SignUp.html', context)


#书籍信息页面
def Book_Info(req, book_isbn):
    context = {}

    if req.user.is_authenticated:
        context['is_login'] = True
        context['user'] = req.user
    else:
        context['is_login'] = False

    book = models.Books.objects.get(isbn=book_isbn)
    comments = models.Ratings.objects.filter(book=book)
    likely_books = models.Books.objects.filter(category=book.category)
    context['book'] = book
    context['likely_books'] = likely_books
    context['comments'] = comments
    return render(req, 'bookms/Book_Info.html', context)


#用户户界面
@login_required(login_url='/SignIn')
def User_Home(req, user_id):
    context = {}
    user = User.objects.get(id = user_id)
    user_r = req.user
    if user == user_r:
        context['user'] = user
        reader = models.Readers.objects.get(user=user)
        book_list = models.Borrows.objects.filter(reader=reader)
        book_list_hist = models.Borrow_histry.objects.filter(reader=reader)
        all_books = models.Books.objects.all()
        new_books = []

        if reader.forbid:
            if reader.is_unforbid():
                reader.forbid_date = None
                reader.forbid = False
                reader.save()
            else:
                context['forbid'] = True

        if reader.latest_borrowed_category:
            likely_like_list = models.Books.objects.filter(category=reader.latest_borrowed_category)
        else:
            likely_like_list = []

        for book in all_books:
            if book.is_included_recently():
                new_books.append(book)

        context['new_books'] = new_books
        context['likely_like_list'] = likely_like_list
        context['book_list'] = book_list
        context['book_list_hist'] = book_list_hist
        return render(req, 'bookms/Home.html', context)
    else:
        return render(req, 'bookms/permission_denied.html')


#退出
def SignOut(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))


#借书
@login_required(login_url='/SignIn')
@csrf_exempt
def Borrow(req, book_isbn):
    book = models.Books.objects.get(isbn=book_isbn)
    context = {
        'book': book,
        'user': req.user,
        'is_login': True,
    }
    if req.method == 'POST':
        reader = models.Readers.objects.get(user=req.user)
        borrowed_books = models.Borrows.objects.filter(reader=reader)
        num_borrowed = borrowed_books.count()
        if reader.forbid:
            if num_borrowed >= 1:
                context['message'] = '最多只能借一本书'
                template = loader.get_template('bookms/messages.html')
                return HttpResponse(template.render(context))
            else:
                borrow = models.Borrows(
                    reader=reader,
                    book=book,
                    date=datetime.datetime.now()
                )
                reader.latest_borrowed_category = book.category
                borrow.save()
                book.num_lend = book.num_lend + 1
                book.save()
                reader.save()
                context['message'] = '借书成功'
                template = loader.get_template('bookms/messages.html')
                return HttpResponse(template.render(context))
        elif num_borrowed >= 5:
            context['message'] = '最多只能借五本'
            template = loader.get_template('bookms/messages.html')
            return HttpResponse(template.render(context))
        elif book.num_lend >= book.num_copies:
            context['message'] = '书已借完'
            template = loader.get_template('bookms/messages.html')
            return HttpResponse(template.render(context))
        elif models.Borrows.objects.filter(reader=reader, book__isbn=book_isbn).count() != 0:
            context['message'] = '您已经借过这本书'
            template = loader.get_template('bookms/messages.html')
            return HttpResponse(template.render(context))
        else:
            borrow = models.Borrows(
                reader=reader,
                date=datetime.datetime.now(),
                book=book
            )
            reader.latest_borrowed_category = book.category
            borrow.save()
            book.num_lend = book.num_lend + 1
            book.save()
            reader.save()
            context['message'] = '借书成功'
            template = loader.get_template('bookms/messages.html')
            return HttpResponse(template.render(context))

    return render(req, 'bookms/Borrow.html', context)


#还书
@login_required(login_url='/SignIn')
@csrf_exempt
def ReturnBook(req, book_isbn):
    context = {
        'is_success': False,
        'user': req.user,
        'is_login': True,
    }
    reader = models.Readers.objects.get(user=req.user)
    book = models.Books.objects.get(isbn=book_isbn)
    borrow_rec = models.Borrows.objects.get(reader=reader, book=book)
    context['book'] = book
    context['borrow_rec'] = borrow_rec

    if req.method == 'POST':
        rate = req.POST.get('rate', 0)
        comment = req.POST.get('comment', '')
        #过期那么过期记录+1
        if borrow_rec.is_overdue():
            if reader.forbid:
                reader.forbid_date = datetime.datetime.now()
                reader.save()
            else:
                reader.delay_times += 1

                #如果过期记录达到三次，那么最大借书本书变成一本
                if reader.delay_times == 3:
                    reader.forbid_date = datetime.datetime.now()
                    reader.forbid = True
                    reader.delay_times = 0
                reader.save()

        if rate != 0:
            try:
                rate_rec = models.Ratings.objects.get(reader=reader, book=book)
                rate_rec.rate = rate
                if comment != '':
                    rate_rec.comment = comment
            except:
                rate_rec = models.Ratings(
                    book=book,
                    reader=reader,
                    rate=rate
                )
                if comment != '':
                    rate_rec.comment = comment
            rate_rec.save()
            rate_rec_all = models.Ratings.objects.filter(book=book)
            rate_all=[]
            for r in rate_rec_all:
                rate_all.append(r.rate)
            book.rate = sum(rate_all)/len(rate_all)
            book.save()

        borrow_hist = models.Borrow_histry(
            reader=borrow_rec.reader,
            book=borrow_rec.book,
            borrow_date=borrow_rec.date,
            return_date=datetime.datetime.now()
        )
        borrow_hist.save()
        borrow_rec.delete()
        book.num_lend = book.num_lend - 1
        book.save()

        context['message'] = '还书成功'
        template = loader.get_template('bookms/messages.html')
        return HttpResponse(template.render(context))

    return render(req, 'bookms/ReturnBook.html', context)


#续借
@login_required(login_url='/SignIn')
def Renewal(req, book_isbn):
    context = {
        'is_login': True,
        'user': req.user,
    }
    reader = models.Readers.objects.get(user=req.user)
    book = models.Books.objects.get(isbn=book_isbn)
    borrow_rec = models.Borrows.objects.get(reader=reader, book=book)

    if borrow_rec.repeat == 2:
        context['message'] = '只能续借两次！'
        template = loader.get_template('bookms/messages.html')
        return HttpResponse(template.render(context))
    elif borrow_rec.is_overdue():
        context['message'] = '不能续借过期图书，请先归还！'
        template = loader.get_template('bookms/messages.html')
        return HttpResponse(template.render(context))
    else:
        borrow_rec.repeat = borrow_rec.repeat + 1
        #borrow_rec.date = datetime.datetime.now()
        borrow_rec.save()

        template = loader.get_template('bookms/messages.html')
        context['message'] = '成功！'
        return HttpResponse(template.render(context))