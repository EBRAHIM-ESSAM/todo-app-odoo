# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class TodoManagement(models.Model):
    _name = 'todo.task'
    _description = 'todo_app.todo_app'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char()
    assign_id = fields.Many2one('res.partner')
    description = fields.Text()
    due_date = fields.Date()
    estimated_time = fields.Float(string='Estimated time')
    total_hours = fields.Float(compute='_computed_total_hours')
    line_ids = fields.One2many('todo.line','todo_id')
    active = fields.Boolean(default=True)
    is_late = fields.Boolean()
    state = fields.Selection([
        ('new', 'New'),
        ('inProgress', 'In progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),],sdefault='new')
    @api.depends('line_ids','estimated_time','line_ids.hours')
    def _computed_total_hours(self):
        for rec in self:
            rec.total_hours = 0.0
            if rec.line_ids :
                for line in rec.line_ids:
                    rec.total_hours += line.hours
                    if rec.total_hours > rec.estimated_time:
                        raise ValidationError(_('The Total timesheet hours (%s) exceed the estimated time(%s)' % (rec.total_hours, rec.estimated_time)))



    def check_due_date(self):
        todo_task_ids = self.search([])
        for rec in todo_task_ids:
            if rec.due_date and fields.Date.today() > rec.due_date and rec.state in ['new' ,'inProgress']:
                rec.is_late = True



    def action_progress(self):
        for item in self:
            item.state = 'inProgress'

    def action_completed(self):
        for item in self:
            item.state = 'completed'

    def action_new(self):
        for item in self:
            item.state = 'new'

    def action_closed(self):
        for item in self:
            item.state = 'closed'


class TodoLine(models.Model):
    _name = 'todo.line'

    date = fields.Date()
    description = fields.Char()
    hours = fields.Float()
    todo_id = fields.Many2one('todo.task')
