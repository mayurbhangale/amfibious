#!/usr/bin/env python3
import amfibious

# Get data from AMFI
downloader = amfibious.AmfibiousCrawler()
downloader.download_data()

# Parse and write jsons
k = amfibious.AmfibiousParser()
k.write_json_from_csvs('data/amfidata/','data/json_data')

# Dump data to MongoDB
m = amfibious.AmfiMongo()
m.write_jsons_to_docments('data/amfidata')
