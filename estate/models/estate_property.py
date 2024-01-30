# import datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


# from datetime import timedelta


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    description = fields.Text('Description', )
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From',  # default='get_date'
                                    copy=False, )  # Exercise: prevent copying of the availability date
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True,
                                 copy=False)  # Exercise: set the selling price as read-only || prevent copying of
    # the selling price values
    bedrooms = fields.Integer('Bedrooms', default="2")
    living_area = fields.Integer('Living Area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage ?')
    garden = fields.Boolean('Garden ?')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection([('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
                                          default='East')
    state = fields.Selection(
        selection=[('New', 'New'), ('Offer received', 'Offer received'), ('Offer accepted', 'Offer accepted'),
                   ('Sold', 'Sold'), ('Canceled', 'Canceled')],
        required=True, copy=False, default='New')
    property_status = fields.Selection(
        string="Property_Status",
        selection=[('Sold', 'Sold'), ('Cancelled', 'Cancelled'), ('None', 'None')],
        default='None'
    )
    name = fields.Char(required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    salesperson_id = fields.Many2one('res.users', string="Sales Man",
                                     default=lambda self: self.env.user)  # also add default field
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many('estate.property.offer', "property_id", string="offers")
    total_area = fields.Float(compute="property_total_area")

    best_offer = fields.Float(compute="property_best_offer")

    _sql_constraints = [
        ('check_expected_price',
         'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_selling_price',
         'CHECK(selling_price > 0)',
         'A property selling price must be positive'),
    ]

    # @api.constrains('selling_price')
    # def _check_selling_price(self):
    #     for record in self:
    #         if record.selling_price < (0.9 * record.expected_price):
    #             raise ValidationError(
    #                 -('The serial number has already been assigned: \n Product: %s, Serial Number: %s'))

    # Computed Values

    # Property's Total Area
    @api.depends("living_area", "garden_area")
    def property_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    # Property's Best Offer
    @api.depends("offer_ids.price")
    def property_best_offer(self):
        for record in self:
            try:
                max_value = max(record.offer_ids.mapped('price'))
                record.best_offer = max_value
            except ValueError:
                record.best_offer = 0
        # for record in self:
        #     if record.offer_ids:
        #         max_value = max(record.offer_ids.mapped('offer_ids.price'))
        #         record.best_offer = max_value
        #     else:
        #         record.best_offer = False

    @api.onchange("garden")
    def onchange_for_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = None
            self.garden_orientation = None

    # def testt(self):
    #     print('test')
    #     return

    def sell_property_button(self):
        for record in self:
            if record.property_status == 'Cancelled':
                raise ValidationError('You cannot sell a cancelled property.')
            elif record.property_status == 'None':
                record.property_status = 'Sold'
                return True
            elif record.property_status == 'Sold':
                return True
        else:
            record.property_status == 'Sold'
            return True

    def cancel_property_button(self):
        for record in self:
            if record.property_status == 'Sold':
                raise ValidationError('You cannot cancel a sold property.')
            elif record.property_status == 'None':
                record.property_status = 'Cancelled'
                return True
            elif record.property_status == 'Cancelled':
                return True
            else:
                record.property_status == 'Cancelled'
                return True
