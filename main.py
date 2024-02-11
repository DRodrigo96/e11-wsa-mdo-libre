# main.py
# ==================================================
# standard
import os
# --------------------------------------------------

os.system('scrapy runspider ./scripts/crawler.py -o ./resources/MERCADO_LIBRE_DATA.csv')
