import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):

    def validate(self):
        total = 0
        selected_articles = set()

        for row in self.article:

            # Duplicate article check
            if row.article in selected_articles:
                frappe.throw(
                    f"Article <b>{row.article}</b> is already selected. Please choose a different article."
                )

            selected_articles.add(row.article)

            # Calculate Amount
            row.amount = (row.qty or 0) * (row.rate or 0)
            total += row.amount

        self.total_amount = total

    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()

            for row in self.article:
                article = frappe.get_doc("Article", row.article)
                article.status = "Issued"
                article.save()

        elif self.type == "Return":
            self.validate_return()

            for row in self.article:
                article = frappe.get_doc("Article", row.article)
                article.status = "Available"
                article.save()

    def validate_issue(self):
        self.validate_membership()

        for row in self.article:
            article = frappe.get_doc("Article", row.article)

            if article.status == "Issued":
                frappe.throw(f"Article {row.article} is already issued.")

    def validate_return(self):
        for row in self.article:
            article = frappe.get_doc("Article", row.article)

            if article.status == "Available":
                frappe.throw(
                    f"Article {row.article} cannot be returned without being issued first."
                )

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value(
            "Library Setting",
            "maximum_no_of_issued_article"
        )

        count = frappe.db.count(
            "Library Transaction",
            {
                "library_member": self.library_member,
                "type": "Issue",
                "docstatus": DocStatus.submitted(),
            },
        )

        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )

        if not valid_membership:
            frappe.throw("The member does not have a valid membership")