# nawashipy


Alert message

{
    "ticker": "{{ticker}}",
    "interval": "{{interval}}",
    "order_type": "{{strategy.order.action}}",
    "balance_type": "usdt",
    "quantity": "100% of balance"
}


webhook service

1. cd /etc/systemd/system/

2. touch webhook.service

3. sudo nano webhook.service

Add:
///

[Unit]
Description=Webhook Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/webhook.py
Restart=always

[Install]
WantedBy=multi-user.target

///
