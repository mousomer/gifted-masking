# E06 user-owned full verification

The E06 pre-verification package is ready, but this is the required
user-owned full repository gate. Codex did not run it.

Run this command from the repository root. It is intentionally not executed by
the E06 corrective pass.

```bash
cd /Users/omer/workspace/personal/repos/gifted-masking
MPLCONFIGDIR=/private/tmp/e06_user_verify \
./scripts/verify.sh 2>&1 | tee /private/tmp/e06_user_full_verification.log
```

To preserve the verification exit code through `tee`, use this form:

```bash
cd /Users/omer/workspace/personal/repos/gifted-masking
set -o pipefail
MPLCONFIGDIR=/private/tmp/e06_user_verify \
./scripts/verify.sh 2>&1 | tee /private/tmp/e06_user_full_verification.log
verify_status=${pipestatus[1]}
echo "verify exit code: ${verify_status}"
exit ${verify_status}
```

Do not run the E06 standard or qualification configurations after this command.
They remain refused pending a fresh independent Sol review and any required
separate authorization. Preserve `/private/tmp/e06_user_full_verification.log`
for the next assessor.
