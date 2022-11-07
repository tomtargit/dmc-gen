
from PIL import Image
from fpdf import FPDF
from pylibdmtx.pylibdmtx import encode, decode

from dmc.dmc import Dmc

class Project:

    def __init__(self, arg_name):
        self.name = arg_name
        self.location = ''
        self.sheets = []


    def AddSheet(self, sheet):
        self.sheets.append(sheet)


    
class Sheet:  # sheet can contain many DmcConfigs
    def __init__(self, uid, arg_name,  arg_size='A4', orientation='P'):
        self.uid = uid
        self.name = arg_name
        self.size = arg_size
        self.orientation = orientation
        self.dmc_config = []

    def add_dmc(self, name):
        self.dmc_config.append(Dmc(name))

    def display_sheet(self):
        print('Sheet config: ', self.name, self.size)
        for item in self.dmc_config:
            item.display_config()

    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size=12)
        x_start = 10
        y_start = 10
        interline = 4
        header_size = 8
        for dmc_idx, dmc_config in enumerate(self.dmc_config):
            pdf.set_font('helvetica', size=header_size)
            header_length = pdf.get_string_width(dmc_config.name)

            x_increment = dmc_config.size
            y_increment = dmc_config.size + interline

            x_pos = x_start + x_increment * dmc_idx

            pdf.set_xy(x_pos, y_start)
            pdf.cell(0, 0, dmc_config.name, 0, 0)

            pdf.line(x_pos-0.2, 0, x_pos-0.2, 297)
            for dmc_idx2, dmcs in enumerate(dmc_config.get_dmcs()):
                tmp_img = generate(dmcs)
                # tmp_img.show()
                # tmp_img.save('dmtx.png')
                y_pos = y_start + header_size + y_increment*dmc_idx2
                pdf.image(tmp_img, x_pos, y_pos, h=dmc_config.size, type='PNG')
                pdf.set_font('helvetica', size=dmc_config.size/3)
                pdf.set_xy(x_pos, y_pos+1.05*dmc_config.size)
                pdf.cell(0, 0, dmcs, 0, 2)

        pdf.output("hello_world.pdf")

    def generate(data):

        encoded = encode(data.encode('utf8'), size='SquareAuto')
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
        return img
        # img.show()
        # img.save('dmtx.png')
        # print(decode(Image.open('dmtx.png')))
        # TODO: add size definition for DMC genertion or DMC sizing when printing to PDF



if __name__ == '__main__':
    pass
