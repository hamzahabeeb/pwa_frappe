// Copyright (c) 2025
// For license information, please see license.txt

frappe.query_reports["Stock Report"] = {
    "filters": [
        {
            "fieldname": "item_code",
            "label": "Item Code",
            "fieldtype": "Link",
            "options": "Item",
            "reqd": 0
        },
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "reqd": 0
        },
        {
            "fieldname": "warehouse",
            "label": "Warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "reqd": 0
        },
        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Link",
            "options": "Item Group",
            "reqd": 0
        },
        {
            "fieldname": "brand",
            "label": "Brand",
            "fieldtype": "Link",
            "options": "Brand",
            "reqd": 0
        },
        {
            "fieldname": "batch_no",
            "label": "Batch",
            "fieldtype": "Link",
            "options": "Batch",
            "reqd": 0
        }
    ]
};
