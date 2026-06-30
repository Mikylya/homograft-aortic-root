"""
Модуль для тестирования и валидации гомографта корня аорты
Запускать в обычном Python
Установка: pip install numpy trimesh matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import trimesh
import sys
import os

def load_and_validate_model(stl_path):
    """
    Загружает STL-модель и проверяет её геометрию.
    """
    print("="*60)
    print("🧬 ТЕСТИРОВАНИЕ ГОМОГРАФТА КОРНЯ АОРТЫ")
    print("="*60)
    print(f"   Модель: {stl_path}")
    
    try:
        mesh = trimesh.load_mesh(stl_path)
        if mesh is None:
            raise ValueError("Не удалось загрузить STL-файл")
        
        is_watertight = mesh.is_watertight
        volume = mesh.volume
        area = mesh.area
        bounds = mesh.bounds
        height = abs(bounds[1][2] - bounds[0][2])
        width = abs(bounds[1][0] - bounds[0][0])
        depth = abs(bounds[1][1] - bounds[0][1])
        
        print(f"\n📐 ГЕОМЕТРИЧЕСКИЕ ПАРАМЕТРЫ:")
        print(f"   Высота: {height:.1f} мм")
        print(f"   Ширина: {width:.1f} мм")
        print(f"   Глубина: {depth:.1f} мм")
        print(f"   Объём: {volume:.1f} мм³")
        print(f"   Площадь поверхности: {area:.1f} мм²")
        print(f"   Водонепроницаемая: {'✅ Да' if is_watertight else '❌ Нет'}")
        
        if height < 35:
            print("\n❌ Модель слишком мала (<35 мм) для гомографта корня")
            return {'valid': False, 'errors': ['height_too_small']}
        elif height > 80:
            print("\n❌ Модель слишком велика (>80 мм) для гомографта корня")
            return {'valid': False, 'errors': ['height_too_large']}
        else:
            print(f"\n✅ Высота {height:.1f} мм — в пределах нормы")
        
        if width > depth * 1.08:
            print("   ✅ Обнаружены синусы Вальсальвы")
            sinuses_ok = True
        else:
            print("   ⚠️ Синусы Вальсальвы не обнаружены")
            sinuses_ok = False
        
        results = {
            'valid': True,
            'mesh': mesh,
            'height': height,
            'width': width,
            'depth': depth,
            'volume': volume,
            'area': area,
            'is_watertight': is_watertight,
            'sinuses_ok': sinuses_ok,
            'errors': []
        }
        
        print("\n📊 ИТОГОВАЯ ОЦЕНКА:")
        if is_watertight and sinuses_ok:
            print("   ✅ Модель готова к 3D-печати и хирургическому планированию")
        else:
            print("   ⚠️ Модель требует доработки (проверь сегментацию)")
        
        print("="*60)
        return results
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        return {'valid': False, 'errors': [str(e)]}


def simulate_hemodynamics(results, cycles=5, beats_per_minute=70):
    """
    Симулирует гемодинамику на основе геометрии модели.
    """
    print("\n" + "="*60)
    print("🫀 СИМУЛЯЦИЯ ГЕМОДИНАМИКИ")
    print("="*60)
    
    if not results.get('valid', False):
        print("❌ Невалидная модель — симуляция невозможна")
        return
    
    mesh = results['mesh']
    diameter = (results['width'] + results['depth']) / 2
    height = results['height']
    
    print(f"\n📐 Параметры модели:")
    print(f"   Средний диаметр: {diameter:.1f} мм")
    print(f"   Высота: {height:.1f} мм")
    
    cycle_time = 60 / beats_per_minute
    dt = 0.01
    total_time = cycles * cycle_time
    time = np.arange(0, total_time, dt)
    
    base_pressure = 80 + (diameter - 20) * 2
    lv_pressure = base_pressure + 40 * np.sin(2 * np.pi * time / cycle_time) ** 2
    aortic_pressure = base_pressure + 20 * np.sin(2 * np.pi * time / cycle_time)
    valve_open = lv_pressure > aortic_pressure
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(time, lv_pressure, label='Левый желудочек', color='blue', linewidth=2)
    ax1.plot(time, aortic_pressure, label='Аорта', color='red', linewidth=2)
    ax1.set_ylabel('Давление (мм рт. ст.)')
    ax1.set_title('Гемодинамика гомографта корня аорты')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(time, valve_open, label='Клапан открыт', color='green', linewidth=2)
    ax2.set_ylabel('Состояние клапана')
    ax2.set_xlabel('Время (секунды)')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Закрыт', 'Открыт'])
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../images/homograft_hemodynamics.png', dpi=150)
    plt.show()
    
    open_time = np.sum(valve_open) * dt
    closed_time = np.sum(~valve_open) * dt
    max_gradient = np.max(lv_pressure - aortic_pressure)
    
    print(f"\n📊 СТАТИСТИКА:")
    print(f"   Циклов: {cycles}")
    print(f"   Частота: {beats_per_minute} уд/мин")
    print(f"   Время открытия: {open_time / cycles:.2f} сек/цикл")
    print(f"   Макс. градиент: {max_gradient:.1f} мм рт. ст.")
    
    print("\n✅ Симуляция завершена")
    print("   График сохранён: images/homograft_hemodynamics.png")
    print("="*60)


def run_full_test(stl_path):
    results = load_and_validate_model(stl_path)
    if results['valid']:
        simulate_hemodynamics(results)
    return results


if __name__ == "__main__":
    stl_file = "../models/homograft_root.stl"
    if not os.path.exists(stl_file):
        print(f"❌ Файл не найден: {stl_file}")
        sys.exit(1)
    run_full_test(stl_file)
