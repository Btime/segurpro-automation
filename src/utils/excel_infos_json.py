from openpyxl import Workbook

class ExcelCollector:
    def __init__(self) -> None:
        self.excel_name = 'SERGURPRO_EM_ABERTO.xlsx'

    def create_excel(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "SERGURPRO"

        headers = ["ID_ACTIVITY", "ROV", "STATUS", "NOME_SITE", "SISTEMA", "DESCRICAO", "TRIAGEM"]
        self.ws.append(headers)
    
    def append_info(self, id_activity, rov, status, nome_site, sistema, descricao, triagem):
        self.ws.append([id_activity, rov, status, nome_site, sistema, descricao, triagem])

    def save_excel(self):
        self.wb.save(self.excel_name)