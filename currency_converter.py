#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import urllib2
import json
import argparse


def enter_currency(from_flag, currency):
 
    error = True

    currency_dict = {
        'ALL': 'Lek',
        'AFN': '؋',
        'ARS': '$',
        'AWG': 'ƒ',
        'AUD': '$',
        'AZN': 'ман',
        'BSD': '$',
        'BBD': '$',
        'BYN': 'Br',
        'BZD': 'BZ$',
        'BMD': '$',
        'BOB': '$b',
        'BAM': 'KM',
        'BWP': 'P',
        'BGN': 'лв',
        'BRL': 'R$',
        'BND': '$',
        'KHR': '៛',
        'CAD': '$',
        'KYD': '$',
        'CLP': '$',
        'CNY': '¥',
        'COP': '$',
        'CRC': '₡',
        'HRK': 'kn',
        'CUP': '₱',
        'CZK': 'Kč',
        'DKK': 'kr',
        'DOP': 'RD$',
        'XCD': '$',
        'EGP': '£',
        'SVC': '$',
        'EUR': '€',
        'FKP': '£',
        'FJD': '$',
        'GHS': '¢',
        'GIP': '£',
        'GTQ': 'Q',
        'GGP': '£',
        'GYD': '$',
        'HNL': 'L',
        'HKD': '$',
        'HUF': 'Ft',
        'ISK': 'kr',
        'INR': '0',
        'IDR': 'Rp',
        'IRR': '﷼',
        'IMP': '£',
        'ILS': '₪',
        'JMD': 'J$',
        'JPY': '¥',
        'JEP': '£',
        'KZT': 'лв',
        'KPW': '₩',
        'KRW': '₩',
        'KGS': 'лв',
        'LAK': '₭',
        'LBP': '£',
        'LRD': '$',
        'MKD': 'ден',
        'MYR': 'RM',
        'MUR': '₨',
        'MXN': '$',
        'MNT': '₮',
        'MZN': 'MT',
        'NAD': '$',
        'NPR': '₨',
        'ANG': 'ƒ',
        'NZD': '$',
        'NIO': 'C$',
        'NGN': '₦',
        'KPW': '₩',
        'NOK': 'kr',
        'OMR': '﷼',
        'PKR': '₨',
        'PAB': 'B/.',
        'PYG': 'Gs',
        'PEN': 'S/.',
        'PHP': '₱',
        'PLN': 'zł',
        'QAR': '﷼',
        'RON': 'lei',
        'RUB': '₽',
        'SHP': '£',
        'SAR': '﷼',
        'RSD': 'Дин.',
        'SCR': '₨',
        'SGD': '$',
        'SBD': '$',
        'SOS': 'S',
        'ZAR': 'R',
        'KRW': '₩',
        'LKR': '₨',
        'SEK': 'kr',
        'CHF': 'CHF',
        'SRD': '$',
        'SYP': '£',
        'TWD': 'NT$',
        'THB': '฿',
        'TTD': 'TT$',
        'TRY': '0',
        'TVD': '$',
        'UAH': '₴',
        'GBP': '£',
        'USD': '$',
        'UYU': '$U',
        'UZS': 'лв',
        'VEF': 'Bs',
        'VND': '₫',
        'YER': '﷼',
        'ZWD': 'Z$',
    }

    if from_flag is True:
        ask_currency = "Can't find such currency - %s. Enter input currency here: " % currency

    elif from_flag is False:
        ask_currency = "Can't find such currency - %s. Enter output currency here: " % currency

    while error is True:

        if currency in currency_dict:
            return currency.split()
        elif currency in currency_dict.values():
            currency = [curr for curr,sym in currency_dict.iteritems() if sym == currency]
            return currency
        elif currency == 'all':
            currency =  currency_dict.keys()
            return currency
        else:
            print "You entered wrong currency. Check your entered value. "\
                "Upper case is important. Value must not"\
                "contains blanks. You can enter one of the next currencies:"

            print "============ \n %s \n ============" % list(currency_dict)
            currency = raw_input(ask_currency)

def convert_currency(currency_from, currency_to, currency_input):
    
    result = {}
    in_data = {}
    out_data = {}
    
    for cur_fr in currency_from:

        in_data = {"amount": currency_input, "currency": cur_fr}

        for cur_to in currency_to:

            yql_base_url = "https://query.yahooapis.com/v1/public/yql"
            yql_query = \
                'select%20*%20'+ \
                'from%20yahoo.finance.xchange%20' + \
                'where%20pair%20in%20("' + \
                cur_fr + \
                cur_to + \
                '")'
            yql_query_url = \
                yql_base_url + \
                "?q=" + \
                yql_query + \
                "&format=json&env=store%3A%2F%2F" + \
                "datatables.org%2Falltableswithkeys"

            try:
                yql_response = urllib2.urlopen(yql_query_url)
                try:
                    yql_json = json.loads(yql_response.read())

                    out_data[cur_to] = "%.2f" % \
                        (
                            currency_input * \
                            float(yql_json['query']['results']['rate']['Rate'])
                        )
    
                except (ValueError, KeyError, TypeError), e:
                    out_data[cur_to] = "Can't find rates"

            except IOError, e:
                if hasattr(e, 'code'):
                    return e.code
                elif hasattr(e, 'reason'):
                    return e.reason

            if len(currency_from) > 1:
                result[cur_fr] = {'input': in_data, 'output': out_data.copy()}
            else:
                result = {'input': in_data, 'output': out_data.copy()}

    return result

parser = argparse.ArgumentParser(description='Process options for currency converter.')

parser.add_argument('--amount', dest='amount',
                   default=1.00,
                   help='enter value to convert(default is 1.00)')
parser.add_argument('--input_currency', dest='input_currency',
                   default='all',
                   help='enter input currency')
parser.add_argument('--output_currency', dest='output_currency',
                   default='all',
                   help='enter output currency')

args = parser.parse_args()

currency_from = enter_currency(True, args.input_currency)
currency_to = enter_currency(False, args.output_currency)
currency_input = float(args.amount)

output = convert_currency(list(currency_from), list(currency_to), currency_input)
print json.dumps(output, sort_keys=True, indent=4, separators=(',', ': '))
