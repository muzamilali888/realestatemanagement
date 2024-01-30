from odoo import fields, models
from odoo.exceptions import ValidationError


class EstatePropertiesType(models.Model):
    _name = "estate.property.type"
    _description = "Model for Real-Estate Property Type"

    name = fields.Char(required=True)
