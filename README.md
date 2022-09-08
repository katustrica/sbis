Как настроить debugger в PyCharm:
1. Скачать файлы и распаковать в одно место. Пусть это будет папка `C:\sbis\SCRIPTS\`
2. Зайти в файл config.ini и ввести свои данные:
	- Путь до папки **online** внутри собранного стенда
	- Адрес на который зареган стенд
	- Порт
	- `test` / `pre-test` / ...
	- Логин пользователя
	- Пароль пользователя
![image](https://user-images.githubusercontent.com/28065104/189142879-5554ed48-127b-42bf-950b-2516fa8b72df.png)

---
3. Настраиваем PyCharm
	1. Открываем конфигурации дебагов![image](https://user-images.githubusercontent.com/28065104/189144093-610b2653-588f-4807-855f-4a13a16705fe.png)
	2. Выбираем `Python`
![image](https://user-images.githubusercontent.com/28065104/189144472-c5cbcada-a4ec-4f34-bc4c-49558e7fe9b3.png)
	3.  Настраиваем произвольное имя, путь до файла `run.py`, который мы распаковали в `C:\sbis\SCRIPTS\` *(см. 1 строчку)*, выбираем нужный нам интерпретатор.![image](https://user-images.githubusercontent.com/28065104/189145749-20adaa6b-7b24-4237-a755-5cbd54a2f4d9.png)
4. Заходим в файл `debug.py`. Настраиваем функцию `main` как нам нужно:
	- Можем импортировать любые модули
	- вызывать SQL команды, в том числе и на изменение
	- Проверять любые функции
![image](https://user-images.githubusercontent.com/28065104/189149370-2f2c0fef-1cbd-4598-816a-d05f38b0cc95.png)
	- У меня есть несколько примеров, например функция `test_events_lists`, которая вызывает все событийные реестры. Также очень удобно использовать декоратор @log_result, который логирует результат выполнения функции, и его не нужно print`ить или логировать вручную постоянно.
	![image](https://user-images.githubusercontent.com/28065104/189150065-f7b976bf-0778-4915-9286-5ccc454f7a2a.png)


