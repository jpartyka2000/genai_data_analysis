#!/opt/anaconda/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import sys
from time import strptime
from datetime import date

# from matching import Constants_Miscellaneous
from satool import Constants_Miscellaneous

#quit()
#sys.path.append(match_path)

import psycopg2  #connection for PostgreSQL database


class DatabaseLoaderClass():
    def __init__(self):
        self.check_set = set()
        self.database_connections = {}
        self.database_cursors = {}
        self.initialize_database_connections()

    def initialize_database_connections(self):
        pass
        #self.database_connections['pgsql'] = psycopg2.connect(
        #    "host=10.48.24.112 port=5432 dbname=study_data user=postgres password=r00t4gres")
        #self.database_connections['pgsql'].autocommit = True
        #self.database_cursors['pgsql'] = self.database_connections['pgsql'].cursor()

        #self.database_connections['pgsql-pa'] = psycopg2.connect(
        #    "host=10.48.24.112 port=5432 dbname=panswers_io user=postgres password=r00t4gres")
        #self.database_connections['pgsql-pa'].autocommit = True
        #self.database_cursors['pgsql-pa'] = self.database_connections['pgsql-pa'].cursor()

        #self.database_connections['pgsql-pa-dev'] = psycopg2.connect(
        #    "host=10.48.24.112 port=5432 dbname=panswers_io_dev user=postgres password=r00t4gres")
        #self.database_connections['pgsql-pa-dev'].autocommit = True
        #self.database_cursors['pgsql-pa-dev'] = self.database_connections['pgsql-pa-dev'].cursor()

    def close_database_connections(self):

        for key in self.database_cursors.keys():
            try:
                self.database_cursors[key].close()
            except:
                continue

        for key in self.database_connections.keys():
            try:
                self.database_connections[key].close()
            except:
                continue

    def get_business_unit_id(self, company_id):

        cur = self.database_cursors['pgsql-pa-dev']
        query = """SELECT Primary_Business_Unit_Id from Companies where Company_Id=%s;""" % (company_id)

        cur.execute(query)

        row = cur.fetchone()

        if row is None:
            business_unit_id = None
        else:
            business_unit_id = row[0]

        return business_unit_id


    def get_all_clients(self):

        company_list = []

        cur = self.database_cursors['pgsql-pa-dev']
        query = """SELECT company_name FROM companies;"""
        cur.execute(query)
        row = cur.fetchone()
        while row is not None:
            result_string = row[0]
            result_string = result_string.encode('utf-8').strip()
            company_list.append(result_string)
            row = cur.fetchone()

        return company_list

    def get_client_id(self, company_name):

        cleaned_name = str()
        id_value = str()

        #check name for special characters
        if "'" in company_name:
            cleaned_name = company_name.replace('\'', '\'\'')
        elif company_name == "Macys":
            cleaned_name = "Macy''s"
        elif company_name == "Wellpoint (ACM)":
            cleaned_name = "WellPoint"
        elif company_name == "New York and Company":
            cleaned_name = "New York & Company"
        else:
            cleaned_name = company_name

        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT company_id FROM companies WHERE company_name='%s';""" % (cleaned_name)
        cur.execute(query)
        row = cur.fetchone()

        if row is not None:
            id_value = row[0]
        else:
            id_value = None

        return id_value


    def get_client_jobs(self, company_id):

        jobs_list = []
        cur = self.database_cursors['pgsql-pa-dev']

        #query = """SELECT Job_Id,Job_Name,Status from Jobs WHERE Company_Id=%s AND Status=1;""" % (company_id)
        query = """SELECT Job_Id,Job_Name,Status from Jobs WHERE Company_Id=%s;""" % (company_id)

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:

            this_job_list = []
            job_id = row[0]

            this_job_list.append(job_id)

            job_name = row[1]
            job_name = job_name.encode('utf-8').strip()
            this_job_list.append(job_name)

            status = row[2]
            status_str = ""

            if status == 2:
                status_str = "Inactive"
            else:
                status_str = "Active"

            this_job_list.append(status_str)

            #add this_job_list to jobs_list
            jobs_list.append(this_job_list)
            row = cur.fetchone()

        return jobs_list

    def get_client_positions(self, business_unit_id):

        #fetch all fields from each row returned in the query
        positions_list = []
        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT * FROM Positions WHERE Business_Unit_Id=%s ORDER BY Title;""" % (business_unit_id)

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            positions_list.append(row)
            row = cur.fetchone()

        return positions_list

    def get_client_position_versions(self, position_id):

        position_versions_list = []

        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT * FROM Position_Versions WHERE Position_Id=%s AND Lifecycle_State=2;""" % (position_id)

        cur.execute(query)
        row = cur.fetchone()

        if row is not None:
            position_versions_list.append(row)
            row = cur.fetchone()

        return position_versions_list


    def get_client_position_position_types(self, position_id):

        #this list contains all the fields in each row returned by the query
        position_position_types_list = []

        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT * FROM Position_Position_Types WHERE Position_Id=%s ORDER BY Position_Type_Id;""" % (
        position_id)

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            position_position_types_list.append(row)
            row = cur.fetchone()

        return position_position_types_list

    def get_client_department_name(self, company_department_id):

        result_list = []

        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT Department_Name FROM Company_Departments WHERE Company_Department_Id=%s;""" % (
        company_department_id)

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            result_list.append(row[0])
            row = cur.fetchone()

        return result_list

    def get_client_position_geography(self, position_company_geography_id):

        cur = self.database_cursors['pgsql-pa-dev']

        query = """SELECT Geography_Name FROM Company_Geographies WHERE Company_Geography_Id=%s;""" % (
        position_company_geography_id)

        cur.execute(query)
        row = cur.fetchone()

        return row[0]


    def get_client_profiles(self, company_name):

        profile_list = []
        client_id = self.get_client_id(company_name)

        cur = self.database_cursors['pgsql-pa-dev']
        query = """SELECT profile_name from profiles WHERE company_id=%s;""" % (client_id)
        cur.execute(query)
        row = cur.fetchone()
        while row is not None:
            result_string = row[0]
            result_string = result_string.encode('utf-8').strip()
            profile_list.append(result_string)
            row = cur.fetchone()

        return profile_list

    def create_study_id(self, study_date=None, company_name=None, company_id=None):

        if company_name is not None:
            client_id = int(self.get_client_id(company_name))
        else:
            client_id = int(company_id)

        #error conditions
        if company_name is None and company_id is None:
            return None

        if study_date is None:
            return None

        #study date format for strings must be YYYY-MM-DD
        #"date" type is ok otherwise
        if isinstance(study_date, date):
            #month = str(study_date.month)
            month = '%0.2d' % (study_date.month)
            year = str(study_date.year)
        else:
            year_month_day = study_date.split('-')
            year = year_month_day[0]
            month = year_month_day[1]

        new_date = month + year

        client_id_str = '%0.4d' % client_id
        id_string = client_id_str + new_date

        return id_string

    def select_spreadsheet_data(self, query):

        results_list = []
        cur = self.database_cursors['pgsql-pa-dev']

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            #convert tuple to list
            results_list.append(row)
            row = cur.fetchone()

        return results_list

    def select_query(self, query):

        results_list = []

        cur = self.database_cursors['pgsql-pa-dev']

        cur.execute(query)
        row = cur.fetchone()

        while row is not None:
            #convert tuple to list
            result_list = [str(x) for x in row]
            results_list.append(result_list)
            row = cur.fetchone()

        return results_list

    def dml_query(self, query, strip_newlines=False):

        if strip_newlines:
            query = query.replace('\n', '')

        cur = self.database_cursors['pgsql-pa-dev']

        cur.execute(query)
