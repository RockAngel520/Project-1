import logging

import pandas as pd

from src.config import LOGS_PATH, PATH_OPERATIONS

logging.basicConfig(
    filename=LOGS_PATH / "services.log",
    encoding="utf-8",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
)

services_logger = logging.getLogger("app.services")


def search_word_in_operations(search_word: str) -> pd.DataFrame | None:
    "Функция поиска слова в описании или категории"
    services_logger.info('Запуск функции "search_word_in_operations"')
    try:
        with open(PATH_OPERATIONS, "rb") as excel_file:
            services_logger.info('Прочитан файл в функции "search_word_in_operations"')
            df = pd.read_excel(excel_file)
            df = df.where(pd.notnull(df), None)
            df_with_word = df[
                (df["Описание"].str.contains(search_word, case=False, na=False))
                | (df["Категория"].str.contains(search_word, case=False, na=False))
            ]
            return df_with_word
    except (FileNotFoundError, PermissionError) as e:
        services_logger.error(
            f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)} в функции search_word_in_operations"
        )
        print(f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)}")


# if __name__ == "__main__":
#     print(search_word_in_operations("газпромбанк"))
