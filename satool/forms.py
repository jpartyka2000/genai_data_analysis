import difflib

from django import forms
from satool.models import LoginModel, DataEntryModel, StudyPeriodModel
from django.contrib.auth.models import User

#For all choices, we want the dropdown value to be what's submitted in the form
#That's why we have duplicate entries
COMPANY_NAMES = (
    ("Dillard's Inc.", "Dillard's Inc."),
    ("BJ's", "BJ's"),
    ("Nestle Waters", "Nestle Waters"),
    ("Foot Locker", "Foot Locker")
)

ANALYST_CHOICES = (
    ('Brent / Jenny', 'Brent / Jenny'), ('Michelle', 'Michelle'),
    ('Brent', 'Brent'), ('Jenny', 'Jenny'), ('Alex', 'Alex'),
    ('John', 'John'), ('Hung', 'Hung'), ('Bill', 'Bill')
)

TERM_CLASSIFICATIONS = (
    ('Voluntary', 'Voluntary'), ('Involuntary', 'Involuntary'),
    ('Missing', 'Missing'), ('Retained', 'Retained'), ('Neither', 'Neither')
)


COMPANY_PROFILES = (
    ('No Profile', 'No Profile'), ('Best Practice Profile', 'Best Practice Profile'),
    ('Sales Associate 1', 'Sales Associate 1'), ('Dock Worker 5', 'Dock Worker 5')
)

JOB_LEVEL = (
    ('Director', 'Director'), ('Individual Contributor', 'Individual Contributor'),
    ('Manager', 'Manager'), ('Not Profiled', 'Not Profiled'),
    ('Supervisor', 'Supervisor')
)

POSITION_TYPE = (
    ('Not Profiled', 'Not Profiled'), ('Sales', 'Sales'),
    ('Service', 'Service'), ('Supervisory', 'Supervisory')
)

LOCATION_CLASSIFICATION = (
    ('Open', 'Open'), ('Closed', 'Closed')
)

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LoginModel
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.username = cleaned_data.get("username")
        self.password = cleaned_data.get("password")




class DataEntryForm(forms.Form):
    client_name = forms.CharField(label='Company Name', widget=forms.Select(choices = []))
    #study_date = forms.DateField(initial='2001-01-01', help_text='Date format is either YYYY-MM-DD or MM/DD/YYYY')
    #study_name = forms.CharField(max_length=40, help_text='Enter a short description of the study')
    study_date = forms.DateField()
    study_name = forms.CharField(max_length=40)
    analyst_name = forms.CharField(max_length=50, widget=forms.Select(choices=ANALYST_CHOICES))
    csv_file = forms.FileField()


    def set_client_field(self, company_list):

        #set the field options to the values
        company_choices = zip(company_list, company_list)

        self.fields['client_name'].widget.choices = company_choices


class VariableMatchingForm(forms.Form):

    #create fields for the form
    employee_id = forms.CharField(label='Employee ID', widget=forms.Select(choices = []))
    first_name = forms.CharField(required=False, label='First Name', widget=forms.Select(choices = []))
    middle_name = forms.CharField(required=False, label='Middle Name', widget=forms.Select(choices = []))
    last_name = forms.CharField(required=False, label='Last Name', widget=forms.Select(choices = []))
    email = forms.CharField(required=False, label='Email', widget=forms.Select(choices = []))
    ssn = forms.CharField(required=False, label='SSN (4 digits)', widget=forms.Select(choices = []))
    position_name = forms.CharField(label='Position', widget=forms.Select(choices = []))
    profile_name = forms.CharField(label='Profile', widget=forms.Select(choices = []))
    work_schedule = forms.CharField(label='Full Time/Part Time/Seasonal/Temporary', widget=forms.Select(choices = []))
    location_info_1 = forms.CharField(label='Location Information 1', widget=forms.Select(choices = []))
    location_info_2 = forms.CharField(label='Location Information 2', widget=forms.Select(choices = []))
    location_info_3 = forms.CharField(label='Location Information 3', widget=forms.Select(choices = []))
    orig_hire_date = forms.CharField(label='Original Hire Date', widget=forms.Select(choices = []))
    date_in_position = forms.CharField(label='Date In Position', widget=forms.Select(choices = []))
    final_date = forms.CharField(label='Original Term Date', widget=forms.Select(choices = []))
    orig_term_reason = forms.CharField(label='Term Reason', widget=forms.Select(choices = []))
    pa_id = forms.CharField(label='PA ID', widget=forms.Select(choices = []))
    given_first_name = forms.CharField(label='Given First Name', widget=forms.Select(choices = []))
    given_last_name = forms.CharField(label='Given Last Name', widget=forms.Select(choices = []))
    given_email = forms.CharField(label='Given Email', widget=forms.Select(choices = []))
    given_ssn = forms.CharField(label='Given SSN', widget=forms.Select(choices = []))
    match_last_name = forms.CharField(label='Match Last Name', widget=forms.Select(choices = []))
    match_email = forms.CharField(label='Match Email', widget=forms.Select(choices = []))
    match_ssn = forms.CharField(label='Match SSN', widget=forms.Select(choices = []))
    pma_time = forms.CharField(label='PMA Time', widget=forms.Select(choices = []))
    ppi_minutes = forms.CharField(label='PPI Time', widget=forms.Select(choices = []))
    consistency = forms.CharField(label='Consistency', widget=forms.Select(choices = []))
    click_through = forms.CharField(label='Click Through', widget=forms.Select(choices = []))   
    sequence = forms.CharField(label='Sequence', widget=forms.Select(choices = []))   
    distortion = forms.CharField(label='Distortion', widget=forms.Select(choices = []))   
    lcs_length = forms.CharField(label='LCS Length', widget=forms.Select(choices = []))   
    lcs_frequency = forms.CharField(label='LCS Frequency', widget=forms.Select(choices = []))   
    tests_taken = forms.CharField(label='Tests Taken', widget=forms.Select(choices = []))   
    earliest_test_completion = forms.CharField(label='Earliest Test Completion', widget=forms.Select(choices = []))   
    latest_test_completion = forms.CharField(label='Latest Test Completion', widget=forms.Select(choices = []))   
    earliest_assessment_completion = forms.CharField(label='Earliest Assessment Completion', widget=forms.Select(choices = []))   
    latest_assessment_completion = forms.CharField(label='Latest Assessment Completion', widget=forms.Select(choices = []))   
    fit_score = forms.CharField(label='Fit Score for Profile', widget=forms.Select(choices = []))   
    matched_how = forms.CharField(label='Match Type', widget=forms.Select(choices = []))   
    multiple_entries = forms.CharField(label='Multiple Entries', widget=forms.Select(choices = []))   
    incomplete_entry = forms.CharField(label='Incomplete Entry', widget=forms.Select(choices = []))   
    good_or_questionable_match = forms.CharField(label='Good or Questionable Match', widget=forms.Select(choices = []))   
    ppi_minutes_flagged= forms.CharField(label='PPI Time QC Test', widget=forms.Select(choices = []))   
    consistency_flagged = forms.CharField(label='Inconsistency QC Test', widget=forms.Select(choices = []))   
    click_through_flagged = forms.CharField(label='Click Through QC Test', widget=forms.Select(choices = []))   
    sequence_flagged = forms.CharField(label='Sequence QC Test', widget=forms.Select(choices = []))   
    distortion_flagged = forms.CharField(label='Distortion QC Test', widget=forms.Select(choices = []))   
    lcs_length_flagged = forms.CharField(label='LCS Length QC Test', widget=forms.Select(choices = []))   
    num_qc_flags = forms.CharField(label='Sum of QC Tests', widget=forms.Select(choices = []))   
    assessed_before_hired = forms.CharField(label='Assessed Before Hired?', widget=forms.Select(choices = []))   
    predeploy_start = forms.CharField(label='Beginning of Pre-Deployment', widget=forms.Select(choices = []))   
    predeploy_end = forms.CharField(label='End of Pre-Deployment', widget=forms.Select(choices = []))   
    postdeploy_start = forms.CharField(label='Beginning of Post Deployment', widget=forms.Select(choices = []))   
    postdeploy_end = forms.CharField(label='End of Post-Deployment', widget=forms.Select(choices = []))   
    hire_pre_or_post = forms.CharField(label='Hired in Pre or Post', widget=forms.Select(choices = []))   
    term_pre = forms.CharField(label='Termed in Pre or Post', widget=forms.Select(choices = []))   
    days_employed = forms.CharField(label='Length of Employment', widget=forms.Select(choices = []))   
    trimmed_term_date = forms.CharField(label='Trimmed Term Date', widget=forms.Select(choices = []))   
    trimmed_term_reason = forms.CharField(label='Trimmed Term Reason', widget=forms.Select(choices = []))   
    term_category = forms.CharField(label='VIN', widget=forms.Select(choices = []))   

    def __init__(self, *args, **kwargs):
        header_list = kwargs.pop('column_headers') #remove argument before call to super
        super(VariableMatchingForm, self).__init__(*args, **kwargs)

        #set the field options to the values
        field_choices = zip(header_list, header_list)

        #first value is 'No Match'
        field_choices.insert(0, ('None', 'No Match'))

        #set field choices and default value of field with "best guess"
        for value in self.fields.keys():
            self.fields[value].widget.choices = field_choices

            #give at most two best guesses from the header list that are at least a 10% match, higher score first
            #default is 0.6, but we want guesses for every field
            default_guesses = difflib.get_close_matches(value, header_list, 2, 0.1)

            if len(default_guesses) == 0:
                self.fields[value].initial = 'No Match'
            else:
                self.fields[value].initial = default_guesses[0] 



class TermClassificationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        term_reasons = kwargs.pop('term_reasons') #remove argument before call to super
        super(TermClassificationForm, self).__init__(*args, **kwargs)

        for index, reason_dict in enumerate(term_reasons):
            #outstring = 'index = %s\nreason = %s\ncount = %s\n' % (str(index), reason_dict['reason'], str(reason_dict['count']))
            #fp.write(outstring)
            reason_string = """forms.CharField(max_length=100, label='Term Reason', initial="%s", widget=forms.TextInput(attrs={'readonly':'readonly'}))""" % reason_dict['reason']
            count_string = "forms.CharField(max_length=8, label='Count', initial='%d', widget=forms.TextInput(attrs={'readonly':'readonly'}))" % reason_dict['count']
            self.fields['term_reason_%s' % index] = eval(reason_string)
            self.fields['term_count_%s' % index] = eval(count_string)
            self.fields['term_category_%s' % index] = forms.CharField(max_length=40, label='Category', widget=forms.Select(choices=TERM_CLASSIFICATIONS)) 


class PositionToProfileMatchingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        profiles_list = kwargs.pop('profiles_list') #remove argument before call to super
        positions_list = kwargs.pop('positions_list') #remove argument before call to super
        super(PositionToProfileMatchingForm, self).__init__(*args, **kwargs)

        profile_choices = zip(profiles_list, profiles_list)
        profile_choices.insert(0, ('Best Practice Profile', 'Best Practice Profile'))
        profile_choices.insert(0, ('Not Profiled', 'Not Profiled'))

        for index, positions_dict in enumerate(positions_list):
            position_string = """forms.CharField(max_length=100, label='Unique Position', initial="%s", widget=forms.TextInput(attrs={'readonly':'readonly'}))""" % \
                    positions_dict['unique_position']
            count_string = "forms.CharField(max_length=8, label='Count', initial='%d', widget=forms.TextInput(attrs={'readonly':'readonly'}))" % positions_dict['count']
            self.fields['position_%s' % index] = eval(position_string)
            self.fields['position_count_%s' % index] = eval(count_string)
            #self.fields['profile_%s' % index] = forms.CharField(max_length=75, label='Profile', widget=forms.Select(choices=COMPANY_PROFILES))
            self.fields['profile_%s' % index] = forms.CharField(max_length=75, label='Profile', widget=forms.Select(choices=profile_choices))
            self.fields['job_level_%s' % index] = forms.CharField(max_length=70, label='Job Level', widget=forms.Select(choices=JOB_LEVEL))
            self.fields['position_type_%s' % index] = forms.CharField(max_length=70, label='Position Type', widget=forms.Select(choices=POSITION_TYPE))

    def set_profile_field(self, company_list):

        #set the field options to the values
        company_choices = zip(company_list, company_list)

        self.fields['client_name'].widget.choices = company_choices


class LocationClassificationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        locations_list = kwargs.pop('locations_list') #remove argument before call to super
        super(LocationClassificationForm, self).__init__(*args, **kwargs)
        for index, locations_dict in enumerate(locations_list):
            location_string = """forms.CharField(max_length=100, label='Unique Location', initial="%s", widget=forms.TextInput(attrs={'readonly':'readonly'}))""" % \
                    locations_dict['unique_location']
            count_string = "forms.CharField(max_length=8, label='Count', initial='%d', widget=forms.TextInput(attrs={'readonly':'readonly'}))" % locations_dict['count']
            self.fields['location_%s' % index] = eval(location_string)
            self.fields['location_count_%s' % index] = eval(count_string)
            self.fields['location_class_1_%s' % index] = forms.CharField(max_length=10, label='Location Class 1', widget=forms.Select(choices=LOCATION_CLASSIFICATION))
            self.fields['location_class_2_%s' % index] = forms.CharField(required=False, max_length=70, label='Location Class 2')
            self.fields['location_class_3_%s' % index] = forms.CharField(required=False, max_length=70, label='Location Class 3')
            self.fields['location_class_4_%s' % index] = forms.CharField(required=False, max_length=70, label='Location Class 4')


class StudyPeriodForm(forms.ModelForm):
    study_period_start_2 = forms.DateField(required=False)
    study_period_start_3 = forms.DateField(required=False)
    study_period_start_4 = forms.DateField(required=False)
    study_period_end_2 = forms.DateField(required=False)
    study_period_end_3 = forms.DateField(required=False)
    study_period_end_4 = forms.DateField(required=False)
    minimum_days_2 = forms.IntegerField(required=False)
    minimum_days_3 = forms.IntegerField(required=False)
    minimum_days_4 = forms.IntegerField(required=False)

    class Meta:
        model = StudyPeriodModel
        fields = ['study_period_start_1', 'study_period_start_2', \
            'study_period_start_3', 'study_period_start_4', \
            'study_period_end_1', 'study_period_end_2', 'study_period_end_3', \
            'study_period_end_4', 'minimum_days_1', 'minimum_days_2', \
            'minimum_days_3', 'minimum_days_4', 'study_period_link_1', \
            'study_period_link_2', 'study_period_link_3', 'study_period_link_4']


class RegistrationForm(forms.ModelForm):
    "This is used to register the associated AuthUser"
    email = forms.EmailField(label=(u'Email Address'))
    role = forms.CharField(label=(u'Role'))

    class Meta:
        model = User
        fields = ('email', 'role')
        #exclude = ('user') #add other field you don't want either
        # use fields to add or exclude to remove fields from form

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError('That email is already in the system. Make sure you have not already registered.')

    def clean_role(self):
        role = self.cleaned_data['role']
        roles = ['Behavioral Analyst', 'Behavioral Scientist', 'Data Analyst', 'R&D Engineer', 'R&D Scientist', \
                 'Client Account Manager', 'HCM Personnel']
        if role not in roles:
            raise forms.ValidationError('You have not selected a role. Please try again!')

