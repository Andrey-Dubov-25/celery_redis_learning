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

@app.task
def add(x: int, y: int) -> int:
    print(f'--- [ВОРКЕР] add({x}, {y}) ---')
    return x + y

@app.task
def multiply(x: int, y: int) -> int:
    print(f'--- [ВОРКЕР] multiply({x}, {y}) ---')
    return x * y

@app.task
def subtract(x: int, y: int) -> int:
    print(f'--- [ВОРКЕР] subtract({x}, {y}) ---')
    return x - y

@app.task
def fetch_item(item_id: int) -> dict:
    """Имитиция загрузки элемента из внешнего API."""
    time.sleep(random.uniform(0.5, 2.0))
    print(f'--- [ВОРКЕР] fetch_item({item_id}) ---')
    return {'id': item_id, 'name': f'Item-{item_id}'}

@app.task
def process_chunk(chunk_id: int) -> str:
    """Обработка куска данных."""
    time.sleep(random.uniform(0.3, 1.0))
    print(f'--- [ВОРКЕР] process_chunk({chunk_id}) ---')
    return f'chunk-{chunk_id}-done'

@app.task
def aggregate(results: list) -> dict:
    """Callback: получает список результатов всех задач группы."""
    print(f'--- [ВОРКЕР] aggregate получил {len(results)} результатов ---')
    return {
        'total': len(results),
        'items': results,
        'status': 'all_ok'
    }
