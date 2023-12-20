import csv
import datetime as dt
from pathlib import Path
from collections import defaultdict
from pep_parse.settings import STATUS
from pep_parse.constants import DATETIME_FORMAT, RESULTS_PEP, FILE_NAME

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def open_spider(self, spider):
        self.pep_statuses = defaultdict(int)

    def process_item(self, item, spider):
        self.pep_statuses[item.get(STATUS)] += 1
        return item

    def close_spider(self, spider):
        pep_statuses = self.pep_statuses.items()
        RESULTS_PEP.extend(pep_statuses)
        RESULTS_DIR = BASE_DIR / 'results'
        RESULTS_DIR.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_path = RESULTS_DIR / FILE_NAME.format(now_formatted)

        with open(file_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='unix', quoting=csv.QUOTE_NONE)
            writer.writerows(RESULTS_PEP)
