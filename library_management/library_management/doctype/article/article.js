frappe.ui.form.on("Article", {
    refresh(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button("Create Transaction", function () {

                let d = new frappe.ui.Dialog({
                    title: "Create Library Transaction",
                    fields: [
                        {
                            label: "Library Member",
                            fieldname: "library_member",
                            fieldtype: "Link",
                            options: "Library Member",
                            reqd: 1
                        }
                    ],
                    primary_action_label: "Create",
                    primary_action(values) {

                        frappe.call({
                            method: "frappe.client.insert",
                            args: {
                                doc: {
                                    doctype: "Library Transaction",
                                    library_member: values.library_member,
                                    type: "Issue",
                                    date: frappe.datetime.get_today(),
                                    article: [
                                        {
                                            article: frm.doc.name,
                                            qty: 1,
                                            rate: frm.doc.price
                                        }
                                    ]
                                }
                            },
                            callback(r) {
                                if (!r.exc) {
                                    frappe.msgprint(
                                        __("Library Transaction {0} created successfully.", [r.message.name])
                                    );
                                    d.hide();
                                }
                            }
                        });

                    }
                });

                d.show();

            });

        }

    }
});
