Changelog
=========

19.0.1.1.4 (2026-06-23)
------------------------

**Improvements**

- Agregado ``static/description/banner.png`` (560x280), la imagen de
  portada/miniatura ("cover image") que exige el scanner de calidad
  de Odoo Apps Store. Es un archivo distinto de ``icon.png``.

19.0.1.1.3 (2026-06-23)
------------------------

**Improvements**

- Agregado ``static/description/icon.png`` (icono del modulo, visible
  en el listado de Odoo Apps) y referenciado como imagen de cabecera
  en ``index.html``.

19.0.1.1.2 (2026-06-23)
------------------------

**Bugfixes**

- ``static/description/index.html`` reescrita en ASCII puro (entidades
  HTML para tildes/enies/simbolos): el importador de Odoo Apps Store
  duplicaba la codificacion UTF-8 y mostraba texto corrupto
  (``MÃ³dulo`` en vez de ``Módulo``).
- Eliminadas las propiedades CSS que el sanitizador de Apps Store
  descarta del atributo ``style`` (``background``, ``border-left``,
  ``gap``, ``justify-content``, ``align-items``, ``flex-wrap``,
  ``grid-template-columns``); el layout de tarjetas/grillas se
  reemplaza por tablas HTML nativas.

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
