from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from functools import reduce
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from string import ascii_letters
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



from django.core.cache import cache



from django.contrib.auth.decorators import user_passes_test

from django.conf import settings
import base64


#from .utils import paginator_func, items_list_func

# from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# rest
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import viewsets, views, status
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, UserSerializer, LoginSerializer,  RegisterSerializer

# jwt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

def user_is_not_superuser(user):
    return not user.is_superuser


def user_is_superuser(user):
    return user.is_superuser


User = get_user_model()



def sign_up(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    email = request.GET.get('email')
    if username and password:
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Email Verification'

            email_to = email
            email_from = settings.EMAIL_HOST_USER
            context = {'user': user, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(
                force_bytes(user.pk)), 'token': default_token_generator.make_token(user), 'email': email_to, 'scheme':request.scheme}
            email_template = render_to_string(
                'myapp/email/account-activate.html', context)
            verification_email = EmailMessage(
                email_subject, email_template, email_from, [email_to])
            verification_email.content_subtype = 'html'
            verification_email.send()

            # login(request, user)
            data = ['user-signup-success', user.username, user.email]
        except:
            data = ['user-signup-error']
        return JsonResponse(data, safe=False)

    else:
        messages.info(request, 'open>signupModal', extra_tags='signup>home')
        return redirect('home')


def sign_in(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    print(username, password)
    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        #     sms = 'user-auth-success'
        # else:
        #     sms = 'user-auth-error'
        # return HttpResponse(sms)
            data = ['user-auth-success', request.user.username]

        else:
            data = ['user-auth-error']
        print(data)

        return JsonResponse(data, safe=False)

    else:
        messages.info(request, 'open>loginModal', extra_tags='login>home')
        return redirect('home')



def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # user = UserModel._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # sms = 'Thank you for your email confirmation. Now you can login your account.'
        login(request, user)
        messages.info(request, f'open>profileModal>email-verification-success>{request.user.username}', extra_tags='acc_activate>home')
        return redirect('home')
    else:
        sms = 'Activation link is invalid!'
        return HttpResponse(sms)


def sign_in2(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        if user.is_superuser:
            return redirect('dashboard')
        else:
            messages.info(request, f'open>contentModal>',
                          extra_tags='login>home')
            return redirect('home')
    else:
        messages.info(request, 'Incorrect Username or Password')

    # return render(request, 'myapp/signin.html')
    return redirect('home')


def sign_out(request):
    logout(request)
    # return redirect('sign-in')
    return redirect('home')


@login_required
@user_passes_test(user_is_superuser)
def dashboard(request):
    if request.method == "POST":
        for i in request.POST:
            if 'item-' in i:
                pk = int(i.replace('item-', ''))

                if request.POST[i] != '':
                    item = Item.objects.get(id=pk)
                    item.title = request.POST[i]
                    item.save()
            if 'itemad-' in i:
                pk = int(i.replace('itemad-', ''))

                if request.POST[i] == 'on':
                    item = Item.objects.get(id=pk)
                    item.is_ad = True
                    item.save()

            if 'itemchecked-' in i:
                pk = int(i.replace('itemchecked-', ''))

                if request.POST[i] == 'on':
                    item = Item.objects.get(id=pk)
                    item.is_checked = True
                    item.save()

    items = Item.objects.all().order_by('-date_crawled')
    context = {'items': items}
    return render(request, 'myapp/dashboard.html', context)


@login_required
@user_passes_test(user_is_superuser)
def dashboard_is_checked(request):
    if request.method == "POST":
        for i in request.POST:
            if 'item-' in i:
                pk = int(i.replace('item-', ''))

                if request.POST[i] != '':
                    item = Item.objects.get(id=pk)
                    item.title = request.POST[i]
                    item.save()
            if 'itemad-' in i:
                pk = int(i.replace('itemad-', ''))

                if request.POST[i] == 'on':
                    item = Item.objects.get(id=pk)
                    item.is_ad = True
                    item.save()

            if 'itemchecked-' in i:
                pk = int(i.replace('itemchecked-', ''))

                if request.POST[i] == 'on':
                    item = Item.objects.get(id=pk)
                    item.is_checked = True
                    item.save()

    items = Item.objects.filter(is_checked=True).order_by('-date_crawled')
    context = {'items': items}
    return render(request, 'myapp/dashboard.html', context)


@login_required
@user_passes_test(user_is_superuser)
def dashboard_is_ad(request):
    if request.method == "POST":
        for i in request.POST:
            if 'item-' in i:
                pk = int(i.replace('item-', ''))

                if request.POST[i] != '':
                    item = Item.objects.get(id=pk)
                    item.title = request.POST[i]
                    item.save()
            if 'itemad-' in i:
                pk = int(i.replace('itemad-', 'on'))

                if request.POST[i] != '':
                    item = Item.objects.get(id=pk)
                    item.is_ad = True
                    item.save()

            if 'itemchecked-' in i:
                pk = int(i.replace('itemchecked-', 'on'))

                if request.POST[i] != '':
                    item = Item.objects.get(id=pk)
                    item.is_checked = True
                    item.save()

    items = Item.objects.filter(is_ad=True).order_by('-date_crawled')
    context = {'items': items}
    return render(request, 'myapp/dashboard.html', context)


@login_required
def save_to_gemme(request):
    img = request.GET.get('img', None)
    title = request.GET.get('title', None)
    if img and title:
        Item.objects.create(title=title, img_url=img)
    print('hey')
    return None


def home(request):
    domain = get_current_site(request)
    return render(request, 'myapp/spa.html', {"domain":domain})


@login_required
# @user_passes_test(user_is_not_superuser)
def profile(request, username):
    page = request.GET.get('page', 1)
    messages.info(request, 'open>profileModal>', extra_tags='profile>home')
    # return render(request, 'myapp/profile.html', context)
    return redirect('home')

@login_required
def profile_data(request):
    profile_img = request.GET.get('profileImg')
    print(request.FILES, request.GET, request.POST)
    return HttpResponse('k')

def search(request, query):
    page = request.GET.get('page', 1)

    if request.method == "POST":
        search_input = request.POST['search-input']
        request.session['query'] = query

    try:
        search_input = request.session['query']
        # items_list = Item.objects.filter(
        #     reduce(Q.__and__, [Q(title__icontains=s) for s in search_input]))
        # items_list = Item.objects.filter(title__icontains=search_input)
        items_list = items_list_func(search_input)

    except:
        items_list = Item.objects.all()
    cache.set('items_query', items_list, timeout=None)
    print(cache.get('items_query'))
    items = paginator_func(items_list, page)

    ads = items_list[:9]
    suggestions = items_list[:3]
    locants = items_list[:9]
    item_last = Item.objects.last()

    context = {'suggestions': suggestions, 'ads': ads, 'locants': locants,
               'item_last': item_last, 'items': items}
    # return render(request, 'myapp/base 3.html', context)
    query = query.replace('&$', '/')
    messages.info(
        request, f'open>searchModal>{query}', extra_tags='search>home')
    return redirect('home')


# def sort(request, query):
#     messages.info(request, f'open>contentModal>{query}', extra_tags='sort>home')
#     return redirect('home')

def sort(request, query):
    messages.info(request, f'open>category>{query}', extra_tags='sort>home')
    return redirect('home')


def user_auth(request):
    user_auth_get = request.GET.get('userAuthGet')
    if user_auth_get:
        print(request.user)
        if request.user.is_authenticated:
            data = 'user-auth-success'

        else:
            data = 'user-auth-error'

        return HttpResponse(data)
    else:
        return redirect('home')


def user_add_post(request):
    if request.user.is_authenticated:
        print(request.user)
        # sms = 'Authenticated'
        sms = 'open>profileModal'
    else:
        sms = 'open>loginModal>'

    messages.info(request, sms, extra_tags='user_add_post>home')
    return redirect('home')


def saved(request):
    messages.info(request, f'open>savedModal', extra_tags='saved>home')
    return redirect('home')


def menu(request):
    messages.info(request, f'open>menuModal', extra_tags='menu>home')
    return redirect('home')


def map(request):
    messages.info(request, f'open>mapModal', extra_tags='map>home')
    return redirect('home')


def post(request, id):
    page = request.GET.get('page', 1)
    post = Item.objects.get(id=id)

    if request.method == "POST":
        search_input = request.POST['search-input']
        request.session['query'] = search_input
        return redirect("search")

    items_list = items_list_func(post.title)
    print("poooossstttt")
    # items_list = cache.get('items_query')
    indx = 0
    indx_list = []
    try:
        for letter in post.url:
            if letter == '.':
                indx_list.append(indx)
            indx += 1
        f_indx = int(indx_list[0]+1)
        l_indx = int(indx_list[1])

        web_dmn = post.url[f_indx: l_indx]
    except:
        web_dmn = ''

    items = paginator_func(items_list, page)

    post.visits += 1
    post.save()

    ads = items_list[:9]
    suggestions = items_list[:3]
    locants = items_list[:9]
    item_last = Item.objects.last()

    context = {'post': post, 'web_dmn': web_dmn, 'suggestions': suggestions, 'ads': ads,
               'locants': locants, 'item_last': item_last, 'items': items}
    # return render(request, 'myapp/post copy.html', context)
    messages.info(request, f'open>postModal>{id}', extra_tags='post>home')
    return redirect('home')



def load_username(request):
    input_val = request.GET.get('inputVal')
    if input_val:
        users = User.objects.filter(username=input_val)
        if len(users) > 0:
            return HttpResponse("error")
        else:
            return HttpResponse("success")
    else:
        return redirect('home')


def load_data(request):
    search_input = request.GET.get('query')
    items_list = Item.objects.filter(description__istartswith=search_input)
    items = items_list[:6]
    data = [item.description for item in items]
    return JsonResponse(data, safe=False)


def home_data(request):
    page = request.GET.get('page')
    query = request.GET.get('query')
    pop_state = request.GET.get('popState')
    if page:
        start = (int(page) - 1) * 5
        end = 20 + start
        if query:
            items_list = Item.objects.filter(description__icontains=query)
        else:
            items_list = Item.objects.all()
        items = items_list[start:end]
        liked_items = request.session.get('liked_items')
        try:
            len(liked_items)
        except TypeError:
            liked_items = []

        data = []
        for item in items:
            try:
                # img_height = (item.height_field/item.width_field)*100
                img_height_width_ratio = (item.height_field/item.width_field)
                # print(img_height_width_ratio)
                item_dict = {'id': item.id, 'img': item.img.url,
                             'description': item.description, 'img_height_width_ratio': img_height_width_ratio}
                if item.id in liked_items:
                    item_dict['liked'] = "yes"
                else:
                    item_dict["liked"] = "no"
                data.append(item_dict)
            except:
                print('error')
        return JsonResponse(data, safe=False)
    elif pop_state:
        print('pop state', pop_state)
        return JsonResponse([], safe=False)
    else:
        data = []
        # page reloads
        messages = get_messages(request)
        for message in messages:
            # if 'spa>home' in message.tags:
            #     data.append(str(message))
            # elif 'post>home' in message.tags:
            #     data.append(str(message))
            # elif 'search>home' in message.tags:
            #     data.append(str(message))
            # elif 'saved>home' in message.tags:
            #     data.append(str(message))
            # elif 'menu>home' in message.tags:
            #     data.append(str(message))
            # elif 'map>home' in message.tags:
            #     data.append(str(message))
            data.append(str(message))

        return JsonResponse(data, safe=False)

def user(request):
    username = request.GET.get('username')
    try:
        User.objects.get(username=username)
        data = {}
        status = 200
    except:
        data = {}
        status = 404

    return JsonResponse(data, safe=False, status=status)

def saved_view(request):
    button_value = request.GET.get('buttonValue')
    button_id = request.GET.get('buttonId')
    # saved_items = request.session.get('saved_items')
    saved_items = cache.get('saved_items')
    saved_count = request.GET.get('savedCount')

    if button_value == 'saved':
        if saved_items:
            try:
                saved_items.append(int(button_id))
                # request.session['saved_items'] = saved_items
                cache.set('saved_items',  saved_items, timeout=None)

            except:
                return HttpResponse('id error')
            print('present')
        else:
            try:
                cache.set('saved_items',  [int(button_id)], timeout=None)
                # request.session['saved_items'] = [int(button_id)]
            except:
                return HttpResponse('id error')

        print(saved_items)
        return HttpResponse(f'item {button_id} saved')

    elif button_value == 'not-saved':
        try:
            saved_items.remove(int(button_id))
            # request.session['saved_items'] = saved_items
            cache.set('saved_items',  saved_items, timeout=None)

            print(saved_items)
            return HttpResponse(f'item {button_id} not saved')
        except:
            return HttpResponse('id error')

    elif saved_count:
        try:
            saved_items_count = len(saved_items)
        except TypeError:
            saved_items_count = 0
        return HttpResponse(saved_items_count)
    else:
        data = []
        try:
            len(saved_items)
        except TypeError:
            saved_items = []

        for item_id in saved_items:
            item = Item.objects.get(id=item_id)
            img_height_width_ratio = (item.height_field/item.width_field)
            item_dict = {'id': item.id, 'img': item.img.url,
                         'description': item.description, 'img_height_width_ratio': img_height_width_ratio}
            data.append(item_dict)
        return JsonResponse(data, safe=False)


def like_view(request):
    button_value = request.GET.get('buttonValue')
    button_id = request.GET.get('buttonId')
    liked_items = request.session.get('liked_items')
    saved_count = request.GET.get('savedCount')

    if button_value == 'liked':
        if liked_items:
            try:
                liked_items.append(int(button_id))
                request.session['liked_items'] = liked_items
            except:
                return HttpResponse('id error')
        else:
            try:
                request.session['liked_items'] = [int(button_id)]
            except:
                return HttpResponse('id error')
        return HttpResponse(f'item {button_id} liked')

    elif button_value == 'not-liked':
        try:
            liked_items.remove(int(button_id))
            request.session['liked_items'] = liked_items
            return HttpResponse(f'item {button_id} not liked')
        except:
            return HttpResponse('id error')

    elif saved_count:
        try:
            liked_items_count = len(liked_items)
        except TypeError:
            liked_items_count = 0
        return HttpResponse(liked_items_count)
    else:
        data = []
        try:
            len(liked_items)
        except TypeError:
            liked_items = []

        for item_id in liked_items:
            item = Item.objects.get(id=item_id)
            img_height_width_ratio = (item.height_field/item.width_field)
            item_dict = {'id': item.id, 'img': item.img.url,
                         'description': item.description, 'img_height_width_ratio': img_height_width_ratio}
            data.append(item_dict)
        return JsonResponse(data, safe=False)


def search_data(request):
    search_input = request.GET.get('query')
    page = request.GET.get('page')
    start = (int(page) - 1) * 5
    end = 20 + start

    items_list = items_list_func(search_input)
    items = items_list[start:end]
    liked_items = request.session.get('liked_items')
    try:
        len(liked_items)
    except TypeError:
        liked_items = []

    data = []

    for item in items:
        img_height_width_ratio = (item.height_field/item.width_field)
        item_dict = {'id': item.id, 'img': item.img.url,
                     'description': item.description, 'img_height_width_ratio': img_height_width_ratio}
        if item.id in liked_items:
            item_dict['liked'] = "yes"
        else:
            item_dict["liked"] = "no"
        data.append(item_dict)

    return JsonResponse(data, safe=False)


def post_data(request):
    post_id = request.GET.get('postId')
    item = Item.objects.get(id=int(post_id))

    indx = 0
    indx_list = []
    try:
        for letter in item.url:
            if letter == '.':
                indx_list.append(indx)
            indx += 1
        f_indx = int(indx_list[0]+1)
        l_indx = int(indx_list[1])

        web_dmn = item.url[f_indx: l_indx]
    except:
        web_dmn = ''

    contacts = []
    for contact in item.itemcontact_set.all():
        contacts.append([contact.type, contact.description])
    # print(contacts)
    # contacts.append(['nc', '0658589758'])

    img_height_width_ratio = (item.height_field/item.width_field)
    data = {'id': item.id, 'img': item.img.url, 'desc': item.description,
            'url': item.url, 'date': item.date_crawled, 'lon': item.lon, 'lat': item.lat, 'src': web_dmn, 'img_height_width_ratio': img_height_width_ratio, 'contacts': contacts}
    return JsonResponse(data)


def get_coord(request):
    # x = 1
    get_coords = request.GET.get('getCoords')
    item_retrieve_init = request.GET.get('itemRetrieveInit', 0)
    item_retrieve_init = int(item_retrieve_init)
    item_retrieve_end = item_retrieve_init + 8
    items_list = Item.objects.all()[item_retrieve_init:item_retrieve_end]
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        request.session['coord'] = {'lat': float(lat), 'lon': float(lon)}
        data = {'coord': request.session['coord']}
        return JsonResponse(data)

    if get_coords:
        item = Item.objects.last()
        try:
            img = item.img.url
        except:
            img = item.img_url
        # data = request.session['coord']
        data = {'origin': request.session['coord'], 'destination': {
            'lat': item.lat, 'lon': item.lon}}
        return JsonResponse(data, safe=False)

    data = []
    for item in items_list:
        try:
            img = item.img.url
        except:
            img = item.img_url
        data.append({'id': item.id, 'img': img, 'title': item.title,
                     'lat': item.lat, 'lon': item.lon})

    # data = serializers.serialize("json", data)
    # data = {"lon": lon, "lat": lat}

    return JsonResponse(data, safe=False)

def coords(request):
    page = request.GET.get('page')
    search_query = request.GET.get('query', '')
    # query = Item.objects.filter(description=search_query)
    # query = Item.objects.all()
    # data = paginator_func(items, page)
    query = items_list_func(search_query)
    paginator = Paginator(query, 10)
    try:
        paginator_page = paginator.page(page)
    except PageNotAnInteger:
        paginator_page = paginator.page(1)
    except EmptyPage:
        paginator_page = paginator.page(paginator.num_pages)

    items = [{'id': x.id, 'img': x.img.url, 'desc': x.description,
              'hwr': x.height_field/x.width_field,
            #   'lat': -6.623 + 0.001 * random.randrange(823, 837), 'lng': 39.15 + 0.01*random.randrange(823, 837)
              'lat': -6.906438, 'lng': 39.171877
              } for x in paginator_page]
    data = {
        "count": paginator.count,
        "hasNext": paginator_page.has_next(),
        "hasPrevious": paginator_page.has_previous(),
        "results": items
    }
    return JsonResponse(items, safe=False)


def get_coord2(request):
    try:
        item_coord = Item.objects.filter(store__lon__isnull=False)[0]
        lat = item_coord.store.lat
        lon = item_coord.store.lon
        data = {"lon": lon, "lat": lat}
        return JsonResponse(data)
    except:
        lat = 0
        lon = 0
        data = {"lon": lon, "lat": lat}
        return JsonResponse(data)


def map_state(request):
    map_state = request.GET.get('mapState')
    # get_map_state = request.GET.get('getMapState')
    if map_state:
        request.session['map_state'] = map_state

    # elif get_map_state:
    map_state = request.session['map_state']
    return HttpResponse(map_state)

def paginator_func(items_list, page):

    paginator = Paginator(items_list, 16)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items


def feed(request):
    page = request.GET.get('page')
    search_query = request.GET.get('query','')
    # query = Item.objects.filter(description__icontains=search_query)

    # query = Item.objects.all()
    # data = paginator_func(items, page)
    items_list = items_list_func(search_query)
    paginator = Paginator(items_list, 20)
    try:
        paginator_page = paginator.page(page)
    except PageNotAnInteger:
        paginator_page = paginator.page(1)
    except EmptyPage:
        paginator_page = paginator.page(paginator.num_pages)

    saved_items = cache.get('saved_items')
    try:
        len(saved_items)
    except TypeError:
        saved_items = []

    items = [{'id': x.id, 'img': x.img.url, 'desc': x.description,
              'hwr': x.height_field/x.width_field,
              'isSaved': True if x.id in saved_items else False} for x in paginator_page]

    data = {
        "count": paginator.count,
        "hasNext": paginator_page.has_next(),
        "hasPrevious": paginator_page.has_previous(),
        "results": items
    }
    return JsonResponse(data, safe=False)

class LoginViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(viewsets.ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


def items_list_func(received_word):
    conj = 'is and not if are na watch elfu'.lower()#.split(' ')
    # conj = 'Naviforce hublot patteck pateck Macbook wallet watch iphone'.lower()#.split(' ')


    # removing back slash
    post_title = received_word.replace('\n', ' ')

    # removing non letters
    for i in post_title.split(' '):
        for x in i:
            if x not in ascii_letters:
                post_title = post_title.replace(i, '')


    post_title = post_title.lower().split(' ')
    search_query = []
    for i in post_title:
        if i not in conj:
            search_query.append(i)

    search_query = search_query[:5]
    items_query = []

    # looping on number of words in search_query
    for i in range(len(search_query)):
        max_indx = len(search_query) - i

        items_list = Item.objects.filter(reduce(Q.__and__, [Q(description__icontains=s) for s in search_query[0:max_indx]])).order_by('-date_crawled')

        # checking item_list_1 is put in items_query
        if i > 0:
            for items_query_item in items_query:
                # item_query_item is a db model query stored in items_query

                items_list = items_list.exclude(id__in=items_query_item)

        items_query.append(items_list)
        # end loop

    items_query_final = []
    for items_list in items_query:
        for item in items_list:
            items_query_final.append(item)

    # adding the rest of items not considering the search query (search_query)
    items_list = Item.objects.all().order_by('-date_crawled')
    for items_query_item in items_query:
        items_list = items_list.exclude(id__in=items_query_item)


    for item in items_list:
        items_query_final.append(item)

    # return Item.objects.all()
    return items_query_final