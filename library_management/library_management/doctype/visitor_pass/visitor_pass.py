import frappe
import qrcode
from io import BytesIO
from frappe.utils.file_manager import save_file
from frappe.model.document import Document


class VisitorPass(Document):

    def before_save(self):
        if not self.status:
            self.status = "Checked In"

        self.generate_qr()

    def validate(self):
        if self.check_in_time and self.check_out_time:
            if self.check_out_time < self.check_in_time:
                frappe.throw("Check-out Time cannot be earlier than Check-in Time.")

    def generate_qr(self):

        qr = qrcode.make(self.name)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        file_doc = save_file(
            f"{self.name}.png",
            buffer.getvalue(),
            "Visitor Pass",
            self.name,
            is_private=0
        )

        self.qr_code = file_doc.file_url