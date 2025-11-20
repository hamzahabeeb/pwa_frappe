// your_app/your_app/report/stock_report/stock_report.js

frappe.query_reports["Stock Report"] = {
    "filters": [
        {
            fieldname: "item_code",
            label: "Item Code",
            fieldtype: "Link",
            options: "Item",
            reqd: 0,
        },
        {
            fieldname: "item_group",
            label: "Item Group",
            fieldtype: "Link",
            options: "Item Group",
            reqd: 0,
        },
        {
            fieldname: "warehouse",
            label: "Warehouse",
            fieldtype: "Link",
            options: "Warehouse",
            reqd: 0,
        }
    ]
};
