import pandas as pd

def split_hours_for_two_teachers(df_current, df_past, discipline, load_type, groups):
    # ... (ваша функция остается без изменений) ...
    key_cols = ['Дисциплина', 'Вид нагрузки', 'Группы']
    
    mask_past = (
        (df_past['Дисциплина'] == discipline) & 
        (df_past['Вид нагрузки'] == load_type) & 
        (df_past['Группы'] == groups)
    )
    past_rows = df_past[mask_past]
    
    if len(past_rows) == 2:
        total_past_hours = past_rows['Нагрузка'].sum()
        
        if total_past_hours > 0:
            prop1 = past_rows.iloc[0]['Нагрузка'] / total_past_hours
            prop2 = past_rows.iloc[1]['Нагрузка'] / total_past_hours
            
            mask_current = (
                (df_current['Дисциплина'] == discipline) & 
                (df_current['Вид нагрузки'] == load_type) & 
                (df_current['Группы'] == groups)
            )
            current_idx = df_current[mask_current].index
            
            if len(current_idx) > 0:
                idx = current_idx[0]
                total_current_hours = df_current.loc[idx, 'Нагрузка']
                
                row1 = df_current.loc[idx].copy()
                row2 = df_current.loc[idx].copy()
                
                row1['Нагрузка'] = total_current_hours * prop1
                row1['Табельный №'] = past_rows.iloc[0]['Табельный №']
                row1['ФИО'] = past_rows.iloc[0]['ФИО']
                row1['Должность'] = past_rows.iloc[0]['Должность']
                
                row2['Нагрузка'] = total_current_hours * prop2
                row2['Табельный №'] = past_rows.iloc[1]['Табельный №']
                row2['ФИО'] = past_rows.iloc[1]['ФИО']
                row2['Должность'] = past_rows.iloc[1]['Должность']
                
                df_current = df_current.drop(idx)
                df_current = pd.concat([df_current, pd.DataFrame([row1, row2])], ignore_index=True)
                
                print(f"✅ Нагрузка по '{discipline}' ({load_type}, {groups}) успешно разделена.")
                print(f"   Пропорция: {prop1:.2f} ({past_rows.iloc[0]['ФИО']}) к {prop2:.2f} ({past_rows.iloc[1]['ФИО']})")
            else:
                print(f"⚠️ Строка не найдена в текущем году.")
        else:
            print(f"⚠️ Сумма часов в прошлом году равна 0, деление невозможно.")
    else:
        print(f"❌ Условие не выполнено: в прошлом году было не 2 преподавателя (найдено: {len(past_rows)}).")
        
    return df_current


# === ГЛАВНЫЙ КОД - УБРАНЫ КОММЕНТАРИИ ===
if __name__ == "__main__":
    try:
        # 1. Загружаем файлы
        print("Загрузка файлов...")
        df_past = pd.read_excel('Список 15вар - осень.xls')
        df_current = pd.read_excel('Список 15вар - весна.xls')
        print("✅ Файлы загружены")
        
        # 2. Выберите конкретную дисциплину из ваших файлов
        # Например, из файла "осень" я вижу:
        # - "Техническое документоведение (ЕСКД, ЕСТПП, ЕСТД)" с ПЗ для Т1О-301Б-17
        # - "История профессии" с ЛР для Т11О-101Б-19 (там 4 преподавателя)
        
        target_discipline = 'Техническое документоведение (ЕСКД, ЕСТПП, ЕСТД)'
        target_load_type = 'ПЗ'
        target_groups = 'Т1О-301Б-17'
        
        print(f"\nОбработка: {target_discipline} ({target_load_type}, {target_groups})")
        
        # 3. Применяем функцию
        df_current = split_hours_for_two_teachers(
            df_current, 
            df_past, 
            discipline=target_discipline, 
            load_type=target_load_type, 
            groups=target_groups
        )
        
        # 4. Сохраняем результат
        df_current.to_excel('Результат_задача_6.xlsx', index=False)
        print("\n✅ Готово! Файл сохранен как 'Результат_задача_6.xlsx'")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()