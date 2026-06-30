"""
Модуль автоматической валидации геометрии аорты
Запускать в обычном Python
"""

import trimesh
import numpy as np

def validate_homograft_geometry(stl_path, verbose=True):
    results = {'valid': True, 'errors': [], 'warnings': [], 'metrics': {}}
    
    try:
        mesh = trimesh.load_mesh(stl_path)
        if mesh is None:
            results['valid'] = False
            results['errors'].append("Не удалось загрузить STL-файл")
            return results
        
        if not mesh.is_watertight:
            results['warnings'].append("Модель не водонепроницаема (watertight)")
        
        bounds = mesh.bounds
        width = abs(bounds[1][0] - bounds[0][0])
        depth = abs(bounds[1][1] - bounds[0][1])
        height = abs(bounds[1][2] - bounds[0][2])
        
        results['metrics']['width'] = width
        results['metrics']['depth'] = depth
        results['metrics']['height'] = height
        
        if height < 35:
            results['errors'].append(f"Высота {height:.1f} мм < 35 мм — модель слишком мала")
        elif height > 80:
            results['errors'].append(f"Высота {height:.1f} мм > 80 мм — модель слишком велика")
        
        if verbose:
            print("\n📊 РЕЗУЛЬТАТЫ ВАЛИДАЦИИ:")
            print(f"   Ширина: {width:.1f} мм")
            print(f"   Глубина: {depth:.1f} мм")
            print(f"   Высота: {height:.1f} мм")
            print(f"   Объём: {mesh.volume:.1f} мм³")
            print(f"   Треугольников: {len(mesh.faces)}")
            print(f"   Водонепроницаемая: {'Да' if mesh.is_watertight else 'Нет'}")
            
            if results['errors']:
                print(f"\n❌ ОШИБКИ:")
                for err in results['errors']:
                    print(f"   - {err}")
            if results['warnings']:
                print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ:")
                for warn in results['warnings']:
                    print(f"   - {warn}")
            
            if not results['errors'] and not results['warnings']:
                print("\n✅ МОДЕЛЬ ПРОШЛА ВСЕ ПРОВЕРКИ")
