from odoo import (models, fields, api)
from odoo.exceptions import ValidationError

from datetime import timedelta, datetime


class EstatePropertiesOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Real-Estate Property Tag"
    price = fields.Float('Price')
    status = fields.Selection([('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False, )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    @api.depends("validity", "date_deadline", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            datetime_temp = fields.Datetime.now() + timedelta(days=record.validity)
            record.date_deadline = datetime_temp.date()

    def _inverse_date_deadline(self):
        for record in self:
            temp = record.date_deadline - (record.create_date.date() or datetime.now().date())
            record.validity = temp.days

    _sql_constraints = [
        ('check_offer_price',
         'CHECK(price > 0)',
         'An offer price must be strictly positive'),
    ]
    # Actions for Buttons
    def action_accept_offer(self):
        for record in self:
            property_obj = self.env['estate.property'].search([('id', '=', record.property_id.id)])
            record.status = "Accepted"
            property_obj.buyer_id = record.partner_id
            property_obj.selling_price = record.price

    def action_refuse_offer(self):
        for record in self:
            record.status = "Refused"
