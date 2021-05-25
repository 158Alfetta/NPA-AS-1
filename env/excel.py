import openpyxl
from openpyxl.styles import Color, PatternFill, Font, Border, Alignment, Side
from openpyxl.cell import Cell
from openpyxl.utils.cell import *

class excelModule:
    def __init__(self, filename, sheet):
        self.filename = filename
        self.sheet = sheet

    def createFile(self):
        wb = openpyxl.Workbook()
        wb.save(self.filename)

    def load_workbook(self): # for write only
        self.workbook = openpyxl.load_workbook(self.filename)
        all_sheets = self.workbook.sheetnames
        self.worksheet = self.workbook[all_sheets[self.sheet]]

    def saveFile(self): # use after written
        self.workbook.save(self.filename)

    def adjust_width(self, column_number, width):
        column = get_column_letter(column_number)
        self.worksheet.column_dimensions[column].width = width

    def text_alignment(self, row, column, position):
        cell = self.worksheet.cell(row, column)
        cell.alignment = Alignment(horizontal=position, vertical='center', wrap_text=True)

    def setBold(self, row, column):
        cell = self.worksheet.cell(row, column)
        cell.font = Font(bold=True)

    def fillColor(self, row, column, color):
        color_filter = {
            'blue' : 'ACBACA',
            'green' : 'C7E4B4',
            'yellow' : 'FFFF72',
            'red' : "FF9098"
        }
        color = color_filter[color]
        cell = self.worksheet.cell(row, column)
        cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')

    def mergeCell(self, row_start, row_end, column_start, column_end):
        worksheet = self.worksheet
        worksheet.merge_cells(start_row=row_start, start_column=column_start, end_row=row_end, end_column=column_end)

    def setBorder(self, row, column, style):
        thin_border = Border(left=Side(style=style), 
                         right=Side(style=style), 
                         top=Side(style=style), 
                         bottom=Side(style=style))
        
        self.worksheet.cell(row, column).border = thin_border

    def writeCell(self, row, column, value):
        cell = self.worksheet.cell(row, column)
        cell.value = value

    def writeHeader(self, header):
        for head in header:
            col = header.index(head) + 1
            self.writeCell(row=1, column=col, value=head)
            self.text_alignment(row=1, column=col, position='center')
            self.fillColor(row=1, column=col, color='blue')
            self.setBold(row=1, column=col)
            self.setBorder(row=1, column=col, style='thin')