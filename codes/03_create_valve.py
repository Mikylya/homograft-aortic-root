"""
Модуль для создания СТВОРОК КЛАПАНА для гомографта корня аорты
Запускать в обычном Python
Установка: pip install numpy trimesh
"""

import numpy as np
import trimesh

def create_homograft_leaflets(radius=13, height=15, thickness=1.0):
    """
    Создаёт три створки для гомографта корня аорты.
    Створки имеют анатомическую форму полумесяца.
    """
    theta = np.linspace(0, np.pi, 30)
    r = radius * (1 - 0.25 * np.sin(theta))
    
    top_x = r * np.cos(theta)
    top_y = r * np.sin(theta)
    top_z = np.ones_like(theta) * height
    
    bottom_x = r * np.cos(theta) * 0.9
    bottom_y = r * np.sin(theta) * 0.9
    bottom_z = np.zeros_like(theta)
    
    vertices = []
    faces = []
    
    for i in range(len(theta) - 1):
        vertices.append([top_x[i], top_y[i], top_z[i]])
        vertices.append([bottom_x[i], bottom_y[i], bottom_z[i]])
        vertices.append([top_x[i+1], top_y[i+1], top_z[i+1]])
        idx = len(vertices) - 3
        faces.append([idx, idx+1, idx+2])
        
        vertices.append([bottom_x[i], bottom_y[i], bottom_z[i]])
        vertices.append([bottom_x[i+1], bottom_y[i+1], bottom_z[i+1]])
        vertices.append([top_x[i+1], top_y[i+1], top_z[i+1]])
        idx = len(vertices) - 3
        faces.append([idx, idx+1, idx+2])
    
    leaflet = trimesh.Trimesh(vertices=vertices, faces=faces)
    leaflet = leaflet.simplify_quadric_decimation(200)
    return leaflet


def create_homograft_valve(radius=13, height=15):
    """
    Размещает три створки по кругу (как в настоящем клапане).
    """
    leaflet = create_homograft_leaflets(radius, height)
    
    leaflets = []
    for i in range(3):
        l = leaflet.copy()
        angle = i * 2 * np.pi / 3
        rot = trimesh.transformations.rotation_matrix(angle, [0, 0, 1])
        l.apply_transform(rot)
        shift = radius * 0.3
        l.apply_translation([shift * np.cos(angle), shift * np.sin(angle), 0])
        leaflets.append(l)
    
    return trimesh.util.concatenate(leaflets)


if __name__ == "__main__":
    print("="*60)
    print("🫀 ГЕНЕРАЦИЯ СТВОРОК ДЛЯ ГОМОГРАФТА КОРНЯ АОРТЫ")
    print("="*60)
    
    valve = create_homograft_valve(radius=13, height=15)
    valve.export("../models/valve_leaflets.stl")
    
    print("✅ Створки клапана сохранены: models/valve_leaflets.stl")
    print("   Радиус: 13 мм")
    print("   Высота: 15 мм")
    print("="*60)
