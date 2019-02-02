#!/usr/bin/env python3
import requests, bs4
import json, os, sys
import time, datetime
import re
from amfibious import AmfibiousCrawler

class AmfibiousParser:
   def __init__(self):
        self.NODATA = re.compile('No data found on the basis of selected parameters for this report')
        self.HEADING = re.compile('Scheme Code;Scheme Name')
        self.OPENENDED = re.compile('Open Ended Scheme')
        self.AMC = re.compile('Mutual Fund')

   def nodata(self,raw_string):
       """ Checks if the data file has any useful info """
       if re.search(self.NODATA,raw_string):
           return True
       else:
           return False
   def write_file(self,fh,data):
        #Add some validations here
        try:
            fh.write(data)
            fh.close()
        except:
            print("Unexpected error:{0}".format(sys.exc_info()[0]))

   def process_raw(self,raw_string):
       """ This will remove all blank lines from the downloaded file. Returns
       a list of non-blank lines"""
       return [ line for line in raw_string.split('\n') if line.strip() ]

   def parse(self,processed_data,data={}):
       """ The goal is:
           - Create a scheme code wise json structure with 2 sections:
           - meta: a dictionary that has scheme name, fund AMC, category etc
           - data: list of (date, NAV) tuples
       """
       for line in processed_data:
           if re.search(self.HEADING,line):
               headings = line.split(';')
           elif re.search(self.OPENENDED,line):
              c = []
              parts = line.split('(')
              for p in parts:
                  c.append(p.split('-'))
                  categories = [item.strip(')').strip() for sublist in c for item in sublist]
           elif line.endswith('Mutual Fund'):
              amc = line
              if not amc in data.keys():
                data[amc] = {}
           elif len(line.split(';')) > 1:
               code,name,nav,rp,sp,date = line.split(';')
               if code not in data[amc].keys():
                 data[amc][code] = {}
                 data[amc][code]["data"] = []
                 data[amc][code]["meta"] = { "name": name, "amc": amc, "fund_type": "open ended", "scheme_code": int(code), "categories": categories }
               #year = datetime.datetime.strptime(date,'%d-%b-%Y').year
               #if year in data[amc][code]["data"].keys():
                   #data[amc][code]["data"][year].append({"date": date,"nav": nav})
               #else:
               #    data[amc][code]["data"][year] = []
               data[amc][code]["data"].append({"scheme_code": int(code), "date": datetime.datetime.strptime(date,'%d-%b-%Y'),"nav": nav})
       return data

   def write_json(self, filename, json_data):
       fh = open(filename,'w+')
       self.write_file(fh,json.dumps(json_data,indent=4,default=str))

   def get_json_from_amc_csvs(self,amc,in_dir):
       filematch = '_'.join(amc.split())
       amc_data = {}
       for root, dirs, files in os.walk(in_dir):
           for f in files:
               if not f.find(filematch):
                   d = open(os.path.join(in_dir,f)).read()
                   if not self.nodata(d):
                       pdata = self.process_raw(d)
                       amc_data = self.parse(pdata,amc_data)
       return amc_data

   def write_json_data(self,data, out_dir):
       for amc in data.keys():
           for scheme in data[amc].keys():
               meta_file = os.path.join(out_dir,scheme + '_meta.json')
               meta_data = data[amc][scheme]['meta']
               data_file = os.path.join(out_dir,scheme + '_data.json')
               data_data = data[amc][scheme]['data']
               self.write_json(meta_file,meta_data)
               self.write_json(data_file, data_data)

   def write_json_from_csvs(self,in_dir,out_dir):
       amfiobj = AmfibiousCrawler()
       amc_pairs = amfiobj.get_amc_codes()
       for amc_name, amc_code in amc_pairs.items():
           data = self.get_json_from_amc_csvs(amc_name,in_dir)
           self.write_json_data(data, out_dir)

   def write_direct_json_from_cvs(self,in_dir,out_dir):
       if not os.path.exists(out_dir):
           os.mkdir(out_dir)
       data = self.get_jsons_from_csvs(in_dir)
       for amc in data.keys():
           for scheme in data[amc].keys():
               meta_file = os.path.join(out_dir,scheme + '_meta.json')
               meta_data = data[amc][scheme]['meta']
               data_file = os.path.join(out_dir,scheme + '_data.json')
               data_data = data[amc][scheme]['data']
               if re.search('direct',meta_data['name'],re.IGNORECASE):
                   self.write_json(meta_file,meta_data)
                   self.write_json(data_file, data_data)

