from celery import chain, group, chord
from tasks import add, multiply, subtract, fetch_item, process_chunk, aggregate

workflow = chain(
    add.s(2, 3),
    multiply.s(10),
    subtract.s(5)
)
# workflow = add.s(2, 3) | multiply.s(10) | subtract.s(5)

task = workflow.apply_async()
print(f'ID цепочки: {task.id}')
print(f'Результат: {task.get(timeout=10)}')


jobs = group(fetch_item.s(i) for i in range(1, 6))
task = jobs.apply_async()

print(f'Группа ID: {task.id}')
result = task.get(timeout=15)
print(f'Результаты (порядок совпадает с порядком задач):')
for r in result:
    print(f"  {r}")


workflow = chord(
    (process_chunk.s(i) for i in range(1, 6)), aggregate.s()
)
task = workflow.apply_async()
print(f'Chord ID: {task.id}')
print(f'Итог: {task.get(timeout=20)}')