import frappe
import json


@frappe.whitelist(allow_guest=True)
def generate_xml(input_data: dict = None):
    data = input_data or frappe.request.data
    if not isinstance(data, dict):
        data = json.loads(data)

    invoice_type = data.get("invoice_type")
    template = "simplified_e_invoice.xml" if invoice_type.lower() == "simplified" else "standard_e_invoice.xml"

    # render XML Template
    invoice_xml = frappe.render_template(
        f"ksa_compliance/templates/{template}",
        context={"invoice": data.get("invoice"), "seller": data.get("seller"), "buyer": data.get("buyer"),
                 "business_settings": data.get("business_settings")},
        is_path=True
    )
    invoice_xml = invoice_xml.replace("&", "&amp;")
    invoice_xml = invoice_xml.replace("\n", "")

    return invoice_xml
