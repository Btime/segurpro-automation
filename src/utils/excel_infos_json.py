from openpyxl import Workbook

class ExcelCollector:
    def __init__(self) -> None:
        self.nome_excel = 'SERGURPRO_EM_ABERTO.xlsx'

    def create_excel(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "SERGURPRO"

        headers = ["ROV", "STATUS", "NOME_SITE", "SISTEMA", "DESCRICAO", "TRIAGEM"]
        self.ws.append(headers)
    
    def append_info(self, rov, status, nome_site, sistema, descricao, triagem):
        self.ws.append([rov, status, nome_site, sistema, descricao, triagem])

    def save_excel(self):
        self.wb.save(self.nome_excel)