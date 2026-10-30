from odoo import models, fields, api

from odoo.addons.g2p_registry_type_addon.models import G2PRegistryType


class G2PEligibilityRuleDefinition(models.Model):
    _name = "g2p.eligibility.rule.definition"
    _description = "G2P Program Eligibility Rule Definition"
    _rec_name = "mnemonic"

    mnemonic = fields.Char(string="Rule Mnemonic", required=True)
    rule_number = fields.Integer(
        string="Rule Number",
        required=True,
        default=lambda self: self._get_default_rule_number(),
        store=True,
    )
    description = fields.Char(string="Description")
    program_id = fields.Many2one("g2p.program.definition", string="G2P Program")
    target_registry = fields.Selection(
        selection=G2PRegistryType.selection(), string="Target Registry", required=True
    )
    set_operator = fields.Selection(
        selection=[
            ('NONE', 'NONE'),
            ('INTERSECT', 'INTERSECT'),
            ('EXCEPT', 'EXCEPT'),
            ('UNION', 'UNION'),
        ],
        string="Set Operator",
        default='NONE',
        store=True,
        required=True
    )
    pbms_domain = fields.Char(string="Domain", required=True)

    _sql_constraints = [
        ('rule_number_program_id_unique', 'unique(rule_number, program_id)', 'Rule Number must be unique per Program.')
    ]


    @api.model
    def _get_default_rule_number(self):
        program_id = self.env.context.get('default_program_id')
        last = self.search([('program_id', '=', program_id)], order='rule_number desc', limit=1)
        return last.rule_number + 1 if last else 1

    def action_open_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "View Eligibility Rule Details",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "flags": {"mode": "readonly"},
            "views": [[False, "form"]],
            "context": dict(self._context, default_no_create=True, no_create=True, create=False),
        }
