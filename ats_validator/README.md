# ATS Validator — Módulo Odoo 18

Módulo genérico para Odoo 18 que permite validar el **Anexo Transaccional Simplificado (ATS)** del SRI Ecuador enviando un XML a un servicio REST externo y mostrando los resultados directamente en la interfaz de Odoo.

> Este módulo es un **cliente genérico**. No genera el XML del ATS — eso lo hace el módulo de localización ecuatoriana instalado en tu instancia. Este módulo toma ese XML, lo envía al validador y presenta el resultado.

---

## Requisitos

| Requisito | Versión |
|-----------|---------|
| Odoo | 19.0 |
| Python | 3.10+ |
| `requests` | incluido en Odoo |
| Servicio ATS Validator | corriendo y accesible |

### Servicio ATS Validator

Este módulo requiere el microservicio **[ats-validator](https://github.com/tu-org/ats-validator)** corriendo como backend de validación. Es un JAR de Spring Boot autocontenido que expone la API REST utilizada por este módulo.

```bash
java -jar ats-validator-1.0.0.jar
# Escucha en http://localhost:8080 por defecto
```

---

## Instalación

1. Copia la carpeta `ats_validator` dentro de tu directorio de addons custom.
2. Actualiza la lista de módulos en Odoo (`Ajustes > Activar modo desarrollador > Actualizar lista de aplicaciones`).
3. Busca **ATS Validator** e instálalo.

---

## Configuración

Ve a **Contabilidad › Configuración › Ajustes**, sección **Validador ATS**, y configura la URL del servicio:

```
http://localhost:8080
```

Si el servicio corre en otro host o puerto, cámbialo aquí. El valor se guarda como parámetro del sistema (`ats_validator.server_url`) y aplica a todas las compañías.

---

## Uso

### 1. Acceder al menú

**Contabilidad › Reportes › Validaciones ATS**

### 2. Crear una validación

- Haz clic en **Nuevo**.
- Adjunta el archivo `.xml` del ATS en el campo **Archivo XML**.
- Pulsa **Validar XML**.

### 3. Leer los resultados

| Resultado | Descripción |
|-----------|-------------|
| Estado `Válido` | El XML pasa XSD y reglas de negocio. Se muestra el **talón resumen HTML** del SRI. |
| Estado `Inválido` | Se muestran los errores XSD y/o errores de reglas de negocio que impiden la validez. |
| Advertencias | Se muestran aunque el documento sea válido. No bloquean la validación. |

El talón HTML generado por el servicio es autocontenido (CSS y logo embebidos) y se renderiza directamente en la vista de Odoo.

---

## Flujo de validación

```
Usuario sube XML
      │
      ▼
POST /api/ats/validar  ──── error de conexión ──► UserError con mensaje
      │
      ▼
Respuesta JSON
      │
      ├── valido: true  ──► Estado = Válido + talón HTML visible
      │
      └── valido: false ──► Estado = Inválido + errores XSD / negocio visibles
```

---

## Estructura del módulo

```
ats_validator/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── ats_validation.py        # Modelo principal + llamada HTTP
│   └── res_config_settings.py  # URL configurable desde Ajustes
├── views/
│   ├── ats_validation_views.xml       # Vistas list y form
│   ├── res_config_settings_views.xml  # Sección en Ajustes de Contabilidad
│   └── menu.xml                       # Ítem de menú bajo Contabilidad > Reportes
├── security/
│   └── ir.model.access.csv      # Acceso por rol contable
├── data/
│   └── sequences.xml            # Secuencia ATS/YYYY/NNNN
└── README.md
```

---

## Permisos

| Grupo | Leer | Escribir | Crear | Eliminar |
|-------|------|----------|-------|----------|
| Contabilidad / Usuario | ✓ | ✓ | ✓ | — |
| Contabilidad / Administrador | ✓ | ✓ | ✓ | ✓ |

---

## API del servicio (referencia)

El módulo consume únicamente este endpoint:

```
POST {url}/api/ats/validar
Content-Type: application/xml

<body: contenido del XML>
```

Respuesta esperada:

```json
{
  "valido": true,
  "erroresXsd": [],
  "errores": [],
  "advertencias": [],
  "talonHtml": "<html>...</html>"
}
```

---

## Autor y soporte

**Nelio Ciguencia** — [@nelio2120](https://github.com/nelio2120) — neliomarcos040@gmail.com

---

## Licencia

[LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html)
