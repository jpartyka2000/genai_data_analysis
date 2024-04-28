from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
#from django.shortcuts import render_to_response, render
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import authenticate, login, logout
#from axes.decorators import watch_login

from satool.forms import LoginForm, RegistrationForm
# from siteuser.models import SiteUser

def register_site_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/register/")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.clean_email()
            email = form.clean_email()
            password = BaseUserManager().make_random_password(length=6)


            auth_user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                auth_user.username = username
                auth_user.set_password(password)
                auth_user.save()
                # site_user, created = SiteUser.get_or_create_site_user(user=auth_user,
                #                                                       role=form.clean_role(),
                #                                                       email=email)
                # if created:
                #     site_user.save()
                context = {'form': form, 'auth_user': auth_user}
                return render(request, 'registrationSuccess.html', context)
            else:
                'user is already in the system'
                context = {'form': form, 'auth_user': request.user}
                return render(request, 'register.html', context)
        else:
            #return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
            return render(request, 'register.html', context)
    else:
        form = RegistrationForm()
        context = {'form':form}
        return render(request, 'register.html', context)
        #return render_to_response('register.html', context, context_instance=RequestContext(request))


def registration_failure(request):
    #return render_to_response('registrationFailure.html', {}, context_instance=RequestContext(request))
    return render(request, 'registrationFailure.html', {})


def lockout_site_user(request):
    context = {}
    return render(request, 'toomanyattempts.html', context)
    #return render(request, "loginSuccess.html", context)


def login_site_user(request):

    #@watch_login
    def login_inner_function(request, context):
        user = False
        if context['form']:
            context['form'].clean()
            username = context['form'].username
            password = context['form'].password
            user = authenticate(username=username, password=password)
        else:
            pass

        if user is not None:
            login(request, user)
            user, created = User.objects.get_or_create(username=username)
            if created:
                pass
            else:
                context['auth_user'] = request.user
            if username in ('ltanner','hbaines','achon','mriou'):
                return HttpResponseRedirect("/voltron")
            #return HttpResponseRedirect("/teamchemistry/")
            return render(request, 'loginSuccess.html', context)
        else:
            #The user's credentials are not valid
            context['form'].add_error('username', "Username/Password combination isn't valid!")
            context['auth_user'] = request.user
            return render(request, 'login.html', context)

    if request.method != 'POST' and request.user.is_authenticated():
        'auth_user is authenticated and does not need to login - just direct them successful login page'
        auth_user = request.user
        auth_user = User.objects.get(username=auth_user.username)
        if auth_user.username in ('ltanner','hbaines','achon','mriou'):
            return HttpResponseRedirect("/voltron/") 
        #return HttpResponseRedirect("/teamchemistry/")
        return render_to_response("loginSuccess.html", {'auth_user': auth_user}, context_instance=RequestContext(request))

    elif request.method == 'POST' and request.user.is_authenticated() != True:
        'auth_user is not authenticated and is attempting to login with a username and password'
        form = LoginForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            return login_inner_function(request, context)
        else:
            'form is not valid for non-authenticated auth_user, display login page with errors'
            return HttpResponseForbidden('login')

    else:
        'user is not submitting the form, show the blank login form'
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context , context_instance = RequestContext(request))


def forbid_site_user(request):
    return render_to_response('403.html',{}, RequestContext(request))


def logout_site_user(request):
    logout(request)
    context = {}
    return render(request, 'login.html', context)
