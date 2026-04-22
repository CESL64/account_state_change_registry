from odoo import fields, models
from odoo.exceptions import UserError


class StateChangeRegistry(models.Model):
    _inherit = "state.change.registry"

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Factura",
    )

    def send_state_change_notification(self):
        self.ensure_one()
        result = super().send_state_change_notification()

        # En este modulo solo notificamos cambios de facturas.
        if self.document_type != "invoice":
            return result

        if not self.invoice_id:
            raise UserError("Este registro no esta ligado a una factura.")

        partners_to_notify = self.invoice_id.message_partner_ids.filtered("email")
        if not partners_to_notify:
            raise UserError(
                "La factura no tiene seguidores con correo electronico para notificar."
            )

        template = self.env.ref(
            "account_state_change_registry.mail_template_invoice_state_change_notification"
        )
        email_values = {
            "email_to": ",".join(partners_to_notify.mapped("email")),
            "recipient_ids": [(6, 0, partners_to_notify.ids)],
            "email_from": self.env.user.email_formatted or self.env.company.email,
        }
        template.send_mail(
            self.id,
            force_send=True,
            email_values=email_values,
        )

        self.invoice_id.message_post(
            body=(
                "Se envio notificacion por correo para el cambio de estado "
                f"'{self.previous_state or ''}' -> '{self.new_state or ''}'."
            ),
            partner_ids=partners_to_notify.ids,
            subtype_xmlid="mail.mt_note",
        )

        self.mail_sent = True
        return result
