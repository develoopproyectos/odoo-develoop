# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Dev_pc_ProjectTechnolgyCustom(models.Model):
    
    _name = "project.technology"
    _description = "List of technology"

    sequence = fields.Integer(default=1)
    name = fields.Char("Name")
    project_id = fields.Many2one('project.project', string="Project")
    