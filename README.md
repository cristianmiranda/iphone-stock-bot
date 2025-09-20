# 📱 iPhone 15 Stock Bot

## Deployment

```bash
# Build and push docker image
docker build -t iphonestockbot .
docker tag iphonestockbot:latest 387720813372.dkr.ecr.us-east-1.amazonaws.com/iphonestockbot:latest
docker push 387720813372.dkr.ecr.us-east-1.amazonaws.com/iphonestockbot:latest

# Refresh lambda
aws lambda update-function-code --function-name iPhoneStockBot --image-uri 387720813372.dkr.ecr.us-east-1.amazonaws.com/iphonestockbot:latest
```

## AWS Lambda payload

```json
{
  "bot_token": "367849242:ABEY8aTMHxFZQRFqf3kguuz8jSBOp3QnKKR",
  "recipients": [168964322, 167890751]
}
```

## AWS resources:

- Lambda
- ECR
- EventBridge Scheduler

![](https://i.imgur.com/nsdQf2r.png)

```
Hecho con ❤️ en 🇦🇷 ... papá! 🤙🏼
```
