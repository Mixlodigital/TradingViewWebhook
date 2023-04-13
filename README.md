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
cd /etc/systemd/system/

touch webhook.service

sudo nano webhook.service

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
