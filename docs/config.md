An example config:

```yaml
name: clay
org: thecity
service: clay

qa:
  taskRole: mediaplayECSRole
  executionRole: ecsTaskExecutionRole
  deployment:
    command: ["npm", "run", "start:dev"]
    cpu: 1
    memory: 128
    port: 3001
    desiredCount: 1
    # maxHealthyPercent: 100
    # minHealthyPercent: 80
  loadBalancer:
    targetGroupArn: arn:aws:elasticloadbalancing:us-east-1:971661474345:targetgroup/thecity-qa-clay/35db979ce5e37cfd
  logging:
    logDriver: awslogs
    options:
      awslogs-group: /ecs/mediaplay-v2
      awslogs-region: us-east-1
      awslogs-stream-prefix: ecs
```
