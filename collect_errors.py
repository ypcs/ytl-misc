#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2013 The Matriculation Examination Board of Finland
# Author: Ville Korhonen <ville.korhonen@ylioppilastutkinto.fi>

import os
import sys
import csv
import re
import argparse

_ = lambda x:x

SCHOOLS_HEADERS = "numero;nimi;sähköposti"
ERRORS_HEADERS = ["Aihe","Leipäteksti","Lähettäjä: (nimi)","Lähettäjä: (osoite)","Lähettäjä: (laji)","Vastaanottaja: (nimi)","Vastaanottaja: (osoite)","Vastaanottaja: (laji)","Kopio: (nimi)","Kopio: (osoite)","Kopio: (laji)","Piilokopio: (nimi)","Piilokopio: (osoite)","Piilokopio: (laji)","Laskutustiedot","Luokat","Luottamuksellisuus","Matka","Tärkeys"]

IGNORE_EMAILS = [
    'lautakunta@ylioppilastutkinto.fi',
    '*@ylioppilastutkinto.fi',
    '*@*.ytl.local',
]

EMAIL_REGEXP = '([A-Za-z0-9.]{1,}@[A-Za-z0-9.]{1,})'

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

def main(args):
    if not os.path.exists(args.schooldata):
        print _("School data file (%s) not found! Exiting...") % args.schooldata
        return 1

    if not os.path.exists(args.errordata):
        print _("Error data file (%s) not found! Exiting...") % args.errordata
        return 1

    prog = re.compile(EMAIL_REGEXP)

    schools = []
    with open(args.schooldata) as scsv:
        reader = csv.reader(scsv, delimiter=';')
        for r in reader:
            sid = r[0]
            sname = r[1].decode('iso-8859-1')
            semail = r[2]
            schools.append({
                           'id': sid,
                           'name': sname.strip(),
                           'email': semail.strip().lower(),
                           })
    
    error_emails = []
    with open(args.errordata) as escv:
        reader = csv.reader(escv, delimiter=',', quotechar='"')
        for r in reader:
            matches = re.findall(prog, r[1])
            error_emails += matches
    cleaned_emails = f7(error_emails)

    mapping = []
    unknowns = []


    for e in cleaned_emails:
        em = e.strip().lower()
        found = False
        if not em in IGNORE_EMAILS:
            for s in schools:
                if em == s['email']:
                    res = '%s\t"%s", %s' % (s['id'], s['name'], em)
                    print res.encode('ascii', 'ignore')
                    found = True
            if not found:
                unknowns.append(em)

    print 
    for u in unknowns:
        print "Tuntematon: %s" % u





def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--schooldata', dest='schooldata', help=_("CSV containing mapping from schools to emails"))
    parser.add_argument('-e', '--errors', dest='errordata', help=_("CSV containing errors"))

    args = parser.parse_args()
    sys.exit(main(args))


if __name__ == "__main__":
    run()    
