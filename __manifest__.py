# -*- coding: utf-8 -*-
{
    'name': "dara_mallas",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dirección de Asuntos Regulatorios",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/mallas_security.xml',
        'security/ir.model.access.csv',
        'views/udla_menu.xml',
        'views/views.xml',
        'views/templates.xml',
        'models/subjects/views/subject.xml',
        'models/subjects/views/subject_inherit.xml',
        'models/subjects/views/subject_scacrse.xml',
        'models/subjects/views/subject_scadtl.xml',
        'models/subjects/views/subject_prerequisite.xml',
        'models/subjects/views/subject_elective.xml',
        'models/subjects/views/subject_itinerary.xml',
        'models/subjects/views/subject_corequisite.xml',
        'models/subjects/views/subject_grade.xml',
        'models/subjects/views/subject_grade_mode.xml',
        'models/subjects/views/subject_attributes.xml',
        'models/subjects/views/subject_rule.xml',
        'models/subjects/views/subject_department.xml',
        'models/subjects/views/subject_schedule_class.xml',
        'models/subjects/views/subject_inherit_homologation.xml',
        'models/program/views/program.xml',
        'models/program/views/specialization_views.xml',
        'models/areas/views/area.xml',
        'models/areas/views/area_homologation.xml',
        'models/period/views/period.xml',
        'models/college/views/college.xml',
        'models/study_plan/views/study_plan.xml',
        'models/study_plan/views/study_plan_line.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}