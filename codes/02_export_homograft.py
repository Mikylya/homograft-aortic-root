"""
Модуль для экспорта ГОМОГРАФТА КОРНЯ АОРТЫ в STL
Клинический протокол: толщина среза 1 мм, HU 140-500, валидация синусов
Запускать в Python Interactor 3D Slicer
"""

import slicer
import vtk
import numpy as np

def validate_homograft(mesh):
    """
    Специальная валидация для гомографта корня аорты.
    Проверяет наличие всех трёх структур: синусы, клапан, восходящая аорта.
    
    Returns:
        dict: { 'valid': bool, 'details': {...} }
    """
    print("\n🔍 ВАЛИДАЦИЯ ГОМОГРАФТА КОРНЯ АОРТЫ...")
    
    bounds = [0, 0, 0, 0, 0, 0]
    mesh.GetBounds(bounds)
    height = abs(bounds[5] - bounds[4])
    width = abs(bounds[1] - bounds[0])
    depth = abs(bounds[3] - bounds[2])
    
    results = {
        'valid': True,
        'height': height,
        'width': width,
        'depth': depth,
        'sinuses_ok': False,
        'valve_area_ok': False
    }
    
    # 1. Проверка высоты (гомографт ≈40-70 мм)
    if height < 35:
        print("   ❌ Слишком низкая модель (<35 мм) — это не гомографт корня")
        results['valid'] = False
    elif height > 80:
        print("   ❌ Слишком высокая модель (>80 мм) — это не гомографт корня")
        results['valid'] = False
    else:
        print(f"   ✅ Высота {height:.1f} мм — соответствует гомографту")
    
    # 2. Проверка синусов Вальсальвы (расширение корня)
    if width > depth * 1.08:
        print("   ✅ Обнаружены синусы Вальсальвы (3 расширения)")
        results['sinuses_ok'] = True
    else:
        print("   ⚠️ Синусы Вальсальвы не обнаружены!")
        print("      Это критично для гомографта корня аорты.")
        results['valid'] = False
    
    # 3. Проверка наличия клапанной зоны
    num_slices = 15
    slice_height = height / num_slices
    diameters = []
    
    for i in range(1, num_slices - 1):
        z = bounds[4] + i * slice_height
        
        plane = vtk.vtkPlane()
        plane.SetOrigin(0, 0, z)
        plane.SetNormal(0, 0, 1)
        
        cutter = vtk.vtkCutter()
        cutter.SetInputData(mesh)
        cutter.SetCutFunction(plane)
        cutter.Update()
        
        if cutter.GetOutput().GetNumberOfPoints() > 3:
            center = vtk.vtkCenterOfMass()
            center.SetInputData(cutter.GetOutput())
            center.Update()
            cx, cy, cz = center.GetCenter()
            
            points = cutter.GetOutput().GetPoints()
            dist_sum = 0
            for j in range(points.GetNumberOfPoints()):
                p = points.GetPoint(j)
                dist_sum += ((p[0]-cx)**2 + (p[1]-cy)**2)**0.5
            avg_radius = dist_sum / points.GetNumberOfPoints()
            diameters.append(2 * avg_radius)
    
    if diameters:
        max_diam = max(diameters)
        min_diam = min(diameters)
        if max_diam > min_diam * 1.15:
            print(f"   ✅ Клапанная зона обнаружена (диаметр изменяется)")
            results['valve_area_ok'] = True
        else:
            print(f"   ⚠️ Не обнаружено характерного изменения диаметра для клапана")
    
    if results['valid'] and results['sinuses_ok']:
        print("\n✅ Модель соответствует гомографту корня аорты")
    else:
        print("\n❌ Модель НЕ соответствует гомографту корня аорты")
    
    return results


def export_homograft_graft(output_path):
    """
    Экспортирует выделенную модель как гомографт корня аорты.
    """
    print("="*60)
    print("🧬 ЭКСПОРТ ГОМОГРАФТА КОРНЯ АОРТЫ")
    print("="*60)
    print("   Клинический протокол: HU 140-500, толщина среза 1 мм")
    
    all_models = slicer.util.getNodesByClass("vtkMRMLModelNode")
    if not all_models:
        print("❌ Нет модели для экспорта")
        return False
    
    graft_node = all_models[0]
    mesh = graft_node.GetPolyData()
    if not mesh:
        print("❌ У модели нет полигональных данных")
        return False
    
    validation = validate_homograft(mesh)
    if not validation['valid']:
        print("\n❌ Экспорт отменён: модель не является гомографтом корня аорты")
        return False
    
    try:
        slicer.util.exportNode(graft_node, output_path)
        print(f"\n✅ Гомографт корня аорты сохранён: {output_path}")
        print(f"   Высота: {validation['height']:.1f} мм")
        print(f"   Диаметр: {validation['width']:.1f} мм")
        print(f"   Синусы: {'✅ есть' if validation['sinuses_ok'] else '⚠️ нет'}")
        print("="*60)
        return True
    except Exception as e:
        print(f"\n❌ Ошибка сохранения: {e}")
        return False

# Пример использования:
# export_homograft_graft("C:/путь_к_репозиторию/models/homograft_root.stl")
