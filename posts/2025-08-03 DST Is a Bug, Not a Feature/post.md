tags: DST, DaylightSaving

### DST Is a Bug, Not a Feature: Countries That Ditched It (and Didn't Regret It)

Daylight Saving Time isn't "saving" anything. It's a 100-year-old hack that introduces twice-yearly bugs into every system that touches schedules, logs, billing, notifications, cron jobs, and human sanity.

We advance clocks in spring → people lose an hour of sleep → heart attacks spike slightly, accidents go up, life satisfaction dips. Fall back → everyone celebrates the "extra hour" until they realize it's just redistributing misery. Energy savings? Negligible or negative in modern AC-heavy worlds. Developer pain? Infinite.

Yet somehow, most of Europe and North America still run this circus. Meanwhile, a growing list of countries said "nah" and haven't looked back. Let's meet the defectors who fixed their timezone code and moved on with fixed offsets forever.

### 1. Russia (abolished 2014, after a brief "permanent DST" experiment gone wrong)
Tried permanent summer time 2011–2014 → dark winter mornings, kids going to school in pitch black, massive complaints. Switched back to permanent standard time (winter time) in 2014. Result? No more biannual chaos, simpler scheduling across 11 time zones (now 11 again after earlier cuts), no regrets reported. Russians just shrugged and kept living. If a country spanning ~11 time zones can ditch the switch without imploding, your app can too.

### 2. China (tried 1986–1991, abolished permanently)
Short experiment for "energy conservation." Saved a bit of kWh in theory, but caused massive confusion-people forgot to change clocks, meetings double-booked, factories messed up. Government killed it in 1992 citing "inconvenience." China never looked back. One timezone (UTC+8, no DST ever), 1.4B+ people, zero clock-change bugs in WeChat/Alipay/Douyin. Coincidence? I think not. They basically run on naive Asia/Shanghai everywhere and it scales beautifully.

### 3. Iceland (abolished effectively since 1968, permanent UTC+0)
Way up north with insane summer daylight anyway (midnight sun vibes). Tried DST briefly, ditched it because extending already-long days made zero sense. No clock changes since the late 60s. Icelanders just live with consistent time. Productivity didn't collapse. Northern lights still appear. Win.

### 4. Turkey (switched to permanent DST in 2016 → effectively no more changes)
They didn't "abolish" the switch so much as lock it on summer time forever (UTC+3 year-round). No fall-back. No spring-forward. Just fixed. Energy arguments aside, no biannual disruptions. Business goes on.

### 5. Recent dropouts (last 10–15 years): Armenia, Azerbaijan, Belarus, Georgia, Iran, Jordan, Namibia, Samoa, Syria, Uruguay
These are the fresh ones. Jordan/Syria went permanent summer time recently (2022). Namibia, Uruguay ditched after trials showed meh energy gains and lots of hassle. Iran bounced for religious/political reasons but stayed off. Pattern? Once you stop the twice-yearly jolt, nobody riots to bring it back. The switch is the bug; fixed offset is the stable release.

For Australia the story is entirely different, Australia - the chaotic half-defector that accidentally proved the point. Australia is the ultimate “we tried DST and mostly hated it” exhibit.

Three mainland states (Queensland, Western Australia, Northern Territory) never observe DST and have been on permanent standard time forever.
Queensland in particular has been loud about it since 1992 - they tried it, voters hated the late sunsets messing with kids’ bedtimes and farmers’ routines, and they killed it permanently. No regrets.

The other states (NSW, Victoria, SA, Tasmania, ACT) still do the biannual dance… but even there, every few years someone floats “permanent summer time” or “permanent standard” and the public usually says “just pick one and leave it alone.”
Result? A country with wildly inconsistent rules across borders, yet the non-DST states report zero chaos compared to the ones that still flip. Queensland businesses schedule with Brisbane time year-round, no bugs, no double-booked Zoom calls, no “did the meeting move because of DST?” drama. Meanwhile Sydney/Melbourne teams still deal with the March/October ritual.

Australia basically runs a live A/B test: half the country on fixed offset, half still running legacy code. Guess which half has fewer timezone-support tickets? Fixed wins.
Bonus honorable mentions:

Arizona (most of it, since 1968) - Hot desert + DST = more AC runtime in evenings = higher bills. Opted out permanently. Navajo Nation still does DST for border reasons, but the state as a whole? Nope.

Most equatorial/tropical countries - Never bothered in the first place. Daylight barely varies year-round. Why add bugs when nature already gave you a stable API?

### What These Countries Teach Us Devs
- Biannual changes are **non-deterministic garbage** injected into otherwise predictable systems.
- Permanent fixed offset = fewer edge cases (no "did this event happen before/after the switch?"), simpler queries, no timezone DB updates breaking prod every March/October.
- "But energy savings!" - Modern studies show it's a wash or net negative. Countries that quit report no measurable regret spike.
- Humans adapt fast to fixed local wall-clock time. Meetings at 9 AM stay 9 AM forever. Cron jobs don't ghost or double-fire.

 
DST isn't a feature. It's technical debt the world is slowly paying off.