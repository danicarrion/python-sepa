# -*- coding: utf-8 -*-

import random
import string
from datetime import datetime
from jinja2 import Environment, PackageLoader


SEQUENCE_TYPES = ("FRST", "RCUR", "FNAL", "OOFF")


def prep_str(original_string):
    final_string = u""

    for char in original_string or "":
        try:
            char.decode("ascii")
        except UnicodeEncodeError:
            pass
        else:
            final_string += char.upper()
            continue

        if char == u"á" or char == u"Á":
            final_string += "A"
        elif char == u"é" or char == u"É":
            final_string += "E"
        elif char == u"í" or char == u"Í":
            final_string += "I"
        elif char == u"ó" or char == u"Ó":
            final_string += "O"
        elif char == u"ú" or char == u"Ú":
            final_string += "U"
        elif char == u"ü" or char == u"Ü":
            final_string += "U"
        elif char == u"ñ" or char == u"Ñ":
            final_string += "N"
        elif char == u"º" or char == u"ª":
            continue
        elif char == "ç" or char == "Ç":
            final_string += "C"

    return final_string.encode('ascii', errors='replace')


class Payment(object):
    total_amount = 0
    total_invoices = 0

    def __init__(self, company, invoices, name_map=None, backend="django"):
        self.company = company
        self.invoices = invoices
        self.name_map = name_map
        self.backend = backend
        self.current_time = datetime.now()
        self.env = Environment(loader=PackageLoader('sepa', 'templates'))
        self.template = self.env.get_template('core.xml')

    def get_key(self, name):
        if self.name_map is not None and name in self.name_map:
            return self.name_map[name]
        else:
            return name

    def get_value(self, model, name):
        name = self.get_key(name)

        for model_name in name.split(".")[:-1]:
            model = getattr(model, model_name)

        return getattr(model, name)

    def append_payment_info(self, invoices, payment_infos, sequence_type):
        if len(invoices) == 0:
            return

        payment_info = {
            "seq_tp": sequence_type,
            "pmt_inf_id": "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(35)),
            "pmt_mtd": "DD",
            "cd__sl": "SEPA",
            "cd__li": "CORE",
            "reqd_colltn_dt": self.current_time.strftime("%Y-%m-%d"),  # Add 2 days?
        }
        total_amount = 0
        total_invoices = 0

        payment_info["transaction_infos"] = []
        for invoice in invoices:
            transaction_info = {}

            amount = self.get_value(invoice, "amount")
            total_amount += amount

            transaction_info["end_to_end_id"] = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(35))
            transaction_info["instd_amt"] = "%.02f" % amount
            transaction_info["nm"] = prep_str(self.get_value(invoice, "debtor"))
            transaction_info["iban"] = self.get_value(invoice, "iban")
            transaction_info["ustrd"] = prep_str(self.get_value(invoice, "remittance_information"))
            transaction_info["mndt_id"] = prep_str(self.get_value(invoice, "mandate_reference"))
            transaction_info["dt_of_sgntr"] = self.get_value(invoice, "mandate_date_of_signature").strftime("%Y-%m-%d")

            payment_info["transaction_infos"].append(transaction_info)
            total_invoices += 1

        payment_info["ctrl_sum"] = total_amount
        payment_info["nb_of_txs"] = total_invoices

        self.total_amount += total_amount
        self.total_invoices += total_invoices

        payment_infos.append(payment_info)

    def filter_invoices_by_sequence_type(self, sequence_type):
        if self.backend == "django":
            return self.invoices.filter(**{self.get_key("sequence_type"): sequence_type})

    def render_xml(self):
        context = {}

        context["payment_infos"] = []
        for sequence_type in SEQUENCE_TYPES:
            self.append_payment_info(self.filter_invoices_by_sequence_type(sequence_type), context["payment_infos"],
                                     sequence_type)

        # Header group definition
        context["msg_id"] = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(35))
        context["cre_dt_tm"] = self.current_time.strftime("%Y-%m-%dT%H:%M:%S")
        context["ctrl_sum"] = "%.02f" % self.total_amount
        context["nb_of_txs"] = str(self.total_invoices)
        context["nm"] = prep_str(self.get_value(self.company, "name"))
        context["vatin"] = prep_str(self.get_value(self.company, "vatin"))
        context["iban"] = self.get_value(self.company, "iban")
        context["bic"] = self.get_value(self.company, "bic")

        return self.template.render(**context)
