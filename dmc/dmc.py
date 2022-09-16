# pip install pylibdmtx
# pip install pylibdmtx[scripts]

# sudo apt-get install libdmtx0b
# pip install fpdf2

# load
from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image
from fpdf import FPDF
import json
from . import constants as c


# TODO: define if number should be printed beneath code
class DmcConfig:

    def __init__(self, arg_name):
        self.name = arg_name
        self.size = 0
        self.quiet_zone = 0
        self.count = 0
        self.dmc_part = []
        self.dmcs = []


    def to_json(self):
        json.dumps(self.__dict__)

    def get_dmcs(self):
        self.dmcs = []
        for x in range(self.count):
            result_dmc = ''
            for item in self.dmc_part:
                if type(item) == DmcConfigConstant:
                    result_dmc += item.phrase
                if type(item) == DmcConfigCounter:
                    result_dmc += str(int(item.start)+x*int(item.step)).zfill(item.chars_num)
            print(result_dmc)
            self.dmcs.append(result_dmc)
        return self.dmcs

    def set_size(self, arg_size):
        self.size = arg_size

    def set_count(self, arg_count):
        self.count = arg_count

    def set_quiet_zone(self, arg_quiet_zone):
        self.quiet_zone = arg_quiet_zone

    def add_dmc_part(self, arg_data):
        if type(arg_data) == DmcConfigConstant \
                or type(arg_data) == DmcConfigCounter:
            self.dmc_part.append(arg_data)
        else:
            print('----Data not valid')

    def display_config(self):
        print('\t', self.name, self.size, self.quiet_zone, self.count)
        for item in self.dmc_part:
            if type(item) == DmcConfigConstant:
                print('\t\t', item.type, item.phrase)
            if type(item) == DmcConfigCounter:
                print('\t\t', item.type, 'start', item.start, 'by', item.step, 'characters', item.chars_num)

        # def main():
        #     pdf = FPDF()
        #     pdf.add_page()
        #     pdf.set_font('helvetica', size=12)
        #     pdf.cell(txt="hello world")
        #     pdf.output("hello_world.pdf")

class DmcConfigCounter:
    def __init__(self, start, step, chars_num):
        self.type = 'Counter'
        self.start = start
        self.step = step
        self.chars_num = chars_num

class DmcConfigConstant:
    def __init__(self, phrase):
        self.type = 'Constant'
        self.phrase = phrase


class DmcSheet:  # sheet can contain many DmcConfigs
    def __init__(self, arg_name, arg_size):
        self.name = arg_name
        self.size = arg_size
        self.orientation = 'P'
        self.dmc_config = []

    def add_dmc(self, name):
        self.dmc_config.append(DmcConfig(name))

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
