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
    // "C": "https://github.com/tree-sitter/tree-sitter-c",
    // "C++": "https://github.com/tree-sitter/tree-sitter-cpp",
    // "C#": "https://github.com/tree-sitter/tree-sitter-c-sharp",
    // "Go": "https://github.com/tree-sitter/tree-sitter-go",
    // "HTML": "https://github.com/tree-sitter/tree-sitter-html",
    // "Java": "https://github.com/tree-sitter/tree-sitter-java",
    // "JavaScript": "https://github.com/tree-sitter/tree-sitter-javascript",
    // "Kotlin": "https://github.com/mburyakov/tree-sitter-kotlin",
    // "PHP": "https://github.com/tree-sitter/tree-sitter-php",
    "Python": "https://github.com/tree-sitter/tree-sitter-python"
    // "Ruby": "https://github.com/tree-sitter/tree-sitter-ruby",
    // "Rust": "https://github.com/tree-sitter/tree-sitter-rust",
    // "Swift": "https://github.com/tree-sitter/tree-sitter-swift",

Запуск и использование
------------------------------------------
### В терминале 
```
python -m  sim_dev_search.main top -r <repo_url1> -r <repo_url2> -f <out_file_path> --api-token <github_token>

python -m  sim_dev_search.main prog -r <repo_url1> -r <repo_url2> -f <out_file_path>
```
### Docker
```
docker build -t sim_dev .

docker run -it --name SimDev --rm  sim_dev prog -r <repo_url1> -r <repo_url2> -f <out_file_path>
```