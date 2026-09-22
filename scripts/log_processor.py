import re
from collections import defaultdict
from datetime import datetime
import json
import time
from typing import Dict, List, Tuple


class LogProcessor:
    # Класс для обработки и анализа лог-файлов

    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []
        self.stats = defaultdict(int)
        self.pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
            r'\[(?P<level>\w+)\] '
            r'(?P<message>.*)'
        )

    def load_logs(self) -> List[str]:
        # Загрузка логов из файла
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.logs = f.readlines()
            return self.logs
        except FileNotFoundError:
            print(f"Файл {self.log_file} не найден")
            return []

    def parse_log_line(self, line: str) -> Dict:
        # Парсинг строки лога через re
        match = self.pattern.match(line.strip())
        if match:
            return match.groupdict()
        return None

    def analyze_slow(self) -> Dict:
        # Медленный способ: для каждого уровня отдельно проходим по всем логам. Вложенные циклы
        
        levels = ['ERROR', 'WARNING', 'INFO']
        statistics = {}

        for level in levels:                    # внешний цикл
            count = 0
            for line in self.logs:              # внутренний цикл
                parsed = self.parse_log_line(line)
                if parsed and parsed['level'] == level:
                    count += 1
            statistics[level] = count

        return {'statistics': statistics}

    def analyze(self) -> Dict:
        # Оптимизированный анализ: однократный проход по логам
        error_count = 0
        warning_count = 0
        info_count = 0

        parsed_logs = []

        for line in self.logs:
            parsed = self.parse_log_line(line)
            if parsed:
                parsed_logs.append(parsed)
                level = parsed['level']
                if level == 'ERROR':
                    error_count += 1
                elif level == 'WARNING':
                    warning_count += 1
                elif level == 'INFO':
                    info_count += 1

        return {
            'total_lines': len(self.logs),
            'parsed_lines': len(parsed_logs),
            'statistics': {
                'ERROR': error_count,
                'WARNING': warning_count,
                'INFO': info_count
            },
            'logs': parsed_logs
        }

    def filter_by_level(self, level: str) -> List[Dict]:
        # Фильтрация логов по уровню
        return [log for log in self.logs if self.parse_log_line(log) and
                self.parse_log_line(log)['level'] == level]

    def export_json(self, output_file: str):
        # Экспорт результатов в JSON
        result = self.analyze()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    processor = LogProcessor('sample.log')
    processor.load_logs()

    if not processor.logs:
        print("Нечего обрабатывать. Проверьте, что файл sample.log существует")
        return

    print("Обработчик логов")
    print(f"Всего строк: {len(processor.logs)}")

    # Медленный способ
    start = time.time()
    slow_result = processor.analyze_slow()
    slow_time = time.time() - start

    # Быстрый способ
    start = time.time()
    fast_result = processor.analyze()
    fast_time = time.time() - start

    print("\nСтатистика по уровням:")
    for level, count in fast_result['statistics'].items():
        print(f"  {level}: {count}")

    print("Сравнение производительности")
    print(f"Медленный способ (вложенные циклы): {slow_time:.6f} сек")
    print(f"Быстрый способ (словарь):            {fast_time:.6f} сек")
    if fast_time > 0:
        print(f"Ускорение: {slow_time / fast_time:.1f}x")

    # Проверяем, что результаты совпадают
    match = slow_result['statistics'] == fast_result['statistics']
    print(f"Результаты совпадают: {match}")

    # Экспорт в JSON
    processor.export_json('logs_analysis.json')
    print("\nРезультаты экспортированы в logs_analysis.json")


if __name__ == "__main__":
    main()

# Версия 1.0 — обработчик логов с оптимизацией