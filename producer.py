import time

from tasks import generate_report

print('[ПРОДЮСЕР] Отправляю задачу на генерацию отчёта...')

task = generate_report.delay(report_id=5)

print(f'[ПРОДЮСЕР] Задача отправлена. Её ID: {task.id}')
print('[ПРОДЮСЕР] Я не жду выполнения. Продолжаю свою работу...')


for i in range(3):
    time.sleep(1)
    print(f'[ПРОДЮСЕР] Выполняю другую работу... {i+1}/3')

print(
    '[ПРОДЮСЕР] Основная работа завершена. Но отчёт всё ещё готовится в фоне.'
)