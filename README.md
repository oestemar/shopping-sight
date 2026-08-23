# Shopping-sight

Flask + MySQL + Supabase を用いて構築した EC サイト（購入側＋管理者側）。メニュー・商品表示・購入処理のフロントエンド機能と、商品管理・在庫管理・注文管理・ユーザー管理・管理者権限などのバックオフィス機能を備えています。

## 1.プロジェクト概要
Shopping-sight は以下の 2 つの画面で構成されています：

### 購入側（Userflow）
一般ユーザーが商品を閲覧し、カートに入れ、決済して購入するための画面。

- カテゴリー表示
- 商品一覧・商品詳細
- カート機能
- 精算確認
- 決済方法選択（Stripe / Paspo / QR ※疑似決済）
- 注文完了
- ユーザー登録・ログイン
- 注文履歴表示

### 管理者側（Admin）
ECサイトの運営者が商品・在庫・注文・ユーザーを管理するための画面。

- ログイン / ログアウト / ログイン認証
- ダッシュボード
- 商品管理（一覧・詳細・編集・追加・CSVインポート）
- 商品画像管理（Supabase）
- 注文管理（一覧・詳細・ステータス変更）
- 在庫管理（一覧・更新・履歴）
- カテゴリー管理（一覧・編集・追加）
- ユーザー管理（一覧・詳細・削除）
- 管理者管理（一覧・詳細・追加・削除・パスワード変更）：アクセス権限設定（demo / admin / super）

## 2.技術構成
- Python 3.x
- Flask
- MySQL / SQLAlchemy
- Supabase（商品画像ストレージ）
- Railway
- Bootstrap 5
- Jinja2
- Session 認証
- HTML / CSS / JavaScript

## 3.ディレクトリ構成（概要）
```
shopping-sight/
  ├── app.py
  ├── models/               # DBモデル
  ├── admin/                # 管理者側ルート
  ├── shop/                 # 購入側ルート
  ├── static/               # CSS / JS / 画像
  ├── templates/            # HTMLテンプレート
  ├── requirements.txt
  └── README.md
```


## 4.画面遷移図
### 管理者側
- 管理者版仕様書（Admin版）に記載 → 商品管理 / 注文管理 / 在庫管理 / カテゴリ管理 / ユーザー管理 / 管理者管理

### 購入側
Userflow版仕様書に記載
→ メニュー / 商品一覧 / 商品詳細 / カート / 精算 / 決済 / 完了

## 5.API仕様書
### 管理者側 API
- 認証
- 商品管理
- 商品画像管理
- 注文管理
- 在庫管理
- カテゴリ管理
- ユーザー管理
- 管理者管理

### 購入側 API
- カテゴリ
- 商品一覧・詳細
- カート
- 精算
- 決済
- 注文履歴
- ユーザー認証
- （詳細は Admin版 / Userflow版 仕様書に記載）

## [6.テスト仕様書](/docs/テスト仕様書.md)
- 購入処理テスト
- カート操作テスト
- 決済処理テスト（疑似）
- 商品管理テスト
- 在庫管理テスト
- 注文管理テスト
- カテゴリ管理テスト
- ユーザー管理テスト
- 管理者権限テスト

## 7.セットアップ手順（例）
- git clone https://github.com/xxx/shopping-sight.git
- cd shopping-sight
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- MySQL にテーブルを作成し、.env に接続情報と Supabase のキーを設定。