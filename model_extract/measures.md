### _BonusMeasures[Бонус]  folder=Бонусы fmt=#,0
```dax
SUM('Document_ЗаказКлиента_АридаБонусы'[Бонус])
```

### _BonusMeasures[Бонус по предоплате]  folder=Бонусы fmt=#,0
```dax
SUM('Document_ЗаказКлиента_АридаБонусы'[БонусПредоплата])
```

### _BonusMeasures[Бонус Всего]  folder=Бонусы fmt=#,0
```dax
SUM('Document_ЗаказКлиента_АридаБонусы'[БонусВсего])
```

### _Measures[Expenses]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_ТоварыНаСкладах'[ВНаличии]),
    'AccumulationRegister_ТоварыНаСкладах'[RecordType] = "Expense"
)
```

### _Measures[Receipts]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_ТоварыНаСкладах'[ВНаличии]),
    'AccumulationRegister_ТоварыНаСкладах'[RecordType] = "Receipt"
)
```

### _Measures[Opening_Balance]  folder=Товары fmt=#,0
```dax
VAR vDate = MIN('Calendar'[Date])
RETURN
CALCULATE(
    SUMX('AccumulationRegister_ТоварыНаСкладах', 
        IF('AccumulationRegister_ТоварыНаСкладах'[RecordType] = "Receipt", 1, -1) * 'AccumulationRegister_ТоварыНаСкладах'[ВНаличии]
    ),
    FILTER(ALL('Calendar'), 'Calendar'[Date] < vDate)
)
```

### _Measures[Plan_Amount]  folder=План fmt=#,0
```dax
SUM('AccumulationRegister_ПланыПродаж'[Сумма])
```

### _Measures[OrderAmount]  folder=Заказы fmt=
```dax
SUM('Document_ЗаказКлиента_Товары'[Сумма])

formatStringDefinition = "#,##0;-#,##0;"
```

### _Measures[ActualSales]  folder=Реализации fmt=#,0
```dax
CALCULATE(
    SUM('Document_РеализацияТоваровУслуг_Товары'[Сумма]),
    'Document_РеализацияТоваровУслуг'[ЗаказКлиента] <> "00000000-0000-0000-0000-000000000000"
)
```

### _Measures[Payment]  folder=Реализации fmt=#,0
```dax
SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма])
```

### _Measures[Debt]  folder=Реализации fmt=0
```dax
SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма])
```

### _Measures[Выполнение %]  folder=План fmt=0%;-0%;0%
```dax
DIVIDE([OrderAmount], [Plan_Amount])
```

### _Measures[Plan_Variance]  folder=План fmt=
```dax
- [Plan_Amount]
```

### _Measures[Plan_Qty]  folder=План fmt=#,0
```dax
SUM('AccumulationRegister_ПланыПродаж'[Количество])
```

### _Measures[Plan_Qty_Variance (временно с заказами)]  folder=План fmt=
```dax
[OrderAmount] - [Plan_Qty]
```

### _Measures[ContractAmount]  folder=Договоры fmt=
```dax
SUM('Catalog_ДоговорыКонтрагентов'[Сумма])

formatStringDefinition = "#,##0;-#,##0;"
```

### _Measures[OrderAmount_OnlyWithPlan]  folder=Заказы fmt=#,0
```dax
IF(
    [Plan_Amount] > 0,
    COALESCE(SUM('Document_ЗаказКлиента'[СуммаДокумента]), 0),
    BLANK()
)
```

### _Measures[ContractPayment%]  folder=Договоры fmt=0.0%;-0.0%;0.0%
```dax
DIVIDE(
    [Payment],
    [ContractAmount],
    0)
```

### _Measures[Order_Nomen_Sum]  folder=Заказы fmt=
```dax
SUM('Document_ЗаказКлиента_Товары'[Сумма])
```

### _Measures[Order_Nomen_Qty]  folder=Заказы fmt=#,0
```dax
SUM('Document_ЗаказКлиента_Товары'[Количество])
```

### _Measures[Contract_Count]  folder=Договоры fmt=0
```dax
DISTINCTCOUNT('Catalog_ДоговорыКонтрагентов'[Ref_Key])
```

### _Measures[Closing_Balance]  folder=Товары fmt=#,0
```dax
VAR vToday = TODAY()
VAR vSelectedDate = MAX('Calendar'[Date])
VAR vTargetDate = IF(ISFILTERED('Calendar'[Date]), vSelectedDate, vToday)
VAR vResult = 
    CALCULATE(
        [Opening_Balance] + [Receipts] - [Expenses],
        'Calendar'[Date] <= vTargetDate
    )
RETURN
IF(
    vTargetDate <= vToday,
    vResult
)
```

### _Measures[Revenue]  folder=Маржинальность fmt=#,0
```dax
SUM('AccumulationRegister_ВыручкаИСебестоимостьПродаж'[СуммаВыручкиБезНДС])
```

### _Measures[Стоимость по Реальному Входу]  folder=Маржинальность fmt=#,0
```dax
SUM('Document_ЗаказКлиента_АридаРеальныйВход'[СуммаСтоимость])
```

### _Measures[GrossProfit]  folder=Маржинальность fmt=#,0
```dax
[Revenue] - [Стоимость по Реальному Входу]
```

### _Measures[GrossMargin_Pct]  folder=Маржинальность fmt=0%;-0%;0%
```dax
DIVIDE([GrossProfit], [Revenue])
```

### _Measures[ПланОплатПоДоговорам]  folder=Договоры fmt=#,0
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[СуммаПлатежа]),
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Date])
)
```

### _Measures[ФактОплатДляДоговоров]  folder=Договоры fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма]),
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'AccumulationRegister_РасчетыСКлиентами'[Date])
)
```

### _Measures[%ОплатОтносительноПлана]  folder=Договоры fmt=#,0%;-#,0%;#,0%
```dax
DIVIDE(
    [ФактОплатДляДоговоров],
    [ПланОплатПоДоговорам],
    0)
```

### _Measures[Оплата Распределенная]  folder=Договоры fmt=#,0
```dax
SUMX(
    VALUES('AccumulationRegister_РасчетыСКлиентами'[ЗаказКлиента]),
    VAR vKey = 'AccumulationRegister_РасчетыСКлиентами'[ЗаказКлиента]
    VAR vLineSales = 
        CALCULATE(
            SUM('Document_ЗаказКлиента_Товары'[Сумма]),
            'Document_ЗаказКлиента'[Договор_Key] = vKey
        )
    VAR vTotalSales = 
        CALCULATE(
            SUM('Document_ЗаказКлиента_Товары'[Сумма]),
            ALL('Document_ЗаказКлиента_Товары'),
            ALL('Document_ЗаказКлиента'),
            'Document_ЗаказКлиента'[Договор_Key] = vKey
        )
    VAR vTotalPayment = [Payment]
    RETURN
    IF(
        vTotalSales > 0,
        DIVIDE(vLineSales, vTotalSales, 0) * vTotalPayment,
        IF(ISINSCOPE('Catalog_Номенклатура'[Наименование]), 0, vTotalPayment)
    )
)
```

### _Measures[Оплата Распределенная (тескт)]  folder=Договоры fmt=
```dax
VAR vCalcResult = 
    SUMX(
        VALUES('AccumulationRegister_РасчетыСКлиентами'[ЗаказКлиента]),
        VAR vKey = 'AccumulationRegister_РасчетыСКлиентами'[ЗаказКлиента]
        VAR vLineSales = 
            CALCULATE(
                SUM('Document_ЗаказКлиента_Товары'[Сумма]), 
                'Document_ЗаказКлиента'[Договор_Key] = vKey
            )
        VAR vTotalSales = 
            CALCULATE(
                SUM('Document_ЗаказКлиента_Товары'[Сумма]),
                ALL('Document_ЗаказКлиента_Товары'),
                ALL('Document_ЗаказКлиента'),
                'Document_ЗаказКлиента'[Договор_Key] = vKey
            )
        VAR vTotalPayment = [Payment]
        RETURN
        IF(
            vTotalSales > 0,
            DIVIDE(vLineSales, vTotalSales, 0) * vTotalPayment,
            IF(ISINSCOPE('Catalog_Номенклатура'[Наименование]), 0, vTotalPayment)
        )
    )
RETURN
IF(
    ISBLANK(vCalcResult) || vCalcResult = 0,
    BLANK(),
    IF(
        ISINSCOPE('Catalog_Номенклатура'[Наименование]),
        "~" & FORMAT(vCalcResult, "#,0", "ru-RU"),
        FORMAT(vCalcResult, "#,0", "ru-RU")
    )
)
```

### _Measures[ПланПРЕДОплатПоДоговорам]  folder=Договоры fmt=#,0
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[СуммаПлатежа]),
    'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ВариантОплаты] = "ПредоплатаДоОтгрузки",
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Date])
)
```

### _Measures[Оплата Предоплаты]  folder=Договоры fmt=
```dax
SUMX(
    VALUES('Catalog_ДоговорыКонтрагентов'[Ref_Key]),
    SUMX(
        VALUES('Axis_Calendar'[Month]), 
        VAR Plan = [ПланПРЕДОплатПоДоговорам]
        VAR Fact = CALCULATE(SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма]))
        RETURN 
            IF(Plan > 0, MIN(Plan, Fact), BLANK())
    )
)
```

### _Measures[% Выполнения Предоплаты]  folder=Договоры fmt=0%;-0%;0%
```dax
VAR Plan = [ПланПРЕДОплатПоДоговорам]
VAR Fact = [Оплата Предоплаты]
RETURN
    IF(Plan > 0, DIVIDE(Fact, Plan, 0), BLANK())
```

### _Measures[Plan_Performance_%_производ]  folder=План fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Производители'[Производитель])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        CALCULATE([Plan_Amount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[OrderAmount_Weight_%_производ]  folder=Заказы fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Производители'[Производитель])),
        CALCULATE([OrderAmount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[PlanAmount_Weight_%_производ]  folder=План fmt=0%;-0%;0%
```dax
VAR currentVal = [Plan_Amount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Производители'[Производитель])),
        CALCULATE([Plan_Amount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[OrderAmount_Weight_%_подразд]  folder=Заказы fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Производители'[Производитель])),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_СтруктураПредприятия'[Подразделение]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_СтруктураПредприятия'[Подразделение])),
        CALCULATE([OrderAmount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[PlanAmount_Weight_%_подразд]  folder=План fmt=0%;-0%;0%
```dax
VAR currentVal = [Plan_Amount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Производители'[Производитель])),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        CALCULATE([Plan_Amount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[Plan_Perfomance_%_подразд]  folder=План fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Производители'[Производитель])),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_СтруктураПредприятия'[Подразделение]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_СтруктураПредприятия'[Подразделение])),
        CALCULATE([Plan_Amount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[OrderAmount_Weight_%_3]  folder=Заказы fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        ISINSCOPE('Catalog_Партнеры'[Контрагент]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Партнеры'[Контрагент])),
        ISINSCOPE('Catalog_ДоговорыКонтрагентов'[Номер]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_ДоговорыКонтрагентов'[Номер])),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([OrderAmount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        CALCULATE([OrderAmount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[OrderAmount_all]  folder=Заказы fmt=
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_Товары'[Сумма]),
    ALL('Document_ЗаказКлиента'))
```

### _Measures[Клиенты]  folder=Поставщики и Клиенты fmt=#,0
```dax
CALCULATE(
    DISTINCTCOUNT('Catalog_Партнеры'[Ref_Key]),
'Catalog_Партнеры'[Партнер с договором] <> BLANK())
```

### _Measures[Менеджеры]  folder=Поставщики и Клиенты fmt=0
```dax
CALCULATE(
    DISTINCTCOUNT('Catalog_Пользователи'[Ref_Key]),
    'Catalog_Пользователи'[Менеджер с договором] <> BLANK()
)
```

### _Measures[ПросроченныеОплаты]  folder=Договоры fmt=#,0
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Overdue]),
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Date])
)
```

### _Measures[Fact_FIFO]  folder=Договоры fmt=
```dax
VAR vCurrentDate = MAX('Axis_Calendar'[По дням])
VAR vTotalFact = 
    CALCULATE(
        [ФактОплатДляДоговоров], 
        REMOVEFILTERS('Axis_Calendar')
    )
VAR vRTPlan = 
    CALCULATE(
        [ПланОплатПоДоговорам], 
        'Axis_Calendar'[По дням] <= vCurrentDate,
        REMOVEFILTERS('Axis_Calendar')
    )
VAR vPlanToday = [ПланОплатПоДоговорам]
VAR vRTPlanPrev = vRTPlan - vPlanToday
VAR vAllocated = 
    MIN(
        MAX(vTotalFact - vRTPlanPrev, 0), 
        vPlanToday
    )
RETURN
IF(vPlanToday > 0, vAllocated)
```

### _Measures[Fact_FIFO2]  folder=Договоры fmt=#,0
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Fact_FIFO]),
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Date])
)
```

### _Measures[StockValueClosing]  folder=Товары fmt=#,0
```dax
[StockValueOpening] + [StockValueReceipts] - [StockValueExpenses]
```

### _Measures[StockValueOpening]  folder=Товары fmt=#,0
```dax
VAR vDate = MIN('Calendar'[Date])
RETURN
CALCULATE(
    SUMX('AccumulationRegister_СебестоимостьТоваров', 
        IF('AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Receipt", 1, -1) * 'AccumulationRegister_СебестоимостьТоваров'[Стоимость]
    ),
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE(),
    FILTER(ALL('Calendar'), 'Calendar'[Date] < vDate)
)
```

### _Measures[StockValueExpenses]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_СебестоимостьТоваров'[Стоимость]),
    'AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Expense",
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE()
)
```

### _Measures[StockValueReceipts]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_СебестоимостьТоваров'[Стоимость]),
    'AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Receipt",
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE()
)
```

### _Measures[StockQtyClosing]  folder=Товары fmt=#,0
```dax
[StockQtyOpening] + [StockQtyReceipts] - [StockQtyExpenses]
```

### _Measures[StockQtyOpening]  folder=Товары fmt=#,0
```dax
VAR vDate = MIN('Calendar'[Date])
RETURN
CALCULATE(
    SUMX('AccumulationRegister_СебестоимостьТоваров', 
        IF('AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Receipt", 1, -1) * 'AccumulationRegister_СебестоимостьТоваров'[Количество]
    ),
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE(),
    FILTER(ALL('Calendar'), 'Calendar'[Date] < vDate)
)
```

### _Measures[StockQtyExpenses]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_СебестоимостьТоваров'[Количество]),
    'AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Expense",
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE()
)
```

### _Measures[StockQtyReceipts]  folder=Товары fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_СебестоимостьТоваров'[Количество]),
    'AccumulationRegister_СебестоимостьТоваров'[RecordType] = "Receipt",
    'AccumulationRegister_СебестоимостьТоваров'[Active] = TRUE()
)
```

### _Measures[OrderSum_по_отгрузке]  folder=Заказы fmt=
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_Товары'[Сумма]),
    REMOVEFILTERS('Document_ЗаказКлиента'[Date]),
    TREATAS(
        VALUES('Calendar'[Date]), 
        'Document_ЗаказКлиента'[Дата отгрузки]
    )
)
```

### _Measures[OrderSum_по_отгрузке_планфакт_%]  folder=Заказы fmt=
```dax
DIVIDE(
    [ActualSales],
    [OrderSum_по_отгрузке]
)
```

### _Measures[OrderSum_по_отгрузке_планфакт_△]  folder=Заказы fmt=
```dax
[ActualSales] - [OrderSum_по_отгрузке]
```

### _Measures[OrderStatus]  folder=Заказы fmt=
```dax
IF(
    ISINSCOPE('Document_ЗаказКлиента'[Number]),
    MAX('Document_ЗаказКлиента'[_OrderStatus])
)
```

### _Measures[ContractStatus]  folder=Договоры fmt=
```dax
IF(
    ISINSCOPE('Document_ЗаказКлиента'[Number]),
    MAX('Document_АридаПодпишиОнлайнЭД'[Статус])
)
```

### _Measures[Purchases_Sum]  folder=Приобретение fmt=#,0
```dax
SUM('Document_ПриобретениеТоваровУслуг_Товары'[Сумма])
```

### _Measures[Договоры, кол-во]  folder=Договоры fmt=0
```dax
CALCULATE(
    DISTINCTCOUNT('Catalog_ДоговорыКонтрагентов'[Ref_Key]),
    
    'Catalog_ДоговорыКонтрагентов'[ХозяйственнаяОперация] = "РеализацияКлиенту"
)
```

### _Measures[Contract_Narochno]  folder=Договоры fmt=0
```dax
CALCULATE([Договоры, кол-во], 'Document_ЗаказКлиента'[АридаВидПодписи] = "Нарочно")
```

### _Measures[Contract_Electronno]  folder=Договоры fmt=0
```dax
CALCULATE([Договоры, кол-во], 'Document_ЗаказКлиента'[АридаВидПодписи] = "Электронно")
```

### _Measures[Contract_original]  folder=Договоры fmt=0
```dax
CALCULATE(
    [Договоры, кол-во],
    'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE())
```

### _Measures[Срок годности]  folder=Товары fmt=Short Date
```dax
VAR vResult = SELECTEDVALUE('Catalog_СерииНоменклатуры'[ГоденДо])
RETURN
vResult
```

### _Measures[OrderP_Sum]  folder=Заказы поставщику fmt=#,0
```dax
SUM('Document_ЗаказПоставщику_Товары'[Сумма])
```

### _Measures[OrderP_Qty]  folder=Заказы поставщику fmt=#,0
```dax
SUM('Document_ЗаказПоставщику_Товары'[Количество])
```

### _Measures[Purchases_Qty]  folder=Приобретение fmt=#,0
```dax
SUM('Document_ПриобретениеТоваровУслуг_Товары'[Количество])
```

### _Measures[РеализацияСГрануляцией]  folder=Реализации fmt=#,0
```dax
CALCULATE(
    SUM('Document_РеализацияТоваровУслуг_Товары'[Сумма]),
    
    TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_РеализацияТоваровУслуг'[Date])
)
```

### _Measures[Order_Sum_СГрануляцией_Отгрузка]  folder=Заказы fmt=#,0
```dax
CALCULATE(
    SUM('Document_ЗаказКлиента_Товары'[Сумма]),
    REMOVEFILTERS('Document_ЗаказКлиента'[Date]),
    TREATAS(
        VALUES('Axis_Calendar'[По дням]), 
        'Document_ЗаказКлиента'[Дата отгрузки]
    )
)
```

### _Measures[Оплаты_Поставщикам]  folder=Приобретение fmt=0
```dax
SUM('Document_СписаниеБезналичныхДенежныхСредств_РасшифровкаПлатежа'[Сумма])
```

### _Measures[Contract_Electronno_original]  folder=Договоры fmt=0
```dax
CALCULATE(
    [Договоры, кол-во], 
    'Document_ЗаказКлиента'[АридаВидПодписи] = "Электронно",
    'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE()
)
```

### _Measures[Contract_Narochno_original]  folder=Договоры fmt=0
```dax
CALCULATE(
    [Договоры, кол-во], 
    'Document_ЗаказКлиента'[АридаВидПодписи] = "Нарочно",
    'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE()
)
```

### _Measures[Реализации]  folder=Реализации fmt=
```dax
SUM('Document_РеализацияТоваровУслуг_Товары'[Сумма])
```

### _Measures[Fact_FIFO_Matrix]  folder=Договоры fmt=#,0
```dax
VAR vFIFO = 
    CALCULATE(
        SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Fact_FIFO]),
        TREATAS(VALUES('Axis_Calendar'[По дням]), 'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[Date])
    )
VAR vTotal = SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма])
RETURN
IF(
    HASONEVALUE('Axis_Calendar'[По дням]),
    vFIFO,
    vTotal
)
```

### _Measures[MatrixValue]  folder=Договоры fmt=0
```dax
VAR vOrig = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE())
VAR vCopy = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = TRUE(), 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE())
VAR vNotProv = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE(), 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = FALSE())
VAR vSign = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "Подписан")
VAR vSignVend = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "ПодписанПоставщиком")
VAR vNotSign = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", ISBLANK('Catalog_ДоговорыКонтрагентов'[Статус ЭП]))
VAR vCol = SELECTEDVALUE('MatrixColumns'[ColName])
VAR vRows = VALUES('MatrixRows'[RowName])
VAR vSum = 
    IF("Оригинал" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vOrig, 0) +
    IF("Копия" IN vRows && (vCol = "Подписано + Копия" || ISBLANK(vCol)), vCopy, 0) +
    IF("Не предоставлено" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotProv, 0) +
    IF("Подписано" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vSign, 0) +
    IF("Подписано поставщиком" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vSignVend, 0) +
    IF("Не подписано" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotSign, 0)
RETURN IF(vSum = 0, BLANK(), vSum)
```

### _Measures[TableFilter]  folder=Договоры fmt=0
```dax
VAR vCol = SELECTEDVALUE('MatrixColumns'[ColName])
VAR vRows = VALUES('MatrixRows'[RowName])
VAR vIsFiltered = ISCROSSFILTERED('MatrixColumns'[ColName]) || ISCROSSFILTERED('MatrixRows'[RowName])

VAR vResult = 
    COUNTROWS(
        FILTER(
            'Catalog_ДоговорыКонтрагентов',
            VAR vVid = 'Catalog_ДоговорыКонтрагентов'[ВидПодписания]
            VAR vStatusEP = 'Catalog_ДоговорыКонтрагентов'[Статус ЭП]
            VAR vOrigBool = 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора]
            VAR vCopyBool = 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора]
            
            VAR vOrigMatch = vVid = "Нарочно" && vOrigBool = TRUE()
            VAR vCopyMatch = vVid = "Нарочно" && vCopyBool = TRUE() && vOrigBool = FALSE()
            VAR vNotProvMatch = vVid = "Нарочно" && vOrigBool = FALSE() && vCopyBool = FALSE()
            VAR vSignMatch = vVid = "Электронно" && vStatusEP = "Подписан"
            VAR vSignVendMatch = vVid = "Электронно" && vStatusEP = "ПодписанПоставщиком"
            VAR vNotSignMatch = vVid = "Электронно" && ISBLANK(vStatusEP)
            
            RETURN
            ("Оригинал" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)) && vOrigMatch) ||
            ("Копия" IN vRows && (vCol = "Подписано + Копия" || ISBLANK(vCol)) && vCopyMatch) ||
            ("Не предоставлено" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)) && vNotProvMatch) ||
            ("Подписано" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)) && vSignMatch) ||
            ("Подписано поставщиком" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)) && vSignVendMatch) ||
            ("Не подписано" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)) && vNotSignMatch)
        )
    )

RETURN 
    IF(NOT(vIsFiltered), 1, IF(vResult > 0, 1, 0))
```

### _Measures[MatrixValue+]  folder=Договоры fmt=
```dax
VAR vCol = SELECTEDVALUE('MatrixColumns'[ColName])
VAR vRows = VALUES('MatrixRows'[RowName])

VAR vOrigCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE())
VAR vOrigSum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = TRUE())

VAR vCopyCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = TRUE(), 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE())
VAR vCopySum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = TRUE(), 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE())

VAR vNotProvCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE(), 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = FALSE())
VAR vNotProvSum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Нарочно", 'Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора] = FALSE(), 'Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора] = FALSE())

VAR vSignCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "Подписан")
VAR vSignSum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "Подписан")

VAR vSignVendCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "ПодписанПоставщиком")
VAR vSignVendSum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", 'Catalog_ДоговорыКонтрагентов'[Статус ЭП] = "ПодписанПоставщиком")

VAR vNotSignCount = CALCULATE(COUNTROWS('Catalog_ДоговорыКонтрагентов'), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", ISBLANK('Catalog_ДоговорыКонтрагентов'[Статус ЭП]))
VAR vNotSignSum = CALCULATE(SUM('Catalog_ДоговорыКонтрагентов'[Сумма]), 'Catalog_ДоговорыКонтрагентов'[ВидПодписания] = "Электронно", ISBLANK('Catalog_ДоговорыКонтрагентов'[Статус ЭП]))

VAR vTotalCount = 
    IF("Оригинал" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vOrigCount, 0) +
    IF("Копия" IN vRows && (vCol = "Подписано + Копия" || ISBLANK(vCol)), vCopyCount, 0) +
    IF("Не предоставлено" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotProvCount, 0) +
    IF("Подписано" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vSignCount, 0) +
    IF("Подписано поставщиком" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vSignVendCount, 0) +
    IF("Не подписано" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotSignCount, 0)

VAR vTotalSum = 
    IF("Оригинал" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vOrigSum, 0) +
    IF("Копия" IN vRows && (vCol = "Подписано + Копия" || ISBLANK(vCol)), vCopySum, 0) +
    IF("Не предоставлено" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotProvSum, 0) +
    IF("Подписано" IN vRows && (vCol IN {"Подписано", "Подписано + Копия"} || ISBLANK(vCol)), vSignSum, 0) +
    IF("Подписано поставщиком" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vSignVendSum, 0) +
    IF("Не подписано" IN vRows && (vCol = "Не Подписано" || ISBLANK(vCol)), vNotSignSum, 0)

VAR vFormattedSum = SUBSTITUTE(FORMAT(DIVIDE(vTotalSum, 1000000), "#,0"), ",", " ") & " млн. тг"

RETURN 
    IF(vTotalCount = 0 || ISBLANK(vTotalCount), BLANK(), vTotalCount & UNICHAR(10) & vFormattedSum)
```

### _Measures[Маржа по Реальному Входу]  folder=Маржинальность fmt=#,0
```dax
SUM('Document_ЗаказКлиента_АридаРеальныйВход'[Разница])
```

### _Measures[Маржинальность по Реальному Входу]  folder=Маржинальность fmt=0.0%;-0.0%;0.0%
```dax
DIVIDE(
    [Маржа по Реальному Входу],
    [OrderAmount],
    BLANK()
)
```

### _Measures[Plan_Performance_%_поменеджеру]  folder=План fmt=0%;-0%;0%
```dax
VAR currentVal = [OrderAmount]
VAR parentVal = 
    SWITCH(
        TRUE(),
        ISINSCOPE('Catalog_Номенклатура'[Наименование]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Номенклатура'[Наименование])),
        ISINSCOPE('Catalog_Производители'[Производитель]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Производители'[Производитель])),
        ISINSCOPE('Catalog_Пользователи'[Менеджер]), 
            CALCULATE([Plan_Amount], ALLSELECTED('Catalog_Пользователи'[Менеджер])),
        CALCULATE([Plan_Amount], ALLSELECTED())
    )
RETURN
    DIVIDE(currentVal, parentVal)
```

### _Measures[Отгружено по заказу]  folder=InventoryFlow fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_ЗаказыКлиентов'[Заказано]),
    'AccumulationRegister_ЗаказыКлиентов'[RecordType] = "Expense",
    TREATAS(VALUES('Document_ЗаказКлиента_Товары'[Номенклатура_Key]), 'AccumulationRegister_ЗаказыКлиентов'[Номенклатура_Key]),
    FILTER(ALL('AccumulationRegister_ЗаказыКлиентов'), 'AccumulationRegister_ЗаказыКлиентов'[Date] <= MAX('ДатаФормирования'[Date]))
)
```

### _Measures[Отгружено по ордерам]  folder=InventoryFlow fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_ТоварыКОтгрузке'[КОтгрузке]),
    'AccumulationRegister_ТоварыКОтгрузке'[RecordType] = "Expense",
    'AccumulationRegister_ТоварыКОтгрузке'[ДокументОтгрузки_Type] = "StandardODATA.Document_ЗаказКлиента",
    TREATAS(VALUES('Document_ЗаказКлиента_Товары'[Номенклатура_Key]), 'AccumulationRegister_ТоварыКОтгрузке'[Номенклатура_Key]),
    TREATAS(VALUES('Document_ЗаказКлиента_Товары'[Склад_Key]), 'AccumulationRegister_ТоварыКОтгрузке'[Склад_Key]),
    FILTER(ALL('AccumulationRegister_ТоварыКОтгрузке'), 'AccumulationRegister_ТоварыКОтгрузке'[Date] <= MAX('ДатаФормирования'[Date]))
)
```

### _Measures[Осталось отгрузить по ордерам]  folder=InventoryFlow fmt=
```dax
SUM('Document_ЗаказКлиента_Товары'[Количество]) - [Отгружено по ордерам]
```

### _Measures[В наличии остаток]  folder=InventoryFlow fmt=#,0
```dax
CALCULATE(
    SUM('AccumulationRegister_СвободныеОстатки'[ВНаличии]),
    TREATAS(VALUES('Document_ЗаказКлиента_Товары'[Номенклатура_Key]), 'AccumulationRegister_СвободныеОстатки'[Номенклатура_Key]),
    TREATAS(VALUES('Document_ЗаказКлиента_Товары'[Склад_Key]), 'AccumulationRegister_СвободныеОстатки'[Склад_Key])
)
```

### _Measures[Остаток предоплаты]  folder=InventoryFlow fmt=
```dax
IF(
    ISINSCOPE('Document_ЗаказКлиента_Товары'[LineNumber]) && COUNTROWS('Document_ЗаказКлиента_Товары') = 0,
    BLANK(),
    VAR vPrepay =
        CALCULATE(
            SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[СуммаПлатежа]),
            'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ВариантОплаты] = "ПредоплатаДоОтгрузки"
        )
    VAR vPaid =
        CALCULATE(
            SUM('AccumulationRegister_РасчетыСКлиентами'[Сумма]),
            'AccumulationRegister_РасчетыСКлиентами'[RecordType] = "Expense",
            FILTER(ALL('AccumulationRegister_РасчетыСКлиентами'), 'AccumulationRegister_РасчетыСКлиентами'[Date] <= MAX('ДатаФормирования'[Date]))
        )
    RETURN
        vPrepay - vPaid
)
```

### _Measures[Менеджер]  folder=InventoryFlow fmt=
```dax
LOOKUPVALUE(
    'Catalog_Пользователи'[Менеджер],
    'Catalog_Пользователи'[Ref_Key],
    SELECTEDVALUE('Catalog_ДоговорыКонтрагентов'[Менеджер_Key])
)
```

### _Measures[Клиент]  folder=InventoryFlow fmt=
```dax
LOOKUPVALUE(
    'Catalog_Контрагенты'[_Контрагент],
    'Catalog_Контрагенты'[Ref_Key],
    SELECTEDVALUE('Catalog_ДоговорыКонтрагентов'[Контрагент_Key])
)
```

### _Measures[Производитель]  folder=InventoryFlow fmt=
```dax
LOOKUPVALUE(
    'Catalog_Производители'[Производитель],
    'Catalog_Производители'[Ref_Key],
    SELECTEDVALUE('Catalog_Номенклатура'[Производитель_Key])
)
```

### _Measures[Склад]  folder=InventoryFlow fmt=
```dax
LOOKUPVALUE(
    'Catalog_Склады'[Склад],
    'Catalog_Склады'[Ref_Key],
    SELECTEDVALUE('Document_ЗаказКлиента_Товары'[Склад_Key])
)
```

### _Measures[Номенклатура]  folder=InventoryFlow fmt=
```dax
IF(
    ISINSCOPE('Document_ЗаказКлиента_Товары'[LineNumber]),
    LOOKUPVALUE(
        'Catalog_Номенклатура'[Наименование],
        'Catalog_Номенклатура'[Ref_Key],
        SELECTEDVALUE('Document_ЗаказКлиента_Товары'[Номенклатура_Key])
    )
)
```

### _Measures[Статус договора]  folder=InventoryFlow fmt=
```dax
IF(
    NOT ISINSCOPE('Document_ЗаказКлиента'[Number])
        || (ISINSCOPE('Document_ЗаказКлиента_Товары'[LineNumber]) && COUNTROWS('Document_ЗаказКлиента_Товары') = 0),
    BLANK(),
    IF(
        SELECTEDVALUE('Document_ЗаказКлиента'[АридаВидПодписи]) = "Электронно",
        IF(SELECTEDVALUE('Document_ЗаказКлиента'[Статус ЭП]) = "Подписан", "Подписан", "Не подписан"),
        IF(
            SELECTEDVALUE('Catalog_ДоговорыКонтрагентов'[АридаОригиналДоговора]) = TRUE()
                || SELECTEDVALUE('Catalog_ДоговорыКонтрагентов'[АридаКопияДоговора]) = TRUE(),
            "Подписан",
            "Не подписан"
        )
    )
)
```

### _Measures[Условия оплаты]  folder=InventoryFlow fmt=
```dax
IF(
    NOT ISINSCOPE('Document_ЗаказКлиента'[Number])
        || (ISINSCOPE('Document_ЗаказКлиента_Товары'[LineNumber]) && COUNTROWS('Document_ЗаказКлиента_Товары') = 0),
    BLANK(),
    VAR vPrepayPct =
        CALCULATE(
            SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ПроцентПлатежа]),
            'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ВариантОплаты] = "ПредоплатаДоОтгрузки"
        )
    VAR vCreditPct =
        CALCULATE(
            SUM('Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ПроцентПлатежа]),
            'Document_ЗаказКлиента_ЭтапыГрафикаОплаты'[ВариантОплаты] = "КредитПослеОтгрузки"
        )
    RETURN
        IF(ISBLANK(vPrepayPct), 0, vPrepayPct) & "/" & IF(ISBLANK(vCreditPct), 0, vCreditPct)
)
```

### _Measures[Check_Contract_Order]  folder=Заказы fmt=
```dax
VAR ContractAmt = [ContractAmount]
VAR OrderAmt = [OrderAmount]
RETURN
IF(
    ContractAmt <> OrderAmt,
    "#FF0000",
    BLANK()
)
```

### _Measures[Mismatch_Count]  folder=Заказы fmt=0
```dax
CALCULATE(
    DISTINCTCOUNT('Catalog_ДоговорыКонтрагентов'[Номер]),
    FILTER(
        VALUES('Catalog_ДоговорыКонтрагентов'[Номер]),
        [ContractAmount] <> [OrderAmount]
    )
)
```

### _Measures[Mismatch_Status]  folder=Заказы fmt=
```dax
VAR ContractAmt = [ContractAmount]
VAR OrderAmt = [OrderAmount]
RETURN
IF(
    ContractAmt <> OrderAmt,
    "Нестыковка",
    BLANK()
)
```

