from odoo import models, fields, api

from odoo.addons.g2p_registry_type_addon.models import G2PRegistryType

class G2PPriorityRuleDefinition(models.Model):
    _name = "g2p.priority.rule.definition"
    _description = "G2P Priority Rule Definition"
    _rec_name = "mnemonic"

    mnemonic = fields.Char(string="Rule Mnemonic", required=True)
    description = fields.Char(string="Description")
    disbursement_cycle_id = fields.Many2one("g2p.disbursement.cycle", string="Disbursement Cycle")
    program_id = fields.Integer(related="disbursement_cycle_id.program_id.id", string="Program ID", readonly=True)
    target_registry = fields.Selection(
        selection=G2PRegistryType.selection(), string="Registry Type", required=True
    )
    pbms_domain = fields.Char(string="Domain", required=True)

    @api.model
    def default_get(self, fields):
        """Override to change default modal title from 'Create Priority Rule' to 'Disbursement Rule'."""
        res = super(G2PPriorityRuleDefinition, self).default_get(fields)
        self = self.with_context(default_name="Create Disbursement Rule")
        return res

    def action_open_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "View Disbursement Rule Details",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
            "flags": {"mode": "readonly"},
            "views": [[False, "form"]],
            "context": dict(self._context, default_no_create=True, no_create=True, create=False),

        }

