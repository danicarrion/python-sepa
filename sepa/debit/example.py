import random
import string

from sepa.debit.core import Payment


class Dummy(object):
    pass


company = Dummy()
company.name = "TestCompany Ltd."
company.iban = "LOLIBAN"
company.bic = "LOLIBIC"
company.creditor_scheme_id = "ES12004M12345678"

invoices = []
for i in range(5):
    invoice = Dummy()
    invoice.amount = random.randint(0, 500) + (random.randint(0, 100) / 100)
    invoice.mandate_reference = "INVIMANDREF" + "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    invoice.mandate_date_of_signature = "INVIMANDSIGN" + "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    invoice.debtor = "DEBTOR" + "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    invoice.iban = "IBAN" + "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    invoice.remittance_information = "REMINF" + "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
    invoices.append(invoice)

payment = Payment(company, invoices, backend="test")
print(payment.render_xml())
