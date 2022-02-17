# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Administrator(models.Model):
    _name = 'tickets_fhoi.administrator'
    _description = 'Generates queues'
    _rec_name = 'doctor_name'

    doctor_name = fields.Char(
        string='Doctor',
        help="Type doctor's name",
        required=True)

    prefix_ticket = fields.Char(
        string='Identifier',
        help='Identify tickets-2 char',
        size=2,
        required=True)

    current_ticket = fields.Char(
        string="Current Ticket",
        default="No asignado",
        required=True,
        translate=True
        )

    tickets_ids = fields.One2many(
        comodel_name='tickets_fhoi.tickets',
        inverse_name='doctor_id',
        string='Tickets')

    tickets_waiting = fields.Integer(
        string="Waiting",
        default=0)

    tickets_called = fields.Integer(
        string="Called",
        default=0)

    tickets_total = fields.Integer(
        string="Total",
        default=0)

    # unique identifier
    _sql_constraints = [
        ('prefix_ticket_unique', 'UNIQUE(prefix_ticket)', 'A doctor must have a unique identifier'),
        ('doctor_name_unique', 'UNIQUE(doctor_name)', 'Doctors cannot have the same name')
    ]

    # update values after creating them
    def write(self, values):

        if 'doctor_name' in values.keys():
            values['doctor_name'] = values.get('doctor_name').upper()
            
        if 'prefix_ticket' in values.keys():
            values['prefix_ticket'] = values.get('prefix_ticket').upper()
        
        return super(Administrator, self).write(values)
    
    # modify values when creating them. Uppercase values
    @api.model
    def create(self, values):
        res = super(Administrator, self).create(values)
        for value in res:
            value.doctor_name = value.doctor_name.upper()
            value.prefix_ticket = value.prefix_ticket.upper()
        return res

    # automated action: archive values in tickets_fhoi_archived_data
    def archived_queue(self):
        recs = self.env["tickets_fhoi.administrator"].sudo().search([])
        queues = []
        for rec in recs:
            
            name = rec.doctor_name
            waiting = rec.tickets_waiting
            called = rec.tickets_called
            total = rec.tickets_total

            data = {
                'name': name,
                'waiting': waiting,
                'called': called,
                'total': total
            }

            queues.append(data)

        archive = self.env["tickets_fhoi.archived_data"]
        
        #inserting values to archived_data table
        archive.sudo().create(queues)
            
    

class Tickets(models.Model):
    _name = 'tickets_fhoi.tickets'
    _description = 'Generate tickets'
    _rec_name = 'ticket_code'
    _order = 'ticket_code'

    ticket_code = fields.Char(
        string='Ticket',
        default='Nuevo',
        compute='_get_ticket',
        required=True,
        store=True,
        readonly=True,
        translate=True)

    ticket_status = fields.Selection(
        string='Status',
        selection=[('c','called'),('w','waiting')],
        required=True,
        default='w')

    doctor_id = fields.Many2one(
        comodel_name='tickets_fhoi.administrator',
        string='Doctor',
        ondelete='cascade',
        required=True,
        default=1)

    called_date = fields.Datetime(
        string="Call Date")


    def check_stored_tickets(self, doctor):
        records = self.search([('doctor_id.doctor_name', '=', doctor)], count=True)
        if not records:
            return records
        elif records == 1:
            return records
        else:
            last_record = self.search([('doctor_id.doctor_name', '=', doctor)])
            # print(last_record)
            last_record = self.search([('doctor_id.doctor_name', '=', doctor)], limit=2, order='id desc')
            records = last_record[1].ticket_code
            # print(records+' last record')
            records = (int(records[2:])) + 1
            # print(f'sliced {records}')
            # print(self.env['res.users'].browse(self.env.user.id).name)
            return records

    def update_queue(self):
        for record in self:

            doctor = self.doctor_id.id
            total = record.search([('doctor_id.id','=', doctor)], count=True)
            waiting = record.search([('doctor_id.id','=', doctor), ('ticket_status', '=', 'w')], count=True)
            called = total - waiting

            record.doctor_id.write({
            'tickets_waiting': waiting,
            'tickets_called': called,
            'tickets_total': total
            })      
    
    @api.depends('doctor_id')
    def _get_ticket(self):
        # print(self.doctor_id.id) #it gives id. ie: 1, 2, 3 ...
        prefix = self.doctor_id.prefix_ticket #it gives the prefix depending on doctor_id. ie: AT, BT
        doctor = self.doctor_id.doctor_name
        records = self.check_stored_tickets(doctor)
        sequence = ''
        records -= 1
        

        if records < 0:
            records += 2
            sequence = f'{prefix}00{records}'
            self.ticket_code = sequence
            self.update_queue()
        else:
            records += 1
            record_str = str(records)
            if len(record_str) == 1:
                sequence = f'{prefix}00{records}'
            elif len(record_str) == 2:
                    sequence = f'{prefix}0{records}'
            else:
                sequence = f'{prefix}{records}'
            
            self.ticket_code = sequence
            self.update_queue()    


    def print_ticket(self):
        self.update_queue()
        report= self.sudo().env.ref('tickets_fhoi.report_print_ticket').report_action(self)
        return report