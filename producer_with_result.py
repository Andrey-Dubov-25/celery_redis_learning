import time

from tasks import generate_report


print('[ПРОДЮСЕР] Отправляю задачу на генерацию отчёта...')
task = generate_report.delay(report_id=5)
print(f'[ПРОДЮСЕР] Задача отправлена. Её ID: {task.id}')

print('--- Начинаю опрашивать статус (не блокируя основной поток) ---')

last_state = None

while not task.ready():
    current_state = task.state

    if current_state != last_state:
        print(f'    [статус изменился] -> {current_state}')
        last_state = current_state
    time.sleep(1)

print(f'[ПРОДЮСЕР] Задача завершена.')
print(f'[ПРОДЮСЕР] Итоговый статус: {task.state}')
print(f'[ПРОДЮСЕР] Результат: {task.result}')
