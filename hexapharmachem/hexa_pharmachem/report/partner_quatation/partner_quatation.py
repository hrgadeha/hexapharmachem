# Copyright (c) 2013, Bhavik Patel and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.core.doctype.user_permission.user_permission import get_user_permissions

def execute(filters=None):
	columns, data = [], []
	columns = get_column(filters)
	data = get_data(filters)
	return columns, data
	
	
def get_column(filters):
	columns = [
		{
			"label": _("Opportunity Name"),
			"fieldtype": "Link",
			"fieldname": "opportunity_name",
			"options": "Opportunity",
			"width": 100
		},
		{
			"label": _("Lead"),
			"fieldtype": "Link",
			"fieldname": "lead",
			"options": "Lead",
			"width": 100
		},
		{
			"label": _("Customer Name"),
			"fieldtype": "Data",
			"fieldname": "name",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			"width": 100
		},
		{
			"label": _("Item Code"),
			"fieldtype": "Data",
			"fieldname": "item_code",
			"width": 100
		},
		{
			"label": _("Item Name"),
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 100
		},{
			"label": _("Qty"),
			"fieldtype": "Data",
			"fieldname": "Qty",
			"width": 100
		}]
	return columns
	
def get_permitted_documents(doctype):
	return [d.get('doc') for d in get_user_permissions().get(doctype, []) \
		if d.get('doc')]

def get_data(filters):
	#return []
	user_permitted_item = get_permitted_documents('Item')
	#user_permitted_item = frappe.db.sql("""select for_value from `tabUser Permission` where allow='Item' """)
	value = ()
	condition = ''
		
	if user_permitted_item:
		condition = "  where item.item_code in %s "
		value = set(user_permitted_item)

	return frappe.db.sql(""" select op.name, op.lead , op.customer_name, op.status , 
	item.item_code, item.item_name, item.qty from `tabOpportunity` as op inner join `tabOpportunity Item` as item 
	 on item.parent= op.name {condition} """.format(condition=condition),value)
	
	
