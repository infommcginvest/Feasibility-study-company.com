# WEB-FSC-6 decisions log

D1 (step zero). macOS has no `timeout`/`gtimeout`; every subprocess and network call is wrapped in `perl -e 'alarm N; exec @ARGV'` or a Python `timeout=` argument.
D2 (step zero). Cut from local `main` = `origin/main` = 1d48cc2. Rollback point = Netlify deploy 6acc9381d815c5ea34cbeee7.
