import time
import random

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

@app.task(
    autoretry_for=(ConnectionError,),
    max_retries=3,
    retry_backoff=True,
    retry_jitter=True
)
def flaky_task(user_id: int) -> str:
    """
    Имитация нестабильной задачи: ~50% шанс упасть.
    При падении Celery автоматически повторить её (до 3 раз).
    """
    print(f'--- [ВОРКЕР] flaky_task для user_id={user_id} ---')
    if random.random() < 0.5:
        raise ConnectionError('Не удалось достучаться до внешнего API')
    
    print(f'--- [ВОРКЕР] flaky_task: успех для user_id={user_id} ---')
    return f'Пользователь {user_id} обработан'