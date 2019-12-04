# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.model
    def create(self, values):
        self.add_followers(values)
        new_id = super(SaleOrder, self).create(values)
        
        new_id.message_subscribe([x.partner_id.id for x in
                                    new_id.message_follower_ids])

        body = "SO created, please check"
        new_id.send_followers(body) 
        return new_id

    # menambah followers di so

    @api.model
    def add_followers(self, values):
        uid = self.env.uid
        group_ids = self.find_notif_users()
        partner_ids= []

        for group in group_ids :
            for user in group.users :
                if user.id != uid:
                    partner_ids.append(user.partner_id.id)

            if partner_ids :
                values['message_follower_ids'] = [(0,0, {
                    'res_model' : 'sale.order',
                    'partner_id' : pid }) for pid in partner_ids]

    # mencari nama2 grup yang hendak di notif 
    @api.model
    def find_notif_users(self):
        group_obj = self.env['res.groups']
        group_ids = group_obj.sudo().search([
            ('category_id', '=', 'Sales'),
            ('name', '=', 'Manager') ])
            
        return group_ids  

    @api.multi
    def send_followers(self, body):

        # to inbox followers and write notes
        followers = [x.partner_id.id for x in 
                        self.message_follower_ids]

        self.message_post(body=body,
                            type="notification", subtype="mt_comment",
                            partner_ids=followers,
                            )
        return

    
    
    
        
    
    

    
