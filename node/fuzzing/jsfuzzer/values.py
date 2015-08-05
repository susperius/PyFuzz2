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
    INTS = ['0', '1', '5e6', '-7e6', '8e-6', '2e100', '7500000000', '4400000000', '-4400000000', '-7500000000',
            '4500000000', '2200000000', '-2200000000', '-4500000000', '1e6', '-1e6', '1e-6', '1e100', 'Infinity',
            'null', 'undefined', "uneval(n1)", "eval(n1)", "eval(n1, $)"]

    BUTTON_TYPE = ['button', 'submit', 'reset']

    BOOL = ['true', 'false']

    CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '0', '1', '2', '3', '4', '5', '6',
             '7', '8', '9', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', '`', '´', '*', '+', '#', '-',
             '_', '.', ':', ';', ',', '>', '<', '€', '@', 'ä', 'Ä', 'ü', 'Ü', 'ö', 'Ö', '°', '^', '\\', '\'']

    CHARACTER_SET = ['UTF-8', 'UTF-16']

    ONOFF = ['on', 'off']

    TEXT_DIRECTION = ['ltr', 'rtl', 'auto']

    LANG_CODES = ['ab', 'aa', 'af', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'ay', 'az', 'ba', 'eu', 'bn', 'dz', 'bh', 'bi',
                  'br', 'bg', 'my', 'be', 'km', 'ca', 'zh', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fo', 'fa',
                  'fj', 'fi', 'fr', 'fy', 'gl', 'gd', 'gv', 'ka', 'de', 'el', 'kl', 'gn', 'gu', 'ht', 'ha', 'hi', 'hu',
                  'is', 'io', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kn', 'ks', 'kk', 'rw', 'ky', 'rn', 'ko',
                  'ku', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mo', 'mn', 'na',
                  'ne', 'no', 'oc', 'or', 'om', 'ps', 'pl', 'pt', 'pa', 'qu', 'rm', 'ro', 'ru', 'sm', 'sg', 'sa', 'sr',
                  'sh', 'st', 'tn', 'sn', 'ii', 'sd', 'si', 'ss', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg',
                  'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tr', 'tk', 'tw', 'ug', 'uk', 'ur', 'uz', 'vi', 'vo',
                  'wa', 'cy', 'wo', 'xh', 'Yi', 'yo', 'zu', ]

    CSS_STYLES = [['align-content', 'stretch', 'center', 'flex-start', 'flex-end', 'space-between', 'space-around'],
                  ['align-items', 'stretch', 'center', 'flex-start', 'flex-end', 'space-between', 'space-around'],
                  ['align-self', 'stretch', 'center', 'flex-start', 'flex-end', 'space-between', 'space-around'],
                  ['background-attachment', 'fixed', 'scroll', 'local', 'initial', 'inherit'],
                  ['background-color', '#b0c4de', 'none', 'inherit', '#ff6600'],
                  ['background-image', 'http://127.0.0.1:8080/pic.jpg', 'none', 'inherit'],
                  ['background-position', 'size', '50% 50%', '10 10', 'left top', 'right top' 'center top',
                   'left center', 'right center', 'left bottom', 'right bottom', 'center center', 'center bottom',
                   'inherit'],
                  ['background-repeat', 'repeat', 'repeat-x', 'repeat-y', 'no-repeat', 'inherit'],
                  ['background-clip', 'border-box', 'padding-box', 'content-box', 'inherit'],
                  ['background-origin', 'border-box', 'padding-box', 'content-box', 'inherit'],
                  ['background-size', 'auto', '10px 50px', '50%', '100px', 'inherit', 'cover', 'contain'],
                  ['border', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge', 'hidden',
                   'four-sides', '5px'],
                  ['border-bottom', '5px', '#b0c4de', 'thick', '#ff6600'],
                  ['border-bottom-color', '#b0c4de', '#ff6600'],
                  ['border-bottom-style', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge',
                   'hidden'],
                  ['border-bottom-width', '5px', 'thick', 'thin', 'medium'],
                  ['border-color', '#b0c4de', '#ff6600'],
                  ['border-left', '10px', '#ff0000', 'thin', 'thick', 'medium'],
                  ['border-left-color', '#ff0000', '#ff6600'],
                  ['border-left-style', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge',
                   'hidden'],
                  ['border-left-width', '10px', 'thin'],
                  ['border-right', '5px', '#b0c4de', 'thin', 'medium', 'thick'],
                  ['border-right-color', '#b0c4de', '#ff6600'],
                  ['border-right-style', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge',
                   'hidden'],
                  ['border-right-width', '5px', 'thin', 'medium', 'thick'],
                  ['border-style', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge',
                   'hidden', 'four-sides', 'thick'],
                  ['border-top', '5px', '#b0c4de', 'thick', 'thin', 'medium'],
                  ['border-top-color', '#b0c4de', '#ff6600'],
                  ['border-top-style', 'solid', 'double', 'groove', 'dotted', 'dashed', 'inset', 'outset', 'ridge',
                   'hidden'],
                  ['border-top-width', '5px', 'thick'],
                  ['border-width', '5px', 'thick'],
                  ['box-shadow', 'none', 'inherit', '20px 20px 50px 20px pink', '10px 10px black',
                   '10px 10px 50px 20px pink inset', '50px 50px 5px orange', '-20px -20px -50px -20px pink',
                   '10px -10px black', '10px -10px 50px -20px pink inset', '-50px -50px 5px orange'],
                  ['bottom', 'auto', '10px', '-10px', '50%', 'inherit'],
                  ['clear', 'left', 'right', 'both'],
                  ['clip', 'auto', 'rect(0px, 25px, 100px, 0px)', 'rect(20px, 20px, 20px, 20px)'],
                  ['color', '#b0c4de', '#ff6600'],
                  ['direction', 'rtl', 'ltr'],
                  ['display', 'block', 'inline', 'flex', 'run-in', 'list-item', 'table', 'table-caption'],
                  ['float', 'left', 'right'],
                  ['font-family', 'Georgia', 'Palatino Linotype', 'Book Antiqua', 'Arial', 'Helvetica'],
                  ['font-size', '100%', '10px', 'small', 'inherit'],
                  ['font-style', 'italic', 'oblique', 'normal'],
                  ['font-variant', 'small-caps'],
                  ['font-weight', 'bold', '900'],
                  ['height', '100px', 'auto'],
                  ['hanging-punctuation', 'first', 'none', 'last', 'allow-end', 'force-end'],
                  ['justify-content', 'flex-start', 'flex-end', 'center', 'space-between', 'space-around'],
                  ['letter-spacing', '2px'],
                  ['line-height', '2', '90%'],
                  ['list-style', 'circle', 'square', 'disc', 'upper-alpha', 'lower-alpha', 'upper-roman', 'lower-roman',
                   'decimal', 'inside', 'outside', 'none'],
                  ['list-style-image', 'file:///c:/pyfuzz/fuzzing/background.jpg'],
                  ['list-style-position', 'inside', 'outside'],
                  ['list-style-type', 'circle', 'square', 'disc', 'upper-alpha', 'lower-alpha', 'upper-roman',
                   'lower-roman', 'decimal'],
                  ['margin', '5px', '10%', 'auto'],
                  ['margin-bottom', '2px', '30%', 'auto'],
                  ['margin-left', '5px', '50%', 'auto'],
                  ['margin-right', '5px', '50%', 'auto'],
                  ['margin-top', '10px', '60%', 'auto'],
                  ['overflow', 'visible', 'hidden', 'scroll', 'auto', 'inherit'],
                  ['overflow-y', 'visible', 'hidden', 'scroll', 'auto', 'inherit'],
                  ['overflow-x', 'visible', 'hidden', 'scroll', 'auto', 'inherit'],
                  ['padding', '5px', '100%', 'four-sides'],
                  ['padding-bottom', '10px', '100%'],
                  ['padding-left', '5px', '40%'],
                  ['padding-right', '6px', '100%'],
                  ['padding-top', '10px', '40%'],
                  ['position', 'absolute', 'relative', '100%', '100px'],
                  ['text-align', 'right', 'center', 'left', 'justify'],
                  ['text-decoration', 'line-through', 'overline', 'underline', 'none'],
                  # ['text-decoration-color', '#b0c4de', '#ff6600'],
                  # ['text-decoration-style', 'solid', 'double', 'dotted', 'dashed', 'wavy'],
                  ['text-indent', '5px', '5%'],
                  ['text-justify', 'inter-word', 'inter-ideograph', 'inter-cluster', 'distribute', 'kashida', 'trim'],
                  ['text-transform', 'capitalize', 'lowercase', 'uppercase'],
                  ['vertical-align', 'vertical-values'],
                  ['white-space', 'nowrap'],
                  ['width', '100pz', '100%', 'auto'],
                  ['word-spacing', '2px', '10px'],
                  ['z-index', '1']]
