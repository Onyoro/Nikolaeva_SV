import re
from collections import defaultdict
from datetime import datetime
import json
from typing import Dict, List, Tuple

class LogProcessor:
    """Класс для обработки и анализа лог-файлов"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []
        self.stats = defaultdict(int)
        
    def load_logs(self) -> List[str]:
        """Загрузка логов из файла"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.logs = f.readlines()
            return self.logs
        except FileNotFoundError:
            print(f"Файл {self.log_file} не найден")
            return []
    
    def parse_log_line(self, line: str) -> Dict:
        """Парсинг строки лога с оптимизацией через re"""
        # Оптимизированный паттерн с использованием re.compile
        pattern = re.compile(
            r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
            r'\[(?P<level>\w+)\] '
            r'(?P<message>.*)'
        )
        match = pattern.match(line.strip())
        if match:
            return match.groupdict()
        return None
    
    def analyze(self) -> Dict:
        """Анализ логов с агрегацией статистики"""
        # Оптимизация: однократный проход по логам
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
        """Фильтрация логов по уровню"""
        return [log for log in self.logs if self.parse_log_line(log) and 
                self.parse_log_line(log)['level'] == level]
    
    def export_json(self, output_file: str):
        """Экспорт результатов в JSON"""
        result = self.analyze()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

# Пример использования с оптимизацией
def main():
    processor = LogProcessor('sample.log')
    processor.load_logs()
    
    # Анализ с оптимизацией
    stats = processor.analyze()
    print(f"Статистика логов: {stats['statistics']}")
    
    # Экспорт в JSON
    processor.export_json('logs_analysis.json')

if __name__ == "__main__":
    main()