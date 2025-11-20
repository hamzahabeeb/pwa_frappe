# your_app/your_app/report/stock_report/stock_report.py
import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": "Item Code",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Item Name",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Item Group",
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 140
        },
        {
            "label": "Warehouse",
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150
        },
        {
            "label": "Actual Qty",
            "fieldname": "actual_qty",
            "fieldtype": "Float",
            "width": 120
        }
    ]


def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("item_code"):
        conditions += " AND bin.item_code = %(item_code)s"
        values["item_code"] = filters["item_code"]

    if filters.get("item_group"):
        conditions += " AND item.item_group = %(item_group)s"
        values["item_group"] = filters["item_group"]

    if filters.get("warehouse"):
        conditions += " AND bin.warehouse = %(warehouse)s"
        values["warehouse"] = filters["warehouse"]

    data = frappe.db.sql(f"""
        SELECT
            bin.item_code,
            item.item_name,
            item.item_group,
            bin.warehouse,
            bin.actual_qty
        FROM
            `tabBin` bin
        LEFT JOIN
            `tabItem` item ON item.name = bin.item_code
        WHERE
            1=1 {conditions}
        ORDER BY
            bin.item_code
    """, values, as_dict=True)

    return data
