import base64
from unittest.mock import MagicMock, patch

import requests

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestAtsValidation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.record = self.env['ats.validation'].create({
            'xml_file': base64.b64encode(b'<ats></ats>'),
            'xml_filename': 'ats.xml',
        })

    def test_action_validar_requires_xml_file(self):
        record = self.env['ats.validation'].create({})
        with self.assertRaises(UserError):
            record.action_validar()

    @patch('odoo.addons.ats_validator.models.ats_validation.requests.post')
    def test_action_validar_valid_response(self, mock_post):
        mock_post.return_value = MagicMock(
            json=lambda: {'valido': True, 'talonHtml': '<p>ok</p>'},
        )
        self.record.action_validar()
        self.assertEqual(self.record.state, 'valid')
        self.assertTrue(self.record.is_valid)
        self.assertEqual(self.record.talon_html, '<p>ok</p>')
        self.assertFalse(self.record.errors_xsd)

    @patch('odoo.addons.ats_validator.models.ats_validation.requests.post')
    def test_action_validar_invalid_response(self, mock_post):
        mock_post.return_value = MagicMock(
            json=lambda: {
                'valido': False,
                'erroresXsd': ['campo X requerido'],
                'errores': ['regla de negocio Y'],
                'advertencias': ['posible inconsistencia Z'],
            },
        )
        self.record.action_validar()
        self.assertEqual(self.record.state, 'invalid')
        self.assertFalse(self.record.is_valid)
        self.assertEqual(self.record.errors_xsd, ['campo X requerido'])
        self.assertTrue(self.record.has_errors)
        self.assertIn('regla de negocio Y', self.record.errors_display)

    @patch('odoo.addons.ats_validator.models.ats_validation.requests.post')
    def test_action_validar_connection_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError()
        with self.assertRaises(UserError):
            self.record.action_validar()

    @patch('odoo.addons.ats_validator.models.ats_validation.requests.post')
    def test_action_validar_timeout(self, mock_post):
        mock_post.side_effect = requests.exceptions.Timeout()
        with self.assertRaises(UserError):
            self.record.action_validar()

    @patch('odoo.addons.ats_validator.models.ats_validation.requests.post')
    def test_action_reset_clears_results(self, mock_post):
        mock_post.return_value = MagicMock(
            json=lambda: {'valido': False, 'errores': ['x']},
        )
        self.record.action_validar()
        self.record.action_reset()
        self.assertEqual(self.record.state, 'draft')
        self.assertFalse(self.record.is_valid)
        self.assertFalse(self.record.errors)
        self.assertFalse(self.record.talon_html)
