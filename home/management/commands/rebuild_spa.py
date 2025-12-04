# management/commands/rebuild_spa.py
import os
import subprocess
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Пересборка SPA проекта и автоматическое обновление ссылок в шаблоне spa_page.html'

    def add_arguments(self, parser):
        parser.add_argument(
            '--install',
            action='store_true',
            help='Выполнить предварительно npm install'
        )
        parser.add_argument(
            '--no-clean',
            action='store_true',
            help='НЕ удалять старые файлы с хэшами (очистка включена по умолчанию)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Подробный вывод процесса сборки'
        )

    def handle(self, *args, **options):
        # force = options.get('force', False)
        install = options.get('install', False)
        no_clean = options.get('no_clean', False)
        verbose = options.get('verbose', False)
        
        # Пути к проектам
        base_dir = Path(settings.BASE_DIR)
        spa_dir = base_dir / 'spa'
        static_spa_dir = base_dir / 'static' / 'spa'
        template_file = base_dir / 'home' / 'templates' / 'spa_page.html'
        
        # Проверяем существование директорий
        if not spa_dir.exists():
            self.stdout.write(self.style.ERROR(f"ОШИБКА: SPA директория не найдена: {spa_dir}"))
            return
            
        if not template_file.exists():
            self.stdout.write(self.style.ERROR(f"ОШИБКА: Шаблон не найден: {template_file}"))
            return

        self.stdout.write(self.style.SUCCESS("\n=== НАЧИНАЕМ ПЕРЕСБОРКУ SPA ПРОЕКТА ==="))
        
        # Шаг 0: Очистка старых файлов (включена по умолчанию)
        if not no_clean:
            self.stdout.write("Удаляем старые файлы с хэшами...")
            try:
                self.clean_old_hashed_files(static_spa_dir)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка очистки старых файлов: {e}"))
                return
        else:
            self.stdout.write("Пропускаем очистку старых файлов (--no-clean)")
        
        # Шаг 1: NPM Install (опционально)
        if install:
            self.stdout.write("Выполняем npm install...")
            try:
                # Windows compatibility - use npm.cmd
                result = subprocess.run(
                    ['npm.cmd', 'install'],
                    cwd=spa_dir,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    self.stdout.write(self.style.SUCCESS("NPM зависимости установлены"))
                else:
                    self.stdout.write(self.style.WARNING("NPM install завершен с предупреждениями"))
                    if verbose:
                        self.stdout.write(result.stderr)
            except subprocess.TimeoutExpired:
                self.stdout.write(self.style.ERROR("Таймаут npm install"))
                return
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка npm install: {e}"))
                return
        
        # Шаг 2: NPM Build
        self.stdout.write("Выполняем сборку проекта...")
        try:
            build_cmd = ['npm.cmd', 'run', 'build']
            if verbose:
                build_cmd.append('--verbose')
            
            result = subprocess.run(
                build_cmd,
                cwd=spa_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS("Сборка проекта завершена успешно"))
                if verbose:
                    self.stdout.write(result.stdout)
            else:
                self.stdout.write(self.style.ERROR("Ошибка сборки проекта"))
                self.stdout.write(result.stderr)
                return
                
        except subprocess.TimeoutExpired:
            self.stdout.write(self.style.ERROR("Таймаут сборки"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка сборки: {e}"))
            return

        # Шаг 3: Поиск нового JS файла
        self.stdout.write("Ищем новые собранные файлы...")
        assets_dir = static_spa_dir / 'assets'
        
        if not assets_dir.exists():
            self.stdout.write(self.style.ERROR(f"Директория assets не найдена: {assets_dir}"))
            return
            
        # Ищем JS файлы
        js_files = list(assets_dir.glob('index-*.js'))
        if not js_files:
            self.stdout.write(self.style.ERROR("JS файлы не найдены в assets"))
            return
            
        # Берем последний JS файл (по времени модификации)
        latest_js_file = max(js_files, key=lambda f: f.stat().st_mtime)
        
        # Ищем CSS файлы (опционально)
        css_files = list(assets_dir.glob('index-*.css'))
        latest_css_file = max(css_files, key=lambda f: f.stat().st_mtime) if css_files else None
        
        self.stdout.write(f"Найден JS файл: {latest_js_file.name}")
        if latest_css_file:
            self.stdout.write(f"Найден CSS файл: {latest_css_file.name}")
        
        # Шаг 4: Обновление шаблона
        self.stdout.write("Обновляем ссылки в шаблоне...")
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Обновляем JS ссылку
            js_pattern = r"{% static 'spa/assets/index-[^']+' %}"
            js_replacement = f"{{% static 'spa/assets/{latest_js_file.name}' %}}"
            content = re.sub(js_pattern, js_replacement, content)
            
            # Обновляем CSS ссылку если нужно
            # if latest_css_file:
            #     css_pattern = r"href=\"{% static 'spa/assets/index-[^']+\.css' %}\""
            #     css_replacement = f"href=\"{{% static 'spa/assets/{latest_css_file.name}' %}}\""
            #     content = re.sub(css_pattern, css_replacement, content)
            
            # Сохраняем обновленный файл
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.stdout.write(self.style.SUCCESS(f"Шаблон обновлен: {template_file}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка обновления шаблона: {e}"))
            return

        # Шаг 5: Финальный отчет
        self.stdout.write(self.style.SUCCESS("\n=== ПЕРЕСБОРКА SPA ЗАВЕРШЕНА УСПЕШНО! ==="))
        self.stdout.write(f"ОТЧЕТ:")
        if no_clean:
            self.stdout.write(f"   Очистка: Пропущена (--no-clean)")
        else:
            self.stdout.write(f"   Очистка: Выполнена")
        self.stdout.write(f"   JS файл: {latest_js_file.name}")
        # if latest_css_file:
        #     self.stdout.write(f"   CSS файл: {latest_css_file.name}")
        # self.stdout.write(f"   Размер JS: {self.format_file_size(latest_js_file.stat().st_size)}")
        # if latest_css_file:
        #     self.stdout.write(f"   Размер CSS: {self.format_file_size(latest_css_file.stat().st_size)}")
        self.stdout.write(f"   Шаблон: {template_file.name}")
        
        self.stdout.write("\nДля применения изменений перезапустите Django сервер")
        self.stdout.write("или используйте: python manage.py runserver")

    def format_file_size(self, size_bytes):
        """Форматирует размер файла в читаемый вид"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
            
    def clean_old_hashed_files(self, static_spa_dir):
        """Удаляет старые файлы с хэшами из директории assets"""
        assets_dir = static_spa_dir / 'assets'
        
        if not assets_dir.exists():
            self.stdout.write(self.style.WARNING(f"Директория assets не найдена: {assets_dir}"))
            return
        
        # Ищем все файлы с хэшами (index-*.js, index-*.css, *.woff2)
        patterns = ['index-*.js', 'index-*.css', '*.woff2']
        deleted_count = 0
        
        for pattern in patterns:
            files = list(assets_dir.glob(pattern))
            for file_path in files:
                try:
                    file_path.unlink()
                    self.stdout.write(f"  Удален: {file_path.name}")
                    deleted_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  Не удалось удалить {file_path.name}: {e}"))
        
        if deleted_count > 0:
            self.stdout.write(self.style.SUCCESS(f"Удалено {deleted_count} старых файлов с хэшами"))
        else:
            self.stdout.write(self.style.WARNING("Старые файлы с хэшами не найдены"))