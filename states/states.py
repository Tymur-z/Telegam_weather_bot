from aiogram.fsm.state import State, StatesGroup


class WeatherStates(StatesGroup):
    waiting_for_city = State()
    waiting_for_forecast_city = State()


class FavoritesStates(StatesGroup):
    waiting_for_city_to_add = State()
