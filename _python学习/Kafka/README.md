# Kafka 入门示例（confluent_kafka）

这个目录包含一个最小可运行的 Kafka Producer / Consumer 示例，用来理解 Kafka 的核心工作方式：

- Producer 把消息写入 **topic**
- Broker 把消息持久化到 **partition**（每个分区内有序）
- Consumer 以 **consumer group** 的形式消费消息，并维护 **offset**（消费位置）

文件：

- `producer.py`：发送 JSON 消息，带 key、headers，含 delivery report
- `consumer.py`：消费消息，打印 topic/partition/offset，演示手动提交 offset

## 0. 安装依赖

```bash
pip install confluent-kafka
```

> `confluent-kafka` 依赖 `librdkafka`，Windows 上一般 `pip` 安装即可。

## 1. 准备 Kafka（本地最快：Docker）

你需要一个正在运行的 Kafka Broker（默认监听 `localhost:9092`）。

如果你会用 Docker，可以用 `docker compose` 起一个单节点（KRaft）Kafka。下面提供一个最简 `docker-compose.yml` 供参考（你可以放到任意目录运行，不要求放在本目录）：

```yaml
services:
  kafka:
    image: bitnami/kafka:latest
    ports:
      - "9092:9092"
    environment:
      - KAFKA_ENABLE_KRAFT=yes
      - KAFKA_CFG_PROCESS_ROLES=broker,controller
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka:9093
      - KAFKA_CFG_NODE_ID=1
      - ALLOW_PLAINTEXT_LISTENER=yes
```

启动：

```bash
docker compose up -d
```

## 2. 创建 topic

如果你的 Kafka 没有自动创建 topic（有些环境默认关闭），需要手动建一个：

```bash
# 进入容器
docker exec -it <容器名> bash

# 创建 topic
auto_create=false
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic demo-topic --partitions 1 --replication-factor 1

# 查看 topic 列表
/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

> 不同镜像的 Kafka CLI 位置可能不同；也可以用你本机安装的 Kafka CLI。

## 3. 运行 Consumer

在本目录运行：

```bash
python consumer.py --bootstrap localhost:9092 --topic demo-topic --group demo-group --from-beginning
```

说明：

- `--group`：consumer group 名字。Kafka 用它来做“同组内负载均衡、组间各自消费”。
- `--from-beginning`：当该 group **没有提交过 offset** 时，从最早开始读。
- 默认是 **手动提交 offset**（更利于理解 exactly-once/at-least-once 语义）。

## 4. 运行 Producer

另开一个终端：

```bash
python producer.py --bootstrap localhost:9092 --topic demo-topic --count 10
```

你会看到：

- Producer 侧有 `delivery report`（写入 broker 成功/失败）
- Consumer 侧会打印每条消息的 `topic/partition/offset/key/headers`

## 5. 你应该重点理解的概念

- **topic**：消息的逻辑分类。
- **partition**：topic 的物理分片。
  - 同一个 partition 内严格有序。
  - key 会影响分区选择（同 key 通常会落到同分区，从而保证该 key 的消息有序）。
- **offset**：partition 内消息的位置。
- **consumer group**：
  - 同一个 group 内，多个 consumer 会对 partition 做分配，实现并行消费。
  - 不同 group 之间互不影响，各自维护 offset（相当于“多套订阅者”）。
- **提交 offset**：
  - 自动提交：简单但不易控制处理语义。
  - 手动提交：更清晰，处理完再提交，更容易做到 at-least-once。

## 6. 常见问题排查

- **连接不上 `localhost:9092`**
  - Kafka 没启动
  - `advertised.listeners` 配错（容器里启动时尤其常见）
  - 端口被占用

- **Producer 发送成功但 Consumer 看不到**
  - topic 不一致
  - consumer group 已经提交过 offset，并且从最新开始读（不加 `--from-beginning`）
  - 消息被发到别的 partition（本例 partitions=1 不太会）

- **Windows 控制台编码问题**
  - Producer/Consumer 都用 UTF-8 解码；如果你终端显示乱码，换用支持 UTF-8 的终端或调整代码输出。
