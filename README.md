# Account State Change Registry

## Overview
`account_state_change_registry` extends the base module `state_change_registry` to cover **customer invoices and vendor bills managed through `account.move`**.

Its purpose is to automatically capture state transitions on accounting documents and provide a complete operational trace through logs, chatter integration, reports, wizards, and email notifications.

## Main Features
- 🧾 Inherits `account.move` and tracks changes in the `state` field
- 📝 Creates a `state.change.registry` record every time an invoice state changes
- 💬 Posts a message in the invoice chatter when a state transition occurs
- 🔗 Links each log to its source invoice through `invoice_id`
- 📂 Adds a notebook page on the invoice form to display related state change records
- 📄 Adds reporting capabilities:
  - dedicated QWeb report for invoice state-change logs
  - inherited invoice report section with the same tracking table
- ✉️ Implements email notification logic for invoice-related state changes
- ✅ Marks `mail_sent` when the notification process is completed
- 🧮 Includes a reporting wizard by date range and company

## Email Notification Flow
This module inherits the public hook `send_state_change_notification()` from the base module and specializes it for invoices.

Current behavior:
- only sends notifications for records with `document_type = 'invoice'`
- uses `invoice_id` as the source document
- sends notifications to followers of the invoice
- leaves traceability in:
  - the invoice chatter
  - the `state.change.registry` chatter

## User Interface Enhancements
- Invoice form extension with a **State Change Records** tab
- Read-only list of related logs
- Notification button per line for manual email dispatch
- Reporting wizard available from the Finance reports menu

## Reports
- 📊 Invoice-specific state change report
- 📥 Inherited section inside `account.report_invoice_document`
- Designed to present tracking information clearly to accounting users and auditors

## Dependencies
- `account`
- `state_change_registry`

## Value Provided
This module strengthens accounting control by combining:
- automatic audit logging
- operational visibility
- communication traceability
- management reporting

It is especially useful in environments where invoice lifecycle control and accountability are critical.
