# Composio Instagram publishing

This adapter uses the Composio CLI and the Instagram Graph API tools exposed through it. The user must connect an eligible Instagram Business or Creator account before publishing.

## Connect and verify

```bash
composio link instagram
composio execute INSTAGRAM_GET_USER_INFO -d '{"ig_user_id":"me","fields":"id,username,account_type"}'
```

The returned account identity must be checked before posting. Do not assume that the currently connected account is the intended brand account.

## Reel flow

1. Use `INSTAGRAM_POST_IG_USER_MEDIA` to create a `REELS` container from a local `video_file` or a stable direct HTTPS `video_url`.
2. Capture the returned `creation_id`.
3. Use `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` with that `creation_id` and wait for processing.
4. Optionally verify the returned media ID with the Instagram media lookup tool.

`scripts/publish_instagram.py` implements this flow and is dry-run by default. Pass `--publish` only after the user has approved the public action.

## Known pitfalls

- Instagram publishing needs the correct Business/Creator context and `ig_user_id`.
- Direct video URLs must be reachable by Meta and should not be a landing page or an expiring redirect.
- A failed or already-published container cannot be reused; create a new container.
- Reels commonly need 60–120 seconds to process; the publish step waits rather than immediately retrying.
- Never commit Composio credentials or account identifiers that are not intended to be public.

