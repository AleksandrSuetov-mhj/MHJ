2024-08-20,вт
Независимо от размера начального шага показывается одна успешная попытка.

2024-08-23,пт
Добавить выход из алгоритма по достижении заданного значения функции

2024-08-26,пн
Выделить класс для вывода информации о процессе

Сделать вывод об итогах вычислений на сетке и общих итогах

2024-08-29,чт
Написал производный класс с блокировкой направления на предыдущую точку.
В двумерном случае без блокировки вычислений=1278, с блокировкой=1234, чблокировок=44
Выигрыш примерно 4%.

Первоначально использовал опрос всех направлений; 
получилось плохо из-за опроса направлений, противоположных к успешным.


===============================

<details>
<summary>Результаты запусков</summary>

~/MHJ$ python -m MHJ_obj.MHJ00_cls

+ + + + + Модуль /home/runner/MHJ/MHJ_obj/MHJ00_cls.py - Проверка работы + + + + +
 Создан объект MHJ00_wrt№1 Создан объект MHJ00_prn№1 Создан объект MHJ00_cls№1
+ + + MHJ00_cls№1: dim=2; Fval=4.00e+00/Func=tsFnRosen; ss_init=1.00e-02; ss_min=1.00e-03; ss_coef=2; minFval=1.00e-01; maxNEv=100000.0; X=[-1, 1]; 
Достигнуто ограничение по значению функции
- - - MHJ00_cls: Fval=9.95e-02; ss_cur=2.50e-03; pathLen=3.55e+00; NEv=1278/NSc=732/X=+8.5e-01 +7.2e-01; 
Работа модуля /home/runner/MHJ/MHJ_obj/MHJ00_cls.py завешилась штатно
~/MHJ$ python -m MHJ_obj.MHJ01_cls

+ + + + + Проверка работы модуля /home/runner/MHJ/MHJ_obj/MHJ01_cls.py Создан объект MHJ01_wrt№1 Создан объект MHJ01_prn№1 Создан объект MHJ01_cls№1
+ + + MHJ01_cls№1: dim=2; Fval=4.00e+00/Func=tsFnRosen; ss_init=1.00e-02; ss_min=1.00e-03; ss_coef=2; minFval=1.00e-01; maxNEv=100000.0; X=[-1, 1]; useBlock=True/
Достигнуто ограничение по значению функции
- - - MHJ01_cls: Fval=9.95e-02; ss_cur=2.50e-03; pathLen=3.55e+00; NEv=1234/NSc=732/X=+8.5e-01 +7.2e-01; Nblk=44/
- - - - - Проверка работы модуля завешилась штатно//home/runner/MHJ/MHJ_obj/MHJ01_cls.py
~/MHJ$ python -m MHJ_obj.MHJ11_cls

+ + + + + Проверка работы модуля /home/runner/MHJ/MHJ_obj/MHJ11_cls.py Создан объект MHJ11_wrt№1 Создан объект MHJ11_prn№1 Создан объект MHJ11_cls№1
+ + + MHJ11_cls№1: dim=2; Fval=4.00e+00/Func=tsFnRosen; ss_init=1.00e-02; ss_min=1.00e-03; ss_coef=2; minFval=1.00e-01; maxNEv=100000.0; X=[-1, 1]; useSearchGoodDirs=True/
Достигнуто ограничение по значению функции
- - - MHJ11_cls: Fval=9.95e-02; ss_cur=2.50e-03; pathLen=3.71e+00; NEv=932/NSc=396/X=+8.5e-01 +7.2e-01; |NSrchGd/Sc= 244/ 211
- - - - - Проверка работы модуля завешилась штатно//home/runner/MHJ/MHJ_obj/MHJ11_cls.py

</details>

