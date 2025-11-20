import frappe


def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    message = get_cards(filters)
    return columns, data, message


# -------------------------------------------------------------
# Columns
# -------------------------------------------------------------
def get_columns():
    return [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 130},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 180},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 140},
        {"label": "Brand", "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 120},
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float", "width": 130},
        {"label": "Batch Summary", "fieldname": "batch_summary", "fieldtype": "Data", "width": 300},
    ]

def get_data(filters):
    conditions, params = build_conditions(filters)

    query = f"""
        SELECT
            i.name AS item_code,
            i.item_name,
            i.item_group,
            i.brand,
            bin.warehouse,
            SUM(bin.actual_qty) AS actual_qty
        FROM `tabBin` bin
        INNER JOIN `tabItem` i ON i.name = bin.item_code
        WHERE bin.actual_qty > 0
          {conditions}
        GROUP BY i.name, bin.warehouse
        ORDER BY i.item_name ASC
    """

    data = frappe.db.sql(query, params, as_dict=True)

    # Attach batch summary
    for row in data:
        row["batch_summary"] = get_batch_summary(row["item_code"], row["warehouse"])

    return data

def get_batch_summary(item_code, warehouse):
    batch_data = frappe.db.sql("""
        SELECT
            sbn.batch_no,
            SUM(sbn.qty) AS qty
        FROM `tabStock Ledger Entry` sle
        INNER JOIN `tabSerial and Batch Bundle` sbb
            ON sbb.name = sle.serial_and_batch_bundle
        INNER JOIN `tabSerial and Batch Entry` sbn
            ON sbn.parent = sbb.name
        WHERE sle.item_code = %s
          AND sbn.warehouse = %s
          AND sle.docstatus = 1
        GROUP BY sbn.batch_no
        HAVING qty > 0
    """, (item_code, warehouse), as_dict=True)

    if not batch_data:
        return "—"

    lines = []
    for b in batch_data:
        batch = b.batch_no
        qty = b.qty or 0
        lines.append(f"<b>{batch}</b>: {qty}")

    return "<br>".join(lines)


def build_conditions(filters):
    conditions = ""
    params = {}

    if filters.get("item_code"):
        conditions += " AND bin.item_code = %(item_code)s"
        params["item_code"] = filters["item_code"]

    if filters.get("item_name"):
        conditions += " AND i.item_name LIKE %(item_name)s"
        params["item_name"] = f"%{filters.get('item_name')}%"

    if filters.get("warehouse"):
        conditions += " AND bin.warehouse = %(warehouse)s"
        params["warehouse"] = filters["warehouse"]

    if filters.get("item_group"):
        conditions += " AND i.item_group = %(item_group)s"
        params["item_group"] = filters["item_group"]

    if filters.get("brand"):
        conditions += " AND i.brand = %(brand)s"
        params["brand"] = filters["brand"]

    if filters.get("batch_no"):
        conditions += """
            AND bin.item_code IN (
                SELECT item
                FROM `tabBatch`
                WHERE name = %(batch_no)s
            )
        """
        params["batch_no"] = filters["batch_no"]

    return conditions, params

def get_cards(filters):
    conditions, params = build_conditions(filters)

    items = frappe.db.sql(f"""
        SELECT item_group, SUM(actual_qty) AS qty
        FROM (
            SELECT i.item_group, bin.actual_qty
            FROM `tabBin` bin
            INNER JOIN `tabItem` i ON i.name = bin.item_code
            WHERE bin.actual_qty > 0 {conditions}
        ) AS t
        GROUP BY item_group
    """, params, as_dict=True)

    if not items:
        return ""

    html = "<div style='display:flex;gap:15px;margin:15px 0;flex-wrap:wrap;'>"
    for row in items:
        html += f"""
            <div style="padding:12px;border-radius:10px;border:1px solid #ddd;min-width:150px;box-shadow:0 1px 4px rgba(0,0,0,0.08);">
                <div style='color:#666;font-size:13px;'>{row.item_group}</div>
                <div style='font-size:20px;font-weight:600;color:#007bff;'>{row.qty}</div>
            </div>
        """
    html += "</div>"
    return html
