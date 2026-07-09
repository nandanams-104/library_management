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
        {
            "label": "Person",
            "fieldname": "created_from",
            "fieldtype": "Link",
            "options": "Person",
            "width": 150,
        },
    ]

    filters_dict = {}

    if filters and filters.get("library_member"):
        filters_dict["library_member"] = filters.get("library_member")

    transactions = frappe.get_all(
        "Library Transaction",
        filters=filters_dict,
        fields=["name", "library_member", "date"]
    )

    data = []

    for transaction in transactions:

        person = frappe.db.get_value(
            "Library Member",
            transaction.library_member,
            "created_from"
        )

        articles = frappe.get_all(
            "Transaction",
            filters={"parent": transaction.name},
            fields=["article", "amount"]
        )

        for article in articles:
            data.append({
                "library_member": transaction.library_member,
                "article": article.article,
                "amount": article.amount,
                "date": transaction.date,
                "name": transaction.name,
                "created_from": person,
            })

    return columns, data