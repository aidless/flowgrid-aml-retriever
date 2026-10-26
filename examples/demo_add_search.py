#!/usr/bin/env python3
"""Offline Add/Search demo: three messages, two searches, one isolation check.

No HTTP server, no API key, no third-party package. The db is in-memory.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aml_retriever.api import MemoryService
from aml_retriever.config import RetrieverConfig


def main() -> None:
    service = MemoryService(RetrieverConfig(db_path=":memory:"))
    try:
        service.add(
            request_id="demo-1",
            user_id="alice",
            session_id="alice-1",
            messages=[
                {"role": "user", "timestamp": 1785945600000,
                 "content": "The launch date moved to August 14, 2026. Owner: Lin Tao."},
                {"role": "assistant", "timestamp": 1785945660000,
                 "content": "Noted the August 14 date and Lin Tao as owner."},
                {"role": "user", "timestamp": 1786032000000,
                 "content": "Update: the launch date is now August 21, 2026."},
            ],
        )

        for label, query in (
            ("current launch", "When is the launch?"),
            ("owner", "Who is Lin Tao?"),
        ):
            result = service.search(user_id="alice", query=query, top_k=3)
            print(f"\n{label}: returned {len(result.results)} (of {result.total} candidates)")
            for rank, evidence in enumerate(result.results[:2], 1):
                content = " ".join(evidence.content.split())
                print(f"  {rank}. {content}")

        other = service.search(user_id="bob", query="When is the launch?", top_k=3)
        print(f"\nisolation: bob sees {other.total} hits")
        print("\ndemo: 3 messages · 2 searches · 1 isolation check · no server, no API key")
    finally:
        service.close()


if __name__ == "__main__":
    main()
