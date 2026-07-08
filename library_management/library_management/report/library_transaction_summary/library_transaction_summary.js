// Copyright (c) 2026, nandana and contributors
// For license information, please see license.txt

frappe.query_reports["Library Transaction Summary"] = {
	"filters": [
		{  
			"label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member"

		}


	]
};
