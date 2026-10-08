## Детали договора
- actionButton  | 
- tableEx  | Values: Catalog_Номенклатура.Наименование, Document_ЗаказКлиента_Товары.Количество, Document_ЗаказКлиента_Товары.Цена, Document_ЗаказКлиента_Товары.Сумма
- tableEx  | Values: Document_ЗаказКлиента_ЭтапыГрафикаОплаты.ПроцентПлатежа, Document_ЗаказКлиента_ЭтапыГрафикаОплаты.ДатаПлатежа, Document_ЗаказКлиента_ЭтапыГрафикаОплаты.СуммаПлатежа, Document_ЗаказКлиента_ЭтапыГрафикаОплаты.ВариантОплаты, Catalog_ДоговорыКонтрагентов.ТипДоговора, Catalog_ДоговорыКонтрагентов.Description, Catalog_ДоговорыКонтрагентов.Ref_Key, Catalog_ДоговорыКонтрагентов.АридаКопияДоговора, Catalog_ДоговорыКонтрагентов.АридаОригиналДоговора
- cardVisual  | Data: Catalog_ДоговорыКонтрагентов.Номер, Catalog_Партнеры.Контрагент, Catalog_АридаСезоны.Сезон, _Measures.ContractAmount(m), _Measures.ContractPayment%(m)

## Оплаты
- pivotTable  | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Axis_Calendar.Day | Values: _Measures.ПланОплатПоДоговорам(m), _Measures.Fact_FIFO_Matrix(m), _Measures.ПросроченныеОплаты(m)
- listSlicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- listSlicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- listSlicer  | Values: Грануляция по временам.Грануляция
- shape  | 
- textbox  | 
- lineClusteredColumnComboChart 'План оплат  по договорам' | Category: Axis_Calendar.По месяцам, Грануляция по временам.Грануляция | Y: _Measures.ПланОплатПоДоговорам(m), _Measures.Fact_FIFO2(m)
- image  | 
- listSlicer 'Дата' | Values: 
- actionButton  | 
- donutChart 'СуммаПлатежа by ВариантОплаты' | Category: Document_ЗаказКлиента_ЭтапыГрафикаОплаты.ВариантОплаты | Y: Document_ЗаказКлиента_ЭтапыГрафикаОплаты.СуммаПлатежа

## Договоры
- listSlicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- listSlicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- image  | 
- listSlicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- cardVisual 'Договоры' | Data: _Measures.ContractAmount(m), _Measures.Payment(m)
- textbox  | 
- shape  | 
- listSlicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- pivotTable  | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: _Measures.ContractAmount(m), _Measures.Payment(m), _Measures.ContractPayment%(m)
- actionButton  | 

## 🔖СТАБИЛИЗАЦИЯ МАРЖА
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- textbox  | 
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- actionButton  | 
- image  | 
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- pivotTable  | Rows: Catalog_Пользователи.Менеджер, Document_ЗаказКлиента.Number, Catalog_Номенклатура.Наименование | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.Стоимость по Реальному Входу(m), _Measures.Маржа по Реальному Входу(m), _Measures.Маржинальность по Реальному Входу(m)
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- shape  | 
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение

## Бонусы
- pivotTable 'регион' | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _BonusMeasures.Бонус по предоплате(m), _BonusMeasures.Бонус(m), _BonusMeasures.Бонус Всего(m)
- textbox  | 
- listSlicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- listSlicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- cardVisual 'Договоры' | Data: _BonusMeasures.Бонус Всего(m)
- clusteredColumnChart 'Заказы по дате поставки' | Category: Catalog_СтруктураПредприятия.Подразделение | Y: _BonusMeasures.Бонус Всего(m)
- actionButton  | 
- pivotTable 'производитель' | Rows: Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование, Catalog_Пользователи.Менеджер | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _BonusMeasures.Бонус по предоплате(m), _BonusMeasures.Бонус(m), _BonusMeasures.Бонус Всего(m)
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- listSlicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- listSlicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- image  | 
- shape  | 
- pivotTable 'менеджер' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _BonusMeasures.Бонус по предоплате(m), _BonusMeasures.Бонус(m), _BonusMeasures.Бонус Всего(m)
- bookmarkNavigator  | 

## договора и заказы для стабилизации
- card  | Values: _Measures.Mismatch_Count(m)
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- image  | 
- actionButton  | 
- listSlicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- listSlicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- listSlicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- tableEx  | Values: Catalog_СтруктураПредприятия.Подразделение, Catalog_ДоговорыКонтрагентов.Статус, Catalog_Партнеры.Контрагент, _Measures.ContractAmount(m), _Measures.OrderAmount(m), _Measures.Payment(m), Catalog_ДоговорыКонтрагентов.Номер, _Measures.Mismatch_Status(m), Catalog_ДоговорыКонтрагентов.ВидПодписания, Catalog_ДоговорыКонтрагентов.Оригинал договора, Catalog_ДоговорыКонтрагентов.Копия договора, Catalog_ДоговорыКонтрагентов.Статус ЭП
- pivotTable  | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер | Values: _Measures.ContractAmount(m), Document_ЗаказКлиента.Number, _Measures.OrderAmount(m)
- cardVisual 'Договоры' | Data: _Measures.ContractAmount(m), _Measures.Payment(m)
- listSlicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение

## План продаж
- clusteredColumnChart 'План Факт по Подразделениям' | Category: Catalog_СтруктураПредприятия.Подразделение | Y: _Measures.Plan_Amount(m), _Measures.OrderAmount(m)
- shape  | 
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- pivotTable 'по регионам' | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер | Values: _Measures.Plan_Qty(m), _Measures.Plan_Amount(m), _Measures.PlanAmount_Weight_%_подразд(m), _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_подразд(m), _Measures.Выполнение %(m)
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- cardVisual 'План продаж' | Data: _Measures.Plan_Amount(m), _Measures.Plan_Qty(m), _Measures.Выполнение %(m)
- actionButton  | 
- pivotTable  | Rows: Catalog_Пользователи.Менеджер, Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование | Values: _Measures.Plan_Qty(m), _Measures.Plan_Amount(m), _Measures.PlanAmount_Weight_%_подразд(m), _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_подразд(m), _Measures.Выполнение %(m)
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- textbox  | 
- pivotTable  | Rows: Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование, Catalog_Пользователи.Менеджер | Values: _Measures.Plan_Qty(m), _Measures.Plan_Amount(m), _Measures.PlanAmount_Weight_%_производ(m), _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_производ(m), _Measures.Выполнение %(m)
- bookmarkNavigator  | 
- image  | 

## ОП
- cardVisual  | Data: _Measures.Closing_Balance(m), Catalog_Склады.Склад, _Measures.Клиенты(m), _Measures.Purchases_Sum(m), _Measures.OrderAmount(m)
- cardVisual  | Data: _Measures.OrderAmount(m), _Measures.ActualSales(m), _Measures.Payment(m), _Measures.Менеджеры(m), _Measures.Выполнение %(m)
- listSlicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- actionButton  | 
- shape  | 
- image  | 
- listSlicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- listSlicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- cardVisual  | Data: _Measures.Plan_Amount(m), _Measures.OrderAmount(m), _Measures.Contract_Count(m), _Measures.Выполнение %(m), _Measures.PlanAmount_Weight_%_подразд(m)
- listSlicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент

## Реализация
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- actionButton  | 
- listSlicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- shape  | 
- listSlicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- image  | 
- textbox  | 
- pivotTable  | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- clusteredBarChart 'Заказы по складам' | Category: Catalog_Склады.Склад | Y: Document_РеализацияТоваровУслуг_Товары.Сумма
- cardVisual 'Реализации и оплаты' | Data: _Measures.ActualSales(m), _Measures.Payment(m)

## Товары
- textbox  | 
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- actionButton  | 
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Число формирования' | Values: 
- cardVisual 'Товары' | Data: _Measures.StockQtyClosing(m), _Measures.StockValueClosing(m)
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- slicer 'Производитель' | Values: Catalog_Производители.Производитель
- tableEx  | Values: Catalog_Номенклатура.Наименование, Catalog_Склады.Склад, Catalog_СерииНоменклатуры.ГоденДо, _Measures.Closing_Balance(m)
- slicer 'Срок годности' | Values: Catalog_СерииНоменклатуры.ГоденДо
- pivotTable  | Rows: Catalog_Номенклатура.Наименование, Catalog_Склады.Склад | Values: _Measures.StockQtyOpening(m), _Measures.StockValueOpening(m), _Measures.StockQtyExpenses(m), _Measures.StockValueExpenses(m), _Measures.StockQtyReceipts(m), _Measures.StockValueReceipts(m), _Measures.StockQtyClosing(m), _Measures.StockValueClosing(m)
- clusteredColumnChart  | Category: Catalog_Склады.Склад | Y: _Measures.StockValueClosing(m)
- pivotTable 'Отчет отгрузка' | Rows: Document_ЗаказКлиента.Number, Document_ЗаказКлиента_Товары.LineNumber | Values: _Measures.Номенклатура(m), _Measures.Менеджер(m), _Measures.Клиент(m), _Measures.Производитель(m), _Measures.Склад(m), Document_ЗаказКлиента_Товары.Цена, _Measures.OrderAmount(m), _Measures.Order_Nomen_Qty(m), _Measures.Отгружено по заказу(m), _Measures.Отгружено по ордерам(m), _Measures.Статус договора(m), _Measures.Условия оплаты(m), _Measures.Осталось отгрузить по ордерам(m), _Measures.В наличии остаток(m), _Measures.Остаток предоплаты(m)
- slicer 'Производитель' | Values: Catalog_Производители.Производитель
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- advancedSlicerVisual  | Values: Catalog_СерииНоменклатуры.Просроченный товар
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- image  | 
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- shape  | 

## Заказы
- tableEx  | Values: Catalog_ДоговорыКонтрагентов.Статус, Catalog_Партнеры.Контрагент, _Measures.ContractAmount(m), _Measures.Payment(m), Catalog_ДоговорыКонтрагентов.Номер, Catalog_ДоговорыКонтрагентов.ВидПодписания, Catalog_ДоговорыКонтрагентов.Оригинал договора, Catalog_ДоговорыКонтрагентов.Копия договора, Catalog_ДоговорыКонтрагентов.Статус ЭП
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- listSlicer  | Values: Грануляция по временам.Грануляция
- slicer 'Статус договора' | Values: Catalog_ДоговорыКонтрагентов.Статус
- bookmarkNavigator  | 
- pivotTable 'договора счет' | Columns: MatrixColumns.ColName | Rows: MatrixRows.GroupName, MatrixRows.RowName | Values: _Measures.MatrixValue(m)
- actionButton  | 
- pivotTable 'по менеджеру' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_3(m), _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- slicer 'Производитель' | Values: Catalog_Производители.Производитель
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- pieChart  | Category: Document_ЗаказКлиента.СпособДоставки | Y: Document_ЗаказКлиента.Ref_Key
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- shape  | 
- cardVisual 'Заказы и оплаты' | Data: _Measures.OrderAmount(m), _Measures.Payment(m)
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- image  | 
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- slicer 'дата между' | Values: Calendar.Date
- pivotTable 'по производителю' | Rows: Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование, Catalog_Пользователи.Менеджер | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_3(m), _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- donutChart  | Category: Document_ЗаказКлиента.СпособДоставки | Y: _Measures.OrderAmount(m)
- pivotTable 'по региону' | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер, Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_3(m), _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- lineChart 'Заказы по дате поставки' | Category: Axis_Calendar.По месяцам, Грануляция по временам.Грануляция | Y: _Measures.Order_Sum_СГрануляцией_Отгрузка(m), _Measures.РеализацияСГрануляцией(m), Грануляция по метрикам.Грануляция по метрикам
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- pivotTable 'по товару' | Rows: Catalog_Номенклатура.Наименование, Catalog_Пользователи.Менеджер | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_3(m), _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- actionButton  | 
- listSlicer  | Values: Грануляция по метрикам.Грануляция по метрикам
- slicer 'Сезон' | Values: Catalog_ДоговорыКонтрагентов.Сезон
- textbox  | 

## Заказы по статусам отгрузки
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- pivotTable 'по менеджеру' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Document_ЗаказКлиента.Number | Values: _Measures.OrderStatus(m), _Measures.OrderAmount(m), _Measures.ActualSales(m), _Measures.Оплата Распределенная (тескт)(m)
- cardVisual 'Заказы, оплаты и статусы по предоплатам' | Data: _Measures.OrderAmount(m), _Measures.Payment(m)
- actionButton  | 
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- image  | 
- shape  | 
- textbox  | 

## Маржинальность
- pivotTable 'менеджер' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.Стоимость по Реальному Входу(m), _Measures.Маржа по Реальному Входу(m), _Measures.Маржинальность по Реальному Входу(m)
- pivotTable 'регион' | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер | Values: _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.Стоимость по Реальному Входу(m), _Measures.Маржа по Реальному Входу(m), _Measures.Маржинальность по Реальному Входу(m)
- image  | 
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- bookmarkNavigator  | 
- actionButton  | 
- pivotTable 'производитель' | Rows: Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование, Catalog_Пользователи.Менеджер | Values: Document_ЗаказКлиента_Товары.Цена, _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), Document_ЗаказКлиента_АридаРеальныйВход.Стоимость, _Measures.Стоимость по Реальному Входу(m), _Measures.Маржа по Реальному Входу(m), _Measures.Маржинальность по Реальному Входу(m)
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- textbox  | 
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- cardVisual 'План продаж' | Data: _Measures.Plan_Amount(m), _Measures.OrderAmount(m), _Measures.Маржа по Реальному Входу(m), _Measures.Маржинальность по Реальному Входу(m)
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- clusteredColumnChart 'Маржа по Подразделениям' | Category: Catalog_СтруктураПредприятия.Подразделение | Y: _Measures.Маржа по Реальному Входу(m)
- shape  | 

## для стабилизации
- pivotTable 'СТАБ ПЛАН ОПЛАТ = ЗАКАЗЫ' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер | Values: _Measures.ПланОплатПоДоговорам(m), _Measures.OrderAmount(m), Document_ЗаказКлиента.Number, _Measures.Fact_FIFO2(m)
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- actionButton  | 
- slicer 'номер договора' | Values: Catalog_ДоговорыКонтрагентов.Номер
- actionButton  | 
- cardVisual 'Все виды оплат по отчету' | Data: _Measures.Оплата Распределенная (тескт)(m), _Measures.Оплата Распределенная(m), _Measures.Payment(m), _Measures.Fact_FIFO_Matrix(m)
- actionButton  | 
- sankey02300D1BE6F5427989F3DE31CCA9E0F32020 'Договоры по видам подписания' | Weight: _Measures.Договоры, кол-во(m) | Source: Catalog_ДоговорыКонтрагентов.Статус | Destination: Catalog_ДоговорыКонтрагентов.ВидПодписания | SourceLabels: _Measures.Договоры, кол-во(m)
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- tableEx 'Факт оплат' | Values: Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, AccumulationRegister_РасчетыСКлиентами.Сумма, AccumulationRegister_РасчетыСКлиентами.Date, AccumulationRegister_РасчетыСКлиентами.Recorder_Type
- pivotTable 'по менеджеру' | Rows: Catalog_Пользователи.Менеджер, Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_Номенклатура.Наименование | Values: Document_ЗаказКлиента.Number, _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_3(m), _Measures.ActualSales(m), Document_ПоступлениеБезналичныхДенежныхСредств.Number, _Measures.Оплата Распределенная (тескт)(m)
- pivotTable  | Rows: Catalog_СтруктураПредприятия.Подразделение, Catalog_Пользователи.Менеджер, Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование | Values: _Measures.Plan_Qty(m), _Measures.Plan_Amount(m), _Measures.PlanAmount_Weight_%_подразд(m), _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m), _Measures.OrderAmount_Weight_%_подразд(m), _Measures.Plan_Perfomance_%_подразд(m)
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- actionButton  | 
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- tableEx 'План оплат' | Values: Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Document_ЗаказКлиента_ЭтапыГрафикаОплаты.СуммаПлатежа, Document_ЗаказКлиента_ЭтапыГрафикаОплаты.Date
- cardVisual 'План продаж' | Data: _Measures.Plan_Amount(m), _Measures.Plan_Qty(m)
- slicer 'Номенклатура' | Values: Catalog_ТоварныеКатегории.Description
- tableEx  | Values: Catalog_Пользователи.Менеджер, Catalog_Производители.Производитель, Catalog_Номенклатура.Наименование, Document_ЗаказКлиента.Number, _Measures.Order_Nomen_Qty(m), _Measures.OrderAmount(m)
- cardVisual 'Заказы и оплаты' | Data: _Measures.OrderAmount(m), _Measures.Payment(m)
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- tableEx 'Договор' | Values: Catalog_Партнеры.Контрагент, Catalog_ДоговорыКонтрагентов.Номер, Catalog_ДоговорыКонтрагентов.Сумма
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Номенклатура' | Values: Catalog_ТоварныеКатегории.Description
- actionButton  | 
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение

## Приобретение
- clusteredColumnChart 'План Факт по Подразделениям' | Category: Calendar.YearMonthFull | Y: _Measures.OrderP_Sum(m), _Measures.Purchases_Sum(m)
- slicer 'Контрагент' | Values: Catalog_Партнеры.Контрагент
- slicer 'Товарная категория' | Values: Catalog_ТоварныеКатегории.Description
- slicer 'Тип культур' | Values: Catalog_АридаТипыКультурыИПрепаратов.Description
- shape  | 
- slicer 'Регион' | Values: Catalog_СтруктураПредприятия.Подразделение
- actionButton  | 
- slicer 'Группа препаратов' | Values: Catalog_АридаГруппыПрепаратов.Description
- image  | 
- cardVisual 'Приход товаров' | Data: _Measures.OrderP_Sum(m), _Measures.Purchases_Sum(m), _Measures.OrderP_Qty(m), _Measures.Purchases_Qty(m)
- slicer 'Сезон' | Values: Catalog_АридаСезоны.Сезон
- slicer 'Номенклатура' | Values: Catalog_Номенклатура.Наименование
- slicer 'Менеджер' | Values: Catalog_Пользователи.Менеджер
- pivotTable  | Rows: Catalog_Производители.Производитель, Document_ЗаказПоставщику.Number, Catalog_Номенклатура.Наименование | Values: _Measures.OrderP_Sum(m), _Measures.Purchases_Sum(m), _Measures.OrderP_Qty(m), _Measures.Purchases_Qty(m), _Measures.Оплаты_Поставщикам(m)

