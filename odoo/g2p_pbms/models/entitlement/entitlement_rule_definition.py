from odoo import models, fields, api

import logging
import json
from odoo.addons.g2p_registry_type_addon.models import G2PRegistryType, G2PTargetModelMapping

_logger = logging.getLogger(__name__)

class G2PEntitlementRuleDefinition(models.Model):
    _name = "g2p.entitlement.rule.definition"
    _description = "G2P Program Entitlement Rule Definition"
    _rec_name = "mnemonic"

    mnemonic = fields.Char(string="Rule Mnemonic", required=True)
    description = fields.Char(string="Description")
    program_id = fields.Many2one("g2p.program.definition", string="G2P Program")
    benefit_code_id = fields.Many2one(
        'g2p.benefit.codes',
        string="Benefit Code",
        help="Select a benefit code defined in the selected program."
    )
    decimal_places = fields.Integer(
        string="Decimal Places",
        related="benefit_code_id.decimal_places",
        readonly=True,
        store=True,
    )
    measurement_unit = fields.Char(
        string="Measurement Unit",
        related="benefit_code_id.measurement_unit",
        readonly=True,
    )
    quantity = fields.Float(string="Quantity", required=True)
    multiplier = fields.Char(
        string="Multiplier",
        help="Select an integer field from the registry to use as a multiplier."
    )
    target_registry = fields.Selection(
        selection=G2PRegistryType.selection(), string="Target Registry", required=True
    )
    pbms_domain = fields.Char(string="Domain", required=True)
    allowed_benefit_code_ids = fields.Many2many(
        'g2p.benefit.codes', related='program_id.benefit_code_ids', store=False
    )
    allowed_multipliers = fields.Char(compute='_compute_multiplier_options', store=False)

    @api.model
    def create(self, vals):
        multiplier_value = vals.get('multiplier')
        _logger.info("Multiplier in create: %s", multiplier_value)
        _logger.info("all VALS: %s", vals)

        # Add custom logic here
        return super().create(vals)
    
    @api.depends("target_registry")
    def _compute_multiplier_options(self):
        NUMERIC_FIELD_TYPES = {'integer', 'float', 'double', 'monetary', 'numeric', 'biginteger', 'smallinteger', 'decimal'}
        for rec in self:
            registry_type = rec.target_registry
            
            model_name = G2PTargetModelMapping.get_target_model_name(registry_type)
            if not model_name:
                rec.allowed_multipliers = "[]"
                continue

            model = self.env[model_name]
            numeric_fields = [
                (name, field.string or name)
                for name, field in model._fields.items()
                if field.type in NUMERIC_FIELD_TYPES and name != "id"
            ]
            rec.allowed_multipliers = json.dumps(numeric_fields)

    def action_open_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "View Entitlement Rule Details",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "flags": {"mode": "readonly"},
            "views": [[False, "form"]],
            "context": dict(self._context, default_no_create=True, no_create=True, create=False),

        }

