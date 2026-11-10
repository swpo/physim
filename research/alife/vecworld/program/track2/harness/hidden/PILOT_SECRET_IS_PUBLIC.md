# This secret is public

`secret.hex` is the noise secret of the round-2 harness pilot on the closed-form toy world. It was committed to
this public repository on 7 Nov 2026 (commit ee48b30b5) and therefore protects nothing. Found by the round-5
agentenv study and its checker on 10 Nov 2026.

- The toy pilot and anything derived from this secret must never be used as an exam.
- The file is kept because the pilot's scripts and saved results refer to it; deleting it from the head of the
  branch would not remove it from the history.
- Rule since then: no study commits a secret. Secrets are drawn at run time (`os.urandom`), kept out of git, and
  only their commitments are stored (see `../../gliders_exam/HIDDEN_NOT_COMMITTED.md` and
  `../../../roadmap/DECISIONS.md`, decision 5).
