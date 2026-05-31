# zh-Hans Custom Inference Test Account Runbook

## Purpose

This runbook defines the minimum safe account state needed to verify `GUI-WS-06` for a public-RC decision.

## Account Requirements

- The account is not the user's main account.
- The account is safe to use in a local debug build of `WarpOss.app`.
- Settings > AI shows `自定义推理`.
- The account can create and remove a disposable custom endpoint.
- The account has no real custom endpoint named `zh-smoke-delete-endpoint`.
- The account is not used for team ownership transfer, billing mutation, cloud environment deletion, or managed secret deletion.

## Disposable Endpoint Values

```text
Name: zh-smoke-delete-endpoint
URL: https://example.com
API key: sk-zh-smoke-dummy-key
Model: zh-smoke-model
Alias: zh-smoke
```

These values are non-secret smoke placeholders. Do not enter a real API key for the disposable endpoint unless a future test explicitly requires an actual model request.

## Debug Fixture Boundary

The debug fixture lane uses `WARP_CN_CUSTOM_INFERENCE_SMOKE=1` only in debug builds. It seeds the disposable endpoint in memory, registers no-op secure storage, and skips the macOS App Group secure-state directory so the GUI smoke does not prompt for Keychain or privacy access.

Fixture evidence can verify localized rendering, edit-modal copy, cancel-delete behavior, and final remove behavior. It cannot satisfy the public-RC account requirement because it does not prove a real logged-in workspace can create and remove a custom endpoint.

## Evidence Requirements

- Process environment proof for `WARP_DATA_PROFILE=zh-rc6`.
- For fixture smoke only, process environment proof for `WARP_CN_CUSTOM_INFERENCE_SMOKE=1`.
- Screenshot showing Settings > AI > `自定义推理`.
- Screenshot showing `zh-smoke-delete-endpoint` after creation.
- Fixture smoke may use the in-memory seeded endpoint instead of the add form.
- Screenshot showing `移除端点？`.
- Screenshot after clicking `取消`, proving the endpoint remains.
- Screenshot after final removal, proving the endpoint is absent.

## Secret Handling

- Do not write passwords, tokens, cookies, magic links, or real API keys to docs.
- Redact account identifiers if screenshots reveal private information.
- Store screenshots only under `docs/gui-smoke-artifacts/phase9/`.
