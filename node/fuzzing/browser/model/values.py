# coding=utf8
__author__ = 'susperius'


class FuzzValues:
    #  Types: APP_DATA, BOOL, BUTTON_TYPE, CHAR, CHARACTER_SET, COORDS, CSS, CSS_CLASS, DATETIME, DIRECTION, ELEM_ID, FORM_ID, FORM_METHOD, FORM_TARGET,
    #         FORM_ENCTYPE, HEADERS_ID, HTML_CODE, HTTP_EQUIV, INT, ID, LANG, MAP_NAME, MEDIA_TYPE, MEDIA_QUERY, MENU, METADATA_NAME, ONOFF, PIXELS, PRELOAD, REL, SCROLLING, SHAPE,
    #         SANDBOX, SORTED, STRING, TABLE_SCOPE, TARGET, TRACK_KIND, URL, WRAP
    #

    INTERESTING_VALUES = ['0', '1', '5e6', '-7e6', '8e-6', '2e100', 'null', 'pink', 'false',
                          'true', '7500000000', '4400000000', '-4400000000', '-7500000000',
                          "A" * 40, "B" * 40, '']
    STRINGS = ["A" * 40, "B" * 40, "C" * 40, "D" * 40, '', '<foo/>', '{}', '[]', "0",  "1", "0xffffffff",
               "0x10000000", "0x04000000", "0x01000000", "-1", "-4", "-10000000", "10000000", "0%",
               "100%",  "1000%", "-1%", "(3/0)", "(0/0)", "(-3/0)", "%s%s%s%s%s%s%s%s%s",
               "%n%n%n%n%n%n%n%n%n", "\\0", "\\n", "", 'Infinity', 'null', 'undefined', "uneval(n1)",
               "eval(n1)", "eval(n1, $)"]
    INTS = ['0', '1', '5', '3', '10', '2' '5e6', '-7e6', '8e-6', '2e100', '7500000000', '4400000000', '-4400000000', '-7500000000',
            '4500000000', '2200000000', '-2200000000', '-4500000000', '1e6', '-1e6', '1e-6', '1e100', 'Number.MIN_VALUE',
            'Number.NEGATIVE_INFINITY', 'Number.POSITIVE_INFINITY']

    PURE_INTS = ['0', '1', '7500000000', '4400000000', '-4400000000', '-7500000000',
                 '4500000000', '2200000000', '-2200000000', '-4500000000', '10', '20', '31337', 'Number.MAX_VALUE',
                 'Number.MIN_VALUE', 'Number.NEGATIVE_INFINITY', 'Number.POSITIVE_INFINITY'] #, 'Number.NaN']

    BUTTON_TYPE = ['button', 'submit', 'reset']

    BOOL = ['true', 'false']

    CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '0', '1', '2', '3', '4', '5', '6',
             '7', '8', '9', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', '`', '´', '*', '+', '#', '-',
             '_', '.', ':', ';', ',', '>', '<', '€', '@', 'ä', 'Ä', 'ü', 'Ü', 'ö', 'Ö', '°', '^', '\\'] #, '\'']

    COLORS = ['#FF8C00', '#FFA500', '#FF4500']

    CHARACTER_SET = ['UTF-8', 'UTF-16']

    FORM_ENCTYPE = ['application/x-www-form-urlencoded', 'multipart/form-data', 'text/plain']

    FORM_TARGET = ['_blank', '_self', '_parent', '_top']

    FORM_METHOD = ['get', 'post']

    HTTP_EQUIV = ['content-type', 'default-style', 'refresh']

    INPUT_TYPES = ['password', 'button', 'checkbox', 'color', 'date', 'datetime', 'datetime-local', 'email',
                        'file', 'hidden', 'image', 'month', 'number', 'radio', 'range', 'reset', 'search', 'submit',
                        'text', 'time', 'url', 'week']

    MEDIA_TYPE = ['video/mpeg', 'audio/mpeg', 'video/webm', 'application/javascript', 'text/css', 'text/html',
                  'text/xml']

    METADATA_NAME = ['application-name', 'author', 'description', 'generator', 'keywords']

    ONOFF = ['on', 'off']

    PRELOAD = ['auto', 'metadata', 'none']

    REL = ['alternate', 'author', 'bookmark', 'help', 'license', 'next', 'nofollow', 'noreferrer', 'prefetch',
           'prev', 'search', 'tag']

    SCROLLING = ['yes', 'no', 'auto']

    SANDBOX = ['allow-forms', 'allow-pointer-lock', 'allow-popups', 'allow-same-origin', 'allow-scripts',
               'allow-top-navigation']

    SHAPE = ['default', 'rect', 'circle', 'poly']

    SORTED = ['reversed', 'number', 'reversed number', 'number reversed']

    TABLE_SCOPE = ['col', 'colgroup', 'row', 'rowgroup']

    TARGET = ['_blank', '_parent', '_self', '_top']

    TEXT_DIRECTION = ['ltr', 'rtl', 'auto']

    TRACK_KIND = ['captions', 'chapters', 'descriptions', 'metadata', 'subtitles']

    YESNO = ['yes', 'no']

    WRAP = ['hard', 'soft']

    LANG_CODES = ['ab', 'aa', 'af', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'ay', 'az', 'ba', 'eu', 'bn', 'dz', 'bh', 'bi',
                  'br', 'bg', 'my', 'be', 'km', 'ca', 'zh', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fo', 'fa',
                  'fj', 'fi', 'fr', 'fy', 'gl', 'gd', 'gv', 'ka', 'de', 'el', 'kl', 'gn', 'gu', 'ht', 'ha', 'hi', 'hu',
                  'is', 'io', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kn', 'ks', 'kk', 'rw', 'ky', 'rn', 'ko',
                  'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mo', 'mn', 'na',
                  'ne', 'no', 'oc', 'or', 'om', 'ps', 'pl', 'pt', 'pa', 'qu', 'rm', 'ro', 'ru', 'sm', 'sg', 'sa', 'sr',
                  'sh', 'st', 'tn', 'sn', 'ii', 'sd', 'si', 'ss', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg',
                  'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tr', 'tk', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'vo',
                  'wa', 'cy', 'wo', 'xh', 'Yi', 'yo', 'zu', ]

