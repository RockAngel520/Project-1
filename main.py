from src.reports import spending_by_category
from src.utils import read_excel_file
from src.views import json_answer_main, json_simple_search

if __name__ == "__main__":
    print(json_answer_main('2021-12-12 14:12:12'))
    print(json_simple_search('авиа'))
    print(spending_by_category(read_excel_file(), "Книги", "2021-05-29 14:12:12"))

