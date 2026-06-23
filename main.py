# main.py
import asyncio
import io
import os
import re
import smtplib
import time
import unicodedata
import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from dotenv import load_dotenv


import numpy as np
import pandas as pd
from google.cloud import bigquery
from playwright.async_api import async_playwright

#----ESTO SALE DEL .env
load_dotenv()
PROJECT_ID = os.environ["GCP_PROJECT"]
EMISOR = os.environ.get("EMISOR", "")
PASSWORD = os.environ.get("PASSWORD", "")
###RECEPTOR = os.environ.get("RECEPTOR", "")

client = bigquery.Client(project=PROJECT_ID)
# query = '''SELECT DISTINCT Proveedor, Nombre,
# COALESCE(
#   NULLIF(Email1, ''),
#   NULLIF(Email2, ''),
#   NULLIF(Email3, '')
# ) AS Email FROM `finsadashboard.raw_data.Proveedores`
# WHERE COALESCE(
#   NULLIF(Email1, ''),
#   NULLIF(Email2, ''),
#   NULLIF(Email3, '')
# )  is not NULL'''

query = '''SELECT DISTINCT Proveedor, Nombre,
'daniel.perez@danuanalitica.com' AS Email 
FROM `finsadashboard.raw_data.Proveedores` LIMIT 3
'''
