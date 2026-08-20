# Restoring the campaign branch on GitHub (2 files, 2 minutes)

You received two files:
- campaign_55commits.bundle  (md5 2fabb2392c0143f42fef7d0ff0efaa0e) — ALL 55
  unpushed commits with full git history, on top of the branch tip GitHub
  already has (82a6835).
- state_transfer.tgz (md5 9af7d2d30473e82dc847438483b0fffa) — the same
  content as a plain file tree (141 changed files under 100KB; only large
  regenerable .ms/.gens solver files excluded), in case the bundle route
  is ever inconvenient.

## Easiest path (uses the GitHub web upload you've used before)
1. On github.com, open branch claude/fable-ce-backup, "Add file" -> upload
   BOTH files to the repo root. Commit.
2. Tell Claude "bundle is uploaded". A worker session with working git
   credentials then runs, roughly:
     git clone <repo> && cd <repo>
     git fetch origin claude/fable-ce-backup
     git show origin/claude/fable-ce-backup:campaign_55commits.bundle > /tmp/b.bundle
     git bundle verify /tmp/b.bundle
     git fetch /tmp/b.bundle HEAD:refs/heads/restore
     git push origin restore:claude/opus-5-counterexample-plan-sep6yk
   and the campaign branch on GitHub becomes exactly the local branch,
   full history, correct authorship.

## Alternative (your own machine, if you have git + repo access)
   git clone https://github.com/git-df-scott/jacobian_planar.git && cd jacobian_planar
   git bundle verify /path/to/campaign_55commits.bundle
   git fetch /path/to/campaign_55commits.bundle HEAD:refs/heads/tmp55
   git push origin tmp55:claude/opus-5-counterexample-plan-sep6yk
