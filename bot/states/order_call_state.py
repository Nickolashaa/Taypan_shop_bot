from aiogram.fsm.state import State, StatesGroup


class OrderCallState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_comment = State()
