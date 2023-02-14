import pandas
import xlrd

from src.helpers.img import get_img_urls

__all__ = (
    'DataCreator'
)


class DataCreator:

    def __init__(self, file_name: str = f"spisokAZS.xls"):
        workbook = xlrd.open_workbook_xls(file_name, ignore_workbook_corruption=True)
        self.gs_data = pandas.read_excel(workbook)

    def create_gas_stations_data(self):
        """
        Сгенерировать данные для имитации первого источника.
        :return:
            Возвращает список АЗС содержащий следующую информацию по каждой из АЗС:
            •	Id
            •	Координаты
            •	Номер
            •	Адрес
            •	Список URL изображений
            •	Список дополнительных услуг

        """
        main_data = self.gs_data[["number", "address", "latitude", "longitude", "additional_services"]]
        sort_data = [
            {
                "id": index,
                "number": row["number"],
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "img_list": get_img_urls(),
                "additional_services": self.create_service_list(str(row["additional_services"]))
            } for index, row in main_data.iterrows()]

        return sort_data

    def create_fuel_data(self):
        """
        Сгенерировать данные для имитации второго источника.
        Возвращает список АЗС содержащий следующую информацию по каждой из АЗС:
        •	Id
        •	Список цен на топливо, каждый элемент которого состоит из:
        ◦	Название топлива
        ◦	Цена топлива
        ◦	Валюта цены топлива

        :return:
        """
        gas_data = self.gs_data.iloc[:, 5:20]
        sort_data = [{
            "id": index,
            "fuel": self.create_fuel_list(row.to_dict())
        } for index, row in gas_data.iterrows()]
        return sort_data

    @staticmethod
    def create_service_list(services: str):
        if services == 'nan' or services == '':
            return []
        else:
            return services.split('\n')

    @staticmethod
    def create_fuel_list(gas_dict: dict):
        fuel_list = []

        for fuel in gas_dict:
            if str(gas_dict[fuel]) != 'nan' or not pandas.isna(gas_dict[fuel]):
                try:
                    fuel_list.append({
                        "title": fuel,
                        "cost": float(str(gas_dict[fuel]).split()[0]),
                        "currency": str(gas_dict[fuel]).split()[1]
                    })
                except IndexError:
                    print(f"Ошибка при попытке обработать стоимость со значением {gas_dict[fuel]}")
        return fuel_list
