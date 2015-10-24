__author__ = 'susperius'


def node_overview_node_entry(node_name, node_address, crashes, status, last_contact):
    return "<tr>\r\n<td><a href=\"/index.py?func=node_detail&node=" + node_address + "\">" + node_name + "</a></td>\r\n" + \
            "<td>" + node_address + "</td>\r\n" +\
            "<td>" + crashes + "</td>\r\n" + \
            "<td>" + status + "</td>\r\n" + \
            "<td>" + last_contact + "</td>\r\n" + \
            "</tr>\r\n"


def node_detail_table_entry(caption, value):
    return "<tr><td><b>" + caption + "</b></td>\r\n" + \
           "<td>" + value + "</td></tr>\r\n"


def node_detail_table_entry_editable(caption, value):
    return "<tr><td><b>" + caption + "</b></td>\r\n" + \
           "<td><input type=\"text\" name=\"" + caption.lower() + "\" value=\"" + \
           value + "\" size=\"60\"></td></tr>\r\n"


