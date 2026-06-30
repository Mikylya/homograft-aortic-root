"""
Модуль для загрузки DICOM-данных в 3D Slicer
Запускать в Python Interactor 3D Slicer
"""

import slicer
import vtk

def load_dicom(folder_path):
    """
    Загружает DICOM из папки с проверкой качества данных.
    
    Args:
        folder_path (str): путь к папке с DICOM-файлами
        
    Returns:
        volume_node: узел с загруженной томографией, или None при ошибке
    """
    print("="*60)
    print("🔬 ЗАГРУЗКА DICOM-ДАННЫХ")
    print("="*60)
    print(f"   Папка: {folder_path}")
    
    try:
        # Загружаем данные
        loaded_nodes = slicer.util.loadDICOM(folder_path)
        
        if not loaded_nodes:
            raise ValueError("❌ Папка пуста или DICOM-файлы не найдены.")
        
        # Находим томографию
        volume_node = None
        for node in loaded_nodes:
            if node.IsA("vtkMRMLScalarVolumeNode"):
                volume_node = node
                break
        
        if not volume_node:
            raise ValueError("❌ Томография не найдена в загруженных данных.")
        
        # Проверяем качество
        spacing = volume_node.GetSpacing()
        slice_thickness = spacing[2]
        
        print(f"\n✅ Загружено: {volume_node.GetName()}")
        print(f"📏 Толщина среза: {slice_thickness:.2f} мм")
        
        if slice_thickness > 1.5:
            print("⚠️ ВНИМАНИЕ: толстые срезы (>1.5 мм).")
            print("   Модель может быть неточной.")
            print("   Для восходящей аорты с клапаном нужны срезы ≤ 1 мм.")
        else:
            print("✅ Качество хорошее. Можно строить модель.")
        
        # Проверка наличия контраста (анализ HU в центре среза)
        image_data = volume_node.GetImageData()
        if image_data:
            dims = image_data.GetDimensions()
            center_voxel = image_data.GetScalarComponentAsDouble(
                dims[0]//2, dims[1]//2, dims[2]//2, 0
            )
            if center_voxel > 100:
                print("   ✅ Похоже, есть контраст (HU > 100) — хорошо для аорты")
            else:
                print("   ⚠️ Низкий HU в центре. Возможно, нет контраста.")
                print("      Для модели аорты рекомендуется КТ с контрастом.")
        
        print("="*60)
        return volume_node
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        print("="*60)
        return None

# Пример использования:
# volume = load_dicom("C:/путь_к_DICOM")
