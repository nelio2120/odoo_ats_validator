# ATS Validator for Odoo 18

[![Odoo 18.0](https://img.shields.io/badge/Odoo-18.0-875A7B)](https://www.odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)

Módulo genérico para Odoo 18 que valida el **Anexo Transaccional Simplificado (ATS)** del SRI Ecuador. Sube un XML, lo envía a un microservicio validador y muestra los resultados — errores XSD, errores de reglas de negocio, advertencias y el **talón resumen HTML** — directamente en la interfaz de Odoo.

> **Este módulo es un cliente genérico.** No genera el XML del ATS. Lo hace el módulo de localización ecuatoriana instalado en tu instancia. Este módulo toma ese XML, lo envía al validador externo y presenta el resultado.

---

## Características

- Sube cualquier XML del ATS y lo valida en un clic
- Muestra errores de estructura XSD con detalle
- Muestra errores de reglas de negocio del SRI (las mismas que aplica el DIMM)
- Muestra advertencias sin bloquear la validez
- Renderiza el **talón resumen HTML** oficial directamente en Odoo cuando el XML es válido
- Historial de validaciones con secuencia automática `ATS/YYYY/NNNN`
- URL del servicio configurable desde Ajustes, sin tocar código
- Permisos integrados con los roles contables de Odoo

---

## Requisitos

### Odoo

| Componente | Versión |
|------------|---------|
| Odoo | 18.0 |
| Python | 3.10+ |
| Módulos Odoo | `account`, `mail` |

### Microservicio ATS Validator

Este módulo **requiere** el microservicio [ats-validator](https://github.com/nelio2120/ats-validator) corriendo y accesible desde el servidor Odoo. Es un JAR de Spring Boot autocontenido (~29 MB) que incluye los catálogos del SRI y las mismas reglas de validación del DIMM.

**Requisito del microservicio:** Java 11 o superior.

```bash
# Verificar Java
java -version

# Levantar el servicio (puerto 8080 por defecto)
java -jar ats-validator-1.0.0.jar
```

El servicio está listo cuando aparece en la consola:

```
Started AtsValidatorApplication in X seconds
```

---

## Instalación

### Desde Odoo Apps

1. En el backend de Odoo ve a **Aplicaciones**.
2. Busca **ATS Validator**.
3. Haz clic en **Instalar**.

### Instalación manual

1. Descarga o clona este repositorio:

   ```bash
   git clone https://github.com/nelio2120/odoo_ats_validator.git
   ```

2. Copia la carpeta `ats_validator` dentro de tu directorio de addons:

   ```bash
   cp -r odoo_ats_validator/ats_validator /ruta/a/tus/addons/
   ```

3. Agrega la ruta a `addons_path` en tu `odoo.conf` si aún no está incluida.

4. Reinicia el servidor Odoo:

   ```bash
   ./odoo-bin -c odoo.conf
   ```

5. Ve a **Ajustes › Activar modo desarrollador › Actualizar lista de aplicaciones**.

6. Busca **ATS Validator** e instálalo.

---

## Configuración

Ve a **Ajustes › sección "Validador ATS"** y establece la URL del microservicio:

| Campo | Valor por defecto | Descripción |
|-------|-------------------|-------------|
| URL del servidor validador | `http://localhost:8080` | Dirección completa del microservicio ATS |

El valor se guarda como parámetro del sistema (`ats_validator.server_url`) y aplica globalmente.

**Ejemplo si el servicio corre en otro servidor:**

```
http://192.168.1.100:8080
```

---

## Uso paso a paso

### 1. Acceder al módulo

Ve a **Contabilidad › Reportes › Validaciones ATS**.

### 2. Crear una validación

1. Haz clic en **Nuevo**.
2. En el campo **Archivo XML**, sube el archivo `.xml` del ATS generado por tu módulo de localización.
3. Haz clic en **Validar XML**.

### 3. Interpretar los resultados

El módulo muestra el resultado en la misma pantalla:

| Estado | Color | Descripción |
|--------|-------|-------------|
| **Válido** | Verde | El XML pasa validación XSD y todas las reglas de negocio del SRI. Se muestra el talón resumen. |
| **Inválido** | Rojo | Hay errores que impiden la validez. Se detallan los errores XSD y/o de negocio. |

#### Sección de errores XSD

Errores de estructura del XML contra el esquema oficial `at.xsd` del SRI. Indican que el XML no cumple el formato requerido.

#### Sección de errores de reglas de negocio

Errores de contenido según las reglas del DIMM (e.g., códigos de retención inválidos, porcentajes incorrectos, RUCs no válidos). El XML tiene estructura correcta pero datos inválidos.

#### Sección de advertencias

Avisos que no bloquean la validez pero que conviene revisar antes de presentar el ATS al SRI.

#### Talón Resumen

Cuando el XML es válido, se renderiza directamente en Odoo el talón HTML oficial generado por el servicio. Es autocontenido (CSS y logo embebidos) y puede guardarse como `.html` para presentarlo.

### 4. Re-validar o reiniciar

- **Re-validar**: vuelve a enviar el mismo XML al servicio (útil si corregiste el archivo).
- **Reiniciar**: limpia los resultados y vuelve al estado borrador para subir un nuevo XML.

---

## Flujo de validación

```
Usuario sube XML
      │
      ▼
POST /api/ats/validar  ──── error de conexión ──► Mensaje de error en pantalla
      │
      ▼
Respuesta JSON del servicio
      │
      ├── valido: true  ──► Estado = Válido
      │                     Talón HTML visible en pantalla
      │
      └── valido: false ──► Estado = Inválido
                            Errores XSD y/o de negocio visibles
                            Advertencias si las hay
```

---

## Permisos

| Grupo Odoo | Leer | Crear | Editar | Eliminar |
|------------|------|-------|--------|----------|
| Contabilidad / Usuario | ✓ | ✓ | ✓ | — |
| Contabilidad / Administrador | ✓ | ✓ | ✓ | ✓ |

---

## Estructura del módulo

```
ats_validator/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── ats_validation.py        # Modelo principal + llamada HTTP al servicio
│   └── res_config_settings.py  # Campo URL configurable en Ajustes
├── views/
│   ├── ats_validation_views.xml       # Vistas list y form
│   ├── res_config_settings_views.xml  # Bloque en Ajustes generales
│   └── menu.xml                       # Contabilidad > Reportes > Validaciones ATS
├── security/
│   └── ir.model.access.csv      # Permisos por rol contable
├── data/
│   └── sequences.xml            # Secuencia ATS/YYYY/NNNN
└── README.md
```

---

## API del microservicio (referencia técnica)

El módulo consume únicamente este endpoint:

```
POST {url}/api/ats/validar
Content-Type: application/xml

[cuerpo: contenido completo del XML del ATS]
```

Respuesta:

```json
{
  "valido": false,
  "erroresXsd": [],
  "errores": [
    "El CONCEPTO RETENCIÓN EN LA FUENTE reportado [501] no es válido para tipo de pago."
  ],
  "advertencias": [],
  "talonHtml": null
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `valido` | boolean | `true` solo si no hay errores XSD ni de negocio |
| `erroresXsd` | array | Errores de estructura contra el esquema `at.xsd` |
| `errores` | array | Errores de reglas de negocio del SRI |
| `advertencias` | array | Advertencias (no bloquean la validez) |
| `talonHtml` | string / null | HTML del talón resumen; presente solo cuando `valido: true` |

---

## Preguntas frecuentes

**¿El módulo funciona sin el microservicio?**
No. El microservicio es el motor de validación. Sin él, el botón "Validar XML" mostrará un error de conexión.

**¿El módulo genera el XML del ATS?**
No. La generación del XML corresponde al módulo de localización ecuatoriana (`l10n_ec` u otro). Este módulo solo valida el XML generado.

**¿Puedo usar un servicio en un servidor remoto?**
Sí. Configura la URL completa en Ajustes (e.g., `http://mi-servidor.com:8080`).

**¿Los datos del XML se almacenan en Odoo?**
El archivo XML se adjunta al registro de validación en la base de datos de Odoo. Los resultados (errores, talón) también se guardan en el registro.

---

## Licencia

[LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html) — libre para usar, modificar y distribuir, incluyendo en instancias Odoo Enterprise.
