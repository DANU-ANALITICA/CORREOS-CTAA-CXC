# CORREOS CTAA (CXC)

## Descripción

Este proyecto envía las **cuentas por cobrar pendientes** a cada cliente de **CTAA** por correo electrónico.

La información se lee desde **BigQuery**, se arma un reporte HTML por cliente y se envía vía **Gmail SMTP**.

## Fuentes de datos

El proyecto usa **2 sources** en BigQuery:

1. **Cuentas por cobrar** — facturas pendientes por cliente.
   - Tabla: `ctaa-460716.intermediate.int_facturacion_cuentas_cobrar`
   - Filtros: `FECHA_FACTURA > '2026-01-01'`, `SALDO_ACTUAL > 0`, match por `NOMBRE_CLIENTE`

2. **Correos de clientes** — destinatarios a quienes se envía el cobro.
   - Tabla: `ctaa-460716.raw_data.clientes_correo`
   - Modo prueba: todos los correos apuntan a `lucia.balli@danuanalitica.com`

## Flujo (`main.py`)

1. `get_correos_clientes()` — obtiene la lista de clientes y correos.
2. `get_cuentas_por_cobrar(nombre_cliente)` — trae las facturas pendientes de ese cliente.
3. `send_email_cxc(df, nombre_cliente, email_destino)` — envía el reporte HTML con la tabla y el saldo total.

Por cada cliente se repite: consultar CXC → si hay datos, enviar correo.

## Configuración

Variables en `.env`:

| Variable | Uso |
|----------|-----|
| `GCP_PROJECT` | Proyecto de Google Cloud |
| `EMISOR` | Cuenta Gmail que envía |
| `PASSWORD` | App password de Gmail |

## Corrida del script

### Requisitos previos

1. Entorno virtual activo y dependencias instaladas (ver `Instructivo.MD`).
2. Autenticación con Google Cloud:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. Archivo `.env` configurado con `GCP_PROJECT`, `EMISOR` y `PASSWORD`.

### Comandos

Desde la carpeta del proyecto:

```bash
cd "/Users/luciaballi/Correos - CTAA (CXC)"
source venv/bin/activate
python main.py
```

### Qué hace al correr

1. Lee los clientes desde BigQuery (`clientes_correo`).
2. Por cada cliente, consulta sus cuentas por cobrar pendientes.
3. Si hay facturas con saldo > 0, envía un correo HTML con el reporte.
4. En consola verás el progreso: cliente, cantidad de facturas y confirmación de envío.

> **Modo prueba:** todos los correos se envían a `lucia.balli@danuanalitica.com`, no a los clientes reales.

---

_Más detalles se irán agregando conforme avance el desarrollo._
