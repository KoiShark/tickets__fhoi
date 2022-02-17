# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DoctorTicket(models.Model):
    _name = 'tickets_fhoi.tickets'
    _inherit = 'tickets_fhoi.tickets'
    
    # getting filtered records for doctor's view
    def get_filtered_record(self):
        view_id_kanban = self.sudo().env['ir.ui.view'].search([('name', '=', 'tickets_fhoi.tickets.doctor.view.kanban')])

        user = self.sudo().env['res.users'].browse(self.env.user.id)
        user_name = user.name.upper()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Doctor',
            'res_model': 'tickets_fhoi.tickets',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'view_id': view_id_kanban.id ,
            'target': 'current',
            'domain': [('doctor_id.doctor_name', '=', user_name), ('ticket_status','=','w')]
        }

    # updates the doctor's view after calling a ticket
    def update_current_ticket(self):
        for record in self:
            time =fields.datetime.now() 
            
            # updates the ticket's status
            record.write({
                'ticket_status': 'c',
                'called_date': time })
            
            # updates the current ticket in the administrator queue 
            record.doctor_id.write({'current_ticket': record.ticket_code})

        self.update_queue()
        reload_now = self.get_filtered_record()
        return reload_now
    
    # automatic action: deleting tickets after working hours
    def delete_tickets(self):
        tickets = self.env["tickets_fhoi.tickets"].sudo().search([('ticket_status', '=', 'c')])
        tickets.sudo().unlink()
        
        # updating queues info
        queues = self.env["tickets_fhoi.administrator"].sudo().search([])

        for value in queues:
            doctor = value.id
            available_tickets = self.env["tickets_fhoi.tickets"].sudo().search([('doctor_id', '=', doctor)], count=True)
            waiting = self.env["tickets_fhoi.tickets"].sudo().search([('doctor_id', '=', doctor), ('ticket_status', '=', 'w')], count=True)
            called = available_tickets - waiting

            value.write({
                'tickets_waiting': waiting,
                'tickets_called': called,
                'tickets_total': available_tickets
            })