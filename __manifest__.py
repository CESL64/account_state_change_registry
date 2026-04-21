{
    "name": "Account State Change Registry",
    "version": "18.0.1.0.0",
    "summary": "Registro de cambios de estado para facturas",
    "description": "Hereda account.move para registrar cambios en state.",
    "author": "Prueba Tecnica",
    "license": "LGPL-3",
    "category": "Accounting",
    "depends": [
        "account",
        "state_change_registry",
    ],
    "data": [
        "views/state_change_registry_views.xml",
        "views/account_move_views.xml",
    ],
    "installable": True,
    "application": False,
}
