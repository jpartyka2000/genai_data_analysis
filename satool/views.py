#import json

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect
import psycopg2

from satool.models import LoginModel, DataEntryModel, StudyPeriodModel
from satool.forms import LoginForm, DataEntryForm, VariableMatchingForm, TermClassificationForm, PositionToProfileMatchingForm, LocationClassificationForm, StudyPeriodForm
import aggtool

tool = aggtool.AggToolClass(debug=True, log_file=True)
form_dict = {}

def profile_popup(request):
    return render(request, 'satool/profile_popup.html')


def location_popup(request):
    return render(request, 'satool/location_popup.html')


def termination_popup(request):
    return render(request, 'satool/termination_popup.html')


@ensure_csrf_cookie
def index(request):
    if request.user.is_authenticated():
        form = LoginForm()
        context = {'form': form}
        return render(request, 'satool/index.html', context)
    else:
        return HttpResponseRedirect('/accessdenied/')



@ensure_csrf_cookie
def logout_user(request):
    if request.user.is_authenticated():
        logout(request)

    form = LoginForm()
    context = {'form': form}
    return render(request, 'satool/index.html', context)


def data_entry(request):
    if request.user.is_authenticated():
        welcome_message = "Study Aggregation Tool 0.1"
        data_entry_form = DataEntryForm()

        #get the list of clients
        companies_list = tool.get_all_clients()
        data_entry_form.set_client_field(companies_list)

        #set storage location with handler from aggtool class
        data_entry_form.fields['csv_file'].storage = tool.fs
        context = {'form': data_entry_form, 'auth_user': request.user}
        return render(request, 'satool/data_entry.html', context)
    else:
        context = {'form': form, 'auth_user':request.user}
        return render(request, 'satool/data_entry.html', context)

def variable_matching(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = DataEntryForm(request.POST, request.FILES)
        if form.is_valid():
            data_entry_object = DataEntryModel( client_name=request.POST['client_name'], \
                                                study_date=request.POST['study_date'], \
                                                study_name=request.POST['study_name'], \
                                                analyst_name=request.POST['analyst_name'], \
                                                csv_file = request.FILES['csv_file'])
            data_entry_object.save()
        else:
            context = {'form': form, 'auth_user':request.user}
            return render(request, 'satool/data_entry.html', context) 

    else:
        form = DataEntryForm()
        context = {'form': form, 'auth_user':request.user}
        return render(request, 'login.html', context)

def test_download(request):
    if request.method == 'POST':
        form = DataEntryForm(request.POST, request.FILES)
        if form.is_valid(): 
            data_entry_object = DataEntryModel( \
                client_name=request.POST['client_name'], \
                study_date=request.POST['study_date'], \
                study_name=request.POST['study_name'], \
                analyst_name=request.POST['analyst_name'], \
                csv_file = request.FILES['csv_file'])
            data_entry_object.save()

            context = {'form': form, 'file_name': data_entry_object.csv_file.name}
            return render(request, 'satool/test_download.html', context) 

        else:
            context = {'form': form}
            return render(request, 'satool/data_entry.html', context) 

    else:
        form = DataEntryForm()
        context = {'form': form}
        return render(request, 'satool/data_entry.html', context) 

def term_classification(request):
    if request.method == 'POST':
        #make sure the form is bound
        #https://docs.djangoproject.com/en/1.6/ref/forms/api/#bound-and-unbound-forms

        ###
        #
        #Big NOTE:  When using a customized init with ordered arguments,
        #you have to pass the POST
        #request as a parameter, not a default ordered argument, or else
        #the POST will bind to the default ordered argument.
        #In this case, the post was binding to the user if we had the
        #following Python statement:
        #
        #form = VariableMatchingForm(request.user, data=request.POST)
        #
        #instead of just:
        #
        #form = VariableMatchingForm(request.POST)
        #
        #see: https://code.djangoproject.com/ticket/9803
        #http://www.factory-h.com/blog/?p=196
        #http://agiliq.com/books/django-gotchas/forms.html

        headers_list = tool.get_column_headers() 
        form = VariableMatchingForm(column_headers=headers_list, data=request.POST)
        if form.is_valid(): 
            form_data = form.cleaned_data
            request.session['variable_matching_object'] = form_data

            tool.set_variable_matching_map(form_data)
            tool.set_client_profiles()
            tool.compute_term_position_location_frequency()
            term_reasons_list = tool.get_term_frequency()

            term_classification_form = TermClassificationForm(term_reasons=term_reasons_list)

            context = {'form': term_classification_form, 'term_reasons': term_reasons_list}
            return render(request, 'satool/term_classification.html', context) 

        else:
            context = {'form': form}
            return render(request, 'satool/variable_matching.html', context) 
    else:
        form = VariableMatchingForm()
        context = {'form': form}
        return render(request, 'satool/variable_matching.html', context) 


def position_to_profile_matching(request):
    if request.method == 'POST':
        term_reasons_list = tool.get_term_frequency()
        form = TermClassificationForm(term_reasons=term_reasons_list, data=request.POST)
        if form.is_valid(): 
            form_data = form.cleaned_data
            request.session['term_classification_object'] = form_data
            tool.set_term_classification_map(form_data)
            positions_match_list = tool.get_position_frequency()
            company_profiles_list = tool.get_client_profiles()

            position_to_profile_matching_form = PositionToProfileMatchingForm(positions_list=positions_match_list, profiles_list=company_profiles_list)

            context = {'form': position_to_profile_matching_form, 'positions_list': positions_match_list, 'profiles_list':company_profiles_list}
            return render(request, 'satool/position_to_profile_matching.html', context) 

        else:
            context = {'form': form}
            return render(request, 'satool/term_classification.html', context) 
    else:
        form = TermClassificationForm()
        context = {'form': form}
        return render(request, 'satool/term_classification.html', context) 


def location_classification(request):
    if request.method == 'POST':
        positions_match_list = tool.get_position_frequency()
        company_profiles_list = tool.get_client_profiles()
        form = PositionToProfileMatchingForm(positions_list=positions_match_list, profiles_list=company_profiles_list, data=request.POST)
        if form.is_valid(): 
            form_data = form.cleaned_data
            tool.set_position_to_profile_map(form_data)
            request.session['position_to_profile_matching_object'] = form_data
            locations_class_list = tool.get_location_frequency()

            location_classification_form = LocationClassificationForm(locations_list=locations_class_list)

            context = {'form': location_classification_form, 'locations_list': locations_class_list}
            return render(request, 'satool/location_classification.html', context) 

        else:
            context = {'form': form}
            return render(request, 'satool/position_to_profile_matching.html', context) 
    else:
        form = PositionToProfileMatchingForm()
        context = {'form': form}
        return render(request, 'satool/position_to_profile_matching.html', context) 


def study_period(request):
    if request.method == 'POST':
        locations_class_list = tool.get_location_frequency()
        form = LocationClassificationForm(locations_list=locations_class_list, data=request.POST)
        if form.is_valid(): 
            form_data = form.cleaned_data
            tool.set_location_classification_map(form_data)
            request.session['location_classification_object'] = form_data
            study_period_form = StudyPeriodForm()
            context = {'form': study_period_form}
            return render(request, 'satool/study_period.html', context) 

        else:
            context = {'form': form}
            return HttpResponse('invalid study period')
            return render(request, 'satool/location_classification.html', context) 
    else:
        form = LocationClassificationForm()
        context = {'form': form}
        return render(request, 'satool/location_classification.html', context) 


def get_model_fields(model_object):
    output_string = ''
    field_tuples = model_object._meta.get_fields_with_model()

    for tup in field_tuples:
        if tup[0].name != 'id':
            form_dict[tup[0].name] =  eval('model_object.' + str(tup[0].name))

            append_string = '%s: %s<br />' % (tup[0].name, eval('model_object.' + str(tup[0].name)))
            output_string += append_string

    output_string += '<hr />'

    return output_string
         

def get_session_data(session_data):
    output_string = ''

    for key in session_data.keys():
        if key != 'id':
            form_dict[key] = session_data.get(key)

            append_string = '%s: %s<br />' % (key, session_data.get(key))
            output_string += append_string

    output_string += '<hr />'

    return output_string


def produce_csv(request):
    if request.method == 'POST':
        form = StudyPeriodForm(request.POST)
        if form.is_valid(): 
            study_period_object = form.save()
            #request.session['study_period_object'] = study_period_object.pk
            #sp_object = StudyPeriodModel.objects.get(pk=request.session['study_period_object'])

            sp_object = StudyPeriodModel.objects.get(pk=study_period_object.pk)
            de_object = DataEntryModel.objects.get(pk=request.session['data_entry_object'])
            #de_data = request.session['data_entry_object']
            vm_data = request.session['variable_matching_object']
            tc_data = request.session['term_classification_object']
            pp_data = request.session['position_to_profile_matching_object']
            lc_data = request.session['location_classification_object']

            #final_string = get_session_data(de_data) + get_session_data(vm_data) + \
            final_string = get_model_fields(de_object) + get_session_data(vm_data) + \
                get_session_data(tc_data) + get_session_data(pp_data) + \
                get_session_data(lc_data) + get_model_fields(sp_object)

            tool.set_form_dictionary(form_dict)
            csv_url = tool.process_csv_data()

            context = {'agg_data': final_string, 'csv_url':csv_url}
            #context = {'agg_data': final_string, 'csv_url':de_object.csv_file.name}
            return render(request, 'satool/results.html', context) 

        else:
            context = {'form': form}
            return render(request, 'satool/study_period.html', context) 
    else:
        form = StudyPeriodForm()
        context = {'form': form}
        return render(request, 'satool/study_period.html', context) 
