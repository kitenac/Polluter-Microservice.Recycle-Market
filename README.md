# Description is in progress...
shortly - it`s the first microservice "Polluter Microservice" from project "Recycler Market" 
- \* there`ll be link to main repo, where all the microservices are being run with k8s \*  
- \* also links to other microservices of this project \*



### Scripts

#### Init DB
python3 -m app.data.preparing.build_some_tables

#### Create svg diagram of DB`s Tables relationships
python3 -m db_visualizer.db_visualizer 



--------------------------------------------------
#TODO - expand, cut and translate old ddescription to english:

# Схема БД и сущности:
![Logo](data_model_diagram.svg)

Базовые сущности:
- Poluter_OO - сущность клиента, генерирующего отходы\
- PolluterWaste - отходы клиента по категории: число отходов выбранной категории у клиента
- WasteCategory - категория отходов и время на её переработку

Сущности представления и накопления отходов:
- RecyclerWaste - отходы клиента, принятые в хранилище переработки у переработчика\


# Роль компонентов, их связь 

#### app
- веб-север с CRUD по сущностям 
- клиентам достаточно просто положить свои отходы в очередь (PolluterWastes) из которой демон (recycler-demon) их заберёт и распределит оптимально\

ядро - app/setup_app.py - ядро файл с настройкой веб-приложения и конфигами

#### recycler-demon  
Это демон-обработчик отходов (в будущем будет отдельным микросервисом с подбором транспортной и перерабатывающей компаний). Он реализует логику автоматического перераспределения, удаления, обновления отходов у клиентов и обработчиков

Он управляет:
- очередями отходов клиентов (PolluterWastes): перенаправляет отходы в ближайшие пункты переработки, имеющие свободное место в хранилище переработки 
- хранилищами переработки (RecyclerWastes): удаляет поступившие отходы, когда они переработались 

Т.е. схема циркуляции отходов такая:\ 
PolluterWastes -> Recycler Storages -> Recycler Wastes -> отходы переработаны, в Recycler Storages вновь освободилось место и оно готово принимать новые отходы данного типа от клиентов\

ядро - recycler_demon/demon.py

####  запуск приложения и связь компонентов
- start.sh - запуск приложения (отрабатывают моки для тестовых данных и main.py запускается)\
- main.py - последовательный запуск компонентов\ 
- связь компонентов - через IPC метод send_command_to_demon()\

в recycle_demon_logs видно какую команду и в какое время получил демон от клиента 
demon_main_IPC.py/send_command_to_demon() - метод, который вызываетя на ручках app для синхронизации БД app (postgress) и БД recycler-demon (хранимых в RAM переменные, как кэш - в Redis хочу перенести) 


  

# Frontend-like admin-page

http://127.0.0.1:8001/api/v1.0/admin/

  

Here you can see queue of PolluterWastes, how they move to RecyclerWastes and how RecylerStorage reacts on it

- once waste is recyled (by timer) - RecyclerStorage gets it`s resources back

  

- admin page is buggy, but works fine as frontend to monitor entities

- to generate entities - use mock (see section bellow)

  
  

# About Demon and muliprocessing

App/backend - parent\

RecyclerDemon - child\

RecyclerDemon stores db in memory and manages waste redestribution and recycling (deletes wastes from recycler storage slots when it`s time)\

RecyclerDemon - loads DB only once - when runned\

than App gives updated data to Recycler_Demon through IPC-queury of commands - feeds demon updates\

  

Also RecyclerDemon maintanes and populates cache with distances between pollutors and recyclers, btw distances stores squared (not to count radical - just to have ability to range avaliable recyclers by distance) \

The DB Table RecyclerWastes (queue of wastes being recycled in recycler\`s storage slots) - fully under Demon`s controll, no one else modifies it

  
  

# Docs

http://127.0.0.1:8001/docs

  

# Mocking tables with data:

python3 mock_tables.py

- also will be api mock-methods to add some random wastes or recyclers

  

# Draw graph of DB:

from repo`s folder run:

- python3 -m db-visualizer.db-visualizer

  

# Required packages

for drawing grah of DB:

- sudo apt-get install graphviz

- sudo apt-get install --reinstall xdg-utils

  
  
  

# \[Experimental/for-future\] Rendering graphs:

i`ve managed to constract suitable api for visualazing relationships between objects

- maby in future i`ll find some usecases for it - see app.rel_graph.py

  

Requirments to use it:

- apt-get install libbz2-dev

  

than reinstall current python version (3.12.1 in my case)\

bc python can`t see libbz2-dev without reinstalation: https://stackoverflow.com/questions/27727919/pythonbrew-importing-bz2-yields-importerror-no-module-named-bz2

- pyenv uninstall 3.12.1

- pyenv install 3.12.1

  

now app/rel_graph.py should work fine (it`s API can be used from mocks or some route)

python3 app/rel_graph.py