<<<<<<< HEAD
# FDScript

FDScript is a lightweight scripting language for Discord bots. Scripts are executed line by line; each command begins with `$` and takes arguments inside `[]` separated by `;`. Lines without a `$` prefix are sent as plain text to the channel.

---

## Syntax Rules

- Every command starts with `$`
- Arguments go inside `[]` and are separated by `;`
- Whitespace around tokens is ignored
- Lines starting with `#` are comments and are skipped
- Inline comments are also supported: anything after a bare `#` outside brackets is ignored
- A line with no `$` prefix is sent verbatim to the Discord channel (built-in variables are resolved first)
- An unclosed `[` causes a syntax error; an extra closing `]` also causes a syntax error
- The entire script is validated before any line executes — if any error is found, **all errors** are reported and nothing runs

> Notes: Commands that start with '$' are considered a command regardless of the function it performs, so most commands are a combination of functions, variables, and states. 

---

## Commands

### var

Declares or updates a temporary in-memory variable. Variables live only for the duration of the current script execution.

**Setter:**
```
$var[name; value]
```

**Getter (used inline):**
```
$var[name]
```

Example:
```
$var[score; 10]
$sendMessage[Your score is $var[score]]
```

Output:
```
Your score is 10
```

> **Variable resolution order:** When `$var[name]` is encountered, the interpreter checks (1) temporary variables set with `$var[name; value]`, then (2) built-in read-only variables. Persistent variables are only accessible via `$getVar[name]`.

---

### setVar / getVar

Stores and retrieves persistent variables saved to disk as JSON files. These values survive across script executions.

```
$setVar[name; value]
$getVar[name]
```

`$getVar[name]` is used inline inside arguments, not as a standalone command.

Variable names are sanitized to only alphanumeric characters, `-`, and `_` when saved. Each variable is stored as its own `.json` file.

Example:
```
$setVar[visits; 42]
$sendMessage[Total visits: $getVar[visits]]
```

Output:
```
Total visits: 42
```

---

### sendMessage

Sends a text message to the current channel (or to the DM target if `$dm` was used).

```
$sendMessage[text]
```

Example:
```
$sendMessage[Hello from the bot!]
```

Output:
```
Hello from the bot!
```

---

### Embed Builder

Embeds are built by setting fields individually, then they are automatically sent at the end of script execution.

```
$title[text]
$description[text]
$color[hex or name]
$footer[text]
```

All four fields are optional. The embed is only sent if at least one field has been set.

**Color** accepts either a hex string (`2ecc71` or `#2ecc71`) or one of the named colors below:

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

If the color value is unrecognized, it falls back to `dark` (`#2B2D31`).

Example:
```
$title[Server Update]
$description[Maintenance starts at 10 PM.]
$color[orange]
$footer[Posted by the admin team]
```

Output: A Discord embed with an orange sidebar, the given title, description, and footer.

---

### sendEmbedMessage

Sends a full embed to a **specific channel by ID**. Requires all 5 arguments.

```
$sendEmbedMessage[channelID; title; description; color; footer]
```

The footer is mandatory. Color accepts hex or named colors (same as `$color`).

Example:
```
$sendEmbedMessage[123456789012345678; Announcement; The vote is now open.; blurple; FDBot]
```

---

### strictArgs

Validates the number of words the user passed after the command trigger. If the condition is not met, the error message is sent and execution **continues** (it does not stop the script).

```
$strictArgs[comparison; error text]
```

The comparison checks the word count after the command name. Supported operators: `>` `<` `=` `>=` `<=` `!=`.

Examples:

```
# Require at least one word
$strictArgs[>0; Please provide a username.]
$sendMessage[Looking up: $message]
```

```
# Require exactly 2 words
$strictArgs[=2; Please provide exactly two words.]
```

> **Note:** In the original simple form `$strictArgs[; error text]`, passing an empty first argument is a logic error. Always provide a comparison expression.

---

### dm

Redirects all subsequent output (plain text and `$sendMessage`) to a DM channel instead of the current channel.

**DM the command author:**
```
$dm
```

**DM a specific user by ID or mention:**
```
$dm[userID]
$dm[<@userID>]
```

Once set, all output goes to that user's DMs for the rest of the script execution.

Example:
```
$dm
$sendMessage[This message goes to your DMs, $authorName!]
```

---

### deletecommand

Deletes the message that triggered the command. Requires the bot to have the `Manage Messages` permission in that channel.

```
$deletecommand
```

If the bot lacks permission, a `🔵 Environment Error` is sent and execution continues.

---

### clear

Bulk-deletes messages from the current channel. Requires the `Manage Messages` permission.

```
$clear
$clear[count]
```

With no argument, deletes the last **10** messages (default). The maximum is **100** (Discord's bulk-delete limit per request).

Example:
```
$clear[25]
```

---

### clientTyping

Shows a "Bot is typing…" indicator in the channel while the script runs. The indicator is automatically stopped when any message is sent.

```
$clientTyping
```

---

### ping

Sends the bot's current WebSocket latency in milliseconds to the channel. Can also be used inline.

```
$ping
```

Inline usage:
```
$sendMessage[Current latency: $ping]
```

Output:
```
Current latency: 42ms
```

---

### uptime

Sends the time elapsed since the bot started, formatted as `Xd Xh Xm Xs`. Can also be used inline.

```
$uptime
```

Inline usage:
```
$sendMessage[Bot has been running for $uptime]
```

Output:
```
Bot has been running for 2d 4h 12m 7s
```

---

### addTimestamp

Sends a Discord timestamp for the current time. When used as a standalone command it sends the timestamp. When used inline inside another argument, it returns the timestamp string.

**Standalone (default `T` format):**
```
$addTimestamp
```

**With a format code:**
```
$addTimestamp[format]
```

| Format | Display |
|--------|---------|
| `t` | Short time: `4:20 PM` |
| `T` | Long time: `4:20:00 PM` |
| `d` | Short date: `04/20/2025` |
| `D` | Long date: `April 20, 2025` |
| `f` | Short date/time: `April 20, 2025 4:20 PM` |
| `F` | Long date/time: `Sunday, April 20, 2025 4:20 PM` |
| `R` | Relative: `2 hours ago` |

Example:
```
$sendMessage[Event starts: $addTimestamp[R]]
```

---

### log

Takes a snapshot of the execution log up to that point and sends it to a specified channel after the script finishes. Useful for auditing command usage.

```
$log[channelID]
$log[channelID; name_code]
```

`name_code` is an optional label that appears in the log header. Multiple `$log` calls in the same script each capture events since the previous `$log` call.

If the log is short enough, it is sent as a code block. If it exceeds Discord's 2000-character limit, it is sent as a `.txt` file attachment (up to 10 MB).

Example:
```
$log[987654321098765432; admin-audit]
```

---

### addUserReactions

Adds emoji reactions to the **user's** triggering message. Accepts any combination of Unicode and custom Discord emojis. Maximum **20** emojis.

```
$addUserReactions[emoji1; emoji2; ...]
```

Example:
```
$addUserReactions[👍; ❤️; <:custom:123456789>]
```

---

### addBotReactions

Adds emoji reactions to the **last message sent by the bot** in this execution. Must be called after at least one bot message has been sent. Maximum **20** emojis.

```
$addBotReactions[emoji1; emoji2; ...]
```

Example:
```
$sendMessage[Cast your vote!]
$addBotReactions[👍; 👎]
```

---

## Built-in Variables

Read-only references resolved at runtime. Use them inline anywhere with `$name`.

| Variable | Value |
|---|---|
| `$authorID` | Numeric ID of the message author |
| `$authorName` | Username of the message author |
| `$mention` | Mention string of the message author (`<@id>`) |
| `$channelID` | Numeric ID of the current channel |
| `$channelName` | Name of the current channel |
| `$guildName` | Name of the current server (`DM` in direct messages) |
| `$message` | Text after the command trigger (empty if no argument was given) |
| `$messageID` | Numeric ID of the triggering message |
| `$botName` | Username of the bot |
| `$botID` | Numeric ID of the bot |
| `$ping` | Bot's current WebSocket latency in milliseconds (e.g. `42ms`) |
| `$uptime` | Time since bot started, formatted as `Xd Xh Xm Xs` |
| `$addTimestamp` | Discord timestamp for right now using the default `T` format |
| `$randomUserID` | ID of a random non-bot member of the current server |

Example:
```
$sendMessage[Hello $authorName, your ID is $authorID]
```

Output:
```
Hello user, your ID is 123456789012345678
```

---

## Math Commands

Each command takes exactly two numeric arguments. All five can be used as standalone commands (result sent to channel) or inline inside other arguments. Integer results are displayed without a decimal point; non-integer results keep their decimal.

```
$sum[a; b]
$sub[a; b]
$mul[a; b]
$div[a; b]
$mod[a; b]
```

Division by zero produces a `🟡 Runtime Error` instead of crashing.

Example:
```
$var[x; 8]
$var[y; 3]
$sum[$var[x]; $var[y]]
$sub[$var[x]; $var[y]]
$mul[$var[x]; $var[y]]
$div[$var[x]; $var[y]]
$mod[$var[x]; $var[y]]
```

Output:
```
11
5
24
2.6666666666666665
2
```

Inline usage:
```
$var[x; 8]
$sendMessage[Result is $sum[$var[x]; 2]]
```

Output:
```
Result is 10
```

---

## Random Commands

### randomint

Returns a random integer between `min` and `max` (inclusive). If `min > max`, they are automatically swapped. Can be used standalone or inline.

```
$randomint[min; max]
```

Example:
```
$sendMessage[Your lucky number: $randomint[1; 100]]
```

---

### randomstr

Picks one item at random from a list of strings. Can be used standalone or inline.

```
$randomstr[option1; option2; option3; ...]
```

Example:
```
$randomstr[rock; paper; scissors]
```

---

### randomUserID

Picks a random non-bot member from the current server and sends their numeric ID. Only works inside a server (not in DMs).

```
$randomUserID
```

Can also be used inline:
```
$sendMessage[Random member ID: $randomUserID]
```

---

## Conditions: if / elif / else / endif

Evaluates a condition and executes the matching branch. Supported operators: `==` `!=` `>` `<` `>=` `<=`.

Numeric strings are compared numerically; non-numeric strings fall back to lexicographic comparison. Only `==` and `!=` support string comparison — `>`, `<`, `>=`, `<=` require numeric values.

```
$if[condition]
  ...
$elif[condition]
  ...
$else
  ...
$endif
```

Example:
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

Output:
```
Grade: B
```

### Compound Conditions: $and / $or

Multiple conditions can be combined inside `$if` or `$elif` using `$and` or `$or`. These cannot be used as standalone commands.

```
$if[$and[condition1; condition2; ...]]
$if[$or[condition1; condition2; ...]]
```

`$and` requires **all** conditions to be true. `$or` requires **at least one** to be true.

Example:
```
$var[age; 20]
$var[score; 85]
$if[$and[$var[age] >= 18; $var[score] >= 80]]
$sendMessage[Eligible!]
$else
$sendMessage[Not eligible.]
$endif
```

Output:
```
Eligible!
```

---

## while / endwhile

Repeats a block as long as a condition is true.

```
$while[condition]
  ...
$endwhile
```

Example:
```
$var[n; 1]
$while[$var[n] <= 3]
$sendMessage[Iteration $var[n]]
$var[n; $sum[$var[n]; 1]]
$endwhile
```

Output:
```
Iteration 1
Iteration 2
Iteration 3
```

---

## for / endfor

Repeats a block a fixed number of times. The count must resolve to a whole number; floats are truncated to integers.

```
$for[count]
  ...
$endfor
```

Example:
```
$for[3]
$sendMessage[Hello!]
$endfor
```

Output:
```
Hello!
Hello!
Hello!
```

---

## break

Exits the nearest enclosing `$while` or `$for` loop immediately. Using `$break` outside a loop is a logic error caught at validation time.


```
$break
```

Example:
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

Output:
```
Stopped at 4
```

---

## return / returnXxx Commands

These commands store data into named **return variables** that can be retrieved inline with `$return[varName]`.

> Notes: Some of these commands are 'sensitive' and should only be used for very specific purposes. You are responsible for any use of these commands.

### return

Reads the value stored by a `$returnXxx` command.

```
$return[varName]
```

This is an inline-only command. The variable must have been populated by one of the `$returnXxx` commands below.

---

### returnGuildUsersID

Fetches the IDs of all non-bot members in a server and stores them in a return variable.

> Notes: It is preferable not to use 'chunk' if the server has more than 5k-10k and more users, as the bot's response may be delayed by several minutesb or bot Exposed to ban. Use 'cache' as long as the number of members on your server does not exceed 50k-100k users.

```
$returnGuildUsersID[guildID; fetchMode; var; separator]
```

| Argument | Description |
|---|---|
| `guildID` | Numeric ID of the server |
| `fetchMode` | `cache` (use cached members) or `chunk` (fetch all members from Discord) |
| `var` | Name of the return variable to store the result |
| `separator` | Character or named separator to join IDs (see [Separators](#separators)) |

Example:
```
$returnGuildUsersID[$guildID; cache; members; com]
$sendMessage[Member IDs: $return[members]]
```

---

### returnGuildChannelsID

Fetches the IDs of channels in a server filtered by type, and stores them in a return variable.

```
$returnGuildChannelsID[guildID; channelType; var; separator]
```

| `channelType` | Matches |
|---|---|
| `text` | Text channels |
| `voice` | Voice channels |
| `category` | Category channels |
| `forum` | Forum channels |
| `stage` | Stage channels |
| `all` | All channel types |

Example:
```
$returnGuildChannelsID[$guildID; text; channels; com]
$sendMessage[Text channel IDs: $return[channels]]
```

---

### returnGuildRolesID

Fetches the IDs of roles in a server, optionally filtered by a permission, and stores them in a return variable. The `@everyone` role is always excluded.

```
$returnGuildRolesID[guildID; permission; var; separator]
```

Leave `permission` empty or use `all` to get all roles. You can also pass a raw permission integer.

Supported named permissions include: `admin`, `manage_guild`, `manage_roles`, `manage_channels`, `manage_messages`, `kick_members`, `ban_members`, `moderate_members`, `send_messages`, `view_channel`, `connect`, `speak`, and many others. Use the error message when in doubt — it lists all valid names.

Example:
```
$returnGuildRolesID[$guildID; admin; adminRoles; com]
$sendMessage[Admin role IDs: $return[adminRoles]]
```

---

### returnGetReactions

Fetches reaction data from a specific message and stores it in a return variable.

> Notes: This is considered less sensitive, but it should be noted that if the number of reactions exceeds 5k or more, for example up to 100k, it is preferable not to use (the command still needs more maintenance and adjustment).

```
$returnGetReactions[channelID; messageID; type; var; separator; emoji]
```

| Argument | Description |
|---|---|
| `channelID` | Numeric ID of the channel containing the message |
| `messageID` | Numeric ID of the message |
| `type` | `usersID` (returns IDs of users who reacted) or `tr` (returns total reaction count) |
| `var` | Name of the return variable |
| `separator` | Separator for joining user IDs (only used with `usersID`) |
| `emoji` | The emoji to look up (Unicode or custom `<:name:id>`) |

With `type = tr`, if the emoji was not found on the message, the result is `0` (no error).

Example:
```
$returnGetReactions[$channelID; $messageID; tr; voteCount; com; 👍]
$sendMessage[Total 👍 votes: $return[voteCount]]
```

---

## Plain Text

Any line that does not start with `$` is sent directly to the channel. Built-in variables and inline commands are resolved before sending.

Example:
```
Welcome to the server, $authorName!
Your channel is #$channelName.
```

Output:
```
Welcome to the server, user!
Your channel is #general.
```

---

## Separators

Several commands that return lists of IDs accept a `separator` argument. You can pass a literal character or one of the named separator aliases:

| Name | Character |
|---|---|
| `dot` | `.` |
| `com` | `,` |
| `apo` | `'` |
| `sem` | `;` |
| `colon` | `:` |

> **Important:** Because `;` is the argument delimiter, you can **never** pass a semicolon directly as a separator. Use the name `sem` instead.

Example using `com`:
```
$returnGuildUsersID[$guildID; cache; ids; com]
```

---

## Inline Comments

Comments can appear at the end of any line, outside of brackets. Everything after a bare `#` at depth 0 is ignored.

```
$var[score; 100] # set initial score
$sendMessage[Score: $var[score]] # send it
```

---

## Error System

FDScript validates all commands before execution begins. If any error is found, **execution stops entirely** and all errors are reported to the channel. No partial execution occurs.

Errors are categorized by severity and shown with color-coded icons:

| Icon | Category | Common Causes |
|---|---|---|
| 🔴 | **Syntax Error** | Unknown command, unclosed bracket, mismatched block |
| 🟠 | **Logic Error** | Wrong argument count, invalid operator, `$break` outside loop, empty target in `$dm[]` |
| 🟡 | **Runtime Error** | Division by zero, non-numeric argument where number expected, `$for` count not an integer |
| 🔵 | **Environment Error** | Channel/guild not found, bot lacks permission, DM user not found |

Full error table:

| Error | Cause |
|---|---|
| Unknown command | A `$name` not in the recognized command list |
| Syntax error | An unclosed `[` or extra `]` |
| Wrong argument count | Passing the wrong number of arguments to a command |
| Non-numeric argument | Passing a string where a number is expected |
| Division by zero | Second argument to `$div` resolves to `0` |
| Unmatched block | `$endif` / `$endwhile` / `$endfor` without a matching opener, or vice versa |
| Mismatched block | `$endif` used where `$endwhile` was expected, etc. |
| `$break` outside loop | Using `$break` outside a `$while` or `$for` |
| `$and` / `$or` standalone | These can only be used inside a condition |

Example:
```
$wew[now]
```

Output:
```
🔴 Syntax Error — Line 1: Unknown command `wew`
```

---

## Full Examples

### Persistent hit counter

```
$var[count; $getVar[hits]]
$var[count; $sum[$var[count]; 1]]
$setVar[hits; $var[count]]
$sendMessage[$authorName, you have used this command $var[count] times.]
```

Output on the third call:
```
user, you have used this command 3 times.
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

### Random role picker

```
$randomstr[Warrior; Mage; Rogue; Healer]
```

---

### DM a specific user

```
$dm[123456789012345678]
$sendMessage[Hello! You've been selected for a giveaway.]
```

---

### Reaction vote collector

```
$sendMessage[Vote now! 👍 for yes, 👎 for no.]
$addBotReactions[👍; 👎]
```

---

### Announce to a specific channel with embed

```
$sendEmbedMessage[$channelID; Weekly Update; Check out the new changes this week!; blurple; FDBot Announcements]
```

---

### Audit log snapshot

```
$sendMessage[Command executed.]
$log[987654321098765432; command-audit]
```

---

## Variable Resolution Order

When `$var[name]` is encountered, the interpreter resolves it in this order:

1. Temporary in-memory variables set with `$var[name; value]`
2. Built-in read-only variables such as `$authorID` and `$channelName`

Persistent variables set with `$setVar` are accessed **only** via `$getVar[name]` and are not part of the above lookup chain.

`$return[name]` accesses an entirely separate store — the return variable map — populated only by `$returnXxx` commands.
=======
# FDScript

FDScript is a lightweight scripting language for Discord bots. Scripts are executed line by line; each command begins with `$` and takes arguments inside `[]` separated by `;`. Lines without a `$` prefix are sent as plain text to the channel.

---

## Syntax Rules

- Every command starts with `$`
- Arguments go inside `[]` and are separated by `;`
- Whitespace around tokens is ignored
- Lines starting with `#` are comments and are skipped
- Inline comments are also supported: anything after a bare `#` outside brackets is ignored
- A line with no `$` prefix is sent verbatim to the Discord channel (built-in variables are resolved first)
- An unclosed `[` causes a syntax error; an extra closing `]` also causes a syntax error
- The entire script is validated before any line executes — if any error is found, **all errors** are reported and nothing runs

---

## Commands

### var

Declares or updates a temporary in-memory variable. Variables live only for the duration of the current script execution.

**Setter:**
```
$var[name; value]
```

**Getter (used inline):**
```
$var[name]
```

Example:
```
$var[score; 10]
$sendMessage[Your score is $var[score]]
```

Output:
```
Your score is 10
```

> **Variable resolution order:** When `$var[name]` is encountered, the interpreter checks (1) temporary variables set with `$var[name; value]`, then (2) built-in read-only variables. Persistent variables are only accessible via `$getVar[name]`.

---

### setVar / getVar

Stores and retrieves persistent variables saved to disk as JSON files. These values survive across script executions.

```
$setVar[name; value]
$getVar[name]
```

`$getVar[name]` is used inline inside arguments, not as a standalone command.

Variable names are sanitized to only alphanumeric characters, `-`, and `_` when saved. Each variable is stored as its own `.json` file.

Example:
```
$setVar[visits; 42]
$sendMessage[Total visits: $getVar[visits]]
```

Output:
```
Total visits: 42
```

---

### sendMessage

Sends a text message to the current channel (or to the DM target if `$dm` was used).

```
$sendMessage[text]
```

Example:
```
$sendMessage[Hello from the bot!]
```

Output:
```
Hello from the bot!
```

---

### Embed Builder

Embeds are built by setting fields individually, then they are automatically sent at the end of script execution.

```
$title[text]
$description[text]
$color[hex or name]
$footer[text]
```

All four fields are optional. The embed is only sent if at least one field has been set.

**Color** accepts either a hex string (`2ecc71` or `#2ecc71`) or one of the named colors below:

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

If the color value is unrecognized, it falls back to `dark` (`#2B2D31`).

Example:
```
$title[Server Update]
$description[Maintenance starts at 10 PM.]
$color[orange]
$footer[Posted by the admin team]
```

Output: A Discord embed with an orange sidebar, the given title, description, and footer.

---

### sendEmbedMessage

Sends a full embed to a **specific channel by ID**. Requires all 5 arguments.

```
$sendEmbedMessage[channelID; title; description; color; footer]
```

The footer is mandatory. Color accepts hex or named colors (same as `$color`).

Example:
```
$sendEmbedMessage[123456789012345678; Announcement; The vote is now open.; blurple; FDBot]
```

---

### image

Sends an image as a Discord embed (image-only, no title or description). The URL must start with `http://` or `https://` and point directly to an image.

```
$image[url]
```

Can also be used inline inside other commands:
```
$image[$var[myImageUrl]]
```

Example:
```
$image[https://example.com/photo.png]
```

> **Note:** URLs that redirect to a webpage (e.g. Google Photos share links) will not display. Use direct image URLs only.

---

### reply

Makes all subsequent output in the script send as a Discord reply to the triggering message. Affects plain text lines, `$sendMessage`, `$image`, embeds, and all other send commands.

```
$reply
```

Example:
```
$reply
$sendMessage[Here is your answer!]
```

> When `$alwaysReply` is set as the event type for a script, replies are automatically enabled without needing `$reply`.

---

### dm

Redirects all subsequent output (plain text and `$sendMessage`) to a DM channel instead of the current channel.

**DM the command author:**
```
$dm
```

**DM a specific user by ID or mention:**
```
$dm[userID]
$dm[<@userID>]
```

Once set, all output goes to that user's DMs for the rest of the script execution.

Example:
```
$dm
$sendMessage[This message goes to your DMs, $authorName!]
```

---

### deletecommand

Deletes the message that triggered the command. Requires the bot to have the `Manage Messages` permission in that channel.

```
$deletecommand
```

If the bot lacks permission, a `🔵 Environment Error` is sent and execution continues.

---

### clear

Bulk-deletes messages from the current channel. Requires the `Manage Messages` permission.

```
$clear
$clear[count]
```

With no argument, deletes the last **10** messages (default). The maximum is **100** (Discord's bulk-delete limit per request).

Example:
```
$clear[25]
```

---

### cooldown

Limits how often a user can trigger a script. If the user runs it again before the cooldown expires, the error message is sent and execution stops.

```
$cooldown[duration; error message]
```

| Unit | Meaning |
|------|---------|
| `s` | Seconds |
| `m` | Minutes |
| `h` | Hours |
| `d` | Days |

Use `{time}` or `%time%` in the error message to show the remaining seconds.

Example:
```
$cooldown[30s; ⏳ Please wait {time} before using this again!]
$sendMessage[Command executed!]
```

---

### clientTyping

Shows a "Bot is typing…" indicator in the channel while the script runs. The indicator is automatically stopped when any message is sent.

```
$clientTyping
```

---

### strictArgs

Validates the number of words the user passed after the command trigger. If the condition is not met, the error message is sent and execution **continues** (it does not stop the script).

```
$strictArgs[comparison; error text]
```

The comparison checks the word count after the command name. Supported operators: `>` `<` `=` `>=` `<=` `!=`.

Examples:

```
# Require at least one word
$strictArgs[>0; Please provide a username.]
$sendMessage[Looking up: $message]
```

```
# Require exactly 2 words
$strictArgs[=2; Please provide exactly two words.]
```

---

### onlyAdmin

Restricts script execution to users with the `Administrator` permission. If the user is not an admin, the script stops immediately.

```
$onlyAdmin
$onlyAdmin[error message]
```

Example:
```
$onlyAdmin[❌ You need Administrator permission to use this.]
$sendMessage[Admin command executed.]
```

---

### onlyIf

Stops script execution if the given condition is false. The optional error message is sent when the condition fails.

```
$onlyIf[condition]
$onlyIf[condition; error message]
```

Example:
```
$onlyIf[$authorID == 123456789; ❌ Only the bot owner can use this.]
$sendMessage[Owner command executed.]
```

---

### ban

Bans a user from the server. Requires the bot to have the `Ban Members` permission.

```
$ban
$ban[userID or mention]
```

With no argument, bans the message author. Accepts a raw user ID or a mention (`<@id>`).

Example:
```
$ban[$message[1]]
```

---

### kick

Kicks a user from the server. Requires the bot to have the `Kick Members` permission.

```
$kick
$kick[userID or mention]
```

With no argument, kicks the message author.

---

### unban

Unbans a user from the server by ID. Requires the `Ban Members` permission.

```
$unban[userID]
```

---

### timeout

Puts a user in timeout (mutes them) for a specified duration. Requires the `Moderate Members` permission.

```
$timeout[userID or mention; duration]
```

Duration uses the same format as `$cooldown`: a number followed by `s`, `m`, `h`, or `d`.

Example:
```
$timeout[$message[1]; 10m]
```

---

### untimeout

Removes a timeout from a user. Requires the `Moderate Members` permission.

```
$untimeout[userID or mention]
```

---

### slowmode

Sets the slowmode interval for the current channel. Requires the `Manage Channels` permission.

```
$slowmode[seconds]
```

Use `0` to disable slowmode.

Example:
```
$slowmode[5]
```

---

### getBotInvent

Sends the bot's OAuth2 invite link (with Administrator permissions). Can also be used inline.

```
$getBotInvent
```

Inline usage:
```
$sendMessage[Invite the bot: $getBotInvent]
```

---

### ping

Sends the bot's current WebSocket latency in milliseconds to the channel. Can also be used inline.

```
$ping
```

Inline usage:
```
$sendMessage[Current latency: $ping]
```

Output:
```
Current latency: 42ms
```

---

### uptime

Sends the time elapsed since the bot started, formatted as `Xd Xh Xm Xs`. Can also be used inline.

```
$uptime
```

Inline usage:
```
$sendMessage[Bot has been running for $uptime]
```

---

### addTimestamp

Sends a Discord timestamp for the current time. When used as a standalone command it sends the timestamp. When used inline inside another argument, it returns the timestamp string.

**Standalone (default `T` format):**
```
$addTimestamp
```

**With a format code:**
```
$addTimestamp[format]
```

| Format | Display |
|--------|---------|
| `t` | Short time: `4:20 PM` |
| `T` | Long time: `4:20:00 PM` |
| `d` | Short date: `04/20/2025` |
| `D` | Long date: `April 20, 2025` |
| `f` | Short date/time: `April 20, 2025 4:20 PM` |
| `F` | Long date/time: `Sunday, April 20, 2025 4:20 PM` |
| `R` | Relative: `2 hours ago` |

Example:
```
$sendMessage[Event starts: $addTimestamp[R]]
```

---

### log

Takes a snapshot of the execution log up to that point and sends it to a specified channel after the script finishes. Useful for auditing command usage.

```
$log[channelID]
$log[channelID; name_code]
```

`name_code` is an optional label that appears in the log header. Multiple `$log` calls in the same script each capture events since the previous `$log` call.

If the log is short enough, it is sent as a code block. If it exceeds Discord's 2000-character limit, it is sent as a `.txt` file attachment (up to 10 MB).

Example:
```
$log[987654321098765432; admin-audit]
```

---

### addUserReactions

Adds emoji reactions to the **user's** triggering message. Accepts any combination of Unicode and custom Discord emojis. Maximum **20** emojis.

```
$addUserReactions[emoji1; emoji2; ...]
```

Example:
```
$addUserReactions[👍; ❤️; <:custom:123456789>]
```

---

### addBotReactions

Adds emoji reactions to the **last message sent by the bot** in this execution. Must be called after at least one bot message has been sent. Maximum **20** emojis.

```
$addBotReactions[emoji1; emoji2; ...]
```

Example:
```
$sendMessage[Cast your vote!]
$addBotReactions[👍; 👎]
```

---

## Built-in Variables

Read-only references resolved at runtime. Use them inline anywhere with `$name`.

| Variable | Value |
|---|---|
| `$authorID` | Numeric ID of the message author |
| `$authorName` | Username of the message author |
| `$mention` | Mention string of the message author (`<@id>`) |
| `$channelID` | Numeric ID of the current channel |
| `$channelName` | Name of the current channel |
| `$guildID` | Numeric ID of the current server |
| `$guildName` | Name of the current server (`DM` in direct messages) |
| `$membersCount` | Total member count of the current server |
| `$message` | Text after the command trigger (empty if no argument was given) |
| `$message[n]` | The nth word after the command trigger (1-based index) |
| `$messageID` | Numeric ID of the triggering message |
| `$botName` | Username of the bot |
| `$botID` | Numeric ID of the bot |
| `$ping` | Bot's current WebSocket latency in milliseconds (e.g. `42ms`) |
| `$uptime` | Time since bot started, formatted as `Xd Xh Xm Xs` |
| `$addTimestamp` | Discord timestamp for right now using the default `T` format |
| `$randomUserID` | ID of a random non-bot member of the current server |

Example:
```
$sendMessage[Hello $authorName, your ID is $authorID]
```

Output:
```
Hello user, your ID is 123456789012345678
```

### $message with index

`$message[n]` returns the nth word the user typed after the command trigger (1-based).

```
# User types: !cmd hello world
$sendMessage[First word: $message[1]]   # → hello
$sendMessage[Second word: $message[2]]  # → world
$sendMessage[All words: $message]       # → hello world
```

---

## Math Commands

Each command takes exactly two numeric arguments. All five can be used as standalone commands (result sent to channel) or inline inside other arguments. Integer results are displayed without a decimal point; non-integer results keep their decimal.

```
$sum[a; b]
$sub[a; b]
$mul[a; b]
$div[a; b]
$mod[a; b]
```

Division by zero produces a `🟡 Runtime Error` instead of crashing.

Example:
```
$var[x; 8]
$var[y; 3]
$sendMessage[$sum[$var[x]; $var[y]]]
```

Output:
```
11
```

Inline usage:
```
$sendMessage[Result is $sum[8; 2]]
```

Output:
```
Result is 10
```

---

## Random Commands

### randomint

Returns a random integer between `min` and `max` (inclusive). If `min > max`, they are automatically swapped. Can be used standalone or inline.

```
$randomint[min; max]
```

Example:
```
$sendMessage[Your lucky number: $randomint[1; 100]]
```

---

### randomstr

Picks one item at random from a list of strings. Can be used standalone or inline.

```
$randomstr[option1; option2; option3; ...]
```

Example:
```
$randomstr[rock; paper; scissors]
```

---

### randomUserID

Picks a random non-bot member from the current server and sends their numeric ID. Only works inside a server (not in DMs).

```
$randomUserID
```

Can also be used inline:
```
$sendMessage[Random member ID: $randomUserID]
```

---

## replaceText

Replaces all occurrences of a substring within a string. Can be used inline.

```
$replaceText[text; search; replacement]
```

Example:
```
$sendMessage[$replaceText[hello world; world; FDScript]]
```

Output:
```
hello FDScript
```

---

## Conditions: if / elif / else / endif

Evaluates a condition and executes the matching branch. Supported operators: `==` `!=` `>` `<` `>=` `<=`.

Numeric strings are compared numerically; non-numeric strings fall back to lexicographic comparison. Only `==` and `!=` support string comparison — `>`, `<`, `>=`, `<=` require numeric values.

```
$if[condition]
  ...
$elif[condition]
  ...
$else
  ...
$endif
```

Example:
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

Output:
```
Grade: B
```

### Compound Conditions: $and / $or

Multiple conditions can be combined inside `$if` or `$elif` using `$and` or `$or`. These cannot be used as standalone commands.

```
$if[$and[condition1; condition2; ...]]
$if[$or[condition1; condition2; ...]]
```

`$and` requires **all** conditions to be true. `$or` requires **at least one** to be true.

Example:
```
$var[age; 20]
$var[score; 85]
$if[$and[$var[age] >= 18; $var[score] >= 80]]
$sendMessage[Eligible!]
$else
$sendMessage[Not eligible.]
$endif
```

Output:
```
Eligible!
```

---

## while / endwhile

Repeats a block as long as a condition is true.

```
$while[condition]
  ...
$endwhile
```

Example:
```
$var[n; 1]
$while[$var[n] <= 3]
$sendMessage[Iteration $var[n]]
$var[n; $sum[$var[n]; 1]]
$endwhile
```

Output:
```
Iteration 1
Iteration 2
Iteration 3
```

---

## for / endfor

Repeats a block a fixed number of times. The count must resolve to a whole number; floats are truncated to integers.

```
$for[count]
  ...
$endfor
```

Example:
```
$for[3]
$sendMessage[Hello!]
$endfor
```

Output:
```
Hello!
Hello!
Hello!
```

---

## break

Exits the nearest enclosing `$while` or `$for` loop immediately. Using `$break` outside a loop is a logic error caught at validation time.

```
$break
```

Example:
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

Output:
```
Stopped at 4
```

---

## return / returnXxx Commands

These commands store data into named **return variables** that can be retrieved inline with `$return[varName]`.

### return

Reads the value stored by a `$returnXxx` command.

```
$return[varName]
```

This is an inline-only command. The variable must have been populated by one of the `$returnXxx` commands below.

---

### returnGuildUsersID

Fetches the IDs of all non-bot members in a server and stores them in a return variable.

```
$returnGuildUsersID[guildID; fetchMode; var; separator]
```

| Argument | Description |
|---|---|
| `guildID` | Numeric ID of the server |
| `fetchMode` | `cache` (use cached members) or `chunk` (fetch all members from Discord) |
| `var` | Name of the return variable to store the result |
| `separator` | Character or named separator to join IDs (see [Separators](#separators)) |

Example:
```
$returnGuildUsersID[$guildID; cache; members; com]
$sendMessage[Member IDs: $return[members]]
```

---

### returnGuildChannelsID

Fetches the IDs of channels in a server filtered by type, and stores them in a return variable.

```
$returnGuildChannelsID[guildID; channelType; var; separator]
```

| `channelType` | Matches |
|---|---|
| `text` | Text channels |
| `voice` | Voice channels |
| `category` | Category channels |
| `forum` | Forum channels |
| `stage` | Stage channels |
| `all` | All channel types |

Example:
```
$returnGuildChannelsID[$guildID; text; channels; com]
$sendMessage[Text channel IDs: $return[channels]]
```

---

### returnGuildRolesID

Fetches the IDs of roles in a server, optionally filtered by a permission, and stores them in a return variable. The `@everyone` role is always excluded.

```
$returnGuildRolesID[guildID; permission; var; separator]
```

Leave `permission` empty or use `all` to get all roles. You can also pass a raw permission integer.

Supported named permissions include: `admin`, `manage_guild`, `manage_roles`, `manage_channels`, `manage_messages`, `kick_members`, `ban_members`, `moderate_members`, `send_messages`, `view_channel`, `connect`, `speak`, and many others.

Example:
```
$returnGuildRolesID[$guildID; admin; adminRoles; com]
$sendMessage[Admin role IDs: $return[adminRoles]]
```

---

### returnGetReactions

Fetches reaction data from a specific message and stores it in a return variable.

```
$returnGetReactions[channelID; messageID; type; var; separator; emoji]
```

| Argument | Description |
|---|---|
| `channelID` | Numeric ID of the channel containing the message |
| `messageID` | Numeric ID of the message |
| `type` | `usersID` (returns IDs of users who reacted) or `tr` (returns total reaction count) |
| `var` | Name of the return variable |
| `separator` | Separator for joining user IDs (only used with `usersID`) |
| `emoji` | The emoji to look up (Unicode or custom `<:name:id>`) |

With `type = tr`, if the emoji was not found on the message, the result is `0`.

Example:
```
$returnGetReactions[$channelID; $messageID; tr; voteCount; com; 👍]
$sendMessage[Total 👍 votes: $return[voteCount]]
```

---

## Plain Text

Any line that does not start with `$` is sent directly to the channel. Built-in variables and inline commands are resolved before sending.

Example:
```
Welcome to the server, $authorName!
Your score is $var[score] and your ping is $ping.
```

---

## Separators

Several commands that return lists of IDs accept a `separator` argument. You can pass a literal character or one of the named separator aliases:

| Name | Character |
|---|---|
| `dot` | `.` |
| `com` | `,` |
| `apo` | `'` |
| `sem` | `;` |
| `colon` | `:` |

> **Important:** Because `;` is the argument delimiter, you can **never** pass a semicolon directly as a separator. Use the name `sem` instead.

---

## Inline Comments

Comments can appear at the end of any line, outside of brackets. Everything after a bare `#` at depth 0 is ignored.

```
$var[score; 100] # set initial score
$sendMessage[Score: $var[score]] # send it
```

---

## Error System

FDScript validates all commands before execution begins. If any error is found, **execution stops entirely** and all errors are reported to the channel. No partial execution occurs.

| Icon | Category | Common Causes |
|---|---|---|
| 🔴 | **Syntax Error** | Unknown command, unclosed bracket, mismatched block |
| 🟠 | **Logic Error** | Wrong argument count, invalid operator, `$break` outside loop |
| 🟡 | **Runtime Error** | Division by zero, non-numeric argument, `$for` count not integer |
| 🔵 | **Environment Error** | Channel not found, bot lacks permission, DM user not found |

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

## Variable Resolution Order

When `$var[name]` is encountered, the interpreter resolves it in this order:

1. Temporary in-memory variables set with `$var[name; value]`
2. Built-in read-only variables such as `$authorID` and `$channelName`

Persistent variables set with `$setVar` are accessed **only** via `$getVar[name]` and are not part of the above lookup chain.

`$return[name]` accesses an entirely separate store — the return variable map — populated only by `$returnXxx` commands.

>>>>>>> 5032b13 (Initial commit: BCFD-L source code)
