{
    "name": "Hospital Management SystemV3",
    "author": "NLS V3",
    "category_id": "Hospital",
    "license": "AGPL-3",
    "summary": "Hospital Management System",
    "version": "18.0.1.0.0",
    "depends": [
        'mail',
        'base',
        'account'

                ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/patient_views.xml",
        "views/patient_readonly_views.xml",
        "views/appointment_views.xml",
        "views/appointment_line_views.xml",
        "views/patient_tag_views.xml",
        "views/menu.xml",

    ]
}