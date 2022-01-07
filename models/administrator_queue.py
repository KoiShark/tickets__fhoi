# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class tickets__fhoi(models.Model):
#     _name = 'tickets__fhoi.tickets__fhoi'
#     _description = 'tickets__fhoi.tickets__fhoi'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Administrator_queue(models.Model):
    _name = 'administrator.queue'
    _description = 'Genera colas de doctores'

    doctor = fields.Char(string='Doctor', default='Ingresa nombre del doctor')
    