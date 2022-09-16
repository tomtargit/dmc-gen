# This file runs application.

import os
from dmc.dmc import DmcConfig, DmcSheet, DmcConfigConstant, DmcConfigCounter


def main():
    sheets = []
    sheets.append(DmcSheet('jeden', 'A4'))

    sheets[0].add_dmc('variant_no')
    sheets[0].dmc_config[0].set_count(10)
    sheets[0].dmc_config[0].set_size(10)
    sheets[0].dmc_config[0].add_dmc_part(DmcConfigConstant('4500000010'))
    sheets[0].dmc_config[0].add_dmc_part(DmcConfigCounter(1, 1, 3))
    sheets[0].add_dmc('body')
    sheets[0].dmc_config[1].set_count(10)
    sheets[0].dmc_config[1].set_size(15)
    sheets[0].dmc_config[1].add_dmc_part(DmcConfigConstant('5555100030'))
    sheets[0].dmc_config[1].add_dmc_part(DmcConfigCounter(1, 1, 3))


    selector = 0

    while selector != 9:

        match selector:
            case 0:
                os.system('cls||clear')
                print('Sheets: ', len(sheets))
                for idx, sheet in enumerate(sheets):
                    print('\t', idx, ":", sheet.name)
                print("\n")
                print("1: Create new sheet")
                print("2: Display sheet")
                print("4: Delete sheet")

            case 1:
                tmp_name = str(input('Insert name '))
                tmp_format = str(input('Insert format '))
                sheets.append(DmcSheet(tmp_name, tmp_format))

            case 2:
                tmp_sheet_idx = int(input('Insert sheet id: '))
                #sheets[tmp_sheet_idx].display_sheet()
                sheets[tmp_sheet_idx].generate_pdf()

            case 3:
                sheets[0].dmc_config[0].to_json()

            case 5:
                dmcs = sheets[0].dmc_config[0].get_dmcs()
                print(dmcs)
               # generate(dmcs)

            case 9:
                break


        selector = int(input('Select option '))

    print('end')

    pass


if __name__ == '__main__':
    main()


