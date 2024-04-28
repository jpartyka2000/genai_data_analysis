# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 21:07:38 2014

@author: ldavis1
"""


'''
TODO

Change database to allow uuid for hcm, add study_date to study_info_table
Change database less_than_five_days to less_than_min_days (new form allows for variable number of minimum)
Add personal identifying information to master_list
Add personal identitying information to database as a table called personal_info
Add location "name" or "number" to store code or location from original data
Ask about adding pma_minutes to database
Remove hiring_term from database -- going to consolidate full/part/temp/seasonal into working_schedule

'''
import logging, os
import csv
import datetime
import time
import uuid
import chardet
import re
from collections import Counter

from django.conf import settings
from satool.databaseloader import DatabaseLoaderClass
from django.core.files.storage import FileSystemStorage #, File
from django.conf import settings

class AggToolClass():

    def __init__(self, study_name='test', analyst_name='None', log_file=False, debug=False):
        self.__version__ = '0.1'
        self.debug = debug
        media_url = settings.MEDIA_ROOT
        #fh = file(media_url+'aggtool.log', 'w')
        #fh.close();


        #if log_file:
        #    if self.debug:
        #        logging.basicConfig(filename= media_url+'aggtool.log' ,level=logging.DEBUG)
        #    else:
        #        logging.basicConfig(filename= media_url+'aggtool.log',level=logging.WARNING)

        #database connection
        self.database_loader = DatabaseLoaderClass()

        #The column headers from the input csv data (or file) 
        self.header_row_from_input = []
        self.csv_data = []
        
        #The dictionary of values from all the web forms combined
        self.form_dict = {} 

        #regular expression to exclude blank rows from being inserted into csv_data and ca_spreadsheet_rows table
        self.blank_row_regex = re.compile('^(,)+$')

        #the indices of the termination reason, position name, and location headers in the list
        #the list is self.header_row_from_input
        self.term_index = int()
        self.position_index = int()
        self.location_info_1_index = int()
        self.location_info_2_index = int()
        self.location_info_3_index = int()
        self.location_info_4_index = int()

        #lists of term reasons, positions, and locations
        self.client_term_reason_list = []
        self.unique_position_list = []
        self.unique_location_list = []

        #dicts containing the frequency of the occurences in the lists
        self.client_term_reason_frequencies = [] 
        self.unique_position_frequencies = []
        self.unique_location_frequencies = []
        
        '''
        Mappings of the variable match fields, term reasons, profiles, 
        locations, and study data from the respective forms
        '''
        #self.data_entry_map = {}

        #mapping of the csv headers to the variables from the web form
        self.variable_matching_map = {}

        #mapping of the termination reasons to the classifications from the web form
        self.term_classification_map = {}

        #mapping of the positions to profiles from the web form
        self.position_to_profile_map = {}

        #mapping of the locations from the web form
        self.location_classification_map = {}

        #the list of the database column names
        self.database_columns_list = self.create_database_columns_list()

        #the destination row for the aggregation
        self.processed_row = ['',]*len(self.database_columns_list)

        #mapping of keys to index locations for the data
        self.header_index_map = {}

        #the analyst that processed the study data
        self.analyst_name = analyst_name

        #the name of the company that the study is being processed for
        self.client_name = str()

        #the list of all possible clients from the PA_IO data
        #self.all_clients = self.database_loader.get_all_clients()

        #the list of all profiles associated with a specific client
        self.client_profiles = []

        if study_name == 'test':
            #self.study_file_name = 'test_' + str(datetime.datetime.now().microsecond) + '.csv'
            self.study_file_name = 'satool/test_output.csv'
        else:
            self.study_file_name = study_name + '.csv'

        #file system for storing files
        if os.path.isdir(settings.MEDIA_ROOT+"satool/"):
            pass
        else:
            pass
            #os.mkdir(settings.MEDIA_ROOT+"satool/")

        self.fs = FileSystemStorage(location=settings.MEDIA_ROOT + 'satool/')

    def get_csv_data(self):
        return self.csv_data

    def get_column_headers(self):
        return self.header_row_from_input 

    def get_term_frequency(self):
        return self.client_term_reason_frequencies

    def get_position_frequency(self):
        return self.unique_position_frequencies

    def get_location_frequency(self):
        return self.unique_location_frequencies

    def get_database_columns_list(self):
        return self.database_columns_list

    def get_all_clients(self):
        return self.all_clients

    def get_client_name(self):
        return self.client_name

    def get_client_profiles(self):
        return self.client_profiles

    def get_client_id(self):
        return self.database_loader.get_client_id(self.client_name)

    def get_database_column_index(self, key):
        if key in self.database_columns_list:
            return self.database_columns_list.index(key)
        else:
            logging.warning('key: %s from form is not in the header reference list' % key)
            return None

    '''
    def set_data_entry_map(self, data_entry_from_form):
        self.data_entry_map = data_entry_from_form
    '''
    
    def set_csv_data(self, csv_data):
        self.csv_data = csv_data
        
    def set_column_headers(self, headers):    
        self.header_row_from_input = headers

    def set_variable_matching_map(self, form_field_matches):
        self.variable_matching_map = form_field_matches 
        
    def get_variable_matching_map(self):
        return self.variable_matching_map    

    def set_term_classification_map(self, term_classification_from_form):
        self.term_classification_map = term_classification_from_form

    def set_position_to_profile_map(self, positions_and_profiles_from_form):
        self.position_to_profile_map = positions_and_profiles_from_form

    def set_location_classification_map(self, location_classification_from_form):
        self.location_classification_map = location_classification_from_form

    def set_client_name(self, company_name):
        self.client_name = company_name

    def set_client_profiles(self):
        if self.variable_matching_map:
            self.client_profiles = self.database_loader.get_client_profiles(self.client_name)
        else:
            raise Exception('Variable Map not set')

    def set_form_dictionary(self, form_dict):
        '''
        Set the dictionary of values from all the web forms
        NOTE: This must be done after all the input forms are processed
        '''
        self.form_dict = form_dict

    def reset_processed_row(self):
        self.processed_row = ['',]*len(self.database_columns_list)


    def get_csv_data_from_db2(self, spreadsheet_id, usage):

       chunk_list = []
       csv_data = []

       if usage == 1:

           idx = 0

           for idx, one_matching_spreadsheet_row in enumerate(MatchingSpreadsheetRows.objects.using("pa_io").filter(spreadsheet_id=spreadsheet_id).order_by('matching_spreadsheet_row_id')):

               if idx == 0:
                   one_row_string = one_matching_spreadsheet_row.row.encode("ascii","ignore")
                   header_list = one_row_string.split(",")
                   continue

               one_row_string = one_matching_spreadsheet_row.row.encode("ascii","ignore")
               one_row_list = one_row_string.split(",")
               chunk_list.append(one_row_list)

               if idx % 1000 == 0:
                   csv_data += chunk_list
                   del chunk_list[:]

       else:

           idx = 0

           for idx, one_ca_spreadsheet_row in enumerate(CaSpreadsheetRows.objects.using("pa_io").filter(spreadsheet_id=spreadsheet_id).order_by('ca_spreadsheet_row_id')):

               if idx == 0:
                   one_row_string = one_ca_spreadsheet_row.row.encode("ascii","ignore")
                   header_list = one_row_string.split(",")
                   continue

               one_row_string = one_ca_spreadsheet_row.row.encode("ascii","ignore")
               one_row_list = one_row_string.split(",")
               chunk_list.append(one_row_list)

               if idx % 1000 == 0:
                   csv_data += chunk_list
                   del chunk_list[:]

       if idx == 0:
        
           #query the spreadsheets table and get the data field. If it is not empty, then this spreadsheet needs to be accessed using
           #the old way
           csv_data = self.get_csv_data_from_db(spreadsheet_id)
       else:
           #get remainder of last chunk
           csv_data += chunk_list

           #assign header_str and csv_data to their corresponding aggtool fields
           self.set_column_headers(header_list)
           self.set_csv_data(csv_data) 

       return csv_data 


    def get_csv_data_from_db(self, spreadsheet_id):
    
       #retrieve data associated with a given spreadsheet_id
       select_sql = """SELECT data, encoding_method FROM Spreadsheets WHERE spreadsheet_id=%s;""" % (spreadsheet_id) 

       spreadsheet_result = self.database_loader.select_spreadsheet_data(select_sql)
    
       csv_data = spreadsheet_result[0][0]
       encoding_method = spreadsheet_result[0][1]
    
       #encode from unicode to str
       csv_data = csv_data.encode(encoding_method)
       
       #next, we split the data using newlines as a delimiter
       csv_data_list = csv_data.split('\n')
       
       #get the data 
       row_string_list = [onerowstr for index, onerowstr in enumerate(csv_data_list) if index > 0]
       
       #for each element of data_list, split it by \t, since adjacent cells are separated by tabs
       csv_data = [one_row_string.split('\t') for one_row_string in row_string_list]
       
       #get the header
       header_str = csv_data_list[0]
       
       #turn header into a list of strings
       header_list = header_str.split('\t')
       
       #assign header_str and csv_data to their corresponding aggtool fields
       self.set_column_headers(header_list)
       self.set_csv_data(csv_data) 
       
       return csv_data 


    def get_row_number(self):
       return len(self.csv_data)


    def insert_csv_data_into_db2(self, request, usage=1):

       #get the headers and data as a single string, where each row is separated by a newline character
       csv_headers = self.get_column_headers()
       csv_data = self.get_csv_data()
       header_str = ",".join(csv_headers)

       #detect character encoding of csv data
       encoding = chardet.detect(header_str)

       encoding_method = encoding['encoding']

       #next, retrieve other parameters for the insert query
       #add a new row into the Spreadsheets table

       try:
           spreadsheet_id = int(Spreadsheets.objects.using("pa_io").latest('spreadsheet_id').spreadsheet_id) + 1
       except Exception:
           return -1

       user_id = request.session['user_id']    
       #spreadsheet_date = time.strftime("%b %d, %Y, %I:%M %p")
       created_date = time.strftime("%Y-%m-%d").encode("ascii", "ignore") 
       match_name = request.POST['study_name']

       #if the match name has apostrophes, be sure to escape them
       match_name = match_name.replace("'","''")

       company_id = request.session['company_id']
       Spreadsheets.objects.using('pa_io').create(spreadsheet_id=spreadsheet_id, user_id=user_id, company_id=company_id,
                                                  spreadsheet_name=match_name,usage=usage,data="",share_type=2,created_by=user_id,
                                                  created_date=created_date,last_updated_by=user_id,last_updated_date=created_date,
                                                  encoding_method=encoding_method)

       #next, insert spreadsheet data into matching_spreadsheet_rows table
       header_str = ",".join(csv_headers)

       if usage == 1:

           try:
               start_id = int(MatchingSpreadsheetRows.objects.using("pa_io").latest('matching_spreadsheet_row_id').matching_spreadsheet_row_id) + 1
           except Exception:
               start_id = 1

           MatchingSpreadsheetRows.objects.using("pa_io").create(matching_spreadsheet_row_id=start_id,row=header_str,spreadsheet_id=spreadsheet_id)
           start_id += 1

       else:
           try:
               start_id = int(CaSpreadsheetRows.objects.using("pa_io").latest('ca_spreadsheet_row_id').ca_spreadsheet_row_id) + 1
           except Exception:
               start_id = 1

           CaSpreadsheetRows.objects.using("pa_io").create(ca_spreadsheet_row_id=start_id,row=header_str,spreadsheet_id=spreadsheet_id)
           start_id += 1

       matching_spreadsheets_rows_obj_list = []
       ca_spreadsheets_rows_obj_list = []

       for idx, onerow in enumerate(csv_data):

           comma = ''
           try:
              one_row_str = ''

              for oneitem in onerow:
                  oneitem = oneitem.encode('ascii','ignore')
                  one_row_str += comma + oneitem
                  comma = ','
           except Exception:
               one_row_str += comma + "____"

           #if this row is full of commas, then we have a blank row. Skip and go to next row
           if self.blank_row_regex.match(one_row_str):
               continue

           if usage == 1:
               this_rows_obj = MatchingSpreadsheetRows(matching_spreadsheet_row_id=start_id,
                                                            row=one_row_str,
                                                            spreadsheet_id=spreadsheet_id)
    
               matching_spreadsheets_rows_obj_list.append(this_rows_obj)
           
               if len(matching_spreadsheets_rows_obj_list) == 300:
                   MatchingSpreadsheetRows.objects.using("pa_io").bulk_create(matching_spreadsheets_rows_obj_list, 300)
                   del matching_spreadsheets_rows_obj_list[:] 
           
           else:
               
               this_rows_obj = CaSpreadsheetRows(ca_spreadsheet_row_id=start_id,
                                                            row=one_row_str,
                                                            spreadsheet_id=spreadsheet_id)

               ca_spreadsheets_rows_obj_list.append(this_rows_obj)

               if len(ca_spreadsheets_rows_obj_list) == 300:
                   CaSpreadsheetRows.objects.using("pa_io").bulk_create(ca_spreadsheets_rows_obj_list, 300)
                   del ca_spreadsheets_rows_obj_list[:] 

           start_id += 1

       if usage == 1:
           MatchingSpreadsheetRows.objects.using("pa_io").bulk_create(matching_spreadsheets_rows_obj_list, 300)
       else:
           CaSpreadsheetRows.objects.using("pa_io").bulk_create(ca_spreadsheets_rows_obj_list, 300)

       return spreadsheet_id 


    def insert_csv_data_into_db(self, request, usage=1):
      
       #get the headers and data as a single string, where each row is separated by a newline character
       csv_headers = self.get_column_headers()
       csv_data = self.get_csv_data()
    
       headers_formatted = '\t'.join(csv_headers)
    
       data_flattened = ['\t'.join(onerow) for onerow in csv_data]
       data_formatted = '\n'.join(data_flattened)
       final_data = headers_formatted + '\n' + data_formatted
       final_data = final_data.replace("\'", "\'\'")
    
       #detect character encoding of csv data
       encoding = chardet.detect(final_data)
       
       encoding_method = encoding['encoding']
       #encoding_confidence = encoding['confidence']      
    
       final_data = final_data.decode(encoding_method)
       
       #next, retrieve other parameters for the insert query
       #add a new row into the Spreadsheets table
       #to get the spreadsheet id, get the max number of rows and add 1
       spreadsheet_id_sql = """SELECT MAX(spreadsheet_id) from Spreadsheets;"""
    
       result_list = self.database_loader.select_query(spreadsheet_id_sql)
       spreadsheet_id = int(result_list[0][0]) + 1 
        
       user_id = request.session['user_id']    
       spreadsheet_date = time.strftime("%b %d, %Y, %I:%M %p") 
       match_name = request.POST['study_name']
       
       #if the match name has apostrophes, be sure to escape them
       match_name = match_name.replace("'","''")
       
       company_id = request.session['company_id']
       
       
       value_tuple = (spreadsheet_id, user_id, company_id, match_name, usage, final_data, 2, user_id, spreadsheet_date, user_id, spreadsheet_date, encoding_method)
    
       spreadsheet_sql = """INSERT INTO spreadsheets(
            spreadsheet_id, user_id, company_id, spreadsheet_name, usage, 
            data, share_type, created_by, created_date, last_updated_by, 
            last_updated_date, encoding_method)
       VALUES (%s, %s, %s, '%s', %s, '%s', %s, %s, '%s', %s, '%s', '%s');""" % value_tuple
       
       self.database_loader.dml_query(spreadsheet_sql)
       return spreadsheet_id 

    def create_database_columns_list(self):
        '''
        The database tables used are:
        identifying_info
        demographic_info
        employment_info
        pa_assessment_info
        removal_reasons
        study_info
        analyst_info

        Please see the schema for more information on the tables.

        Based on these tables, make the master list of database fields.
        If the database tables change, these fields must be updated.
        
        Steps:
        1. make a string listing the fields in each table
        2. convert the database field strings into lists
        3. concatenate the lists, removing duplicates
        '''

        #define the fields used in the database tables 
        identifying_info_table_fields = 'hcm_id, study_id, employee_id, client_id, client_name, position_name, work_schedule, hiring_term, job_level, position_type, industry, zip_code, city, state, census_subregion, census_region, country, location_class_1, location_class_2, location_class_3, location_class_4'
                
        demographic_info_table_fields = 'hcm_id, study_id, ethnicity, birth_year, postal_code, gender, language, age_at_hire'

        employment_info_table_fields = 'hcm_id, study_id, orig_hire_date, date_in_position, rehire_date, orig_term_date, orig_term_reason, term_class_scheme, predeploy_start, predeploy_end, postdeploy_start, postdeploy_end, hire_pre_or_post, term_pre, days_employed, term_category, terminated, final_date'

        pa_assessment_info_table_fields = 'hcm_id, study_id, profile_name, profile_id, pa_id, matched_how, complete, click_through, click_through_flagged, consistency, consistency_flagged, falsification, falsification_flagged, lcs_length, lcs_length_flagged, ppi_minutes, ppi_minutes_flagged, ppi_total_item_minutes, ppi_total_item_minutes_flagged, sequence, sequence_flagged, num_qc_flags, pma_in_profile, tests_taken, ppi_1, ppi_2, gzdf, pma, earliest_test_completion, latest_test_completion, earliest_assessment_completion, latest_assessment_completion, fit_score, rec_cat, rec_vs_rq_minus, rq_plus, rr_plus, a_na, verbal, numerical, mental'

        removal_reasons_table_fields = 'hcm_id, study_id, duplicate, pre_pre, missing_original_hire_date, td_before_ohd, dip_before_ohd, exit_date_no_reason, exit_reason_no_date, future_hire_date, future_term_date, positions_not_profiled, best_practice_profile, data_not_in_study_period, neither_term_reason, incomplete_assessment_post, post_assessed_after_hire, negative_days, less_than_min_days, post_prof_creat, location_closed, rehires, change_position, max_removals, final_term'

        study_info_table_fields = 'study_id, analyst_id, dataset_name, project_results' 

        analyst_info_table_fields = 'analyst_id, analyst_name'

        #convert to lists, remove duplicates, and append to master list
        master_list = []
        identifying_info_list = identifying_info_table_fields.split(', ')
        master_list += identifying_info_list

        demographic_info_list = demographic_info_table_fields.split(', ')
        demographic_headers = [value for value in demographic_info_list if value not in master_list]
        master_list += demographic_headers

        employment_info_list = employment_info_table_fields.split(', ')
        employment_headers = [value for value in employment_info_list if value not in master_list]
        master_list += employment_headers

        pa_assessment_info_list = pa_assessment_info_table_fields.split(', ')
        pa_assessment_headers = [value for value in pa_assessment_info_list if value not in master_list]
        master_list += pa_assessment_headers

        removal_reasons_list = removal_reasons_table_fields.split(', ')
        removal_reasons_headers = [value for value in removal_reasons_list if value not in master_list]
        master_list += removal_reasons_headers

        study_info_list = study_info_table_fields.split(', ')
        study_headers = [value for value in study_info_list if value not in master_list]
        master_list += study_headers

        analyst_info_list = analyst_info_table_fields.split(', ')
        analyst_headers = [value for value in analyst_info_list if value not in master_list]
        master_list += analyst_headers

        return master_list


    def compute_term_position_location_frequency(self):
        '''
        Count the different termination reasons, position names, and locations
        so that we know the frequency of each and can return it to the html form
        '''

        #find the column index associated with each field name
        for key, value in self.variable_matching_map.iteritems():
            if key == 'orig_term_reason':  #name of the field that stores termination reason
                self.term_index = self.header_row_from_input.index(value.encode('utf-8'))
            elif key == 'position_name':  #name of the field that stores the name of the position 
                try:
                    #self.position_index = self.header_row_from_input.index(value.encode('utf-8'))
                    #self.position_index = self.header_row_from_input.index(value)
                    self.position_index = 7
                    logging.warning('position_name')
                    logging.warning(value)
                except:
                    logging.warning('header row from position_name exception')
                    logging.warning(self.header_row_from_input)
                    raise Exception(value)
            elif key == 'location_info_1':  #name of the form field that stores the location 
                self.location_info_1_index = self.header_row_from_input.index(value.encode('utf-8'))
            elif key == 'location_info_2':  
                self.location_info_2_index = self.header_row_from_input.index(value.encode('utf-8'))
            elif key == 'location_info_3':  
                self.location_info_3_index = self.header_row_from_input.index(value.encode('utf-8'))
            elif key == 'location_info_4': 
                self.location_info_4_index = self.header_row_from_input.index(value.encode('utf-8'))

        #add each occurence in the row to the overall list, removing extra whitespace at the end
        for row in self.csv_data:
            if row[self.term_index] == '':
                self.client_term_reason_list.append('None')
            else:
                self.client_term_reason_list.append(row[self.term_index].rstrip())
            if row[self.position_index] == '':
                self.unique_position_list.append('None')
            else:
                self.unique_position_list.append(row[self.position_index].rstrip())
            if row[self.location_info_1_index] == '':
                self.unique_location_list.append('None')
            else:
                self.unique_location_list.append(row[self.location_info_1_index].rstrip())


        #use a Counter object to get the frequencies
        client_term_reason_dict = dict(Counter(self.client_term_reason_list))
        unique_position_dict = dict(Counter(self.unique_position_list))
        unique_location_dict = dict(Counter(self.unique_location_list))
            
        #format the counters
        self.client_term_reason_frequencies = [{'reason': key, 'count': value} for key, value in client_term_reason_dict.iteritems()]
        self.unique_position_frequencies = [{'unique_position': key, 'count': value} for key, value in unique_position_dict.iteritems()]
        self.unique_location_frequencies = [{'unique_location': key, 'count': value} for key, value in unique_location_dict.iteritems()]

    '''
    The full header list

    ['hcm_id', 'study_id', 'employee_id', 'client_id', 'client_name', 'position_name', 'work_schedule', 'hiring_term', 'job_level', 'position_type', 'industry', 'zip_code', 'city', 'state', 'census_subregion', 'census_region', 'country', 'location_class_1', 'location_class_2', 'location_class_3', 'location_class_4', 'ethnicity', 'birth_year', 'postal_code', 'gender', 'language', 'age_at_hire', 'orig_hire_date', 'date_in_position', 'rehire_date', 'orig_term_date', 'orig_term_reason', 'term_class_scheme', 'predeploy_start', 'predeploy_end', 'postdeploy_start', 'postdeploy_end', 'hire_pre_or_post', 'term_pre', 'days_employed', 'term_category', 'terminated', 'final_date', 'profile_name', 'profile_id', 'pa_id', 'matched_how', 'complete', 'click_through', 'click_through_flagged', 'consistency', 'consistency_flagged', 'falsification', 'falsification_flagged', 'lcs_length', 'lcs_length_flagged', 'ppi_minutes', 'ppi_minutes_flagged', 'ppi_total_item_minutes', 'ppi_total_item_minutes_flagged', 'sequence', 'sequence_flagged', 'num_qc_flags', 'pma_in_profile', 'tests_taken', 'ppi_1', 'ppi_2', 'gzdf', 'pma', 'earliest_test_completion', 'latest_test_completion', 'earliest_assessment_completion', 'latest_assessment_completion', 'fit_score', 'rec_cat', 'rec_vs_rq_minus', 'rq_plus', 'rr_plus', 'a_na', 'verbal', 'numerical', 'mental', 'duplicate', 'pre_pre', 'missing_original_hire_date', 'td_before_ohd', 'dip_before_ohd', 'exit_date_no_reason', 'exit_reason_no_date', 'future_hire_date', 'future_term_date', 'positions_not_profiled', 'best_practice_profile', 'data_not_in_study_period', 'neither_term_reason', 'incomplete_assessment_post', 'post_assessed_after_hire', 'negative_days', 'less_than_min_days', 'post_prof_creat', 'location_closed', 'rehires', 'change_position', 'max_removals', 'final_term', 'analyst_id', 'dataset_name', 'project_results', 'analyst_name']
    '''

    def map_form_keys_to_indices(self):
        '''
        Map the keys from the form fields to indexes within
        the processed row that will be written to the database

        NOTE: The processed row must be the same length as the
        number of columns
        '''

        for index, key in enumerate(self.database_columns_list):
            self.header_index_map[key] = index


    def read_text_area_data(self, text_area_data):

        header_list = []
        self.csv_data = []

        text_area_row_list = text_area_data.split('\r\n')

        #parse rows in text area, add to csv_data, and insert into MatchingSpreadsheetRows
        for idx, one_row_str in enumerate(text_area_row_list):

            if idx == 0:
                one_row_str = one_row_str.encode("ascii","ignore")
                header_list = one_row_str.split('\t')
                continue

            one_row_str = one_row_str.encode("ascii","ignore")
            self.csv_data.append(one_row_str.split('\t'))

        self.header_row_from_input = header_list


    def read_spreadsheet_data(self, spreadsheet_id):

        #clear self.csv_data value from previous uploads before we start reading
        self.csv_data = []

        chunk_list = []
        header_list = []

        for idx, one_ca_spreadsheet_row in enumerate(CaSpreadsheetRows.objects.using("pa_io").filter(spreadsheet_id=spreadsheet_id).order_by('ca_spreadsheet_row_id')):

            if idx == 0:
                one_row_string = one_ca_spreadsheet_row.row.encode("ascii","ignore")
                header_list = one_row_string.split(",")
                continue

            one_row_string = one_ca_spreadsheet_row.row.encode("ascii","ignore")
            one_row_list = one_row_string.split(",")
            chunk_list.append(one_row_list)

            if idx % 1000 == 0:
                self.csv_data += chunk_list
                del chunk_list[:]

        #get remainder of last chunk
        self.csv_data += chunk_list
        self.header_row_from_input = header_list


    def read_csv_data_from_file(self, filename):
        
        filename = str(filename)
    
        #clear self.csv_data value from previous uploads before we start reading
        self.csv_data = []

        try:
            file_path = self.fs.path(filename)
        except NotImplementedError:
            logging.error(filename + ' was not found for reading')
            raise Exception('File not found for reading')

        with open(file_path, 'r') as file_handle:
            file_reader = csv.reader(file_handle)
            count = 0
            for row in file_reader:
                if count == 0:
                    count = 1
                    self.header_row_from_input = row
                else:
                    if row:
                        #if row is a blank row, then skip it
                        if row.count('') == len(row):
                            continue
                        else:
                            self.csv_data.append(row)

    def find_form_field_end_number(self, field_name):
        '''
        Fields that are autogenerated by the form have a number appended at the end
        i.e. position_type_2
        This function returns the "2"
        '''

        #find the last underscore and get everything after it.
        #this is the number
        index = field_name.rfind('_')
        end_number = field_name[index + 1:]
        return end_number

    def process_csv_data(self):
        '''
        Process the csv data based upon the input from
        the web forms.  Write the processed data to a file.

        Steps:
        1. process match variables
        2. classify terminations, profiles, and locations
        3. Process removals
        4. Write to file

        NOTE: the set_form_dictionary method must be called BEFORE
        this method
        '''

        #return nothing if the values from the forms are not set before calling the
        #process_csv method
        if not self.form_dict:
            logging.error('Must set the form_dict attribute using the set_form_dictionary method prior to processing the csv data')
            if self.debug:
                raise Exception('Must set the form_dict before processing the csv data')
            else:
                return

        #output_file = open(self.study_file_name, 'wb')
        output_file = open('/var/www/django/media/satool/test_output.csv', 'wb')
        file_writer = csv.writer(output_file)
        file_writer.writerow(self.database_columns_list)

        variable_matching_map_keys = self.variable_matching_map.keys()
        variable_matching_map_values = self.variable_matching_map.values()

        #map the keys from the form dictionary to indices in the processed row
        self.map_form_keys_to_indices()

        for row in self.csv_data:
            if row:
                self.reset_processed_row()

                #add a uuid for the hcm_id
                self.processed_row[0] = str(uuid.uuid4())

                #add client id
                #self.processed_row[3] = self.form_dict['client_id']
                self.processed_row[3] = self.get_client_id()
                self.processed_row[4] = self.get_client_name()

                #add study id
                self.processed_row[1] = self.database_loader.create_study_id(study_date=self.form_dict['study_date'], company_name=self.form_dict['client_name'])

                #process rows from the csv file
                #
                #Get the values from the csv data and put them in the proper
                #location in the row for entry into the "big data" tables

                for index, row_value in enumerate(row):

                    #set the termination category value
                    #using the termination reason
                    if index == self.term_index:    #termination reason index
                        for key, dict_value in self.term_classification_map.iteritems():
                            if row_value == dict_value.encode('utf-8'):     #The term reason from the csv data matches the term reason in the form data
                                #get the last value of the key -- it has the "number of the term reason"
                                reason_number = self.find_form_field_end_number(key)

                                #set the term cateory
                                processed_list_index = self.header_index_map['term_category']
                                term_class_key = 'term_category_' + reason_number 
                                self.processed_row[processed_list_index] = self.term_classification_map[term_class_key]

                                #set the term reason
                                processed_list_index = self.header_index_map['orig_term_reason']
                                term_class_key = 'term_reason_' + reason_number 
                                self.processed_row[processed_list_index] = self.term_classification_map[term_class_key]

                                break

                    #set the position; set the profile name, job level, and position type based on the position
                    elif index == self.position_index:
                        for key, dict_value in self.position_to_profile_map.iteritems():
                            if row_value == dict_value.encode('utf-8'):     #The position from the csv data matches the position in the form data

                                position_number = self.find_form_field_end_number(key)

                                processed_list_index = self.header_index_map['position_name']
                                position_key = 'position_' + position_number 
                                self.processed_row[processed_list_index] = self.position_to_profile_map[position_key]

                                processed_list_index = self.header_index_map['profile_name']
                                position_key = 'profile_' + position_number 
                                self.processed_row[processed_list_index] = self.position_to_profile_map[position_key]

                                processed_list_index = self.header_index_map['job_level']
                                position_key = 'job_level_' + position_number 
                                self.processed_row[processed_list_index] = self.position_to_profile_map[position_key]

                                processed_list_index = self.header_index_map['position_type']
                                position_key = 'position_type_' + position_number 
                                self.processed_row[processed_list_index] = self.position_to_profile_map[position_key]

                                break


                    #set the location classifications
                    elif index == self.location_info_1_index:
                        for key, dict_value in self.location_classification_map.iteritems():
                            if row_value == dict_value.encode('utf-8'):     #The location from the csv data matches the location in the form data

                                location_number = self.find_form_field_end_number(key)

                                processed_list_index = self.header_index_map['location_class_1']
                                location_key = 'location_class_1_' + location_number 
                                self.processed_row[processed_list_index] = self.location_classification_map[location_key]

                                processed_list_index = self.header_index_map['location_class_2']
                                location_key = 'location_class_2_' + location_number 
                                self.processed_row[processed_list_index] = self.location_classification_map[location_key]

                                processed_list_index = self.header_index_map['location_class_3']
                                location_key = 'location_class_3_' + location_number 
                                self.processed_row[processed_list_index] = self.location_classification_map[location_key]

                                processed_list_index = self.header_index_map['location_class_4']
                                location_key = 'location_class_4_' + location_number 
                                self.processed_row[processed_list_index] = self.location_classification_map[location_key]



                    else:
                        #copy the rest of the values from the csv data to the processed row
                        header_value = self.header_row_from_input[index] 

                        try:
                            #if header_value in variable_key_list:
                            #if header_value in variable_matching_map_keys:
                            if header_value in variable_matching_map_values:
                                #processed_key = self.variable_matching_map[header_value]
                                processed_key = variable_matching_map_keys[variable_matching_map_values.index(header_value)]

                                if processed_key in self.database_columns_list:
                                    processed_list_index = self.header_index_map[processed_key]
                                    self.processed_row[processed_list_index] = row_value

                        except ValueError:
                            continue


                #### Process removal logic ###

                #1. Classification Check

                study_periods_to_check = []

                if self.form_dict['study_period_link_1'] == 'Profile' or self.form_dict['study_period_link_1'] == 'Location':
                    study_periods_to_check.append('1')
                elif self.form_dict['study_period_link_2'] == 'Profile' or self.form_dict['study_period_link_2'] == 'Location':
                    study_periods_to_check.append('2')
                elif self.form_dict['study_period_link_3'] == 'Profile' or self.form_dict['study_period_link_3'] == 'Location':
                    study_periods_to_check.append('3')
                elif self.form_dict['study_period_link_4'] == 'Profile' or self.form_dict['study_period_link_4'] == 'Location':
                    study_periods_to_check.append('4')
                else:
                    logging.error('No study period set')
                    if self.debug:
                        raise Exception('No study period selected')
                    else:
                        return
                        
                #2.  Period Check:
                
                hire_index = self.header_index_map['orig_hire_date']

                '''
                Values from the form dictionary are pure dates.  Thus, we must
                use a datetime structure to get the date from the format, but
                strip time component
                '''
                hire_value = datetime.datetime.strptime(self.processed_row[hire_index], '%m/%d/%Y').date()


                removal_index = self.header_index_map['data_not_in_study_period']

                for period in study_periods_to_check:
                    start_key_value = 'study_period_start_' + period
                    end_key_value = 'study_period_end_' + period

                    if self.form_dict[start_key_value] <= hire_value <= self.form_dict[end_key_value]:
                        self.processed_row[removal_index] = 0
                    else:
                        self.processed_row[removal_index] = 1
                        break

                #3.  Missing original hire_date

                hire_index = self.header_index_map['orig_hire_date']
                hire_value = self.processed_row[hire_index]

                removal_index = self.header_index_map['missing_original_hire_date']

                if not hire_value:
                    self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0
                

                #4.  Term before Hire

                hire_index = self.header_index_map['orig_hire_date']
                term_index = self.header_index_map['orig_term_date']
                hire_value = self.processed_row[hire_index]
                term_value = self.processed_row[term_index]

                removal_index = self.header_index_map['td_before_ohd']
                
                if term_value == '':
                    self.processed_row[removal_index] = 0
                else:
                    #Make sure the comparison is between date objects (no time needed)
                    if datetime.datetime.strptime(term_value, '%m/%d/%Y').date() < datetime.datetime.strptime(hire_value, '%m/%d/%Y').date():
                        self.processed_row[removal_index] = 1
                    else:
                        self.processed_row[removal_index] = 0
                

                #5.  In position before hire

                hire_index = self.header_index_map['orig_hire_date']
                date_index = self.header_index_map['date_in_position']
                hire_value = self.processed_row[hire_index]
                date_value = self.processed_row[date_index]

                removal_index = self.header_index_map['dip_before_ohd']

                if date_value == '':
                    self.processed_row[removal_index] = 0
                else:
                    if datetime.datetime.strptime(date_value, '%m/%d/%Y').date() < datetime.datetime.strptime(hire_value, '%m/%d/%Y').date():
                        self.processed_row[removal_index] = 1
                    else:
                        self.processed_row[removal_index] = 0

                #6.  Exit date no exit reason

                date_index = self.header_index_map['orig_term_date']
                reason_index = self.header_index_map['orig_term_reason']
                date_value = self.processed_row[date_index]
                reason_value = self.processed_row[reason_index]

                removal_index = self.header_index_map['exit_date_no_reason']
                
                # term date is not none and term reason is none
                if date_value and not reason_value:
                    self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0


                #7.  Exit reason no exit date

                date_index = self.header_index_map['orig_term_date']
                reason_index = self.header_index_map['orig_term_reason']
                date_value = self.processed_row[date_index]
                reason_value = self.processed_row[reason_index]

                removal_index = self.header_index_map['exit_reason_no_date']


                # term reason is not none and date is none, flag it
                if reason_value:
                    if date_value:
                        self.processed_row[removal_index] = 0
                    else:
                        self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0


                #8.  Future term date

                term_index = self.header_index_map['orig_term_date']
                orig_hire_index = self.header_index_map['orig_hire_date']
                rehire_index = self.header_index_map['rehire_date']
                term_value = self.processed_row[term_index]
                orig_hire_value = self.processed_row[orig_hire_index]
                rehire_value = self.processed_row[rehire_index]

                removal_index = self.header_index_map['future_term_date']

                #find the max hire date
                if not rehire_value:
                    max_value = orig_hire_value
                else:
                    if datetime.datetime.strptime(orig_hire_value, '%m/%d/%Y').date() < datetime.datetime.strptime(rehire_value, '%m/%d/%Y').date():
                        max_value = rehire_value
                    else:
                        max_value = orig_hire_value

                #if term_value == '':
                if not term_value:
                    self.processed_row[removal_index] = 0
                else:
                    if datetime.datetime.strptime(max_value, '%m/%d/%Y').date() < datetime.datetime.strptime(term_value, '%m/%d/%Y').date():
                        self.processed_row[removal_index] = 1
                    else:
                        self.processed_row[removal_index] = 0
                        
                #9.  Positions not profiled

                profile_index = self.header_index_map['profile_name']
                profile_value = self.processed_row[profile_index]
                type_index = self.header_index_map['position_type']
                type_value = self.processed_row[type_index]

                removal_index = self.header_index_map['positions_not_profiled']

                if type_value == 'Not Profiled' or profile_value == 'Not Profiled':
                    self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0
                
                #10. Best practice profile

                profile_index = self.header_index_map['profile_name']
                profile_value = self.processed_row[profile_index]

                removal_index = self.header_index_map['best_practice_profile']

                if type_value == 'Not Profiled' or profile_value == 'Not Profiled':
                    self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0
                

                #11. "Neither" termination reason

                hire_index = self.header_index_map['orig_hire_date']
                term_index = self.header_index_map['orig_term_date']
                category_index = self.header_index_map['term_category']
                category_value = self.processed_row[category_index]

                removal_index = self.header_index_map['neither_term_reason']

                hire_value = datetime.datetime.strptime(self.processed_row[hire_index], '%m/%d/%Y').date()

                #Only do a date conversion if there is a termination date
                if self.processed_row[term_index]:
                    term_value = datetime.datetime.strptime(self.processed_row[term_index], '%m/%d/%Y').date()
                else:
                    term_value = ''

                if category_value == 'Neither':
                    for period in study_periods_to_check:
                        start_key_value = 'study_period_start_' + period
                        end_key_value = 'study_period_end_' + period

                        if self.form_dict[start_key_value] <= hire_value <= self.form_dict[end_key_value]:
                            if term_value:
                                if self.form_dict[start_key_value] <= term_value <= self.form_dict[end_key_value]:
                                    self.processed_row[removal_index] = 1
                                    break
                                else:
                                    self.processed_row[removal_index] = 0
                            else:
                                self.processed_row[removal_index] = 0

                        else:
                            self.processed_row[removal_index] = 0
                else:
                    self.processed_row[removal_index] = 0

                #12. Incomplete assessment

                pa_id_index = self.header_index_map['pa_id']
                pa_id_value = self.processed_row[pa_id_index]
                fit_index = self.header_index_map['fit_score']
                fit_value = self.processed_row[fit_index]

                removal_index = self.header_index_map['incomplete_assessment_post']

                if pa_id_value:
                    if fit_value:
                        self.processed_row[removal_index] = 0
                    else:
                        self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0
                

                #13. Assessed after hire

                orig_hire_index = self.header_index_map['orig_hire_date']
                early_index = self.header_index_map['earliest_test_completion']
                latest_index = self.header_index_map['latest_test_completion']
                
                if self.processed_row[orig_hire_index]:
                    orig_hire_value = datetime.datetime.strptime(self.processed_row[orig_hire_index], '%m/%d/%Y').date() 
                else:
                    orig_hire_value = ''

                if self.processed_row[early_index]:
                    early_value = datetime.datetime.strptime(self.processed_row[early_index], '%m/%d/%Y').date() 
                else:
                    early_value = ''

                if self.processed_row[latest_index]:
                    latest_value = datetime.datetime.strptime(self.processed_row[latest_index], '%m/%d/%Y').date() 
                else:
                    latest_value = ''

                removal_index = self.header_index_map['post_assessed_after_hire']

                #find the max test completed date
                if early_value:
                    if latest_value:
                        if early_value < latest_value:
                            max_value = latest_value 
                        else:
                            max_value = early_value
                    else:
                        max_value = early_value 

                else:
                    if latest_value:
                        max_value = latest_value 
                    else:
                        max_value = ''

                if max_value and orig_hire_value:
                    if orig_hire_value < max_value:
                        self.processed_row[removal_index] = 1
                    else:
                        self.processed_row[removal_index] = 0
                else:
                    self.processed_row[removal_index] = 0


                #14. Days employed

                hire_index = self.header_index_map['orig_hire_date']
                term_index = self.header_index_map['orig_term_date']
                hire_value = datetime.datetime.strptime(self.processed_row[hire_index], '%m/%d/%Y').date()

                #Only do a date conversion if there is a termination date
                if self.processed_row[term_index]:
                    term_value = datetime.datetime.strptime(self.processed_row[term_index], '%m/%d/%Y').date()
                else:
                    term_value = ''

                days_index = self.header_index_map['days_employed']
                terminated_index = self.header_index_map['terminated']

                for period in study_periods_to_check:
                    start_key_value = 'study_period_start_' + period
                    end_key_value = 'study_period_end_' + period

                    if term_value:

                        self.processed_row[terminated_index] = 1

                        if self.form_dict[start_key_value] <= hire_value <= self.form_dict[end_key_value]:
                            if self.form_dict[start_key_value] <= term_value <= self.form_dict[end_key_value]:
                                date_diff = term_value - hire_value 
                                self.processed_row[days_index] = date_diff.days
                            else:
                                self.processed_row[days_index] = 0
                        else:
                            if self.form_dict[start_key_value] > term_value or term_value > self.form_dict[end_key_value]:
                                date_diff = self.form_dict[end_key_value] - hire_value 
                                self.processed_row[days_index] = date_diff.days
                            else:
                                self.processed_row[days_index] = 0

                    else:
                        self.processed_row[terminated_index] = 0
                        if self.form_dict[start_key_value] <= hire_value <= self.form_dict[end_key_value]:
                            date_diff = self.form_dict[end_key_value] - hire_value 
                            self.processed_row[days_index] = date_diff.days
                        else:
                            self.processed_row[days_index] = 0
                    

                #15. Employed Less than minimum_days 

                days_index = self.header_index_map['days_employed']
                days_value = self.processed_row[days_index]

                removal_index = self.header_index_map['less_than_min_days']

                for period in study_periods_to_check:
                    key_value = 'minimum_days_' + period

                    if days_value < self.form_dict[key_value]:
                        self.processed_row[removal_index] = 1
                    else:
                        self.processed_row[removal_index] = 0

                        
                #16. Location closed check

                location_index = self.header_index_map['location_class_1']
                location_value = self.processed_row[location_index]

                removal_index = self.header_index_map['location_closed']

                if location_value == 'Open':
                    self.processed_row[removal_index] = 0
                else:
                    self.processed_row[removal_index] = 1


                #17. Rehire date check

                hire_index = self.header_index_map['orig_hire_date']
                rehire_index = self.header_index_map['rehire_date']
                hire_value = datetime.datetime.strptime(self.processed_row[hire_index], '%m/%d/%Y').date()

                if self.processed_row[rehire_index]:
                    rehire_value = datetime.datetime.strptime(self.processed_row[rehire_index], '%m/%d/%Y').date()
                else:
                    rehire_value = ''


                removal_index = self.header_index_map['rehires']

                if rehire_value:
                    if hire_value == rehire_value:
                        self.processed_row[removal_index] = 0
                    else:
                        self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 0


                #18. Changed position check

                hire_index = self.header_index_map['orig_hire_date']
                date_index = self.header_index_map['date_in_position']
                hire_value = datetime.datetime.strptime(self.processed_row[hire_index], '%m/%d/%Y').date()

                if self.processed_row[date_index]:
                    date_value = datetime.datetime.strptime(self.processed_row[date_index], '%m/%d/%Y').date()
                else:
                    date_value = ''

                removal_index = self.header_index_map['change_position']

                if date_value:
                    if hire_value == date_value:
                        self.processed_row[removal_index] = 0
                    else:
                        self.processed_row[removal_index] = 1
                else:
                    self.processed_row[removal_index] = 1


                ##### End of Removal Reasons ####


                file_writer.writerow(self.processed_row)
                output_file.flush()

        output_file.close()
        return self.study_file_name


