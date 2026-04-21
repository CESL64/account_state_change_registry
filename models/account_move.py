from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    state_change_registry_ids = fields.One2many(
        comodel_name="state.change.registry",
        inverse_name="invoice_id",
        string="Registros de Cambio de Estado",
    )

    def write(self, vals):
        track_state = "state" in vals
        previous_states = {move.id: move.state for move in self} if track_state else {}

        res = super().write(vals)
        if not track_state:
            return res

        registry_model = self.env["state.change.registry"]

        for move in self:
            if move.partner_id.not_registry_change:
                continue

            previous_state = previous_states.get(move.id)
            new_state = move.state
            if previous_state == new_state:
                continue

            change_dt = fields.Datetime.now()
            change_dt_text = fields.Datetime.to_string(change_dt)
            move.message_post(
                body=f"Registro de estado actualizado en {change_dt_text}",
            )

            taxes = move.invoice_line_ids.mapped("tax_ids").mapped("name")
            registry_model.create(
                {
                    "name": move.payment_reference or move.name or move.display_name or str(move.id),
                    "document_type": "invoice",
                    "invoice_id": move.id,
                    "amount": move.amount_total,
                    "line_count": len(move.invoice_line_ids),
                    "tax_summary": ", ".join(sorted(set(taxes))),
                    "company_id": move.company_id.id,
                    "previous_state": previous_state,
                    "new_state": new_state,
                    "change_date": change_dt,
                    "user_id": self.env.user.id,
                }
            )

        return res
