# pip install pylibdmtx
# pip install pylibdmtx[scripts]
# pip install fpdf2

# load
from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image
from fpdf import FPDF


class DmcConfig:

    def __init__(self, arg_name):
        self.name = arg_name
        self.size = 0
        self.quiet_zone = 0
        self.count = 0
        self.dmc_part = []
        self.dmcs = []

    def get_dmcs(self):
        self.dmcs = []
        for x in range(self.count):
            result_dmc = ''
            for item in self.dmc_part:
                if type(item) == DmcConfig.DmcConfigConstant:
                    result_dmc += item.phrase
                if type(item) == DmcConfig.DmcConfigCounter:
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
        if type(arg_data) == DmcConfig.DmcConfigConstant \
                or type(arg_data) == DmcConfig.DmcConfigCounter:
            self.dmc_part.append(arg_data)
        else:
            print('----Data not valid')

    def display_config(self):
        print('\t', self.name, self.size, self.quiet_zone, self.count)
        for item in self.dmc_part:
            if type(item) == DmcConfig.DmcConfigConstant:
                print('\t\t', item.type, item.phrase)
            if type(item) == DmcConfig.DmcConfigCounter:
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
        for dmc_idx, dmc_config in enumerate(self.dmc_config):
            for dmc_idx2, dmcs in enumerate(dmc_config.get_dmcs()):
                tmp_img = generate(dmcs)
                # tmp_img.show()
                # tmp_img.save('dmtx.png'')
                x_start = 10
                y_start = 10
                x_increment = 30
                y_increment = 30
                x_pos = x_start + x_increment*dmc_idx
                y_pos = y_start + y_increment*dmc_idx2
                pdf.image(tmp_img, x_pos, y_pos, type='PNG')
        pdf.output("hello_world.pdf")

def generate(arg_list):

    encoded = encode(arg_list[0].encode('utf8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    return(img)
    # img.show()
    # img.save('dmtx.png')
    # print(decode(Image.open('dmtx.png')))


if __name__ == '__main__':
    pass
