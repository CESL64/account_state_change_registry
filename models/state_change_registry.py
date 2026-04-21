from odoo import fields, models


class StateChangeRegistry(models.Model):
    _inherit = "state.change.registry"

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Factura",
    )
