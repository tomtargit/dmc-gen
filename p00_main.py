# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

from p10_dmc import *


def main():
    Sheets = []
    Sheets.append(DmcSheet('jeden', 'A4'))

    test = DmcSheet('jeden', 'A4')
    Sheets[0].add_dmc('variant_no')
    Sheets[0].dmc_config[0].set_count(10)
    Sheets[0].dmc_config[0].add_dmc_part(DmcConfig.DmcConfigConstant('4500000010'))
    Sheets[0].dmc_config[0].add_dmc_part(DmcConfig.DmcConfigCounter(1, 1, 3))


    selector = 0

    while selector != 9:

        match selector:
            case 0:
                os.system('cls')
                print('Sheets: ', len(Sheets))
                for idx, sheet in enumerate(Sheets):
                    print('\t', idx, ":", sheet.name)
                print("\n")
                print("1: Create new sheet")
                print("2: Display sheet")
                print("4: Delete sheet")

            case 1:
                tmp_name = str(input('Insert name '))
                tmp_format = str(input('Insert format '))
                Sheets.append(DmcSheet(tmp_name, tmp_format))

            case 2:
                tmp_sheet_idx = int(input('Insert sheet id: '))
                Sheets[tmp_sheet_idx].display_sheet()
                Sheets[tmp_sheet_idx].generate_pdf()



            case 5:
                dmcs = Sheets[0].dmc_config[0].get_dmcs()
                print(dmcs)
               # generate(dmcs)

            case 9:
                break


        selector = int(input('Select option '))

    print('end')

    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


