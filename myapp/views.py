from django.shortcuts import render, redirect
from .models import *
import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
import razorpay
from django.db.models import Sum


# ─────────────────────────────────────────────────────────────
#  CUSTOMER VIEWS
# ─────────────────────────────────────────────────────────────

def index(request):
    course = Courses.objects.all()
    return render(request, 'index.html', {'course': course})


def contact(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "User Already Exists"
            return render(request, 'contact.html', {'msg': msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mno=request.POST['mno'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype']
                )
                msg1 = "Register Successfully"
                return render(request, 'contact.html', {'msg1': msg1})
            else:
                msg = "Password & Confirm Password does not match !!"
                return render(request, 'contact.html', {'msg': msg})
    else:
        return render(request, 'contact.html')


def profile(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        user.name = request.POST['name']
        user.mno = request.POST['mno']
        try:
            user.profile = request.FILES['profile']
            user.save()
            request.session['profile'] = user.profile.url
        except:
            pass
        user.save()
        if user.usertype == "Customer":
            return redirect('index')
        elif user.usertype == "Manager":
            return redirect('mindex')
        elif user.usertype == "Admin":
            return redirect('admin_panel')
    else:
        if user.usertype == "Customer":
            return render(request, 'profile.html', {'user': user})
        elif user.usertype == "Manager":
            return render(request, 'mprofile.html', {'user': user})
        elif user.usertype == "Admin":
            return render(request, 'admin_panel.html', {'user': user})


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])

            if user.password == request.POST['password']:
                # Set session ONLY after password match
                request.session['email'] = user.email
                request.session['profile'] = user.profile.url

                if user.usertype == "Admin":
                    return redirect('admin_panel')     # → Super Admin Panel
                elif user.usertype == "Manager":
                    return redirect('mindex')          # → Teacher Dashboard
                else:
                    return redirect('index')           # → Customer Homepage
            else:
                msg = "Password does not match!"
                return render(request, 'login.html', {'msg': msg})

        except User.DoesNotExist:
            msg = "Email does not exist!"
            return render(request, 'login.html', {'msg': msg})

    return render(request, 'login.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['profile']
    except KeyError:
        pass
    return redirect('login')


def fpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            otp = random.randint(1001, 9999)
            subject = 'OTP FOR forgot-password'
            message = 'Hi ' + user.name + ' your otp is : ' + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            request.session['email'] = user.email
            request.session['otp'] = otp
            return render(request, 'otp.html')
        except:
            msg = "Email does not exist!!"
            return render(request, 'fpass.html', {'msg': msg})
    else:
        return render(request, 'fpass.html')


def otp(request):
    if request.method == "POST":
        try:
            otp = int(request.session['otp'])
            uotp = int(request.POST['uotp'])
            if otp == uotp:
                del request.session['otp']
                return render(request, 'newpass.html')
            else:
                msg = "Invalid OTP!!"
                return render(request, 'fpass.html', {'msg': msg})
        except:
            msg = "Something went wrong!"
            return render(request, 'otp.html', {'msg': msg})
    else:
        return render(request, 'otp.html')


def newpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['email'])
            if request.POST['npassword'] == request.POST['cnpassword']:
                user.password = request.POST['npassword']
                user.save()
                del request.session['email']
                return redirect('login')
            else:
                msg = "Password & Confirm password Does not Match !!"
                return render(request, 'newpass.html', {'msg': msg})
        except:
            msg = "Something went wrong!"
            return render(request, 'newpass.html', {'msg': msg})
    else:
        return render(request, 'newpass.html')


def cpass(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        try:
            if user.password == request.POST['opassword']:
                if request.POST['npassword'] == request.POST['cnpassword']:
                    user.password = request.POST['npassword']
                    user.save()
                    return redirect('logout')
                else:
                    msg = "New password & confirm new password does not match!!"
                    if user.usertype == "Customer":
                        return render(request, 'cpass.html', {'msg': msg})
                    elif user.usertype == "Manager":
                        return render(request, 'mcpass.html', {'msg': msg})
            else:
                msg = "Old password does not match!!"
                if user.usertype == "Customer":
                    return render(request, 'cpass.html', {'msg': msg})
                elif user.usertype == "Manager":
                    return render(request, 'mcpass.html', {'msg': msg})
        except Exception as e:
            msg = "Something went wrong: " + str(e)
            return render(request, 'cpass.html', {'msg': msg})
    else:
        if user.usertype == "Customer":
            return render(request, 'cpass.html')
        elif user.usertype == "Manager":
            return render(request, 'mcpass.html')


# ─────────────────────────────────────────────────────────────
#  COURSE VIEWS
# ─────────────────────────────────────────────────────────────

def about(request):
    return render(request, 'about.html')


def courses(request):
    courses = Courses.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def course_details(request):
    return render(request, 'course-details.html')


def events(request):
    return render(request, 'events.html')


def pricing(request):
    return render(request, 'pricing.html')


def starter_page(request):
    return render(request, 'starter.html')


def trainers(request):
    return render(request, 'trainers.html')


def cdetails(request, pk):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    course = Courses.objects.get(pk=pk)
    w = False
    try:
        Wishlist.objects.get(courses=course, user=user)
        w = True
    except Wishlist.DoesNotExist:
        w = False
    return render(request, 'cdetails.html', {'course': course, 'user': user, 'w': w})


def cpdetails(request, pk):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session.get('email'))
    course = Courses.objects.get(pk=pk)
    return render(request, 'cpdetails.html', {'course': course})


# ─────────────────────────────────────────────────────────────
#  WISHLIST VIEWS
# ─────────────────────────────────────────────────────────────

def addwish(request, pk):
    try:
        user = User.objects.get(email=request.session['email'])
        courses = Courses.objects.get(pk=pk)
        Wishlist.objects.get_or_create(user=user, courses=courses)
        return redirect('/wishlist/?added=1')
    except:
        return redirect('login')


def wishlist(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    wishlist = Wishlist.objects.filter(user=user)
    last_course = wishlist.last().courses if wishlist.exists() else None
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'course': last_course})


def delwish(request, pk):
    try:
        if 'email' not in request.session:
            return redirect('login')
        user = User.objects.get(email=request.session['email'])
        course = Courses.objects.get(pk=pk)
        Wishlist.objects.filter(user=user, courses=course).delete()
        return redirect('/wishlist/?deleted=1')
    except:
        return redirect('wishlist')


# ─────────────────────────────────────────────────────────────
#  CART / PAYMENT VIEWS
# ─────────────────────────────────────────────────────────────

def addcart(request, pk):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    courses = Courses.objects.get(pk=pk)
    Cart.objects.create(user=user, courses=courses, tprice=courses.cprice, qty=1, payment=False)
    return redirect('cart')


def cart(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user, payment=False)
    net = cart.aggregate(total=Sum('tprice'))['total'] or 0
    payment = None
    if net > 0:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': net * 100, 'currency': 'INR', 'payment_capture': 1})
    return render(request, 'cart.html', {'cart': cart, 'net': net, 'payment': payment})


def deletecart(request, pk):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    courses = Courses.objects.get(pk=pk)
    Cart.objects.filter(user=user, courses=courses, payment=False).delete()
    return redirect('cart')


def success(request):
    payment_id = request.GET.get('razorpay_payment_id')
    if not payment_id:
        return redirect('cart')
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=user, payment=False)
    for i in cart:
        i.payment = True
        i.save()
    return render(request, 'success.html', {'payment_id': payment_id})


# ─────────────────────────────────────────────────────────────
#  TEACHER (MANAGER) VIEWS
# ─────────────────────────────────────────────────────────────

def mindex(request):
    course = Courses.objects.all()
    return render(request, 'mindex.html', {'course': course})


def mabout(request):
    return render(request, 'mabout.html')


def add(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.session['email'])
            Courses.objects.create(
                user=user,
                cname=request.POST['cname'],
                cprice=request.POST['cprice'],
                desc=request.POST['desc'],
                duration=request.POST['duration'],
                tname=request.POST['tname'],
                texp=request.POST['texp'],
                cimage=request.FILES['cimage']
            )
            msg1 = "Course added successfully!"
            return render(request, 'add.html', {'msg1': msg1})
        except Exception as e:
            msg = f"Error: {str(e)}"
            return render(request, 'add.html', {'msg': msg})
    return render(request, 'add.html')


def view(request):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    course = Courses.objects.filter(user=user)
    return render(request, 'view.html', {'course': course})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Courses

def edit(request, pk):
    course = get_object_or_404(Courses, pk=pk)

    if request.method == "POST":
        course.cname = request.POST.get('cname')
        course.cprice = request.POST.get('cprice')
        course.desc = request.POST.get('desc')
        course.duration = request.POST.get('duration')
        course.tname = request.POST.get('tname')
        course.texp = request.POST.get('texp')

        # Only update image if new one uploaded
        if request.FILES.get('cimage'):
            course.cimage = request.FILES.get('cimage')

        if request.FILES.get('timage'):
            course.timage = request.FILES.get('timage')

        course.save()
        return redirect('admin_courses')

    return render(request, 'edit.html', {'course': course})


def delete(request, pk):
    if 'email' not in request.session:
        return redirect('login')
    user = User.objects.get(email=request.session['email'])
    course = Courses.objects.get(pk=pk)
    course.delete()
    return redirect('view')




def _get_admin_user(request):
    """Return User if logged-in Admin, else None."""
    if 'email' not in request.session:
        return None
    try:
        user = User.objects.get(email=request.session['email'])
        if user.usertype == "Admin":
            return user
    except User.DoesNotExist:
        pass
    return None


def admin_panel(request):
    """Dashboard — stats + recent users & courses."""
    user = _get_admin_user(request)
    if not user:
        return redirect('login')

    total_users   = User.objects.exclude(usertype="Admin").count()
    total_courses = Courses.objects.count()
    paid_orders   = Cart.objects.filter(payment=True)
    total_orders  = paid_orders.count()
    total_revenue = paid_orders.aggregate(rev=Sum('tprice'))['rev'] or 0

    # ✅ Exclude Admin from Recent Users
    recent_users = User.objects.exclude(usertype="Admin").order_by('-id')[:5]

    recent_courses = Courses.objects.order_by('-id')[:5]

    return render(request, 'admin_panel.html', {
        'admin_name':     user.name,
        'total_users':    total_users,
        'total_courses':  total_courses,
        'total_orders':   total_orders,
        'total_revenue':  total_revenue,
        'recent_users':   recent_users,
        'recent_courses': recent_courses,
    })
def admin_users(request):
    """List all registered users — excludes Admin accounts."""
    user = _get_admin_user(request)
    if not user:
        return redirect('login')

    # Exclude Admin accounts — show only Customers and Teachers (Managers)
    users = User.objects.exclude(usertype="Admin").order_by('id')
    return render(request, 'admin_users.html', {
        'admin_name': user.name,
        'users':      users,
    })


def admin_courses(request):
    """List all courses with Edit / Delete links."""
    user = _get_admin_user(request)
    if not user:
        return redirect('login')

    courses = Courses.objects.select_related('user').order_by('-id')
    return render(request, 'admin_courses.html', {
        'admin_name': user.name,
        'courses':    courses,
    })


def admin_orders(request):
    """List all successfully paid orders."""
    user = _get_admin_user(request)
    if not user:
        return redirect('login')

    orders        = Cart.objects.filter(payment=True).select_related('user', 'courses').order_by('-ttime')
    total_revenue = orders.aggregate(rev=Sum('tprice'))['rev'] or 0
    unique_buyers = orders.values('user').distinct().count()

    return render(request, 'admin_orders.html', {
        'admin_name':    user.name,
        'orders':        orders,
        'total_revenue': total_revenue,
        'unique_buyers': unique_buyers,
    })