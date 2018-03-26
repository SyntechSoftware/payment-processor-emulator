import json
import urllib
import re
import hashlib
import random

from .models import BillingParams, Transaction, Tokenization


def process_pay(params, supplier, is_inner_valid=False):

    tr_param = BillingParams.objects.filter(supplier=supplier).first()

    if tr_param:
        success_url = tr_param.success_url
        failure_url = tr_param.failure_url
        transaction_password = tr_param.transaction_password
        include_cc = tr_param.include_cc
        generate_errors = tr_param.generate_errors
    else:
        success_url = "/done/"
        failure_url = "/done/"
        transaction_password = ""
        include_cc = False
        generate_errors = False

    tranmode = params.get("tranmode", '')

    standard = False
    validate = False
    tokenization = False
    credit = False

    if 'A' in tranmode:
        standard = True
    if 'V' in tranmode:
        validate = True
    if 'K' in tranmode:
        tokenization = True
    if 'C' in tranmode:
        credit = True

    ccno = params.get("ccno", "") if isinstance(params.get("ccno"), basestring) else ""

    use_token = False
    if not ccno:
        tk = Tokenization.objects.filter(token=params.get('TranzilaTK', '')).first()
        print tk, params.get('TranzilaTK', '')
        if tk:
            ccno = tk.ccno
            use_token = True

    Response = "000"

    if not standard and not validate and not tokenization and not credit:
        Response = "062"

    if transaction_password and transaction_password != params.get('TranzilaPW'):
        Response = "062"

    ccno = re.sub("[^0-9]", "", ccno)
    try:
        summ = float(params.get("sum", "0.0"))
    except (ValueError, TypeError):
        summ = 0.0

    if summ <= 0:
        Response = "708"

    if not validate_ccno(ccno):
        Response = "033"

    if not use_token and not validate_cvv(params.get("mycvv")):
        Responsecvv = 0
        Response = "006"
    else:
        Responsecvv = 1

    if not validate_exdate(params.get("expdate"), params.get("expmonth"), params.get("expyear")):
        Response = "710"

    if Response == "000" and generate_errors:
        if random.random()*100 > 70:
            Response = "003"

    results = {}

    results.update(params)

    if not include_cc:
        results['ccno'] = ccno[-4:]

    results['Response'] = Response

    csum = 0.0
    dsum = 0.0

    if standard or validate:
        dsum = summ
    if credit or validate:
        csum = summ

    ConfirmationCode = ''.join(random.choice("0123456789") for _ in range(7))
    Tempref = ''.join(random.choice("0123456789") for _ in range(8))

    results['ConfirmationCode'] = ConfirmationCode
    results['Tempref'] = Tempref

    if Response == "000":
        results['Responsesource'] = 0
        results['Responseid'] = 0
    else:
        results['Responsesource'] = 1
        results['Responseid'] = 1
        csum = 0.0
        dsum = 0.0

    results['Responsecvv'] = Responsecvv

    results['cardtype'] = int(random.random() * 9 + 1)
    results['cardissuer'] = int(random.random() * 9 + 1)
    results['cardaquirer'] =int(random.random() * 9 + 1)

    if tokenization and ccno:
        tk = Tokenization.objects.filter(ccno=ccno).first()
        while not tk:
            tk_id = 'V' + ''.join(random.choice("0123456789abcdefjhijklmnopqrstuvwxyz") for _ in range(18))
            tt = Tokenization.objects.filter(token = tk_id).first()
            if not tt:
                tk = Tokenization(token=tk_id, supplier=supplier, ccno=ccno)
                tk.save()
        results['TranzilaTK'] = tk.token

    tt = Transaction(
        supplier=supplier,
        Response=Response,
        sum=summ,
        csum=csum,
        dsum=dsum,
        tranmode=tranmode,
        ConfirmationCode=ConfirmationCode,
        Tempref=Tempref,
        params=json.dumps(results)
    )
    tt.save()

    results['index'] = tt.id

    return urllib.urlencode(results)


def validate_ccno(number):
    try:
        dub, tot = 0, 0
        for i in range(len(number) - 1, -1, -1):
            for c in str((dub + 1) * int(number[i])):
                tot += int(c)
            dub = (dub + 1) % 2

        return (tot % 10) == 0
    except ValueError:
        return False


def validate_exdate(expdate, expmonth, expyear):

    try:
        dd = int(expdate) if expdate else None
    except (TypeError, ValueError):
        dd = None
    try:
        dm = int(expmonth) if expmonth else None
    except (TypeError, ValueError):
        dm = None
    try:
        dy = int(expyear) if expyear else None
    except (TypeError, ValueError):
        dy = None

    try:
        if dd:
            dm = dd/100
            dy = dd % 100

        if not dm or not dy:
            return False
        dz = dy*100 + dm
        from datetime import date
        dc = (date.today().year % 100) * 100 + date.today().month

        return dz >= dc

    except (TypeError, ValueError):
        return False


def validate_cvv(cvv):
    if cvv and (len(cvv) == 3 or len(cvv) == 4):
        if cvv[0:1] == cvv[1:2] and cvv[2:3] == cvv[1:2]:
            return True
    return False
