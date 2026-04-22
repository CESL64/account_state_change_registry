from datetime import datetime, time
from markupsafe import escape

from odoo import fields, models
from odoo.exceptions import ValidationError


class StateChangeRegistryReportWizard(models.TransientModel):
    _name = "state.change.registry.report.wizard"
    _description = "State Change Registry Report Wizard"

    date_start = fields.Date(string="Fecha inicio", required=True)
    date_end = fields.Date(string="Fecha fin", required=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compania",
        required=True,
        default=lambda self: self.env.company,
    )
    result_html = fields.Html(string="Resultado", readonly=True, sanitize=False)

    def action_show_records(self):
        self.ensure_one()
        if self.date_start > self.date_end:
            raise ValidationError("La fecha inicio no puede ser mayor que la fecha fin.")

        start_dt = datetime.combine(self.date_start, time.min)
        end_dt = datetime.combine(self.date_end, time.max)

        domain = [
            ("company_id", "=", self.company_id.id),
            ("change_date", ">=", fields.Datetime.to_string(start_dt)),
            ("change_date", "<=", fields.Datetime.to_string(end_dt)),
            ("document_type", "=", "invoice"),
        ]
        records = self.env["state.change.registry"].search(domain, order="change_date desc")

        rows = []
        for rec in records:
            rows.append(
                f"""
                <tr>
                    <td>{escape(rec.change_date or "")}</td>
                    <td>{escape(rec.name or "")}</td>
                    <td>{escape(rec.user_id.display_name or "")}</td>
                    <td style="text-align:center;">{escape(rec.previous_state or "")}</td>
                    <td style="text-align:center;">{escape(rec.new_state or "")}</td>
                    <td style="text-align:right;">{escape(rec.amount or 0.0)}</td>
                    <td style="text-align:right;">{escape(rec.line_count or 0)}</td>
                </tr>
                """
            )

        if not rows:
            rows.append(
                """
                <tr>
                    <td colspan="7" style="text-align:center;">No se encontraron registros para el criterio seleccionado.</td>
                </tr>
                """
            )

        self.result_html = f"""
            <div class="table-responsive">
                <table class="table table-sm table-bordered table-striped">
                    <thead class="thead-dark">
                        <tr>
                            <th>Fecha</th>
                            <th>Nombre</th>
                            <th>Usuario</th>
                            <th>Estado previo</th>
                            <th>Estado nuevo</th>
                            <th>Monto</th>
                            <th>Cantidad de lineas</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(rows)}
                    </tbody>
                </table>
            </div>
        """

        return {
            "type": "ir.actions.act_window",
            "name": "Reporte de Registros de Cambio de Estado",
            "res_model": "state.change.registry.report.wizard",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }
