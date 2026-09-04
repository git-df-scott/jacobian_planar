"""Exercise real GitHub storage in Actions; all agent destinations stay disabled."""

import os

from math_mailbox import GitHubStore, Mailbox, Pinger, RemoteError, relay_one


def main():
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("This integration check runs only in GitHub Actions")
    branch = "mailbox/ci-" + os.environ["GITHUB_RUN_ID"] + "-" + os.environ["GITHUB_RUN_ATTEMPT"]
    store = GitHubStore(os.environ["GITHUB_REPOSITORY"], branch)
    ref = store.prefix + "/git/refs/heads/" + branch
    try:
        store.api("GET", store.prefix + "/git/ref/heads/" + branch)
    except RemoteError as exc:
        if exc.status != 404:
            raise
    else:
        raise RuntimeError("Test branch already exists; refusing to reuse or delete it")

    store.ensure_branch(os.environ["GITHUB_REF_NAME"])
    try:
        box = Mailbox(store)
        config = box.init()
        assert not any(route["enabled"] for route in config["routes"].values())
        args = ("codex", "claude", "Mailbox transport check", "Synthetic transport check only.",
                "cloud-smoke", "ci-codex")
        row = box.send(*args, max_rounds=1)
        mid = row["message"]["id"]
        assert box.send(*args, max_rounds=1) == row
        assert len(box.inbox("claude")) == 1
        assert relay_one(box, Pinger(store), mid)["status"] == "not_configured"
        assert box.get(mid)["state"]["read_at"] is None
        box.claim(mid, "ci-claude")
        box.acknowledge(mid, "ci-claude")
        assert box.get(mid)["state"]["read_at"] is not None
        reply = box.reply(mid, "ci-claude", "Transport received; no mathematical claim.")
        rid = reply["message"]["id"]
        assert box.get(mid)["state"]["reply_id"] == rid
        assert reply["message"]["to"] == "codex"
        box.claim(rid, "ci-codex")
        box.acknowledge(rid, "ci-codex", complete=True)
        assert box.inbox("codex") == box.inbox("claude") == []
        print("PASS: real GitHub send, readback, deduplication, claim, ACK, reply, completion.")
        print("Both agent ping routes remained disabled.")
    finally:
        store.api("DELETE", ref)
        print("Removed this run's temporary mailbox branch.")


if __name__ == "__main__":
    main()
