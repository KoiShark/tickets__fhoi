# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ArchivedData(models.Model):
    _name = 'tickets_fhoi.archived_data'
    _description = 'Data saved from Queues'
    _order = 'data_date'

    data_date = fields.Date(
        string='Date',
        required=True,
        default=fields.date.today())

    name = fields.Char(
        string='Name')

    called = fields.Integer(
        string='Called',
        default=0)

    waiting = fields.Integer(
        string='Waiting',
        default=0)

    total = fields.Integer(
        string='Total',
        default=0)