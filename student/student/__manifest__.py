# -*- coding: utf-8 -*-
{
    'name': "student list",
    "author": "NLS V1",
    "category_id": "Student List",
    "license": "AGPL-3",
    "summary": "Student Management System",
    "version": "18.0.1.0.0",

    # any module necessary for this one to work correctly
    'depends': [
        'mail',
        'base'
    ],

    # always loaded
    "data": [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/school_views.xml',
        'views/hobby_views.xml',
        'views/menu.xml',

    ]

}

