# CORREOS CTAA (CXC)

## Descripción

Este proyecto envía las **cuentas por cobrar pendientes** a cada cliente de **CTAA**.

La información se obtiene desde **BigQuery**.

## Fuentes de datos (por ahora)

Por el momento el proyecto usa **2 sources** en BigQuery:

1. **Cuentas por cobrar** — de aquí salen las cuentas pendientes por cliente.
   - Tabla: `ctaa-460716.intermediate.int_facturacion_inventario_pendientes`

2. **Correos de clientes** — de aquí salen los correos de los clientes a quienes se les enviará el cobro.

---

_Más detalles se irán agregando conforme avance el desarrollo._
