# Connect Discord And LINEWORKS

## 概要
DiscordとLINE WORKSを連携するためのサービスです。

## 使い方
1. DiscordのBotを作成し、トークンを取得
2. LINE WORKSのBotを作成し、トークンを取得
3. `git clone`
4. `cp .env.sample .env`
   - `DISCORD_BOT_TOKEN`: `DiscordのBotトークン`
   - `LW_API_20_CLIENT_ID`: `LINEWORKSのAPIクライアントID`
   - `LW_API_20_CLIENT_SECRET`: `LINEWORKSのAPIクライアントシークレット`
   - `LW_API_20_SERVICE_ACCOUNT_ID`: `LINEWORKSのAPIサービスアカウントID`
   - `LW_API_20_BOT_ID`: `LINEWORKSのボットID`
   - `LW_API_20_BOT_SECRET`: `LINEWORKSのボットシークレット`
   - `LW_API_20_CHANNEL_ID`: `LINEWORKS側に送信するチャンネルID`
   - `TUNNEL_TOKEN`: `Cloudflare Tunnelのトークン`
   - `DISCORD_CHANNEL_ID`: `Discord側に送信するチャンネルID`
   - `CHANNEL_LIST`: `メッセージを取得するチャンネルリスト`
     - 例：`CHANNEL_LIST=1234567890,1234567891,1234567892`

5. `docker-compose up -d`

## 送受信されるメッセージ
- Discord -> LINEWORKS 
    - [x] メッセージ
    - [ ] 添付ファイル
    - [ ] 画像・動画
    - [ ] スタンプ
- LINEWORKS -> Discord
    - [x] メッセージ
    - [ ] 添付ファイル
    - [ ] 画像・動画
    - [ ] スタンプ

## 送受信されるチャンネル
- Discord -> LINEWORKS
  - `env.CHANNEL_LIST`で指定したチャンネルのメッセージが`env.LW_API_20_CHANNEL_ID`のチャンネルに送信されます。
- LINEWORKS -> Discord
  - `env.LW_API_20_CHANNEL_ID`のチャンネルのメッセージが`env.DISCORD_CHANNEL_ID`のチャンネルに送信されます。