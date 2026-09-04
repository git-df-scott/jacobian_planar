import copy
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from math_mailbox import (Busy, Conflict, GitHubStore, Mailbox, MailboxError,
                         Pinger, RemoteError, Uncertain, message_path, relay_one)


class MemoryStore:
    repo, branch = "example/research", "mailbox/v2"

    def __init__(self):
        self.rows = {}
        self.lock = threading.Lock()
        self.conflicts = 0
        self.lose_next_response = False

    def ensure_branch(self, base):
        pass

    def get(self, path):
        with self.lock:
            row = self.rows.get(path)
            return (copy.deepcopy(row[0]), row[1]) if row else (None, None)

    def put(self, path, value, sha, commit_message):
        with self.lock:
            current = self.rows.get(path)
            if self.conflicts:
                self.conflicts -= 1
                raise Conflict()
            if sha != (current[1] if current else None):
                raise Conflict()
            version = str(int(sha or "0") + 1)
            self.rows[path] = (copy.deepcopy(value), version)
            if self.lose_next_response:
                self.lose_next_response = False
                raise Uncertain()
            return version

    def paths(self, recipient):
        with self.lock:
            return [p for p in self.rows if p.startswith(f".math-mailbox/messages/{recipient}/")]

    def url(self, message_id):
        return "https://github.com/example/research/blob/mailbox/v2/" + message_path(message_id)


class FakePinger:
    def __init__(self, error=None):
        self.calls = 0
        self.error = error

    def validate(self, recipient, route):
        pass

    def send(self, row, route):
        self.calls += 1
        if self.error:
            raise self.error
        return {"url": "https://example.invalid/receipt"}


class MailboxTests(unittest.TestCase):
    def setUp(self):
        self.now = 1000.0
        self.store = MemoryStore()
        self.box = Mailbox(self.store, lambda: self.now, lambda _: None)
        self.box.init()

    def send(self, key="test-key", body="Please check this candidate.", **kwargs):
        return self.box.send("codex", "claude", "transport test", body, key, "codex-test", **kwargs)

    def enabled(self):
        self.box.configure("claude", "trig_TEST")
        return self.send()["message"]["id"]

    def test_init_is_idempotent_and_does_not_enable_routes(self):
        self.box.init()
        self.assertFalse(self.box.config()["routes"]["claude"]["enabled"])
        self.assertFalse(self.box.config()["routes"]["codex"]["enabled"])

    def test_send_readback_and_retry_preserve_original(self):
        row = self.send()
        self.now += 100
        duplicate = self.send()
        self.assertEqual(row, duplicate)
        self.assertEqual(len(self.box.inbox("claude")), 1)
        self.assertEqual(duplicate["state"]["delivery"]["status"], "pending")

    def test_same_key_with_different_content_is_rejected(self):
        self.send()
        with self.assertRaisesRegex(MailboxError, "different content"):
            self.send(body="Different candidate")

    def test_conflict_is_retried_without_lost_message(self):
        self.store.conflicts = 2
        self.send()
        self.assertEqual(len(self.box.inbox("claude")), 1)

    def test_lost_success_response_does_not_duplicate_send(self):
        self.store.lose_next_response = True
        self.send()
        self.assertEqual(len(self.box.inbox("claude")), 1)

    def test_concurrent_distinct_sends_are_not_lost(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda i: self.send(key=f"message-{i}"), range(16)))
        self.assertEqual(len(self.box.inbox("claude")), 16)

    def test_only_one_concurrent_claimant_wins(self):
        mid = self.send()["message"]["id"]
        def claim(session):
            try:
                self.box.claim(mid, session)
                return session
            except Busy:
                return None
        with ThreadPoolExecutor(max_workers=8) as pool:
            winners = list(pool.map(claim, [f"session-{i}" for i in range(8)]))
        self.assertEqual(len([w for w in winners if w]), 1)

    def test_stale_claim_can_be_reclaimed(self):
        mid = self.send()["message"]["id"]
        self.box.claim(mid, "old", 30)
        self.now += 31
        row = self.box.claim(mid, "new")
        self.assertEqual(row["state"]["claim"]["session"], "new")
        with self.assertRaises(Busy):
            self.box.acknowledge(mid, "old")

    def test_claim_renewal_extends_same_session_lease(self):
        mid = self.send()["message"]["id"]
        self.box.claim(mid, "worker", 30)
        self.now += 20
        row = self.box.claim(mid, "worker", 30)
        self.assertEqual(row["state"]["claim"]["until"], self.now + 30)

    def test_no_false_read_receipt_from_claim_or_delivery(self):
        mid = self.enabled()
        self.box.claim(mid, "worker")
        relay_one(self.box, FakePinger(), mid)
        self.assertIsNone(self.box.get(mid)["state"]["read_at"])
        self.box.acknowledge(mid, "worker")
        self.assertEqual(self.box.get(mid)["state"]["read_at"], self.now)

    def test_ack_requires_live_claim(self):
        mid = self.send()["message"]["id"]
        with self.assertRaises(Busy):
            self.box.acknowledge(mid, "worker")
        self.box.claim(mid, "worker", 30)
        self.now += 31
        with self.assertRaises(Busy):
            self.box.acknowledge(mid, "worker")

    def test_reply_is_addressed_back_and_only_written_once(self):
        mid = self.send()["message"]["id"]
        self.box.claim(mid, "worker")
        answer = self.box.reply(mid, "worker", "This is a transport check, not a mathematical result.")
        again = self.box.reply(mid, "worker", "A duplicate invocation must not post again")
        self.assertEqual(answer, again)
        self.assertEqual(answer["message"]["to"], "codex")
        self.assertEqual(answer["message"]["in_reply_to"], mid)
        self.assertEqual(len(self.box.inbox("codex")), 1)
        self.assertEqual(self.box.inbox("claude"), [])

    def test_reply_crash_after_send_can_be_finalized(self):
        mid = self.send()["message"]["id"]
        self.box.claim(mid, "worker")
        parent = self.box.get(mid)
        saved = self.box.send("claude", "codex", "transport test", "Already saved",
                              "reply:" + mid, "worker", parent=parent)
        answer = self.box.reply(mid, "worker", "Different text after restart")
        self.assertEqual(answer["message"]["id"], saved["message"]["id"])
        self.assertEqual(answer["message"]["body"], "Already saved")
        self.assertEqual(self.box.get(mid)["state"]["reply_id"], answer["message"]["id"])

    def test_round_limit_is_inherited_and_enforced(self):
        mid = self.send(max_rounds=1)["message"]["id"]
        self.box.claim(mid, "worker")
        reply = self.box.reply(mid, "worker", "Final response")
        rid = reply["message"]["id"]
        self.box.claim(rid, "second-worker")
        with self.assertRaisesRegex(MailboxError, "round limit"):
            self.box.reply(rid, "second-worker", "Should not be sent")
        self.box.acknowledge(rid, "second-worker", complete=True)
        self.assertEqual(self.box.inbox("codex"), [])

    def test_expired_messages_are_visible_in_history_only(self):
        mid = self.send(ttl_hours=1)["message"]["id"]
        self.now += 3601
        self.assertEqual(self.box.inbox("claude"), [])
        self.assertEqual(len(self.box.inbox("claude", True)), 1)
        with self.assertRaises(MailboxError):
            self.box.claim(mid, "worker")

    def test_artifact_requires_pinned_commit(self):
        with self.assertRaises(MailboxError):
            self.send(artifacts=["https://github.com/example/research/blob/main/candidate.py"])
        self.send(artifacts=["https://github.com/example/research/blob/" + "a" * 40 + "/candidate.py"])

    def test_routes_cannot_be_arbitrary_webhook_urls(self):
        with self.assertRaises(MailboxError):
            self.box.configure("claude", "https://untrusted.invalid/steal-token")
        with self.assertRaises(MailboxError):
            self.box.configure("codex", 0)

    def test_unconfigured_route_does_not_send(self):
        mid = self.send()["message"]["id"]
        pinger = FakePinger()
        result = relay_one(self.box, pinger, mid)
        self.assertEqual(result["status"], "not_configured")
        self.assertEqual(pinger.calls, 0)

    def test_accepted_ping_is_not_repeated(self):
        mid = self.enabled()
        pinger = FakePinger()
        relay_one(self.box, pinger, mid)
        relay_one(self.box, pinger, mid)
        self.assertEqual(pinger.calls, 1)

    def test_saved_acceptance_survives_missing_destination_credentials(self):
        mid = self.enabled()
        pinger = FakePinger()
        relay_one(self.box, pinger, mid)
        def missing(*args):
            raise MailboxError("Credential is unavailable")
        pinger.validate = missing
        self.assertEqual(relay_one(self.box, pinger, mid)["status"], "accepted")
        self.assertEqual(pinger.calls, 1)

    def test_concurrent_relays_only_one_sends(self):
        mid = self.enabled()
        pinger = FakePinger()
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda _: relay_one(self.box, pinger, mid), range(8)))
        self.assertEqual(pinger.calls, 1)

    def test_read_receipt_does_not_generate_a_ping(self):
        mid = self.enabled()
        self.box.claim(mid, "worker")
        self.box.acknowledge(mid, "worker")
        pinger = FakePinger()
        self.assertEqual(relay_one(self.box, pinger, mid)["status"], "already_read")
        self.assertEqual(pinger.calls, 0)

    def test_uncertain_ping_is_not_automatically_repeated(self):
        mid = self.enabled()
        pinger = FakePinger(Uncertain())
        self.assertEqual(relay_one(self.box, pinger, mid)["status"], "uncertain")
        self.now += 600
        relay_one(self.box, pinger, mid)
        self.assertEqual(pinger.calls, 1)
        pinger.error = None
        self.assertEqual(relay_one(self.box, pinger, mid, True)["status"], "accepted")

    def test_rate_limit_retry_is_delayed_and_bounded(self):
        mid = self.enabled()
        pinger = FakePinger(RemoteError(429))
        relay_one(self.box, pinger, mid)
        relay_one(self.box, pinger, mid)
        self.assertEqual(pinger.calls, 1)
        for _ in range(3):
            self.now += 1000
            relay_one(self.box, pinger, mid)
        self.assertEqual(pinger.calls, 3)
        self.assertEqual(self.box.get(mid)["state"]["delivery"]["status"], "exhausted")

    def test_http_500_is_uncertain_and_401_is_rejected(self):
        for code, expected in [(500, "uncertain"), (401, "rejected")]:
            mid = self.send(key=f"http-{code}")["message"]["id"]
            self.box.configure("claude", "trig_TEST")
            self.assertEqual(relay_one(self.box, FakePinger(RemoteError(code)), mid)["status"], expected)

    def test_relay_crash_becomes_uncertain_after_lease(self):
        mid = self.enabled()
        row, sha = self.store.get(message_path(mid))
        row["state"]["delivery"].update(status="sending", attempt_id="old", lease_until=999, attempts=1)
        self.store.put(message_path(mid), row, sha, "test")
        pinger = FakePinger()
        self.assertEqual(relay_one(self.box, pinger, mid)["status"], "uncertain")
        self.assertEqual(pinger.calls, 0)


class AdapterTests(unittest.TestCase):
    def test_github_store_handles_base64_and_compare_and_swap(self):
        calls = []
        def http(method, url, token, payload, headers):
            calls.append((method, url, payload))
            if method == "GET":
                return {"encoding": "base64", "content": "eyJ4IjogMX0=", "sha": "old-sha"}
            return {"content": {"sha": "new-sha"}}
        store = GitHubStore("owner/repo", token="fake", http=http)
        data, sha = store.get(".math-mailbox/config.json")
        store.put(".math-mailbox/config.json", {"x": 2}, sha, "receipt")
        self.assertEqual(data, {"x": 1})
        self.assertIn("ref=mailbox%2Fv2", calls[0][1])
        self.assertEqual(calls[1][2]["sha"], "old-sha")
        self.assertEqual(calls[1][2]["branch"], "mailbox/v2")

    def test_store_cannot_write_campaign_branch(self):
        with self.assertRaises(MailboxError):
            GitHubStore("owner/repo", "main", token="fake")

    def test_claude_adapter_uses_documented_endpoint_and_session_receipt(self):
        calls = []
        def http(method, url, token, payload, headers):
            calls.append((url, payload, headers))
            return {"claude_code_session_id": "session_123", "claude_code_session_url": "https://claude.ai/code/session_123"}
        store = MemoryStore()
        box = Mailbox(store, lambda: 1000, lambda _: None)
        box.init()
        row = box.send("codex", "claude", "test", "Private candidate body", "key", "session")
        pinger = Pinger(store, "fake", http)
        route = {"kind": "claude_routine", "routine_id": "trig_TEST"}
        pinger.validate("claude", route)
        receipt = pinger.send(row, route)
        self.assertEqual(calls[0][0], "https://api.anthropic.com/v1/claude_code/routines/trig_TEST/fire")
        self.assertNotIn("Private candidate body", json.dumps(calls))
        self.assertEqual(receipt["session_id"], "session_123")

    def test_codex_adapter_recovers_existing_comment_without_posting(self):
        store = MemoryStore()
        box = Mailbox(store, lambda: 1000, lambda _: None)
        box.init()
        row = box.send("claude", "codex", "test", "candidate", "key", "session")
        marker = "<!-- math-mailbox:" + row["message"]["id"] + " -->"
        calls = []
        def api(method, path, payload=None):
            calls.append(method)
            return [{"id": 123, "html_url": "https://github.com/example/research/pull/1#issuecomment-123", "body": marker + "\n@codex handle"}]
        store.api = api
        store.prefix = "/repos/example/research"
        receipt = Pinger(store).send(row, {"pr_number": 1})
        self.assertEqual(receipt["comment_id"], 123)
        self.assertEqual(calls, ["GET"])


if __name__ == "__main__":
    unittest.main()
