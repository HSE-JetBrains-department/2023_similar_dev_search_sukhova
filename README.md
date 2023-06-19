![Test](https://github.com/ILilliasI/2023_similar_dev_search_sukhova/actions/workflows/test.yml/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

Проект "Поиск похожих разработчиков"
==========================================
Описание        
------------------------------------------
Проект, который находит похожих разработчиков, основываясь на схожести используемых языков программирования, библиотек, имён переменных и т.п.

Этапы разработки  
------------------------------------------
1. Discover 
2. Clone
3. Handle VCS
4. Classify
5. Filter
6. Parse
7. Similar dev search

Поиск похожих разработчиков
------------------------------------------
Поиск осуществляется на основе используемых языков и имён переменных. Из исходных признаков составляется вектор, 
для определения близости находятся вектора с наивысшей метрикой cosine similarity.

Для найденных похожих разработчиков выводится информация о часто используемых ими языках и именах переменных (если имена переменных были найдены в исходных файлах).

Запуск и использование
------------------------------------------
### В терминале 
```
python -m  sim_dev_search top -r <repo_url1> -r <repo_url2> -f <out_file_path> --api-token <github_token>

python -m  sim_dev_search prog -r <repo_url1> -r <repo_url2> -f <out_file_path>

python -m  sim_dev_search sim_dev -u <user_email> --in-file-path <in_file_path> --out-file-path <out_file_path>

python -m unittest discover tests
```
### Docker
```
docker build -t sim_dev .

docker run -it --name SimDev --rm  sim_dev prog -r <repo_url1> -r <repo_url2> -f <out_file_path>
```
