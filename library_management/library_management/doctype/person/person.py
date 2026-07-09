from frappe.model.document import Document
import frappe


class Person(Document):

    def validate(self):
        if self.age <= 18:
            frappe.throw("Person's age must be at least 18")

        if self.email and "@" not in self.email:
            frappe.throw("Please enter a valid Email")

    def before_save(self):
        self.full_name = f"{self.first_name} {self.last_name or ''}"

        # get_all
        persons = frappe.db.get_all(
            "Person",
            fields=["name", "first_name", "email"]
        )

        frappe.msgprint(f"All Persons: {persons}")

    def after_insert(self):

        doc = frappe.get_doc({
            "doctype": "Library Member",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_from": self.name,
            "full_name": self.full_name
        })
        doc.insert()

        frappe.msgprint(f"Library Member Created: {doc.name}")

        # get_list
        members = frappe.db.get_list(
            "Library Member",
            filters={"created_from": self.name},
            fields=["name"]
        )

        frappe.msgprint(f"Library Members: {members}")

        # get_value
        member_first_name = frappe.db.get_value(
            "Library Member",
            {"created_from": self.name},
            "first_name"
        )

        frappe.msgprint(f"Library Member First Name: {member_first_name}")

        # set_value
        frappe.db.set_value(
            "Library Member",
            doc.name,
            "first_name",
            self.first_name.upper()
        )

        updated_name = frappe.db.get_value(
            "Library Member",
            doc.name,
            "first_name"
        )

        frappe.msgprint(f"Updated Library Member First Name: {updated_name}")

    def on_trash(self):
        
        members = frappe.get_all(
            "Library Member",
            filters={"created_from": self.name},
            fields=["name"]
        )

        for member in members:
            frappe.delete_doc("Library Member", member["name"])

        frappe.msgprint("Related Library Members Deleted Successfully")