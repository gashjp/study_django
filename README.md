# a

## Tutorial

https://code.visualstudio.com/docs/python/tutorial-django

## Memo

- アプリ作成 `> python manage.py startapp web`
- gitignore: `https://www.toptal.com/developers/gitignore/api/windows,visualstudiocod,macos,python,django`
- デバッグ実行: Ctrl + F5

## Troubleshooting

- [windows]このシステムではスクリプトの実行が無効になっているため、ファイル~
  - 実行ポリシーを確認する
  - https://qiita.com/ponsuke0531/items/4629626a3e84bcd9398f

PS C:> Get-ExecutionPolicy
Restricted
PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS C:> Get-ExecutionPolicy
RemoteSigned
