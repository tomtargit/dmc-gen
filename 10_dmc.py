# pip install pylibdmtx
# pip install pylibdmtx[scripts]

# load
from pylibdmtx.pylibdmtx import encode, decode
from PIL import Image


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
                print('\t\t', item.type, item.start, item.step, item.chars_num)

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


def generate(arg_list):

    encoded = encode(arg_list[0].encode('utf8'))
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.show()
    # img.save('dmtx.png')
    # print(decode(Image.open('dmtx.png')))


if __name__ == '__main__':
    Sheets = []
    Sheets.append(DmcSheet('jeden', 'A4'))

    test = DmcSheet('jeden', 'A4')
    # print(test.name, test.size)
    Sheets[0].add_dmc('variant_no')
    # test.add_dmc('variant_no1')
    # print(test.dmc_config[0].name)
    # print(test.dmc_config[1].name)
    Sheets[0].dmc_config[0].set_count(10)
    Sheets[0].dmc_config[0].add_dmc_part(DmcConfig.DmcConfigConstant('4500000010'))
    Sheets[0].dmc_config[0].add_dmc_part(DmcConfig.DmcConfigCounter(1, 1, 3))

    # print(test.dmc_config[0].dmc_part[0].type)
    # print(test.dmc_config[0].dmc_part[0].chars_num)
    # print(test.dmc_config[0].dmc_part[1].type)
    # print(test.dmc_config[0].dmc_part[1].phrase)

    # print('------')
    # test.display_sheet()

    selector = 0

    while selector != 9:

        match selector:
            case 0:
                print('Sheets: ', len(Sheets))

            case 1:
                dmcs = Sheets[0].dmc_config[0].get_dmcs()
                print(dmcs)
                generate(dmcs)
            case 9:
                break

        selector = int(input('Select option'))

    print('end')
