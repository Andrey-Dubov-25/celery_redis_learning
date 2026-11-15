import time

from celery_app import app


@app.task
def generate_report(report_id: int) -> str:
    """
    Имитация долгой операции по генерации отчета.
    В реальной жизни здесь могла бы быть работа с файлами, БД и т.д.
    """
    print(f'--- [ВОРКЕР] Начинаю генерацию отчёта №{report_id} ---')
    time.sleep(10)
    result = f'Отчёт №{report_id} успешно сгенерирован'
    print(f'--- [ВОРКЕР] {result} ---')
    return result
