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


# ─── BIGQUERY ─────────────────────────────────────────────────────────────────
def get_backorder_mty(provider_name: str ) -> pd.DataFrame:
    """
    Retrieves backorder records from BigQuery for a specific client.
    """
    
    query = """
       SELECT
    referencia AS referencia,
     clave_cliente,
    count(*) as num_facturas,
    COUNTIF(status_comprobante = 'PENDIENTE')  AS GASTOS_PENDIENTES_POR_FACTURAR,
    COUNTIF(status_comprobante = 'FACTURADO')  AS GASTOS_FACTURADOS
  FROM
    ctaa-460716.intermediate.int_facturacion_inventario_pendientes
    GROUP BY 
    1,
    2
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("provider_name", "STRING", provider_name)
        ]
    )
    
    df = client.query(query, job_config=job_config).to_dataframe()
    return df


if __name__ == "__main__":
    df = get_backorder_mty("test")
    print(df.head())
    print(f"Filas: {len(df)}")