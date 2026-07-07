import frappe

def execute(filters=None):
    columns = [
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 180,
        },
        {
            "label": "Article",
            "fieldname": "article",
            "fieldtype": "Link",
            "options": "Article",
            "width": 180,
        },
        {
            "label": "Amount",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120,
        },
	    {
            "label": "Date",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Transaction",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Library Transaction",
            "width": 180,
        },
    ]

    data = frappe.db.sql("""
        SELECT
            lt.library_member,
            t.article,
            t.amount,
			lt.date,
            lt.name
        FROM `tabLibrary Transaction` lt
        JOIN `tabTransaction` t
            ON t.parent = lt.name
    """, as_dict=True)

    return columns, data