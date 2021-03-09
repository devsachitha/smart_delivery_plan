# -*- coding: utf-8 -*-
{
    'name': "Delivery Plan",

    'summary': """
       Smart Trading Asia Pending Delivery Plan & Next Day Delivery Plan """,

    'description': """
       Smart Trading Asia Pending Delivery Plan & Next Day Delivery Plan
    """,

    'author': "Codeso",
    'website': "https://codeso.lk",
    'license':'Other proprietary',
    'category': 'Employees',
    'version': '1.0.0',
    'depends': ['sale'],
    'data': [
        'views/delivery_plan.xml',
        'views/next_day_delivery_plan.xml',
        'reports/report.xml'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}