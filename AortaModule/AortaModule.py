"""
AortaModule.py — GUI-модуль для 3D Slicer
Позволяет загружать DICOM, валидировать геометрию и экспортировать гомографт корня аорты
КАК ПОЛЬЗОВАТЬСЯ
Установка:
1. Скопируйте папку AortaModule/ в папку с твоим проектом
2. В 3D Slicer: Edit → Application Settings → Modules → Add
3. Добавь путь к папке с AortaModule/
4. Перезапустите 3D Slicer
5. Модуль появится в списке: Modules → Export → Homograft Aorta Exporter
"""

import slicer
from slicer.ScriptedLoadableModule import *
import vtk
import os

class HomograftAortaExporter(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Homograft Aorta Exporter"
        self.parent.categories = ["Export"]
        self.parent.dependencies = []
        self.parent.contributors = ["Sofya Mikulyak"]
        self.parent.helpText = """
        Экспорт гомографта корня аорты с валидацией.
        1. Загрузи DICOM
        2. Выдели аорту в Segment Editor
        3. Нажми 'Validate Geometry' для проверки синусов
        4. Нажми 'Export STL' для сохранения
        """


class HomograftAortaExporterWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        
        # Основной макет
        layout = self.layout
        layout.setSpacing(10)
        
        # ===== ЗАГОЛОВОК =====
        titleLabel = qt.QLabel("🧬 Homograft Aorta Exporter")
        titleLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        # ===== БЛОК 1: ЗАГРУЗКА DICOM =====
        loadGroupBox = qt.QGroupBox("1. Загрузка DICOM")
        loadLayout = qt.QVBoxLayout()
        
        self.loadButton = qt.QPushButton("📂 Загрузить DICOM")
        self.loadButton.connect('clicked(bool)', self.onLoadDICOM)
        loadLayout.addWidget(self.loadButton)
        
        self.loadStatusLabel = qt.QLabel("Статус: готов к загрузке")
        loadLayout.addWidget(self.loadStatusLabel)
        
        loadGroupBox.setLayout(loadLayout)
        layout.addWidget(loadGroupBox)
        
        # ===== БЛОК 2: ВАЛИДАЦИЯ =====
        validateGroupBox = qt.QGroupBox("2. Валидация геометрии")
        validateLayout = qt.QVBoxLayout()
        
        self.validateButton = qt.QPushButton("🔍 Проверить синусы Вальсальвы")
        self.validateButton.connect('clicked(bool)', self.onValidate)
        validateLayout.addWidget(self.validateButton)
        
        self.validateStatusLabel = qt.QLabel("Статус: не проверено")
        validateLayout.addWidget(self.validateStatusLabel)
        
        validateGroupBox.setLayout(validateLayout)
        layout.addWidget(validateGroupBox)
        
        # ===== БЛОК 3: ЭКСПОРТ =====
        exportGroupBox = qt.QGroupBox("3. Экспорт STL")
        exportLayout = qt.QVBoxLayout()
        
        self.exportButton = qt.QPushButton("📤 Экспортировать гомографт (STL)")
        self.exportButton.connect('clicked(bool)', self.onExport)
        exportLayout.addWidget(self.exportButton)
        
        self.exportPathLabel = qt.QLabel("Путь: не выбран")
        exportLayout.addWidget(self.exportPathLabel)
        
        exportGroupBox.setLayout(exportLayout)
        layout.addWidget(exportGroupBox)
        
        # ===== БЛОК 4: СТВОРКИ КЛАПАНА =====
        valveGroupBox = qt.QGroupBox("4. Створки клапана")
        valveLayout = qt.QVBoxLayout()
        
        self.valveButton = qt.QPushButton("🫀 Создать створки (Python)")
        self.valveButton.connect('clicked(bool)', self.onGenerateValve)
        valveLayout.addWidget(self.valveButton)
        
        self.valveStatusLabel = qt.QLabel("Статус: не созданы")
        valveLayout.addWidget(self.valveStatusLabel)
        
        valveGroupBox.setLayout(valveLayout)
        layout.addWidget(valveGroupBox)
        
        # ===== БЛОК 5: ВЫВОД СТАТУСА =====
        statusGroupBox = qt.QGroupBox("📋 Лог")
        statusLayout = qt.QVBoxLayout()
        
        self.statusText = qt.QTextEdit()
        self.statusText.setReadOnly(True)
        self.statusText.setMaximumHeight(150)
        statusLayout.addWidget(self.statusText)
        
        statusGroupBox.setLayout(statusLayout)
        layout.addWidget(statusGroupBox)
        
        # Инициализация
        self.volumeNode = None
        self.modelNode = None
        self.validationPassed = False


    def log(self, message):
        """Добавляет сообщение в лог"""
        self.statusText.append(f"[{slicer.util.now()}] {message}")
        print(message)
    
    
    def onLoadDICOM(self):
        """Загружает DICOM через диалог выбора папки"""
        self.log("🔍 Выбор папки с DICOM...")
        
        folderPath = qt.QFileDialog.getExistingDirectory(None, "Выберите папку с DICOM")
        if not folderPath:
            self.log("❌ Папка не выбрана")
            return
        
        self.log(f"📂 Загрузка: {folderPath}")
        
        try:
            # Используем код из 01_load_dicom.py
            loadedNodes = slicer.util.loadDICOM(folderPath)
            if not loadedNodes:
                self.log("❌ DICOM-файлы не найдены")
                return
            
            # Находим томографию
            for node in loadedNodes:
                if node.IsA("vtkMRMLScalarVolumeNode"):
                    self.volumeNode = node
                    break
            
            if not self.volumeNode:
                self.log("❌ Томография не найдена")
                return
            
            # Проверка толщины среза
            spacing = self.volumeNode.GetSpacing()
            sliceThickness = spacing[2]
            self.log(f"✅ Толщина среза: {sliceThickness:.2f} мм")
            
            if sliceThickness == 1.0:
                self.log("✅ Соответствует клиническому протоколу (1 мм)")
            elif sliceThickness > 1.5:
                self.log("⚠️ Толстые срезы (>1.5 мм) — модель будет неточной")
            
            self.loadStatusLabel.setText(f"Загружено: {self.volumeNode.GetName()}")
            self.log("✅ DICOM загружен успешно")
            
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
            self.loadStatusLabel.setText("Ошибка загрузки")
    
    
    def onValidate(self):
        """Проверяет наличие синусов Вальсальвы в выделенной модели"""
        self.log("🔍 Валидация геометрии...")
        
        # Находим все 3D-модели
        models = slicer.util.getNodesByClass("vtkMRMLModelNode")
        if not models:
            self.log("❌ Нет 3D-модели. Сначала сделай сегментацию.")
            self.validateStatusLabel.setText("Ошибка: нет модели")
            return
        
        self.modelNode = models[0]
        mesh = self.modelNode.GetPolyData()
        if not mesh:
            self.log("❌ У модели нет полигональных данных")
            return
        
        # Проверка синусов (упрощённая)
        bounds = [0, 0, 0, 0, 0, 0]
        mesh.GetBounds(bounds)
        width = abs(bounds[1] - bounds[0])
        depth = abs(bounds[3] - bounds[2])
        height = abs(bounds[5] - bounds[4])
        
        self.log(f"📏 Высота: {height:.1f} мм")
        self.log(f"📏 Ширина: {width:.1f} мм")
        self.log(f"📏 Глубина: {depth:.1f} мм")
        
        if height < 35 or height > 80:
            self.log("❌ Высота не соответствует гомографту (нужно 40-70 мм)")
            self.validateStatusLabel.setText("❌ Невалидная высота")
            self.validationPassed = False
            return
        
        if width > depth * 1.08:
            self.log("✅ Синусы Вальсальвы обнаружены!")
            self.validateStatusLabel.setText("✅ Синусы обнаружены")
            self.validationPassed = True
        else:
            self.log("⚠️ Синусы Вальсальвы не обнаружены")
            self.validateStatusLabel.setText("⚠️ Синусы не обнаружены")
            self.validationPassed = False
        
        self.log("✅ Валидация завершена")
    
    
    def onExport(self):
        """Экспортирует модель в STL"""
        self.log("📤 Экспорт STL...")
        
        if not self.validationPassed:
            self.log("⚠️ Валидация не пройдена. Экспорт отменён.")
            self.log("   Сначала нажми 'Проверить синусы Вальсальвы'")
            return
        
        if not self.modelNode:
            self.log("❌ Нет модели для экспорта")
            return
        
        # Выбор пути сохранения
        outputPath = qt.QFileDialog.getSaveFileName(
            None, "Сохранить как STL", "homograft_root.stl", "STL Files (*.stl)"
        )
        if not outputPath:
            self.log("❌ Экспорт отменён")
            return
        
        try:
            slicer.util.exportNode(self.modelNode, outputPath)
            self.log(f"✅ Экспорт успешен: {outputPath}")
            self.exportPathLabel.setText(f"Путь: {outputPath}")
        except Exception as e:
            self.log(f"❌ Ошибка экспорта: {e}")
    
    
    def onGenerateValve(self):
        """Запускает генерацию створок клапана через внешний Python-скрипт"""
        self.log("🫀 Запуск генерации створок...")
        
        # Путь к скрипту 03_create_valve.py
        # Предполагается, что он лежит в папке ../codes/ относительно модуля
        scriptPath = os.path.join(os.path.dirname(__file__), '..', 'codes', '03_create_valve.py')
        
        if not os.path.exists(scriptPath):
            self.log(f"❌ Скрипт не найден: {scriptPath}")
            return
        
        try:
            # Запускаем скрипт в отдельном процессе
            import subprocess
            result = subprocess.run(
                ['python', scriptPath],
                capture_output=True,
                text=True,
                timeout=60
            )
            self.log(result.stdout)
            if result.stderr:
                self.log(f"⚠️ {result.stderr}")
            self.log("✅ Генерация створок завершена")
            self.valveStatusLabel.setText("✅ Створки созданы")
        except subprocess.TimeoutExpired:
            self.log("❌ Превышено время выполнения")
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")


# Регистрация модуля в Slicer
# Автоматически выполняется при загрузке модуля
def register():
    import sys
    if not hasattr(sys.modules[__name__], 'instance'):
        sys.modules[__name__].instance = HomograftAortaExporter(slicer.scriptedLoadableModule)
    return sys.modules[__name__].instance


# Для тестирования внутри 3D Slicer
if __name__ == "__main__":
    import sys
    if not hasattr(sys.modules[__name__], 'widget'):
        sys.modules[__name__].widget = HomograftAortaExporterWidget()
