from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ats_validator_url = fields.Char(
        string='URL del Validador ATS',
        config_parameter='ats_validator.server_url',
        default='http://localhost:8080',
        placeholder='http://localhost:8080',
    )
