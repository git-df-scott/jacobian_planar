#!/usr/bin/env python3
"""A GitHub-backed mailbox for cloud agents. Python 3.10+, standard library only."""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import os
import re
import sys
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = ".math-mailbox"
AGENTS = ("codex", "claude")
DEFAULT_BRANCH = "mailbox/v2"
MAX_ATTEMPTS = 3
DEFAULT_CONFIG = {
    "version": 1,
    "routes": {
        "codex": {"enabled": False, "kind": "codex_pr", "pr_number": None},
        "claude": {"enabled": False, "kind": "claude_routine", "routine_id": None},
    },
}


class MailboxError(Exception):
    pass


class Conflict(MailboxError):
    pass


class Busy(MailboxError):
    pass


class RemoteError(MailboxError):
    def __init__(self, status):
        self.status = status
        super().__init__(f"Remote service returned HTTP {status}")


class Uncertain(MailboxError):
    """A write might have reached the remote service; do not blindly repeat it."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(method, url, token, payload=None, headers=None):
    request_headers = {"Accept": "application/json", "User-Agent": "math-mailbox/1"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
    request_headers.update(headers or {})
    req = Request(url, data=None if payload is None else json.dumps(payload).encode(),
                  headers=request_headers, method=method)
    try:
        with build_opener(NoRedirect()).open(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except HTTPError as exc:
        # Never print response bodies, request headers, or credentials.
        raise RemoteError(exc.code) from None
    except (URLError, TimeoutError, OSError):
        if method in ("POST", "PUT", "PATCH"):
            raise Uncertain("Write outcome unknown; check the saved record before retrying") from None
        raise MailboxError("Remote read failed; retry the read") from None
    except (ValueError, UnicodeError):
        if method in ("POST", "PUT", "PATCH"):
            raise Uncertain("Write returned an unreadable receipt; check before retrying") from None
        raise MailboxError("Remote service returned invalid JSON") from None


def validate_repo(repo):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise MailboxError("Repository must be OWNER/REPO")
    return repo


def validate_branch(branch):
    if (not re.fullmatch(r"mailbox/[A-Za-z0-9][A-Za-z0-9_./-]*", branch)
            or ".." in branch or "//" in branch or branch.endswith(("/", ".", ".lock"))):
        raise MailboxError("Use a dedicated mailbox/ branch, such as mailbox/v2")
    return branch


def message_path(message_id):
    if not re.fullmatch(r"(codex|claude)-[0-9a-f]{32}", message_id):
        raise MailboxError("Invalid message ID")
    return f"{ROOT}/messages/{message_id.split('-')[0]}/{message_id}.json"


def validate_artifact(url):
    if len(url) > 2048 or not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/blob/[0-9a-f]{40}/[^\s?#]+", url):
        raise MailboxError("Artifact links must use a full 40-character commit SHA")
    return url


class GitHubStore:
    def __init__(self, repo, branch=DEFAULT_BRANCH, token=None, http=request_json):
        self.repo = validate_repo(repo)
        self.branch = validate_branch(branch)
        self.token = token if token is not None else (
            os.environ.get("MATH_MAILBOX_GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
            or os.environ.get("GITHUB_TOKEN"))
        if not self.token:
            raise MailboxError("Set MATH_MAILBOX_GITHUB_TOKEN or GH_TOKEN in the cloud environment")
        self.http = http

    def api(self, method, path, payload=None):
        return self.http(method, "https://api.github.com" + path, self.token, payload,
                         {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"})

    @property
    def prefix(self):
        return f"/repos/{self.repo}"

    def ensure_branch(self, base="main"):
        path = self.prefix + "/git/ref/heads/" + quote(self.branch, safe="/")
        try:
            self.api("GET", path)
            return
        except RemoteError as exc:
            if exc.status != 404:
                raise
        head = self.api("GET", self.prefix + "/git/ref/heads/" + quote(base, safe="/"))
        try:
            self.api("POST", self.prefix + "/git/refs",
                     {"ref": "refs/heads/" + self.branch, "sha": head["object"]["sha"]})
        except (Uncertain, RemoteError) as exc:
            if isinstance(exc, RemoteError) and exc.status != 422:
                raise
            self.api("GET", path)  # Concurrent initialization, or a lost success response.

    def get(self, path):
        endpoint = self.prefix + "/contents/" + quote(path, safe="/")
        try:
            data = self.api("GET", endpoint + "?" + urlencode({"ref": self.branch}))
        except RemoteError as exc:
            if exc.status == 404:
                return None, None
            raise
        if data.get("encoding") != "base64":
            raise MailboxError("Mailbox record is not a small UTF-8 JSON file")
        try:
            return json.loads(base64.b64decode(data["content"])), data["sha"]
        except (ValueError, KeyError, UnicodeError):
            raise MailboxError("Mailbox record is corrupt") from None

    def put(self, path, value, sha, commit_message):
        raw = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()
        payload = {"message": commit_message, "branch": self.branch,
                   "content": base64.b64encode(raw).decode()}
        if sha is not None:
            payload["sha"] = sha
        try:
            result = self.api("PUT", self.prefix + "/contents/" + quote(path, safe="/"), payload)
        except RemoteError as exc:
            if exc.status in (409, 422):
                raise Conflict("Mailbox changed concurrently; reread before writing") from None
            raise
        return result["content"]["sha"]

    def paths(self, recipient):
        # Tree API avoids the Contents API's 1,000-entry directory limit.
        head = self.api("GET", self.prefix + "/git/ref/heads/" + quote(self.branch, safe="/"))
        commit = self.api("GET", self.prefix + "/git/commits/" + head["object"]["sha"])
        tree = self.api("GET", self.prefix + "/git/trees/" + commit["tree"]["sha"] + "?recursive=1")
        if tree.get("truncated"):
            raise MailboxError("Mailbox tree is too large; rotate to a new mailbox/ branch")
        prefix = f"{ROOT}/messages/{recipient}/"
        return [x["path"] for x in tree["tree"] if x["type"] == "blob"
                and x["path"].startswith(prefix) and x["path"].endswith(".json")]

    def url(self, message_id):
        return f"https://github.com/{self.repo}/blob/{self.branch}/{message_path(message_id)}"


class Mailbox:
    def __init__(self, store, clock=time.time, pause=time.sleep):
        self.store, self.clock, self.pause = store, clock, pause

    def mutate(self, path, update, subject="receipt"):
        for attempt in range(6):
            value, sha = self.store.get(path)
            changed = update(copy.deepcopy(value))
            if changed == value:
                return value
            try:
                self.store.put(path, changed, sha, f"[mailbox] {subject}")
            except (Conflict, Uncertain):
                self.pause(min(0.2 * (2 ** attempt), 3))
                continue  # All mutations are reread and applied idempotently.
            saved, _ = self.store.get(path)
            if saved is None:
                raise Uncertain("Remote write was not visible on readback")
            return saved
        raise Conflict("Mailbox stayed busy; retry with the same message key")

    def init(self, base="main"):
        self.store.ensure_branch(base)
        return self.mutate(f"{ROOT}/config.json", lambda old: old or copy.deepcopy(DEFAULT_CONFIG), "initialize")

    def config(self):
        value, _ = self.store.get(f"{ROOT}/config.json")
        if not value or value.get("version") != 1:
            raise MailboxError("Initialize this mailbox first")
        return value

    def configure(self, recipient, target=None, disabled=False):
        if recipient not in AGENTS:
            raise MailboxError("Recipient must be codex or claude")
        if not disabled:
            if recipient == "codex" and (not isinstance(target, int) or target < 1):
                raise MailboxError("Codex needs a pull request number in this repository")
            if recipient == "claude" and not re.fullmatch(r"trig_[A-Za-z0-9]+", str(target)):
                raise MailboxError("Claude needs a routine trigger ID beginning trig_")
        def update(config):
            if config is None:
                raise MailboxError("Initialize this mailbox first")
            route = config["routes"][recipient]
            route["enabled"] = not disabled
            if not disabled:
                route["pr_number" if recipient == "codex" else "routine_id"] = target
            return config
        return self.mutate(f"{ROOT}/config.json", update, "configure")

    def get(self, message_id):
        value, _ = self.store.get(message_path(message_id))
        if value is None:
            raise MailboxError("Message not found")
        if value.get("version") != 1 or value.get("message", {}).get("id") != message_id:
            raise MailboxError("Mailbox record is corrupt or has an unsupported version")
        return value

    def send(self, sender, recipient, topic, body, key, session, artifacts=(),
             max_rounds=6, ttl_hours=168, parent=None):
        self.config()
        if sender not in AGENTS or recipient not in AGENTS or sender == recipient:
            raise MailboxError("Send between codex and claude")
        if not key or len(key) > 200 or not session or len(session) > 200:
            raise MailboxError("A stable message key and session ID are required (at most 200 characters each)")
        if not 1 <= len(topic) <= 160 or not 1 <= len(body.encode()) <= 48000:
            raise MailboxError("Topic must be 1–160 characters; body must be 1–48,000 UTF-8 bytes")
        if not 1 <= max_rounds <= 20 or not 1 <= ttl_hours <= 720 or len(artifacts) > 20:
            raise MailboxError("Use 1–20 rounds, 1–720 hours, and at most 20 artifact links")
        artifacts = [validate_artifact(url) for url in artifacts]
        message_id = recipient + "-" + hashlib.sha256((sender + "\0" + key).encode()).hexdigest()[:32]
        now = self.clock()
        message = {"id": message_id, "from": sender, "to": recipient, "sender_session": session,
                   "topic": topic, "body": body, "artifacts": artifacts, "in_reply_to": None,
                   "conversation": message_id, "round": 0, "max_rounds": max_rounds,
                   "created_at": now, "expires_at": now + ttl_hours * 3600}
        if parent is not None:
            p = parent["message"]
            if p["to"] != sender or p["from"] != recipient or p["round"] >= p["max_rounds"]:
                raise MailboxError("Reply route is invalid or this conversation reached its round limit")
            if p["expires_at"] <= now:
                raise MailboxError("Conversation has expired")
            message.update(in_reply_to=p["id"], conversation=p["conversation"],
                           round=p["round"] + 1, max_rounds=p["max_rounds"], expires_at=p["expires_at"])
        record = {"version": 1, "message": message,
                  "state": {"claim": None, "read_at": None, "reader_session": None,
                            "handled_at": None, "reply_id": None,
                            "delivery": {"status": "pending", "attempts": 0, "next_attempt_at": 0}}}
        def create(existing):
            if existing is None:
                return record
            # A retried send must not change the message or extend its expiry.
            fields = ("from", "to", "topic", "body", "artifacts", "in_reply_to", "max_rounds")
            if any(existing["message"].get(field) != message[field] for field in fields):
                raise MailboxError("This message key already exists with different content")
            return existing
        return self.mutate(message_path(message_id), create, "send " + message_id)

    def inbox(self, recipient, include_handled=False):
        if recipient not in AGENTS:
            raise MailboxError("Recipient must be codex or claude")
        rows = []
        for path in self.store.paths(recipient):
            row = self.get(path.rsplit("/", 1)[1][:-5])
            if include_handled or (not row["state"]["handled_at"] and row["message"]["expires_at"] > self.clock()):
                rows.append(row)
        return sorted(rows, key=lambda row: (row["message"]["created_at"], row["message"]["id"]))

    def claim(self, message_id, session, lease_seconds=900):
        if not session or len(session) > 200 or not 30 <= lease_seconds <= 3600:
            raise MailboxError("Supply a session ID and a lease of 30–3,600 seconds")
        now = self.clock()
        def update(row):
            if row is None or row["message"]["expires_at"] <= now:
                raise MailboxError("Message is missing or expired")
            state = row["state"]
            if state["handled_at"]:
                raise Busy("Message is already handled")
            claim = state["claim"]
            if claim and claim["session"] != session and claim["until"] > now:
                raise Busy("Another session holds this message")
            state["claim"] = {"session": session, "until": min(now + lease_seconds, row["message"]["expires_at"])}
            return row
        row = self.mutate(message_path(message_id), update)
        if row["state"]["claim"]["session"] != session:
            raise Busy("Another session acquired the claim")
        return row

    def require_claim(self, row, session):
        claim = row["state"]["claim"]
        if not claim or claim["session"] != session or claim["until"] <= self.clock():
            raise Busy("Claim this message with your session ID first; renew an expired lease")

    def acknowledge(self, message_id, session, complete=False):
        now = self.clock()
        def update(row):
            if row is None:
                raise MailboxError("Message not found")
            if row["state"]["handled_at"]:
                return row
            self.require_claim(row, session)
            row["state"]["read_at"] = row["state"]["read_at"] or now
            row["state"]["reader_session"] = session
            if complete:
                row["state"]["handled_at"] = now
                row["state"]["claim"] = None
            return row
        return self.mutate(message_path(message_id), update)

    def reply(self, message_id, session, body, artifacts=()):
        parent = self.get(message_id)
        p = parent["message"]
        if parent["state"]["reply_id"]:
            return self.get(parent["state"]["reply_id"])
        self.require_claim(parent, session)
        # One deterministic reply slot per message, including crash recovery.
        key = "reply:" + message_id
        reply_id = p["from"] + "-" + hashlib.sha256((p["to"] + "\0" + key).encode()).hexdigest()[:32]
        existing, _ = self.store.get(message_path(reply_id))
        if existing is not None:
            if existing["message"].get("in_reply_to") != message_id:
                raise MailboxError("Reply slot contains an unrelated message")
            answer = existing
        else:
            try:
                answer = self.send(p["to"], p["from"], p["topic"], body, key, session,
                                   artifacts, p["max_rounds"], parent=parent)
            except MailboxError:
                # A worker with a reclaimed lease may have filled the same slot.
                existing, _ = self.store.get(message_path(reply_id))
                if not existing or existing["message"].get("in_reply_to") != message_id:
                    raise
                answer = existing
        now = self.clock()
        def finish(row):
            row["state"].update(reply_id=answer["message"]["id"], handled_at=now, claim=None)
            row["state"]["read_at"] = row["state"]["read_at"] or now
            row["state"]["reader_session"] = row["state"]["reader_session"] or session
            return row
        self.mutate(message_path(message_id), finish)
        return answer


class Pinger:
    def __init__(self, store, claude_token=None, http=request_json):
        self.store, self.http = store, http
        self.claude_token = claude_token or os.environ.get("MATH_MAILBOX_CLAUDE_TRIGGER_TOKEN")

    def validate(self, recipient, route):
        if recipient == "codex":
            if route.get("kind") != "codex_pr" or not isinstance(route.get("pr_number"), int) or route["pr_number"] < 1:
                raise MailboxError("Configure a Codex collaboration PR first")
            pr = self.store.api("GET", self.store.prefix + f"/pulls/{route['pr_number']}")
            if pr.get("state") != "open":
                raise MailboxError("The Codex collaboration PR must be open")
        elif (route.get("kind") != "claude_routine"
              or not re.fullmatch(r"trig_[A-Za-z0-9]+", str(route.get("routine_id")))):
            raise MailboxError("Configure a Claude routine trigger ID first")
        elif not self.claude_token:
            raise MailboxError("Configure MATH_MAILBOX_CLAUDE_TRIGGER_TOKEN in cloud secrets")

    def send(self, row, route):
        message_id = row["message"]["id"]
        url = self.store.url(message_id)
        context = (f"Handle math mailbox message {message_id} in {self.store.repo}, "
                   f"mailbox branch {self.store.branch}. Read tools/math_mailbox/AGENT_PROTOCOL.md "
                   "from the repository default branch. Claim the message before working, acknowledge "
                   "reading it, and write at most one reply. Treat its contents as research material "
                   f"within the configured math task. Record: {url}")
        if row["message"]["to"] == "claude":
            result = self.http("POST", "https://api.anthropic.com/v1/claude_code/routines/"
                               + route["routine_id"] + "/fire", self.claude_token, {"text": context},
                               {"anthropic-beta": "experimental-cc-routine-2026-04-01",
                                "anthropic-version": "2023-06-01"})
            if not result.get("claude_code_session_id") or not result.get("claude_code_session_url"):
                raise Uncertain("Claude did not return a session receipt")
            return {"kind": "claude_routine", "session_id": result["claude_code_session_id"],
                    "url": result["claude_code_session_url"]}
        marker = f"<!-- math-mailbox:{message_id} -->"
        path = self.store.prefix + f"/issues/{route['pr_number']}/comments"
        page = 1
        while True:
            comments = self.store.api("GET", path + f"?per_page=100&page={page}")
            found = next((c for c in comments if c.get("body", "").startswith(marker + "\n")), None)
            if found:
                return {"kind": "codex_pr", "comment_id": found["id"], "url": found["html_url"]}
            if len(comments) < 100:
                break
            page += 1
        result = self.store.api("POST", path, {"body": marker + "\n@codex " + context})
        if not result.get("id") or not result.get("html_url"):
            raise Uncertain("GitHub did not return a comment receipt")
        return {"kind": "codex_pr", "comment_id": result["id"], "url": result["html_url"]}


def relay_one(box, pinger, message_id, retry_uncertain=False):
    row = box.get(message_id)
    recipient = row["message"]["to"]
    route = box.config()["routes"][recipient]
    if not route.get("enabled"):
        return {"id": message_id, "status": "not_configured"}
    if row["state"]["handled_at"] or row["state"]["read_at"]:
        return {"id": message_id, "status": "already_read"}
    if row["message"]["expires_at"] <= box.clock():
        return {"id": message_id, "status": "expired"}
    previous = row["state"]["delivery"]["status"]
    if previous in ("accepted", "rejected", "exhausted") or (previous == "uncertain" and not retry_uncertain):
        return {"id": message_id, "status": previous}
    pinger.validate(recipient, route)
    attempt_id = uuid.uuid4().hex
    now = box.clock()
    def acquire(record):
        state, delivery = record["state"], record["state"]["delivery"]
        if state["handled_at"] or state["read_at"] or record["message"]["expires_at"] <= now:
            return record
        status = delivery["status"]
        if status == "sending":
            if delivery["lease_until"] > now:
                return record
            delivery.update(status="uncertain", error="Previous relay stopped without a receipt")
            return record
        if status in ("accepted", "rejected", "exhausted"):
            return record
        if status == "uncertain" and not retry_uncertain:
            return record
        if delivery["attempts"] >= MAX_ATTEMPTS:
            delivery.update(status="exhausted")
            return record
        if delivery.get("next_attempt_at", 0) > now:
            return record
        delivery.update(status="sending", attempt_id=attempt_id, lease_until=now + 120,
                        attempts=delivery["attempts"] + 1, attempted_at=now)
        return record
    current = box.mutate(message_path(message_id), acquire)
    delivery = current["state"]["delivery"]
    if delivery.get("attempt_id") != attempt_id or delivery["status"] != "sending":
        return {"id": message_id, "status": delivery["status"]}
    try:
        receipt = pinger.send(current, route)
        outcome = {"status": "accepted", "receipt": receipt, "accepted_at": box.clock(), "error": None}
    except Uncertain:
        outcome = {"status": "uncertain", "error": "Remote acceptance unknown; inspect destination before retrying"}
    except RemoteError as exc:
        # 429 explicitly rejects the request and can be retried. A 5xx may follow
        # an accepted POST, so keep it uncertain rather than multiply AI runs.
        status = "failed" if exc.status == 429 else ("uncertain" if exc.status >= 500 else "rejected")
        outcome = {"status": status, "error": f"HTTP {exc.status}",
                   "next_attempt_at": box.clock() + 60 * (2 ** (delivery["attempts"] - 1))}
    def finish(record):
        d = record["state"]["delivery"]
        if d.get("attempt_id") == attempt_id:
            d.update(outcome)
            d.pop("lease_until", None)
        return record
    result = box.mutate(message_path(message_id), finish)
    return {"id": message_id, **result["state"]["delivery"]}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=os.environ.get("MATH_MAILBOX_REPO"), help="OWNER/REPO")
    p.add_argument("--branch", default=os.environ.get("MATH_MAILBOX_BRANCH", DEFAULT_BRANCH))
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init").add_argument("--base", default="main")
    c = sub.add_parser("configure")
    c.add_argument("--to", choices=AGENTS, required=True)
    target = c.add_mutually_exclusive_group(required=True)
    target.add_argument("--pr", type=int)
    target.add_argument("--routine")
    target.add_argument("--disable", action="store_true")
    sub.add_parser("config")
    c = sub.add_parser("send")
    c.add_argument("--from", dest="sender", choices=AGENTS, required=True)
    c.add_argument("--to", choices=AGENTS, required=True)
    c.add_argument("--topic", required=True)
    c.add_argument("--body-file", required=True, help="UTF-8 file, or - for stdin")
    c.add_argument("--key", required=True, help="Unique stable key; reuse it on retries")
    c.add_argument("--session", required=True)
    c.add_argument("--artifact", action="append", default=[])
    c.add_argument("--max-rounds", type=int, default=6)
    c.add_argument("--ttl-hours", type=int, default=168)
    for name in ("inbox", "wait"):
        c = sub.add_parser(name)
        c.add_argument("--to", choices=AGENTS, required=True)
        c.add_argument("--topic")
        if name == "inbox":
            c.add_argument("--all", action="store_true")
        else:
            c.add_argument("--seconds", type=int, default=30)
    c = sub.add_parser("get")
    c.add_argument("id")
    for name in ("claim", "ack", "complete", "reply"):
        c = sub.add_parser(name)
        c.add_argument("id")
        c.add_argument("--session", required=True)
        if name == "claim":
            c.add_argument("--lease-seconds", type=int, default=900)
        if name == "reply":
            c.add_argument("--body-file", required=True)
            c.add_argument("--artifact", action="append", default=[])
    c = sub.add_parser("relay")
    c.add_argument("--id", help="Only this message")
    c.add_argument("--retry-uncertain", action="store_true")
    return p


def read_body(path):
    if path == "-":
        return sys.stdin.read(48001)
    with open(path, encoding="utf-8") as stream:
        return stream.read(48001)


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if not args.repo:
            raise MailboxError("Supply --repo or MATH_MAILBOX_REPO")
        box = Mailbox(GitHubStore(args.repo, args.branch))
        cmd = args.command
        if cmd == "init":
            result = box.init(args.base)
        elif cmd == "config":
            result = box.config()
        elif cmd == "configure":
            if (args.to == "codex" and args.routine) or (args.to == "claude" and args.pr):
                raise MailboxError("Use --pr for codex or --routine for claude")
            result = box.configure(args.to, args.pr or args.routine, args.disable)
        elif cmd == "send":
            result = box.send(args.sender, args.to, args.topic, read_body(args.body_file), args.key,
                              args.session, args.artifact, args.max_rounds, args.ttl_hours)
        elif cmd in ("inbox", "wait"):
            if cmd == "wait" and not 1 <= args.seconds <= 55:
                raise MailboxError("Wait duration must be 1–55 seconds")
            deadline = time.monotonic() + (args.seconds if cmd == "wait" else 0)
            while True:
                result = box.inbox(args.to, getattr(args, "all", False))
                if args.topic:
                    result = [r for r in result if r["message"]["topic"] == args.topic]
                if result or time.monotonic() >= deadline:
                    break
                time.sleep(min(10, max(0, deadline - time.monotonic())))
        elif cmd == "get":
            result = box.get(args.id)
        elif cmd == "claim":
            result = box.claim(args.id, args.session, args.lease_seconds)
        elif cmd in ("ack", "complete"):
            result = box.acknowledge(args.id, args.session, cmd == "complete")
        elif cmd == "reply":
            result = box.reply(args.id, args.session, read_body(args.body_file), args.artifact)
        else:
            if args.retry_uncertain and not args.id:
                raise MailboxError("Uncertain retries require a specific --id")
            ids = [args.id] if args.id else [r["message"]["id"] for agent in AGENTS for r in box.inbox(agent)]
            pinger = Pinger(box.store)
            result = []
            for message_id in ids:
                try:
                    result.append(relay_one(box, pinger, message_id, args.retry_uncertain))
                except MailboxError as exc:
                    result.append({"id": message_id, "status": "error", "error": str(exc)})
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if cmd == "relay" and any(r["status"] in ("error", "rejected", "uncertain", "exhausted") for r in result) else 0
    except (MailboxError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
