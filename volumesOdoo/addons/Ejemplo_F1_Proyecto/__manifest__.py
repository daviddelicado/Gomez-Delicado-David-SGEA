{
    'name': 'Campeonato F1 Manager',
    'version': '1.0',
    'summary': 'Gestión del Campeonato Mundial de Fórmula 1',
    'description': 'Módulo para gestionar escuderías, pilotos, carreras y clasificación.',
    'author': 'Estudiante DAW',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/escuderia_views.xml',
        'views/piloto_views.xml',
        'views/carrera_views.xml',
        'views/clasificacion_views.xml',
        'wizard/add_piloto_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}