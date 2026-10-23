# Browser and file handling

Use the client-supported browser and file APIs, not assumptions about a particular Playwright wrapper. One client may provide `setInputFiles`; another may require a filechooser event and a chooser object's `setFiles`. Discover the supported mechanism and follow its documentation. Do not invent methods or switch to an unsupported lower-level API.

## Uploads

Use absolute paths to the intended files in the ignored credential directory. Register a chooser listener before clicking the upload control when the client requires it. Prefer a supported file-input API over an OS dialog. Native-picker automation is possible only where the host explicitly supports it and its policies permit it; otherwise give the user the exact file path and leave the correct wizard step open.

For a browser-extension upload failure, follow that client's documented permission/troubleshooting instructions. File-URL access can be required by some extensions, but it is not a universal browser requirement. Do not broaden extension or website permissions speculatively.

After one failed attempt, inspect the current page for a blocker before retrying. Once the mechanism is known unavailable, batch remaining manual file selections where practical instead of repeating identical failing calls. Password entry remains a user handoff unless the user chose the disclosed MCP transport.

## Downloads

Register the supported download listener before clicking. A timeout does not prove the download failed: inspect the browser's download state or narrowly check the expected filename in the known download directory. Confirm the file's identity before moving it. Avoid duplicate one-time key creation because an event was missed.

Move sensitive downloads promptly to `credentials/`, preserving existing files and restrictive permissions. For a sandbox-restricted move, use the host's approval mechanism; do not silently leave a one-time private key in a broadly shared location or bypass filesystem controls.

## Verify changes

Allow asynchronous saves/navigation to settle using the client's observation APIs. Refresh the relevant state before choosing the next action; old errors and previous wizard steps can linger during navigation. Reopen the saved credential record to verify actual state instead of repeating a mutation.

Keep screenshots clear of passwords, private-key contents, complete service-account JSON, and sensitive clipboard data. If sharing proof, show a saved status or checklist with no secret material. A displayed key ID is not proof that the corresponding private key was uploaded or accepted by the store.
