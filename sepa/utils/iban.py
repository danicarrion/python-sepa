def is_valid(iban):
    """
    http://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
    """
    try:
        iban = "".join(iban.split()).upper()
    except AttributeError:
        return False

    code = (iban[4:] + iban[:4])
    code = "".join(str(ord(char) - 55) if ord(char) >= 65 else char for char in code)

    return True if int(code) % 97 == 1 else False
