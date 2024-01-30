from odoo import fields, models


class EstatePropertiesTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real-Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_type_name_tag',
         'UNIQUE(name)',
         'A property property tag name must be unique'),
    ]