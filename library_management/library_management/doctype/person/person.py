from frappe.model.document import Document
import frappe


class Person(Document):

    def before_insert(self):
        frappe.msgprint("before_insert called")

    def after_insert(self):
        doc = frappe.get_doc({
            'doctype': 'Library Member',
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_from':self.name,
            'full_name': self.full_name
        })
        doc.insert()
        doc.name


    def before_validate(self):
        frappe.msgprint("before_validate called")

    def validate(self):
        if self.age <= 18:
            frappe.throw("Person's age must be at least 18")

        if self.email and "@" not in self.email:
            frappe.throw("Please enter a valid Email")

    def before_save(self):
        self.full_name = f"{self.first_name} {self.last_name or ''}"

    def on_update(self):
        frappe.msgprint("Record Updated")

    def before_submit(self):
        frappe.msgprint("before_submit called")

    def on_submit(self):
        frappe.msgprint("Person Submitted")

    def before_cancel(self):
        frappe.msgprint("before_cancel called")

    def on_cancel(self):
        frappe.msgprint("Person Cancelled")

    def on_trash(self):
        frappe.msgprint("Person Deleted")

    def after_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(f"Renamed from {old_name} to {new_name}")

    def onload(self):
        frappe.msgprint("Document Loaded")