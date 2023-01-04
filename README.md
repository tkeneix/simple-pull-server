# simple-pull-server
GitBucketからのWebhookをハンドリングしてgit pullするシンプルなサーバー

> security tokenの設定に対応していないため、テスト環境で試す程度にする.  

## 設定  
### pull_server.yaml  
sample配下のyamlをconf以下に配置する.  
discordよりwebhookのURLを生成し、yamlの定義に指定する.  
また、`git pull`を発行したいパスを指定する.  

### gitbucket  
![setting_gitbucket](/doc/setting_gitbucket.png)

## discordへの通知  
![message_on_discord](/doc/message_on_discord.png)

