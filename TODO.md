# Tareas para Implementar HashTable para savegame.json

## Plan Aprobado
- [x] Paso 1: Crear Laboratorio1_EstructuraDeDatos/TODO.md (este archivo)
- [x] Paso 2: Crear hashtable.py con HashTable completa (load/save savegame)
- [x] Paso 3: Probar carga de savegame.json en HashTable (ver comando abajo)
- [ ] Paso 4: Opcional: Integrar en save_system.py/PlayerManager
- [x] Paso 5: Completar tarea

¡Completado! hashtable.py lista y probada.

## Comando para Test Manual:
```
cd Laboratorio1_EstructuraDeDatos
python -c "from hashtable import HashTable; ht=HashTable(); ht.load('game/savegame.json'); print(ht.keys()); print(ht.get('oscar')); ht.save('game/test_save.json')"
```

Archivos creados: hashtable.py, TODO.md. Listo para integración opcional.

