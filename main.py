import json
import csv
import sys
from typing import List
from abc import ABCMeta, abstractmethod


class Ljud:
    def __init__(self, ime: str, plata: int):
        self.ime: str = ime
        self.plata: int = plata

    def plata_gore(self, koliko_gore: int):
        print(type(self.plata))
        self.plata += koliko_gore


class PeopleReader(metaclass=ABCMeta):

    @abstractmethod
    def read(self) -> List[Ljud]:
        pass


class JSONPeopleReader(PeopleReader):
    def read(self) -> List[Ljud]:
        with open("input.json") as f:
            people = json.load(f)

        ljudi = [

            Ljud(ime=i['ime'], plata=i['plata'])
            for i in people
        ]

        return ljudi


class CSVPeopleReader(PeopleReader):
    def read(self) -> List[Ljud]:
        with open("input.csv") as moj_csv_input:
            people = csv.DictReader(moj_csv_input)

            ljudi = [
                Ljud(i['ime'], int(i['plata']))
                for i in people
            ]

        return ljudi


def get_reader(file_type: str) -> PeopleReader:
    if file_type == 'json':
        return JSONPeopleReader()
    if file_type == 'csv':
        return CSVPeopleReader()


def uvecaj_platu(people):
    for it in people:
        it.plata_gore(100)


def main(input_file_type: str, output_file_type: str):

    reader: PeopleReader = get_reader(input_file_type)

    people: List[Ljud] = reader.read()

    uvecaj_platu(people)

    normalni_ljudi = [
        x.__dict__
        for x in people
    ]

    # ovo isto onako odvojeno sa klasama
    with open("output.json", "w") as outfile_json:
        outfile_json.write(json.dumps(normalni_ljudi))

    with open("output.csv", "w") as outfile_csv:
        writer = csv.DictWriter(outfile_csv, fieldnames=['ime', 'plata'])
        writer.writeheader()
        writer.writerows(normalni_ljudi)


if __name__ == '__main__':
    input_file_type = sys.argv[1]
    output_file_type = sys.argv[2]
    main(input_file_type, output_file_type)
