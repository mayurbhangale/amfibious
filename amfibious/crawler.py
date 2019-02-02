#!/usr/bin/env python3
import requests, bs4
import json, os
import time, datetime
import sys
import config

class AmfibiousCrawler:
    def __init__(self):
        self.CODES_URL = 'https://www.amfiindia.com/nav-history-download'
        self.NAV_URL_TEMPLATE = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&'
        self.START_DATE = config.START_DATE
        self.END_DATE = datetime.datetime.strftime(datetime.datetime.today(),'%d-%b-%Y')

    def get_url_data(self,url):
        try:
            r = requests.get(url,timeout=100000)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        return r.text

    def get_amc_codes(self):
        url = 'https://www.amfiindia.com/nav-history-download'
        r = self.get_url_data(url)
        if r:
          soup = bs4.BeautifulSoup(r, 'html.parser')
          NavDownMFName =  soup.find_all("select",id="NavDownMFName")
          amc_codes = { e.string:e.attrs['value'] for e in NavDownMFName[0].findAll('option') if e.attrs['value'] != ''}
        else:
           amc_codes = None
        return amc_codes

    def write_file(self,fh,data):
        #Add some validations here
        try:
            fh.write(data)
            fh.close()
        except:
            print("Unexpected error:{0}".format(sys.exc_info()[0]))

    def get_amc_nav_data(self,amc,start_date=None,end_date=None):
        if start_date is None:
            start_date = self.START_DATE
        if end_date is None:
            end_date = self.END_DATE
        url = self.NAV_URL_TEMPLATE + 'frmdt=' + start_date + '&todt=' + end_date + '&mf=' + amc
        data = self.get_url_data(url)
        return data

    def write_amc_files(self,start_date=None,end_date=None):
        if start_date is None:
            start_date = self.START_DATE
        if end_date is None:
            end_date = self.END_DATE
        amc_pairs = self.get_amc_codes()
        lockdata = {}
        today = datetime.datetime.strftime(datetime.datetime.strptime(end_date, '%d-%b-%Y'), '%s')
        for amc_name, amc_code in amc_pairs.items():
            data = self.get_amc_nav_data(amc_code,start_date=start_date,end_date=end_date)
            name = '_'.join(amc_name.split())
            filename = '_'.join([name, today]) + '.csv'
            self.write_file(open(os.path.join('amfidata',filename),'w+'), data)
            lockdata[amc_name] = end_date
            time.sleep(20)
        lockdata['global'] = end_date
        self.write_file(open('amfidata/lockfile.json','w+'), json.dumps(lockdata,sort_keys=True, indent=4))

    def init_or_update(self):
        """ Returns startdate to get the data from, depending on when the
        update was perfomed last"""
        data_init = False
        data_update = False
        if os.path.isfile('amfidata/lockfile.json'):
            d = json.load(open('amfidata/lockfile.json'))
            return datetime.datetime.strftime(datetime.datetime.strptime(d['global'],'%d-%b-%Y') + datetime.timedelta(days=1), '%d-%b-%Y')
        else:
            return self.START_DATE
    def download_data(self):
        start_date = self.init_or_update()
        self.write_amc_files(start_date=start_date)
