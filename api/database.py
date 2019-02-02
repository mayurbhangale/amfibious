from mongoengine import connect

from models import NAVs, Schemes

connect('amfibious', host='localhost',port=27017)