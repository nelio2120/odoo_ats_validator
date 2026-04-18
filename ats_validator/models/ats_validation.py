import base64
import json
import logging

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AtsValidation(models.Model):
    _name = 'ats.validation'
    _description = 'Validación ATS'
    _order = 'create_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Referencia',
        required=True,
        default=lambda self: _('Nuevo'),
        copy=False,
    )
    xml_file = fields.Binary(
        string='Archivo XML',
        attachment=True,
    )
    xml_filename = fields.Char(string='Nombre del archivo')
    server_url = fields.Char(
        string='URL del servidor',
        compute='_compute_server_url',
        store=False,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('valid', 'Válido'),
            ('invalid', 'Inválido'),
        ],
        string='Estado',
        default='draft',
        readonly=True,
        copy=False,
    )
    is_valid = fields.Boolean(string='¿Válido?', readonly=True, copy=False)
    errors_xsd = fields.Text(string='Errores XSD (raw)', readonly=True, copy=False)
    errors = fields.Text(string='Errores de negocio (raw)', readonly=True, copy=False)
    warnings = fields.Text(string='Advertencias (raw)', readonly=True, copy=False)
    talon_html = fields.Html(
        string='Talón Resumen',
        readonly=True,
        copy=False,
        sanitize=False,
    )
    errors_xsd_display = fields.Html(
        string='Errores XSD',
        compute='_compute_display_fields',
        readonly=True,
    )
    errors_display = fields.Html(
        string='Errores de negocio',
        compute='_compute_display_fields',
        readonly=True,
    )
    warnings_display = fields.Html(
        string='Advertencias',
        compute='_compute_display_fields',
        readonly=True,
    )
    has_errors_xsd = fields.Boolean(compute='_compute_display_fields')
    has_errors = fields.Boolean(compute='_compute_display_fields')
    has_warnings = fields.Boolean(compute='_compute_display_fields')

    @api.depends_context('company')
    def _compute_server_url(self):
        url = self.env['ir.config_parameter'].sudo().get_param(
            'ats_validator.server_url', 'http://localhost:8080'
        )
        for rec in self:
            rec.server_url = url

    def _items_to_html(self, raw_json):
        """Convierte un JSON array de strings a lista HTML."""
        if not raw_json:
            return ''
        try:
            items = json.loads(raw_json)
        except (json.JSONDecodeError, TypeError):
            items = [raw_json]
        if not items:
            return ''
        li = ''.join(f'<li>{item}</li>' for item in items)
        return f'<ul style="margin:0;padding-left:1.2em">{li}</ul>'

    @api.depends('errors_xsd', 'errors', 'warnings')
    def _compute_display_fields(self):
        for rec in self:
            xsd = json.loads(rec.errors_xsd or '[]')
            err = json.loads(rec.errors or '[]')
            warn = json.loads(rec.warnings or '[]')
            rec.has_errors_xsd = bool(xsd)
            rec.has_errors = bool(err)
            rec.has_warnings = bool(warn)
            rec.errors_xsd_display = rec._items_to_html(rec.errors_xsd)
            rec.errors_display = rec._items_to_html(rec.errors)
            rec.warnings_display = rec._items_to_html(rec.warnings)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nuevo')) == _('Nuevo'):
                vals['name'] = self.env['ir.sequence'].next_by_code('ats.validation') or _('Nuevo')
        return super().create(vals_list)

    def action_validar(self):
        self.ensure_one()
        if not self.xml_file:
            raise UserError(_('Debe adjuntar un archivo XML antes de validar.'))

        url = self.env['ir.config_parameter'].sudo().get_param(
            'ats_validator.server_url', 'http://localhost:8080'
        ).rstrip('/')
        endpoint = f'{url}/api/ats/validar'

        xml_bytes = base64.b64decode(self.xml_file)

        try:
            response = requests.post(
                endpoint,
                data=xml_bytes,
                headers={'Content-Type': 'application/xml'},
                timeout=60,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise UserError(
                _('No se pudo conectar al servidor ATS en %s.\n'
                  'Verifique que el servicio esté activo.') % url
            )
        except requests.exceptions.Timeout:
            raise UserError(_('El servidor ATS no respondió en el tiempo límite (60 s).'))
        except requests.exceptions.HTTPError as exc:
            raise UserError(_('El servidor ATS respondió con error: %s') % str(exc))

        try:
            result = response.json()
        except Exception:
            raise UserError(_('La respuesta del servidor no es un JSON válido.'))

        is_valid = result.get('valido', False)
        self.write({
            'is_valid': is_valid,
            'state': 'valid' if is_valid else 'invalid',
            'errors_xsd': json.dumps(result.get('erroresXsd') or []),
            'errors': json.dumps(result.get('errores') or []),
            'warnings': json.dumps(result.get('advertencias') or []),
            'talon_html': result.get('talonHtml') or False,
        })

    def action_reset(self):
        self.ensure_one()
        self.write({
            'state': 'draft',
            'is_valid': False,
            'errors_xsd': False,
            'errors': False,
            'warnings': False,
            'talon_html': False,
        })
