from typing import List

from docxtpl import DocxTemplate

from record import Record


def build(records: List[Record], metadata: dict, template: DocxTemplate, output_path: str):
    sum_debit = sum(map(lambda x: x.Debit, records))
    sum_credit = sum(map(lambda x: x.Credit, records))
    labels = ['Дата', '№', 'Номер счета', 'ИНН', 'Контрагент'] + (['Сумма по дебету'] if sum_debit else []) + \
             (['Сумма по кредиту'] if sum_credit else []) + ['Наименование платежа']
    table = map(lambda x: [x.Date,
                           x.Number,
                           x.Account,
                           x.INN,
                           x.Name
                           ] + ([x.Debit] if sum_debit else []) + ([x.Credit] if sum_credit else []) + [x.Reason],
                records)
    context = {
        'labels': labels,
        'table': table,
        'number': metadata.get('number'),
        'date': metadata.get('date'),
        'address': metadata.get('address'),
        'name': metadata.get('name'),
        'sum_debit': sum_debit,
        'sum_credit': sum_credit
    }
    template.render(context)
    template.save(output_path)
