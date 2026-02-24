
import argparse
import json
import signal
import sys
from typing import Optional

from confluent_kafka import Consumer, KafkaException, Message


def _decode(msg: Message) -> str:
    val = msg.value()
    if val is None:
        return ""
    try:
        obj = json.loads(val.decode("utf-8", errors="replace"))
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return val.decode("utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="Kafka Consumer demo (confluent_kafka)")
    parser.add_argument("--bootstrap", default="localhost:9092", help="bootstrap.servers")
    parser.add_argument("--topic", default="demo-topic", help="topic name")
    parser.add_argument("--group", default="demo-group", help="group.id")
    parser.add_argument(
        "--from-beginning",
        action="store_true",
        help="if no committed offset, start from earliest",
    )
    parser.add_argument("--auto-commit", action="store_true", help="enable auto commit")
    args = parser.parse_args()

    running = True

    def _stop(_sig: int, _frame: Optional[object] = None):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    consumer = Consumer(
        {
            "bootstrap.servers": args.bootstrap,
            "group.id": args.group,
            "enable.auto.commit": bool(args.auto_commit),
            "auto.offset.reset": "earliest" if args.from_beginning else "latest",
        }
    )

    try:
        consumer.subscribe([args.topic])
        print(f"[consumer] subscribed topic={args.topic} group={args.group}")
        print("[consumer] Ctrl+C to exit")

        while running:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            value_text = _decode(msg)
            k = msg.key()
            key = k.decode("utf-8", errors="replace") if k is not None else None
            headers = msg.headers() or []

            print(
                "[consume] "
                f"topic={msg.topic()} partition={msg.partition()} offset={msg.offset()} "
                f"key={key} value={value_text} headers={headers}"
            )

            if not args.auto_commit:
                consumer.commit(message=msg, asynchronous=False)

    except Exception as e:
        print(f"[consumer] error: {e}")
        raise
    finally:
        consumer.close()
        print("[consumer] closed")


if __name__ == "__main__":
    main()

