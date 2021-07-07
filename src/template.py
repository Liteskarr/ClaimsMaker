from docx import Document


def build_table_template(output_path: str):
    document = Document()
    table = document.add_table(4, 3)
    table.style = 'Table Grid'
    label_cells = table.rows[0].cells
    label_cells[0].text = '{%tc for label in labels %}'
    label_cells[1].text = '{{ label }}'
    label_cells[2].text = '{%tc endfor %}'
    start_content_cells = table.rows[1].cells
    start = start_content_cells[0].merge(start_content_cells[1]).merge(start_content_cells[2])
    start.text = '{%tr for row in table %}'
    content_cells = table.rows[2].cells
    content_cells[0].text = '{%tc for column in row %}'
    content_cells[1].text = '{{ column }}'
    content_cells[2].text = '{%tc endfor %}'
    end_content_cells = table.rows[3].cells
    end = end_content_cells[0].merge(end_content_cells[1]).merge(end_content_cells[2])
    end.text = '{%tr endfor %}'
    document.save(output_path)


if __name__ == '__main__':
    build_table_template('../templates/main_template.docx')
