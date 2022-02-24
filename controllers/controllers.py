# -*- coding: utf-8 -*-
from odoo import http

# class TicketsFhoi(http.Controller):
    
#     @http.route('/tickets__fhoi/tickets__fhoi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tickets__fhoi/tickets__fhoi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tickets__fhoi.listing', {
#             'root': '/tickets__fhoi/tickets__fhoi',
#             'objects': http.request.env['tickets__fhoi.tickets__fhoi'].search([]),
#         })

#     @http.route('/tickets__fhoi/tickets__fhoi/objects/<model("tickets__fhoi.tickets__fhoi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tickets__fhoi.object', {
#              'object': obj
#         })

