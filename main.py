# main.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import pandas as pd
from google.cloud import bigquery

# ─── CONFIGURACIÓN (.env) ─────────────────────────────────────────────────────
load_dotenv()
PROJECT_ID = os.environ["GCP_PROJECT"]
EMISOR = os.environ.get("EMISOR", "")
PASSWORD = os.environ.get("PASSWORD", "")

client = bigquery.Client(project=PROJECT_ID)


# ─── CORREOS DE CLIENTES ──────────────────────────────────────────────────────
# Source 2: obtiene nombre y correo de cada cliente desde BigQuery.
# Modo prueba: todos los correos apuntan a lucia.balli para no enviar a clientes reales.
def get_correos_clientes() -> pd.DataFrame:
    query = """
    SELECT DISTINCT
        nombre_cliente,
        "lucia.balli@danuanalitica.com" AS email_cliente
    FROM ctaa-460716.raw_data.clientes_correo
    where nombre_cliente = 'FANUC MEXICO'
    """
    return client.query(query).to_dataframe()


# ─── CUENTAS POR COBRAR (BIGQUERY) ────────────────────────────────────────────
# Source 1: trae las facturas pendientes de un cliente filtrando por NOMBRE_CLIENTE.
def get_cuentas_por_cobrar(nombre_cliente: str) -> pd.DataFrame:
    query = """
    SELECT
        GRUPO_EMPRESARIAL,
        RAZON_SOCIAL,
        FECHA_FACTURA,
        FACTURA,
        SALDO_ACTUAL
    FROM `ctaa-460716.intermediate.int_facturacion_cuentas_cobrar`
    WHERE FECHA_FACTURA > '2026-01-01'
      AND UPPER(TRIM(NOMBRE_CLIENTE)) = UPPER(TRIM(@nombre_cliente))
      AND SALDO_ACTUAL > 0
    ORDER BY FECHA_FACTURA DESC
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("nombre_cliente", "STRING", nombre_cliente)
        ]
    )
    return client.query(query, job_config=job_config).to_dataframe()


# ─── ENVÍO DE CORREO ────────────────────────────────────────────────────────────
# Arma el HTML con la tabla de CXC y lo envía por Gmail SMTP.
def send_email_cxc(df: pd.DataFrame, nombre_cliente: str, email_destino: str) -> None:
    if df.empty:
        print(f"Sin cuentas por cobrar para {nombre_cliente}, no se envía correo.")
        return

    total_saldo = df["SALDO_ACTUAL"].sum()

    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333333;
            margin: 20px;
        }}
        h2 {{
            color: #0d2c54;
            border-bottom: 2px solid #0d2c54;
            padding-bottom: 8px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 15px;
            font-size: 13px;
        }}
        th {{
            background-color: #0d2c54;
            color: white;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #dddddd;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #f1f3f5;
        }}
        .total {{
            margin-top: 15px;
            font-weight: 600;
            color: #0d2c54;
        }}
    </style>
    </head>
    <body>
    <p>Buen día,</p>
    <p>Te comparto el reporte de <strong>cuentas por cobrar pendientes</strong> de CTAA para su revisión.</p>
    <h2>Cuentas por cobrar — {nombre_cliente}</h2>
    {df.to_html(index=False)}
    <p class="total">Saldo total pendiente: ${total_saldo:,.2f}</p>
    <br>
    <p style="font-size: 11px; color: #777777;">Este es un correo automático generado por el sistema.</p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Cuentas por cobrar pendientes — {nombre_cliente}"
    msg["From"] = EMISOR
    msg["To"] = email_destino
    msg.attach(MIMEText(html, "html"))

    if not EMISOR or not PASSWORD:
        print("⚠️ EMISOR o PASSWORD no están configurados en .env. No se puede enviar el correo.")
        return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMISOR, PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Correo enviado a {email_destino} ({nombre_cliente})")
    except Exception as e:
        print(f"❌ Error al enviar correo a {email_destino}: {e}")


# ─── EJECUCIÓN ──────────────────────────────────────────────────────────────────
# Por cada cliente: consulta sus CXC pendientes y envía el reporte por correo.
if __name__ == "__main__":
    try:
        correos = get_correos_clientes()
        print(f"Clientes a procesar: {len(correos)}\n")

        for _, row in correos.iterrows():
            nombre = row["nombre_cliente"]
            email = row["email_cliente"]
            print(f"--- {nombre} → {email} ---")
            print("Consultando cuentas por cobrar...")
            df = get_cuentas_por_cobrar(nombre)
            print(f"{len(df)} facturas pendientes\n")
            print("Enviando reporte por correo...")
            send_email_cxc(df, nombre, email)
            print()
    except Exception as e:
        print(f"Ocurrió un error: {e}")
