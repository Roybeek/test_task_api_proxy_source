from fastapi import FastAPI

from src.helpers import DataCreator, ApiAnswer

app = FastAPI()


# Поскольку апишка тестовая, не буду использовать версинирование. Назову метод мануально.
@app.get("/get_gas_station_info", tags=["Test source 1"])
async def gas_station_info():
    try:
        creator = DataCreator()
        data = creator.create_gas_stations_data()
        return ApiAnswer.response(data=data)
    except Exception as e:
        return ApiAnswer.response(error=f"При обработке запроса возникло исключение {str(e)}", status_code=500)


@app.get("/get_fuel_info", tags=["Test source 2"])
async def gas_info():
    try:
        creator = DataCreator()
        data = creator.create_fuel_data()
        return ApiAnswer.response(data=data)
    except Exception as e:
        return ApiAnswer.response(error=f"При обработке запроса возникло исключение {str(e)}", status_code=500)
