frappe.ui.form.on("Visitor Pass", {
    refresh(frm) {

        // Hide Check-out Time until Checked Out
        frm.toggle_display("check_out_time", frm.doc.status === "Checked Out");

        // Show Check Out button
        if (!frm.is_new() && frm.doc.status === "Checked In") {

            frm.add_custom_button("Check Out", function () {

                frm.set_value("status", "Checked Out");
                frm.set_value("check_out_time", frappe.datetime.now_time());

                frm.save();

            });
        }
    }
});