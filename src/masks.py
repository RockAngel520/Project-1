import logging

logging.basicConfig(
    filename="logs/masks.log",
    encoding="utf-8",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
)

mask_card_number_logger = logging.getLogger("app.get_mask_card_number")
get_mask_account_logger = logging.getLogger("app.get_mask_account")


def get_mask_card_number(card_number: str) -> str:
    """Функция возвращающая маску введенного номера карты"""
    mask_card_number_logger.info('Запуск функции "get_mask_card_number"')
    str_card_number = str(card_number)  # перевод номера карты в строку

    if len(str_card_number) == 0:
        mask_card_number_logger.error("Введен пустой номер карты")
        raise AssertionError("Номер карты не может быть пустым")
    if len(str_card_number) != 16:
        mask_card_number_logger.error(f"Номер карты введен не из 16 цифр - {str_card_number}")
        raise AssertionError("Номер карты должен состоять из 16 цифр")
    if not str_card_number.isdigit():
        mask_card_number_logger.error(f"Номер карты включает не только цифры - {str_card_number}")
        raise AssertionError("Номер карты должен состоять только из цифр")

    mask_card_number = f"{str_card_number[:4]} {str_card_number[4:6]}** **** {str_card_number[-4:]}"
    mask_card_number_logger.info(f"К карте с номером {str_card_number} успешно применена маска")

    return mask_card_number


def get_mask_account(account_number: str) -> str:
    """Функция возвращающая маску введенного номера счета"""
    get_mask_account_logger.info('Запуск функции "get_mask_account"')
    str_account_number = str(account_number)  # перевод номера счета в строку

    if len(str_account_number) == 0:
        get_mask_account_logger.error("Введен пустой номер счета")
        raise AssertionError("Номер счета не может быть пустым")
    if len(str_account_number) != 20:
        get_mask_account_logger.error(f"Номер счета введен не из 20 цифр - {str_account_number}")
        raise AssertionError("Номер счета должен состоять из 20 цифр")
    if not str_account_number.isdigit():
        get_mask_account_logger.error(f"Номер счета включает не только цифры - {str_account_number}")
        raise AssertionError("Номер счет должен состоять только из цифр")

    mask_account_number = f"**{str_account_number[-4:]}"
    get_mask_account_logger.info(f"К счету с номером {get_mask_account_logger} успешно применена маска")

    return mask_account_number


if __name__ == '__main__':
    print(get_mask_card_number('1234123412341234'))
    print(get_mask_account('12341234123412341234'))
