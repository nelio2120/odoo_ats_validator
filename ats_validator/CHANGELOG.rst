Changelog
=========

19.0.1.1.1 (2026-06-23)
------------------------

**Bugfixes**

- Reescrita ``static/description/index.html`` como fragmento HTML con
  estilos inline. Odoo Apps Store elimina el bloque ``<style>`` y las
  etiquetas de documento (``<html>``, ``<head>``, ``<body>``) de la
  descripción, por lo que el diseño se mostraba sin ningún CSS aplicado.

19.0.1.1.0 (2026-06-23)
------------------------

**Improvements**

- URL del validador por defecto ahora apunta al servicio público alojado
  (``https://validator.ats.erp360app.com``); el autohospedaje queda como
  opción avanzada.
- ``errors_xsd``, ``errors`` y ``warnings`` migrados de ``fields.Text``
  (JSON serializado a mano) a ``fields.Json``, eliminando el
  ``json.dumps``/``json.loads`` manual.
- Eliminado el campo ``server_url`` (computado, no usado en ninguna vista).
- Agregados tests unitarios para ``action_validar`` y ``action_reset``
  (``tests/test_ats_validation.py``).

19.0.1.0.0 (2026-06-23)
------------------------

- Primera versión del módulo para Odoo 19.0: subida de XML del ATS,
  validación contra el microservicio externo, visualización de errores
  XSD, errores de negocio, advertencias y talón resumen HTML.
