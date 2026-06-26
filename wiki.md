# FDScript Wiki

> A lightweight scripting language for Discord bots — built into **FDSB**.
> Scripts run line-by-line; commands start with `$` and take arguments inside `[]` separated by `;`.

---

## 📑 Table of Contents

### Core
- [Syntax Rules](#syntax-rules)
- [Plain Text Lines](#plain-text-lines)
- [Inline Comments](#inline-comments)
- [Escape Sequences](#escape-sequences)
- [Inline Commands Reference](#inline-commands-reference)
- [Variable Resolution Order](#variable-resolution-order)
- [Error System](#error-system)

### Variables
- [`$var` — Temporary Variables](#var--temporary-variables)
- [`$setVar` / `$getVar` — Persistent Variables](#setvar--getvar--persistent-variables)
- [Built-in Variables](#built-in-variables)

### Messaging
- [`$sendMessage`](#sendmessage)
- [`$reply`](#reply)
- [`$dm`](#dm)
- [`$image`](#image)

### Embed Builder
- [Inline Embed Commands](#embed-builder)
- [`$sendEmbedMessage`](#sendembedmessage)

### Moderation
- [`$ban`](#ban)
- [`$kick`](#kick)
- [`$unban`](#unban)
- [`$timeout` / `$untimeout`](#timeout--untimeout)
- [`$slowmode`](#slowmode)
- [`$deletecommand`](#deletecommand)
- [`$clear`](#clear)

### Access Control
- [`$onlyAdmin`](#onlyadmin)
- [`$onlyIf`](#onlyif)
- [`$strictArgs`](#strictargs)
- [`$cooldown`](#cooldown)

### Math
- [`$sum` `$sub` `$mul` `$div` `$mod`](#math-commands)

### Randomness
- [`$randomint`](#randomint)
- [`$randomstr`](#randomstr)
- [`$randomUserID`](#randomuserid)

### String Utilities
- [`$replaceText`](#replacetext)

### Flow Control
- [`$if` / `$elif` / `$else` / `$endif`](#conditions-if--elif--else--endif)
- [`$and` / `$or`](#compound-conditions-and--or)
- [`$while` / `$endwhile`](#while--endwhile)
- [`$for` / `$endfor`](#for--endfor)
- [`$break`](#break)
- [`$wait`](#wait)
- [`$replyIn`](#replyin)

### Bot Info
- [`$ping`](#ping)
- [`$uptime`](#uptime)
- [`$addTimestamp`](#addtimestamp)
- [`$getBotInvent`](#getbotinvent)
- [`$clientTyping`](#clienttyping)

### Logging & Reactions
- [`$log`](#log)
- [`$addUserReactions`](#adduserreactions)
- [`$addBotReactions`](#addbotreactions)

### Return Commands
- [`$return`](#return)
- [`$returnGuildUsersID`](#returnguildusersid)
- [`$returnGuildChannelsID`](#returnguildchannelsid)
- [`$returnGuildRolesID`](#returnguildrolesid)
- [`$returnGetReactions`](#returngetreactions)

### Events
- [`$onJoined`](#onjoined)
- [`$onLeave`](#onleave)
- [`$alwaysReply`](#alwaysreply)

### Reference
- [Separators](#separators)
- [Color Names](#color-names)
- [Full Examples](#full-examples)

---

## Syntax Rules

| Rule | Details |
|------|---------|
| Commands start with `$` | `$sendMessage[Hello]` |
| Arguments go inside `[]` | Separated by `;` |
| Whitespace is ignored | Around tokens at line boundaries |
| `#` starts a comment | Whole line or inline (outside brackets) |
| No `$` prefix → plain text | Sent verbatim to the channel (built-ins resolved first) |
| Unclosed `[` | → Syntax Error |
| Extra `]` | → Syntax Error |
| **Pre-execution validation** | All errors are found and reported before anything runs |

> **Important:** The entire script is validated before execution starts. If any error is found, nothing runs and every error is reported at once.

---

## Plain Text Lines

Any line that does **not** start with `$` is sent directly to the channel. Built-in variables and inline expressions are resolved inside it before sending.

```
Welcome, $authorName!
Your channel is #$channelName.
```

**Output:**
```
Welcome, user!
Your channel is #general.
```

Empty lines and lines that resolve to only whitespace are silently skipped — no blank messages are sent.

---

## Inline Comments

Comments can appear at the end of any line, outside brackets. Everything after a bare `#` at bracket depth 0 is ignored.

```
$var[score; 100]           # set initial score
$sendMessage[$var[score]]  # send it
```

Whole-line comments also work:

```
# This entire line is ignored
$sendMessage[This line runs]
```

---

## Escape Sequences

Escape sequences let you embed special characters inside any string. The backslash `\` is the escape character.

| Sequence | Result |
|----------|--------|
| `\n` | Newline |
| `\t` | Tab |
| `\r` | Carriage return |
| `\\` | Literal backslash |
| `\0` | Null character |
| `\'` | Single quote |
| `\"` | Double quote |
| `\a` | Bell |
| `\b` | Backspace |
| `\f` | Form feed |
| `\v` | Vertical tab |

Escape sequences are processed in **all** strings — plain text lines, command arguments, and inline expressions. They are applied before variable and command resolution.

**Example:**
```
$sendMessage[Line one\nLine two\nLine three]
```
```
Line one
Line two
Line three
```

```
$var[tab_example; column1\t\tcolumn2]
$sendMessage[$var[tab_example]]
```
```
column1		column2
```

> Unknown escape sequences (e.g. `\q`) are passed through unchanged.

---

## Inline Commands Reference

Some commands can be used **inside** other commands' arguments — they resolve to a string value before the outer command runs. Others can only be used as **standalone** statements.

### Bare Inline Variables (no brackets needed)

These can appear anywhere in text — plain lines or inside any argument:

| Variable | Description |
|----------|-------------|
| `$authorID` | ID of the message author |
| `$authorName` | Username of the message author |
| `$mention` | Mention string of the author |
| `$botID` | Bot's numeric ID |
| `$botName` | Bot's username |
| `$channelID` | Current channel's numeric ID |
| `$channelName` | Current channel's name |
| `$guildID` | Server's numeric ID |
| `$guildName` | Server's name |
| `$messageID` | ID of the triggering message |
| `$message` | Full text after the command trigger |
| `$ping` | Bot latency in milliseconds |
| `$uptime` | Time since bot started |
| `$addTimestamp` | Discord timestamp for now (T format) |
| `$randomUserID` | ID of a random non-bot member |

### Inline Commands With Arguments

These can be nested inside other commands' arguments and return a value:

| Command | Usage |
|---------|-------|
| `$var[name]` | Read a temporary variable |
| `$var[name; value]` | Set a temporary variable (returns empty string) |
| `$getVar[name]` | Read a global persistent variable |
| `$getVar[name; userID]` | Read a per-user persistent variable |
| `$return[varName]` | Read a return variable |
| `$message[n]` | The nth word after the command trigger |
| `$randomint[min; max]` | Random integer |
| `$randomstr[a; b; ...]` | Random string from list |
| `$sum[a; b]` | Addition |
| `$sub[a; b]` | Subtraction |
| `$mul[a; b]` | Multiplication |
| `$div[a; b]` | Division |
| `$mod[a; b]` | Modulo |
| `$replaceText[text; search; replacement]` | String replacement |

**Example — nesting inline commands:**
```
$sendMessage[You rolled: $randomint[1; 6] and $randomint[1; 6]]
$sendMessage[Score after bonus: $sum[$var[score]; 10]]
$sendMessage[$replaceText[$var[msg]; bad; ***]]
```

> Commands **not** in the above tables (e.g. `$sendMessage`, `$ban`, `$if`, `$log`) are **standalone only** — they cannot be nested inside another command's arguments. Using them there produces a Logic Error message inline.

---

## Variable Resolution Order

When any expression is resolved, the order is:

1. Escape sequences are processed first (`\n` → newline, etc.)
2. Built-in bare inline variables (`$authorID`, `$ping`, etc.)
3. Inline commands with arguments (`$var[name]`, `$getVar[name]`, etc.)
4. Module-based inline resolvers (commands with a `resolve_inline` method)

Within `$var[name]` specifically, the lookup order is:

1. Temporary variables set with `$var[name; value]`
2. Built-in read-only variables (`$authorID`, `$channelName`, etc.)

> **Persistent variables** (`$setVar`) are **only** accessible via `$getVar[name]` — not through `$var`.
> **Return variables** are **only** accessible via `$return[name]` — populated by `$returnXxx` commands.

---

## Error System

FDScript validates the **entire script** before execution. If any error is found, **nothing runs** and all errors are reported together.

| Icon | Category | Common Causes |
|------|----------|---------------|
| 🔴 | **Syntax Error** | Unknown command, unclosed bracket, mismatched block |
| 🟠 | **Logic Error** | Wrong argument count, invalid operator, `$break` outside loop, `$log` with no channel ID |
| 🟡 | **Runtime Error** | Division by zero, non-numeric argument, `$for` count not an integer |
| 🔵 | **Environment Error** | Channel/guild not found, bot lacks permission, DM user not found |

When a runtime or environment error occurs during execution, the error is sent to the channel and the script stops immediately.

**Example:**
```
$wew[now]
```
```
🔴 Syntax Error — Line 1: Unknown command `wew`
```

**Multiple errors example:**
```
$if[x > 5]
$sendMessage[Hello]
```
```
2 errors found, aborted:
🔴 Syntax Error — Line 1: `$if` not closed with `$endif`
```

---

## `$var` — Temporary Variables

Lives only for the current script execution. Gone when the script ends.

**Set:**
```
$var[name; value]
```

**Get (inline):**
```
$var[name]
```

**Example:**
```
$var[score; 10]
$sendMessage[Your score is $var[score]]
```
```
Your score is 10
```

**Using in conditions:**
```
$var[count; 5]
$if[$var[count] >= 5]
$var[label; high]
$else
$var[label; low]
$endif
$sendMessage[Count is $var[label]]
```

> `$var` is part of the inline resolver — it can be nested inside any command's arguments. Variables are stored in `temp_vars` and survive for the entire script execution including inside loops and conditional blocks.

---

## `$setVar` / `$getVar` — Persistent Variables

Saved to disk as `.json` files. Survive across script executions and bot restarts.

Variable names are sanitized to alphanumeric characters, `-`, and `_`.

---

### Global persistent variables

Shared across all users.

**Write:**
```
$setVar[name; value]
```

**Read (inline only):**
```
$getVar[name]
```

Storage location: `bot_vars/<name>.json`

**Example:**
```
$setVar[visits; 42]
$sendMessage[Total visits: $getVar[visits]]
```
```
Total visits: 42
```

---

### Per-user persistent variables

Each user gets their own value, keyed by their Discord ID.

**Write:**
```
$setVar[name; value; userID]
```

**Read (inline only):**
```
$getVar[name; userID]
```

Storage location: `bot_ids/ids_data.json` (all users in a single file, structured as `{name: {userID: value}}`)

**Example — per-user score tracker:**
```
$var[current; $getVar[score; $authorID]]
$var[current; $sum[$var[current]; 1]]
$setVar[score; $var[current]; $authorID]
$sendMessage[$authorName, your score is now $var[current].]
```

> You can use `$authorID` or any resolved ID string as the `userID` argument.

---

## Built-in Variables

Read-only. Resolved at runtime. Use them inline anywhere.

| Variable | Value |
|----------|-------|
| `$authorID` | Numeric ID of the message author |
| `$authorName` | Username of the message author |
| `$mention` | Mention string of the author (`<@id>`) |
| `$channelID` | Numeric ID of the current channel |
| `$channelName` | Name of the current channel |
| `$guildID` | Numeric ID of the current server |
| `$guildName` | Name of the current server (`DM` in DMs) |
| `$membersCount` | Total member count of the current server |
| `$message` | All text after the command trigger |
| `$message[n]` | The nth word after the command trigger (1-based) |
| `$messageID` | Numeric ID of the triggering message |
| `$botName` | Username of the bot |
| `$botID` | Numeric ID of the bot |
| `$ping` | Bot's WebSocket latency (e.g. `42ms`) |
| `$uptime` | Time since bot started (`Xd Xh Xm Xs`) |
| `$addTimestamp` | Discord timestamp for now (default `T` format) |
| `$randomUserID` | ID of a random non-bot member in the server |

### `$message[n]` — Word indexing

```
# User types: !cmd hello world
$sendMessage[$message[1]]   # → hello
$sendMessage[$message[2]]   # → world
$sendMessage[$message]      # → hello world
```

---

## `$sendMessage`

Sends a text message to the current channel (or DM target if `$dm` was used, or as a reply if `$reply` was used).

```
$sendMessage[text]
```

```
$sendMessage[Hello from the bot!]
$sendMessage[Your ID is $authorID]
```

---

## `$reply`

Makes all subsequent output in the script reply to the triggering message. Affects plain text, `$sendMessage`, `$image`, embeds, and all send commands.

```
$reply
$sendMessage[Here is your answer, $mention!]
```

> When the event type is `$alwaysReply`, replies are automatic — no need for `$reply`.

---

## `$dm`

Redirects all subsequent output to a DM channel.

**DM the command author:**
```
$dm
```

**DM a specific user:**
```
$dm[userID]
$dm[<@userID>]
```

```
$dm
$sendMessage[This goes to your DMs, $authorName!]
```

> `$dm[]` with an empty argument is a 🟠 Logic Error caught at validation.

---

## `$image`

Sends an image as a Discord embed (image-only). URL must be a direct link starting with `http://` or `https://`.

```
$image[url]
$image[$var[myImageUrl]]    ← inline usage
```

```
$image[https://example.com/photo.png]
```

> Google Photos share links and similar redirect URLs will **not** display. Use direct image URLs only.

---

## Embed Builder

Build embeds by setting fields individually. The embed is sent automatically at the end of execution — only if at least one field is set.

```
$title[text]
$description[text]
$color[hex or name]
$footer[text]
```

All four fields are optional. You can set them in any order.

**Example:**
```
$title[Server Update]
$description[Maintenance starts at 10 PM.]
$color[orange]
$footer[Posted by the admin team]
```

> The embed is flushed after all commands finish. If `$reply` was active, the embed is also sent as a reply.

---

## `$sendEmbedMessage`

Sends a full embed to a **specific channel by ID**. All 5 arguments are required.

```
$sendEmbedMessage[channelID; title; description; color; footer]
```

```
$sendEmbedMessage[123456789012345678; Announcement; The vote is now open.; blurple; FDBot]
```

---

## `$ban`

Bans a user from the server. Requires `Ban Members` permission.

```
$ban                    ← bans the message author
$ban[userID]
$ban[<@userID>]
$ban[$message[1]]       ← ban first word of user input
```

---

## `$kick`

Kicks a user from the server. Requires `Kick Members` permission.

```
$kick
$kick[userID]
$kick[<@userID>]
```

---

## `$unban`

Unbans a user by ID. Requires `Ban Members` permission.

```
$unban[userID]
```

---

## `$timeout` / `$untimeout`

**Timeout** puts a user in mute for a duration. **Untimeout** removes it. Both require `Moderate Members` permission.

```
$timeout[userID or mention; duration]
$untimeout[userID or mention]
```

Duration format: number + unit (`s` `m` `h` `d`)

```
$timeout[$message[1]; 10m]
$untimeout[$authorID]
```

---

## `$slowmode`

Sets the slowmode interval for the current channel. Requires `Manage Channels` permission. Use `0` to disable.

```
$slowmode[seconds]
```

```
$slowmode[5]
$slowmode[0]    ← disable slowmode
```

---

## `$deletecommand`

Deletes the message that triggered the command. Requires `Manage Messages` permission.

```
$deletecommand
```

If the bot lacks permission, a 🔵 Environment Error is sent and execution continues.

---

## `$clear`

Bulk-deletes messages from the current channel. Requires `Manage Messages` permission.

```
$clear           ← deletes last 10 (default)
$clear[count]    ← max 100
```

```
$clear[25]
```

---

## `$onlyAdmin`

Restricts execution to users with the `Administrator` permission. Script stops immediately if the user is not an admin.

```
$onlyAdmin
$onlyAdmin[error message]
```

```
$onlyAdmin[❌ You need Administrator permission to use this.]
$sendMessage[Admin command executed.]
```

---

## `$onlyIf`

Stops execution if the given condition is false. Optionally sends an error message.

```
$onlyIf[condition]
$onlyIf[condition; error message]
```

**Supported operators:** `==` `!=` `>` `<` `>=` `<=`

```
$onlyIf[$authorID == 123456789; ❌ Only the bot owner can use this.]
$sendMessage[Owner command executed.]
```

Supports `$and` and `$or` inside the condition:

```
$onlyIf[$or[$authorID == 111; $authorID == 222]; ❌ Not allowed.]
```

---

## `$strictArgs`

Validates the number of words the user passed after the command trigger. If the condition fails, the error message is sent and execution **continues**.

```
$strictArgs[comparison; error text]
```

Supported operators: `>` `<` `=` `>=` `<=` `!=`

```
$strictArgs[>0; Please provide a username.]
$strictArgs[=2; Please provide exactly two words.]
```

---

## `$cooldown`

Limits how often a user can trigger a script. If triggered again before the cooldown expires, the error message is sent and execution stops.

```
$cooldown[duration; error message]
```

| Unit | Meaning |
|------|---------|
| `s` | Seconds |
| `m` | Minutes |
| `h` | Hours |
| `d` | Days |

Use `{time}` or `%time%` in the error message to show remaining seconds.

```
$cooldown[30s; ⏳ Please wait {time} before using this again!]
$sendMessage[Command executed!]
```

---

## Math Commands

All five math commands accept exactly two numeric arguments. They work standalone (result sent to channel) **or** inline inside other arguments.

```
$sum[a; b]    ← addition
$sub[a; b]    ← subtraction
$mul[a; b]    ← multiplication
$div[a; b]    ← division
$mod[a; b]    ← modulo (remainder)
```

- Division by zero → 🟡 Runtime Error (script aborts).
- Non-numeric arguments → 🟠 Logic Error (script aborts).
- Integer results display without a decimal point (e.g. `10` not `10.0`).

**Standalone:**
```
$sum[8; 3]
```
```
11
```

**Inline:**
```
$var[x; 8]
$var[y; 3]
$sendMessage[Result: $sum[$var[x]; $var[y]]]
```
```
Result: 11
```

---

## `$randomint`

Returns a random integer between `min` and `max` (inclusive). If `min > max`, they are swapped automatically.

```
$randomint[min; max]
```

```
$sendMessage[Your lucky number: $randomint[1; 100]]
```

---

## `$randomstr`

Picks one item at random from a list of strings.

```
$randomstr[option1; option2; option3; ...]
```

```
$randomstr[rock; paper; scissors]
```

---

## `$randomUserID`

Picks a random non-bot member from the current server and returns their numeric ID. Only works inside a server (not in DMs).

```
$randomUserID
$sendMessage[Random member: $randomUserID]
```

---

## `$replaceText`

Replaces all occurrences of a substring within a string. Inline-capable.

```
$replaceText[text; search; replacement]
```

```
$sendMessage[$replaceText[hello world; world; FDScript]]
```
```
hello FDScript
```

```
$var[clean; $replaceText[$message; badword; ***]]
$sendMessage[$var[clean]]
```

---

## Conditions: `$if` / `$elif` / `$else` / `$endif`

Evaluates a condition and executes the matching branch.

```
$if[condition]
  ...
$elif[condition]
  ...
$else
  ...
$endif
```

**Supported operators:** `==` `!=` `>` `<` `>=` `<=`

- If both sides are numeric strings → compared numerically
- Otherwise → lexicographic comparison (only `==` and `!=` produce meaningful results)
- `true` / `false` literals are also accepted

**Example:**
```
$var[score; 75]
$if[$var[score] >= 90]
$sendMessage[Grade: A]
$elif[$var[score] >= 60]
$sendMessage[Grade: B]
$else
$sendMessage[Grade: F]
$endif
```
```
Grade: B
```

Multiple `$elif` branches are supported. Only the first matching branch executes.

---

## Compound Conditions: `$and` / `$or`

Combine multiple conditions inside `$if`, `$elif`, or `$onlyIf`. Cannot be used as standalone commands.

```
$if[$and[condition1; condition2; ...]]
$if[$or[condition1; condition2; ...]]
```

- `$and` → **all** conditions must be true
- `$or` → **at least one** must be true

Nesting is supported:

```
$if[$or[$and[cond1; cond2]; cond3]]
```

**Example:**
```
$var[age; 20]
$var[score; 85]
$if[$and[$var[age] >= 18; $var[score] >= 80]]
$sendMessage[Eligible!]
$else
$sendMessage[Not eligible.]
$endif
```
```
Eligible!
```

---

## `$while` / `$endwhile`

Repeats a block as long as a condition is true.

```
$while[condition]
  ...
$endwhile
```

**Example:**
```
$var[n; 1]
$while[$var[n] <= 3]
$sendMessage[Iteration $var[n]]
$var[n; $sum[$var[n]; 1]]
$endwhile
```
```
Iteration 1
Iteration 2
Iteration 3
```

---

## `$for` / `$endfor`

Repeats a block a fixed number of times. The count must be a whole number; floats are truncated. The count can be a variable or inline expression.

```
$for[count]
  ...
$endfor
```

**Example:**
```
$for[3]
$sendMessage[Hello!]
$endfor
```
```
Hello!
Hello!
Hello!
```

**Dynamic count:**
```
$var[times; 5]
$for[$var[times]]
$sendMessage[Ping!]
$endfor
```

---

## `$break`

Exits the nearest enclosing `$while` or `$for` loop immediately. Using `$break` outside a loop is a 🟠 Logic Error caught at validation.

```
$break
```

**Example:**
```
$var[n; 0]
$while[$var[n] < 10]
$var[n; $sum[$var[n]; 1]]
$if[$var[n] == 4]
$break
$endif
$endwhile
$sendMessage[Stopped at $var[n]]
```
```
Stopped at 4
```

---

## `$wait`

Pauses script execution for a specified duration, then resumes from where it stopped.

```
$wait[duration]
```

Duration format: integer + unit (`s` `m` `h` `d`)

| Unit | Meaning |
|------|---------|
| `s` | Seconds |
| `m` | Minutes |
| `h` | Hours |
| `d` | Days |

**Example:**
```
$sendMessage[Starting process...]
$wait[5s]
$sendMessage[Done! 5 seconds later.]
```

> Unlike `$replyIn`, this **halts the entire script** for the specified time. Use it when the order of operations matters.

---

## `$replyIn`

Delays only the bot's reply message — the rest of the script continues executing normally in the background.

```
$replyIn[duration]
```

Duration format: integer + unit (`s` `m` `h` `d`) — same units as `$wait`.

**Example:**
```
$replyIn[10s]
$sendMessage[This message will appear 10 seconds later.]
```

> **Note:** Maximum delay is 40 light-years. We recommend staying under that.

---

## `$ping`

Sends the bot's current WebSocket latency in milliseconds. Can be used inline.

```
$ping
$sendMessage[Current latency: $ping]
```
```
Current latency: 42ms
```

---

## `$uptime`

Sends the time elapsed since the bot started, formatted as `Xd Xh Xm Xs`. Units are omitted if zero (e.g. `4h 12m 7s` with no days component). Can be used inline.

```
$uptime
$sendMessage[Bot has been running for $uptime]
```
```
Bot has been running for 2d 4h 12m 7s
```

---

## `$addTimestamp`

Sends a Discord timestamp for the current time. Two usages:

**Bare (default `T` format) — inline variable:**
```
$addTimestamp
$sendMessage[Command run at: $addTimestamp]
```

**With format code — standalone command:**
```
$addTimestamp[format]
```

| Code | Display |
|------|---------|
| `t` | Short time: `4:20 PM` |
| `T` | Long time: `4:20:00 PM` |
| `d` | Short date: `04/20/2025` |
| `D` | Long date: `April 20, 2025` |
| `f` | Short date/time: `April 20, 2025 4:20 PM` |
| `F` | Long date/time: `Sunday, April 20, 2025 4:20 PM` |
| `R` | Relative: `2 hours ago` |

```
$sendMessage[Event starts: $addTimestamp[R]]
$addTimestamp[D]
```

An invalid format code produces a 🟠 Logic Error.

---

## `$getBotInvent`

Sends the bot's OAuth2 invite link (with Administrator permissions).

```
$getBotInvent
$sendMessage[Invite the bot: $getBotInvent]
```

---

## `$clientTyping`

Shows a "Bot is typing…" indicator in the current channel while the script runs. Automatically stopped when any message is sent.

```
$clientTyping
```

Useful before long operations to indicate the bot is working.

---

## `$log`

Takes a snapshot of the internal execution log and sends it to a specified channel after the script finishes. Useful for auditing and debugging.

```
$log[channelID]
$log[channelID; name_code]
```

- `name_code` — optional label shown in the log header
- Each `$log` call captures events since the **previous** `$log` call (or since script start for the first call)
- Multiple `$log` calls per script are allowed, each a separate snapshot
- Short logs (≤2000 chars) → code block; long logs → `.txt` file attachment (max 10 MB)
- `$log` without a channel ID is a 🟠 Logic Error caught at validation

```
$sendMessage[Command executed.]
$log[987654321098765432; admin-audit]
```

---

## `$addUserReactions`

Adds emoji reactions to the **user's** triggering message. Max **20** emojis per call.

```
$addUserReactions[emoji1; emoji2; ...]
```

```
$addUserReactions[👍; ❤️; <:custom:123456789>]
```

Supports Unicode emojis, custom server emojis (`<:name:id>`), and animated emojis (`<a:name:id>`). ZWJ sequences (e.g. family emojis) are handled correctly.

---

## `$addBotReactions`

Adds emoji reactions to the **last bot message** sent in this execution. Must be called after at least one bot message has been sent. Max **20** emojis per call.

```
$addBotReactions[emoji1; emoji2; ...]
```

```
$sendMessage[Cast your vote!]
$addBotReactions[👍; 👎]
```

---

## `$return`

Reads a value stored by a `$returnXxx` command. **Inline-only** — not a standalone command.

```
$return[varName]
```

The variable must have been populated by one of the return commands below. Returns an empty string if the variable doesn't exist.

---

## `$returnGuildUsersID`

Fetches the IDs of all non-bot members in a server and stores them in a return variable.

```
$returnGuildUsersID[guildID; fetchMode; var; separator]
```

| Argument | Description |
|----------|-------------|
| `guildID` | Numeric ID of the server |
| `fetchMode` | `cache` or `chunk` |
| `var` | Name of the return variable |
| `separator` | Character or [named separator](#separators) |

> **`fetchMode` guidance:**
> - `cache` — uses cached members. Safe for servers up to ~50k–100k users.
> - `chunk` — fetches all members from Discord directly. Avoid on servers with 5k–10k+ users; can cause significant delays or rate limiting.

```
$returnGuildUsersID[$guildID; cache; members; com]
$sendMessage[Member IDs: $return[members]]
```

---

## `$returnGuildChannelsID`

Fetches channel IDs filtered by type and stores them in a return variable.

```
$returnGuildChannelsID[guildID; channelType; var; separator]
```

| `channelType` | Matches |
|---------------|---------|
| `text` | Text channels |
| `voice` | Voice channels |
| `category` | Category channels |
| `forum` | Forum channels |
| `stage` | Stage channels |
| `all` | All channel types |

```
$returnGuildChannelsID[$guildID; text; channels; com]
$sendMessage[Text channel IDs: $return[channels]]
```

---

## `$returnGuildRolesID`

Fetches role IDs, optionally filtered by permission. `@everyone` is always excluded.

```
$returnGuildRolesID[guildID; permission; var; separator]
```

Leave `permission` empty or use `all` for all roles. Accepts named permissions or raw numeric permission integers.

**Supported named permissions:**

`admin`, `manage_guild`, `manage_roles`, `manage_channels`, `manage_messages`, `manage_webhooks`, `manage_nicknames`, `manage_emojis`, `manage_threads`, `manage_events`, `kick_members`, `ban_members`, `moderate_members`, `mention_everyone`, `send_messages`, `send_tts_messages`, `embed_links`, `attach_files`, `read_message_history`, `use_external_emojis`, `use_external_stickers`, `add_reactions`, `connect`, `speak`, `mute_members`, `deafen_members`, `move_members`, `use_voice_activation`, `priority_speaker`, `stream`, `view_channel`, `view_audit_log`, `view_guild_insights`, `change_nickname`, `create_instant_invite`, `request_to_speak`, `use_application_commands`, `use_embedded_activities`

```
$returnGuildRolesID[$guildID; admin; adminRoles; com]
$sendMessage[Admin role IDs: $return[adminRoles]]
```

```
$returnGuildRolesID[$guildID; all; allRoles; dot]
$returnGuildRolesID[$guildID; ; allRoles; dot]   ← empty = all
```

---

## `$returnGetReactions`

Fetches reaction data from a specific message and stores it in a return variable.

```
$returnGetReactions[channelID; messageID; type; var; separator; emoji]
```

| Argument | Description |
|----------|-------------|
| `channelID` | Channel containing the message |
| `messageID` | Target message ID |
| `type` | `usersID` → list of reactor IDs; `tr` → total reaction count |
| `var` | Name of the return variable |
| `separator` | Separator (used with `usersID`) |
| `emoji` | Unicode emoji or custom emoji (`<:name:id>`) |

With `type = tr`: if the emoji wasn't on the message, result is `0`.

> **Note:** For messages with 5k+ reactions, behavior may be unpredictable. Still being refined for very large reaction counts.

```
$returnGetReactions[$channelID; $messageID; tr; voteCount; com; 👍]
$sendMessage[Total 👍 votes: $return[voteCount]]
```

```
$returnGetReactions[$channelID; $messageID; usersID; voters; com; 👍]
$sendMessage[Voters: $return[voters]]
```

---

## Events

Event scripts are triggered automatically by Discord events rather than user commands. They use a special first-line syntax to declare their type and target channel.

**First-line format:**
```
#PREFIX:$eventName[channelID]
```

The `channelID` in the first line tells the bot where to send any messages produced by the script. The rest of the file is a normal FDScript.

Event scripts live in the `bot_events/` directory, while command scripts live in `bot_commands/`.

---

## `$onJoined`

Triggered when a new member joins the server.

**First line:**
```
#PREFIX:$onJoined[channelID]
```

**Available variables:**

| Variable | Value |
|----------|-------|
| `$authorID` | ID of the member who joined |
| `$authorName` | Username of the member who joined |
| `$mention` | Mention string of the member (`<@id>`) |
| `$channelID` | ID of the target channel (from the first line) |
| `$channelName` | Name of the target channel |
| `$guildID` | Numeric ID of the server |
| `$guildName` | Name of the server |
| `$botID` | Numeric ID of the bot |
| `$botName` | Username of the bot |

> `$message` and `$messageID` are **not available** — there is no triggering message in this event.

**Example:**
```
#PREFIX:$onJoined[123456789012345678]
$sendMessage[Welcome to the server, $mention! 🎉]
```

---

## `$onLeave`

Triggered when a member leaves or is removed from the server.

**First line:**
```
#PREFIX:$onLeave[channelID]
```

**Available variables:** Same as [`$onJoined`](#onjoined) — the member data refers to the user who left.

> `$message` and `$messageID` are **not available**.

**Example:**
```
#PREFIX:$onLeave[123456789012345678]
$sendMessage[**$authorName** has left the server. 👋]
```

---

## `$alwaysReply`

Triggered on **every message** sent in the server (by non-bot users). Unlike command scripts, there is no trigger prefix — the script runs for all messages.

All output is automatically sent as a **reply** to the triggering message. No need for `$reply`.

**First line:**
```
#PREFIX:$alwaysReply
```

> No channel ID on the first line — the bot replies directly in the channel where the message was sent.

**Available variables:** All standard built-in variables are available.

> **`$message` behavior:** Returns the **full message content** — not just text after a trigger, since there is no trigger prefix in this event.

**Example:**
```
#PREFIX:$alwaysReply
$if[$message == hello]
$sendMessage[Hello there, $mention! 👋]
$endif
```

> **Warning:** This event fires on every single message in the server. Use conditions carefully to avoid the bot responding to everything. Consider using `$onlyIf` or `$if` guards.

---

## Separators

Commands that return lists accept a `separator` argument. Pass a literal character or a named alias.

| Name | Character |
|------|-----------|
| `dot` | `.` |
| `com` | `,` |
| `apo` | `'` |
| `sem` | `;` |
| `colon` | `:` |

> **Important:** You can **never** pass `;` directly as a separator — it's the argument delimiter. Use `sem` instead.

Any unlisted string is passed through as a literal separator (e.g. `|`, ` `, `--`).

---

## Color Names

Used with `$color[name]` in the embed builder.

| Name | Hex | Name | Hex |
|------|-----|------|-----|
| `red` | `#E74C3C` | `green` | `#2ECC71` |
| `blue` | `#3498DB` | `yellow` | `#F1C40F` |
| `orange` | `#E67E22` | `purple` | `#9B59B6` |
| `pink` | `#FF69B4` | `white` | `#FFFFFF` |
| `black` | `#000000` | `gray` / `grey` | `#95A5A6` |
| `cyan` | `#1ABC9C` | `gold` | `#F9A825` |
| `navy` | `#2C3E50` | `lime` | `#27AE60` |
| `brown` | `#A0522D` | `teal` | `#008080` |
| `magenta` | `#FF00FF` | `blurple` | `#5865F2` |
| `dark` | `#2B2D31` | | |

Hex values can also be passed directly: `$color[#FF5733]` or `$color[FF5733]`.
Unrecognized values fall back to `dark` (`#2B2D31`).

---

## Full Examples

### Server info embed
```
$color[blurple]
$title[📊 Server Info]
$description[**Name:** $guildName
**ID:** $guildID
**Members:** $membersCount
**Channel:** $channelName]
$footer[Requested by $authorName]
```

---

### Global persistent hit counter
```
$var[count; $getVar[hits]]
$var[count; $sum[$var[count]; 1]]
$setVar[hits; $var[count]]
$sendMessage[$authorName, you have used this command $var[count] times.]
```
*Output on the 3rd call:*
```
user, you have used this command 3 times.
```

---

### Per-user score tracker
```
$var[score; $getVar[points; $authorID]]
$var[score; $sum[$var[score]; 10]]
$setVar[points; $var[score]; $authorID]
$sendMessage[$mention, your total points: $var[score]]
```

---

### Multiline message with escape sequences
```
$sendMessage[**Server Rules**\n\n1. Be respectful.\n2. No spam.\n3. Read the FAQ.]
```
```
**Server Rules**

1. Be respectful.
2. No spam.
3. Read the FAQ.
```

---

### Cooldown command
```
$cooldown[30s; ⏳ Wait {time} before using this again!]
$sendMessage[Command executed!]
```

---

### Simple guessing game
```
$strictArgs[>0; Please provide a number.]
$var[guess; $message]
$var[answer; 7]
$if[$var[guess] == $var[answer]]
$sendMessage[Correct!]
$else
$sendMessage[Wrong, try again.]
$endif
```

---

### Reply to user
```
$reply
$sendMessage[Here is your answer, $mention!]
```

---

### DM a specific user
```
$dm[123456789012345678]
$sendMessage[Hello! You've been selected for a giveaway.]
```

---

### Reaction vote
```
$sendMessage[Vote now! 👍 for yes, 👎 for no.]
$addBotReactions[👍; 👎]
```

---

### Bot invite link
```
$sendMessage[Add the bot: $getBotInvent]
```

---

### Audit log snapshot
```
$sendMessage[Command executed.]
$log[987654321098765432; command-audit]
```

---

### Random role picker
```
$randomstr[Warrior; Mage; Rogue; Healer]
```

---

### Welcome message on join
```
#PREFIX:$onJoined[123456789012345678]
$sendMessage[Welcome $mention! You are member number $membersCount. 🎉]
```

---

### Auto-reply to greetings
```
#PREFIX:$alwaysReply
$if[$or[$message == hello; $message == hi; $message == hey]]
$sendMessage[Hey $mention! 👋]
$endif
```

---

### Compound condition with $and
```
$var[age; 20]
$var[score; 85]
$if[$and[$var[age] >= 18; $var[score] >= 80]]
$sendMessage[Eligible!]
$else
$sendMessage[Not eligible.]
$endif
```

---

### While loop with break
```
$var[n; 0]
$while[$var[n] < 10]
$var[n; $sum[$var[n]; 1]]
$if[$var[n] == 4]
$break
$endif
$endwhile
$sendMessage[Stopped at $var[n]]
```
```
Stopped at 4
```

---

### Fetch all admin roles
```
$returnGuildRolesID[$guildID; admin; adminRoles; com]
$sendMessage[Admin role IDs: $return[adminRoles]]
```

---

### Count votes on a message
```
$returnGetReactions[$channelID; $messageID; tr; voteCount; com; 👍]
$sendMessage[Total 👍 votes: $return[voteCount]]
```

---

*FDScript is part of [BCFD-L](https://github.com/obgwew/BCFD-L) — licensed under AGPLv3.*
