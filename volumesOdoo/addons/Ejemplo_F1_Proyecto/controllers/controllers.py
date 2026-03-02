from odoo import http
from odoo.http import request
import json

class F1Controller(http.Controller):

    @http.route('/f1/pilotos', auth='public', type='http', methods=['GET'])
    def get_pilotos(self, **kw):
        pilotos = request.env['f1.piloto'].sudo().search([])
        data = []
        for p in pilotos:
            data.append({
                'nombre': f"{p.name} {p.apellido}",
                'escuderia': p.escuderia_id.name if p.escuderia_id else "Sin equipo",
                'puntos': p.puntos_totales
            })
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )