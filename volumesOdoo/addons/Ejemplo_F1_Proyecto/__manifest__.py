{
    'name': 'Proyecto F1', # Nombre público del módulo.
    'version': '1.0', # Versión actual de tu desarrollo.
    'summary': 'Gestión del Campeonato Mundial de Fórmula 1', # Subtítulo descriptivo.
    'description': 'Módulo para gestionar escuderías, pilotos, carreras y clasificación.', # Descripción larga.
    'author': 'David Gómez Delicado', # Autor del módulo.
    'depends': ['base'], # Módulos de los que depende. Odoo necesita 'base' como mínimo.
    'data': [
        # Archivos que Odoo cargará al instalar. EL ORDEN ES VITAL:
        # Primero siempre la seguridad, luego las vistas y reportes.
        'security/ir.model.access.csv',
        'views/piloto_views.xml',
        'views/escuderia_views.xml',
        'views/carrera_views.xml',
        'views/clasificacion_views.xml',
        'wizard/add_piloto_wizard_view.xml',
        'views/menu_views.xml',
        'reports/report.xml',
    ],
    'installable': True, # Permite que el módulo aparezca para instalarse.
    'application': True, # Lo marca como una aplicación principal, no como una simple herramienta extra.
}