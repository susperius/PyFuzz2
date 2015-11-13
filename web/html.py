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


def node_detail_table_entry_editable(caption, value, name=None):
    if name is None:
        name = caption
    return "<tr><td><b>" + caption + "</b></td>\r\n" + \
           "<td><input type=\"text\" name=\"" + name.lower() + "\" value=\"" + \
           value + "\" size=\"60\"></td></tr>\r\n"


def table_header(captions, ident=None):
    table = "<table id=\"" + ident + "\" >\r\n" if ident is not None else "<table>"
    table += "\t<tr>\r\n"
    for caption in captions:
        table += "\t\t<th>" + caption + "</th>\r\n" if caption != "" else "\t\t<th/>"
    table += "\t</tr>\r\n"
    return table


def table_footer():
    return "</table>"


def table_entry(cells):
    entry = "\t<tr>\r\n"
    for cell in cells:
        if type(cell) == str:
            entry += "\t\t<td>" + cell + "</td>\r\n"
        if type(cell) == list or type(cell) == set:
            entry += "\t\t<td>\r\n"
            for value in cell:
                entry += "\t\t\t" + value + "<br>\r\n"
            entry += "\t\t</td>\r\n"
    entry += "\t</tr>\r\n"
    return entry


def action_button(caption, action, method):
    return "<form action=\"" + action + "\" method=\""+ method + "\">\r\n" + \
           "<input type=\"submit\" value=\"" + caption + "\">\r\n</form>\r\n"
