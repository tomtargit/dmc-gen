
from uuid import uuid4, UUID

from PIL import Image
from fpdf import FPDF
from pylibdmtx.pylibdmtx import encode, decode

from dmc.dmc import Dmc


class Sheet:  # sheet can contain many DmcConfigs
    """ Manages single sheet definition.
    
    Contains single DMC parameters and lower level contents
    """

    def __init__(self, arg_name,  arg_size='A4', orientation='P'):
        self.id = uuid4()
        self.name = arg_name
        self.size = arg_size
        self.orientation = orientation
        self.dmcs = {}
        self.dmcs_order = []
        self.saved = False

    # def add_dmc(self, name):
    #     self.dmcs.append(Dmc(name))

    def add_dmc(self, dmc: Dmc = Dmc('New')):
        """ Adds dmc to sheet. 
        
        If dmc is not passed as argument, creates empty dmc.
        """
        self.dmcs[dmc.id] = dmc
        self.sheets_order.append(dmc.id)
        print(f'Added dmc: {dmc.id}')

    def remove_dmc(self, dmc_id: UUID):
        """ Removes dmc from sheet. """
        
        # TODO ask user for confirmation

        self.dmcs.pop(dmc_id)
        self.sheets_order.remove(dmc_id)
        print(f'Removed dmc data: {dmc_id}')

    def display_sheet(self):
        print('Sheet config: ', self.name, self.size)
        for item in self.dmcs:
            item.display_config()

    def generate(data):

        encoded = encode(data.encode('utf8'), size='SquareAuto')
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        return img
        # img.show()
        # img.save('dmtx.png')
        # print(decode(Image.open('dmtx.png')))
        # TODO: add size definition for DMC genertion or DMC sizing when printing to PDF


    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=12)
        x_start = 10
        y_start = 10
        interline = 4
        header_size = 8
        for dmc_idx, dmc_config in enumerate(self.dmcs):
            pdf.set_font('helvetica', size=header_size)
            header_length = pdf.get_string_width(dmc_config.name)

            x_increment = dmc_config.size
            y_increment = dmc_config.size + interline

            x_pos = x_start + x_increment * dmc_idx

            pdf.set_xy(x_pos, y_start)
            pdf.cell(0, 0, dmc_config.name, 0, 0)

            pdf.line(x_pos-0.2, 0, x_pos-0.2, 297)
            for dmc_idx2, dmcs in enumerate(dmc_config.get_dmcs()):
                tmp_img = self.generate(dmcs)
                # tmp_img.show()
                # tmp_img.save('dmtx.png')
                y_pos = y_start + header_size + y_increment*dmc_idx2
                pdf.image(tmp_img, x_pos, y_pos, h=dmc_config.size, type='PNG')
                pdf.set_font('helvetica', size=dmc_config.size/3)
                pdf.set_xy(x_pos, y_pos+1.05*dmc_config.size)
                pdf.cell(0, 0, dmcs, 0, 2)

        pdf.output("hello_world.pdf")

class Project:
    """ Manages single project definition.
    
    Contains single project parameters and lower-level components.
    """
    def __init__(self, arg_name: str = "NewProject"):
        self.id = uuid4()
        self.name = arg_name
        self.sheets = {}
        self.sheets_order = []
        self.sheets_gui = {}
        self.saved = False
        self.location = ''

    def add_sheet(self, sheet: Sheet = Sheet('Empty')):
        """ Adds sheet to project. 
        
        If sheet is not passed as argument, creates empty sheet.
        """
        self.sheets[sheet.id] = sheet
        self.sheets_order.append(sheet.id)
        print(f'Added sheet: {sheet.id}')

    def remove_sheet(self, sheet_id: UUID):
        """ Removes sheet from project. """
        
        # TODO ask user for confirmation

        self.sheets.pop(sheet_id)
        self.sheets_order.remove(sheet_id)
        print(f'Removed sheet data: {sheet_id}')

if __name__ == '__main__':
    pass
