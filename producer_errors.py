import time
from tasks import flaky_task

print('[ПРОДЮСЕР] Отправляю нестабильную задачу...')
task = flaky_task.delay(user_id=100)
print(f'[ПРОДЮСЕР] ID: {task.id}')

last_state = None
while not task.ready():
    if task.state != last_state:
        print(f'    [статус] -> {task.state}')
        last_state = task.state
    time.sleep(0.5)

print(f'[ПРОДЮСЕР] Итоговый статус: {task.state}')

if task.state == 'SUCCESS':
    print(f'[ПРОДЮСЕР] Результат: {task.result}')
else:
    print(f'[ПРОДЮСЕР] Задача упала с ошибкой: {type(task.result).__name__}: {task.result}')