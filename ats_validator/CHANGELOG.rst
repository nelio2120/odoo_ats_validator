Changelog
=========

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
