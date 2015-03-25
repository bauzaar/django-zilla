# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import re


PHONE_rex = re.compile(r'^(\+\d{2}(\s?))?\d{5,16}$', flags=re.UNICODE)
def validate_phone(value):
    if value:
        if not PHONE_rex.match(value):
            raise ValidationError(_("Numero telefonico non valido"))


P_IVA_rex = re.compile(r'^\d{11}$', flags=re.UNICODE)
def validate_p_iva(value):
    if not P_IVA_rex.match(value):
        raise ValidationError(_("Partita IVA non valida"))


COD_FISCALE_rex = re.compile(r'^\w{11}$', flags=re.UNICODE)
def validate_codice_fiscale(value):
    if not COD_FISCALE_rex.match(value):
        raise ValidationError(_("Codice fiscale non valido"))


CAP_rex = re.compile(r'^\d{5}$', flags=re.UNICODE)
def validate_cap(value):
    if not CAP_rex.match(value):
        raise ValidationError(_("CAP non valido"))

PROVINCIA_rex = re.compile(r'^[a-zA-Z]{2,3}$', flags=re.UNICODE)
def validate_provincia(value):
    if not PROVINCIA_rex.match(value):
        raise ValidationError(_("Provincia non valida"))