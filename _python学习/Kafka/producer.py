
import argparse
import json
import socket
import time
from datetime import datetime, timezone
from typing import List, Tuple, cast

from confluent_kafka import Producer


def _delivery_report(err, msg):
    if err is not None:
        print(f"[delivery] failed: {err}")
        return
    print(
        "[delivery] ok: "
        f"topic={msg.topic()} partition={msg.partition()} offset={msg.offset()} "
        f"key={msg.key().decode('utf-8', errors='replace') if msg.key() else None}"
    )


def main():
    parser = argparse.ArgumentParser(description="Kafka Producer demo (confluent_kafka)")
    parser.add_argument("--bootstrap", default="localhost:9092", help="bootstrap.servers")
    parser.add_argument("--topic", default="demo-topic", help="topic name")
    parser.add_argument("--count", type=int, default=10, help="messages to send")
    parser.add_argument("--interval", type=float, default=0.2, help="seconds between messages")
    args = parser.parse_args()

    producer = Producer(
        {
            "bootstrap.servers": args.bootstrap,
            "client.id": f"producer-{socket.gethostname()}",
            # 入门建议：先别改这些，等理解后再调
            # "acks": "all",
            # "compression.type": "lz4",
        }
    )

    for i in range(args.count):
        event = {
            "id": i,
            "ts": datetime.now(timezone.utc).isoformat(),
            "message": f"hello kafka {i}",
        }

        key = str(i).encode("utf-8")
        value = json.dumps(event, ensure_ascii=False).encode("utf-8")
        headers = cast(
            List[Tuple[str, str | bytes | None]],
            [
            ("app", "kafka-demo"),
            ("content-type", "application/json"),
            ],
        )

        # 发送消息到指定主题
        # 设置回调函数 _delivery_report 用于确认投递结果
        producer.produce(
            topic=args.topic,
            key=key,
            value=value,
            headers=headers,
            on_delivery=_delivery_report,
        )

        # 触发回调（delivery report）
        producer.poll(0)
        time.sleep(args.interval) #控制消息发送间隔

    print("[producer] flushing...")
    producer.flush(10) #等待所有消息确认（最多10秒）
    print("[producer] done")


if __name__ == "__main__":
    main()

