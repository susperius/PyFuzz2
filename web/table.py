from flask_table import Col, LinkCol, Table


class BoldCol(Col):
    def td(self, item, attr):
        return '<td><b>{}</b></td>'.format(
            self.td_contents(item, self.get_attr_list(attr)))


class NodeTable(Table):
    name = LinkCol("NODE NAME", "node_detail", url_kwargs=dict(addr='addr'), attr='name')
    addr = Col("NODE ADDRESS")
    crashes = Col("CRASHES")
    status = Col("STATUS")
    last_contact = Col("LAST CONTACT")


class SingleNodeTable(Table):
    descr = BoldCol("")
    value = Col("")


class CrashTable(Table):
    maj_hash = Col("MAJOR HASH")
    min_hash = Col("MINOR HASH")
    descr = Col("DESCRIPTION")
    nodes = Col("NODES")
    classification = Col("CLASSIFICTION")
    download = LinkCol("DOWNLOAD", "download_crash", url_kwargs=dict(program='program', maj_hash='maj_hash',
                                                                     descr='descr'),
                       attr='download')
