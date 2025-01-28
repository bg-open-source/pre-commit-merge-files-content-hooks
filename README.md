## To create a package:
1. activate poetry shell
2. delete files pyproject.toml and poetry.lock
3. commit
4. create new tag & commit tag
5. `python setup.py build`
6. `python setup.py sdist` (создаст файл pre_commit_merge_content_hooks-0.0.0.tar.gz)
7. `python setup.py bdist_wheel` (создаст файл pre_commit_merge_content_hooks-0.0.0-py3-none-any.whl)
