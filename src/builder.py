from typing import List

from docxtpl import DocxTemplate

from record import Record
from src.data_parser import parse_file


def build(records: List[Record], metadata: dict, template: DocxTemplate, output_path: str):
    any_debit = any(map(lambda x: x.Debit, records))
    any_credit = any(map(lambda x: x.Credit, records))
    labels = ['Дата', '№', 'Номер счета', 'ИНН', 'Контрагент'] + (['Сумма по дебету'] if any_debit else []) + \
             (['Сумма по кредиту'] if any_credit else []) + ['Наименование платежа']
    table = map(lambda x: [x.Date.strftime('%d.%m.%Y'),
                           x.Number,
                           x.TargetAccount,
                           x.TargetINN,
                           x.TargetName
                           ] + ([x.Debit] if any_debit else []) + ([x.Credit] if any_credit else []) + [x.Reason],
                records)
    context = {
        'labels': labels,
        'table': table,
    }
    template.render(context)
    template.save(output_path)


if __name__ == '__main__':
    tmpl = DocxTemplate('../main_template.docx')
    build(
        list(filter(lambda x: x.TargetINN == 7602071636, parse_file('../data.txt'))),
        {},
        tmpl,
        '../res.docx'
    )
