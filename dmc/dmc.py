
from uuid import uuid4, UUID
from abc import ABC
import json

from . import constants as c


class DmcPart:
    """ Common class to inherit from for different DmcPart classes"""

class DmcPartCounter(DmcPart):
    """ Counter - part of single DMC config. """
    
    def __init__(self, start=0, step=1, chars_num=1):
        self.type = 'Counter'
        self.uuid = uuid4()
        self.start = start
        self.step = step
        self.chars_num = chars_num

class DmcPartConstant(DmcPart):
    """ Constant - part of single DMC config. """

    def __init__(self, phrase='text'):
        self.type = 'Constant'
        self.uuid = uuid4()
        self.phrase = phrase


# TODO: define if number should be printed beneath code
class Dmc:
    """ Contains single DMC configuration """

    def __init__(self, name):
        self.name = name
        self.uuid = uuid4()
        self.size = 1
        self.quiet_zone = 1
        self.count = 0
        self.dmc_parts = {}
        self.dmc_parts_order = []
        self.dmcs = []

    def to_json(self):
        json.dumps(self.__dict__)

    def get_dmcs(self):
        self.dmcs = []
        for x in range(self.count):
            result_dmc = ''
            for item in self.dmc_parts:
                if isinstance(item,DmcPartConstant):
                    result_dmc += item.phrase
                if isinstance(item,DmcPartCounter):
                    result_dmc += str(int(item.start)+x*int(item.step)).zfill(item.chars_num)
            print(result_dmc)
            self.dmcs.append(result_dmc)
        return self.dmcs

    def set_size(self, size):
        self.size = size

    def set_count(self, count):
        self.count = count

    def set_quiet_zone(self, arg_quiet_zone):
        self.quiet_zone = arg_quiet_zone

    # def add_dmc_part(self, arg_data):
    #     if isinstance(arg_data,DmcPartConstant) \
    #             or isinstance(arg_data,DmcPartCounter):
    #         self.dmc_part.append(arg_data)
    #     else:
    #         print('----Data not valid')

    def add_part(self, dmc_part: DmcPart = DmcPartConstant()):
        """ Adds dmc_part to dmc. 
        
        If dmc_part is not passed as argument, 
        creates empty "constant" dmc part.
        """
        self.dmc_parts[dmc_part.id] = dmc_part
        self.dmc_parts_order.append(dmc_part.id)
        print(f'Added dmc: {dmc_part.id}')

    def remove_part(self, dmc_part_id: UUID):
        """ Removes dmc from sheet. """
        
        # TODO ask user for confirmation

        self.dmc_parts.pop(dmc_part_id)
        self.dmc_parts_order.remove(dmc_part_id)
        print(f'Removed dmc data: {dmc_part_id}')

    def display_config(self):
        print('\t', self.name, self.size, self.quiet_zone, self.count)
        for item in self.dmc_part:
            if isinstance(item,DmcPartConstant):
                print('\t\t', item.type, item.phrase)
            if isinstance(item,DmcPartCounter):
                print('\t\t', item.type, 'start', item.start, 'by', item.step, 'characters', item.chars_num)

        # def main():
        #     pdf = FPDF()
        #     pdf.add_page()
        #     pdf.set_font('helvetica', size=12)
        #     pdf.cell(txt="hello world")
        #     pdf.output("hello_world.pdf")


if __name__ == '__main__':
    pass
