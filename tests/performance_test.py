import time
import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics
from pathlib import Path


class PerformanceTester:
  def __init__(self, api_url="http://localhost:8000/api/analyze"):
    self.api_url = api_url
    self.results = []

  def test_single_request(self, image_path):
    try:
      start_time = time.time()

      with open(image_path, 'rb') as f:
        response = requests.post(
          self.api_url,
          files={'image': f},
          timeout=30
        )

      end_time = time.time()

      if response.status_code == 200:
        result_data = response.json()
        return {
          'success': True,
          'total_time': end_time - start_time,
          'processing_time': result_data.get('processing_time', 0),
          'status_code': response.status_code
        }
      else:
        return {
          'success': False,
          'error': f"HTTP {response.status_code}",
          'total_time': end_time - start_time
        }

    except Exception as e:
      return {
        'success': False,
        'error': str(e),
        'total_time': 0
      }

  def test_concurrent_requests(self, image_path, num_requests=10, max_workers=5):
    print(f"Запуск {num_requests} concurrent запросов...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
      futures = [executor.submit(self.test_single_request, image_path)
                 for _ in range(num_requests)]

      results = [future.result() for future in futures]

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    if successful:
      total_times = [r['total_time'] for r in successful]
      processing_times = [r['processing_time'] for r in successful]

      print(f"Успешных запросов: {len(successful)}/{num_requests}")
      print(f"Общее время (среднее): {statistics.mean(total_times):.2f}с")
      print(f"Время обработки моделью (среднее): {statistics.mean(processing_times):.2f}с")
      print(f"Максимальное время: {max(total_times):.2f}с")
      print(f"Минимальное время: {min(total_times):.2f}с")
      print(f"RPS: {len(successful) / sum(total_times):.2f}")

    if failed:
      print(f"\nОшибки: {len(failed)} запросов")
      for error in failed[:3]:
        print(f"  - {error['error']}")


if __name__ == "__main__":
  tester = PerformanceTester()

  test_image = "test_image_perf.jpg"

  if Path(test_image).exists():
    print("=== ТЕСТ ОДНОГО ЗАПРОСА ===")
    single_result = tester.test_single_request(test_image)
    print(f"Результат: {single_result}")

    print("\n=== ТЕСТ НАГРУЗКИ ===")
    tester.test_concurrent_requests(test_image, num_requests=20, max_workers=5)
  else:
    print(f"Тестовое изображение {test_image} не найдено")
