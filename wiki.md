# FDScript Wiki

> A lightweight scripting language for Discord bots — built into **BCFD-L**.
> Scripts run line-by-line; commands start with `$` and take arguments inside `[]` separated by `;`.

---

## 📑 Table of Contents

### Core
- [Syntax Rules](#syntax-rules)
- [Plain Text Lines](#plain-text-lines)
- [Inline Comments](#inline-comments)
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
| Whitespace is ignored | Around tokens |
| `#` starts a comment | Whole line or inline (outside brackets) |
| No `$` prefix → plain text | Sent verbatim to the channel (built-ins resolved first) |
| Unclosed `[` | → Syntax Error |
| Extra `]` | → Syntax Error |
| **Pre-execution validation** | All errors are found and reported before anything runs |

> **Important:** Commands that start with `$` are always treated as commands, regardless of what they do — they can be a mix of functions, variables, and state changes.

---

## Plain Text Lines

Any line that does **not** start with `$` is sent directly to the channel. Built-in variables and inline commands are resolved inside it before sending.

```
Welcome, $authorName!
Your channel is #$channelName.
```

**Output:**
```
Welcome, user!
Your channel is #general.
```

---

## Inline Comments

Comments can appear at the end of any line, outside brackets. Everything after a bare `#` at bracket depth 0 is ignored.

```
$var[score; 100]        # set initial score
$sendMessage[$var[score]]  # send it
```

---

## Variable Resolution Order

When `$var[name]` is encountered, the interpreter resolves in this order:

1. Temporary variables set with `$var[name; value]`
2. Built-in read-only variables (`$authorID`, `$channelName`, etc.)

> Persistent variables (`$setVar`) are **only** accessible via `$getVar[name]` — not through `$var`.
> Return variables are **only** accessible via `$return[name]` — populated by `$returnXxx` commands.

---

## Error System

FDScript validates the **entire script** before execution. If any error is found, **nothing runs** and all errors are reported.

| Icon | Category | Common Causes |
|------|----------|---------------|
| 🔴 | **Syntax Error** | Unknown command, unclosed bracket, mismatched block |
| 🟠 | **Logic Error** | Wrong argument count, invalid operator, `$break` outside loop |
| 🟡 | **Runtime Error** | Division by zero, non-numeric argument, `$for` count not an integer |
| 🔵 | **Environment Error** | Channel/guild not found, bot lacks permission, DM user not found |

**Example:**
```
$wew[now]
```
```
🔴 Syntax Error — Line 1: Unknown command `wew`
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

---

## `$setVar` / `$getVar` — Persistent Variables

Saved to disk as `.json` files. Survive across script executions.

```
$setVar[name; value]
$getVar[name]          ← inline only, not standalone
```

Variable names are sanitized to alphanumeric, `-`, and `_`.

**Example:**
```
$setVar[visits; 42]
$sendMessage[Total visits: $getVar[visits]]
```
```
Total visits: 42
```

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
| `$randomUserID` | ID of a random non-bot member |

### `$message[n]` — Word indexing

```
# User types: !cmd hello world
$sendMessage[$message[1]]   # → hello
$sendMessage[$message[2]]   # → world
$sendMessage[$message]      # → hello world
```

---

## `$sendMessage`

Sends a text message to the current channel (or DM target if `$dm` was used).

```
$sendMessage[text]
```

```
$sendMessage[Hello from the bot!]
```

---

## `$reply`

Makes all subsequent output in the script reply to the triggering message. Affects plain text, `$sendMessage`, `$image`, embeds, and all send commands.

```
$reply
$sendMessage[Here is your answer, $mention!]
```

> You can put `$reply` Anywhere in the message and it will work automatically regardless of its location.

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

All four fields are optional.

**Example:**
```
$title[Server Update]
$description[Maintenance starts at 10 PM.]
$color[orange]
$footer[Posted by the admin team]
```

### Color Names

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

Unrecognized colors fall back to `dark` (`#2B2D31`).

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
```

---

## `$slowmode`

Sets the slowmode interval for the current channel. Requires `Manage Channels` permission. Use `0` to disable.

```
$slowmode[seconds]
```

```
$slowmode[5]
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

```
$onlyIf[$authorID == 123456789; ❌ Only the bot owner can use this.]
$sendMessage[Owner command executed.]
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

Division by zero → 🟡 Runtime Error (no crash).
Integer results display without a decimal point.

**Standalone example:**
```
$var[x; 8]
$var[y; 3]
$sendMessage[$sum[$var[x]; $var[y]]]
```
```
11
```

**Inline example:**
```
$sendMessage[Result is $sum[8; 2]]
```
```
Result is 10
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

Replaces all occurrences of a substring within a string.

```
$replaceText[text; search; replacement]
```

```
$sendMessage[$replaceText[hello world; world; FDScript]]
```
```
hello FDScript
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

- Numeric strings → compared numerically
- Non-numeric strings → lexicographic (only `==` and `!=`)

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

---

## Compound Conditions: `$and` / `$or`

Combine multiple conditions inside `$if` or `$elif`. Cannot be used as standalone commands.

```
$if[$and[condition1; condition2; ...]]
$if[$or[condition1; condition2; ...]]
```

- `$and` → **all** conditions must be true
- `$or` → **at least one** must be true

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

Repeats a block a fixed number of times. The count must be a whole number; floats are truncated.

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

## `$ping`

Sends the bot's current WebSocket latency in milliseconds.

```
$ping
$sendMessage[Current latency: $ping]
```
```
Current latency: 42ms
```

---

## `$uptime`

Sends the time elapsed since the bot started, formatted as `Xd Xh Xm Xs`.

```
$uptime
$sendMessage[Bot has been running for $uptime]
```
```
Bot has been running for 2d 4h 12m 7s
```

---

## `$addTimestamp`

Sends a Discord timestamp for the current time.

```
$addTimestamp              ← standalone, default T format
$addTimestamp[format]      ← with format code
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
```

---

## `$getBotInvent`

Sends the bot's OAuth2 invite link (with Administrator permissions). Can be used inline.

```
$getBotInvent
$sendMessage[Invite the bot: $getBotInvent]
```

---

## `$clientTyping`

Shows a "Bot is typing…" indicator while the script runs. Automatically stopped when any message is sent.

```
$clientTyping
```

---

## `$log`

Takes a snapshot of the execution log and sends it to a specified channel after the script finishes. Useful for auditing.

```
$log[channelID]
$log[channelID; name_code]
```

- `name_code` — optional label shown in the log header
- Multiple `$log` calls each capture events since the previous call
- Short logs → code block; long logs (>2000 chars) → `.txt` file attachment (up to 10 MB)

```
$log[987654321098765432; admin-audit]
```

---

## `$addUserReactions`

Adds emoji reactions to the **user's** triggering message. Max **20** emojis.

```
$addUserReactions[emoji1; emoji2; ...]
```

```
$addUserReactions[👍; ❤️; <:custom:123456789>]
```

---

## `$addBotReactions`

Adds emoji reactions to the **last bot message** in this execution. Must be called after at least one bot message has been sent. Max **20** emojis.

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

The variable must have been populated by one of the return commands below.

---

## `$returnGuildUsersID`

Fetches the IDs of all non-bot members in a server and stores them in a return variable.

```
$returnGuildUsersID[guildID; fetchMode; var; separator]
```

| Argument | Description |
|----------|-------------|
| `guildID` | Numeric ID of the server |
| `fetchMode` | `cache` or `chunk` (see note below) |
| `var` | Name of the return variable |
| `separator` | Character or [named separator](#separators) |

> **`fetchMode` guidance:**
> - `cache` — uses cached members. Safe for servers up to ~50k–100k users.
> - `chunk` — fetches all members from Discord directly. Avoid on servers with 5k–10k+ users; can cause significant delays or bot bans.

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
| `all` | All types |

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

Leave `permission` empty or use `all` for all roles. Accepts named permissions or raw permission integers.

**Supported named permissions:** `admin`, `manage_guild`, `manage_roles`, `manage_channels`, `manage_messages`, `kick_members`, `ban_members`, `moderate_members`, `send_messages`, `view_channel`, `connect`, `speak`, and more.

```
$returnGuildRolesID[$guildID; admin; adminRoles; com]
$sendMessage[Admin role IDs: $return[adminRoles]]
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
| `type` | `usersID` → IDs of reactors; `tr` → total reaction count |
| `var` | Name of the return variable |
| `separator` | Separator (used with `usersID`) |
| `emoji` | Unicode or custom emoji (`<:name:id>`) |

With `type = tr`: if the emoji wasn't on the message, result is `0`.

> **Note:** For messages with 5k+ reactions, this command may behave unexpectedly. It's still being refined for very large reaction counts.

```
$returnGetReactions[$channelID; $messageID; tr; voteCount; com; 👍]
$sendMessage[Total 👍 votes: $return[voteCount]]
```

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

### Persistent hit counter
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
$log[112233445566778899; command-audit]
```

---

### Random role picker
```
$randomstr[Warrior; Mage; Rogue; Healer]
```

---

*FDScript is part of [BCFD-L](https://github.com/obgwew/BCFD-L) — licensed under GPL v3.*
