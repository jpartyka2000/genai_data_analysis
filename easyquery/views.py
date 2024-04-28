from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db import connection
from easyquery.forms import EasyQueryInputForm
from easyquery.models import EasyQueryStudies
from easyquery.models import EasyQueryHistory
from easyquery import prompt_strings
from satool import aggtool

import datetime
import os
import re
import sys
import time
import pandas as pd
import numpy as np
import json
import copy
import math
import nltk
import io

from textblob import TextBlob
from googletrans import Translator
from datetime import datetime
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

tool = aggtool.AggToolClass(debug=True, log_file=False)
regex_mappings = {}
upload_regex = re.compile(",\"([^\",\n]*?)[,|\n|\"|\t]([^\"]*?)\",?")

#nltk.download('punkt')
#nltk.download('stopwords')

def call_gpt(prompt_text, background_context_str=""):
    
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)

    #response = openai.ChatCompletion.create(
    response = client.chat.completions.create(
    messages=[{"role": "system", "content": background_context_str},
              {"role": "user", "content": prompt_text}],
    model='gpt-3.5-turbo',   #gpt-3.5-turbo   #gpt-3.5-turbo-0301  #gpt-4
    temperature=0,
    max_tokens=2000,
    frequency_penalty=0,
    presence_penalty=0
    )

    answer_text = response.choices[0].message.content

    return answer_text

#def call_gpt(prompt_text):
#
#    openai.api_key = os.environ['OPENAI_API_KEY']
#
#    #start_time = time.time()
#
#    response = openai.Completion.create(
#    engine="text-davinci-003",
#    prompt=prompt_text,
#    temperature=0.1,
#    max_tokens=2000,
#    top_p=1,
#    frequency_penalty=0,
#    presence_penalty=0
#    )
#
#    answer_text = response.choices[0].text
#
#    return answer_text

@ensure_csrf_cookie
def index(request):

    context = {}

    welcome_message = "Welcome to EasyQuery"
    form = EasyQueryInputForm()

    #username = request.user.username
    #first_name = request.user.first_name
    #last_name = request.user.last_name


    context['welcome_message'] = welcome_message
    context['form'] = form

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM EASYQUERY_HISTORY")

    return render(request, 'easyquery/index.html', context)

def index_v1(request):

    context = {}

    welcome_message = "Welcome to EasyQuery"
    welcome_message_description = "Data Analysis for EVERYBODY"

    form = EasyQueryInputForm()

    #username = request.user.username
    #first_name = request.user.first_name
    #last_name = request.user.last_name


    context['welcome_message'] = welcome_message
    context['welcome_message_description'] = welcome_message_description
    context['form'] = form

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM EASYQUERY_HISTORY")

    return render(request, 'easyquery/indexv1.html', context)

    

def to_do_list_teams(request):

    context = {}

    welcome_message = "Welcome to EasyQuery"
    welcome_message_description = "Data Analysis for EVERYBODY"

    form = EasyQueryInputForm()

    #username = request.user.username
    #first_name = request.user.first_name
    #last_name = request.user.last_name


    context['welcome_message'] = welcome_message
    context['welcome_message_description'] = welcome_message_description
    context['form'] = form

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM EASYQUERY_HISTORY")

    return render(request, 'easyquery/to_do_list_teams.html', context)

def to_do_list_roadmap(request):

    context = {}

    welcome_message = "Welcome to EasyQuery"
    welcome_message_description = "Data Analysis for EVERYBODY"

    form = EasyQueryInputForm()

    #username = request.user.username
    #first_name = request.user.first_name
    #last_name = request.user.last_name


    context['welcome_message'] = welcome_message
    context['welcome_message_description'] = welcome_message_description
    context['form'] = form

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM EASYQUERY_HISTORY")

    return render(request, 'easyquery/to_do_list_roadmap.html', context)

def to_do_list_questions(request):

    context = {}

    welcome_message = "Welcome to EasyQuery"
    welcome_message_description = "Data Analysis for EVERYBODY"

    form = EasyQueryInputForm()

    #username = request.user.username
    #first_name = request.user.first_name
    #last_name = request.user.last_name


    context['welcome_message'] = welcome_message
    context['welcome_message_description'] = welcome_message_description
    context['form'] = form

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM EASYQUERY_HISTORY")

    return render(request, 'easyquery/to_do_list_questions.html', context)

def processmatch(matchobj):

    thestr = matchobj.group(0)
    match_start = matchobj.start()

    if thestr in regex_mappings:
        last_regex_end_index = match_start + (len(thestr)) - 1
        # regex_file.write('cached regex: ' + thestr + '\n')
        # regex_file.write("final: " + regex_mappings[thestr] + '\n')
        # regex_file.write("----------" + '\n')
        return regex_mappings[thestr]

    # regex_file.write("regex selected: " + thestr + '\n')

    matchstr_front_idx = thestr.find("\"")
    matchstr_back_idx = thestr.rfind("\"")
    matchstr_prefix_str = thestr[:matchstr_front_idx + 1]
    matchstr_suffix_str = thestr[matchstr_back_idx:]
    quoted_portion_str = thestr[matchstr_front_idx + 1:matchstr_back_idx]
    quoted_portion_str = quoted_portion_str.replace(",", ";")
    quoted_portion_str = quoted_portion_str.replace("\n", ";")
    quoted_portion_str = quoted_portion_str.replace("\"", ";")

    # regex_file.write("prefix: " + matchstr_prefix_str + '\n')
    # regex_file.write("quoted: " + quoted_portion_str + '\n')
    # regex_file.write("suffix: " + matchstr_suffix_str + '\n')
    # regex_file.write("final: " + matchstr_prefix_str + quoted_portion_str + matchstr_suffix_str + '\n')
    # regex_file.write("----------" + '\n')

    # add to regex_mappings
    regex_mappings[thestr] = matchstr_prefix_str + quoted_portion_str + matchstr_suffix_str

    return matchstr_prefix_str + quoted_portion_str + matchstr_suffix_str

@csrf_exempt
def create_new_study(request):

    regex_mappings.clear()

    # load csv file uploaded by user
    if 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']

        with open(tool.fs.location + "/" + csv_file.name, 'wb+') as destination:
            for chunk in csv_file.chunks():

                #convert to string so that we can apply regex to the chunk
                chunk = chunk.decode('utf-8')

                chunk = re.sub(r'[^\x00-\x7F]+', '', chunk)

                # remove null bytes
                chunk = chunk.replace('\x00', "")

                # remove all embedded commas, newlines and double quotes
                chunk = upload_regex.sub(processmatch, chunk)

                #convert back to bytes obj
                chunk = bytes(chunk, 'utf-8')

                destination.write(chunk)

        tool.read_csv_data_from_file(csv_file)

    else:
        error_string = "CSV upload error encountered"
        context = {"error_msg":error_string}
        return render(request, 'easyquery/index.html', context)

    headers_list = tool.get_column_headers()
    file_data = tool.get_csv_data()

    # get the MAX value of study_id
    try:
        this_study_id = int(EasyQueryStudies.objects.using('xactly_dev').latest('study_id').study_id) + 1
    except Exception:
        this_study_id = 1

    this_study_name = request.POST['study_name']
    this_user_id = 1
    this_created_date = time.strftime("%Y-%m-%d %I:%M")

    # now insert a new row into the bigtex_studies table
    EasyQueryStudies.objects.using("xactly_dev").create(study_id=this_study_id, study_name=this_study_name, created_by=this_user_id, created_date=this_created_date)

    #create dataframe out of file headers and data
    df_data = pd.DataFrame(file_data, columns=headers_list)

    #store as a session variable
    request.session['df_data'] = df_data.to_json()

    #convert dataframe to html string that is sent to data_display.html
    df_html_str = df_data.to_html(index=False)

    context = {}

    context['df_html_str'] = df_html_str
    context['study_id'] = this_study_id

    # EasyQueryHistory.objects.using("xactly_dev").create(df_html_str_req=df_html_str, user_question='Data Load', output_str='', df_html_str_res='', study_name=this_study_name)

    return render(request, 'easyquery/data_display.html', context)


def create_new_study_v1(request):

    regex_mappings.clear()
    print("sfsdfsdfsfsdfsd")
    # load csv file uploaded by user
    if 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']

        with open(tool.fs.location + "/" + csv_file.name, 'wb+') as destination:
            for chunk in csv_file.chunks():

                #convert to string so that we can apply regex to the chunk
                chunk = chunk.decode('utf-8')

                chunk = re.sub(r'[^\x00-\x7F]+', '', chunk)

                # remove null bytes
                chunk = chunk.replace('\x00', "")

                # remove all embedded commas, newlines and double quotes
                chunk = upload_regex.sub(processmatch, chunk)

                #convert back to bytes obj
                chunk = bytes(chunk, 'utf-8')

                destination.write(chunk)

        tool.read_csv_data_from_file(csv_file)

    else:
        error_string = "CSV upload error encountered"
        context = {"error_msg":error_string}
        return render(request, 'easyquery/index.html', context)

    headers_list = tool.get_column_headers()
    file_data = tool.get_csv_data()

    # get the MAX value of study_id
    try:
        this_study_id = int(EasyQueryStudies.objects.using('xactly_dev').latest('study_id').study_id) + 1
    except Exception:
        this_study_id = 1

    this_study_name = request.POST['study_name']
    this_user_id = 1
    this_created_date = time.strftime("%Y-%m-%d %I:%M")

    # now insert a new row into the bigtex_studies table
    EasyQueryStudies.objects.using("xactly_dev").create(study_id=this_study_id, study_name=this_study_name, created_by=this_user_id, created_date=this_created_date)

    #create dataframe out of file headers and data
    df_data = pd.DataFrame(file_data, columns=headers_list)

    request.session['df_data'] = df_data.to_json()

    def custom_styling(df):
        return (df.style
            .set_table_attributes('class="custom-table"')
    )

    styled_df = custom_styling(df_data)
    #store as a session variable

    #convert dataframe to html string that is sent to data_display.html
    df_html_str = styled_df.to_html()

    context = {}

    context['df_html_str'] = df_html_str
    context['study_id'] = this_study_id
    context['this_study_name'] = this_study_name


    # EasyQueryHistory.objects.using("xactly_dev").create(df_html_str_req=df_html_str, user_question='Data Load', output_str='', df_html_str_res='', study_name=this_study_name)

    return render(request, 'easyquery/data_display_v1.html', context)

#for semantic similarity calculations
def calculate_similarity(row):

    stop_words = list(set(stopwords.words('english')))

    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf_vectorizer.fit_transform([row['latest_customer_tweet'], row['latest_customer_tweet_old']])
    return cosine_similarity(tfidf_matrix)[0, 1]

def switch_columns_order(df):
    columns = df.columns.tolist()
    index_industry = columns.index('Industry')
    index_created = columns.index('created')
    columns[index_industry], columns[index_created] = columns[index_created], columns[index_industry]
    return df[columns]


@csrf_exempt
def custom_styling(df):
        return (df.style
            .set_table_attributes('class="custom-table"')
    )

@csrf_exempt
def answer_user_question(request):

    user_question = request.POST['user_question']

    #get the df_data session variable as a Dataframe object
    df_data_json = request.session['df_data']

    df_data = pd.read_json(df_data_json)

    #in case there is an error, do not change the data frame contents
    df_html_str = df_data.to_html(index=False)

    #user_question = "Make a 'sentiment' column that contains +, - or 0 values associated with each row in the 'latest_customer_tweet' column."
    #user_question = "Add column 'Revenue2'"

    #first, determine the query category
    gpt_category_str = call_gpt(prompt_strings.query_category_prelim_str + user_question).replace("\n","").replace(".","")

    print("gpt_category_str = " + gpt_category_str)

    prelim_instructions_str = None
    imputation_values = {}

    if gpt_category_str == 'Delete column':
        prelim_instructions_str = prompt_strings.drop_column_prelim_str
    elif gpt_category_str == 'Add column':
        prelim_instructions_str = prompt_strings.add_column_prelim_str
    elif gpt_category_str == 'Update values':
        prelim_instructions_str = prompt_strings.update_values_prelim_str
    elif gpt_category_str == 'Add sentiment':
        prelim_instructions_str = prompt_strings.add_sentiment_column_prelim_str
    elif gpt_category_str == 'Rename column':
        prelim_instructions_str = prompt_strings.rename_column_prelim_str
    elif gpt_category_str == 'Change data type':
        prelim_instructions_str = prompt_strings.change_data_type_prelim_str
    elif gpt_category_str == 'Switch columns':
        prelim_instructions_str = prompt_strings.switch_columns_prelim_str
    elif "Delete rows" in gpt_category_str:
        prelim_instructions_str = prompt_strings.delete_rows_prelim_str
    elif "Translate column" in gpt_category_str:
        prelim_instructions_str = prompt_strings.translate_text_column_prelim_str
        translator = Translator()
    elif "Ordinal encoding" in gpt_category_str:
        prelim_instructions_str = prompt_strings.ordinal_encoding_prelim_str
    elif "One-hot encoding" in gpt_category_str:
        prelim_instructions_str = prompt_strings.one_hot_encoding_prelim_str
    elif "Key topics" in gpt_category_str:
        prelim_instructions_str = prompt_strings.key_topic_words_prelim_str
    elif "Semantic similarity" in gpt_category_str:
        prelim_instructions_str = prompt_strings.semantic_similarity_prelim_str
    elif "Drop duplicates" in gpt_category_str:
        prelim_instructions_str = prompt_strings.drop_duplicates_prelim_str
    elif "Impute values" in gpt_category_str:
        prelim_instructions_str = prompt_strings.impute_values_prelim_str
        
        imputation_values = {
            col: df_data[col].mean() if df_data[col].dtype == 'float64' else df_data[col].mode().iloc[0]
            for col in df_data.columns
        }
        
        print(imputation_values)
        
    elif gpt_category_str == "[]":

        #we have flagged an irrelevant/inappropriate question - let user know about this
        output_str = "This question is not relevant for this application."
        output_json_list = json.dumps([output_str, df_html_str])
        return HttpResponse(output_json_list)
    else:
        output_str = "Your request did not go through."
        output_json_list = json.dumps([output_str, df_html_str])
        return HttpResponse(output_json_list)


    postlim_instructions_str = "Only return the pandas code one-liner - do NOT return any other text."

    final_user_question = prelim_instructions_str + user_question + postlim_instructions_str

    print("final_user_question = " + final_user_question)

    gpt_answer_str = call_gpt(final_user_question)
    print("gpt_answer_str = " + gpt_answer_str)

    #remove linebreaks from stdout added by GPT
    gpt_answer_str = gpt_answer_str.replace("\n","")
    gpt_answer_str = gpt_answer_str.strip()

    df_html_str_req = df_data.to_html(index=False)
    output_str = None


    #execute returned pandas code on df_data
    try:
        df_data = eval(gpt_answer_str)

        #if execution is successful, reassign the edited df_data back to the session variable
        request.session['df_data'] = df_data.to_json()

        #we need to encode the new df_data as a string that can be rendered in the web page
        df_html_str = df_data.to_html(index=False)

        output_str = "Pandas operation: " + gpt_answer_str + " has been executed successfully."


    except Exception as e:
        exception_str = repr(e)
        output_str = exception_str

    output_json_list = json.dumps([output_str, df_html_str])

    EasyQueryHistory.objects.using("xactly_dev").create(df_html_str_req=df_html_str_req, user_question=user_question, output_str=output_str, df_html_str_res=df_html_str, study_name=this_study_name)

    return HttpResponse(output_json_list)


@csrf_exempt
def export_data(request):
    
    #get the df_data session variable as a Dataframe object
    df_data_json = request.session['df_data']

    df_data = pd.read_json(df_data_json)

    csv_buffer = io.StringIO()
    df_data.to_csv(csv_buffer, index=False)

    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
        
    return response


@csrf_exempt
def answer_user_question_v1(request):

    user_question = request.POST['user_question']
    this_study_name = request.POST['this_study_name']
    
    #output_json_list = json.dumps(["This is a test!", user_question])
    
    #return HttpResponse(output_json_list)

    #get the df_data session variable as a Dataframe object
    df_data_json = request.session['df_data']

    df_data = pd.read_json(df_data_json)

    styled_df = custom_styling(df_data)

    #in case there is an error, do not change the data frame contents
    #df_html_str = df_data.to_html(index=False)
    df_html_str = styled_df.to_html()

    #user_question = "Make a 'sentiment' column that contains +, - or 0 values associated with each row in the 'latest_customer_tweet' column."
    #user_question = "Add column 'Revenue2'"

    #first, determine the query category
    gpt_category_str = call_gpt(prompt_strings.query_category_prelim_str + user_question).replace("\n","").replace(".","")
    
    #output_json_list = json.dumps(["This is a test!", user_question])
    
    #return HttpResponse(output_json_list)

    print("gpt_category_str = " + gpt_category_str)

    prelim_instructions_str = None
    imputation_values = {}

    if gpt_category_str == 'Delete column':
        prelim_instructions_str = prompt_strings.drop_column_prelim_str
    elif gpt_category_str == 'Add column':
        prelim_instructions_str = prompt_strings.add_column_prelim_str
    elif gpt_category_str == 'Update values':
        prelim_instructions_str = prompt_strings.update_values_prelim_str
    elif gpt_category_str == 'Add sentiment':
        prelim_instructions_str = prompt_strings.add_sentiment_column_prelim_str
    elif gpt_category_str == 'Rename column':
        prelim_instructions_str = prompt_strings.rename_column_prelim_str
    elif gpt_category_str == 'Change data type':
        prelim_instructions_str = prompt_strings.change_data_type_prelim_str
    elif gpt_category_str == 'Switch columns':
        prelim_instructions_str = prompt_strings.switch_columns_prelim_str
    elif "Delete rows" in gpt_category_str:
        prelim_instructions_str = prompt_strings.delete_rows_prelim_str
    elif "Translate column" in gpt_category_str:
        prelim_instructions_str = prompt_strings.translate_text_column_prelim_str
        translator = Translator()
    elif "Ordinal encoding" in gpt_category_str:
        prelim_instructions_str = prompt_strings.ordinal_encoding_prelim_str
    elif "One-hot encoding" in gpt_category_str:
        prelim_instructions_str = prompt_strings.one_hot_encoding_prelim_str
    elif "Key topics" in gpt_category_str:
        prelim_instructions_str = prompt_strings.key_topic_words_prelim_str
    elif "Semantic similarity" in gpt_category_str:
        prelim_instructions_str = prompt_strings.semantic_similarity_prelim_str
    elif "Drop duplicates" in gpt_category_str:
        prelim_instructions_str = prompt_strings.drop_duplicates_prelim_str
    elif "Impute values" in gpt_category_str:
        prelim_instructions_str = prompt_strings.impute_values_prelim_str
        
        imputation_values = {
            col: df_data[col].mean() if df_data[col].dtype == 'float64' else df_data[col].mode().iloc[0]
            for col in df_data.columns
        }
        
        print(imputation_values)
        
    elif gpt_category_str == "[]":

        #we have flagged an irrelevant/inappropriate question - let user know about this
        output_str = "This question is not relevant for this application."
        output_json_list = json.dumps([output_str, df_html_str])
        return HttpResponse(output_json_list)
    else:
        output_str = "Your request did not go through."
        output_json_list = json.dumps([output_str, df_html_str])
        return HttpResponse(output_json_list)


    postlim_instructions_str = "Only return the pandas code one-liner - do NOT return any other text."

    final_user_question = prelim_instructions_str + user_question + postlim_instructions_str

    print("final_user_question = " + final_user_question)

    gpt_answer_str = call_gpt(final_user_question)
    print("gpt_answer_str = " + gpt_answer_str)

    #remove linebreaks from stdout added by GPT
    gpt_answer_str = gpt_answer_str.replace("\n","")
    gpt_answer_str = gpt_answer_str.strip()

    df_html_str_req = df_data.to_html(index=False)
    output_str = None

    #execute returned pandas code on df_data
    try:
        df_data = eval(gpt_answer_str)

        #if execution is successful, reassign the edited df_data back to the session variable
        request.session['df_data'] = df_data.to_json()

        styled_df = custom_styling(df_data)

        #we need to encode the new df_data as a string that can be rendered in the web page
        df_html_str = styled_df.to_html()

        output_str = "Pandas operation: " + gpt_answer_str + " has been executed successfully."


    except Exception as e:
        exception_str = repr(e)
        output_str = exception_str

    output_json_list = json.dumps([output_str, df_html_str])

    EasyQueryHistory.objects.using("xactly_dev").create(df_html_str_req=df_html_str_req, user_question=user_question, output_str=output_str, df_html_str_res=df_html_str, study_name=this_study_name)

    return HttpResponse(output_json_list)


def history_list(request):
    response = {}
    content_data = []
    history_data = list(EasyQueryHistory.objects.all())
    for his in history_data:
        content = {}
        content["id"] = his.id
        content["value"] = his.user_question
        # print(content)
        content_data.append(content)
        # print(content.items())
    # print(content_data)
    return JsonResponse(content_data, safe=False)


def history_detail(request, pk):
    content = {}
    history_data = EasyQueryHistory.objects.get(pk=pk)
    content["id"] = history_data.id
    content["user_question"] = history_data.user_question
    content["output_str"] = history_data.output_str
    content["df_html_str_res"] = history_data.df_html_str_res
    content["df_html_str_req"] = history_data.df_html_str_req
    content["this_study_name"] = history_data.study_name
    print(history_data)
    print(content)
    return JsonResponse(content)
