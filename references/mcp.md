# Bifrost MCP access

Use the [official connection guide](https://bifrost.nativephp.com/docs/mobile/teams/mcp) and the tools actually exposed by the client. The production OAuth endpoint is `https://bifrost.nativephp.com/mcp/oauth`; use the environment-specific endpoint for a preview environment.

## Connect and discover

Use the client's authenticate/reconnect flow. The user signs in and approves OAuth access. Team management also depends on membership, team MCP enablement, feature availability, and subscription eligibility. Do not enable broader access or purchase a subscription without the corresponding authorization.

Discover available tools again after authentication. Names such as `get-started`, `list-teams`, `list-projects`, and credential-upload operations are examples, not guaranteed client identifiers. Pass the selected team's identifier where required by the live schema. Selecting a team in MCP does not necessarily change the dashboard's selected team.

If only authentication tools are exposed, complete that supported flow before assuming project tools are unavailable. If a redirect fails, use a documented callback-completion tool only when present and permitted by the client. Treat callback URLs as sensitive: they can contain authorization codes; do not put them in logs or request them in an ordinary chat message as the default recovery path.

The public MCP guide advertises project discovery, credential upload, credits, builds, and workflows. It does not define every managed-signing operation. Inspect the current schema before deciding whether managed creation, team-key reuse, renewal, or store validation can be done through MCP. Use the browser for unsupported operations rather than inventing tools or parameters.

## Credential transport

Prefer existing team-key references or managed operations when supported; these can avoid retransmitting private material. OAuth permission alone does not authorize uploading a different key.

If an operation requires raw/base64 files or plaintext passwords, explain before reading/transmitting them:

- MCP can automate the upload, but the private material may appear in tool arguments retained in the conversation or client logs.
- The browser alternative lets the user enter signing passwords directly and can avoid putting those values into tool arguments.

Obtain the user's transport choice once for the stated files, destination, and scope. For authorized MCP upload, read existing passwords from the appropriate `.env` variables or another approved source in memory, then call the tool without printing those values. Follow the live file-transport schema; do not run a base64 command whose output will be captured in the transcript just to copy it into another tool.

Keep read-only discovery separate from uploads, access grants, builds, and workflows. A workflow may start multiple builds or send configured notifications; permission to set up credentials does not authorize running it.
