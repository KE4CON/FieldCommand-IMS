# FieldCommand IMS — User Manual (World Edition)

*Every feature, explained and step by step — in plain language.*

*Generated August 13, 2026 · Markdown is the living source of truth.*


---


# 1. Introduction & System Overview

*What FieldCommand IMS is, what problem it solves, and a guided tour of the dashboard you land on when you open it.*

> **QUICK VERSION** — FieldCommand IMS is an incident-management system that runs on a small computer and makes its own Wi-Fi, so it keeps working with **no internet, no cell service, and no power grid**. You use it from a web browser on any phone, tablet, or laptop — no app to install, no login. When you open it you land on the **dashboard**: a grid of **tool cards** you tap to open tools, a row of three **mode** buttons at the top, and a **status sidebar** on the right showing how the server is doing.


## What This Is / What It Is For

When a real disaster hits, the tools everyone leans on tend to fail at the worst possible moment. Cell towers go down, the internet goes dark, and the power grid quits. The cloud software an emergency operations center depends on is suddenly unreachable, and the incident falls back to paper forms, a whiteboard, and whatever one tired person can keep in their head. **FieldCommand IMS exists to remove that failure point.**

FieldCommand IMS is a complete Incident Command System (ICS) and National Incident Management System (NIMS) tool that carries everything it needs inside one small server — a Raspberry Pi. The Pi broadcasts its own private Wi-Fi network (named **EMCOMM-NET** by default), runs a web server, and stores all your data locally. Any device that joins that Wi-Fi and opens a browser gets the full set of tools instantly. There is nothing to download and no account to create.

Because it never depends on the outside world, it does not break when the outside world breaks. When internet **is** available, a few extra features switch on by themselves — live weather alerts, radar, and other online data. When the internet drops, those features quietly pause and everything else keeps running exactly as before. The system is built to lose connectivity without losing your incident.

> **WHO THIS MANUAL IS FOR** — You do not need to be a computer person, and you do not need a radio license, to use most of your organization. If a term looks like alphabet soup, this manual spells it out the first time it appears. The parts that legally require a licensed amateur-radio operator are clearly marked, and they are the only parts that need one.


## What You See First — the Dashboard

Point your browser at the server address (by default **http://192.168.50.1** — Chapter 2 walks through connecting) and the **Station Dashboard** loads. It is the home screen for the whole system, and every tool is one tap away from here. From top to bottom you see:

| What you see | Where it is | What it does |
| --- | --- | --- |
| **Callsign badge** | Top-left of the dark hero bar | Shows your station's name in large letters. Until setup is done it reads **EMCOMM-NET**; after setup it shows your club callsign and your organization name underneath. |
| **Clocks** | Top-right of the hero bar | A big primary clock and a smaller secondary clock. In Amateur Radio mode the big one is **UTC** (the worldwide radio time standard); in the other modes the big one is your **local** time. Both run live, second by second. |
| **Mode pill** | Under the clocks | A small colored tag telling you which of the three modes is active right now. |
| **Mode switcher** | The row of three big buttons below the hero bar | Switches the dashboard between Amateur Radio, Public Safety, and ICS views (see below). |
| **Weather + Radar row** | Top of the main column | Live National Weather Service (NWS) alerts and a link to animated radar — when internet is available. |
| **Tool cards** | The grid filling the main column | Each card opens one tool. Grouped under labeled headings like Operations, Public Safety, and Forms & Traffic. |
| **Status sidebar** | The narrow column on the right | Live health of the server — temperature, memory, disk, internet, GPS — plus a services list and quick links. |

> _[Figure: The FieldCommand Station Dashboard: dark hero bar with callsign badge and clocks, the three mode buttons, tool-card grid, and the status sidebar on the right]_

> **A YELLOW BANNER ON A BRAND-NEW SYSTEM** — If the server has never been set up, a yellow banner appears near the top saying **FieldCommand IMS is not configured** with a link to run the setup wizard. That is normal on a fresh system — everything still works, the banner is just a reminder. Setup is covered in Chapter 3.


## The Three Modes

The three big buttons under the hero bar — **📻 Amateur Radio**, **🚔 Public Safety**, and **🏛 ICS / Incident Command** — are **modes**. A mode simply decides which tool cards are shown, so the screen stays uncluttered and you see the tools that fit what you are doing. Switching modes never hides or deletes anything; the tools you are not looking at are still there, one button away.

| Mode | What it shows | Best for |
| --- | --- | --- |
| **📻 Amateur Radio** | Net control logging, callsign lookup, APRS mapping, Winlink, JS8Call, propagation, radiogram traffic forms | Ham-radio net operations run by licensed operators |
| **🚔 Public Safety** | The public service net logger, radio-ID roster, resource-tracking map, facilities directory, observer view | Public Safety radio nets and unit tracking |
| **🏛 ICS / Incident Command** | The full incident-command platform — Command, Operations, Planning, Logistics, and Finance tools plus every ICS form | Running an actual incident with formal ICS paperwork |

> **THE AMATEUR RADIO MODE CAN BE GRAYED OUT — ON PURPOSE** — The amateur-radio features legally require a licensed operator. If your group set up the system with **no callsign** (because no one holds an amateur license), the **📻 Amateur Radio** button appears dimmed with a small lock, and that is correct — every incident-management and public-safety tool still works normally. A callsign can be added later in Setup, which lights the button up. See Chapter 3.

The mode you pick also changes the primary clock: Amateur Radio mode puts **UTC** front and center because radio operators log in UTC worldwide, while ICS and Public Safety modes put your **local** time front and center, which is what incident paperwork uses.


## Tool Cards — How You Open Things

Almost everything in FieldCommand IMS is reached by tapping a **tool card**. Each card is a small tile with an icon, a name, and a one-line description of what it does. A few cards also show a small tag in the corner — that tag names the technical service or port behind the tool, which you can safely ignore unless you are troubleshooting. Tap a card and the tool opens.

Cards are grouped under section labels so related tools sit together. In Amateur Radio mode, for example, you see headings like **⚡ Operations**, **🚨 Public Safety**, **📋 Forms & Traffic**, and **📚 Reference**. A card marked with a small **↗** opens in a new browser tab because it is a separate mini-application (the live APRS map and the offline Wikipedia library are examples).

> **IF A CARD OPENS A BLANK OR ERROR PAGE** — A card that points to a separate service can only work if that service is running and, in a few cases, if a piece of hardware (like a radio) is attached. If a card opens to nothing, it usually means that optional piece is not set up on your system — it does not mean the whole dashboard is broken. Come back to the dashboard with your browser's Back button.


## The Status Sidebar

The narrow column on the right is the **STATION STATUS** panel — a live readout of the server's health that refreshes on its own. You do not act on it; you glance at it to confirm the system is healthy.

| Readout | Plain meaning |
| --- | --- |
| **DMS bar** | The Dead Man's Switch status. "Disarmed" means the net-inactivity watchdog is off. Covered in its own chapter. |
| **CPU Temp** | How hot the server's processor is, in degrees Celsius. A normal number means the Pi is comfortable. |
| **Memory** | How much of the server's working memory is in use, as a percentage. |
| **Disk** | How full the storage drive is, as a percentage. |
| **Internet** | A green dot means the server currently reaches the internet; red means it does not (and that is fine — see below). |
| **GPS Fix** | Green if an attached GPS receiver has a location lock; amber if not. |
| **Updated** | The time of the last health check, so you know the numbers are current. |
| **SERVICES** | A row of small dots, one per background service (nginx, Direwolf, Chrony, and so on), showing which are running. |

Below the status panel is a small **internet indicator** and a **QUICK LINKS** panel with shortcuts to a few common pages — Observer Mode, the Pre-flight Check, the Print Center, and Callsign Lookup.


## Weather and Radar

Across the top of the main column sit two live widgets. The **⚡ NWS WEATHER ALERTS** panel pulls active National Weather Service warnings and watches for your area and lists them, color-coded by severity. Next to it, the **NWS RADAR** card links to an animated radar loop. Both of these need internet, so they only fill in when the server is online; offline, the weather panel shows a "Waiting for internet connection" note and the rest of the dashboard carries on. A small **⟳** refresh button on the weather panel forces an immediate re-check.


## Offline First — What Keeps Working

The single most important idea in this whole system: **losing the internet does not take FieldCommand IMS down.** A red "Offline" internet dot only means the handful of features that pull live outside data are paused — weather alerts, radar, and a couple of internet radio feeds. Everything that matters for running an incident keeps working with no change at all:

- All ICS forms and the Incident Action Plan (IAP) — the master plan for an operational period
- The T-card resource board and personnel check-in
- Both net loggers (amateur and public service)
- The member roster and Quick Response (QR) code check-in
- Callsign lookup, which uses a copy of the national license database stored right on the server
- The offline maps, the reference library, and the print center

> **GRACEFUL, AUTOMATIC RECOVERY** — You never have to do anything to "go offline" or "come back online." When internet returns, the paused features light back up on their own within a minute or two. When it drops again, they pause again. The system handles the switch quietly in the background.


## Enter Once, Fill Every Form

One design idea runs through the entire ICS side of FieldCommand IMS and is worth understanding up front: **you enter shared incident facts one time, and they flow into every form automatically.** The dashboard's **📋 General Info** card (in ICS mode) opens the page where this happens.

On the **General Information** page you type the incident's name, number, and type; the operational period dates; the incident commander and section chiefs; the key unit leaders; and current weather. A single **💾 Save & Propagate to All Forms** button pushes those values into all of the ICS forms for that incident at once. Change a name here, and every form that uses it updates immediately — you never retype the incident commander's name onto twenty separate forms. The page even fetches current conditions from the National Weather Service and calculates sunrise and sunset from the incident's coordinates when you click **Fetch NWS**.

> **YOU CAN EXPLORE BEFORE YOU COMMIT** — A fresh FieldCommand system is fully working the moment it powers on. Nothing is locked behind setup — you can open the dashboard, tap through the tools, and practice freely before you ever configure the system for your group. This is the ideal way to get comfortable before a real activation.


## Troubleshooting

- *The dashboard won't load at all.* Your device is probably on the wrong Wi-Fi. Connect to **EMCOMM-NET** and type the full address including `http://` — for example `http://192.168.50.1`. Chapter 2 covers connecting step by step.
- *The weather panel just says "Waiting for internet connection."* That is expected when the server is offline. Weather and radar need the internet; the rest of the dashboard works without it. Watch the sidebar **Internet** dot — when it turns green, the weather panel fills in on its own.
- *The 📻 Amateur Radio button is dimmed and won't respond.* That happens when no station callsign is configured, and it is by design — the ham features need a licensed operator. Use the other modes normally, or add a callsign in Setup (Chapter 3) to enable it.
- *A yellow "not configured" banner is at the top.* The system has not been through Setup yet. Everything still works; the banner is a reminder. Run the setup wizard (Chapter 3) when you are ready, and the banner goes away.
- *I tapped a card and got a blank or broken page.* That card points to an optional or separate service that isn't set up on this system, or a needed piece of hardware isn't attached. Tap your browser's Back button to return to the dashboard; the rest of the system is unaffected.
- *The sidebar numbers or service dots aren't updating.* The health readout polls the server every few seconds. If it stalls, the server may be busy starting up (give it a minute after power-on) or your connection to EMCOMM-NET may have dropped — reconnect and reload the page.


# 2. Getting Started — Connecting to FieldCommand

*How any phone, tablet, or laptop joins the FieldCommand Wi-Fi and opens the dashboard — no app to install, no login, any operating system.*

> **QUICK VERSION** — On any phone, tablet, or laptop, open **Wi-Fi settings** and join the network named **EMCOMM-NET** (the password is on the equipment label). Then open a web browser and go to **http://192.168.50.1**. The dashboard loads. That's the whole process — no app, no sign-in, works on Apple, Android, Windows, whatever you have.


## What This Is / What It Is For

Every screen in FieldCommand IMS is just a **web page** served from the Raspberry Pi, exactly like visiting a website — except the "website" lives on the little server in the room with you instead of out on the internet. That one fact is what makes getting started so easy: **if your device has a web browser, it can use FieldCommand IMS.** There is no app to download from an app store, no software to install, and no username or password to create for the system itself.

This chapter is the shortest path from "I just walked in" to "I'm looking at the dashboard." It works the same way for a volunteer's personal phone, a borrowed tablet, an incident laptop, or the operator workstation — every device connects the same two-step way: **join the Wi-Fi, then open the address.**

> **ANY BROWSER, ANY DEVICE** — Chrome, Safari, Firefox, Edge, and the built-in browser on any modern phone or tablet all work. Apple, Android, Windows, Chromebook, Linux — it does not matter. You do not need the newest device; anything from roughly the last several years is fine.


## Step 1 — Join the EMCOMM-NET Wi-Fi

FieldCommand makes its own private Wi-Fi network. You connect to it the same way you connect to Wi-Fi anywhere else.

1. If the server was just powered on, give it about **45 seconds** to finish starting. It is ready when a Wi-Fi network named **EMCOMM-NET** shows up in your device's list of available networks.
2. Open your device's **Wi-Fi settings** (on a phone this is usually in Settings, or by pulling down the control panel and holding the Wi-Fi icon).
3. In the list of networks, tap **EMCOMM-NET**.
4. Enter the Wi-Fi password when asked. The password is printed on the **equipment case label** and listed in the Installation Guide. There are no other credentials to enter.
5. Wait for your device to show it is connected to EMCOMM-NET.

> _[Figure: A phone's Wi-Fi settings screen with EMCOMM-NET selected and connected]_

> **"NO INTERNET" ON THIS NETWORK IS NORMAL** — Your phone may warn that EMCOMM-NET has **no internet access**, or show a small exclamation mark on the Wi-Fi icon. That is completely expected — FieldCommand is a private network for reaching the server, not a path to the internet. If your device offers to **stay connected** to a network with no internet, choose to stay connected. This is the single most common source of confusion, and it is not a problem.


## Step 2 — Open the Dashboard

Once you are on EMCOMM-NET, you reach FieldCommand the same way you reach any web page: by typing its address into a browser.

1. Open any web browser on the device.
2. In the address bar at the top, type **http://192.168.50.1** exactly, including the `http://` part, and go to it.
3. The **FieldCommand Station Dashboard** loads. You are in — that is everything.
4. If a yellow "not configured" banner appears, the system simply hasn't been set up for your group yet (Chapter 3). Everything still works.

> **TYPE THE ADDRESS, DON'T SEARCH FOR IT** — Type `192.168.50.1` into the **address bar**, not into a search box. If you type it as a search, the browser may try to look it up on the internet (which isn't reachable) instead of opening the local server. Including the `http://` at the front helps the browser understand you mean an address, not a search. If your deployment was set up with a different server address, use that number instead — but `192.168.50.1` is the default and what this manual assumes throughout.

There is no login screen. The moment the dashboard loads, you have the full set of tools. FieldCommand does not ask each person to create an account, because in a field activation there is no time for that and often no way to reset a forgotten password. Access is controlled by who can reach the private Wi-Fi, not by individual logins.


## Make It Feel Like an App

You will open the dashboard many times, so it is worth making it one tap away instead of retyping the address each time.

1. With the dashboard open in your phone's browser, tap the browser's **Share** button (or menu).
2. Choose **Add to Home Screen**.
3. Give it a name like "FieldCommand" and confirm.
4. A FieldCommand icon now sits on your home screen. Tapping it opens the dashboard directly, filling the screen like a real app.

> **BOOKMARK IT ON A LAPTOP** — On a laptop, bookmark **http://192.168.50.1** so it is one click away. Consider making it the browser's home page on a dedicated incident laptop or the operator workstation, so the dashboard is up the instant the browser opens.


## The Padlock — A Secure, Encrypted Connection (HTTPS)

FieldCommand now serves the dashboard over **HTTPS** — Hypertext Transfer Protocol Secure, the same locked-padlock technology your bank's website uses. In plain words: everything that travels between your device and the server is **scrambled (encrypted)** so no one else on the air can read it. Member names, phone numbers, check-in details — all of it stays private as it crosses the Wi-Fi. It is also what lets your phone's **camera** work for scanning QR codes, because browsers only turn the camera on for a secure connection.

You do not have to do anything different to get this. If you type the plain **http://192.168.50.1** address, FieldCommand automatically sends you to the secure **https://** version — the extra **s** is added for you. There is nothing new to memorize.

> **WHY YOU MIGHT SEE A WARNING THE FIRST TIME** — On the public internet, a padlock is backed by a certificate bought from an outside company. FieldCommand runs on a **closed, private field network** with no path to those companies, so it makes its **own** certificate. Your browser doesn't recognize it the very first time and may show a one-time warning. This is expected on a private network and does **not** mean anyone is spying on you — it only means the browser has never met this particular server before. You clear it once per device, and then it's quiet forever after.

There are two ways to get past that first-time warning. Either one is fine — pick whichever suits you.


### The quick way — accept the warning once

The fastest option is to tell the browser you trust this server, just this once per device.

1. Go to the dashboard address. If you see a page titled something like **Your connection is not private** or **Not secure**, don't panic — this is the expected first-time message on a private network.
2. Look for a small link or button such as **Advanced**, **Show details**, or **More information**, and tap it.
3. Tap the option that says **Proceed to 192.168.50.1**, **Continue to this site**, or **Visit this website**.
4. The dashboard loads and works normally. Your device remembers this choice, so you won't be asked again on this device.

> **THE ADDRESS BAR MAY STILL SAY "NOT SECURE"** — After you accept the warning the quick way, some browsers keep showing a faint **Not secure** note next to the address. Your connection is still fully encrypted — the note just means the browser is using the server's own certificate rather than one from an outside company. If that note bothers you, use the cleaner way below to get a proper padlock.


### The clean way — install the certificate once (proper padlock, no warning)

If you'd rather see a real padlock with no warning at all, install the server's **root certificate** on the device one time. Think of it as introducing your device to the server so they recognize each other from then on. This is the tidiest option for a device you'll use often, like the operator workstation or your own phone.

1. On the device, open a browser and go to **https://192.168.50.1/fieldcommand-ca.crt** (type it exactly). This downloads a small file called `fieldcommand-ca.crt` — the server's certificate.
2. Open that downloaded file and, when the device asks, choose to **install** or **trust** it. On a phone this is usually under a prompt like *Install certificate*; on a laptop, opening the file starts a short install wizard — accept the defaults.
3. If asked what to trust it for, choose to trust it for **websites** (sometimes worded *SSL* or *web sites*).
4. Go back to **https://192.168.50.1**. You now see a clean **padlock** and no warning, on this device, from now on.

> **EACH DEVICE DOES THIS ONCE** — Whichever way you choose, it is a **one-time step per device**, not something you repeat every visit. A brand-new phone that joins for the first time will see the warning once; every device you've already cleared or installed the certificate on just opens straight to the dashboard. It is worth walking new volunteers through this the first time they connect at a check-in table.


## The One Thing That Trips People Up

Modern phones badly want to be on a network that has internet. Because EMCOMM-NET deliberately has none, a phone left to its own devices may quietly hop back to a cell connection or a nearby Wi-Fi network with internet — and then the dashboard stops loading, seemingly at random. The fix is to keep your device pinned to EMCOMM-NET during an activation.

- In your Wi-Fi settings, turn **off auto-join** for other nearby networks while you are working an activation, so your device can't wander off to them.
- If the dashboard suddenly won't load, glance at your Wi-Fi indicator first — nine times out of ten the device switched networks on its own. Reconnect to EMCOMM-NET and reload the page.
- On a phone, turning **cellular data off** for the duration is a reliable way to force it to stay on EMCOMM-NET (you're not using the internet anyway).


## Laptops, Workstations, and Many Users at Once

A laptop or the operator workstation connects exactly the same way — join EMCOMM-NET, open `http://192.168.50.1`. On Raspberry Pi 500 set up as the station's desktop, the browser may already be pointed at the dashboard for you.

There is no per-device setup and no limit you need to worry about in practice: many volunteers can each be on their own phone, all connected to EMCOMM-NET, all using FieldCommand at the same time. Everyone sees the same live data because it all lives on the one server. One person can be logging a net while another checks people in and a third fills out a form — the system is built for a room full of people working at once.

> **SPREADING WI-FI COVERAGE FARTHER** — If the activation site is large, the network can be extended with additional mesh access points so EMCOMM-NET reaches the whole area, and people's devices roam between them seamlessly. That is a hardware setup covered in the Installation Guide — from a user's point of view you still just join EMCOMM-NET and open the address, wherever you are standing.


## Troubleshooting

- *EMCOMM-NET doesn't appear in my Wi-Fi list.* The server may still be starting — wait about 45 seconds after power-on and refresh the Wi-Fi list. If it still isn't there after a couple of minutes, confirm the Pi and its router have power, and that you are within Wi-Fi range.
- *I'm connected to EMCOMM-NET but the dashboard won't load.* Make sure you typed the full address including `http://` (for example `http://192.168.50.1`) into the **address bar**, not a search box. Then confirm your device is still on EMCOMM-NET and hasn't switched to another network.
- *My phone keeps dropping off EMCOMM-NET.* It is hopping to a network with internet. Turn off auto-join for other networks (and optionally turn off cellular data) so it stays put, then reconnect to EMCOMM-NET.
- *My phone warns "no internet" and asks if I want to stay connected.* Say yes / stay connected. EMCOMM-NET has no internet on purpose; that warning does not mean anything is wrong.
- *The browser tried to search Google instead of opening the page.* You typed the address into a search box, or left off the `http://`. Type it into the address bar with the `http://` prefix.
- *The browser says "Not secure" or "Your connection is not private."* This is the expected one-time message on FieldCommand's private, encrypted network — it has its own security certificate rather than one from an outside company, because there's no internet out here. Tap **Advanced** (or **Show details**), then **Proceed to 192.168.50.1** to continue; you'll only be asked once on this device. For a clean padlock with no warning, install the server's certificate once by opening **https://192.168.50.1/fieldcommand-ca.crt** and choosing to trust it (see "The Padlock" section above).
- *It asks me for a login or account.* FieldCommand itself has no login. If you are being asked to sign in, you have most likely reached a different site because your device is on the wrong network — reconnect to EMCOMM-NET and reload `http://192.168.50.1`.
- *A card on the dashboard says it needs a different address or port.* Some tools open a separate service in a new tab. Those work as long as the server does; if one fails to load, tap Back and keep using the rest of the dashboard normally.


# 3. Organization Setup & Station Configuration

*The one-time setup screen that teaches FieldCommand who you are — your organization, your callsign, your location, your network, and which features to turn on.*

> **QUICK VERSION** — Open a browser to the server address and go to **Setup**. Fill in your **callsign** (or leave it blank), your **organization** and the **agency** you serve, your **location**, and your **network** details; pick which **Active Modules** to turn on; then click **Save**. FieldCommand is now configured for your organization.


## What This Is / What It Is For

Before your organization can run an incident on FieldCommand, the server needs to know a handful of basic facts: who you are, where you are, what to call your Wi-Fi network, and which features you want turned on. The **Setup** screen collects all of that **once**. Everything you type here is saved on the server and reused everywhere — on the dashboard, on printed ICS forms, on the map, and in the header of every report — so you never have to type it again.

Think of Setup as filling out the cover sheet for the whole system. It is normally done one time, by whoever stands the server up, and then left alone. You can come back and change any of it later, but most groups set it and forget it.

> **WHO DOES THIS** — Setup is an administrator task — one person configures the server for the whole team. Everyone else just connects to it (Chapter 2) and starts working; they never see this screen.


## Opening the Setup Screen

1. On any device connected to the FieldCommand Wi-Fi, open a web browser.
2. Go to the server address — by default **http://192.168.50.1** (type it exactly, including the `http://`).
3. The main dashboard opens. Find and click **Setup** (the gear/settings link).
4. The **⚙ FieldCommand IMS Setup** page opens — a single long form divided into labeled sections. You fill it top to bottom, then Save at the end.

> _[Figure: The FieldCommand Setup page: the ⚙ FIELDCOMMAND IMS SETUP heading with the sectioned form below]_

> **A GREEN BANNER MEANS IT'S ALREADY SET UP** — If setup has been completed before, a green **completed** banner shows at the top. That's fine — you can still change any field and Save again; you are just editing the existing configuration.


## Callsign & Identity

The first section, **📡 Callsign & Identity**, tells FieldCommand the amateur-radio identity of the station. It has two fields:

| Field | What to type | Notes |
| --- | --- | --- |
| **Club / Station Callsign** | Your group's club or station callsign — for example **your club callsign** — or **leave it blank** | This is the whole team's shared callsign. The field shows a faint example and the reminder *“or leave blank”*. |
| **Personal Callsign (Operator/Developer)** | The callsign of the person setting the station up (example: `KE4CON`) | Optional; used for attribution. |

> **LEAVING THE CALLSIGN BLANK IS ALLOWED — ON PURPOSE** — If **no one in your group is a licensed amateur-radio operator**, leave the Club / Station Callsign **blank**. FieldCommand then keeps the whole **Amateur Radio** side of the app grayed out, so you only see the features you can legally use. The ham features (APRS, Winlink, 44Net, JS8Call) legally require a properly licensed operator with privileges on the bands and modes used — so the app will not let you enable any of them without a callsign.


## Your Organization & the Agency You Serve

Next, tell FieldCommand who is running the system and, if applicable, who you serve. These names appear on the dashboard header and on every ICS form and report.

| Field | What to type | Example (your organization) |
| --- | --- | --- |
| **Organization Full Name** *(required)* | The full name of your group | your organization |
| **Organization Abbreviation** | A short form of that name | your org's short form |
| **Associated Agency Name** | The agency you support during an incident (leave blank if none) | your served agency |
| **Agency Abbreviation** | A short form of the agency name | your agency's short form |

> **ONLY THE ORGANIZATION NAME IS REQUIRED** — The starred **Organization Full Name** is the only required field in this section. If your group doesn't formally support a single agency, leave the two Agency fields blank.


## Location

The **📍 Location** section places your station on the map and fills in the geographic header on forms. Fill in what you know:

| Field | What to type |
| --- | --- |
| **City** | Your city or town (example: `your city`) |
| **County** | Your county (example: `your county`) |
| **State** | Your state (example: `your state`) |
| **Contact Email** | A contact address for the station |
| **Latitude (decimal)** | Your latitude in decimal degrees (example: `42.3247`) |
| **Longitude (decimal)** | Your longitude in decimal degrees (example: `-88.3822`) — note the minus sign for west |
| **Grid Square (Maidenhead)** | Your Maidenhead grid locator (example: `EN52wa`) — a short code hams use for location |

> **DON'T KNOW YOUR COORDINATES?** — If you leave latitude and longitude blank, the map simply centers on a default until you fill them in. You can look your coordinates up later and come back — nothing else depends on them being perfect on day one.


## System & Network

The **🖥️ System & Network** section covers how devices reach the server and a couple of housekeeping defaults.

| Field | What to type | Default |
| --- | --- | --- |
| **Default Incident Name** | A name pre-filled when you start a new incident | e.g. `County EOC Activation` |
| **Wi-Fi Network Name (SSID)** | The name of the Wi-Fi network operators join | `EMCOMM-NET` |
| **Wi-Fi Password** *(optional)* | The password for that Wi-Fi network. If you fill it in, it gets printed on the back of member ID cards so people can join without asking. Leave it blank to keep it off the cards. | *(blank)* |
| **Server Address** | The web address of the server | `http://192.168.50.1` |
| **Time Zone** | Your local time zone (so logs and forms stamp the right time) | your local zone |

> **CHANGE THE WI-FI NAME OR ADDRESS WITH CARE** — The **Wi-Fi Network Name** and **Server Address** are how every operator's device finds the system. If you change them here, you must also change the matching network settings on the server itself, or people won't be able to connect. For most groups, the defaults (`EMCOMM-NET` and `http://192.168.50.1`) are exactly right — leave them alone unless you have a specific reason.

> **THE WI-FI PASSWORD FIELD IS JUST FOR PRINTING ON CARDS** — The **Wi-Fi Password** field here is optional and does one simple thing: if you type your network's password into it, that password gets printed on the **back of member ID cards** (Chapter 4), so a member can join the Wi-Fi and reach the dashboard without hunting anyone down to ask. Typing it here does **not** change the actual network password — it only decides whether the cards show it. Leave it blank and the cards simply won't print a password. If your group would rather not have the Wi-Fi password floating around on printed cards, leave it empty.


## Organization Logo

Under **🏅 Organization Logo**, you can upload a small image of your group's logo. It appears on the dashboard and on the cover of printed reports. This is optional — skip it and FieldCommand simply shows no logo. To add one, use the file picker to choose an image file from the device you're using.

> _[Figure: The Organization Logo section with the file picker and a preview of the uploaded logo]_


## Default ICS Form Variant

The **📋 Default ICS Form Variant** setting picks which style of Incident Command System (ICS) forms the app fills out by default. Choose the variant your served agency expects; if you're not sure, leave it on the default — you can change the variant on any individual form later.


## Active Modules — Turning Features On

The **🔌 Active Modules** section is a set of on/off switches for FieldCommand's optional features. Turn on only what your group uses; anything you leave off is hidden from the dashboard, keeping the screen uncluttered.

> **HAM MODULES NEED A CALLSIGN** — The amateur-radio modules (**APRS**, **Winlink**, **44Net**, **JS8Call**) cannot be switched on unless a Club / Station Callsign is set above. If you left the callsign blank, those switches stay disabled — by design, because those features legally require a licensed operator. Set a callsign first, then come back and enable them.

Switch on the modules you want, leave the rest off, and remember you can revisit this list anytime as your group's capabilities grow.


## Public Safety Radio System Configuration

The **🚔 Public Safety Radio System Configuration** section is where you describe the public-safety radio system your group monitors or operates alongside — for your organization, that is **public service**. Fill in the system details for your area here so the public-safety net logger and related tools know what talkgroups and channels to expect. If your group is amateur-only and does not touch a public-safety system, you can leave this section as-is.

> _[Figure: The Public Safety Radio System Configuration section]_


## Software Attribution

The final section, **ℹ Software Attribution**, shows the software author and license credit. This is informational and stays the same in every edition — it satisfies the software's license. You don't need to change anything here.


## Saving, and What Changes Afterward

1. Scroll to the bottom of the Setup page.
2. Click **Save** (the save/confirm button).
3. You'll see a confirmation, and the green **completed** banner appears at the top.

Once you Save for the first time, FieldCommand marks itself **set up**. From then on: your organization name and served agency appear in the dashboard header and on forms; the map uses your coordinates; only the **Active Modules** you enabled show on the dashboard; and — if you left the callsign blank — the Amateur Radio features stay grayed out. Every operator who connects now sees a system that's branded and scoped to your organization.

**Can you use FieldCommand before it's set up? Yes.** A brand-new server is fully working the moment it powers on — every feature is available and nothing is hidden, so you can explore and practice freely before you ever open Setup. Finishing Setup does **not** switch the system on; it simply **tailors** it to your group. It fills in your organization, agency, and location everywhere they appear, and it tidies the dashboard so you only see the features that apply to you.

> **WHAT CHANGES ONCE SETUP IS COMPLETE** — Two things get tidied off the dashboard after your first Save: the **Amateur Radio** features are grayed out if you left the callsign blank (they legally require a licensed operator, so the app won't let an unlicensed group use them), and any **Active Modules** you chose not to turn on are hidden. Neither of these stops the server from running — they only change what shows on screen. Before that first Save, none of this tidying happens, so a fresh server deliberately shows **everything** for you to look around.


## Troubleshooting

- *The Setup page won't open / the address doesn't load.* Make sure your device is connected to the FieldCommand Wi-Fi network (default name `EMCOMM-NET`), and that you typed the full address including `http://` — for example `http://192.168.50.1`.
- *Save doesn't work / it says a field is required.* The **Organization Full Name** is required. Fill it in, then Save again. Every other field can be blank.
- *The Amateur Radio modules (APRS/Winlink/44Net/JS8Call) are grayed out and won't turn on.* That's expected when the **Club / Station Callsign** is blank. Enter a valid callsign in the Callsign & Identity section, Save, then return to Active Modules and enable them.
- *My organization name isn't showing on the dashboard/forms.* You may not have Saved. Re-open Setup, confirm the **Organization Full Name** is filled in, and click **Save**; watch for the green completed banner.
- *The map is centered in the wrong place.* Your **Latitude/Longitude** are blank or incorrect. Enter your decimal coordinates (remember the minus sign on Longitude for west), and Save.
- *Operators can't connect after I changed the Wi-Fi Name or Server Address.* Those must match the server's actual network settings. If in doubt, set them back to the defaults (`EMCOMM-NET` and `http://192.168.50.1`) and Save.


# 4. Member Roster & Quick Response (QR) code Check-In Codes

*The central personnel list — who your people are, what they can do, and how to check them in fast with a printed Quick Response (QR) code or a self-service arrival form.*

> **QUICK VERSION** — Open **Member Roster** from the dashboard. The **Directory** tab lists everyone; click **+ Add Member** to add a person, or click a card to edit them. Click the **QR** button on any card to show, print, or save that person's personal check-in code. The **Activation** tab is where you check people in during a real event — click a name to check them in, or use **+ Walk-In Check-In** for someone not on the list. Volunteers can also check themselves in from a phone using the field check-in page.


## What This Is / What It Is For

The **Member Roster** is FieldCommand's central list of people. It holds your regular members, occasional participants, and mutual-aid visitors, each with their identifiers, certifications, equipment, and contact details. It is worth setting up carefully because the rest of the system leans on it: net loggers pull names and callsigns from here, check-in is fastest when a person is already in the roster, and every member gets a personal **QR code** — a small square barcode — that lets them check in almost instantly at an activation.

Everything the roster stores lives on the server only. Phone numbers, emails, and emergency contacts are kept locally and are never sent anywhere outside your own system.

> **TWO KINDS OF "CHECK-IN" IN THIS CHAPTER** — There are two ways people get counted as present, and both are covered here. The **Activation tab** inside the roster is where an operator checks members in from the console. The **field check-in page** is a separate mobile-friendly form a volunteer opens on their own phone to sign themselves in. They feed the same purpose — an accurate list of who is on scene — from two directions.


## Opening the Roster

From the dashboard, tap the **👥 Member Roster** card (it appears in several modes). The roster opens with a top bar of controls and two tabs. The controls, left to right:

| Control | What it does |
| --- | --- |
| **🔍 Search box** | Filters the list as you type — matches name, callsign, radio ID, or member ID. |
| **+ Add Member** | Opens the blank Add Member form to enter a new person. |
| **📥 Import CSV ⓘ** | Bulk-loads members from a spreadsheet file. Hover the ⓘ for the exact column list. |
| **📤 Export CSV** | Downloads the whole roster as a spreadsheet file for backup or sharing. |
| **🖨 Print** | Prints the current roster view. |

Just below sit the two tabs: **📋 Directory** (the full member list, with a live count) and **✅ Activation** (the check-in board for an active event, also with a count). Click a tab to switch between them.

> _[Figure: The Member Roster Directory tab: search and action buttons across the top, the Directory/Activation tabs, and a grid of member cards]_


## Reading a Member Card

In the Directory tab, each person is a **card**. At a glance a card shows a round avatar with the person's first initial, their name, and a small blue badge for their license class if they have one. Below the name sit colored identifier badges and a row of small dots:

- **📻 (green)** — the person's amateur-radio callsign, if they have one
- **📡 (blue)** — their radio ID or unit number, for public service radio systems
- **🪪 (purple)** — their member ID, your group's own internal number
- **Colored dots** — a quick certification summary; a green dot means they hold that certification, a gray dot means they don't (hover a dot to see which certification it is)

On the right edge of each card is a **QR** button (covered below). Click anywhere else on the card to open that member for editing.


## The Three Identifiers

FieldCommand deliberately keeps three separate ID fields because a person can be known three different ways, and any one of them can be blank. Understanding the difference saves confusion later.

| Identifier | What it is | Example |
| --- | --- | --- |
| **Callsign** | An amateur-radio callsign issued by the Federal Communications Commission (FCC). Leave it blank for members who are not licensed hams. The club's shared callsign is your club callsign. | a personal callsign such as `KE4CON` |
| **Radio ID / Unit #** | The unit number a person is known by on a public service trunked or Project 25 (P25) radio system. Used by every kind of member, not just hams. | `Unit 412` |
| **Member ID** | Your organization's own internal membership number — the roster's primary way of telling people apart. This is the number a personal QR code is built from by default. | MEM-042 |

> **BLANK CALLSIGNS ARE EXPECTED** — Non-licensed volunteers are full members of the roster — they simply have no callsign. Leave that field empty. The roster, check-in, and resource tools all work fine for members with no callsign; only the amateur-radio net logging cares about it.


## Adding and Editing a Member

Click **+ Add Member** to open the member form, or click an existing card to edit that person. The form is grouped into labeled sections. You do not have to fill in everything — a name is enough to start.

| Section | Fields | Notes |
| --- | --- | --- |
| **Identifiers** | Callsign · Radio ID / Unit # · Member ID | Any combination; all three may be blank except you'll want at least one way to identify the person. |
| **Personal Info** | First Name · Last Name · License Class | License Class is a dropdown: Amateur Extra, General, Technician, Novice, Advanced, GMRS, or **No amateur license**. |
| **Contact** | Phone · Email · Address · Grid Square · Emergency Contact | Grid Square is a Maidenhead locator (a short code hams use for location). All stored locally only. |
| **Roles** | Net Control (NCS) · Operator · Liaison · Emergency Coordinator (EC) | Check every role that applies. Roles show as badges on the card. |
| **Certifications** | ICS-100/200/300/400/700/800 · EmComm I/II · CPR/AED · First Aid · CERT | Check what the person holds; these drive the green cert dots on the card. |
| **Equipment** | HF Radio · VHF/UHF · Digital · Packet · PACTOR Modem · VARA HF · VARA FM · APRS · Winlink · Go-Box · Generator · Battery/Solar · Vehicle Mount | Check the gear the member can bring, so you can find capabilities fast when tasking. |
| **Notes** | Free text | Anything else worth recording about the person. |

1. Click **+ Add Member** (or click a card to edit).
2. Fill in at least a name, plus whichever identifiers, certifications, and equipment apply.
3. Click **Save Member**. The person appears in the Directory immediately.
4. To remove someone, open their card and click the red **Delete** button, then confirm. Deleting a member does not erase past net-log or check-in history.


## Adding a Member Photo

Each member can have a **photo**. It shows in place of the plain initial avatar and, more usefully, it prints on the member's ID card (covered below). Adding a photo is optional, but a photo is what turns a plain roster entry into a real photo credential someone can wear.

The photo control lives in the member editor. Open a member's card (or start a new one with **+ Add Member**) and look for the **Take / upload photo** control near the top of the form.

1. Open the member in the editor and click **Take / upload photo**.
2. On a **computer**, this opens a file picker — choose a photo already saved on the device (a JPG or PNG image works fine).
3. On a **phone or tablet**, you're offered the choice to **take a new photo** with the camera or pick one from the device's photo library. To take one, allow the camera when asked, frame the person, and snap it.
4. The photo appears as a preview. FieldCommand automatically **shrinks (resizes)** it to a sensible size, so you don't need to worry about a huge image file — just pick or shoot the picture.
5. Click **Save Member**. The photo is now stored with that person and will appear on their ID card.

> **PHOTOS STAY ON YOUR SERVER** — Like everything else in the roster, a member's photo is kept on your own server only — it is never uploaded to the internet. To change a photo later, open the member and use the **Take / upload photo** control again; the new picture replaces the old one.

> **USING THE CAMERA NEEDS THE SECURE CONNECTION** — Taking a photo with a phone camera works only over FieldCommand's secure **HTTPS** connection (the padlock — see Chapter 2). If the camera won't open, make sure the address in your browser starts with `https://`. You can always **upload** an existing photo instead, which works on any connection.


## Bulk-Loading Members with CSV

If you already keep your membership in a spreadsheet, you can load everyone at once instead of typing them in. **CSV** stands for comma-separated values — a plain spreadsheet saved as simple text, which any spreadsheet program can produce with **Save As → CSV**.

Click **📥 Import CSV** and choose your file. The only required column is **member_id**; every other column is optional. Hovering the **ⓘ** next to the button shows the full list.

| Column | Required? | Meaning |
| --- | --- | --- |
| `member_id` | **Yes** | Your internal member number, for example MEM-042. Used to tell people apart. |
| `callsign` | No | Amateur-radio callsign; leave blank for non-ham members. |
| `radio_id` | No | Public Safety radio ID / unit number. |
| `first_name` / `last_name` | No | The person's name. |
| `role` or `roles` | No | One role, or several separated by semicolons. |
| `phone` · `email` · `grid` · `license_class` | No | Contact details, grid square, and license class. |

> **RE-IMPORTING IS SAFE** — Importing the same file again **updates** existing members rather than creating duplicates, because FieldCommand matches on the member ID (falling back to callsign or radio ID). Members already in the roster who are not in the file are left untouched. Use **📤 Export CSV** first to keep a backup before a big import.


## Personal QR Check-In Codes

Every member has a personal **QR code** — a small square barcode that a check-in operator can scan with a camera to sign the person in instantly, no typing. The **QR** button on each member card opens that person's code.

1. In the Directory, click the **QR** button on a member's card.
2. A window opens showing the person's name, their code, and the QR image. When the server has internet, a real scannable QR image is generated. When offline, the window instead shows the member's ID in large text as a manual-entry fallback — an operator can just type or read it.
3. Click **🖨 Print** for a clean printable sheet with the QR code, the member's name, and the check-in web address — good for ID badges or a check-in binder.
4. Click **💾 Save PNG** to download the code as an image the member can keep on their phone.

> **WHERE THE CODE GETS SCANNED** — These personal codes are read by FieldCommand's camera **Scan Check-In** page, which turns a phone or tablet camera into a check-in scanner (covered in its own chapter). By default a member's QR code is built from their member ID. If your group uses physical facility badges, the code can be set to match a badge number instead, so a badge swipe checks the person in.


## Printing Member ID Cards

FieldCommand can print proper **member ID cards** — the kind of photo credential a volunteer clips to a lanyard. Each card is two-sided and sized to slip into a standard badge holder or to laminate, and it pulls everything it needs from the roster and from your Setup branding, so the cards come out correct for your own organization automatically.

There are two ways to print them. To print a stack for the whole group, use the **🪪 Print ID Cards** button at the top of the roster. To print just one person's card, open that member in the editor and click the **ID Card** button there.


### What's on the card

Each card has a **front** and a **back**:

| Side | What it shows |
| --- | --- |
| **Front** | The member's **photo**, their **name**, their identifiers (**callsign**, **member ID**, and **radio ID** — whichever they have), and a scannable **QR code** so the card itself works as a check-in badge. |
| **Back** | The **Wi-Fi network name** and **dashboard address** so the member can get connected, plus the **Wi-Fi password** if you entered one in Setup. All of this comes from your Setup screen (Chapter 3). |

> **THE CARD BACK COMES FROM SETUP** — The access details on the back of the card — Wi-Fi name, Wi-Fi password, and dashboard address — are taken straight from the **System & Network** section of Setup (Chapter 3). If you left the **Wi-Fi Password** field blank there, the back simply omits the password. Fill it in if you want members to be able to join without asking, or leave it out if you'd rather the password not travel around on printed cards.


### Who gets a card

A card is built around a photo, so the rule is simple: a person can have a card once they have a **photo** on file.

- **Regular members** get cards — add each person's photo (above), then print.
- **Walk-ins and mutual-aid visitors** get a card **only if they have a photo**. Most won't, since they're often added quickly with just a name; that's fine — they simply won't have a card printed.
- A member with **no photo** is skipped when printing cards, because a photo credential with no face on it isn't much of a credential.

1. Make sure the members you want cards for have **photos** added.
2. On the roster, click **🪪 Print ID Cards** (or, for a single person, open their editor and click **ID Card**).
3. Your browser's print window opens, showing the laminate-ready cards laid out two-sided. Print them on card stock or regular paper.
4. Cut them out and laminate or slot them into badge holders. Because the front carries a QR code, a finished card doubles as the member's check-in badge.

> **A CARD IS ALSO A CHECK-IN BADGE** — The QR code on the front of the card is the member's personal check-in code. That means at an event you can scan the card itself to sign the person in (Chapter 10) — no separate printout needed. One card handles identity, network access, and check-in all at once.

> **PAIR A HANDHELD SCANNER FOR THE FASTEST TABLE** — At a staffed check-in table, the quickest way to read these cards is an inexpensive **USB or Bluetooth 2D barcode scanner** — the handheld kind stores use. Plug it in (or pair it over Bluetooth) to the check-in device; it acts just like a keyboard, so there's nothing to install. Point it at the card's QR code and it types the code straight into the check-in box for you. This works on any device and is covered in full in Chapter 10.


## The Activation Tab — Checking People In

During a real event, switch to the **✅ Activation** tab. This is the operator's check-in board, and it shows two side-by-side columns: **Roster — Click to Check In** on the left (everyone you can check in) and **Activated Personnel** on the right (everyone currently signed in, with a live count).

1. Use the **Search member to check in…** box to find a person quickly.
2. Click a person's row (or their **Check In** button) on the left. You'll be asked for an **assignment** — type where they're going or what they're doing, or leave it blank.
3. The person moves to the **Activated Personnel** list on the right, marked **Active**.
4. Change anyone's status any time using the dropdown next to their name: **Active**, **Standby**, or **Released**. Releasing someone drops them from the active count.
5. Click **📤 Export Log** to download the activation log as a CSV for the incident record.

> **STATUS MEANINGS** — **Active** = on scene and working. **Standby** = present but not currently assigned. **Released** = done and signed out. The count at the top of the tab reflects everyone who is Active or on Standby — released people no longer count as present.


## Walk-In Check-In

Not everyone who shows up will be in your roster — mutual-aid responders and first-time volunteers arrive unannounced. Click **+ Walk-In Check-In** on the Activation tab to sign one in without adding them to the permanent roster first.

1. Click **+ Walk-In Check-In**.
2. Enter what you know: **Callsign or Radio ID**, **Name**, **Organization**, and **Assignment**. A callsign or a name is enough.
3. Click **Check In Walk-In**. The person appears in Activated Personnel with an amber **WALK-IN** badge so it's clear they're a guest.
4. If the walk-in turns out to be a keeper, click the **+ Roster** button next to their name to save them into the permanent roster.


## The Field Check-In Page

FieldCommand also has a mobile-friendly **Incident Check-In** page that volunteers fill in themselves on their own phones when they arrive — useful when a line forms and one operator can't keep up. It is opened from a link tied to a specific incident (often shared as a QR code or a bookmark at the check-in table), and it is built to be big-buttoned and easy to thumb through on a phone.

At the top it shows which **incident**, **operational period** (the current work shift), and **check-in location** the form is for, so the volunteer knows they're signing into the right event. Then it collects:

| Field | What the volunteer enters |
| --- | --- |
| **Full Name** *(required)* | Their name — the only required field. |
| **Callsign / Radio ID / Badge #** | Any identifier they have. |
| **Agency / Home Unit** | Who they came from. |
| **ICS Position / Role** | Picked from a grouped menu of standard ICS roles (Command, Operations, Planning, Logistics, Finance, and field roles). |
| **Resource Type** | What kind of resource they are — Personnel, Vehicle, Amateur Radio, Medical Unit, and so on. |
| **Equipment / Vehicle** | Any gear or vehicle they bring, if relevant. |
| **Notes** | Anything the check-in recorder should know. |

When they tap **✓ Check In**, they get a big green **Check-In Complete** confirmation with the time, and a button to **Check In Another Person** for the next in line. Their entry flows straight into the incident's **ICS-211** check-in list and the T-card board at the command post. Lower on the same page, an operator sees a live **Currently Checked In** list with a **Check Out** button next to each person for when they leave.

> **THE FIELD PAGE NEEDS AN INCIDENT** — The field check-in page only works when opened through its incident link — that is how it knows which incident to file people under. If it opens with a "No incident specified" warning and a disabled button, the link is missing the incident information; get a fresh link from the console. And as always, the device must be connected to **EMCOMM-NET** to reach the server.


## Troubleshooting

- *The roster says "Cannot reach API" and no members load.* The page can't reach the server. Confirm your device is connected to **EMCOMM-NET** and the server is running, then reload the page.
- *A CSV import didn't add anyone.* Every row needs a **member_id** value, and the first line of the file must be the column headers. Rows with no member ID, callsign, and name are skipped. Fix the file and import again.
- *Re-importing created duplicate people.* Duplicates happen only when the matching identifier changed between imports. Keep the **member_id** consistent for each person across imports and re-imports will update rather than duplicate.
- *The QR window shows a plain code instead of a scannable square.* That's the offline fallback — the scannable image needs internet to generate. The code shown is still valid; an operator can type it in manually at check-in, or reconnect the server to the internet to get the image.
- *I checked someone in twice by accident.* The system blocks a second active check-in for the same member and warns "Member already checked in." If a duplicate slipped in as a walk-in, set the extra one to **Released**.
- *A walk-in I saved to the roster is missing details.* Saving a walk-in creates a minimal record from what was entered at check-in. Open the new card in the Directory and fill in the rest.
- *The field check-in page won't submit / says it can't reach the server.* The device isn't on EMCOMM-NET, or the incident link is incomplete. Reconnect to EMCOMM-NET (address range 192.168.50.x) and use a fresh incident link from the console.


# 5. Incident Management — Creating and Managing Incidents

*How to create an incident, work inside it, advance operational periods, and — when it's over — archive the permanent record to a USB drive.*

> **QUICK VERSION** — Open **Incident Management** from the dashboard and click **+ New Incident**. Give it a **name** and pick a **type** (those two are required), then click **CREATE INCIDENT**. The incident opens and becomes your workspace — click any ICS form button to fill it out, click **⏭ Next Period** to roll to the next shift, and **✕ Close Incident** when it's done. Nothing is ever thrown away by accident: everything you type is saved, and a finished incident can be archived to a USB drive as a permanent record.


## What This Is / What It Is For

Everything you do in the Incident Command System (ICS) side of FieldCommand happens **inside an incident**. An incident is the container that holds all of one activation's paperwork: its ICS forms, its resource T-cards, its personnel check-ins, its cost tracking, its meetings, and its net-log associations. When you create an incident, you are opening a fresh, empty folder for one event; when you fill out a form or check someone in, that record drops into the folder for that incident and stays there.

You can have several incidents in the system at the same time — a real activation, last month's exercise, and a drill you're prepping — and they never mix. Each one keeps its own separate pile of records.

> **INCIDENTS ARE PERMANENT RECORDS** — FieldCommand treats an incident as a legal record of what happened. Everything you enter is **saved automatically** and kept. Closing an incident does not erase it. Even deleting one is a deliberate, guarded action — the normal end-of-incident step is to **archive** the whole package to a USB drive so you have it forever. Assume anything you type into an incident is on the record.


## The Two Incident Management Screens

FieldCommand has two screens that both carry the name **Incident Management**. They do different jobs, and it helps to know which is which:

| Screen | What it's for | How you get there |
| --- | --- | --- |
| **Incident workspace** (`incident.html`) | Create incidents, and work inside one — open ICS forms, advance the operational period, close the incident | The **+ New Incident** / incident links on the dashboard |
| **Incident data screen** (`incident_mgmt.html`) | Housekeeping — archive a finished incident to USB, restore one, delete from the Pi, or run the Beta Reset | The red **DATA** tile / Incident Management (Archive · Restore · Delete) link |

This chapter walks the workspace first (the everyday screen), then the data screen (the once-per-incident cleanup screen).


## Creating an Incident

On the workspace screen, the header shows an **ICS** badge, the words **INCIDENT MANAGEMENT**, and a blue **+ New Incident** button at the right. The page is split in two: a left column listing **Active Incidents** and **Closed Incidents**, and a large right-hand **workspace** area. Before you pick anything, the workspace shows a **NO INCIDENT SELECTED** placeholder with a **+ Create New Incident** button.

1. Click **+ New Incident** (top right) or the **+ Create New Incident** button in the empty workspace.
2. The **📋 CREATE NEW INCIDENT** box opens. Fill in the fields below — only **Incident Name** and **Incident Type** are required (both marked with a *).
3. Click **CREATE INCIDENT**. The box closes, the incident appears in the Active Incidents list, and it opens in the workspace as the incident you're now working in.
4. Changed your mind? Click **Cancel** instead — nothing is created.

> _[Figure: The CREATE NEW INCIDENT modal with the name, type dropdown, jurisdiction, and variant fields]_

| Field | What to type | Notes |
| --- | --- | --- |
| **Incident Name** *(required)* | A plain name for the activation | May be pre-filled from the **Default Incident Name** you set in Setup (Chapter 3). Example: `your county Winter Storm Response 2026`. |
| **Incident Number** | Your agency's tracking number, if it assigns one | Optional — leave blank if you don't use one. Example: `2026-0142`. |
| **Incident Type** *(required)* | Pick the closest match from the dropdown | Grouped into seven categories — see the table below. |
| **Jurisdiction** | The area or authority in charge | May be pre-filled from your Setup location (e.g. `your county, your state`). |
| **Incident Location / Address** | Where the incident is | A street address or GPS coordinates. |
| **Incident Commander** | The person in charge | Start typing to pick a roster member, or type any name or callsign for someone not on the roster. See Unified Command below. |
| **Operational Period Duration** | How long each shift block runs | **12 hours (standard)**, or 8, 24, or 6. This just sets the default length; you can advance a period whenever you like. |
| **ICS Form Variant** | Which flavor of ICS forms to use | **FEMA**, **USCG**, or **NWCG** pills. Defaults to your Setup choice; changeable per form later. |
| **Initial Situation Summary** | A few sentences on what's happening | Optional. Shows on the incident header once created. |


## Single Incident Commander vs. Unified Command

ICS runs under one of two command structures, and FieldCommand handles both the same way — the difference is how you fill in the **Incident Commander** field, not a software setting.

| Structure | When it's used | What to type in the IC field |
| --- | --- | --- |
| **Single Incident Commander (IC)** | One agency or jurisdiction clearly has authority — the common case for a single-organization activation | The IC's name or callsign. The ICS-203 organization chart shows one IC at the top. |
| **Unified Command (UC)** | Two or more agencies share command — multi-agency responses, complex disasters, or incidents crossing boundaries. All agencies still work from one Incident Action Plan (IAP) | Type `Unified Command` or the UC group name. List each participating agency's commander on the ICS-203 under the Unified Command section. |

> **UNIFIED COMMAND CHANGES NOTHING UNDER THE HOOD** — Every ICS form, T-card, and cost record works identically whether you run Single IC or Unified Command. UC is a labeling and documentation convention inside the same incident record — there is no separate mode to turn on.


## Incident Types

The **Incident Type** dropdown is long — about 32 choices grouped into seven categories. The type only labels the incident throughout the interface (it shows as a small badge next to the incident name). All types use the exact same ICS form set, so if none fits perfectly, pick the nearest one — you are not locking anything out.

| Category | Example types |
| --- | --- |
| Natural Hazards | Winter Storm, Flooding, Tornado / Severe Weather, Earthquake, Wildfire, Heat Emergency, Drought |
| Technological | Hazmat / Chemical Spill, Transportation Accident, Structure Fire, Power Outage / Infrastructure, Dam Failure, Nuclear / Radiological |
| Human-Caused | Mass Casualty Incident, Active Threat, Civil Disturbance, Terrorism |
| Search & Rescue | Wilderness, Urban, Water, Missing Person — Dementia / Memory, Missing Person — Child |
| Public Health | Disease Outbreak / Pandemic, Mass Casualty — Medical, Public Health Emergency |
| Planned Events | Planned Event — Public Safety, Planned Event — EMCOMM Exercise, Drill / Training Exercise |
| Other | Mutual Aid Request, EOC Activation, Other / All-Hazards |


## Working Inside an Incident

Click any incident in the left-hand list to open it in the workspace. At the top you get an **incident header** showing the name, the type badge, the location, the jurisdiction, the Incident Commander, and the start time (stamped in Coordinated Universal Time, UTC). If you typed a situation summary, it shows here too. To its right sit three buttons on an active incident: **⏭ Next Period**, **✏ Edit**, and a red **✕ Close Incident**.

Below that is the **operational period bar** — a strip showing **OP 1** (the current period number) with two links on the right: a gold **📋 GENERAL INFO** button and a **📄 Export IAP** button.

> **FILL IN GENERAL INFO FIRST** — The **📋 GENERAL INFO** screen is the one place you type the incident name, dates, commander, and section chiefs — and it auto-fills those values into every ICS form for that period. Do it once at the start of each period and you save yourself re-typing the same header on 20-plus forms. General Info is covered in Chapter 15.


### The ICS Form Grid

The bulk of the workspace is a grid of form buttons, grouped by ICS section with a colored divider for each: **COMMAND**, **OPERATIONS**, **PLANNING**, **LOGISTICS**, **FINANCE / ADMIN**, and **COMMUNICATIONS UNIT**. Each button shows the form number (like **ICS-204**), its name, and which variants it supports. Click one to open and fill it out; forms save automatically. The line above the grid shows the current **Variant** in gold with a **Change →** link if you need a different one for this incident.

| Section divider | Forms you'll find there |
| --- | --- |
| COMMAND | ICS-201 Incident Briefing, 202 Objectives, 207 Organization Chart, 208 Safety Message/Plan |
| OPERATIONS | ICS-204 Assignment List, 211 Check-In List, 219 Resource Status (T-Cards), 210 Resource Status Change |
| PLANNING | ICS-203 Organization Assignment, 209 Incident Status Summary, 215 Operational Planning Worksheet, 215A IAP Safety Analysis — plus a **📅 Meeting Scheduler** link (Chapter 6) |
| LOGISTICS | ICS-205 Radio Communications Plan, 205A Communications List, 206 Medical Plan, 213RR Resource Request |
| FINANCE / ADMIN | ICS-214 Activity Log, 220 Air Operations Summary, 221 Demobilization Check-Out |
| COMMUNICATIONS UNIT | ICS-213 General Message, 309 Communications Log |

At the very bottom is a **📜 ACTIVITY LOG** feed — a running list of what's been done on this incident, newest at the top, so you can see at a glance who touched what and when.


## Advancing Operational Periods

ICS breaks work into **operational periods** — usually 12- or 24-hour shift blocks. FieldCommand tracks the current period and uses it as the default for new forms, T-cards, and check-ins. To move to the next one:

1. Click **⏭ Next Period** in the incident header.
2. The **⏭ ADVANCE OPERATIONAL PERIOD** box opens. In the **Objectives carried forward** field, list what should continue into the next period (optional).
3. Click **Advance Period**. The period counter ticks up (OP 1 becomes OP 2), and the prior period's data is kept and stays viewable.


## Closing an Incident

When the activation is over, click the red **✕ Close Incident** button. FieldCommand asks you to confirm (it warns that closing cannot be undone). Once closed, the incident drops from **Active Incidents** into the **Closed Incidents** list on the left, and its buttons go away — but all its data is still there and fully readable. Closing is about marking the incident finished, not deleting it.


## The Incident Data Screen — Scenario Mode, Archive, Restore, Delete

The second Incident Management screen (the red **DATA** page) is where you handle a finished incident's long-term fate. Across the top a **USB Backup Drive** status strip tells you whether a backup drive is connected — it must be a drive labelled **FIELDCOMMAND** (all caps). Below that the page lists incidents in three groups: **Active Incidents**, **Archived on Pi SSD — awaiting deletion**, and **Archives on USB Backup Drive**.


### Scenario / Training Mode

Any incident can be flagged as a training scenario. On the data screen, each active incident has a **🧪 Mark Scenario** button (it reads **✓ Scenario** once set). Scenario incidents wear a yellow **🧪 SCENARIO** badge everywhere in the interface, so operators always know they're in a drill and not the real thing. You can also tick the scenario box when activating an Event Template (Chapter 6).


### Beta Reset — Wiping Practice Data

> **BETA RESET DELETES ALL INCIDENT DATA** — The red **⚠ BETA / SCENARIO RESET** zone wipes **every** incident from the Pi — incidents, ICS forms, FEMA cost entries, check-ins, T-cards, meetings, and resource history. It **preserves** your roster, hospitals, channel library, resource types, repeaters, and net-logger entries, and it does not touch system configuration. It is meant to hand you a clean system after an exercise. To run it you must type **RESET** in the box and click **🗑 Reset All Scenario Data**, then confirm. There is no undo from this screen — **archive any real incident first**.


### Archive, Restore, and Delete

The normal end-of-incident routine is: archive to USB, confirm the backup, then (optionally) delete from the Pi to free space. Each active incident card carries a **💾 Archive to USB Backup Drive** button and a **Delete** button; restore is offered on the USB archive cards.

| Action | What it does | Reversible? |
| --- | --- | --- |
| **💾 Archive to USB** | Writes a complete package (all forms, T-cards, check-ins, costs, net-log links) to the FIELDCOMMAND drive. The incident then also appears under **Archived on Pi SSD — awaiting deletion**. | Yes — restore any time |
| **↩ Restore to Pi** | Reads an archive back off the USB drive and re-inserts all its data, returning the incident to active status | Yes |
| **Delete from Pi** | Permanently removes the incident and its data from the Pi. Do this only after confirming the archive is on USB. | No — permanent |

> **ABOUT THE USB BACKUP DRIVE** — The drive must be labelled **FIELDCOMMAND** (all caps) — any drive with that label is recognized automatically and the status strip turns green. If the strip is amber/red, the **Archive to USB** buttons stay disabled until you plug the drive in. A rugged 1 TB USB-C drive is a good choice for field use.


## Troubleshooting

- *The incident list says "ICS platform offline" or won't load.* The workspace talks to the incident service on the Pi. Confirm you're on the FieldCommand Wi-Fi and can reach the dashboard; if other pages work but this one doesn't, the incident service may still be starting — wait a moment and reload.
- *I clicked CREATE INCIDENT and nothing happened.* Both **Incident Name** and **Incident Type** are required. If either is blank, FieldCommand pops a reminder and won't create the incident. Fill both in and try again.
- *The incident name or dates aren't showing on my ICS forms.* Fill in the **📋 GENERAL INFO** screen for that operational period — that's what feeds the header onto every form. See Chapter 15.
- *The 💾 Archive to USB button is grayed out.* No backup drive is detected. Plug in a USB drive labelled **FIELDCOMMAND** (all caps) and wait for the status strip at the top to turn green, then try again.
- *I closed an incident by mistake.* Nothing is lost — a closed incident keeps all its data and moves to the **Closed Incidents** list. Re-open it from there to review it. (Re-activating is not done from this screen; restore from a USB archive if you need it fully active again.)
- *I want to clear out practice incidents but keep my roster and channels.* Use the **Beta Reset** on the data screen. It wipes incident data only and preserves the roster, hospitals, channel library, resource types, repeaters, and net-logger entries. Archive any real incident to USB first.
- *I deleted an incident and need it back.* If you had archived it to USB, open the data screen and click **↩ Restore to Pi** on its archive card. If it was never archived, a hard delete is permanent.


# 6. Pre-Planned Event Templates

*Ready-made incident setups you can drop in place in seconds — plus the Meeting Scheduler that plans ICS meetings and prints agendas.*

> **QUICK VERSION** — Open **Event Templates** from the dashboard. On the **⚡ Activate** tab, click a template card (like **Shelter Activation**), type an **Incident Name**, and click **⚡ Activate Template**. FieldCommand instantly creates a new incident already loaded with objectives, resource T-cards, radio channels, and an org chart from that template. To change what a template contains, use the **✏ Manage Templates** tab. Nothing about a template is locked — every value stays editable after you activate it.


## What This Is / What It Is For

An **event template** is a pre-built incident setup you save ahead of time and drop in when an activation starts. Instead of creating a blank incident and typing objectives, adding resources, and entering radio channels by hand every time, you activate a template and all of that appears at once — pre-filled and ready to edit.

Templates are ideal for the incident types you handle again and again: a shelter opening, a search callout, a severe-weather activation. You set them up once — with your local objectives, your usual resource list, and your standard channels — and from then on a two-click activation gives every operator the same consistent starting point. Think of a template as a rubber stamp for a whole incident.

> **A TEMPLATE IS A STARTING POINT, NOT A CAGE** — Activating a template creates a normal incident. Everything it filled in — objectives, resources, channels, org chart — is fully editable afterward, exactly as if you'd typed it yourself. The template just spares you the typing.


## Opening Event Templates — the Two Tabs

The **Event Templates** page opens with a **PLAN** badge and two tabs across the top:

| Tab | What it's for |
| --- | --- |
| **⚡ Activate** | Browse the template gallery and turn a template into a live incident. This is the everyday tab. |
| **✏ Manage Templates** | Create, edit, reorder, delete, export, and import templates. This is where you tailor them to your group. |

The header also carries a **+ New Template** button, a **📥 Import JSON** button, and an **📤 Export All** button (covered further down), plus the **← Dashboard** link.


## The Built-In Templates

FieldCommand ships with six built-in templates covering the most common incident types. Each appears as a card in the Activate gallery showing an icon, a name, a short description, and a count of its objectives, resources, and channels. A small **built-in** tag marks the ones that came with the system. Use any of them as-is, or edit them to match your local protocols.

| Template | What it pre-loads |
| --- | --- |
| **Shelter Activation** | Shelter-management objectives, cot and supply resource types, registration and medical channels, your served agency coordination section |
| **Search & Rescue** | Search-and-rescue objectives, field-team and K9 resource types, search-sector channels, base-camp and medical branches |
| **Severe Weather** | Damage-assessment objectives, utility and debris resource types, shelter and Emergency Operations Center (EOC) coordination channels, public-information branch |
| **Mass Gathering / Event** | Crowd-management objectives, medical and security resource types, venue and dispatch channels, medical and operations branches |
| **HazMat / Spill** | Decontamination and zoning objectives, HazMat-team resource types, hot/warm/cold-zone channels, safety-officer emphasis |
| **Planned Exercise / Drill** | Training objectives, evaluator and observer resource types, an exercise-control channel, and it is pre-tagged as a scenario (🧪) |


## Activating a Template

Activating is a two-step flow on the **⚡ Activate** tab: pick a template, then fill in the few details that are unique to this run.

1. On the **⚡ Activate** tab, click the card for the template you want. The page switches to a configuration view with a **← Back** button and the template name at the top.
2. Fill in the **Incident Details** — see the table below. **Incident Name** is the only required field.
3. Check the **What Will Be Created** preview — it lists the exact objectives, safety message, resources, and channels the template will drop in, so there are no surprises.
4. Click the big blue **⚡ Activate Template** button. FieldCommand creates the incident and builds its ICS-202, ICS-203, ICS-205, and resource T-cards from the template.
5. When it finishes, a green success line appears with quick links — **→ ICS-202**, **→ ICS-203**, **→ ICS-205**, **→ T-Cards**, and **→ Dashboard**. Click one to jump straight to that piece. The page does **not** navigate there on its own, so you land wherever you choose.

> _[Figure: The template configuration view with the Incident Details form and the What Will Be Created preview]_

| Field | What to type | Notes |
| --- | --- | --- |
| **Incident Name** *(required)* | A name for this activation | Example: `Shelter Alpha — Lincoln School` |
| **Incident Commander** | Who's in charge, or `TBD` | Optional |
| **Location / Facility** | Where the incident is | Optional |
| **Jurisdiction** | The area or authority | Optional |
| **Op Period Start / End** | Start and end of the first operational period | Pre-filled to now and 12 hours out; adjust as needed |
| **Mark as training scenario 🧪** | Tick this for a drill | A scenario incident is safe to wipe later with the Beta Reset (Chapter 5). Some templates, like Planned Exercise / Drill, default this on. |

> **CHANNEL FREQUENCIES ARE PLACEHOLDERS** — A template's radio channels come in with names and functions, but you should confirm the actual frequencies for your area on the ICS-205 Radio Communications Plan after activating. The preview reminds you of this.


## Creating and Editing Templates

The **✏ Manage Templates** tab lists every template with **✏ Edit**, **📤** (export), and **⚡ Activate** buttons. To build a new one, click **+ New Template** in the header; to change an existing one, click its **✏ Edit** button. Either way the template editor opens — a single scrolling form divided into sections.

| Editor section | What you set |
| --- | --- |
| **Basic info** | **Template Name** (required), **Incident Type Label**, **Icon** (an emoji), **Sort Order** (controls its place in the gallery), and a **Summary** shown on the card |
| **ICS-202 Objectives** | The list of incident objectives. Click **+ Add Objective** to add a line, the **✕** to remove one; they renumber automatically. |
| **ICS-202 Safety Message** | A default safety message that lands on the ICS-202 |
| **Pre-loaded Resources** | The T-cards to create. Each row has a **Name**, a **Type** (Personnel, Crew, Engine, Vehicle, Equipment, Helicopter, Other), and a **Qty**. Click **+ Add** for more. |
| **ICS-205 Default Channels** | The radio channels. Each row: **Channel Name**, **RX Freq**, **TX Freq**, **Tone**, **Mode** (FM/NFM/AM/USB/LSB/DIG), and **Function** (Command/Tactical/Medical/Logistics/Liaison/Other) |
| **ICS-203 Default Org** | Default org-chart positions — Ops Section Chief, Safety Officer, Public Info Officer, a Branch I label, and Division A–D labels |
| **Scenario default** | A checkbox to make every incident from this template default to a training scenario 🧪 |

1. Make your changes in any section — edits are live in the form.
2. Click **SAVE TEMPLATE** at the bottom. The template list refreshes with your changes.
3. To remove a custom template, open it and click **Delete**. Built-in templates can be edited but **not** deleted — the Delete button is hidden for them, and their edits are kept safe and won't be overwritten by system updates.


## Sharing Templates — Export and Import

Templates travel as plain JSON files, so you can hand a polished template to another FieldCommand system or keep a backup.

- *Export one template.* Click the **📤 Export JSON** button inside the editor, or the **📤** button on its row in Manage Templates. A `.json` file downloads.
- *Export everything.* Click **📤 Export All** in the header to download all your templates in one file, named with today's date.
- *Import.* Click **📥 Import JSON** in the header and pick a template file. FieldCommand adds the templates and tells you how many it imported.


## The Meeting Scheduler

Reached from the **📅 Meeting Scheduler** link in an incident's Planning section (Chapter 5), the Meeting Scheduler plans the standard ICS meetings for an incident, tracks who must attend, prints agendas, and records minutes. It is tied to whichever incident you opened it from — the incident name shows in the header.


### The Planning-P Strip

Across the top runs the **Planning-P strip** — the recognized cycle of ICS meetings shown left to right with arrows: **Incident Briefing → Tactics Meeting → Planning Meeting → Ops Briefing → Agency Reps → Command Staff**. Each step shows its scheduled time and lights up when a meeting of that type exists (blue for scheduled, and it marks as done once completed). Click a step to jump to that meeting.


### Scheduling a Meeting

1. Click **+ Schedule Meeting**. The **📅 SCHEDULE MEETING** box opens.
2. Pick a **Meeting Type** from the grouped dropdown (Planning-P cycle meetings, Public Information meetings, Operational briefings, or Other). FieldCommand auto-fills a title, a suggested **Chair / Facilitator**, the **Required Attendees** by ICS position, and a starter **Agenda** for that meeting type.
3. Set the **Date & Time** and **Operational Period**, and optionally a **Location / Room**.
4. Adjust attendees — tick or untick required positions and type in the assigned person's name; add anyone else under **Additional / Optional Attendees**. Edit or add **Agenda Items** (each with a duration) as needed.
5. Click **SAVE MEETING**. It appears in the list, grouped by operational period.

| Meeting type group | Examples |
| --- | --- |
| Planning P Cycle | Incident Briefing (ICS-201), Tactics Meeting, Planning Meeting, Operations Briefing, Agency Representative Meeting, Command Staff Meeting |
| Public Information | JIC Coordination Meeting, Media Briefing / Press Conference, Community Information Meeting, Social Media Coordination |
| Operational | Shift Briefing, Resource / Logistics Briefing, Finance / Admin Briefing, Demobilization Briefing |
| Other | Training / Drill, Hot Wash / After Action, Other Meeting |

Each meeting card shows the time, location, chair, status, and attendee chips (required attendees are outlined in amber). The card's buttons are **✏ Edit**, **📝 Minutes**, **🖨 Print Agenda**, and **✕** to delete.


### Minutes and Printing

Click **📝 Minutes** on a meeting to record decisions and action items, and to set its status to **Scheduled**, **Completed**, or **Cancelled**. Click **🖨 Print Agenda** to open a clean, printable agenda page: it lists the meeting details, a required-attendees table with a **Present** column to check off, an optional-attendees table, the numbered agenda with durations and a total-time line, and any minutes already recorded — ready to print or hand out.

> **MEETINGS ARE PART OF THE INCIDENT RECORD** — Like everything else on the ICS side, scheduled meetings, attendees, agendas, and minutes are saved with the incident and archived along with it. They are a permanent part of the activation's documentation.


## Troubleshooting

- *The template gallery is empty or shows an error.* The template list comes from the incident service on the Pi. Confirm you're connected to the FieldCommand Wi-Fi and the dashboard loads; if the service is still starting, wait a moment and reload the page.
- *I clicked Activate Template and it wouldn't proceed.* **Incident Name** is required on the configuration view. Type a name, then click **⚡ Activate Template** again.
- *After activating, I'm still on the templates page.* That's on purpose — activation shows success links (→ ICS-202, → T-Cards, → Dashboard, and so on) and lets you choose where to go instead of jumping automatically. Click whichever link you want.
- *The Delete button is missing on a template.* It's a **built-in** template. Built-ins can be edited but not deleted. If you don't want it in the gallery, lower its priority with a high **Sort Order**, or create your own alongside it.
- *My template's radio frequencies are blank on the ICS-205.* Templates seed channel names and functions but you confirm the actual frequencies per activation. Open the ICS-205 and fill them in for your area.
- *Import failed with an invalid-JSON message.* The file you picked isn't a valid FieldCommand template export. Re-export it from the source system with **📤 Export JSON** or **📤 Export All**, then import that file.
- *The Meeting Scheduler says no incident is selected.* Open it from inside an incident (the **📅 Meeting Scheduler** link in the Planning section), not directly — it needs to know which incident the meetings belong to.


# 7. Amateur Radio Net Control Logger

*The live digital net log — check stations in and out, record traffic, run a check-in timer, and print an ICS-309 communications log when the net closes.*

> **QUICK VERSION** — Open **Net Control** from the dashboard. Click **+ New Net**, give it a name and frequency, and **Create Net**. As stations call in, type each **callsign** — the name fills in by itself — and press **Enter** to log them. Click **Check Out** when a station leaves. When you're done, click **Close Net**, then **📄 ICS-309** to print the official communications log.


## What This Is / What It Is For

The **Amateur Radio Net Control Logger** is the live, on-screen replacement for the paper net log that a net control station (the operator running the net) has always kept by hand. It is built for licensed amateur-radio nets — Amateur Radio Emergency Service (ARES), Radio Amateur Civil Emergency Service (RACES), Auxiliary Communications (AUXCOMM), SKYWARN weather nets, traffic nets, and training nets. As each station calls in, you type their callsign and the page records who checked in, when, from where, and for how long. Everything you log rolls straight into a printable **ICS-309 Communications Log** — the standard Incident Command System (ICS) form for radio activity — so there is no recopying at the end of the night.

The whole point is to make logging a net faster and cleaner than pencil and paper, while producing paperwork that a served agency or Emergency Operations Center (EOC) will accept without you having to type it a second time. It also keeps a running clock on how long each operator was on the net, which matters when volunteer hours have to be documented for reimbursement or credit.

> **YOU CAN RUN MORE THAN ONE NET AT ONCE** — FieldCommand keeps every net you open as a separate **tab** across the top of the page. That lets one station log a VHF (Very High Frequency) net and an HF (High Frequency) net side by side, or keep last week's closed net around for reference, without mixing their check-ins together.


## Opening the Net Control Logger

1. On a device connected to the FieldCommand Wi-Fi, open the dashboard (default **http://192.168.50.1**).
2. Click **Net Control** (the 📻 NET CONTROL logger).
3. The Net Control Logger opens. Across the top you'll see the navigation bar, then a **NET TABS** strip, and below that a two-column layout: the working area on the left and a summary sidebar on the right.

> _[Figure: The Net Control Logger with the NET TABS strip, the main logging column, and the NET SUMMARY sidebar]_

Before you create or select a net, most of the screen is quiet: the header reads **No Net Selected**, and the working area says *Select a net to begin logging*. That is normal — you pick a net first, and the form and lists wake up.


## Creating a New Net

Click the green **+ New Net** button at the left of the NET TABS strip. A **Create New Net** box pops up. Fill it in:

| Field | What to type | Notes |
| --- | --- | --- |
| **Net Name** | A plain name for the net (example: `Thursday Evening Net`) | Required — this is the only field you must fill in. |
| **Net Type** | Pick from the list: ARES Net, RACES Net, SKYWARN Net, EmComm Net, Traffic Net, Training Net, HF Net, VHF/UHF Net, or Digital Net | Labels the net; also prints on the ICS-309. |
| **Frequency / Mode** | The working frequency (example: `146.520 FM`) | You can type it, or click **📡 Pick** to choose from your saved channels (the ICS-205 / Channel Library). |
| **Mode** | Operating mode — SSB, FM, AM, CW, Digital, FT8, Winlink, or Other | Optional. |
| **Opened** (date/time) | When the net opened | Optional. **Leave it blank to mean *right now*.** Fill it in only to back-date a net that already started before you opened the logger. |
| **Net Control Callsign** | The callsign of the station running the net (example: `your club callsign`) | Optional. |

1. Type at least a **Net Name**.
2. Click **Create Net**.
3. The net becomes active, a tab for it appears in the NET TABS strip, and a live **elapsed-time clock** starts ticking in the header. The check-in form is now ready.

> **THE 📡 PICK BUTTON SAVES TYPING FREQUENCIES** — If you've set up a Channel Library or an ICS-205 Communications Plan for the incident, the **📡 Pick** button next to the frequency field lets you choose a channel by name — its frequency, mode, and tone fill in for you, so you don't fat-finger a frequency at 0200.


## The Net Header — Reading the Net at a Glance

Once a net is selected, the header panel at the top of the working column shows the net's vital signs:

- **Net name** in large type, with the **type · mode · net ID** underneath.
- **Opened** — the time the net started.
- **Closed** — the time it closed, or *Net open* while it's still running.
- **Duration** — a live count of how long the net has been open, updating every second.
- A **Drill Mode** checkbox and, while the net is open, a red **Close Net** button.


## Logging a Check-In

This is the heart of the page. When a station calls in, you work the **Log Station Check-In / Traffic** form. The fastest path is: type the callsign, glance at the auto-filled name, press **Enter**. Here is every field:

| Field | What it's for |
| --- | --- |
| **Callsign** | The station's callsign. Type it and it forces itself to uppercase. This is the only field you truly need. |
| **Name** | The operator's name. **Fills in by itself** from the callsign lookup — you rarely type it. |
| **Status** | What kind of contact this is: Check-In, Traffic, Priority, Emergency, Net Control, Check-Out, Mobile, or Portable. |
| **Location / Grid** | Where the station is — a town, an address, or a Maidenhead grid square. |
| **Precedence** | How urgent the entry is: Routine, Welfare, Priority, or Emergency. This color-codes the row (see below). |
| **Remarks / Traffic** | A short free-text note — anything worth recording about this station or its message. |
| **ICS Position** | Optional. If this operator is filling a role on an incident, pick it from the grouped list (Incident Commander, Section Chiefs, unit leaders, and so on). |
| **Incident ID** | Optional. Ties this check-in to a specific incident; once filled, a **📋 ICS-211 →** link appears to jump to that incident's check-in list. |

When you finish typing a callsign, FieldCommand looks it up instantly in the **offline Federal Communications Commission (FCC) database** — over 800,000 amateur licensees stored right on the Pi, no internet needed — and a blue **FCC card** slides open above the form showing the operator's **Name**, license **Class**, license **Status**, **Location**, and license **Expires** date. The **Name** field fills automatically. The checkbox at the bottom of the form, **Auto FCC lookup**, is on by default; uncheck it if you'd rather not look callsigns up.

1. Type the station's **callsign**. The name (and the FCC card) appear once you finish.
2. Add **location**, **remarks**, **precedence**, or an **ICS position** if you want them — all optional.
3. Click the green **LOG ENTRY** button, or just press **Enter**.
4. The entry drops into the **Stations Logged** list below, newest at the top, stamped with the time.
5. Use **Clear** to wipe the form without logging if you mis-typed.

> **WHAT THE ROW COLORS MEAN** — Each logged station carries a colored left edge set by its **precedence**: **Emergency** is red, **Priority** is amber, **Welfare** is green, and **Routine** is plain. A station typed in with no callsign but a name is tagged **WALK-IN** in amber, so you can see at a glance who isn't a licensed check-in.


## Checking a Station Out — and How Time Is Counted

Every logged station shows a running **Duration** and, on the right of its row, a **Check Out** button. Click it when the operator leaves the net. The button changes to **✓ Out**, the checkout time is stamped, and the operator's total time on the net is frozen.

FieldCommand rounds each operator's participation time **up to the nearest quarter-hour**. So a station on the net for 20 minutes is credited 30 minutes, and one on for 5 minutes is credited 15. This is deliberate — it matches how volunteer time is documented for reimbursement and mutual-aid credit. You do not have to do this math; the page does it and prints it on the ICS-309.

Two more per-row buttons may appear: **+ Roster** (adds a station that isn't already on your permanent roster, so you don't retype them next time) and a small **✕** to remove an entry you logged by mistake (it asks you to confirm first).


## The Traffic Log Tab

Above the station list are three tabs: **✅ Stations Logged**, **📨 Traffic Log**, and **👥 Roster Chips**. The **Traffic Log** is where you record actual messages that pass on the net — radiograms, health-and-welfare messages, and the like — as opposed to simple check-ins.

| Field | What to type |
| --- | --- |
| **From callsign** | The station the message came from |
| **To callsign / address** | Where the message is going |
| **Type** | Radiogram, Health & Welfare, Official, Priority, or Emergency |
| **Message summary** | A short description of the message |

Click **Log Traffic** and the message drops into the traffic list with a timestamp. This matters because the **ICS-309 is a communications log** — its primary content is the message traffic. Logging traffic here fills the top table of that printed form.


## The Roster Chips Tab

The **Roster Chips** tab lets you preload the operators you expect, so checking them in is one click instead of a typed callsign. Click the dashed **import** area (or drag a file onto it) to load a roster from a **CSV** (comma-separated values) or **JSON** file. Each imported person becomes a small **chip** showing their callsign and name. During the net, click a chip and it drops that callsign and name straight into the check-in form — press Enter and they're logged.


## The Sidebar — Live Net Summary

The right-hand sidebar keeps a running tally you can watch without scrolling: **NET SUMMARY** (net name, check-in count, traffic count, duration, and an OPEN/closed status badge), **ACTIVE NETS** (every net currently open), and **LAST 5 ENTRIES** (the five most recent check-ins). It refreshes on its own as you log.


## Drill Mode

The **Drill Mode** checkbox in the header marks the net as an exercise, not a real emergency. When it's on, a bright banner — **⚠ DRILL / EXERCISE — NOT ACTUAL EMERGENCY ⚠** — appears across the top, and the exported ICS-309 is stamped **DRILL / EXERCISE** with a watermark. Always turn this on for training so no one mistakes exercise traffic for the real thing.


## Sharing and Backing Up the Net

Three buttons sit at the right end of the NET TABS strip:

- **🔗 Observer Link** — copies a read-only web link to the current net. Hand it to a section chief, a served-agency liaison, or an EOC duty officer and they can watch the net update live on their own device without touching your log. See Chapter 9 for Observer Mode.
- **📄 ICS-309** — builds and downloads the official communications log for the current net (covered below).
- **💾 Backup JSON** — saves the entire net (check-ins, traffic, everything) as a JSON file on your device, a simple safety copy you can keep or re-import.


## Closing the Net and Exporting the ICS-309

1. Click the red **Close Net** button in the header.
2. Confirm when asked. **Every station still checked in is automatically checked out** at the net-close time, so no one is left with an open clock.
3. The header now shows the net's open time, close time, and total duration.
4. Click **📄 ICS-309**. FieldCommand builds the complete communications log and both downloads it as a file and opens it in a new tab ready to print.
5. The printed ICS-309 carries the net name, type, frequency and mode, open/close times, total duration, totals for check-ins and messages, a **Message Traffic Log** table, and a full **Station Check-In Log** with each operator's participation duration rounded up to the quarter-hour.

> **THE DEAD MAN'S SWITCH WATCHES FOR SILENCE** — A companion tool, the **Dead Man's Switch**, watches net activity and sounds an alert if no check-in is logged within a time window you set. It's meant for safety monitoring during Search and Rescue (SAR) and field operations, where sudden radio silence may signal trouble. See Chapter 12.


## Troubleshooting

- *The net tabs area says *Cannot reach API server*.* The logger talks to the FieldCommand service on the Pi. Confirm your device is on the FieldCommand Wi-Fi and the server is running, then reload the page.
- *I typed a callsign but no name appeared.* The **Auto FCC lookup** checkbox may be off — turn it back on. Also, the lookup needs at least three characters and a moment to respond; give it a second after you finish typing. If the callsign simply isn't in the offline database, type the name by hand.
- *I clicked LOG ENTRY and nothing happened / it said to enter a callsign.* A check-in needs a callsign. Type one in the Callsign field and log again.
- *I clicked Log Traffic / Check Out but it said to select a net first.* You must have a net selected. Click a net tab (or create one with **+ New Net**) before logging anything.
- *I imported a roster but no chips showed up.* Select a net first, then import — chips attach to the current net. Make sure your file has a **callsign** column (CSV) or a callsign field (JSON).
- *The ICS-309 button did nothing.* You need a net selected before exporting. Select the net, then click **📄 ICS-309** again. If a pop-up was blocked, the file still downloads — check your downloads.
- *A station's participation time looks too high.* That's the quarter-hour round-up working as designed: any part of a quarter-hour counts as a full quarter-hour, matching how volunteer time is documented.


# 8. Public Safety Net Logger

*The same live net log as Chapter 7, tuned for radios identified by unit number instead of amateur callsign — for public service nets, interoperability exercises, and served-agency support.*

> **QUICK VERSION** — Open the **public-safety net logger** from the dashboard. Click **+ New Net**, name it, pick a talkgroup and dispatch center, and **Create Net**. As units call in, type each **Radio ID / Unit #**, pick a **status**, and click **LOG ENTRY**. Click **Check Out** when a unit clears. Close the net and print the **📄 ICS-309** just like the amateur logger. If you already know the Amateur Net Logger (Chapter 7), you already know this one — the mechanics are identical.


## What This Is / What It Is For

The **Public Safety Net Logger** is the same live net log described in Chapter 7, set up for **public service** radio operations instead of amateur ones. The one real difference is *how a participant is identified*. On an amateur net, stations check in by **callsign**, which FieldCommand looks up in the FCC (Federal Communications Commission) license database. On a public service net, units check in by **Radio ID** — the unit number on a trunked, P25 (Project 25 digital public-safety), or conventional radio — and **no license lookup is needed or performed**. This is the tool for Public Safety nets, interoperability exercises, and any net where the participants may not hold amateur licenses.

For your organization, the public service side is branded as the **public-safety net logger**. Everything else — creating nets, logging entries, checking units out, the quarter-hour participation timer, Drill Mode, the Observer Link, and the ICS-309 (the standard Incident Command System communications log) export — works exactly as it does on the amateur logger. **This chapter covers only what's different; for the shared mechanics, read Chapter 7.**

> **SAME ENGINE, DIFFERENT LABELS** — Under the hood the public-safety net logger and the Amateur Net Logger are the same tool. If you've run one, the other holds no surprises — the buttons are in the same places and behave the same way. What changes is the vocabulary: **Radio ID** instead of callsign, **units** instead of stations, and **talkgroups** and **dispatch centers** instead of frequencies and grid squares.


## How It Differs From the Amateur Net Logger

Here is the side-by-side, so you can see exactly which parts change:

| Feature | Amateur Net Logger (Ch. 7) | Public Safety Net Logger |
| --- | --- | --- |
| **Primary ID** | FCC callsign — auto-filled from the offline database | **Radio ID** (unit number) — typed in, no lookup |
| **License check** | FCC lookup confirms an active license | **None required** |
| **Roster lookup** | By callsign → name and member ID | By radio ID → name and member ID |
| **Extra fields** | Location / grid square | **Talkgroup** and **Dispatch Center** |
| **ICS-309 column** | Callsign in the station column | Radio ID in the station column |
| **Typical use** | ARES / RACES / AUXCOMM | Public Safety agency nets, interop exercises |


## Opening the public-safety net logger

1. On a device connected to the FieldCommand Wi-Fi, open the dashboard (default **http://192.168.50.1**).
2. Click the **public-safety net logger** — its header shows the blue **STARCOM** badge and reads **NET LOGGER**.
3. The logger opens with a blue accent theme. The layout mirrors the amateur logger: a net-picker strip, a two-column body with the logging area on the left, and a **STARCOM NET SUMMARY** sidebar on the right.

> _[Figure: The Public Safety Net Logger with the STARCOM badge header, the blue-accented net picker, and the summary sidebar]_

The navigation links at the top let you jump to the **public service Dashboard**, the **Amateur Logger**, or **Observer** mode. Until you create or select a net, the header reads **No Net Selected** and the body says *Select or create a Public Safety net to begin*.


## Creating a Public Safety Net

Click the blue **+ New Net** button. The **Create Public Safety Net** box appears. Its fields are tuned for public service radio:

| Field | What to type | Notes |
| --- | --- | --- |
| **Net Name** | A plain name for the net | Required. |
| **Net Type** | Dispatch Net, Tactical Net, Command Net, Mutual Aid Net, Search and Rescue Net, EOC Coordination Net, or Medical Net | Labels the net and prints on the ICS-309. |
| **Talkgroup** | Digital Talkgroup, Conventional Digital, Conventional Analog, P25, or DMR (Digital Mobile Radio) | The kind of radio channel the net uses. |
| **Channel / Frequency** | The channel name or frequency the net runs on | Free text. |
| **Dispatch Center** | The dispatch center backing the net (example: `your county Sheriff Dispatch`) | Optional; shows in the net header when set. |

1. Type at least a **Net Name**.
2. Pick the **Type**, **Talkgroup**, and **Channel**, and name the **Dispatch Center** if there is one.
3. Click **Create Net**. The net goes active, a tab appears, and the check-in form is ready.


## Logging a Unit Check-In

The **Log Unit Check-In / Traffic** form is where you record each unit as it calls in. Because there's no callsign to look up, you type the **Radio ID** and go — it's the only required field. The form's fields:

| Field | What it's for |
| --- | --- |
| **Radio ID / Unit #** | The unit's radio identifier. Shown in bold, large type. **This is the only field you must fill in.** |
| **Unit Name / Callsign** | The unit's name or the operator's name. |
| **Status** | The unit's state: Check-In, Traffic, Priority Traffic, Emergency, Dispatch, Check-Out, En Route, On Scene, Available, or Out of Service. |
| **Talkgroup** | Which talkgroup the unit is on: Digital Talkgroup, Conventional Digital, Conventional Analog, P25 Direct, DMR Direct, or GMRS (General Mobile Radio Service). |
| **Channel / Frequency** | The channel the unit is using. The **📡 Pick** button lets you choose from your saved channels (ICS-205 / Channel Library). |
| **Precedence** | Routine, Welfare, Priority, or Emergency — color-codes the row exactly as in the amateur logger. |
| **Location** | Where the unit is. |
| **Remarks** | A short free-text note about the unit or its message. |
| **ICS Position** | Optional. The unit's role on an incident, from the grouped list. |
| **Incident ID** | Optional. Ties the check-in to an incident and reveals a **📋 ICS-211 →** link to that incident's check-in list. |

There's also a **📡 Dispatch Center** box at the top-right of the form. Type the dispatch center's name there and it shows in the net header, so everyone watching knows which dispatch is backing the net.

1. Type the **Radio ID / Unit #**.
2. Pick a **Status**, and add talkgroup, channel, location, or remarks as needed.
3. Click the blue **LOG ENTRY** button.
4. The unit drops into the **Units Logged** list, newest at the top, stamped with the time. Use **Clear** to reset the form without logging.

> **NO ENTER-TO-LOG HERE** — Unlike the amateur logger, the public-safety net logger does not log on the Enter key — click the **LOG ENTRY** button to record each unit. Everything else about logging, including the colored precedence edge on each row, works the same.


## Checking Units Out, Traffic, and the Shared Tools

The rest of the public-safety net logger behaves just like Chapter 7, so we'll keep this short:

- **Check Out** — each logged unit has a **Check Out** button and a running **Duration**. Click it when the unit clears; the time is frozen and rounded **up to the nearest quarter-hour**, the same way volunteer and staffing time is documented.
- **Traffic Log tab** — the **📨 Traffic** tab records messages passed on the net (From unit, To unit/address, a Type such as Dispatch / Tactical / Resource Request / Status / Priority / Emergency, and a summary). This traffic is the primary content of the ICS-309.
- **Sidebar** — the **STARCOM NET SUMMARY** panel shows the net name, type, unit count, traffic count, open/close times, and duration; the **ACTIVE NETS** panel lists every open net.
- **Drill Mode** — the header checkbox marks the net as an exercise and raises the **⚠ DRILL / EXERCISE ⚠** banner; the exported ICS-309 is stamped accordingly. Always use it for training.
- **🔗 Observer Link** — copies a read-only link so a supervisor or EOC officer can watch the net live without touching the log (Chapter 9).
- **💾 Backup** — saves the whole net as a JSON file on your device.


## Closing the Net and Exporting the ICS-309

1. Click the red **Close Net** button and confirm. **Every unit still checked in is automatically checked out** at the close time.
2. Click **📄 ICS-309**. The communications log builds, downloads, and opens in a new tab ready to print.
3. The printed form is labeled **STARCOM NET**, and its **Unit Check-In Log** shows the **Radio ID** in the station column (where the amateur version shows a callsign). It carries the net type, channel/frequency, open/close times, totals, the **Message Traffic Log**, and each unit's participation duration rounded up to the quarter-hour.


## Operators Who Hold Both a License and a Radio ID

> **KEEP THE TWO LOGS CLEAN** — Some people carry **both** an amateur license and a public service radio ID. On a Public Safety net, they should check in **by radio ID only**, here. If they also need to take part in a concurrent **amateur** net on the same incident, they check into the **Amateur Net Logger** separately, by callsign (Chapter 7). Logging each person in the correct logger keeps both communications logs accurate and defensible.


## Troubleshooting

- *The net picker is stuck on *Loading nets…* or nets won't appear.* The logger talks to the FieldCommand service on the Pi. Confirm your device is on the FieldCommand Wi-Fi and the server is running, then reload.
- *I typed a unit but clicking LOG ENTRY did nothing / it asked for a Radio ID.* A unit check-in needs a **Radio ID**. Type one in the Radio ID / Unit # field and log again.
- *I only see amateur nets, not my public service nets (or vice-versa).* The public-safety net logger shows only Public Safety nets, and the Amateur Logger shows only amateur nets — they're kept separate on purpose. Use the navigation links at the top to switch loggers.
- *Log Traffic or Check Out said to select a net first.* Click a net tab, or create one with **+ New Net**, before logging.
- *The 📡 Pick button said no channels were found.* You need an ICS-205 Communications Plan or a Channel Library set up for the incident. Until then, type the channel or frequency by hand.
- *The ICS-309 export did nothing.* Select a net first, then click **📄 ICS-309** again. If a pop-up was blocked, the file still downloads — check your downloads folder.


# 9. Observer Mode — Read-Only Net View

*A look-but-don't-touch window into any net, auto-refreshing every 15 seconds, for supervisors and liaisons who need to watch without being able to change anything.*

> **QUICK VERSION** — On the net logger, click **🔗 Observer Link** to copy a web link. Send it to whoever needs to watch — a section chief, a served-agency liaison, an EOC duty officer. They open it in any browser on the FieldCommand Wi-Fi, no login needed. It shows the live net and **refreshes itself every 15 seconds**. They can look but cannot change anything.


## What This Is / What It Is For

**Observer Mode** is a **read-only** view of any net running in FieldCommand. It shows the same check-ins and traffic the net control station sees, but with no buttons to log, edit, close, or change anything — it is a window, not a control panel. The page **refreshes itself automatically every 15 seconds**, so an observer always sees current activity without touching a thing.

It exists so people who need to *monitor* a net don't have to crowd around the net control station's screen or be given access to the live log. Typical observers are Incident Command System (ICS) section chiefs, served-agency liaisons, Emergency Operations Center (EOC) duty officers, or anyone who wants situational awareness of a net's activity from their own device. Because observers cannot change anything, you can hand the link out freely without any risk to the official log.

> **SAFE TO SHARE WIDELY** — An observer link is harmless to pass around. There is no login, and nothing an observer clicks can alter the net. The worst an observer can do is close their own browser tab. This is the right way to give a served agency or a supervisor visibility without giving them the keys.


## Getting an Observer Link

The link is created by the operator running the net, from either net logger:

1. On the Amateur Net Logger (Chapter 7) or the Public Safety Net Logger (Chapter 8), select the net you want people to watch.
2. Click **🔗 Observer Link**. The web address (Uniform Resource Locator, or URL) for that net is copied to your clipboard, and a confirmation shows you the link.
3. Share it however is handy — paste it into Winlink or JS8Call, text it, read it over the net, or just hand someone the device.
4. The observer opens the link in any browser on the FieldCommand Wi-Fi. **No login is required.** The net appears and begins refreshing on its own.

> **OBSERVERS CAN BOOKMARK IT** — The observer link is stable for that net, so an observer can bookmark it and reopen the same net later. The link points to one specific net — if you start a new net, hand out its fresh link.


## Reading the Observer Screen

Across the top is the purple **OBSERVER MODE — READ ONLY** banner, with the net name and description just beneath it, so there's never any doubt this is a watch-only view. On the right of the banner:

- A large green **clock** showing the current time in **UTC** (Coordinated Universal Time), ticking every second.
- An **Auto-refresh in __s** countdown that shows how many seconds until the next refresh.
- A thin purple **refresh bar** below the banner that empties from full to zero over the 15-second cycle — a visual sense of when the next update lands.

> _[Figure: The Observer Mode banner with the READ ONLY label, the UTC clock, the auto-refresh countdown, and the purple refresh bar]_

Below the banner is a header panel with the net's **name** in large type, its **type and net ID** underneath, and a status badge on the right reading **ACTIVE** (green) or **CLOSED** (gray). A small **Updated __ UTC** note shows the time of the last refresh. If the net is a drill, the **⚠ DRILL / EXERCISE — NOT ACTUAL EMERGENCY ⚠** banner appears here too, so observers aren't fooled by exercise traffic.


## The Two Live Panels

The body of the page is split into two side-by-side panels that update together every 15 seconds:

| Panel | What it shows |
| --- | --- |
| **Stations Logged** | Every check-in, newest at the top, with the callsign or radio ID, the operator/unit name, a status badge, the check-in time in UTC, the location, and any remarks. The count of stations is shown in the heading. Rows carry the same precedence colors as the logger — red for Emergency, amber for Priority, green for Welfare. |
| **Traffic Log** | Every message logged on the net, newest at the top, with the from/to stations, the time in UTC, the type, and the note. The message count is shown in the heading. |

> **WHAT THE OBSERVER HEADER LEAVES OUT** — The observer header is deliberately lean. It does **not** currently repeat the net's frequency or mode, and it does **not** show a live elapsed-net timer the way the logger's own header does. Observers see the live check-in and traffic lists — the substance of the net — but not those two header extras.


## Opening Observer Mode Without a Link

If someone opens the observer page **without** a specific net link, they get a **Select a Net to Observe** picker instead. It lists every net on the server as a clickable card showing the net name, its type, the number of entries, and badges for its state — **ACTIVE** or **CLOSED**, plus **STARCOM** for a Public Safety net and **DRILL** for an exercise. Clicking a card opens that net in the read-only view. This is a handy way to browse what's running when you weren't handed a direct link.


## What Observers Can and Cannot Do

The whole design rests on one idea: observers see everything and touch nothing. Here is the line, drawn plainly:

| Observers CAN | Observers CANNOT |
| --- | --- |
| View every check-in as it happens | Add or remove check-ins |
| View the net's open status and activity | Close the net |
| View the full traffic log | Add or edit traffic entries |
| Watch the page refresh itself every 15 seconds | Change any net setting |
| Bookmark the observer link and reopen it later | Reach the Net Control logging view |


## Troubleshooting

- *The page says *Cannot reach API server at 192.168.50.1:5050*.* The observer view reads from the FieldCommand service on the Pi. Make sure the device is on the FieldCommand Wi-Fi and the server is running, then reload.
- *It says *Net not found*.* The link points to a net that no longer exists or was mistyped. Ask the net control station for a fresh **🔗 Observer Link**, or open the observer page with no link to pick from the current list.
- *The list isn't updating.* Observer Mode refreshes every 15 seconds on its own — watch the countdown and the purple bar. If it still looks frozen, reload the page manually; a dropped Wi-Fi connection will stop the refresh until it reconnects.
- *I want to add a check-in but there are no buttons.* That's by design — Observer Mode is read-only. Logging happens on the Net Control logger (Chapter 7) or the Public Safety Net Logger (Chapter 8), not here.
- *The clock shows a different time than my watch.* The observer clock is in **UTC**, the standard time zone for logging, not your local time. That's expected.


# 10. Barcode & Quick Response (QR) code Scan Check-In

*Check people in fast with a phone or tablet camera — scan a badge, the roster fills the form, tap Check In. No camera? Type the ID instead.*

> **QUICK VERSION** — Open **Scan Check-In** on a phone or tablet. Tap **📷 Start Camera** and point it at the person's QR code or barcode. Their details fill the form by themselves — glance at them, then tap **✓ Check In**. No camera or code? Type their **member ID, callsign, or radio ID** in the manual box and tap **Look Up**. Tap **Scan Next Person** and repeat.


## What This Is / What It Is For

**Scan Check-In** is the fast way to check people in at an activation using nothing but a smartphone or tablet camera. Point the camera at a member's **QR code** (Quick Response code — the square dot pattern) or **barcode**, and FieldCommand reads it, looks the person up in the roster, and fills their check-in form automatically. Tap one button and they're in. It's built for the check-in table at a staging area, an EOC (Emergency Operations Center), or a shelter, where a line of people needs to be logged quickly and accurately.

It does all of this **completely offline**. The scanning uses the browser's own built-in **BarcodeDetector** — a camera-reading feature baked into the browser itself — so there is no app to install, no external library, and no internet connection required. It reads QR codes plus several common barcode formats: Code 128, Code 39, EAN-13, EAN-8, Data Matrix, PDF417, and Aztec.

> **IT TIES INTO THE ICS-211 CHECK-IN LIST** — Each person you check in here is filed against an **incident** and operational **period**, and flows into that incident's **ICS-211** (the Incident Command System Check-In List). Scan Check-In is normally opened from an incident's ICS-211 share link, which carries the incident along in the web address so every scan lands in the right place.


## The Ways to Check Someone In

There are four ways to get a code into FieldCommand, and they all end at the same place — a filled-in form you confirm with **✓ Check In**. Pick whichever fits your table and your device; you can mix them freely during one event.

| Method | How it works | Best for |
| --- | --- | --- |
| **Handheld barcode scanner** *(most reliable)* | A **USB or Bluetooth 2D barcode scanner** — the handheld kind stores use — plugged into or paired with the check-in device. It reads the QR code or barcode and **types the value** straight into the manual box, which the page keeps **auto-focused** for exactly this. Works on **any device and any browser**, because to the computer it's just a keyboard. | A staffed check-in table where you want speed and zero fuss |
| **Take Photo of QR** | Tap the take-photo control, which opens the phone's camera to snap a single still picture of the code; FieldCommand reads the code from that photo. | A phone that can't run the live viewfinder but can still take pictures (Android/Chromium) |
| **Live camera viewfinder** | Tap **📷 Start Camera** and hold the code in view; the page reads it automatically, checking the picture about **4 times a second**. The same code won't log twice within 3 seconds, so a code lingering in view can't create duplicates. Needs the secure **HTTPS** connection (the padlock). | Busy tables; members who carry a printed QR code or badge |
| **Manual ID entry** | Type a member ID, callsign, or radio ID in the manual box and press **Enter** or tap **Look Up**. It does the same roster lookup the camera does, and always works everywhere. | When there's no camera or scanner, or for walk-ins who have no code |

> **A HANDHELD 2D SCANNER IS THE SUREST BET** — If you're staffing a check-in table, an inexpensive **USB or Bluetooth 2D barcode scanner** is the most reliable choice by a wide margin. It needs no camera permission, no special browser, and no secure-connection setup — it simply acts like a keyboard and types the code into the box, which the page keeps ready and focused for you. It works the same on a phone, tablet, or laptop and on any browser, so it sidesteps every camera limitation described later in this chapter. Point, beep, done. Keep the manual box as your always-available backup.

> **TAKE-PHOTO AND LIVE CAMERA ARE PHONE FEATURES** — **Take Photo of QR** and the **live camera viewfinder** both use a phone or tablet camera, and both work on **Android with Chrome, Edge, or Samsung Internet**. Neither works in **iPhone/iPad Safari** — that's a limitation of that browser, covered in "Which Browsers Can Scan" below. On an iPhone, use a **handheld scanner** or the **manual ID entry** box instead; both work fine there.


## Opening the Page and Starting the Camera

1. Open **Scan Check-In** — usually from an incident's **ICS-211** share link, or from the dashboard.
2. At the top, a bar shows the **camera viewfinder** with a white targeting frame and a moving scan line.
3. Tap **📷 Start Camera**. The first time, your browser asks permission to use the camera — tap **Allow**.
4. If the device has more than one camera (front and rear), pick the **rear-facing** one from the **camera dropdown** next to the buttons — it's easier to aim at a badge someone is holding.
5. The status line reads **Scanning…** once the camera is live. Tap **⏹ Stop Camera** to turn it off.

> _[Figure: The Scan Check-In viewfinder with the targeting frame and scan line, the Start/Stop Camera buttons, and the camera-select dropdown]_


## Reading the Screen

From top to bottom, the page is laid out for one-handed use at a check-in table:

- **Camera viewfinder** — the live camera picture with a white corner frame to aim inside and a status line at the bottom (*Point camera at QR code or barcode*, then *Scanning…*, then *✓ Scanned:* the code).
- **Camera controls** — **Start Camera**, **Stop Camera**, and the camera-select dropdown.
- **Manual ID entry** — a text box to type a member ID, callsign, or radio ID, with a **Look Up** button, for when scanning isn't an option.
- **Check-in form** — appears after a scan or lookup resolves, pre-filled where possible (covered below).
- **Success box** — a big green **✅ CHECK-IN COMPLETE** confirmation after you submit.
- **Recent Check-Ins This Session** — a running list of the last few people you checked in on this device, so you can see your progress.
- **Incident badge** — a small line at the bottom naming the incident and period these check-ins belong to.


## When Someone Is Found — and When They Aren't

As soon as a code is scanned or an ID is looked up, FieldCommand searches the roster and one of two things happens:

| Result | What you see |
| --- | --- |
| **Found on the roster** | A green banner shows the person's **name, ID, and agency**, tagged as a **✓ Roster member** or **👤 Visitor**. The form's **Name**, **ID**, and **Agency** fields fill in with green borders, and a **suggested ICS position** is selected if the roster has one. Review it, then tap **✓ Check In**. |
| **Not on the roster** | A **not-found** banner appears (*"…" not in roster. Fill in details manually.*). The scanned code drops into the **ID** field, and the cursor jumps to the **Name** field so you can type their details. Then tap **✓ Check In** as usual. |

Either way, tapping **✓ Check In** files the person, shows the full-screen **✅ CHECK-IN COMPLETE** box with their name and check-in time, and — on phones that support it — gives a short **vibrate** so you know it worked without staring at the screen. Tap **Scan Next Person** to clear everything and move to the next person in line.


## The Check-In Form Fields

| Field | What to enter |
| --- | --- |
| **Full Name** *(required)* | The person's name. **Required** — you cannot check someone in without it. |
| **Callsign / ID** | Their callsign, member ID, or unit number. Fills in from the scan when they're on the roster. |
| **Agency** | The organization they're with (example: `your org's short form` or a mutual-aid agency). |
| **ICS Position** | Their role, from the list — Incident Commander, the Section Chiefs, Branch Director, Division/Group Supervisor, Net Control, Amateur Radio Operator, Emergency Medical, Volunteer, or Other. Pre-selected when the roster suggests one. |
| **Resource Type** | What kind of resource they are — Personnel, Amateur Radio, Engine, Crew, Vehicle, Equipment, or Other. |


## The Order the Roster Is Searched

When you scan a code or type an ID, FieldCommand tries to match it against several roster fields in turn, stopping at the first match. That way one scanner reads a member badge, an amateur callsign, or a public-safety unit number without you telling it which is which:

| Search order | Field checked | Example value |
| --- | --- | --- |
| 1st | barcode_id (the badge/QR value) | MEM-042 (or a badge number if set) |
| 2nd | member_id | MEM-042 |
| 3rd | callsign | your club callsign |
| 4th | radio_id | 412 |


## Which Browsers Can Scan

> **CAMERA SCANNING NEEDS THE RIGHT BROWSER** — Camera scanning relies on the browser's built-in **BarcodeDetector**, which is available on **Chrome** (Android and desktop), **Edge**, and **Samsung Internet**. It is **not** available on **iPhone/iPad Safari** or **Firefox**. On those browsers the **Start Camera** button is disabled and the status line tells you so — but the **manual ID entry** box still works normally, so you can always check people in by typing. For a scanning table, an Android phone or a Chrome/Edge device is the safe choice.


## Troubleshooting

- *The Start Camera button is grayed out.* Your browser doesn't support camera scanning (most often iPhone/iPad Safari or Firefox). Use a **handheld barcode scanner** or the **manual ID entry** box, or switch to Chrome, Edge, or Samsung Internet on an Android device.
- *I'm on an iPhone and can't scan.* iPhone/iPad Safari does not support the live camera or take-photo scanning — that's an Apple browser limitation, not a fault. The **manual ID entry** box works normally on an iPhone, and a **handheld USB/Bluetooth barcode scanner** is the best fix for a busy iPhone-based table since it just types the code in.
- *My handheld barcode scanner isn't entering anything.* A 2D scanner acts like a keyboard, so first click into the **manual ID entry** box to make sure it has focus, then scan. Confirm the scanner is plugged in (or paired over Bluetooth) and set to **2D** mode so it can read QR codes, not just old-style 1D barcodes. Test it in any text box — if it doesn't type there either, it's a scanner or pairing issue, not FieldCommand.
- *The camera opens for a still photo instead of a live viewfinder.* On some phones the take-photo option snaps a single picture of the code rather than scanning continuously — that's expected and works the same; just frame the code clearly and take the shot. For continuous scanning, use **Start Camera** on a supported browser (Chrome, Edge, or Samsung Internet).
- *I tapped Start Camera but see a black box or a camera error.* The browser needs camera permission — reload and tap **Allow** when asked. Make sure no other app is using the camera, and that the page was opened over the FieldCommand address, since browsers only allow the camera on trusted connections.
- *The camera is on but won't read the code.* Hold the code flat and steady inside the white frame, fill the frame with it, and give it good light. Glare and motion blur are the usual culprits. If it still won't read, type the ID by hand.
- *It says the person isn't in the roster.* Their code doesn't match any roster field. Fill in the **Name** and **Agency** by hand and tap **✓ Check In** — the check-in still records; it's just entered manually.
- *Check-in failed / server error.* The page couldn't reach the FieldCommand service. Confirm the device is on the FieldCommand Wi-Fi and the server is running, then tap **✓ Check In** again.
- *The same person scanned twice.* The page ignores a repeat of the same code within 3 seconds to prevent exactly this. If a true duplicate slips through, it can be cleaned up on the incident's ICS-211 list.
- *The bottom says *No incident selected*.* Open Scan Check-In from the incident's **ICS-211 share link** so the incident and period travel with it; otherwise check-ins have nowhere to file.


# 11. Federal Communications Commission (FCC) Callsign Lookup

*An offline, on-the-Pi copy of the entire national amateur-radio license database — look up any callsign in a second, with no internet, and let the rest of FieldCommand fill in names for you automatically.*

> **QUICK VERSION** — Open **Callsign Lookup** from the dashboard. Type a callsign in the big box and press **Enter** (or click **Look Up**). A card shows the operator's name, license class, status, and city/state. To find someone whose callsign you don't know, use **Advanced Search** below the box. It all runs on the Pi — no internet needed.


## What This Is / What It Is For

The **Callsign Lookup** tool is a searchable copy of the Federal Communications Commission (FCC) amateur-radio license database — every active licensee in the country, over 800,000 of them — stored right on the Pi. When someone checks into your net and gives a callsign, this is where you confirm who they are, whether their license is still valid, and where they're licensed out of.

The important word is **offline**. The whole database lives in a small file on the server (a SQLite database, which is just a self-contained file full of records). Because it's local, a lookup returns instantly and works even when there's no internet at all — which is exactly the situation FieldCommand is built for. You are not reaching out to the FCC's website; you're reading a copy that was already downloaded and stored for you.

> **WHY THIS MATTERS DURING AN INCIDENT** — During a real activation your internet may be down or unreliable. A live web lookup would fail exactly when you need it. Keeping the database on the Pi means callsign verification keeps working no matter what the network is doing.


## Opening the Tool and Doing a Quick Lookup

At the top of the page is a hero panel headed **📻 CALLSIGN LOOKUP**, with the reminder *“FCC Amateur Radio License Database · Offline SQLite · Updated weekly.”* Under it is one large text box and a **Look Up** button. This is the fast path — if you already know the callsign, you never need anything else on the page.

1. From the dashboard, click **Callsign Lookup**.
2. Click in the big search box and type a callsign — for example `W8XYZ`. It automatically shifts to capital letters as you type.
3. Press **Enter**, or click the **Look Up** button.
4. A result card slides into view below the box with everything the database knows about that callsign.

> _[Figure: The Callsign Lookup page: the amber CALLSIGN LOOKUP hero with the large search box and Look Up button]_

> **IT'S NOT LIVE-AS-YOU-TYPE** — Nothing happens until you press **Enter** or click **Look Up**. Type the whole callsign first, then search. This is deliberate — it avoids hammering the database with a lookup for every keystroke.


## Reading the Result Card

When a callsign is found, the card shows the callsign in large amber letters, a colored **license-class tag**, and a status dot. Below that is a grid of details. Here is what each item means in plain terms:

| Field | What it tells you |
| --- | --- |
| **License Class** (colored tag) | The privilege level of the license: **Technician**, **General**, **Amateur Extra**, **Novice**, or **Advanced**. Higher classes may use more bands and modes. |
| **Status dot** | **Active** (green) means the license is current. Anything else (red) means it is not active — expired, cancelled, or otherwise not in good standing. |
| **Name** | The licensee's name (or the organization/club name, for a club license). |
| **City, State** | Where the license is registered — the licensee's mailing address city and state. |
| **Zip Code** | The mailing-address ZIP code. |
| **Country** | Country of the license (usually US). |
| **Grant Date** | The date the current license was granted. |
| **Expiration Date** | When the license expires. If that date has already passed, it is shown in **red** as a warning. |
| **FRN** | FCC Registration Number — a unique ID the FCC assigns to each licensee. Rarely needed day-to-day. |
| **License ID** | The internal license record number the FCC uses. It's what links through to the official record. |
| **Grid Square** | The operator's Maidenhead grid locator, if the record includes one — a short code hams use to describe location. Only shown when present. |

> **A RED EXPIRATION DATE IS A FLAG, NOT A BLOCK** — If the **Expiration Date** shows in red, that operator's license has lapsed on paper. FieldCommand still shows you the record — it's just alerting you so a net control operator can note it and follow up. Verifying license validity is part of running a clean, legal net.


## The Buttons on a Result

At the bottom of a found result are three actions:

| Button | What it does |
| --- | --- |
| **FCC ULS ↗** | Opens the FCC's official Universal Licensing System page for this exact license in a new browser tab. This one **does** need internet — it's a link out to the FCC's live website for the authoritative record. |
| **+ Add to Roster** | Jumps to the Roster page with this callsign pre-filled, so you can add the operator to your incident roster without retyping their information. |
| **📋 Copy** | Copies the callsign to your clipboard so you can paste it into a form, a log, or a message. |


## Advanced Search — Finding a Callsign You Don't Know

Sometimes you have a name but not a callsign — someone reports "a John Smith from Columbus is trying to reach net control." The **Advanced Search** panel below the main box lets you search the database by details other than the callsign. Fill in any one or more of these boxes and click **Search**:

| Search box | What to enter |
| --- | --- |
| **Last Name / Entity Name** | A surname, or a club/organization name (example: `Smith`). |
| **First Name** | A first name (example: `John`). |
| **State** | Pick a state from the dropdown, or leave it on **All States**. |
| **License Class** | Narrow to one class — Technician, General, Amateur Extra, Novice, or Advanced — or leave on **All Classes**. |
| **City** | A city or town name (example: `Columbus`). |
| **Grid Square** | A Maidenhead grid locator (example: `EN80`). |

You must fill in at least one box — if you click **Search** with everything blank, the page reminds you to enter a search criterion. Results appear in a table below with columns for **Callsign**, **Name**, **Class**, **City**, **State**, **Status**, and **Expires**. A count (for example *“12 results found”*) shows on the right. Click any **callsign** in the table to jump straight to its full result card. The **Clear** button empties all the boxes and wipes the results so you can start a fresh search.

> _[Figure: The Advanced Search panel with the results table showing several matching licensees]_

> **TOO MANY RESULTS? ADD ANOTHER DETAIL** — A common last name alone can return a long list. Add a **State** or **City** to narrow it down. The search returns up to 100 matches at a time, so a broad search may not show everyone — tighten it up.


## Recent Lookups

At the very bottom, under **Recent Lookups**, the page keeps a row of buttons for the last callsigns you looked up (up to 20). Click any one to instantly look it up again. This list is stored in your own browser, so it's per-device — a handy shortcut when you keep coming back to the same few stations during a net.


## Where the Database Fills In Names for You

You often won't open this page directly at all — the same database quietly does its job inside other tools. Whenever you type a callsign into one of these, FieldCommand looks it up in the background and fills in the operator's details:

| Where | How it helps |
| --- | --- |
| **Net Control Logger** | As you enter a callsign in the check-in field, the operator's **name** and **license class** fill in automatically. A **red border** warns you if the callsign isn't in the database or the license has expired. |
| **Scan Check-In** | After a Quick Response (QR) code scan or a manual entry, if the code is a callsign, the FCC record supplies the operator's name (falling back to your roster if it isn't found). |
| **ICS-213 General Message** | The *From Callsign* field pulls the sender's name from the database, so the message is properly attributed without extra typing. |

In other words, the value of having the whole FCC database on the Pi isn't just this one lookup page — it's that every place you enter a callsign gets smarter and faster, all without internet.


## Keeping the Database Current

The FCC updates its license records constantly — new licenses, renewals, upgrades, and expirations. The copy on your Pi is refreshed on a schedule (weekly is typical). If you need to update it manually, an administrator downloads the FCC's license export (from the FCC's Universal Licensing System, ULS) and runs the import step described in the Installation Guide. Day-to-day operators never have to think about this; it's a one-time-per-refresh administrator task.

> **A MISSING CALLSIGN USUALLY MEANS AN OUT-OF-DATE COPY** — If a brand-new licensee or a very recent callsign change isn't found, the local copy simply predates that change. Update the database (or check the FCC ULS link online) to pick up the newest records.


## Troubleshooting

- *Nothing happens when I type.* The tool doesn't search as you type. Finish typing the callsign, then press **Enter** or click **Look Up**.
- *“Callsign not found in FCC database.”* Either the callsign is mistyped, or your local copy of the database doesn't include it yet (very new or recently changed callsigns). Double-check the spelling, try **Advanced Search** by name, or update the database as described above.
- *“Could not reach local FCC database. Ensure the server is running on port 5050.”* The lookup service on the Pi isn't responding. Confirm the FieldCommand server is powered on and running, then try again. This is a server issue, not a typo.
- *A license shows an expired (red) date.* That's the database telling you the license has lapsed on record. It's not an error — note it for your net log and verify with the operator or the live FCC ULS link.
- *Advanced Search says “Enter at least one search criterion.”* You clicked **Search** with every box empty. Fill in at least one field (name, city, state, class, or grid) first.
- *Advanced Search returns nothing.* Your criteria were too narrow or slightly off (a misspelled city, wrong state). Remove a filter or two and search again with less detail.
- *The FCC ULS ↗ button won't open the record.* That button links to the FCC's live website and needs internet. Offline, it won't load — but the local result card still shows you everything stored on the Pi.


# 12. Dead Man's Switch

*A safety timer that watches your net for silence. If nobody checks in within the time you set, it sets off an alarm — so a field team that goes quiet doesn't go unnoticed.*

> **QUICK VERSION** — Open **Dead Man's Switch**. Set a **threshold** (how many minutes of silence you'll allow). **Arm** the net you want to watch. A countdown runs. Every check-in in Net Control resets it. If the countdown ever hits zero, the page flashes red and sounds an alarm so you can investigate. Click **Disarm** when the net closes.


## What This Is / What It Is For

A **Dead Man's Switch** is a safety device that assumes the worst if it stops hearing from you. FieldCommand's version watches your net's check-in activity. As long as check-ins keep coming, it stays quiet. But if the net goes completely silent for longer than a limit you set, it raises an alarm — because unexpected radio silence can mean a field team is in trouble and unable to call for help.

This is built for operations where a quiet radio is genuinely dangerous — search and rescue, a lone operator in the field, a team working a hazardous area. Instead of a human at net control having to remember "wait, when did we last hear from Team 3?", the switch tracks it precisely and never gets distracted.

> **IT WATCHES ACTIVITY — IT DOESN'T TRANSMIT** — The Dead Man's Switch is purely a monitor and an alarm. It doesn't key a radio or call anyone on its own. When it triggers, it's telling **you** to act — make contact, send someone to check, or escalate.


## The Four States

A net being watched moves through four states. The page uses these same words and colors everywhere, so it's worth learning them:

| State | Color | What it means |
| --- | --- | --- |
| **Disarmed** | Green | Not being watched. The timer is off. This is the resting state before you start and after you stop. |
| **Armed** | Amber | Actively watching. The countdown is running and check-ins are resetting it. Everything is normal. |
| **Warning** | Red | The countdown has passed the warning mark (75% of the threshold by default). Time is getting short — a heads-up before the full alarm. |
| **Triggered** | Red (flashing) | The countdown reached zero. The alarm is firing. No activity was heard in time. Investigate now. |


## The Status Ring at the Top

In the top-right of the page is a large circular **status ring**. It's an at-a-glance summary of the **worst** state across every net you're watching. If everything is calm it reads **ALL CLEAR** in green; if any single net is in trouble, the ring jumps to that net's state — **MONITORING** (amber), **WARNING** (red), or **TRIGGERED** (red and pulsing). The idea is that from across the room you can tell the overall situation from the color of that one ring.

> _[Figure: The Dead Man's Switch page: the green ALL CLEAR status ring beside the header, with the configuration panel below]_


## Default Configuration

The **DEFAULT CONFIGURATION** panel sets the behavior used when you arm a net. These are the knobs:

| Setting | What it controls | Default |
| --- | --- | --- |
| **Default Threshold (minutes)** | The maximum silence allowed. If no activity is logged within this many minutes, the switch triggers. Shorter for high-risk operations, longer for routine nets. | `30` |
| **Warning at (% of threshold)** | How far into the countdown the **Warning** state kicks in, as a percentage. At 75%, a 30-minute threshold warns at 22.5 minutes elapsed — giving you a nudge before the full alarm. | `75` |
| **Poll Interval (seconds)** | How often the page checks the server for fresh activity. Lower means faster reaction; higher means less network chatter. | `15` |
| **Alert Sound** | The sound the alarm makes: **Beep**, **Alarm** (a louder, higher tone), or **None (visual only)** if you want the flashing banner but no sound. | `Beep` |

After changing any of these, click **Save Defaults**. The page remembers them on this device and notes the change in the activity log.

> **PICK A THRESHOLD YOU CAN LIVE WITH** — The threshold is a judgment call. Too short and you'll get false alarms every time the net is briefly quiet; too long and a real emergency goes unnoticed for too long. Match it to how often your teams are expected to check in — a good rule of thumb is a bit longer than your normal check-in cycle.


## Monitored Nets

Below the configuration is the **MONITORED NETS** area. Each net you're watching gets its own card, and the small timestamp on the right (**Updated … Z**) tells you when the page last heard from the server. If nothing is being watched yet, you'll see a message telling you to open a net in Net Control and arm the switch.

Each net card packs a lot of information into a small space:

| On the card | What it shows |
| --- | --- |
| **Net name** and **state badge** | The net's name and its current state (disarmed / armed / warning / triggered), color-coded. |
| **Countdown timer** | The big number in the middle — time **remaining** before the alarm, counting down live. It's colored to match the state. |
| **Progress bar** | A visual bar that fills up as the silence grows. Full bar = out of time. |
| **Last activity** | The clock time of the most recent check-in that reset this net's timer. |
| **Elapsed** | How many minutes have passed since that last activity. |
| **Warning at** | The minute mark where this net flips to the Warning state (based on your warning percentage). |
| **Triggered** | Only appears once an alarm has fired — the time it triggered, in red. |

> _[Figure: A monitored net card showing the live countdown timer, progress bar, and Arm / Reset / Disarm buttons]_


## Arming, Resetting, and Disarming a Net

The buttons at the bottom of each net card change depending on its state, so you only ever see the actions that make sense right now:

| Button | When it appears | What it does |
| --- | --- | --- |
| **⚡ Arm** | When the net is disarmed | Starts watching this net. The countdown begins from your threshold and the state turns Armed. |
| **↺ Reset** | When the net is armed, warning, or triggered | Manually restarts the countdown from the top — useful after you've handled an alarm and want to keep watching. |
| **✕ Disarm** | When the net is armed, warning, or triggered | Stops watching this net entirely. It asks you to confirm first, then returns the net to Disarmed. |

> **CHECK-INS RESET THE TIMER FOR YOU — AUTOMATICALLY** — You normally don't touch the **Reset** button at all. **Any** check-in logged in the Net Control Logger for that net resets its countdown on its own. That's the whole point: as long as your teams keep checking in, the timer keeps refreshing and the alarm never fires. **Reset** is just a manual override for when you need it.


## What Happens When the Alarm Fires

If a net's countdown reaches zero, three things happen at once so it's impossible to miss:

- A **red alarm bar** appears across the top of the page reading *“DEAD MAN'S SWITCH TRIGGERED — NET INACTIVITY ALARM,”* flashing to draw the eye.
- The **status ring** and the affected **net card** turn red and pulse.
- The **alert sound** you chose plays (unless you set it to None).

When this happens, act on it: try to raise the silent team or net on the radio, send someone to physically check if you can, and escalate to your incident commander. Once you've made contact or resolved the situation, click **↺ Reset** to restart the countdown (if the net is still running) or **✕ Disarm** to stop watching. The alarm clears on its own once no net is in the triggered state anymore.

> **THE SOUND NEEDS A SPEAKER AND AN AWAKE SCREEN** — The audible alarm plays through the browser on the device showing this page, so that device needs working speakers with the volume up. Run the Dead Man's Switch on a dedicated monitor or tablet at the net control position, and keep that screen awake — a sleeping tablet can't sound an alarm.


## The Activity Log

At the bottom, the **ACTIVITY LOG** is a running timeline of what the switch has done — nets armed, reset, or disarmed, configuration changes, and alarms. Each line shows the time, the net, and a short note. It's a quick record of the session for your after-action notes. The **Clear** button empties the log. The log is kept in this browser only and isn't a permanent incident record, so copy anything important into your official log before clearing it.


## Troubleshooting

- *“Loading DMS state from server…” never goes away, or it says “Server offline.”* The page can't reach the Dead Man's Switch service on the Pi. Confirm the FieldCommand server is running and this device is on the FieldCommand Wi-Fi, then wait for the next poll.
- *No nets show up to monitor.* There's nothing to watch until a net is live. Open a net in **Net Control** first, then return here — the net will appear as a card you can **Arm**.
- *The alarm went off but there was no emergency (false alarm).* Your threshold is shorter than your net's natural quiet periods. Raise the **Default Threshold**, click **Save Defaults**, and re-arm. Then **Reset** the net to restart cleanly.
- *The timer never counts down / never resets.* The switch resets on check-ins logged in the **Net Control Logger**. If check-ins aren't being logged there, the timer won't refresh. Make sure operators are being logged in Net Control, not just heard on the radio.
- *I can't hear the alarm.* Check the device's speaker and volume, and confirm **Alert Sound** isn't set to **None**. Browsers also need a click on the page before they'll play sound — interact with the page once after loading it.
- *I armed the wrong net / want to stop watching.* Click **✕ Disarm** on that net's card and confirm. It returns to the green Disarmed state and stops counting.


# 13. Tactical Automatic Packet Reporting System (APRS) Map

*A live map of every APRS station your radios can hear — vehicles, field teams, weather stations, and repeaters — pulled together from radio and internet feeds into one situational-awareness picture.*

> **QUICK VERSION** — Open the **Tactical Map**. Stations that your radios and feeds are hearing appear as markers, brightest when heard recently. Click a marker for details. Use the **layer buttons** (top-left of the map) to show or hide each source, the **Stations** tab to search, the **Messages** tab to send an APRS text, and the **Markers** tab to drop your own pins for the EOC, shelters, and command posts.


## What This Is / What It Is For

The **Tactical Map** is FieldCommand's main situational-awareness screen. Automatic Packet Reporting System (APRS) is a ham-radio system where stations beacon their position, speed, and a short comment over the air. This map collects those beacons and plots every station on a moving map — so you can watch field teams, vehicles, and mobile resources move in real time, all in one place.

It pulls stations from up to three sources at once and merges them so each station shows up only once, even if more than one source heard it:

| Source | What it is | Needs internet? |
| --- | --- | --- |
| **Direwolf (RF)** | APRS heard directly off the radio, decoded by Direwolf software and served through APRS Command. This is your true off-air picture. | **No** — works fully offline |
| **APRS-IS** | The worldwide APRS internet feed (via the aprs.fi service). Fills in stations beyond radio range. | **Yes** — internet required |

> **OFFLINE CAVEAT — THE BASE MAP MAY NOT DRAW WITHOUT INTERNET** — The station markers are the offline part and always plot. The **background map image** (the streets and terrain) is a separate matter. In the current build the mapping library and default map tiles load from the internet, so with no internet the base map may come up blank while your markers still float on top. For a true no-internet map, an administrator downloads offline map tiles onto the Pi (there's a `download_tiles.sh` step for exactly this). See the Settings tab's **Map Tiles** note.


## The Top Bar

Across the top, the **📡 TACTICAL MAP** bar shows a live **Stations** count (how many unique stations are on the map right now) and a UTC clock. Two buttons live here:

| Button | What it does |
| --- | --- |
| **⟳ Refresh** | Immediately re-polls every source for fresh station data, instead of waiting for the next automatic refresh. |
| **⬇ KML** | Exports the current stations to a KML file — a map format you can open in Google Earth or share with other mapping tools. |


## The Layer Buttons

Down the top-left corner of the map is a stack of **layer buttons**. Each one turns a category of markers on or off, so you can declutter the map to just what you care about. A lit (colored) button means that layer is showing.

| Button | Shows / does |
| --- | --- |
| **🟢 Direwolf** | Stations heard off the radio via Direwolf. |
| **🟣 APRS-IS** | Stations from the internet APRS feed. |
| **📌 Overlays** | Your own hand-placed markers (from the Markers tab). |
| **⬡ My Station** | Your own station's position marker. |
| **◎ Range Ring** | A distance circle around your station, so you can judge how far out a station is. Radius is set in Settings. |
| **🛤 Track** | Draws the movement trail of the station you're tracking, so you can see where it's been. |
| **📡 Repeaters** | Overlays repeaters from the FieldCommand Repeater Database onto the map. |
| **🗺 SARTopo** | Shows a search-and-rescue planning overlay (sectors, assignments, zones) imported on the SARTopo Import page. |

> **SARTOPO OVERLAYS ARE IMPORTED SEPARATELY** — The **SARTopo** layer shows planning data (search sectors, assignments, exclusion zones) that you export from SARTopo/CalTopo as a GeoJSON file and bring in on the **SARTopo Import** page. Once imported, it stays on the map through refreshes; toggle it here with the 🗺 SARTopo button.


## Station Markers and Popups

Each station is drawn with its standard APRS symbol (a car, a house, a weather station, and so on — the app translates APRS symbols into easy-to-read emoji). Two things about a marker tell you its story at a glance:

- *Fill color = how recently it was heard (age).* Bright green means fresh (heard within the last ~15 minutes), amber means aging (roughly 15–60 minutes), and gray means old (over an hour). A faded marker is a station you haven't heard from in a while.
- *Border color = which source heard it.* Green border = Direwolf (RF), purple = APRS-IS, and white = heard by both sources. The Legend in the Settings tab spells this out.

Click any marker to open its popup, which lays out everything known about the station:

| In the popup | Meaning |
| --- | --- |
| **Callsign** + source tags | The station's callsign and which feeds heard it. |
| **Symbol / Type** | Its APRS symbol and category (Mobile, Fixed, Weather, Digi, iGate). |
| **Comment** | The free-text status the operator is beaconing. |
| **Speed / Course** | How fast it's moving and which direction (only if it's moving). |
| **Altitude** | Reported altitude, if any. |
| **Path** | The digipeater path the packet traveled — useful for judging how it reached you. |
| **Freq** | A voice frequency the station is advertising, if included. |
| **Last heard** | When the most recent beacon arrived, and how long ago. |

Two buttons sit at the bottom of the popup: **🛤 Track** starts drawing that station's movement trail, and **✉ Message** opens the Messages tab pre-addressed to that callsign.

> _[Figure: The Tactical Map with colored station markers and an open popup showing a mobile station's details and Track / Message buttons]_


## The Sidebar Tabs

On the right is a sidebar with five tabs: **Stations**, **Msgs**, **Markers**, **Sources**, and **⚙ (Settings)**. Each has a badge count where relevant.


### Stations Tab

A searchable, sortable list of every station on the map, newest-heard first. The filter bar at the top lets you narrow it down: a **search box** (matches callsign or comment text), a **source** dropdown (All / Direwolf / APRS-IS), and a **type** dropdown (All / Mobile / Fixed / Weather / Digi / iGate). Each list row shows the symbol, callsign, source badges, comment, how long ago it was heard, and its coordinates. Click a row to pan the map to that station.


### Messages Tab (Msgs)

APRS can carry short text messages, and this tab is where you read and send them. Received messages appear in the list, unread ones marked with a green edge. To send one, use the **SEND APRS MESSAGE** form at the bottom:

| Field | What to enter |
| --- | --- |
| **To callsign** | The station you're messaging (example: `W8ABC`). |
| **Message text** | Your message. APRS caps a single message at **67 characters** — the box won't let you exceed it. |
| **Via** | The radio path to send through — **Via Direwolf** (over the radio, via APRS Command). |

Click **Send** to transmit. A small status line reports whether it went out. Note that sending an APRS message goes out over the air on amateur radio, so it requires a properly licensed station and callsign set up in the Settings tab.


### Markers Tab

Here you drop your own reference pins on the map — things APRS won't beacon, like the EOC, shelters, and command posts. In the **ADD MARKER** section:

1. Type a **Label** (for example `Shelter A`).
2. Pick a **Type** from the dropdown — 🏛 EOC, 🏠 Shelter, 🚐 Staging Area, 🎯 Command Post, 🏥 Medical, 📡 Repeater, 🔥 Fire / Hazmat, 🚔 Law Enforcement, or 📌 Custom.
3. Set the location: either type **Latitude** and **Longitude**, or click **🗺 Pick on Map** and then click the spot on the map.
4. Optionally add **Notes**.
5. Click **+ Add Marker**. The pin appears immediately and is listed under **PLACED MARKERS**.

Your placed markers persist on the map. **🗑 Clear All Markers** removes them all at once.


### Sources Tab

A status panel for each data feed — **Direwolf RF** and **APRS-IS** — showing whether each is connected, its address, and how many stations it's supplying. A **⟳ Poll** button on each forces an immediate check. At the bottom, the **MERGED DATASET** box summarizes how the sources combined: total unique stations, how many were seen by both sources, and how many came from each source alone. For APRS-IS you can paste an optional **aprs.fi API key** to enable the internet feed (leave it blank to keep APRS-IS off).


### Settings Tab (⚙)

Everything about how the map behaves and where it looks for data:

| Section | What you set |
| --- | --- |
| **My Station** | Your own callsign, latitude, and longitude, plus a **Center on Station** button. If the Pi has a live Global Positioning System (GPS) fix, these fill in automatically. |
| **APRS Sources** | The address and port where the RF feed lives (the RF/Direwolf host and port). |
| **Display** | Auto-refresh interval (15s up to Manual only), map-tile info, the **station age threshold** (how many minutes counts as "fresh"), the range-ring radius in kilometers, whether to show emoji symbols or plain dots, and whether to show callsign labels. |
| **Legend** | A reference key for the age colors (fresh/aging/old), your station, overlays, and the source border colors. |


## Troubleshooting

- *The map background is blank but markers still show.* That's the offline caveat: the base map tiles couldn't load from the internet. Your station data is fine. Have an administrator download offline tiles onto the Pi (the `download_tiles.sh` step), then switch to them with the map's layer control.
- *No stations appear at all.* Check the **Sources** tab. If Direwolf shows disconnected, the radio feed isn't reaching the map — confirm the addresses/ports in **Settings → APRS Sources** and that Direwolf/APRS Command is running. With no internet, APRS-IS will be empty by design.
- *A station I expect isn't showing.* It may not have beaconed recently, may be out of radio range (and APRS-IS is off), or may be filtered out. Clear the filters on the **Stations** tab and click **⟳ Refresh**.
- *Everything looks faded/gray.* Those stations simply haven't been heard recently. If they're all gray, your feeds may have stopped — check the **Sources** tab and refresh.
- *I can't send an APRS message.* Sending needs a licensed station: set your **callsign** in **Settings → My Station**, keep messages under 67 characters, and make sure the **Via** feed (Direwolf) is actually connected.
- *APRS-IS stays empty.* It needs internet and an **aprs.fi API key** entered on the **Sources** tab. Without both, the internet feed stays off — which is expected in a no-internet deployment.
- *My SARTopo overlay isn't visible.* Confirm you imported it on the **SARTopo Import** page, then turn on the **🗺 SARTopo** layer button on the map.


# 14. GPS-Tracked Resource Map

*A live map of where every resource on your incident actually is — each one a colored pin showing its status — with three easy ways to set a position, including one-tap Global Positioning System (GPS) from a phone in the field.*

> **QUICK VERSION** — Open the **Resource Map**, pick your **incident** from the dropdown, and every resource with a position appears as a colored pin (green = available, blue = staging, dark blue = assigned, red = out of service). Click a resource in the sidebar — or a pin on the map — to open **Set Position**, then use **device GPS**, **click the map**, or **type coordinates**, and **Save**. Turn on **Auto-refresh 30s** to watch positions update as teams move.


## What This Is / What It Is For

The **Resource Map** shows the current Global Positioning System (GPS) positions of all the resources on your active incident — engines, teams, staging areas, whatever is on your resource board — so the Operations Section can see the whole picture on a map instead of reading a list of coordinates. Each resource is a color-coded pin, and its color reflects its current status at a glance.

The resources come straight from your incident's **T-card board** (the Incident Command System, ICS, resource-tracking cards). Anything tracked there can be placed on this map. Resources that don't have a position yet aren't lost — they're listed in the sidebar with a dashed-circle marker and a "No GPS" note, so you can see exactly what still needs to be located and positioned.

> **ONE SHARED SET OF RESOURCES** — This map doesn't have its own separate resource list. It reads the same resources your incident already tracks. Add a resource on the T-card board and it shows up here ready to be positioned; update its status there and its pin color changes here.


## Picking an Incident and the Top Bar

The map is always about one incident at a time. The **top bar** holds the controls:

| Control | What it does |
| --- | --- |
| **Incident selector** (dropdown) | Choose which incident's resources to show. Your last choice is remembered, so the map reopens where you left off. |
| **📍 My Location** | Drops a marker at your own device's GPS position and zooms to it — handy for checking the map lines up with where you actually are. |
| **↺ Refresh** | Reloads all resource positions from the server right now. |
| **📡 Repeaters** | Overlays repeaters from the FieldCommand Repeater Database on the map (toggle on/off). |
| **Auto-refresh 30s** (checkbox) | When ticked, the map reloads positions automatically every 30 seconds. Use it when resources are moving and updating their locations. |
| **T-Cards** / **← Dashboard** | Links back to the resource board and the main dashboard. |

> _[Figure: The Resource Map with the incident selector open in the top bar and several colored resource pins on the map]_


## Reading the Pins

A resource that has a position is drawn as a **teardrop pin** with a letter in the middle — the first letter of its resource type (E for Engine, T for Team, and so on) — so you can tell kinds of resources apart without clicking. The pin's color is its status. A resource **without** a position shows instead as a **dashed circle**, both in the sidebar and (where a location is inferred) on the map, marking it as "not placed yet."

| Color | Status | Plain meaning |
| --- | --- | --- |
| 🟢 Green | **Available** | Ready to be assigned. |
| 🔵 Blue | **Staging** | Waiting at a staging area, held in reserve. |
| 🔵 Dark blue | **Assigned** | Given a job and working it. |
| 🟠 Amber | **En Route** | On the way to an assignment. |
| 🔴 Red | **Out of Service** | Not currently usable (out of service). |
| ⭕ Dashed circle | **No GPS yet** | The resource exists but hasn't been positioned. Click it to set a location. |

The **Legend** in the lower-left of the map repeats this color key and reminds you that ✕ / a dashed marker means "no GPS yet" and that clicking any pin lets you edit it. When more than one resource is positioned, the map automatically zooms to fit them all in view.


## The Sidebar List

On the right, the **🚒 RESOURCES** sidebar lists every resource on the incident. Its header shows a count like *“7/12 have GPS”* — meaning 7 of your 12 resources are positioned and 5 still need placing. Each row shows the resource name, a status dot, its type and status, its assignment (if any), personnel count, and — if positioned — its coordinates and location label with a "last updated" time. Rows with a position have a **green** left edge; rows without one have a **gray** edge and read *“No GPS — click to set position.”* Click any row to open the Set Position window for that resource. The **Set All…** button is a reminder of how to place resources (click a resource, or use the map-click method).


## Setting a Resource's Position

Click a resource — in the sidebar, or its pin's **✏ Update Position** button on the map — to open the **Set Position** window. It offers three ways to fix a location, so you can use whichever fits the situation:

| Method | How to use it | Best for |
| --- | --- | --- |
| **📍 Use Device GPS** | Click it and the browser reads **this device's** GPS. The coordinates fill in and it shows the accuracy (± meters). | A field operator standing at the resource, using a phone or tablet. |
| **🗺 Click Map to Place** | Click it; the window closes and the cursor becomes a crosshair. Click the spot on the map to drop the resource there. | Command or Planning placing a resource at a known point on the map. |
| **Type coordinates** | Type the decimal **Latitude** and **Longitude** straight into the boxes. | A position read off a paper map, a handheld GPS, or a radio report. |

> **“DEVICE GPS” MEANS THE DEVICE YOU'RE HOLDING** — **📍 Use Device GPS** reports the position of whatever device has this page open — so it's only useful when that device is physically **at** the resource. If you're back at the EOC placing a team that's miles away, use **Click Map to Place** or type the coordinates instead.

You can also add an optional **Location Label** — a plain-language description like "Division Alpha staging area" — that shows under the coordinates so people don't have to read raw numbers. When the position looks right, click **Save Position**; the pin appears on the map immediately. **Clear GPS** removes the position (the resource goes back to "no GPS"), and **Cancel** closes the window without changes. The window checks your numbers and won't save coordinates that are out of range or blank.

> _[Figure: The Set Position window with Use Device GPS and Click Map to Place buttons, coordinate fields, and a Location Label]_


## My Location, Auto-refresh, and Repeaters

Three top-bar tools round out the map. **📍 My Location** simply marks and zooms to where **you** are — a quick sanity check that the map matches reality. **Auto-refresh 30s** keeps the whole map current on its own, reloading every 30 seconds; leave it on during active operations so moving resources update without you clicking Refresh. **📡 Repeaters** paints nearby repeaters from your Repeater Database onto the map, color-coded by mode, with amber for repeaters flagged for emergency communications (ARES/RACES/SKYWARN) — useful context for planning where teams will have radio coverage. If no repeaters load, import a RepeaterBook file on the Repeater Database page first.


## The Public-Safety Resource Map Variant

A second, related screen — the **Public Safety Resource Map** — works the same way but is built for tracking **public-safety units** rather than ICS T-card resources, and it lets you draw **zones** on the map. Reach for this one when you're plotting law-enforcement, fire, EMS, or other public-safety units alongside your own resources.

Instead of reading from the T-card board, you add units yourself on its **+ Add** tab, entering a **Radio ID / Unit #**, a name/description, a **Type** (Law Enforcement, Fire, EMS, EOC Staff, Public Works, Volunteer, ARES/RACES, Search & Rescue, or Other), a **Status** (Available, Busy/Engaged, Staged/Standby, or Out of Service), and a position (typed or **🗺 Pick on Map**). Each unit becomes a colored dot with a type icon. The **Zones** tab lets you outline areas — pick a **name** and a **color** (blue Operations, green Clear/Safe, amber Caution, red Danger/Restricted, purple Special Ops), then click the map to drop corners and **Finish Zone** to close the shape. It's the tool for marking sectors, evacuation zones, and restricted areas.

> **TWO MAPS, TWO JOBS** — The main **Resource Map** tracks your incident's ICS resources straight from the T-card board and centers on GPS positioning. The **Public Safety Resource Map** is for hand-entered public-safety units and drawing zones. They look alike but hold different data — use the one that matches what you're tracking.


## Troubleshooting

- *The map is empty after I pick an incident.* That incident may have no resources on its T-card board yet, or none of them are positioned. Check the sidebar count — if it reads "0/0," add resources on the T-card board first; if it reads "0/5," the resources exist but need positions set.
- *A resource isn't on the map but is in the sidebar.* It has no GPS position yet (gray edge, "No GPS"). Click it and set a position with device GPS, a map click, or typed coordinates.
- *“Use Device GPS” gives the wrong spot or an error.* It reads the device you're holding, which must be at the resource and have location services allowed in the browser. To place a distant resource, use **Click Map to Place** or type the coordinates instead.
- *Positions aren't updating as teams move.* Turn on the **Auto-refresh 30s** checkbox, or click **↺ Refresh**. Remember the map only shows positions that have actually been re-sent to the server.
- *“Coordinates out of range” when I save.* A typed latitude/longitude is invalid (latitude must be −90 to 90, longitude −180 to 180). Re-check the numbers — and don't forget the minus sign on a west longitude.
- *The Repeaters button shows nothing.* No repeater data is loaded. Import a RepeaterBook CSV on the **Repeater Database** page, then toggle **📡 Repeaters** again.
- *I meant to use the public-safety map with units and zones.* That's the separate **Public Safety Resource Map**. Open it instead — the main Resource Map only shows ICS T-card resources and doesn't draw zones.


# 15. Incident Command System (ICS) Platform Overview — Five-Section Structure

*How FieldCommand organizes an incident into the five ICS sections, how the shared ICS form page works, and how General Info fills the header on every form at once.*

> **QUICK VERSION** — The Incident Command System (ICS) splits an incident into five sections: **Command, Operations, Planning, Logistics, and Finance/Admin**. FieldCommand follows that structure — the form buttons in an incident are grouped by section. Fill in the **📋 General Info** screen once per operational period and it copies the incident name, dates, commander, and section chiefs onto every ICS form automatically. Open any form, type, and it saves on its own; sign the **Prepared By** and **Approved By** lines right on the touchscreen.


## What This Is / What It Is For

The Incident Command System (ICS) is the standard way the United States organizes any incident, defined by the National Incident Management System (NIMS). Its core idea is simple: no matter how big or small the event, the work is divided into five sections, each with a clear job. FieldCommand implements that full five-section structure so your paperwork and your organization chart line up with what every trained responder expects.

This chapter explains what the five sections are, which FieldCommand forms belong to each, and the two screens you'll touch most when doing ICS paperwork — the shared **ICS form page** (where you fill out any individual form) and the **General Info** screen (where you type the shared header once instead of on every form).


## The Five ICS Sections

Every incident, from a one-operator net to a full county activation, is organized around these five sections. A small incident may have one person wearing several of these hats; a large one staffs each separately. FieldCommand keeps the structure the same either way.

| Section | Plain-language job | Key FieldCommand forms |
| --- | --- | --- |
| **Command** | Sets the objectives and is in charge of the whole incident. Led by the Incident Commander (IC). | ICS-201 Incident Briefing, ICS-202 Objectives, ICS-207 Organization Chart, ICS-208 Safety Message/Plan |
| **Operations** | Does the actual field work — the teams, crews, and resources carrying out the plan. | ICS-204 Assignment List, ICS-211 Check-In List, ICS-219 Resource Status (T-Cards), ICS-210 Resource Status Change |
| **Planning** | Tracks the situation and resources, and assembles the Incident Action Plan (IAP) for the next period. | ICS-203 Organization Assignment List, ICS-209 Incident Status Summary, ICS-215 Operational Planning Worksheet, ICS-215A IAP Safety Analysis |
| **Logistics** | Provides everything the incident needs — communications, medical support, facilities, supplies, and vehicles. | ICS-205 Radio Communications Plan, ICS-205A Communications List, ICS-206 Medical Plan, ICS-213RR Resource Request |
| **Finance / Admin** | Tracks time, costs, and records so the incident can be paid for and documented. | ICS-214 Activity Log, ICS-220 Air Operations Summary, ICS-221 Demobilization Check-Out |

In an incident's workspace (Chapter 5), the ICS form buttons are laid out under colored dividers with these same section names, plus a **Communications Unit** group for the ICS-213 General Message and the ICS-309 Communications Log. A record added in one section is visible everywhere it's relevant — a resource entered in Operations shows up in Logistics and Finance too, because they all read from the same incident.


## Command Staff vs. General Staff

Two roles sit beside the Incident Commander rather than inside a section. Knowing the difference keeps your ICS-203 organization chart correct.

| Group | Who's in it | Reports to |
| --- | --- | --- |
| **Command Staff** | Safety Officer (SOFR), Public Information Officer (PIO), and Liaison Officer (LNO) | Directly to the Incident Commander — **not** to a section |
| **General Staff** | The four Section Chiefs — Operations (OSC), Planning (PSC), Logistics (LSC), and Finance/Admin (FSC) | The Incident Commander; each runs their own section |

> **WHO DEVELOPS A FORM ISN'T ALWAYS WHO USES IT** — A few forms are prepared by one section and used by another. The **ICS-204 Assignment List** is developed by the Resources Unit in Planning but distributed to and used by Operations supervisors. The **ICS-205, 205A, 206, and 309** are developed by the Communications and Medical units (which live in Logistics) and then folded into the IAP by Planning. The **ICS-214 Activity Log** is kept by supervisors in every section, and Finance/Admin collects them for the cost record. FieldCommand doesn't force this on you — it's simply how the standard forms flow.


## The Shared ICS Form Page

Every individual ICS form — 201, 202, 204, 205, and the rest — opens on the same **ICS form page**. You reach it by clicking a form button inside an incident. The page top shows a badge with the form number (like **ICS-204**), the form's full name, and a **Form Variant** selector; on the right are **💾 Save** and **🖨 Print** buttons and a link back to the incident. A matching action bar with **💾 Save Form** and **🖨 Print / Export** sits at the bottom.


### Form Variants

The **Form Variant** pills — **FEMA**, **USCG**, and **NWCG** — pick which agency's version of the form you're filling out. Most all-hazards and emergency-communications work uses **FEMA**. The page defaults to the variant set on the incident (which itself came from your Setup default), so you usually don't touch this. Change it only when your served agency specifically expects a different one.

| Variant | Full name | When to use it |
| --- | --- | --- |
| **FEMA** | Federal Emergency Management Agency | The all-hazards default — the right choice for most incidents |
| **USCG** | United States Coast Guard | Coast Guard incidents that use the CG form numbers |
| **NWCG** | National Wildfire Coordinating Group | Wildland-fire incidents that use the wildfire form set |


### Saving and Digital Signatures

Click **💾 Save** (top or bottom) to store the form; a **✓ Saved** indicator confirms it. Forms are tied to the incident and the operational period, so the same form number for a different period is a separate record.

Fields for **Prepared By** and **Approved By** are special — each shows a **Sign** button. Tap it and a signature pad appears; sign with a finger, stylus, or mouse, then tap **✓ Accept Signature** to capture it onto the form (or **✕ Clear signature** to redo it). The captured signature prints on the form, so an on-site IAP package carries real approvals, not just typed names.

> **PRINT MEANS PRINT OR PDF** — The **🖨 Print** / **🖨 Print / Export** button opens a clean, print-formatted version of the form. From the print dialog you can send it to a printer or save it as a Portable Document Format (PDF) file — the same button does both.


## General Info — Enter Once, Fill Every Form

The single biggest time-saver in the ICS section is the **General Information** screen. Reached from the gold **📋 GENERAL INFO** button in an incident's operational-period bar, it collects the header information that would otherwise be re-typed on 20-plus forms — and copies it to all of them at once. The header even states it plainly: *enter once, auto-fills all 29 ICS forms.*

A period selector (◀ **OP PERIOD** ▶) at the top right sets which operational period you're editing, because this information changes from one shift to the next. The screen is divided into labeled sections:

| General Info section | What you enter |
| --- | --- |
| 🚨 **Incident Identity** | Incident Name (required), Incident Number, Type, Jurisdiction, Location/Address, Latitude, Longitude, and the ICS Variant |
| 🕐 **Operational Period** | The From and To date/time for this period |
| ⭐ **Command** | Incident Commander (IC), Deputy IC, Safety Officer (SO), Public Information Officer (PIO), and Liaison Officer (LNO) |
| ⚙️ **General Staff — Section Chiefs** | Operations (OSC), Planning (PSC), Logistics (LSC), and Finance/Admin (FSC) Section Chiefs |
| 👤 **Key Unit Leaders** | Resources (RESL), Situation (SITL), Documentation (DOCL), Demobilization (DMOB), Communications (COML), and Medical (MEDL) Unit Leaders, plus Prepared By and Approved By — used to auto-fill signature blocks |
| 🌤 **Weather** | Temperature, Wind, Humidity, Sky/Conditions, Sunrise, Sunset, and a Forecast box — with a **Fetch NWS** button that pulls the current National Weather Service forecast when the internet is up |

1. Open **📋 GENERAL INFO** from the incident's period bar (or the **📋 General Info** link on any ICS form page).
2. Confirm the **OP PERIOD** selector shows the right period.
3. Fill in the sections top to bottom — at minimum the **Incident Name** and the command/staff names.
4. Click **💾 SAVE & PROPAGATE TO ALL FORMS**. A green confirmation shows the save time, and every ICS form for this period now carries these values in its header.
5. Starting the next shift? Click **📋 Copy to Next Period** to carry the names forward while clearing the period-specific dates and weather.

> **IT ALSO SAVES ITSELF** — General Info auto-saves a few seconds after you stop typing, and it keeps a local copy on your device so nothing is lost if the connection drops. The **Fetch NWS** weather pull and the sunrise/sunset calculation need latitude and longitude filled in first.


## Single Incident Commander vs. Unified Command

The command structure is documented on the **ICS-203 Organization Assignment List**, and General Info's Command section feeds it. For a **Single Incident Commander** incident, one IC's name sits at the top of the chart. For a **Unified Command** incident, the participating agencies are listed together at the command level. FieldCommand handles both structures identically — the ICS-203, ICS-202, and every downstream form behave the same way regardless. See Chapter 5 for how to set each one up when you create the incident.


## Troubleshooting

- *A form opens with a blank header — no incident name or dates.* Fill in and save the **📋 General Info** screen for that operational period. The header on individual forms is populated from General Info; if you skipped it, the fields come up empty.
- *I updated a name in General Info but an old form still shows the old name.* Re-save General Info with **💾 SAVE & PROPAGATE TO ALL FORMS**, then reopen the form. Propagation happens on save; a form left open from before won't refresh on its own.
- *The wrong form variant is showing (FEMA/USCG/NWCG).* The page uses the incident's variant by default. Click the correct **Form Variant** pill at the top of the form, or change the incident's variant from its workspace (Chapter 5).
- *The Sign button won't capture my signature.* Sign inside the pad area, then tap **✓ Accept Signature** — the signature isn't saved until you accept it. Use **✕ Clear signature** to start over. Signatures are available on the Prepared By and Approved By fields.
- *Fetch NWS says weather is unavailable.* The National Weather Service pull needs an internet connection and requires the incident **Latitude** and **Longitude** to be filled in first. Offline, type the weather in by hand.
- *I changed the period selector and my entries disappeared.* Each operational period has its own General Info. Switching periods loads that period's data; your earlier entries are safe under the period you typed them in. Use **📋 Copy to Next Period** to carry names forward.
- *My form didn't save.* Watch for the **✓ Saved** indicator after clicking **💾 Save**. If it doesn't appear, confirm you're connected to the FieldCommand Wi-Fi and the incident service is running, then save again.


# 16. Incident Command System (ICS) Operations Section — T-Card Resource Board

*The Resource Board — a live card wall of every person, vehicle, radio, and piece of gear on the incident, with a NIMS typing library behind it so everyone means the same thing by "Engine" or "Crew".*

> **QUICK VERSION** — Open **Resources** from the top navigation. Click **+ Add Resource**, type a name, pick a **Type** and **Status**, and **Save** — a card appears on the board. Click the colored **status pill** on any card to move it through Available → Assigned → Staging → Out of Service → Demobilized. Use the **filter bar** to narrow a busy board, and **Export CSV** / **Import CSV** to move the whole list in or out.


## What This Is / What It Is For

During an incident, the Operations Section has to know — at a glance — what it has to work with. How many radios are on the shelf? Which vehicle is already out on a task? Is the generator running or broken? The paper way to do this is the **T-card rack**: a physical board full of little cards, one per resource, that you slide between labeled pockets as things change. The **Resource Board** in FieldCommand is the digital version of that rack. Every resource is a **card**; the whole team sees the same board on their own screens, and it updates the moment anyone changes it.

Think of it as a shared, always-current inventory of everything and everyone assigned to the incident. It answers three questions at once: **what do we have, what state is it in, and where is it.** Because it lives on the server, there is no arguing over which printout is the latest — the board is the latest.

> **TWO PAGES, ONE JOB** — This chapter covers two linked screens. **Resources** (the board, `resources.html`) is the live list of your actual gear and people. The **NIMS Resource Typing Library** (`resource_types.html`) is the reference dictionary that defines what each standard resource *type* means. You track real resources on the first; you look up or add type definitions on the second.


## Opening the Resource Board

1. On any device connected to the FieldCommand Wi-Fi, open a web browser.
2. Go to the dashboard at **http://192.168.50.1** and click **Resources** in the top navigation bar (it sits between Roster and Tactical).
3. The **📦 RESOURCE BOARD** page opens. Across the top is a row of **count tiles**; below that a **filter bar**; below that the cards themselves, grouped by type.

> _[Figure: The Resource Board with its count tiles across the top, the filter bar, and resource cards grouped under type headings]_


## Reading the Count Tiles

The strip of boxes at the very top is a running tally of the whole board. It updates automatically as cards are added or their status changes, so it doubles as an at-a-glance status report for the Operations Section Chief.

| Tile | What it counts |
| --- | --- |
| **Available** | Resources ready to be assigned right now |
| **Assigned** | Resources currently out on a task |
| **Staging** | Resources standing by in a staging area, not yet tasked |
| **Out of Service** | Resources that are broken, resting, or otherwise unusable |
| **Demobilized** | Resources that have been released from the incident |
| **Total** | Every resource on the board, regardless of status |


## What a Resource Card Shows

Each card is one resource. A colored bar down the left edge tells you its status at a glance (green = available, amber = assigned, blue = staging, red = out of service, gray = demobilized). The card shows only the fields you filled in — blank fields are simply left off, so a bare-bones card stays clean.

| On the card | What it means |
| --- | --- |
| **Name** (with a type icon) | The resource's designation — for example `IC-7300 HF Radio` or `Team Alpha` |
| **Type badge** | The category, shown top-right (Radio, Vehicle, Personnel, and so on) |
| **Owner** | Who owns or brought the resource — often a callsign like `W8XYZ` |
| **Qty** | How many, if more than one (a single item hides this) |
| **Location** | Where the resource physically is right now |
| **Assigned** | The person or callsign it is assigned to |
| **Task** | The job it is doing — for example `Shelter comms` |
| **ID/Serial** | A serial number or asset tag, if you entered one |
| **Contact** | A phone number or contact for the resource |
| **Status pill** | The colored, clickable badge — click it to cycle the status |
| **Updated** | How long ago the card last changed ("5m ago") |


## Adding a Resource

1. Click **+ Add Resource** at the top right of the board. The **ADD RESOURCE** window opens.
2. Type a **Resource Name / Description** — this is the only required field (the placeholder shows an example, `IC-7300 HF Radio`).
3. Pick a **Type** from the dropdown: Personnel, Vehicle, Radio, Generator, Antenna, Computer/Tablet, Medical, Shelter/Tent, Repeater, or Other.
4. Pick a **Status** (defaults to Available). Fill in any of the optional fields — Owner / Callsign, Quantity, Current Location, Assigned To, Assignment / Task, Notes, Identifier / Serial #, Contact / Phone.
5. Click **Save Resource**. The card appears on the board under its type heading, and the count tiles update.

> **ONLY THE NAME IS REQUIRED** — You can add a resource with nothing but a name and fill in the rest later. If you Save with a blank name, FieldCommand reminds you that the name is required — everything else is optional.


## Changing Status the Fast Way

You do not have to open the edit window just to move a resource along. The colored **status pill** on each card is a button. Click it and the status advances one step through the cycle: **Available → Assigned → Staging → Out of Service → Demobilized → back to Available.** The card's left-edge color and the top count tiles update instantly. This is the digital equivalent of sliding a T-card from one pocket to the next.

To change several fields at once — reassign it, move its location, add a task — click **✏ Edit** on the card instead. The same window you used to add it reopens as **EDIT RESOURCE**, pre-filled with what is already there. Make changes and click **Save Resource**.


## Filtering and Searching

On a large incident the board can hold dozens of cards. The **filter bar** narrows it without deleting anything:

- **Type** dropdown — show only one category, such as Radio.
- **Status** dropdown — show only one status, such as Available.
- **Search** box — type any text and the board keeps only cards whose name, owner, location, or notes contain it.
- **Clear** button — resets all three filters and shows the whole board again.

Filters stack: choosing Type = Vehicle **and** Status = Assigned shows only assigned vehicles. The count tiles always reflect the full board, not the filtered view, so they stay a reliable total.


## Removing a Resource

To take a resource off the board entirely, click the red **✕** button on its card and confirm. This deletes the card. If a resource is only leaving the incident — not being deleted from the record — it is usually better to set its status to **Demobilized** (using the status pill) so it stays visible in the history of the board.


## Moving the List In and Out (CSV)

The two buttons at the top left of the board, **⬇ Export CSV** and **⬆ Import CSV**, let you move the whole resource list between FieldCommand and a spreadsheet program. CSV (Comma-Separated Values) is a plain table file that Excel, Google Sheets, and most incident-management systems can read.

**Export CSV** downloads a file called `resources.csv` containing every resource and all its fields — handy for a backup, a printed inventory, or handing data to another system.

**Import CSV** is smarter than a straight paste. After you pick a file, a mapping window opens so you can line up the spreadsheet's columns with FieldCommand's fields:

1. Click **⬆ Import CSV** and choose a `.csv` file from your device.
2. The **IMPORT RESOURCES FROM CSV** window shows the file name, how many data rows it found, and a **Column Mapping** grid.
3. For each FieldCommand field (name, type, status, owner, and so on), the tool guesses the matching spreadsheet column — for example it recognizes "unit name", "agency", or "quantity". Correct any guess using its dropdown, or set it to **(skip)**.
4. Check the **Preview (first 5 rows)** table to confirm the columns line up.
5. Click **Import [N] Resources**. Status words like "deployed" and type words like "engine" are normalized to FieldCommand's standard values automatically. Rows without a name are skipped, and rows that share a serial number update the existing card instead of duplicating it.

> **IMPORT IS FORGIVING** — You do not need to reformat a spreadsheet before importing. The mapping step and the automatic status/type cleanup are built to accept lists exported from other agencies and tools — just check the preview before you commit.


## The NIMS Resource Typing Library

Behind the board sits a reference screen: the **NIMS Resource Typing Library** (`resource_types.html`). National Incident Management System (NIMS) resource *typing* is the nationwide standard that makes "Type 1 Engine" or "Type 2 Hand Crew" mean the same thing to every agency. This library is FieldCommand's copy of those definitions, so when you request or log a resource, everyone is speaking the same language. It draws from the Federal Emergency Management Agency (FEMA) Resource Typing Library Tool (RTLT).

The page lists resource types as expandable cards, grouped and color-coded by mission category — Fire / HazMat, Search and Rescue, Medical / EMS, Law Enforcement, Public Works, Mass Care, Communications, Incident Management, Transportation, Logistics, UAS / Unmanned, and Other.

| Control | What it does |
| --- | --- |
| **Search box** | Filters the library by name, capability, or description text |
| **Category chips** | Click a colored category button to show only that mission area; **All** shows everything |
| **Click a card** | Expands it to reveal the full definition |
| **Expand All / Collapse All** | Opens or closes every card at once |
| **+ Add Custom Type** | Creates your own resource type for something the standard list does not cover |

An expanded card can show several labeled sections: **📖 What It Is** (the plain definition), **📐 Minimum Standards / Specifications**, **✅ Capability Summary**, **📦 When to Order This Resource**, and a red **⚠ Common Confusion / Watch Points** box that flags the mistakes people make with that type. Cards you create yourself carry a **CUSTOM** tag and an edit (**✏**) button.


## Adding a Custom Resource Type

1. On the NIMS Resource Typing Library page, click **+ Add Custom Type**.
2. Fill in **Kind / Name** (required) — for example `Rescue Team` — and optionally a **Type Level** (Type I, Type II, and so on).
3. Pick a **Category** and, if useful, a **Min Personnel** count.
4. Add any of the detail fields: Full Description, Capability Summary, Metrics / Specifications, What It Is, Minimum Standards, When to Order, and Common Confusion / Pitfalls.
5. Click **SAVE RESOURCE TYPE**. It joins the library under its category with a CUSTOM tag, and you can edit or expand it like any other.

> **TYPES ARE DEFINITIONS, RESOURCES ARE REAL THINGS** — Adding a type to the library does **not** put a resource on the board. The library defines what a "Rescue Team" is; the board tracks your actual Rescue Team, its status, and where it is. Define the type once, then add as many real resources of that type as you have.


## Troubleshooting

- *The board is empty or says "No resources found".* Either nothing has been added yet, or a filter is hiding everything. Click **Clear** in the filter bar; if it is still empty, add a resource with **+ Add Resource**.
- *I can't Save a new resource.* The **Resource Name / Description** is required. Type a name, then Save again — every other field can be left blank.
- *A card vanished after I changed a filter.* It is filtered out, not deleted. Click **Clear** to show the whole board. The count tiles still include it, so compare the Total tile to what you see on screen.
- *Clicking the status pill jumped past the status I wanted.* The pill cycles one step per click through the five statuses; keep clicking to come back around, or use **✏ Edit** and pick the exact status from the dropdown.
- *My CSV import brought in odd type or status values.* Re-open **⬆ Import CSV**, and in the Column Mapping step make sure the Type and Status columns point at the right spreadsheet columns. Unrecognized values are kept as-is; fix them by editing the affected cards.
- *The NIMS Resource Typing Library shows "Could not load resource types — API offline".* The library loads from the FieldCommand server. Confirm your device is on the FieldCommand Wi-Fi and the server at 192.168.50.1 is running, then reload the page.
- *A resource left the incident but I want to keep the record.* Don't delete it — set its status to **Demobilized** with the status pill. Deleting (the red ✕) removes it permanently.


# 17. Incident Command System (ICS) Planning Section & Incident Action Plan (IAP) Assembly

*Gather the operational period's ICS forms into one Incident Action Plan, check how complete it is, build the morning briefing sheet, and turn the whole package into a single PDF anyone can print.*

> **QUICK VERSION** — Open **IAP Assembly** from an incident. Pick the **Operational Period**, tick the forms to include (the required ones start ticked), then click **📄 Save as PDF** to download the whole plan as one file. For a merged PDF built straight from your saved forms, use **IAP Compile** instead. For the morning briefing, open the **ICS-204A Briefing Sheet** and print it landscape.


## What This Is / What It Is For

An **Incident Action Plan (IAP)** is the written game plan for one **operational period** — usually one shift. It says what the objectives are, who is doing what, how everyone will talk to each other, and what to do if someone gets hurt. In the Incident Command System (ICS), you don't write the IAP as one long document; you fill out a set of standard **ICS forms** and then **assemble** the right ones into a package. FieldCommand's Planning Section tools do that assembling for you.

There are three linked screens, and this chapter covers all three: the **IAP Assembly** page (choose forms and export the plan), the **IAP Compile** page (merge your saved forms into one PDF), and the **ICS-204A Briefing Sheet** (a one-page summary of every assignment for the operational period briefing). Each individual form is filled out on its own screen; these pages gather the finished forms together.

> **FILL THE FORMS FIRST, ASSEMBLE SECOND** — These pages don't create the content of a form — they collect forms that already exist. Complete your ICS-202, 203, 204, and the rest on their own pages, then come here to bundle them. A form you never filled out simply shows as "not saved" here.


## The IAP Assembly Page

Open the **INCIDENT ACTION PLAN — ASSEMBLY** page from an incident. It is split into two columns. The **left column** is the form checklist; the **right column** shows a live preview of the IAP cover page plus the options and export tools.

> _[Figure: The IAP Assembly page: form checklist on the left, cover-page preview and options panel on the right, export buttons across the top]_

The left column lists the full ICS form set in IAP order. Each row shows the form number (for example **ICS-204**), its title, a colored tag naming the section that owns it (Command, Operations, Planning, Logistics, or All), a **status label**, and an **Open →** or **Edit →** link that jumps to that form.

| Status label | What it means |
| --- | --- |
| **Saved** | The form has been filled out and saved for this incident and period — a green checkmark |
| **Required — not yet saved** | This form is required for a complete IAP but hasn't been saved yet |
| **Not started** | An optional form that hasn't been filled out |

To include or exclude a form, tick or untick its **checkbox** (or click anywhere on the row). Included rows turn green. The forms usually required for a complete IAP — **ICS-201, 202, 203, 204, 205,** and **206** — start ticked for you; add optional forms like the **ICS-207** organization chart or **ICS-208** safety message as your incident needs them.


## The Cover Page, Period, and Variant

The right column's top box is a **live cover-page preview**. It fills in from your organization setup and the incident record, so you can see how the finished cover will read — your organization's name and logo, the incident name, the operational period, and the Incident Commander.

Below the preview, the **IAP OPTIONS** box holds two dropdowns:

| Option | What it does |
| --- | --- |
| **Operational Period** | Which shift's forms to assemble (Period 1 through 5). Changing it reloads the checklist so each row's status reflects that period. |
| **ICS Form Variant** | Which agency's version of the forms to use — **FEMA**, **USCG** (United States Coast Guard), or **NWCG** (National Wildfire Coordinating Group). Pick the one your served agency expects. |


## The Completeness Bar

Under the options is a **COMPLETENESS** bar. It tracks only the **required** forms and tells you, in plain numbers, how ready the IAP is — for example "4 of 6 required forms saved (67% complete)." The bar turns green at 100%. Use it as a quick pre-flight check before you distribute the plan: if it isn't full, some required form still needs finishing, and the checklist shows which one (look for the red **Required — not yet saved** labels). The **QUICK LINKS** box below jumps straight to the first several forms.


## Getting the IAP Out — Three Buttons

The three buttons in the page header are three ways to produce the finished plan. They differ in where the work happens and how reliable the page layout is.

| Button | When to use it | What happens |
| --- | --- | --- |
| **🖨 Print IAP** | A printer is on the network or attached to your device | Opens a print-ready cover page and table of contents in a new browser tab and launches the print dialog. Allow pop-ups for this to work. |
| **📄 Save as PDF** *(recommended)* | No printer on site, or the plan must go off-site, be emailed, or archived | Sends your selected forms to the FieldCommand server, which builds a proper 8.5" × 11" PDF and downloads it as `IAP_[Incident]_Period[N]_[Date].pdf`. Opens in any PDF reader anywhere; layout is guaranteed. |
| **💾 Save as HTML** *(fallback)* | The server is unreachable, or you want a lightweight file with no server call | Downloads a self-contained web-page version straight from the browser. Open it and use File → Print. Page layout can vary by browser — use PDF when layout matters. |

> **USE SAVE AS PDF FOR ANYTHING THAT LEAVES THE ROOM** — The PDF is built on the Pi server, comes out at a guaranteed letter-size layout, and opens on any device — so it is the right choice for emailing the Emergency Operations Center (EOC), copying to a USB drive, or archiving. Reach for **Save as HTML** only if the PDF button fails.


## The IAP Compile Page

Where IAP Assembly is form-by-form, the **IAP PDF Compile** page (`iap_compile.html`) is built to merge every completed form of the types you pick into one continuous PDF, in the standard IAP order. This is the fuller compiler.

1. Open **IAP Compile** from the dashboard. Choose an **incident** and a **period** (or **All Periods**) from the dropdowns at the top.
2. The **Forms for This IAP** list shows each form type, how many saved copies exist, and whether it belongs in a standard IAP. Form types that have saved data are selectable; ones with no data are grayed out.
3. Saved IAP-order forms are pre-ticked. Adjust the selection by clicking rows, or use the **All** / **None** buttons.
4. In **Compile Options**, choose whether to **Include title page** and keep **IAP order** (202→203→204→205→206…), and optionally type a **Prepared By** name (the Planning Section Chief).
5. Check the **Summary** box — it shows how many form types and how many total pages are selected.
6. Click **📄 Download IAP PDF**. The Pi merges the forms and the file downloads. It can be printed from any device on the network or saved for off-site printing.

> **IF THE PDF COMPILER ISN'T AVAILABLE** — If the page shows a red banner reading "PDF compiler not available on this server," the PDF libraries aren't installed on the Pi. The banner names the exact command to run on the Pi (installing `reportlab` and `pypdf`), after which you restart the ICS service. Until then, use **Save as HTML** on the IAP Assembly page as a stand-in.


## The ICS-204A Briefing Sheet

The **ICS-204A Briefing Sheet** (`briefing_204a.html`) is a single-page rollup of every assignment for the operational period, built for reading aloud at the morning briefing. It gathers all the **ICS-204 Assignment Lists** you've saved and groups them by **branch**, so the whole tactical picture fits on one screen — no flipping between forms.

At the top, a **summary bar** counts the Branches, Divisions/Groups, Resources, and Personnel in the plan. Each branch appears as its own card, color-coded by the standard ICS branch colors, with a table underneath:

| Column | What it shows |
| --- | --- |
| **Division / Group** | The division or group name (or staging area) |
| **Supervisor** | Who is in charge of that division or group |
| **Tactical Channel** | The radio channel that division works on |
| **Resources Assigned** | Chips listing each resource, its leader, and personnel count |
| **Work Assignment (brief)** | A short summary of the tactical task |

The **Branch** filter narrows the view to one branch, and the **Show empty divisions** checkbox reveals divisions with nothing assigned yet (they are hidden by default to keep the sheet tight). When you're ready, **🖨 Print Landscape** produces a clean, printer-friendly page — it prints in landscape so the wide assignment tables fit — with the on-screen buttons and colors removed. Use **↺ Refresh** to pull in any ICS-204 changes made since you opened the page.

> **NO 204S YET?** — If the briefing sheet says "No ICS-204 forms found," the Assignment Lists for this incident and period haven't been created. The page gives you a link straight to a new ICS-204. The briefing sheet only ever reflects what's already in the ICS-204s.


## Troubleshooting

- *The IAP Assembly page says "No incident selected."* These pages work on a specific incident. Open IAP Assembly from an incident page (or pick the incident from the dropdown on IAP Compile) so it knows which forms to gather.
- *A form I completed shows as "not saved" here.* Check that you saved it for the **same operational period** you have selected here — the status is per period. Switch the **Operational Period** dropdown to the right shift, or open the form and confirm it saved.
- *The completeness bar won't reach 100%.* One or more **required** forms haven't been saved. Look for the red **Required — not yet saved** labels in the checklist and finish those forms.
- *Clicking Print IAP did nothing.* The print view opens in a new browser tab, which your browser may have blocked. Allow pop-ups for the FieldCommand address and click **🖨 Print IAP** again.
- *Save as PDF failed with an error.* The PDF is generated on the Pi server. Confirm you're connected to the FieldCommand Wi-Fi and the server is running. As a fallback, use **💾 Save as HTML**, or check the IAP Compile page for the red "PDF compiler not available" banner and follow its instructions.
- *The IAP Compile Download button is grayed out.* You must select at least one form type that has saved data, and the PDF compiler must be available on the server. Tick a form type that shows a saved count, and resolve any red compiler banner first.
- *The Briefing Sheet is missing resources or supervisors.* It only shows what's entered in the ICS-204 forms. Open the relevant ICS-204 (use the **✏ Edit** link on the row), fill in the division supervisor, channel, and resources, save, then click **↺ Refresh**.


# 18. Federal Emergency Management Agency (FEMA) Public Assistance (PA) Cost Documentation

*Track every reimbursable dollar — labor, equipment, materials, and contracts — tied to the active incident, and roll it into a Project Worksheet summary you can hand to your state emergency management agency.*

> **QUICK VERSION** — Open **FEMA Costs**, pick your **incident**, then log costs under the four tabs: **Force Account Labor**, **Force Account Equipment**, **Materials / Contracts**, and **Project Worksheet**. Each entry's total is figured for you and rolled into the totals bar at the top. When the incident is over, fill in the Project Worksheet details and click **📄 Export PW** to get a summary for your state emergency management agency.


## What This Is / What It Is For

When a disaster is federally declared, the **Federal Emergency Management Agency (FEMA)** can reimburse eligible responders for money they spent responding — through a grant program called **Public Assistance (PA)**. But FEMA only pays back costs you can **document**: who worked and for how long, what equipment ran and at what rate, and what you bought and from whom. This page is where your organization keeps that record while the incident is happening, so the money isn't lost to fuzzy memory weeks later.

FEMA sorts eligible costs into a few buckets, and this page mirrors them exactly: **Force Account Labor** (your own people's time), **Force Account Equipment** (your own vehicles and gear), and **Materials and Contracts** (things you bought or hired). Every entry you make is tied to the **active incident**, and the page adds everything up into a **Project Worksheet (PW)** summary — the document your state passes to FEMA.

> **THIS IS A WORKSHEET, NOT THE OFFICIAL FILING** — FieldCommand helps you organize and total your costs — it does **not** replace the official FEMA Project Worksheet (Form FF-104-FY-21-112), and it does not submit anything. Real filings go through your state or territorial emergency management agency with supporting receipts and records. Review every entry with your Finance Section Chief before submission, and remember costs must be tied to the disaster and not already covered by insurance.


## Opening the Page and Reading the Totals Bar

1. From the dashboard, open **FEMA Costs** (the FEMA PA Cost Documentation page).
2. At the top right, choose your incident from the **Select incident...** dropdown. All costs you enter are stored against that incident.
3. The **totals bar** across the top fills in, and the four tabs become active.

The **totals bar** is a live running tab of the whole incident. It shows four numbers, recalculated every time you add or edit an entry:

| Total | What it sums |
| --- | --- |
| **Force Acct Labor** | Every labor entry, including overtime and fringe benefits |
| **Force Acct Equipment** | Every equipment entry (hours × rate) |
| **Materials / Contracts** | Every material and contract entry |
| **Total Eligible Costs** | The three above, added together — your bottom line |

> _[Figure: The FEMA PA Cost Documentation page with the totals bar on top and the four cost tabs below]_


## Force Account Labor

"Force account" means your own personnel, as opposed to hired contractors. The **👷 Force Account Labor** tab tracks the hours your employees and volunteers worked on the incident. For most regular employees, FEMA reimburses **overtime** hours, not regular time — so the form keeps regular and overtime separate, and it accounts for **fringe benefits** (the percentage on top of wages for things like taxes and insurance).

1. On the Labor tab, click **+ Add Labor Entry**.
2. Fill in the person and their hours. As you type rates and fringe, the **Preview Total** updates live so you can see the calculated cost before saving.
3. Click **SAVE**. The entry joins the table and the totals bar updates.

| Field | What to enter |
| --- | --- |
| **Employee Name** *(required)* | The worker's name, entered Last, First |
| **Position / Title** | Their job title, e.g. Emergency Manager |
| **Department** | Their home department or agency |
| **Date Worked** | The day these hours were worked |
| **Regular Hours** | Regular-time hours on the incident |
| **Overtime Hours** | Overtime hours — usually the reimbursable category for employees |
| **Regular Rate ($/hr)** / **OT Rate ($/hr)** | The hourly pay rates from payroll |
| **Fringe Benefits %** | Fringe as a percentage of wages (defaults to 30) |
| **Notes** | Anything useful — the assignment, watch shift, etc. |

The **Total w/Fringe** column is figured automatically as **(regular hours × regular rate + overtime hours × overtime rate) × (1 + fringe%)**. To fix an entry later, click the **✏** button on its row; the same window reopens with a **Delete** button available.

> **IMPORT HOURS FROM THE ACTIVITY LOG** — The **↓ Import from ICS-214** button pulls the unit leaders out of the incident's saved **ICS-214 Activity Logs** and creates a labor entry for each — a fast head start. It fills in the name and unit and marks where it came from, but leaves the **hours and rates as placeholders**. You must open each imported entry and fill in the actual hours and pay rates before the cost is real.


## Force Account Equipment

The **🚛 Force Account Equipment** tab tracks your own vehicles and equipment. FEMA publishes a **Schedule of Equipment Rates** — a national price list of what it pays per hour for each kind of gear — and this tab is built around it. Rather than guess a rate, you look it up.

1. On the Equipment tab, click **+ Add Equipment Entry**.
2. Type the **Equipment Type** (required). To get the official rate, click **📋 Lookup** next to the FEMA Rate field.
3. In the **FEMA Equipment Rate Lookup** window, search for the equipment and click **Use** on the right row — the rate (and its code) drop into your entry automatically.
4. Enter the **Hours Used** and the **Agency Unit ID** (a unit number or asset tag). Add the operator's name if useful. The **Preview Total** shows hours × rate.
5. Click **SAVE**.

| Field | What to enter |
| --- | --- |
| **Equipment Type** *(required)* | What the equipment is, e.g. Pickup Truck (< 1 Ton) |
| **Agency Unit ID** | Your unit number, VIN, or asset tag |
| **FEMA Schedule Code** | The rate-schedule code (fills in from the lookup) |
| **Date Used** | The day the equipment ran |
| **Hours Used** | How many hours it operated on the incident |
| **FEMA Rate ($/hr)** | The hourly rate — set it from **📋 Lookup** |
| **Operator Name** | Who ran it, if tracked separately |
| **Notes** | Mileage, fuel, purpose |

The equipment total is simply **hours × rate**. Rows are edited or deleted with the **✏** button, the same as labor.


## Materials and Contracts

The **📦 Materials / Contracts** tab covers things you **bought** for the incident (sandbags, cones, fuel) and **work you hired out** (a contractor's services). Both live here because both are documented the same way — with a purchase order or invoice.

1. On the Materials / Contracts tab, click **+ Add Material / Contract**.
2. Type a **Description** (required) and choose a **Category** — Materials, Supplies, Contracts, Rental, or Other.
3. Enter the **Vendor / Contractor**, the **Quantity** and **Unit** (each, ton, yd³, hr…), and the **Unit Cost**. The **Total Cost** previews as quantity × unit cost.
4. Record the **PO / Contract #** and any notes (receipt number, justification), then click **SAVE**.

> **KEEP THE PAPER** — FEMA requires **source documentation** for every cost claim. Enter the purchase order or invoice number in the **PO / Contract #** field, and keep the actual receipts and invoices on file — the entry here is the index, not the proof.


## The Project Worksheet

The **📋 Project Worksheet** tab is where the incident's costs come together into a submission-ready summary. The **Eligible Cost Summary** near the bottom is filled in automatically from your three cost tabs — you don't retype any figures. You supply the descriptive details around it:

| Field | What to enter |
| --- | --- |
| **Applicant Name** | Who is claiming the costs — for example your organization |
| **Disaster / Declaration Number** | The FEMA declaration number (e.g. FEMA-DR-XXXX-your state) |
| **Incident Name** | Fills in from the selected incident; editable |
| **Work Category** | The FEMA category A through G (Debris Removal, Emergency Protective Measures, Roads and Bridges, and so on) |
| **Work Description / Scope** | What was done, what was affected, and why it was necessary |
| **Work Start / End Date** | The span of the work being claimed |

When it's ready, click **📄 Export PW** in the page header. FieldCommand generates a formatted plain-text summary — applicant and disaster details, the scope of work, the cost totals by category, and an itemized breakdown of every labor, equipment, and material entry — and downloads it as a `.txt` file. Paste it into the FEMA Grants Portal or attach it to your official Project Worksheet.

> **EQUIPMENT RATES GO STALE** — FEMA updates its equipment rates every year. If the loaded rates are more than a year old, an amber **rate reminder** appears near the top of the page with a link to the **FEMA Equipment Rates** page, where the rates are managed and updated (see Chapter 19). Update them before claiming so your equipment costs use current figures.


## Troubleshooting

- *The tabs are empty and nothing saves.* Choose an incident from the **Select incident...** dropdown first. Every entry is stored against a specific incident; with none selected there is nowhere to save.
- *My totals didn't change after I added an entry.* The totals bar recalculates on save. If a number looks wrong, re-open the entry with **✏** and check the hours, rate, and fringe — the preview inside the window shows the calculation before you save.
- *I imported from ICS-214 but the labor totals are near zero.* The import fills in names and units but leaves **hours and rates as placeholders**. Open each imported labor entry and enter the real hours and pay rates.
- *The FEMA rate lookup won't open or is empty.* The rates load from the FieldCommand server. Confirm you're on the FieldCommand Wi-Fi and the server is running; if an amber rate reminder shows, the rate table may need updating on the **FEMA Equipment Rates** page.
- *An amber "rates are outdated" banner is showing.* The loaded FEMA equipment rates are over a year old. Click **→ Review Rates** and update them so equipment costs use the current schedule.
- *The exported summary shows placeholder text like "[Enter applicant name]."* Those fields were left blank on the Project Worksheet tab. Fill in Applicant, Disaster #, Category, and Scope, then click **📄 Export PW** again.
- *Can I submit straight from FieldCommand?* No. This page produces a worksheet summary only. Official Public Assistance filings go through your state or territorial emergency management agency with supporting documentation — review everything with your Finance Section Chief first.


# 19. Federal Emergency Management Agency (FEMA) Equipment Rate Schedule

*The built-in price list of what FEMA will pay per hour or per day for equipment you own and used on an incident — so your cost paperwork uses the right, current numbers.*

> **QUICK VERSION** — Open **FEMA Equipment Rates**. You'll see a long price list of equipment with a dollar rate on each row. When you need a number, type in the **Search** box or pick a **category** to filter. To change a price, click the **✏** pencil on its row, type the new number, and **Save**. Once a year, after FEMA publishes a new schedule, update the changed prices and click **Update Rate Year** so the yellow "rates are old" warning goes away.


## What This Is / What It Is For

When your organization uses its own equipment on a federally declared disaster — a generator, a truck, a chainsaw, a light tower — the Federal Emergency Management Agency (FEMA) can reimburse you for that use. But it does not pay whatever you ask. FEMA publishes an official price list, the **Schedule of Equipment Rates**, that says exactly how much it will pay per hour (or per day) for each kind of equipment. That list is what this page holds.

The **FEMA Equipment Rates** page is the master copy of that price list living inside FieldCommand. Every time you log a piece of equipment on the cost-documentation pages (Chapter 20), the rate on this page is the number that gets used. Getting these rates right — and current — is what keeps your reimbursement paperwork accurate and defensible.

FieldCommand ships with all **44 standard FEMA equipment categories** already loaded from the 2025 schedule, so the list is useful the moment you open it. You don't build it from scratch; you keep it up to date.

> **EQUIPMENT ONLY — NOT LABOR** — These rates cover **equipment**, never people. The hours a person works are tracked separately as "Force Account Labor" on the cost-documentation page. The page banner says this plainly: *Labor NOT included*. Do not try to log a person's pay here.


## Opening the Page and What You See

1. From the dashboard, go to the **Finance** section and open **FEMA Equipment Rates** (you can also reach it from the FEMA cost pages).
2. The page opens with a blue **FEMA** badge and the title **FEMA Equipment Rate Schedule** at the top.
3. Below the title is an info bar showing the **Rate Year** and a link to the official schedule on fema.gov.
4. The main body is one big table, grouped into category headings, with one row per piece of equipment.

> _[Figure: The FEMA Equipment Rate Schedule page: the FEMA badge and title, the Rate Year info bar, the search box, and the grouped rate table below]_

The equipment is grouped under colored **category headings** — for example *Generators*, *Vehicles*, *Trucks* — so related items sit together. Inside each group, every row is one specific piece of equipment with its own price.


## Reading the Rate Table — Every Column

Each row in the table has these columns, left to right:

| Column | What it means |
| --- | --- |
| **Code** | The FEMA schedule code for this item (for example `8814`). This is FEMA's official reference number — matching it on your paperwork ties your entry to the exact line in FEMA's published schedule. |
| **Description** | The plain description of the equipment — what it is and, often, its size range (for example "Generator, 10-25 kW"). |
| **Unit** | How the rate is measured: **hour**, **day**, **mile**, or **each**. This tells you whether the dollar figure is per hour of use, per day, per mile driven, or per item. |
| **Rate** | The dollar amount FEMA will reimburse per unit, shown in green (for example `$14.50`). This is the number that matters. |
| **Year** | The rate year this specific price belongs to — the year of the FEMA schedule it came from. |
| **Notes** | Any extra note on the item — often blank. |
| **✏ (pencil)** | The edit button. Click it to change this row (covered below). |

> **WHY THE CODE MATTERS** — When you document equipment for reimbursement, FEMA reviewers expect the schedule code. Keeping the **Code** filled in here means it can flow onto your cost entries automatically, so you are not looking it up by hand under pressure.


## Finding One Rate Fast

The 44 categories add up to a long list. Two controls at the top narrow it down:

| Control | What it does |
| --- | --- |
| **Search equipment** box | Type any part of an equipment name, category, or code. The table filters as you type, showing only matching rows. Type `generator` to see just generators. |
| **All categories** dropdown | Pick a single category to show only that group. Set it back to *All categories* to see everything again. |
| **Rate count** | A small note next to the controls shows how many rates currently match — for example "18 rates" — so you know how much you're looking at. |

You can use the search box and the category dropdown together — pick a category, then type to narrow within it.


## The Rate Year Badge and the Stale-Rate Warning

FEMA republishes its equipment schedule every year, and the prices drift upward with inflation. FieldCommand helps you notice when your loaded rates have fallen behind.

At the top of the page, the **Rate Year** shows which year's schedule your rates came from (for example *2025*). If those rates are more than a year old, a yellow **reminder banner** appears across the top warning you the rates are outdated and pointing you to fema.gov for the current schedule. The same warning also shows up on the cost-documentation pages, so whoever is entering costs sees it too.

> **USE THE RATE IN EFFECT AT THE TIME OF THE DISASTER** — FEMA reimburses at the schedule rate that was in effect **when your disaster was declared** — not necessarily the newest one. If your incident happened last year, you may need last year's rate, not this year's. The info bar reminds you of this. When in doubt, check the linked fema.gov schedule and confirm with your Finance Section Chief.


## Editing a Rate

When FEMA publishes new numbers, or you spot one that is wrong, you edit the rate in place:

1. Find the equipment row (search or filter if needed).
2. Click the **✏** pencil button at the right end of the row.
3. The **Edit Rate** box opens, pre-filled with that item's current values.
4. Change what you need — most often just the **Rate ($/unit)** and the **Rate Year**.
5. Click **Save**. The table updates immediately, and the new rate is used everywhere from that moment on.

The edit box holds these fields: **Description**, **Category**, **FEMA Code**, **Unit** (hour, day, mile, or each), **Rate ($/unit)**, **Rate Year**, and an optional **Notes** line. Only the Description is required; the rest fill in the detail.


## Adding a Custom Rate

The 44 built-in categories cover FEMA's standard equipment, but you may own something unusual — a specialized trailer, a piece of gear with a locally negotiated rate. Use **+ Add Custom Rate** at the top of the page to add it.

1. Click **+ Add Custom Rate**.
2. The **Add Custom Rate** box opens, empty.
3. Type a **Description** (required), and fill in **Category**, **FEMA Code**, **Unit**, **Rate**, **Rate Year**, and **Notes** as they apply.
4. Click **Save**. Your custom item now appears in the table alongside the built-in ones and can be picked when documenting costs.

> **DELETING A RATE** — When you open an existing rate with the pencil, a **Delete** button appears in the edit box. Use it to remove a custom rate you no longer need. You'll be asked to confirm first. Removing standard FEMA items is usually a bad idea — edit the price instead of deleting the row.


## Updating the Whole Schedule to a New Year

Once a year, when FEMA releases a fresh Schedule of Equipment Rates, you bring FieldCommand current. There are two parts to this, and it helps to understand the difference.

1. Download the new schedule from the fema.gov link in the info bar.
2. Edit each rate whose **dollar amount changed**, using the pencil (above). This is the part that actually updates prices.
3. When the prices are current, click **📅 Update Rate Year** at the top.
4. Enter the new year and confirm. Every rate's year tag is stamped to that year, and the yellow stale-rate warning clears.

> **UPDATING THE YEAR DOES NOT CHANGE ANY PRICES** — The **Update Rate Year** button only changes the **year label** on the rates — it does **not** touch the dollar amounts. Its own box says so. If you click it without first editing the changed prices, you'll have current-year labels sitting on last-year's numbers. Always update the prices first, then stamp the year.


## How These Rates Feed the Rest of the System

This page is not a standalone reference — it is the source of truth the cost tools pull from. On the **FEMA PA Cost Documentation** page (Chapter 20), when you log a piece of equipment, there is a **📋 Lookup** button that opens a search of exactly these rates; pick one and its dollar rate and FEMA code drop straight into the entry. So the minutes you spend keeping this list current pay off every time someone documents a cost — they get the right number without hunting for it.

Everything here is stored in the server's local database. No internet is needed once the rates are loaded — the fema.gov links are only there for when you want to check or download the official schedule.


## Troubleshooting

- *The table says "Loading rates..." and never fills in.* The page couldn't reach the server. Confirm you're connected to the FieldCommand Wi-Fi and the server is running, then reload the page. If it shows a red "Error loading rates" message, the cost service may be down — check with whoever runs the server.
- *A yellow banner says my rates are old.* That's the stale-rate warning — your loaded rates are more than a year past. Check fema.gov for the current schedule, edit the changed prices, then click **Update Rate Year**. If you're documenting an older incident, remember you may actually want the older rates.
- *I clicked Update Rate Year but the prices didn't change.* That button only changes the year label, never the dollar amounts. Edit each changed rate with the **✏** pencil first, then stamp the new year.
- *Search shows "No rates match."* Your search text or category filter is too narrow. Clear the search box and set the dropdown back to *All categories* to see the full list again.
- *I can't find a piece of equipment I own.* It may not be one of the 44 standard FEMA items. Add it with **+ Add Custom Rate**, or confirm the correct FEMA category on the official schedule.
- *I edited a rate but the cost pages still show the old number.* The cost pages read rates when they load. Reload the cost-documentation page, or re-open the equipment lookup, and the updated rate will appear.


# 20. Cost Tracking Dashboard

*The one-glance money screen — what the incident has cost so far, where the money is going, how fast it's burning, and where it's headed — pulled together automatically from your cost entries.*

> **QUICK VERSION** — Open **Cost Dashboard** and pick your incident from the dropdown. The big tiles show the running total and the split between labor, equipment, and materials. Lower panels show where costs are headed and let you set a **Budget Limit** to track how much is left. The numbers here are read-only — you **enter** costs on the **✏ Edit Costs** page (the FEMA cost documentation page). The dashboard refreshes itself every two minutes.


## What This Is / What It Is For

During a long incident, the Finance Section and the Incident Commander need a fast, honest answer to one question: *what is this costing us, and can we afford to keep going?* The **Cost Dashboard** answers that on one screen. It gathers every cost that has been documented for the incident, adds it all up, breaks it down by type, works out how fast money is being spent, and projects where the total is headed.

The dashboard is a **read-only summary** — a window onto the numbers, not a place you type them in. The actual cost entries are made on the **FEMA PA Cost Documentation** page (Chapter 19 covers the rates those entries use). This dashboard reads all of those entries plus the daily rates on your T-cards, and paints the picture. It refreshes on its own every **two minutes**, so a screen left open in the command post stays roughly current without anyone touching it.

> **WHERE THE MONEY NUMBERS COME FROM** — Everything on this dashboard traces back to the **FEMA Force Account** cost entries — the labor, equipment, and materials logged on the cost-documentation page — and the estimated daily costs set on T-card resources. If a cost isn't entered there, it won't show here. An empty-looking dashboard usually just means no costs have been documented yet.


## Picking an Incident

The dashboard shows one incident at a time. Until you choose one, it simply says *Select an incident to view cost dashboard.*

1. Open **Cost Dashboard** from the dashboard's Finance area.
2. At the top right, open the **Select incident...** dropdown and choose your incident.
3. The dashboard fills in immediately. Your choice is remembered, so next time the page opens straight to it.
4. Use **↺ Refresh** any time to pull the latest numbers without waiting for the automatic two-minute refresh.

> _[Figure: The Cost Dashboard with an incident selected: the row of large stat tiles across the top and the breakdown panels below]_


## The Six Stat Tiles

Across the top sit six large tiles, each a headline number sized to be read from across the room. Left to right:

| Tile | What it shows |
| --- | --- |
| **Total Costs** | The running total of every documented cost on the incident. This is the single most-watched number. Below it: how many resources and personnel are on the T-card board. |
| **Force Acct Labor** | The total cost of people — your own personnel's hours, including overtime and fringe benefits. Shows how many labor entries make it up. |
| **Force Acct Equipment** | The total cost of your own equipment used, priced from the FEMA rate schedule. Shows the entry count. |
| **Materials / Contracts** | The total for things bought or contracted — supplies, rentals, contractor invoices. Shows the entry count. |
| **Elapsed Time** | How long the incident has been open, counted from its start time (for example "2.3d" or "18.5h"). This is what makes the burn rate possible. |
| **Burn Rate** | How fast money is being spent — the dollars-per-hour figure, with the per-day and per-12-hour-period equivalents beneath it. |

> **WHY BURN RATE MIGHT SHOW A DASH** — The **Burn Rate** and **Elapsed Time** tiles need two things to calculate: some documented costs, and a known incident start time. If either is missing, they show a dash (—) and a hint like *Enter costs above to calculate*. Once costs are entered and the incident has a start time, the numbers appear.


## Cost Breakdown

Below the tiles, the **Cost Breakdown** panel shows the same three cost types — **Force Account Labor** (red), **Force Account Equipment** (amber), and **Materials / Contracts** (green) — as horizontal bars. Each bar's length is that category's share of the total, and each line shows both the dollar amount and the percentage. At a glance you can see whether your spending is mostly people, mostly gear, or mostly purchases — which is exactly the split FEMA cares about.


## Resources on Incident

On the left of the middle row, the **Resources on Incident** panel lists the resources from your T-card board, grouped by type. For each type it shows the **Count** (how many of that resource), the **Personnel** on them, and an **Est Daily $** — the estimated daily cost.

That daily-cost column is only filled in if someone has set a daily rate on the T-card. The panel's own note says it plainly: *Set daily cost to include in burn rate estimate.* A row with no rate shows a dash and contributes nothing to the totals. When rates are set, a **Totals** line at the bottom sums the personnel and the daily cost across all resources.

> **T-CARD DAILY RATES FEED THE BURN RATE** — To have resource costs show up here and in the burn-rate estimate, set a **daily or hourly rate on each T-card**. Without those rates, the dashboard can only count the costs typed into the FEMA cost-documentation page. Setting T-card rates is the quickest way to get a realistic running cost during a live incident. Use the **Edit rates →** link in this panel to jump to where they're set.


## Cost Projection

On the right of the middle row, the **Cost Projection** panel answers "if we keep spending at this pace, what will the total be?" Using the current burn rate, it projects the total cost at four fixed horizons:

| Horizon | Meaning |
| --- | --- |
| **Next 12hr (1 period)** | Projected total one operational period out. |
| **Next 24hr (1 day)** | Projected total a full day out. |
| **Next 72hr (3 days)** | Projected total three days out — useful for a multi-day activation. |
| **Next 7 days** | Projected total a week out — the long-range budget picture. |

Each line shows the projected total and, in smaller text, how much of that is added spending beyond today. These are **estimates** — the panel says so — built on the assumption that today's burn rate simply continues. They are for budget planning, not for the official cost record.


## The Budget Tracker

Underneath the projection sits the **Budget Tracker**. If your activation was authorized with a spending limit, type it into the **Budget Limit** box and click **Set**. A bar appears showing how much of the budget is spent, the percentage used, and the dollars remaining.

The bar changes color as you approach the limit — **green** while there's comfortable room, **amber** as you cross about 70 percent, and **red** near or over the limit. If you go over, the line switches to *over budget* in red. It's a simple visual gut-check that the incident is staying within what was approved.

> **THE BUDGET FIGURE IS JUST FOR THIS VIEW** — The number you type into **Budget Limit** is only used to draw this bar. It doesn't change any cost entry or get reported anywhere — it's a local yardstick so you can see spent-versus-authorized at a glance.


## Cost by Operational Period

The bottom panel, **Cost by Op Period**, breaks the spending out period by period — **Labor**, **Equipment**, **Materials**, and a **Total** for each operational period. Costs only land in a period if the underlying FEMA cost entry was tagged with an operational period; anything untagged is grouped under *Unassigned*.

This per-period view is what you want for after-action documentation and for preparing the FEMA Project Worksheet (PW), because it shows how cost accumulated over the life of the incident rather than as one lump sum.


## The Companion Page — Where Costs Are Actually Entered

Because the dashboard is read-only, the real data entry happens next door on the **FEMA PA Cost Documentation** page, reachable from the **✏ Edit Costs** button at the top of the dashboard (or the *Edit rates →* and *Edit Costs* links inside the panels). That page has four tabs — **Force Account Labor**, **Force Account Equipment**, **Materials / Contracts**, and **Project Worksheet** — where each cost is logged with its detail. Everything you type there is what the dashboard sums up here.

A small footnote on the dashboard says the same thing: costs shown come from FEMA Force Account entries, and all projections are estimates to verify with the Finance Section Chief. Treat the dashboard as the summary and the cost-documentation page as the ledger.


## Troubleshooting

- *It just says "Select an incident to view cost dashboard."* You haven't chosen an incident yet. Pick one from the **Select incident...** dropdown at the top right.
- *All my totals are $0 even though we've been working for hours.* No costs have been documented yet. Costs come from the FEMA cost-documentation page — click **✏ Edit Costs** and add labor, equipment, or material entries. Hours worked don't cost anything here until they're entered as labor.
- *Burn Rate and projections show a dash.* They need both documented costs and an incident start time. Add some costs, and make sure the incident has a start time set, then refresh.
- *The Resources panel shows resources but no dollar amounts.* Those T-cards don't have daily rates set. Use **Edit rates →** to set a daily or hourly cost on each resource so it counts.
- *The per-period table says "No period data."* Your cost entries aren't tagged with an operational period. Tag each FEMA cost entry with its period on the cost-documentation page, and they'll sort into periods here.
- *"Error loading cost data."* The page couldn't reach the cost service. Confirm you're on the FieldCommand Wi-Fi and the server is running, then click **↺ Refresh**.
- *The numbers look stale.* The dashboard auto-refreshes every two minutes, but you can force it any time with **↺ Refresh** to pull the latest figures immediately.


# 21. Personnel Accountability

*The Safety Officer's one screen for answering, at any moment, the two questions that keep responders alive: who is on this incident, and is every one of them accounted for right now?*

> **QUICK VERSION** — Open **Personnel Accountability**, pick the incident and period. To take a head count, click **🔴 Conduct PAR**, then click **✓ PAR** on each person as their supervisor confirms them by radio. Watch the **⚠ UNACCOUNTED** tab — if anyone is still there after everyone has reported, escalate to the Incident Commander. Click **↺ Reset PAR** to start a fresh count.


## What This Is / What It Is For

**Personnel accountability** is a core life-safety rule of the National Incident Management System (NIMS) and the Incident Command System (ICS). At any moment during an incident, the Incident Commander (IC) and the Safety Officer must be able to answer two questions with certainty: **Who is on this incident?** and **Where is each person right now?** When conditions change fast — a building starts to collapse, the wind shifts a fire — not being able to locate someone in seconds is how responders get hurt or killed. This page exists so that answer is always one glance away.

FieldCommand tracks accountability at **two levels**, and this page brings both onto one screen for the Safety Officer. The first level is **incident-wide** (the ICS-211 check-in list — everyone who came onto the incident). The second is **per-resource** (the T-card personnel rosters — who is assigned to which crew or unit). Neither alone is enough; together they tell you both that a person is on the incident and exactly where they should be.

| Level | The tool | What it answers |
| --- | --- | --- |
| **Incident level** | ICS-211 Check-In List | Who has formally checked in? When did they arrive? Have they left? Everyone must have a check-in entry. |
| **Resource level** | T-Card Personnel roster | Who is assigned to each specific resource, and where should each crew member be right now? |

> **BOTH LISTS, ALWAYS** — The ICS-211 tells you everyone on the incident. The T-card roster tells you which resource each person is on and where they should be. The **Cross-Reference** view on this page catches gaps in both directions — people who checked in but were never assigned, and people on a T-card who never formally checked in. A person missing from either list is an accountability hole.


## Opening the Page and Reading the Tiles

1. From the dashboard, open **Personnel Accountability** (the red 🔴 Safety Officer tool).
2. Choose the incident from the **Select incident...** dropdown and the operational period from the **Period** dropdown next to it.
3. The **summary tiles** fill in, and the tabbed lists below become active.

The colored **summary tiles** across the top are the whole page in six numbers. They refresh whenever you load or act on the page (and every 60 seconds if you tick **Auto 60s**).

| Tile | What it counts |
| --- | --- |
| **Total Personnel** | Everyone associated with this incident and period |
| **Checked In** | People currently checked in and active on the incident |
| **Checked Out** | People who have left and been checked out |
| **PAR Confirmed** | People confirmed accounted for in the current PAR cycle |
| **Unaccounted** | Checked-in people **not** yet confirmed in this PAR — the number to drive to zero |
| **On T-Cards** | People listed on resource T-cards |

> _[Figure: The Personnel Accountability page: red header with the PAR badge, six summary tiles, the controls bar, and the four tabs]_


## The Four Tabs

Below the controls are four tabs, each a different view of the same people:

- **ICS-211 CHECK-IN LIST** — everyone who has checked into the incident. During a PAR, unconfirmed people sort to the top. Each row offers **✓ PAR**, **📍 Location**, and **Check Out** buttons.
- **T-CARD PERSONNEL** — the same accountability, but grouped by resource (Engine 12, Team Alpha…). Each resource group shows its own PAR tally, e.g. "3/4 PAR," so a supervisor can confirm a whole crew at once.
- **⚠ UNACCOUNTED** — only the people who are checked in but not yet PAR-confirmed. This is the tab you watch during an emergency roll call. When it's empty it shows "✓ All personnel accounted for."
- **CROSS-REFERENCE** — compares the two lists and flags anyone in one but not the other (covered below).


## Conducting a Personnel Accountability Report (PAR)

A **Personnel Accountability Report (PAR)** is a formal, time-stamped roll call that confirms every person on the incident is accounted for. Conduct one at regular intervals, at every shift or operational-period change, whenever a hazard escalates, and immediately any time someone can't be located.

1. Click **🔴 Conduct PAR** in the controls bar. The time is stamped in the **PAR badge** at the top right, and the page jumps to the **ICS-211 CHECK-IN LIST** with unconfirmed people sorted to the top.
2. Call each supervisor or crew boss by radio and have them confirm their people. As each person is confirmed, click **✓ PAR** on their row — the tile counts update in real time and the row turns green.
3. For a crew-by-crew count, switch to the **T-CARD PERSONNEL** tab and confirm by resource; each group shows its own running PAR tally.
4. Watch the **⚠ UNACCOUNTED** tab. If anyone remains after all supervisors have reported, transmit their name and last known assignment.
5. When the **Unaccounted** tile reaches 0, the PAR badge turns green and reads "✓ All accounted for."
6. To begin a new roll call later, click **↺ Reset PAR**. All confirmations clear and a fresh cycle begins.

> **IF SOMEONE CAN'T BE LOCATED** — If a person cannot be accounted for after you've exhausted radio contact, escalate **immediately** to the Incident Commander — do not wait for the rest of the count. On a search-and-rescue or high-risk operation, the Dead Man's Switch (Chapter 12) should already be running as an independent backstop that alerts if net check-ins stop.


## Last Known Location

Knowing someone is accounted for is good; knowing **where** they are is better. On any person's row, click **📍 Location** to open the **UPDATE LAST KNOWN LOCATION** window. Type a plain description — "Division Alpha, east perimeter" or "Base Camp medical tent" — and click **Save**. The location is stamped with a time and shown on the person's row (and feeds the resource map). During a PAR, having supervisors report each crew's location as they confirm it turns the roll call into a live picture of where everyone is.


## Checking People Out

Check-out matters as much as check-in. When a person leaves the incident for any reason, check them out so the accountability count reflects who is **actually** still there. People who leave without being checked out create false positives — they show as unaccounted in a PAR and can trigger a needless search.

1. Find the person in the **ICS-211 CHECK-IN LIST** and click **Check Out** on their row; confirm.
2. Their check-out time is stamped automatically and they drop out of the active accountability count. Their record isn't deleted — it stays for documentation, shown dimmed as **Checked Out**.
3. At the end of the operation, use **⏹ Check All Out** (top of the ICS-211 tab) to check out everyone still shown as checked in — a fast demobilization sweep. It asks you to confirm the count first.


## Cross-Reference — Closing the Gap

The **CROSS-REFERENCE** tab compares the ICS-211 check-in list against the T-card personnel rosters and flags two specific mismatches. Run it at the start of each operational period and whenever new people arrive.

| Flag | What it means | What to do |
| --- | --- | --- |
| **Checked in — not on any T-card** | The person checked in but isn't assigned to any resource. They may be floating staff, a late assignment, or the T-card wasn't updated. | Assign them to a resource and add them to its T-card, or confirm they're intentionally unassigned (e.g. Safety Officer) and note their location. |
| **On T-card — not checked in via ICS-211** | The person is on a resource T-card but has no check-in entry. This is a **safety gap** — they may be deployed to a hazardous area but aren't in the formal accountability system. | Direct them to complete ICS-211 check-in immediately. If they can't be located, escalate to the IC. |

> **A CLEAN CROSS-REFERENCE** — When neither flag appears, the tab reads "✓ All personnel cross-reference OK" — everyone on a T-card has checked in, and everyone checked in is on a T-card. That's the state you want at the start of every operational period.


## Accountability When Conditions Deteriorate Fast

When something changes suddenly — a structure turning unstable, a fire run, a hazardous-materials release — run an emergency PAR without waiting for the schedule.

1. Click **🔴 Conduct PAR** at once — the timestamp marks the start of the check.
2. Transmit on the command channel: "*All supervisors, this is Safety, emergency PAR — report personnel count by division/group immediately.*"
3. As each supervisor reports, click **✓ PAR** for their people on the **T-CARD PERSONNEL** tab.
4. Check the **⚠ UNACCOUNTED** tab after each supervisor. Transmit the name and last known assignment of anyone still unaccounted.
5. If a person can't be located within about five minutes, treat it as a missing-responder emergency — notify the IC, halt operations in the affected area, and start a search.


## Troubleshooting

- *The tiles and lists are blank.* Select an incident from the **Select incident...** dropdown (and a period). The page needs to know which incident to account for.
- *The Unaccounted tab says "Conduct a PAR first."* Unaccounted only means something during a PAR cycle. Click **🔴 Conduct PAR** to start one, then work the list.
- *Everyone shows as unaccounted right after I started the PAR.* That's expected — a fresh PAR marks everyone unconfirmed until you click **✓ PAR** on each person as they're confirmed.
- *Someone is listed but already went home.* They were never checked out. Click **Check Out** on their row so they leave the active count; their record is kept, just dimmed.
- *A crew member is on a T-card but flagged in Cross-Reference.* They haven't completed ICS-211 check-in. Direct them to check in; if they can't be reached, escalate to the IC — this is a real safety gap, not a data glitch.
- *I need to start a new head count.* Click **↺ Reset PAR** and confirm. All PAR confirmations clear and a new cycle begins from zero.
- *The page isn't picking up recent check-ins.* Click **↺ Refresh**, or tick **Auto 60s** to refresh automatically. If it still lags, confirm you're on the FieldCommand Wi-Fi and the server is running.


# 22. ICS-213 General Message

*The standard written-message form for passing traffic between people, sections, or agencies during an incident — fill it in on screen, sign it with your finger or mouse, print it, or hand it to your radio email program.*

> **QUICK VERSION** — Open **ICS-213**. Fill in **To**, **From**, **Subject**, **Date/Time**, and the **Message Text**. Click **⏰ Auto-fill Date/Time** to stamp the current time. If someone must reply, check **Reply Requested**. Optionally sign in the signature box. Click **📄 Generate Form** to see the print-ready copy, then **🖨 Print Form**, **💾 Save to Log**, **📄 Export (.txt)**, or **📡 Send via Winlink**.


## What This Is / What It Is For

The **ICS-213 General Message** is the Incident Command System (ICS) standard for a short written message — the paper (or now digital) equivalent of passing a note in an organized, trackable way. When the Operations Section Chief needs to tell Logistics something in writing, when one agency sends a request to another, or when a radio operator writes down traffic to be delivered, the ICS-213 is the form that carries it.

FieldCommand's ICS-213 is a fillable version of that form. You type the message on screen, optionally sign it by hand right in the browser, and then produce a clean, print-ready copy that looks like the official form. From there you can print it, save it to a log, download it as a text file, or hand it off to a radio email (Winlink) program to send over the air when the internet is down.

> **A MESSAGE, NOT A CONVERSATION** — The ICS-213 carries one message and, if needed, one reply. It's for discrete written traffic — a request, an update, an instruction — not for an ongoing back-and-forth. For logging many messages across a radio net, use the ICS-309 Communications Log (Chapter 23).


## Opening the Form and Its Layout

Open **ICS-213** from the dashboard or the top navigation bar. The screen shows a green live **UTC clock** in the corner and three stacked cards you fill top to bottom:

- **Incident & Routing** — who the message is to, who it's from, and the header details.
- **Message** — the message text itself and the Reply Requested checkbox.
- **Approved / Received** — who approved the message, the signature, and space for a reply.

> _[Figure: The ICS-213 entry screen showing the Incident & Routing, Message, and Approved/Received cards with the signature box]_


## Card 1 — Incident & Routing

This card holds the header and addressing. The fields:

| Field | What to type |
| --- | --- |
| **Incident Name** | The name of the incident this message belongs to (example: `Operation Winter Storm 2026`). |
| **To (Name / Title)** | Who the message is for — a person or a role (example: `Operations Section Chief`). |
| **To (Position / Agency)** | Their position or agency (example: `your county EMA`). |
| **Message Number** | A tracking number for the message (example: `ICS-213-001`). Auto-fill can generate this for you. |
| **From Callsign** | The sender's amateur radio callsign, if they have one. Type it and tab out — the **From (Name / Title)** field fills in automatically from the Federal Communications Commission (FCC) database. Leave blank if the sender is not a licensed ham. |
| **From (Name / Title)** | Who the message is from (example: `Communications Unit Leader`). Fills automatically if you entered a callsign. |
| **From (Position / Agency)** | The sender's position or agency (example: `your org's short form`). |
| **Date** | The message date (example: `Jun 7, 2026`). |
| **Time** | The message time (example: `0930 UTC`). |
| **Subject** | A short subject line (example: `Communications Status Update`). |

> **LET THE CALLSIGN FILL THE NAME** — If the sender is a licensed operator, just type their callsign in **From Callsign** and press Tab. FieldCommand looks the callsign up in its offline FCC database and drops the operator's name into the From field for you. It's faster and avoids typos. Not a ham? Leave the callsign blank and type the name by hand — the form works either way.


## Card 2 — Message

This is the heart of the form. Type your message in the **Message Text** box. The placeholder reminds you how: be clear and concise, and state *who needs to take action, what action is needed, and by when.* A good ICS-213 leaves no doubt about what's being asked.

Below the message is the **Reply Requested** checkbox. Check it if the recipient must send an answer back. When checked, it prints on the form so the reply block is clearly expected — the recipient can see at a glance that you're waiting on them.


## Card 3 — Approved / Received

The last card covers approval, signature, and the reply. In ICS practice, a message often needs sign-off from someone in charge before it goes out.

| Field | What it's for |
| --- | --- |
| **Approved By (Name)** | The name of the person approving the message (example: `Incident Commander`). |
| **Approved By (Title / Position)** | Their position or title. |
| **Approved By (Signature)** | The signature box — draw a signature here (see below). Optional. |
| **Reply (if applicable)** | Space for the recipient's reply, if one comes back. |
| **Replied By (Name / Signature)** | Who wrote the reply. |
| **Reply Date / Time** | When the reply was written. |


## Signing the Form on Screen

The **Approved By** signature box is a real signature pad. You can sign directly in the browser with a **mouse, a stylus, or your finger** on a touch screen — draw your signature in the white box just as you would on paper. If you make a mistake, click **Clear Signature** and try again.

The signature is optional. As the note under the box says, you can leave it blank and sign the printed copy by hand instead. If you do sign on screen, your signature appears on the generated form and prints with it.


## Auto-fill Helpers

Two buttons save typing:

- **⏰ Auto-fill Date/Time** — stamps the **Date** and **Time** fields with the current UTC time, and if the **Message Number** is empty, generates the next one in sequence (like `ICS-213-002`).
- **↺ New** — clears the whole form to start a fresh message.


## Generating the Print-Ready Form

When the form is filled in, click **📄 Generate Form**. The entry cards disappear and a clean, print-styled ICS-213 appears — the official numbered layout with your details in place, your signature if you drew one, and a *REPLY REQUESTED* note if you checked that box. A row of action buttons appears with it.

1. Click **📄 Generate Form** to build the print-ready copy.
2. Review it. To fix something, click **← Edit** to return to the form.
3. When it's right, use one of the action buttons below it.

> _[Figure: The generated print-ready ICS-213 form with the official numbered layout and the action buttons beneath it]_


## Print, Save, Export, and Send

The action buttons under the generated form:

| Button | What it does |
| --- | --- |
| **🖨 Print Form** | Opens your device's print dialog to print the form — or to save it as a PDF, since that's an option in most print dialogs. |
| **💾 Save to Log** | Saves the message to the on-screen log at the bottom of the page (and to the server), so you have a record of what was sent. |
| **📄 Export (.txt)** | Downloads the message as a plain text file, named after the message number. |
| **📡 Send via Winlink** | Prepares the message as a ready-to-send text file for a radio email program (see below). |
| **← Edit** | Goes back to the entry form to make changes. |


## Sending via Winlink

Winlink is the amateur radio email network — a way to send email-style messages over the air when the internet is down (covered in its own chapter). The **📡 Send via Winlink** button does not transmit anything itself. Instead, it prepares the message: it builds a text file with the recipient and subject already set up, downloads it, and tells you what to do next.

1. On the generated form, click **📡 Send via Winlink**.
2. A text file downloads and a message reminds you to open it in your Winlink client.
3. Open that file in your Winlink program (**Pat** on the Raspberry Pi/Linux, or **Winlink Express** on a Windows laptop).
4. Fill in the recipient's actual Winlink address in the To line, then send it over the air from your Winlink program.

> **NO LIVE RADIO LINK IS NEEDED HERE** — FieldCommand doesn't talk to the radio directly. It just hands your Winlink program a ready-made message. The actual over-the-air sending happens in that program — this keeps the message form simple and works no matter which Winlink client you use.


## The Saved-Message Log

At the bottom of the page, **Saved ICS-213 Messages** lists every message you've saved with **💾 Save to Log** — showing its number, subject, To, From, and date. This is your running record of ICS-213 traffic on this device. Each row has an **✕** to delete it, and **Clear All** empties the whole log. The list keeps your most recent messages so you can look back at what was sent.

One more thing this page can do: **import** a Winlink message. If an ICS-213 arrives over Winlink and is brought in through the Winlink import page, it opens this form already filled in and jumps straight to the print-ready view — so a received message is as easy to print and file as one you wrote.


## Troubleshooting

- *I typed a callsign but the name didn't fill in.* The name only auto-fills if the **From (Name / Title)** field is still empty and the callsign is found in the FCC database. If the name box already has text, it won't overwrite it. Some callsigns (clubs, very new licenses) may not be in the local database — just type the name by hand.
- *My signature won't draw.* Make sure you're drawing inside the white signature box. On a touch screen, use your finger or a stylus; with a mouse, click and drag. If it still won't take, click **Clear Signature** and try again — or skip it and sign the printed copy.
- *I clicked Generate Form and my entry fields vanished.* That's expected — the form switched to the print-ready view. Click **← Edit** to get the entry fields back.
- *Print looks wrong / includes the navigation menu.* Use the **🖨 Print Form** button on the generated form, not your browser's menu, so only the ICS-213 prints. The page is set up to hide everything but the form when printing.
- *Send via Winlink didn't send anything.* That button only prepares a file — it never transmits. Open the downloaded file in your Winlink program (Pat or Winlink Express), add the recipient's Winlink address, and send from there.
- *My saved messages disappeared.* The log is stored on the device you used. A different device, or a cleared browser, won't show them. Saving also sends a copy to the server, so the server-side record persists even if the local list is cleared.


# 23. ICS-214 Activity Log & ICS-309 Communications Log

*Two record-keeping forms in one chapter: the ICS-214 that logs what a unit did during a shift, and the ICS-309 that logs the message traffic on a radio net — both print-ready, both feeding the incident record.*

> **QUICK VERSION** — The **ICS-214** logs what a unit or section did during an operational period — add personnel, add timestamped activity entries, sign, and **📄 Generate Form** to print. It can also push its people into **FEMA Labor** costs. The **ICS-309** logs radio message traffic. The easy way to make one is automatic — the Net Logger's **Export ICS-309** button builds it from a net you ran. The **ICS-309 page** itself is for typing a log by hand when there's no net logger record.


## What These Are / What They Are For

This chapter covers two Incident Command System (ICS) record-keeping forms that often get confused because their numbers are close. They do different jobs:

| Form | Records | Kept by |
| --- | --- | --- |
| **ICS-214 Activity Log** | What a unit, resource, or section **did** during an operational period — the significant events and activities, timestamped. | Each unit leader, for their own unit. |
| **ICS-309 Communications Log** | The **message traffic** that passed on a radio net or at a station — who called whom, when, and about what. | The net control operator or radio operator. |

Both produce a clean, print-ready form for the Incident Action Plan (IAP) and the permanent incident record. The ICS-214 has a bonus: it can hand its personnel list straight to the Federal Emergency Management Agency (FEMA) labor cost tracker, bridging the gap between logging what people did and getting them reimbursed for it.


## ICS-214 — Filling In the Header

Open **ICS-214** from the dashboard or the top navigation. The screen has a live UTC clock and several cards. The first, **1. Incident & Unit Information**, sets the context:

| Field | What to type |
| --- | --- |
| **Incident Name** | The incident this log belongs to (example: `Operation Winter Storm 2026`). |
| **Operational Period Date From / To** | The start and end dates of the shift this log covers. |
| **Time From** | The start time of the operational period (example: `0600`). |
| **Unit Name / Designator** | The unit or resource this log is for (example: `your org's short form Communications Unit`). |
| **Unit Leader Name** | The name of the person leading the unit. |
| **Unit Leader Position** | Their ICS position (example: `Communications Unit Leader (COML)`). |


## ICS-214 — Personnel and Resources

The next card, **2. Personnel Assigned to This Period**, is a small table of who worked this shift. It starts with a few blank rows. For each person, fill in **Name**, **ICS Position**, and **Affiliation** (their agency or group). Click **+ Add Person** for more rows, and the **✕** on a row to remove it.

Below that, **2b. Resources Involved** is an optional table for the equipment, vehicles, and other gear used this period — radios, generators, go-boxes, vehicles. Each row has a **Resource** name and a **Type / Kind**. Click **+ Add Resource** to add one. If you leave this empty, it simply won't appear on the printed form.

> **PERSONNEL HERE ARE WHY THE FEMA EXPORT WORKS** — The people you list in the Personnel table are exactly who gets pushed to FEMA labor costs later. If you plan to claim labor reimbursement, take a moment to list everyone accurately — name and affiliation especially — because that's the data the cost tracker starts from.


## ICS-214 — The Activity Log

Card **3. Activity Log** is the point of the form: a running list of what happened, with times. Each entry is a **time** and a short **description** of the activity.

1. Click **+ Add Entry** to add a blank entry you can time-stamp yourself, or **⏰ Add Timestamped Entry** to add one already stamped with the current UTC time.
2. Type the activity in the description box — what happened, plainly (example: "Established contact with county EOC on 146.520").
3. Repeat through the shift. The **⏰ Add Entry Now** button at the top does the same timestamp-and-add so you can log events as they occur.
4. Remove any entry with its **✕** button.

> **LOG AS YOU GO** — The timestamp buttons are built for real-time logging. Each time something notable happens, click **⏰ Add Timestamped Entry** and type a few words. It's far easier than reconstructing the whole shift from memory at the end — and a contemporaneous log is exactly what after-action reviews and reimbursement audits want to see.


## ICS-214 — Signing and Generating

The **4. Prepared By** card records who completed the log: **Prepared By (Name)**, **Position / Title**, and **Date / Time Prepared**. Below those is a **signature box** you can sign in with a mouse, stylus, or finger — the same signature pad used elsewhere, with a **Clear Signature** button and the option to leave it blank and sign the printed copy by hand. The **⏰ Auto-fill Dates** button fills the date fields with the current date and time.

Click **📄 Generate Form** to build the print-ready ICS-214 — the official layout with your personnel table, resources, activity log, and signature in place. From there you can:

| Button | What it does |
| --- | --- |
| **🖨 Print Form** | Opens the print dialog to print the form or save it as a PDF. |
| **💾 Save** | Saves the log (to the server and to this device) so you can come back to it. |
| **💵 Export to FEMA Labor** | Pushes this period's personnel into the FEMA labor cost tracker (see below). |
| **← Edit** | Returns to the entry form to make changes. |


## ICS-214 — Export to FEMA Labor

This is the bridge from activity logging to reimbursement paperwork. Clicking **💵 Export to FEMA Labor** takes everyone in the Personnel table and creates a matching entry in the FEMA Force Account Labor tracker for the active incident — carrying over each person's name, position, and affiliation.

1. Make sure the Personnel table lists everyone who worked, with names filled in.
2. Generate the form, then click **💵 Export to FEMA Labor**.
3. FieldCommand creates a labor entry for each person and tells you how many it exported.
4. Open the **FEMA PA Cost Documentation** page to fill in each person's **hours** and **pay rates** — the export carries the names, but you enter the hours and money there.

> **THE EXPORT CARRIES PEOPLE, NOT HOURS** — The FEMA export creates one labor entry per person but leaves the **hours and rates blank** for you to fill in on the cost page. It's a head-start, not a finished cost record. Also, if no incident is currently selected, the entries are still created but without an incident link — so select your incident first for the cleanest result.


## ICS-309 — Two Ways to Make One

The **ICS-309 Communications Log** records the message traffic on a net or at a station. There are two ways to produce one, and picking the right one saves a lot of typing.

| Method | When to use it |
| --- | --- |
| **Automatic — from the Net Logger** | You ran a net and logged it. The Net Logger (net control / STARCOM logger) has an **Export ICS-309** button that builds the whole log for you — message traffic first, then the check-in list, with the net name, frequency/mode, and open/close times in the header. It both downloads a file and opens a print view. |
| **Manual — the ICS-309 page** | You need to log traffic that wasn't captured in a Net Logger. Open the **ICS-309** page and type each line by hand. |

> **PREFER THE AUTOMATIC EXPORT** — If the traffic happened on a net you were logging, don't retype it here — go back to that net in the Net Logger and click **Export ICS-309**. It's faster and more accurate. Use the manual page only for traffic that has no net-logger record behind it.


## ICS-309 — Filling In the Manual Page

Open **ICS-309** from the navigation. The **Log Header** card sets the context of the log:

| Field | What to type |
| --- | --- |
| **Incident / Event Name** | The incident or event (example: `Severe Storm 2026-06`). |
| **Operational Period — From / To** | The start and end of the period this log covers. |
| **Task No.** | An optional task number. |
| **Operator (Name / Callsign)** | Who kept the log (example: `J. Smith W9XYZ`). |
| **Station / Net** | The station or net name (example: `Net Control / EOC`). |
| **Page** | The page number (example: `1 of 1`). |

The **Log Entries** card is the message table. Each row is one message with a **Date / Time**, a **From** callsign, a **To** callsign, and the **Subject / Message**. Click **+ Add Entry** for a blank row, or **+ Add (timestamp now)** to add a row already stamped with the current time. Remove a row with its **✕**.

1. Fill in the log header.
2. Add a row per message with **+ Add Entry** (or **+ Add (timestamp now)** during live traffic) and type the from, to, and subject.
3. Click **📄 Generate Form** to see the print-ready ICS-309.
4. Use **🖨 Print** to print or save as PDF, or **💾 Save to Incident** to file it in the incident record.

The **Save to Incident** button also lets you tag the log to a specific incident using the dropdown next to it. If the server can't be reached, the log is saved locally on your device instead so nothing is lost, and you're told that's what happened.


## Troubleshooting

- *My ICS-214 came back empty after I reopened the page.* The page tries to restore your last session on this device, but a different device or a cleared browser won't have it. Use **💾 Save** to keep a server copy, and re-open from there.
- *Export to FEMA Labor says I need to add a person.* The Personnel table is empty or has no names filled in. Add at least one person with a name before exporting.
- *I exported to FEMA Labor but the costs show $0.* The export carries names only — hours and rates are blank until you enter them on the FEMA PA Cost Documentation page. Open it and fill in each person's hours and pay.
- *My exported labor entries aren't attached to my incident.* You exported with no incident selected. Select the incident first (its name is remembered across the cost pages), then export again.
- *I don't want to retype my whole net into the ICS-309.* Then don't — if you logged the net in the Net Logger, use its **Export ICS-309** button instead. The manual ICS-309 page is only for traffic with no net-logger record.
- *I clicked Save to Incident and it said "saved locally."* The server was unreachable, so the log was kept on this device as a fallback. Reconnect to the FieldCommand Wi-Fi and try again to file it to the server.
- *The printed form includes the menu bar.* Use the form's own **🖨 Print** button rather than the browser menu — the page hides everything but the form when you print that way.


# 24. Wide Area Network (WAN) Settings & Dual-Source Internet Configuration

*Set up your two internet sources — a preferred one and a fallback — so FieldCommand switches over automatically when the first one drops, and watch which one is live on the WAN Status page.*

> **QUICK VERSION** — Open **WAN Settings** from the dashboard. Fill in **Source A** (your main internet — typically a cellular modem (primary internet)) and, if you have one, **Source B** (your backup — typically a satellite link (fallback internet)). For each, tick **Enabled**, pick a **Role** (Preferred or Fallback) and a **Detection Method**, then click **Save Settings**. Changes go live within about 30 seconds. To see which source is carrying traffic right now, open **WAN Status**.


## What This Is / What It Is For

A **Wide Area Network (WAN)** is just a plain-language term for *your connection to the internet* — the path out of the FieldCommand Raspberry Pi to the wider world. FieldCommand is built to run completely offline, so it never *needs* a WAN. But a handful of features light up when internet is present: live weather radar, National Weather Service (NWS) alerts, solar-propagation data, and pulling hospital lists from public databases. This is where you tell FieldCommand what internet sources you have and how to use them.

The whole point of this page is **automatic failover**. You can define two internet sources — a **preferred** one that gets used first, and a **fallback** that takes over the moment the preferred source goes down. A common field setup is a cellular modem (primary internet) as the preferred source and a satellite link (fallback internet) as the fallback, but nothing is locked to a brand: either source can be cellular, satellite, a phone hotspot, or a fixed office connection. **The role is what matters, not the hardware.**

> **TWO PAGES, TWO JOBS** — **WAN Settings** (`wan_settings.html`) is where you *configure* your sources — an administrator task, done once. **WAN Status** (`wan-status.html`) is the *live monitor* everyone watches during an incident to see which source is up. This chapter covers both.


## Opening the WAN Settings Page

1. From the dashboard, open **WAN / Internet Settings** (marked with an **ADMIN** badge in the page header).
2. The page opens with a short blue explainer box at the top reminding you how preferred and fallback work.
3. Below it are two source cards — **Source A** and **Source B** — a **Dashboard Display** box, and a **USB Backup Drive** box.
4. Fill them in top to bottom, then click **Save Settings** at the bottom.

> _[Figure: The WAN Settings page: Source A card (green left edge, Preferred), the Swap Roles button, and Source B card (amber left edge, Fallback)]_


## Setting Up a Source (A and B)

Each source is a card. **Source A** starts as your **Preferred** source (green left edge); **Source B** starts as the **Fallback** (amber left edge). A disabled card fades to gray. The colored badge in the top corner always tells you what that card is doing right now — **Preferred**, **Fallback**, or **Disabled** — and it updates live as you change the fields. Fill in both cards the same way:

| Field | What to type | Plain meaning |
| --- | --- | --- |
| **Enabled** *(checkbox)* | Tick it to turn this source on | An unticked source is ignored completely — a handy way to park a backup you're not using today without erasing its setup. |
| **Display Name** | A short name — `Cellular`, `Satellite`, `Office Wi-Fi` | What shows on the dashboard status bar. If you leave it blank it just reads `Source A` / `Source B`. |
| **Role** | **Preferred** or **Fallback** | **Preferred** is tried first. **Fallback** is used only when the preferred source is down. Two sources should not both be Preferred — use the Swap button instead. |
| **Type** | Cellular · Phone/mobile hotspot · Satellite · Fixed ISP · Other | Picks the little icon (📡 cellular, 📱 hotspot, 🛰 satellite, 🌐 fixed). Cosmetic — it does not change how detection works. |
| **Provider / Carrier** *(optional)* | Free text — `T-Mobile`, `Starlink`, `Comcast` | Just a label for your own reference. Leave blank if you like. |
| **Detection Method** | One of three choices (see next section) | *How* the Pi decides whether this source is up. This one matters — pick the one that fits your hardware. |


## Detection Method — How the Pi Knows a Source Is Up

The **Detection Method** dropdown is the one field worth getting right. It tells FieldCommand how to test whether a source is actually carrying traffic. Picking the method also reveals a helper box under the dropdown with example addresses, and — for two of the choices — an extra field to fill in.

| Method | What it does | Best for |
| --- | --- | --- |
| **Internet reachable — no device check** | Simplest option. Just checks that *some* internet is reachable, with no attempt to talk to a specific modem or router. | A phone hotspot, a Universal Serial Bus (USB) cellular dongle with no admin page, or any setup where you only have one source and just want up/down. |
| **Ping a gateway IP** | Pings one IP address that only answers when this exact path is live (usually the modem or hotspot gateway). Reveals a **Gateway IP to Ping** field. | Sources with a known gateway. The helper lists common ones — Android hotspot `192.168.43.1`, iPhone `172.20.10.1`, Starlink `192.168.100.1`, HughesNet `192.168.0.1`. |
| **Modem admin page responds** | Checks that the modem or router's own web page answers. Reveals an **Admin URL** field. Bonus: carrier name and signal strength may be picked up automatically. | Cellular modems and routers with a local admin page — for example `http://10.1.1.1` for a generic modem, or `http://192.168.0.1` for a Cradlepoint or Pepwave. |

> **WHEN IN DOUBT, USE THE SIMPLE ONE** — If you are not sure, choose **Internet reachable — no device check**. It works with almost anything and needs no IP address. You can always switch to a smarter method later once you know your modem's gateway address.


## Swapping Preferred and Fallback

Between the two cards is a dashed button: **⇅ Swap preferred ↔ fallback roles between the two sources**. Click it and the two roles trade places instantly — whatever was Preferred becomes Fallback and vice-versa. Use this when you want to *manually* favor one source without touching any cables. For example, if a satellite link (fallback internet) is giving you a cleaner signal than a cellular modem (primary internet) on a given day, swap the roles so satellite is tried first. The change takes effect on the next Save.


## Dashboard Display and the USB Backup Drive

Below the source cards, the **Dashboard Display** box has three checkboxes that control which status cards appear on the main dashboard. Turn off the ones you don't care to see.

| Checkbox | What it shows on the dashboard |
| --- | --- |
| **Show Source A card on dashboard** | The live status of your first (usually preferred) internet source |
| **Show Source B card on dashboard** | The live status of your second (usually fallback) source — off by default |
| **Show AMPRNet / 44Net status card** | The status of the amateur-radio 44Net gateway, if your group uses one |

The **USB Backup Drive** box handles automatic backups. Any USB drive **formatted and labeled `FIELDCOMMAND`** (all caps) triggers a backup the moment you plug it in — any brand, any size, formatted ext4 or exFAT. Two fields let you rename things: **Drive Label** is the exact label the Pi watches for (leave it `FIELDCOMMAND` unless you have a reason), and **Display Name** is just a friendly name like `WD Passport` shown in the app.

> **CHANGING THE DRIVE LABEL TAKES AN EXTRA STEP** — If you change the **Drive Label** away from `FIELDCOMMAND`, you must also edit the matching rule on the Pi itself (`/etc/udev/rules.d/99-fieldcommand-backup.rules`) and reload it, or plugging in the drive won't trigger a backup. For almost everyone, leaving the label as `FIELDCOMMAND` is the right move.


## Saving Your Settings

1. Scroll to the bottom and click **Save Settings**.
2. A confirmation appears: **✓ Saved — changes active within 30s**.
3. The **↺ Reload** button next to it reloads the saved settings from the server, throwing away any unsaved edits — handy if you want to start over.

The WAN monitor runs quietly in the background and re-reads its configuration on its next poll cycle, so allow up to about **30 seconds** (and no more than a minute) for a change to take hold. You do not need to restart anything.


## Watching the WAN Status Page

The companion page, **WAN Status** (`wan-status.html`), is the live monitor. It refreshes itself every 30 seconds and is the page to keep open during an activation. It has several parts, top to bottom:

| Part of the page | What it tells you |
| --- | --- |
| **Active WAN hero banner** | The big banner at the top. Green with a 📶 icon means cellular is carrying traffic; blue with 🛰 means it has failed over to satellite; red with ⚠ means **NO WAN — Operating Offline** (local features still work). |
| **Source cards** (two) | One card per source, showing whether it is **Active**, on **Standby**, or **Down**, plus live stats — carrier, signal, and technology for cellular; latency, throughput, obstruction, and uptime for satellite. |
| **Connectivity Test** | A table that checks reachability of key outside services (NWS weather, Cloudflare DNS, the 44Net gateway) over whatever WAN is active, re-running about every 60 seconds. Each row shows **Reachable** or **Unreachable** and the response time. |
| **WAN Event Log** | A running list of failover and failback events with timestamps in Coordinated Universal Time (UTC) — for example, *Failover to satellite* — so you can see when the connection switched. |
| **Antenna Quick-Reference & Plan Management** | Reference tables for swapping antennas and managing the cellular data plan. These are informational cards for the field team. |

> **LOSING INTERNET IS NOT LOSING FIELDCOMMAND** — When the hero banner turns red and reads **NO WAN — Operating Offline**, that only means the internet-dependent extras (radar, live weather, propagation data) are paused. Every core FieldCommand feature — forms, the map, T-cards, the log — keeps running perfectly on the local Wi-Fi. Internet is a bonus, never a requirement.


## Troubleshooting

- *I saved my WAN settings but nothing changed on the dashboard.* Give it up to a minute — the background monitor only picks up changes on its next poll cycle. If it still hasn't updated, reopen WAN Settings and confirm the source is **Enabled** and you clicked **Save Settings** (watch for the green *✓ Saved* message).
- *The WAN Status page says NO WAN even though I have internet.* Check the **Detection Method**. If you chose *Ping a gateway IP* or *Modem admin page responds*, the address you entered may be wrong or unreachable — switch that source to **Internet reachable — no device check** and Save, then see if it comes up.
- *It never fails over to my backup source.* Make sure **Source B** is ticked **Enabled** and its **Role** is **Fallback**. A fallback that is disabled will never be used. Confirm on the WAN Status page that Source B shows at least **Standby** (not **Down**).
- *Both sources show as Preferred.* Only one should be preferred at a time. Use the **⇅ Swap** button to trade roles, or set one card's **Role** dropdown to **Fallback**, then Save.
- *I plugged in my backup USB drive and no backup happened.* The drive must be labeled exactly `FIELDCOMMAND` in all caps and formatted ext4 or exFAT. If you renamed the trigger label in WAN Settings, the matching rule on the Pi must be updated too — otherwise set the label back to `FIELDCOMMAND`.
- *Cannot reach server / the page won't load.* Confirm your device is on the FieldCommand Wi-Fi and that the Pi is powered up. The WAN Settings and Status pages talk to the server directly, so they need the same local connection as every other page.


# 25. National Weather Service (NWS) Animated Radar

*A live, animated weather-radar map you can play back frame by frame — it lights up whenever FieldCommand has an internet connection, and gracefully holds the last picture when it doesn't.*

> **QUICK VERSION** — Open **Radar** from the dashboard. If FieldCommand has internet, an animated weather-radar loop plays automatically over a dark map. Use the **⏸/▶** button to pause or play, drag the **timeline slider** to scrub through the loop, and set **Speed** to Slow/Med/Fast. Green is light rain, yellow is moderate, red is heavy, purple is extreme. No internet? The page shows the last radar it saw and keeps trying to reconnect.


## What This Is / What It Is For

The **NEXRAD Radar** page shows live, moving weather radar for the United States. **NEXRAD** stands for **Next Generation Radar** — the nationwide network of Doppler weather radars run by the **National Weather Service (NWS)**. The page stitches the most recent radar images into a short animation so you can watch a storm's motion, judge which way it's tracking, and get a feel for how fast and how hard it's coming — all useful for keeping field teams safe and planning around the weather.

The imagery is pulled from an online radar service (RadrView), with an automatic backup source (the Iowa Environmental Mesonet, or **IEM**) if the first one is unavailable. Because the pictures come from the internet, **this page only works while FieldCommand has a WAN (internet) connection** — see Chapter 24. The header says so plainly, right next to the title: *· Requires internet connection*.

> **IT LIGHTS UP WHEN YOU HAVE INTERNET** — Radar is one of FieldCommand's internet-dependent extras. When a WAN source is present, the loop plays. When every internet source is down, the page can't fetch fresh radar — but it doesn't just go blank; it holds onto the last picture it managed to load and quietly reconnects. See **What Happens When There's No Internet**, below.


## Opening the Radar and What You See

1. From the dashboard, open **Radar** (the ⛈ storm-cloud link). It's reachable from all dashboard modes.
2. The page fills the screen with a dark map. A thin header sits on top; a status bar and legend float over the map; and a control bar runs along the bottom.
3. If internet is available, you'll briefly see *Fetching radar frames…* and then the loop begins playing on its own.

> _[Figure: The NEXRAD Radar page: a dark national map with colored radar returns, the reflectivity legend at top-right, and the playback control bar along the bottom]_

The floating pieces around the map are:

| On-screen element | Where it is | What it's for |
| --- | --- | --- |
| **Status line** | Top-left | Shows what's loading — e.g. *NEXRAD CONUS composite* — and how many frames are in the loop. |
| **Palette swatches** | Top-right of the info bar | Three little color circles for picking the radar color scheme (see below). |
| **Reflectivity legend** | Top-right corner | The color scale explaining what each radar color means in dBZ (see below). |
| **Control bar** | Along the bottom | All the playback controls — play/pause, step, the timeline slider, the time readout, and speed. |


## Reflectivity, Velocity, and the Color Legend

Two buttons in the header switch what the radar is showing:

- **Reflectivity** (the default) — how heavy the precipitation is. This is the everyday view most people mean by "weather radar."
- **Velocity** — how fast precipitation is moving toward or away from the radar. This is a more specialized view used to spot rotation. When Velocity is selected, the reflectivity color legend hides itself, because it no longer applies.

For **Reflectivity**, the legend at top-right reads left (light) to right (extreme), labeled with dBZ values from **5** to **65+**. In plain terms:

| Color | Roughly means |
| --- | --- |
| **Green** | Light precipitation — drizzle to light rain |
| **Yellow** | Moderate rain |
| **Red** | Heavy rain — a strong storm cell |
| **Purple / white** | Extreme — very intense core, possible hail |


## The Playback Controls

The control bar along the bottom is where you drive the animation. From left to right:

| Control | What it does |
| --- | --- |
| **⏸ Pause / ▶ Play** | Stops or starts the animation loop. It starts out playing. |
| **⏮ / ⏭ Step** | Move one frame back or forward. Stepping pauses the loop so you can study a single moment — good for watching a storm cell inch across the map. |
| **Timeline slider** | Drag it to jump to any point in the loaded loop. Dragging also pauses playback. |
| **Time readout** | Shows the date and time of the frame you're looking at. The newest frame is highlighted in amber so you always know when you're viewing the latest picture. |
| **Speed: Slow · Med · Fast** | Sets how quickly the loop animates. **Med** is the default; **Slow** is easier to follow a fast-moving line, **Fast** compresses a couple of hours into a quick sweep. |


## Palette and Station Selector

Two extra controls tailor the view:

**Palette** — the three colored circles in the top info bar switch the radar color scheme between **Default**, **Dark**, and **NOAA** (the classic National Oceanic and Atmospheric Administration look). It's purely a preference — pick whichever is easiest for your eyes and screen. The active palette has a white ring around it.

**Station selector** — the dropdown in the header (it starts on **Composite (National)**) lets you jump the map to a specific NEXRAD radar site, such as *KLOT — Chicago, IL* or *KFWS — Dallas/Ft Worth, TX*. This is a *"focus here"* jump — it recenters and zooms the map on that radar's coverage area. The imagery you see stays the national composite; the station picker doesn't change the data, just where you're looking. Choosing **Composite (National)** again zooms back out.

> **IT REFRESHES ITSELF** — As long as internet is available, the page automatically fetches new radar every **5 minutes** and adds it to the loop, so what you're watching stays current without you touching anything.


## How Much History the Loop Covers

The animation isn't a single snapshot — it's a short stack of recent radar images played in sequence, which is what lets you see motion. The status line reports how many are loaded (for example *18 frames*). The frames run oldest to newest, and the newest one is the amber-highlighted frame you land on when the page first loads. So a typical loop shows you roughly the **last couple of hours** of weather, which is usually plenty to judge whether a line of storms is building, weakening, or sliding past your area.

If the primary imagery service is unavailable, FieldCommand automatically falls back to a backup source (the Iowa Environmental Mesonet) and rebuilds the loop from the last couple of hours at roughly 10-minute steps — you'll see the status line note the fallback, but the controls all work the same way. A small pulsing dot near the status line means the page is busy fetching; when it stops, the loop is ready.


## What Happens When There's No Internet

Radar needs the internet, but the page is built to fail gracefully rather than go dark:

- **If it has already loaded radar and then loses internet:** it keeps the last radar picture on screen and changes the status line to something like *Showing last radar (from 3:42 PM) — reconnecting every 30 s…*. You still have a recent picture to work from.
- **If it never managed to load any radar (offline from the start):** a full-screen **RADAR UNAVAILABLE OFFLINE** banner appears with a 📡 icon and a short explanation, plus a **→ Check WAN Status** button that jumps you to the WAN Status page (Chapter 24) so you can see why there's no internet.
- **Either way, it keeps trying.** The page re-checks for internet every **30 seconds** and, the moment a WAN source comes back, it automatically reloads fresh radar and resumes the animation — no need to reload the page yourself.

> _[Figure: The full-screen offline banner reading RADAR UNAVAILABLE OFFLINE with the Check WAN Status button]_


## Troubleshooting

- *The whole screen says RADAR UNAVAILABLE OFFLINE.* FieldCommand has no internet. Radar can't load without a WAN connection. Click **→ Check WAN Status** (or open the WAN Status page from the dashboard) and get an internet source back up per Chapter 24. The radar returns on its own within about 30 seconds of internet coming back.
- *The status line says 'Showing last radar (from …)'.* That's the offline-but-was-online state — internet dropped after some radar had loaded, so you're seeing the last good picture. It's still useful; just remember the time shown isn't current. It updates automatically when internet returns.
- *The radar isn't animating.* The loop may be paused. Click the **▶ Play** button at the bottom-left of the control bar. If you'd used **Step** or dragged the slider, that pauses playback on purpose.
- *I picked a station but the radar picture didn't change.* That's expected — the station selector only recenters the map on that radar's area; the imagery stays the national composite. Use it to zoom in on your region, not to change the data.
- *The colors look wrong or hard to read.* Try a different **Palette** (Default / Dark / NOAA) using the colored circles in the top info bar. And remember the color legend only applies to **Reflectivity** — in **Velocity** view the legend is hidden because it means something different.
- *Radar loads slowly or stalls.* On a weak or busy internet source, frames can take a while to arrive. Give it a moment; the page also has a built-in backup imagery source it falls back to automatically if the primary one fails.


# 26. High Frequency (HF) Propagation Tool

*A one-screen read on how well the long-distance radio bands are working right now — pulled from live solar data when you have internet, so you can pick a band that will actually get your traffic through.*

> **QUICK VERSION** — Open **HF Propagation** from the dashboard. The colored strip at the top shows current space-weather numbers; the **Band Conditions** cards below show which bands are **Good** (green), **Fair** (amber), **Poor**, or **Closed** right now, split into Day and Night. For emergency traffic, **40m is the reliable workhorse day and night** — start there. The **K-Index** is the fastest health check: 0–2 is great, 5+ means degraded HF. Needs internet for live data; falls back to an estimate offline.


## What This Is / What It Is For

**High Frequency (HF)** is the range of radio bands (roughly 1.8 to 30 MHz) that can carry a signal hundreds or thousands of miles by bouncing off the upper atmosphere. **Propagation** is just the word for *how well that bouncing is working right now* — and it changes constantly with the sun, the time of day, and the season. This page gives you a quick, current read so you don't waste time calling on a band that's dead when a different band is wide open.

For a group passing emergency traffic over radio, that's genuinely useful: pick the wrong band and your message goes nowhere; pick the right one and you reach the next county — or the next state — cleanly. The tool pulls live solar and geomagnetic data from **HamQSL** (a well-known amateur-radio space-weather feed) about every 15 minutes when internet is available, and turns it into plain green/amber/red band ratings.

> **AN ESTIMATE, NOT A GUARANTEE** — Propagation is a model, not a promise. These bars are a well-informed starting point; real-world conditions still vary. When the page can't reach the internet, it shows a **model-based estimate** from time-of-day and typical patterns instead of live numbers — clearly marked *Offline — internet unavailable*. Either way, confirm with an actual on-air check before you count on a band.


## Opening the Page

1. From the dashboard, open **HF Propagation** (the ☀ sun link).
2. A thin **refresh bar** sits under the header. It reminds you that solar data updates every 15 minutes, and carries a **⟳ Refresh** button if you want fresh numbers right now.
3. The header's right corner shows when the data was last updated — or *Fetching data…* while it loads.

> _[Figure: The HF Propagation page: the Solar Indices strip of cards across the top, the K-Index scale bar, and the colored Band Conditions cards below]_


## The Solar Indices Strip

Across the top is a row of small cards, each a single space-weather number. They're color-coded — green is favorable, amber is so-so, red is unfavorable — so you can glance at the row and get the gist without knowing the science. Here's what each one means in plain terms:

| Card | Full name | Plain meaning |
| --- | --- | --- |
| **SFI** | Solar Flux Index | The sun's overall radio energy. **Higher is better** for the high bands — above ~130 the upper bands (20m and up) tend to open up; below ~70 you're mostly limited to the lower bands. |
| **SN** | Sunspot Number | How many sunspots are showing. Loosely tracks SFI — more sunspots generally means livelier high-band conditions. |
| **A-Index** | Geomagnetic A-index | A daily measure of how disturbed Earth's magnetic field is. **Lower is better**; under 10 is quiet, over 30 means a stirred-up, degraded ionosphere. |
| **K-Index** | 3-hour Planetary K-index | The short-term version of the A-index, updated every few hours. The single most useful number here — see the K-Index scale below. |
| **X-Ray** | X-Ray Flux Class | Current solar-flare X-ray level. A letter class — an **X** or **M** flare (shown red/amber) can cause a sudden HF blackout on the sunlit side of Earth. |
| **Proton** | Proton Event | Whether a solar proton event is underway. **None** is what you want; an event (shown red) degrades polar radio paths. |
| **Signal** | Signal Noise Level | The current background radio-noise level — how much natural static you're fighting. |


## The K-Index Scale

Just under the strip is a **K-Index Scale** bar — ten cells labeled **K0** through **K9** — with the current level lit up. It's the quickest single health check for HF, because a geomagnetic storm can wreck otherwise-good conditions. Read it like this:

| K level | Condition | What it means for HF |
| --- | --- | --- |
| **K0–K2** | Quiet | Good HF — the ionosphere is calm and stable. |
| **K3–K4** | Unsettled | Fair — some fading and weaker paths, but workable. |
| **K5–K7** | Storm | Degraded HF — polar and long paths suffer; expect trouble. |
| **K8–K9** | Severe storm | Possible HF blackout — high bands may be unusable. |


## Band Conditions Cards

The heart of the page is the **Band Conditions (Day/Night Model)** grid. Each card covers a band group (for example **80m–40m**, **30m–20m**, **17m–15m**, **10m**) and shows two colored bars — one for **Day** and one for **Night** — with a one-word rating. The fuller and greener the bar, the better:

| Rating | Bar color | Meaning |
| --- | --- | --- |
| **Good** | Green, nearly full | Band is open and reliable |
| **Fair** | Amber, about half | Usable, but weaker or spotty |
| **Poor** | Orange-red, short | Marginal — likely to struggle |
| **Closed** | Gray, tiny | Effectively dead for now |

Because the same band behaves very differently by day and by night, the Day/Night split is the important part. A band that's **Good** at night may be **Poor** at midday, and vice-versa — glance at the bar for the time you're actually operating.


## MUF/LUF, the Ionosphere Diagram, and the 24-Hour Guide

Below the band cards are three more visual aids that add depth:

- **MUF / LUF Estimates** — a small table by path distance (Local, Regional, DX, Long Path). **MUF** is the **Maximum Usable Frequency** and **LUF** the **Lowest Usable Frequency** — together they bracket the window of frequencies likely to work for that distance, and the table names a suggested **Best Band** and a rough **Reliability** percentage for each.
- **Ionosphere Layers** — a labeled diagram of the atmospheric layers (D, E, F1, F2) that bend HF signals back to Earth, with a sketched skip path. It's a teaching picture that shows *why* the bands behave as they do; the layer heights shift with the sun and the time of day.
- **24-Hour Band Activity Guide** — a chart with a row per band (80m, 40m, 20m, 15m, 10m) and the hours of the day across the bottom in Coordinated Universal Time (UTC). Shaded blocks mark when each band is typically usable, and a bright **NOW** line marks the current hour so you can see, at a glance, which bands are in their good window right now.


## The EmComm Quick Reference

At the bottom, the **EmComm Propagation Quick Reference** panel is a printable-style cheat sheet built for emergency communications. The left table lists each band's typical **Day Use** and **Night Use** in words (*Best day band*, *Excellent DX*, *Closed*, and so on). The right table translates the solar numbers into effects (*SFI > 150 → high bands open*, *K ≥ 7 → HF blackout possible*). The takeaways the panel spells out are worth remembering:

- **40m is the backbone** — reliable day and night for regional-to-national paths. When in doubt, start on 40m.
- **80m** is the night band for local and regional work.
- **60m** (its five channels) is useful for interoperating with served agencies.
- **14.300 MHz** on 20m is the standard maritime-mobile / distress watch frequency worth monitoring.


## Troubleshooting

- *The numbers all show 'N/A' and it says 'Offline — internet unavailable'.* The page couldn't reach the live solar feed, so it's showing a model-based estimate instead of current data. Get an internet source up (Chapter 24) and click **⟳ Refresh**; the live numbers should fill in.
- *The data looks stale.* Live data updates about every 15 minutes on its own. To force an immediate update, click the **⟳ Refresh** button in the refresh bar under the header. The header's top-right corner shows the last-updated time so you can tell how fresh it is.
- *Every band shows Poor even though the sun looks active.* Check the **K-Index**. A geomagnetic storm (K5 or higher) drags conditions down across the board regardless of solar flux — that's the model doing its job, not a glitch. Wait for the storm to settle.
- *A band the tool calls 'Good' isn't working for me on the air.* These ratings are a model, not a live measurement, and local factors (your antenna, noise, terrain, the far station) all matter. Treat the page as a starting point and confirm with an actual on-air check or a propagation beacon.
- *The band cards or charts look empty or misaligned.* Try the **⟳ Refresh** button, or reload the page. The charts redraw when the window is resized, so resizing the browser can also nudge them back into shape.
- *This tool doesn't show VHF/UHF bands (2m, 70cm).* That's by design — it covers HF only. The Very High Frequency (VHF) and Ultra High Frequency (UHF) bands propagate by different rules and aren't part of this page.


# 27. Winlink Radio Email

*How FieldCommand takes ICS forms that traveled over Winlink radio email and files them into your incident record — using the Winlink Form Import page.*

> **QUICK VERSION** — In your Winlink program, open the message that carries the ICS form and **save its `RMS_Express_Form_*.xml` attachment** (or just copy the message text). In FieldCommand, open **Winlink Form Import**, **drop the file** onto the page (or paste it) and click **Parse Form Data**. Check the fields it pulled out, pick the **Incident** and whether the message was **Received** or **Sent**, then click **Archive to incident** to file it — or **Open in ICS form** to print a clean copy.


## What This Is / What It Is For

**Winlink** is radio email. It lets amateur-radio operators send and receive email-style messages — with attachments — over the air when the regular internet is down. During an incident, your organization uses it to move ICS paperwork between stations that have no other connection. FieldCommand does **not** transmit Winlink itself; the radio work is done by a separate Winlink program running on an operator's computer next to the radio. What FieldCommand adds is the **bridge on the receiving end**: it takes an ICS form that arrived (or was sent) over Winlink and drops it neatly into your incident record, so that message lives alongside the rest of your forms, logs, and reports instead of being stranded in an email inbox.

The whole job happens on one screen — the **Winlink Form Import** page. You give it the form, it reads the fields, you check them, and you file the result. Think of it as the inbox-to-file-cabinet step for radio email.

> **THIS IS A LICENSED-OPERATOR FEATURE** — Winlink runs on amateur-radio frequencies, so it legally requires a properly licensed amateur-radio operator with a callsign (for example **your club callsign**). Like the other ham features, Winlink is only switched on when a **Club / Station Callsign** has been set in Setup (Chapter 3). If your group has no licensed operator, this page stays grayed out — by design.


## The Radio Side — Where the Message Comes From

Before FieldCommand ever sees anything, the message travels over the radio using one of the common Winlink programs. FieldCommand works with whatever your operators already use; the table below is just so you know the names you'll hear on the air.

| Program | Runs on | How it connects |
| --- | --- | --- |
| **Winlink Express** | A Windows laptop at the radio | VARA High Frequency (HF), VARA FM, Telnet, or Pactor |
| **Pat** | The Raspberry Pi or another Linux computer | VARA FM, Telnet, or AX.25 packet |
| **RMS Express** | A Windows laptop | Pactor (needs a hardware SCS modem) |

All you need from the radio side is the ICS form the message carried. Winlink attaches ICS forms as a small file named something like `RMS_Express_Form_ICS213.xml`. In your Winlink program, open the message, **right-click that attachment and Save it** somewhere you can find it — or, if you'd rather, just **copy the whole message text**. Either one is enough for FieldCommand. This works the same whether the form came **in** to you or was one you **sent** out.


## Opening the Winlink Form Import Page

1. On a device connected to the FieldCommand Wi-Fi, open the dashboard.
2. Open **Winlink Form Import** (or go straight to the address `http://192.168.50.1/winlink-import.html`).
3. The **📥 Winlink Form Import** page opens. It is laid out as three numbered steps, top to bottom — **1** provide the data, **2** review it, **3** file it. Steps 2 and 3 stay hidden until you've handed it a form.

> _[Figure: The Winlink Form Import page showing Step 1 with the drop zone and paste box]_


## Step 1 — Provide the Winlink Form Data

The first box, **① Provide the Winlink form data**, is where you hand the form over. You have two ways to do it, and either is fine:

- *Drop or browse for the file.* Drag the saved `RMS_Express_Form_*.xml` file onto the large dashed **drop zone** (the 📂 area that reads *“Drop an RMS_Express_Form file here, or click to browse”*). Or click it to open a file picker and choose the file. It accepts `.xml` and `.txt` files.
- *Paste the text.* Below the drop zone is a box labeled *“— or paste below —”*. Paste the form's XML, or the plain Winlink message text, straight into it.

Then click **Parse Form Data**. FieldCommand reads what you gave it and jumps to Step 2. (The **Clear** button empties everything and starts over.) If you dropped or browsed to a file, it parses automatically — you don't even need to click the button.

> **IT CAN READ THE PLAIN MESSAGE TOO** — If you don't have the neat `.xml` attachment — only the message text — paste that. FieldCommand will scan it for `Label: value` lines and pull out what it can. The tidy XML file gives the cleanest result, but the text fallback means a copy-paste is never wasted.


## Step 2 — Review and Correct the Extracted Data

The **② Review & correct the extracted data** box appears with a colored banner telling you what it found. FieldCommand recognizes three ICS forms automatically:

| Banner says | Meaning |
| --- | --- |
| Green — *Detected an ICS-213 General Message* | A general message form. The most common Winlink ICS form. |
| Green — *Detected an ICS-214 Activity Log* | A unit activity log form. |
| Green — *Detected an ICS-309 Communications Log* | A radio communications log form. |
| Amber — *Form type not recognized automatically* | It couldn't tell which form this is. The data is still captured and can be archived; only the three forms above can be re-printed as clean ICS forms. |

Below the banner is a grid of the fields it pulled out, each in its own editable box. **Read them over and fix anything that looks wrong** — nothing here is locked. Longer items (the message body, activity list, log entries) show as multi-line boxes. What you'll see depends on the form type:

| ICS-213 (General Message) | ICS-214 (Activity Log) | ICS-309 (Comms Log) |
| --- | --- | --- |
| Incident, To (Name/Position), From (Name/Position), Message #, Date, Time, Subject, Message Text, Approved By, Reply | Incident, Unit Name, Unit Leader, Op Period From/To, Time From/To, Prepared By, Activities, Personnel | Incident, Op Period From/To, Task No., Operator, Station / Net, Page, Log Entries |

> **THE “FIELDS NOT AUTOMATICALLY MAPPED” BOX** — Winlink forms come in many versions and sometimes carry an extra field FieldCommand doesn't have a home for. Anything like that shows in an amber **Fields not automatically mapped** box below the grid. Those values are **not lost** — they are kept with the archived record. Glance at them in case one really belongs in a field above; otherwise you can ignore them.


## Step 3 — Tag to Incident and File

The **③ Tag to incident & file** box has two small pickers and two action buttons.

| Control | What it does |
| --- | --- |
| **Incident** | Choose which incident this form belongs to. The list is filled from your active incidents. If there are none, it files to a general archive. |
| **Direction** | Say whether this was **Received (incoming traffic)** or **Sent (outgoing traffic)** — so the record shows which way the message went. |

Then pick one of the two buttons:

- *📄 Open in ICS form (print).* Re-draws the data as a proper, printable ICS-213, ICS-214, or ICS-309 form in a new tab, ready to print or save as a paper copy. (Available only for those three recognized forms.)
- *💾 Archive to incident.* Files the form — every field, the unmapped extras, and the original raw text — into the incident record on the server. A green line confirms it was archived, noting the form type and direction.

> **IF THE SERVER CAN'T BE REACHED** — If **Archive to incident** can't reach the server, FieldCommand doesn't throw the form away — it saves a copy **on the device you're using** and shows an amber message. Once the server is back, come back to this page and archive again so the record lands where it belongs.


## Troubleshooting

- *The Winlink Form Import page is grayed out or missing.* Winlink is a licensed-operator feature. Make sure a **Club / Station Callsign** is set in Setup (Chapter 3) and that the **Winlink** module is switched on under Active Modules.
- *It says “Could not find any form data.”* You pasted something it couldn't read. Paste the actual `RMS_Express_Form` XML, or the full Winlink message text — not just a subject line. Saving the XML attachment from your Winlink program gives the best result.
- *The banner is amber and the form type is “not recognized.”* FieldCommand only auto-identifies ICS-213, ICS-214, and ICS-309. You can still **Archive** an unrecognized form (the data is kept), but **Open in ICS form** won't be available for it.
- *Some fields came in blank or in the wrong box.* Winlink forms vary by version. Just type the corrections into the field boxes in Step 2 before you file — and check the amber **Fields not automatically mapped** box in case a value landed there.
- *The Incident list shows “no active incident.”* There are no incidents to attach to right now, so the form will file to the general archive. Start or select an incident first if you want it tied to one.
- *Archiving showed an amber “server unreachable” message.* The form was saved locally on this device so nothing is lost. Reconnect to the FieldCommand server and archive again.


# 28. Amateur Packet Radio Network (AMPRNet) / 44Net Gateway

*The optional gateway that puts every device on your network onto the worldwide amateur-radio IP network (the 44.0.0.0/8 block) — and the status page that shows whether it's up.*

> **QUICK VERSION** — This is an **optional** add-on for groups led by licensed amateur-radio operators. A second Raspberry Pi (the **gateway Pi** at `192.168.50.2`) holds an encrypted tunnel to the worldwide amateur-radio internet. Open the **AMPRNet / 44Net Gateway** page to see whether the tunnel is **UP** or **DOWN**, your assigned 44.x.x.x address, and who's connected. The page auto-refreshes every 30 seconds. Turning the tunnel on or off can only be done sitting at the gateway Pi itself.

> **DOES THIS EVEN APPLY TO YOU?** — This whole chapter applies **only** if a licensed amateur-radio group leads or is a key partner in your deployment. If your organization is a public-safety agency, municipality, or served organization **without** a licensed ham group involved, the 44Net gateway does not apply — skip this chapter. FieldCommand runs fully without it. Every ICS form, net logger, map, and report works on your normal network with no dependency on AMPRNet whatsoever.


## What This Is / What It Is For

**AMPRNet** — the Amateur Packet Radio Network, also called **44Net** — is a private slice of the internet reserved for amateur radio. Years ago the block of addresses beginning with **44** (written `44.0.0.0/8`) was permanently set aside for hams worldwide. A **gateway** is simply a doorway onto that network. FieldCommand's gateway is a **separate, dedicated Raspberry Pi** (the gateway Pi, at `192.168.50.2`) that holds an encrypted **tunnel** — think of it as a private, protected pipe — out to the amateur-radio network's main gateway on the internet.

When that tunnel is up, **every device on your network** can reach amateur stations, Winlink gateways, and APRS servers that live on 44.x.x.x addresses — over the ham network rather than the commercial internet. This page, the **AMPRNet / 44Net Gateway** page, is your window onto that: it doesn't set the gateway up, it **shows you whether it's working** and lets an operator at the gateway Pi turn it on or off.

> **THE GATEWAY PI IS ON ITS OWN** — The gateway Pi is completely separate from the main FieldCommand server. If it's switched off, unplugged, or never deployed, **nothing else is affected** — the rest of the system keeps running normally. It's a bolt-on, not a foundation.


## A Licensed Amateur-Radio Group Must Own This

A 44Net address is assigned to a specific licensed amateur callsign and is governed by the amateur-radio rules (Part 97). That means the registration, the setup, and all day-to-day use have to be led by the amateur-radio group — not the served agency, not an IT department. In practice a licensed technical lead registers the group at **portal.ampr.org** under a club or personal callsign (for example **your club callsign**), requests a small block of addresses, and configures the gateway Pi. Expect the approval to take a few weeks. Full setup steps live in the Installation Guide.

| Your situation | Deploy a 44Net gateway? |
| --- | --- |
| An amateur-radio emergency group leads or co-leads the deployment | Yes — a licensed operator registers and maintains it under their callsign. |
| An amateur-radio club runs the communications section | Yes — a club callsign (for example your club callsign) is the natural choice. |
| Licensed hams are supporting partners only | Maybe — only if those operators fully own the registration and upkeep. |
| Public-safety agency only, no ham group involved | No — an amateur license is required to register. It cannot be run by a non-licensed agency. |


## What a 44Net Gateway Lets You Do

| Capability | What it means in the field |
| --- | --- |
| **Winlink over the ham network** | Reach Winlink radio-email gateways at 44.x.x.x addresses without touching the commercial internet. |
| **APRS over the ham network** | Reach the APRS position-reporting servers on their 44.x.x.x addresses the same way. |
| **Link two FieldCommand sites** | Two deployments that both have a 44Net gateway can share net-log and status data directly over the ham network. |
| **Reach any 44Net station worldwide** | Any amateur station anywhere with a 44.x.x.x address becomes directly reachable from your network. |
| **Permanent fixed addresses** | Your block of 44.x.x.x addresses is yours for good — it never changes, no matter your internet provider or location. |

> **THE HAM RULES STILL APPLY** — Everything crossing the 44Net gateway is amateur-radio traffic under Part 97: no encrypting the **content** of messages (the tunnel's own protection of the connection is fine and expected), no commercial traffic, and station identification is required. Only licensed operators may use it.


## Opening the Gateway Status Page

1. From the dashboard, open **AMPRNet / 44Net Gateway** (or go to `http://192.168.50.1/amprgate.html`).
2. At the very top you'll see a small **Last polled** line and a big **hero banner** — the tunnel light.
3. The page fills itself in from the gateway Pi and refreshes on its own every **30 seconds**. You can force a refresh with the **⟳ Refresh Status** button lower down.

The **hero banner** is the one thing to read first. It has three states:

| Banner | Meaning |
| --- | --- |
| 🛰 Green — **TUNNEL UP — AMPRNet Connected** | The gateway is on the ham network. Your 44.x.x.x address is shown beneath it. |
| ⚠ Red — **TUNNEL DOWN** | The gateway Pi is reachable but the tunnel isn't connected right now. |
| 🔄 Amber — **Gateway Unreachable** | The gateway Pi itself isn't answering — most often it's powered off or unplugged. |

> _[Figure: The AMPRNet Gateway page with a green TUNNEL UP hero banner and the status cards below]_


## The Status Cards

Below the banner is a row of small cards, each a single live number about the gateway's health. You don't set any of these — they just report.

| Card | What it shows |
| --- | --- |
| **AMPRNet Address** | The 44.x.x.x address assigned to your gateway. |
| **Last Handshake** | How long ago the tunnel last exchanged a keep-alive with the far end. Recent is good. |
| **Data Received / Data Sent** | How much traffic has moved in and out through the tunnel. |
| **Gateway CPU Temp** | The temperature of the gateway Pi's processor — a heat check. |
| **Gateway Memory** | Memory used out of total on the gateway Pi. |
| **IP Forwarding** | Whether the Pi is passing traffic through. Shows a green **✓ Enabled** or a red **✗ DISABLED** — it must be enabled for routing to work. |
| **Gateway Uptime** | How long the gateway Pi has been running since its last reboot. |


## Routes, Peers, and the Access Log

Three tables further down give the detail behind the summary cards:

- *Active Routes.* Lists each network the gateway is carrying traffic for, the path it goes **via**, and a green **Active** or red **Not routed** status dot. If the tunnel is up you should see the 44Net route marked Active.
- *Connected Peers.* Lists other stations connected through the tunnel — each peer's key, its endpoint address, which addresses it's allowed to use, when it last made contact, and whether it's **Connected** or **Idle**.
- *Access Log.* A running list of recent gateway logins and station identifications, kept for the Part 97 requirement to log who used the station. It scrolls, newest activity included.


## Tunnel Control — and Why It's Locked Down

At the bottom is a **Tunnel Control** section with buttons — **▲ Bring Tunnel UP**, **▼ Bring Tunnel DOWN**, **↺ Restart Tunnel**, **⟳ Refresh Status**, and a link to **🛰 Open Gateway Dashboard**. Only **Refresh Status** and the dashboard link work from an ordinary operator's laptop or phone. The three tunnel buttons are deliberately restricted.

> **TURNING THE TUNNEL ON/OFF NEEDS PHYSICAL ACCESS** — Bringing the tunnel **up**, **down**, or **restarting** it can only be done by someone **sitting at the gateway Pi's own keyboard**, in its browser, logged in with a valid callsign. It cannot be done from operator laptops or phones on the network. This is on purpose — it keeps control of a licensed radio resource in the hands of a licensed operator physically present at the equipment. If you press one of these buttons from a regular device, the page will tell you it requires access to the gateway Pi itself.

The **About This Gateway** table at the very bottom is a quick reference card: the gateway Pi's address (`192.168.50.2`), its status link, your 44Net block, the tunnel's far-end endpoint, what it routes, and a link to the amateur-radio address portal (`portal.ampr.org`). It's informational — nothing to change there.


## Troubleshooting

- *The banner says “Gateway Unreachable” (amber).* The gateway Pi isn't answering. Check that it's **powered on and plugged into the network**. The main FieldCommand system is unaffected either way.
- *The banner says “TUNNEL DOWN” (red).* The gateway Pi is up but the tunnel isn't connected. An operator at the gateway Pi keyboard can use **Bring Tunnel UP** or **Restart Tunnel**. If it won't come up, the internet path to the far-end endpoint may be out.
- *The tunnel buttons do nothing from my laptop.* That's expected. Tunnel control only works from the browser **on the gateway Pi itself**, logged in with a callsign. Refresh Status and the dashboard link are the only controls meant for regular devices.
- *IP Forwarding shows a red ✗ DISABLED.* Routing won't work until it's enabled on the gateway Pi. This is a setup item — see the Installation Guide's gateway steps.
- *There's no 44Net route in Active Routes.* Usually the tunnel is down. Get the banner green first; the route should then show Active.
- *I can't register for an address.* Registration at `portal.ampr.org` requires a valid amateur-radio license and callsign, and approval takes a few weeks. This must be done by the group's licensed technical lead.


# 29. JS8Call — High Frequency (HF) Digital Messaging

*The weak-signal keyboard-messaging mode that gets short text through when voice and faster data can't — and the dashboard tile that opens it.*

> **QUICK VERSION** — **JS8Call** is a text-messaging mode for ham radio that gets through when signals are extremely weak. It runs on a **separate Windows laptop** connected to an HF radio — not on the FieldCommand server. On the dashboard, the **📡 JS8Call** tile opens that laptop's JS8Call screen in your browser. The first time you tap it, you type in the laptop's address; after that the tile just opens it. Copying JS8Call needs no callsign, but **transmitting requires a licensed operator**.


## What This Is / What It Is For

**JS8Call** is a way to send short typed messages over amateur radio on the High Frequency (HF) bands — the long-distance shortwave bands. Its trick is that it copies **extremely weak signals**, far weaker than you could ever understand by voice and weaker than most other data modes need. When the bands are poor, the power is low, or the antenna is a compromise, JS8Call often still gets a short message through. That makes it a favorite fallback for emergency communications when nothing faster will connect.

It works like a slow group text chat on the radio: you type a line, it goes out as tones, and other stations listening on the same frequency see it appear. Messages can also be **relayed** — a station that hears you can hold your message and pass it along later when the station you're trying to reach comes within range.

> **TRANSMITTING IS A LICENSED-OPERATOR FEATURE** — JS8Call sends on amateur-radio frequencies, so **transmitting requires a properly licensed amateur-radio operator** with a callsign (for example **your club callsign**). Anyone can *listen*, but keying the radio is a licensed activity. Like the other ham features, the dashboard tile is only present when a callsign has been set in Setup (Chapter 3).


## It Runs on a Separate Windows Laptop

This is the one thing to get straight: **JS8Call is not part of the FieldCommand server.** It is its own program, running on a **Windows laptop** that is plugged into the incident's HF radio (for example an IC-7300 radio with a small USB sound-card interface such as a Digirig). That laptop sits on the same Wi-Fi network as everything else. FieldCommand simply provides a convenient **link** to JS8Call's built-in web screen so you can glance at it from the dashboard — it doesn't run the mode or store its messages itself.

> _[Figure: The FieldCommand dashboard with the purple 📡 JS8Call tile highlighted]_


## Opening JS8Call from the Dashboard

On the dashboard, find the purple **📡 JS8Call** tile. It reads *“HF digital messaging via keyboard.”* The small line at the bottom of the tile is a status hint:

| The tile shows | Meaning |
| --- | --- |
| *⚠ Windows laptop — tap to configure IP* | FieldCommand doesn't yet know the laptop's address. Tap the tile once to enter it. |
| *📡 Windows: 192.168.50.x* | The address is set. Tapping the tile opens JS8Call's screen for that laptop. |

1. Tap the **📡 JS8Call** tile.
2. The first time, a small box asks for **the IP address of the Windows laptop running JS8Call** (for example `192.168.50.2`). You can find that address by running `ipconfig` on the Windows laptop.
3. Type it in and confirm. FieldCommand remembers it on this device, and the tile's hint line updates to show the address.
4. The laptop's JS8Call web screen opens in a new browser tab (it lives on **port 2442** of that laptop). From here on, tapping the tile just opens it — no need to type the address again.

> **CHANGING OR CLEARING THE ADDRESS** — Tap the tile and type a **different** address to point it at another laptop, or **leave the box empty and confirm** to forget the address — the tile returns to *“tap to configure IP.”* The address is remembered per device, so each operator's tablet or phone may need setting once.


## What JS8Call Gives You in an Emergency

| Capability | What it does for you |
| --- | --- |
| **Keyboard messaging** | Live, chat-style typed messages between stations. No callsign is needed just to read what comes in. |
| **Store and forward (relay)** | A message can be held by a station that hears it and passed on when the destination is finally in range. |
| **Heartbeat beacons** | The station can quietly announce itself now and then, which also shows who can currently hear whom (useful propagation information). |
| **Group messaging** | A message addressed to a group name — such as **@EMCOMM**, **@ARES**, or **@RACES** — reaches every station monitoring that group. |
| **Extreme weak-signal reach** | Copies signals down to roughly **-24 dB** signal-to-noise — well below what voice or faster data modes can manage. |


## How It Ties Back to the Incident

Because JS8Call runs in its own program, its messages don't flow automatically into the FieldCommand incident record yet. When an important message comes across — say a request or a status report — the operator reads it in JS8Call and **types the key details into the matching FieldCommand tool**: an ICS-213 General Message (Chapter on ICS forms) or the Net Control logger. That keeps the message in the incident's paper trail alongside everything else. A future FieldCommand update is planned to pull JS8Call traffic into the incident log directly; for now it's a quick manual copy.

> **IT'S ON THE PRE-FLIGHT CHECKLIST** — JS8Call appears as an optional item on the deployment **pre-flight checklist**: confirm JS8Call is running on the Windows laptop, its web screen is reachable on port 2442, the frequency is set, and the heartbeat is configured. Ticking it there is a good habit before you rely on it.


## Troubleshooting

- *There's no JS8Call tile on the dashboard.* It's a licensed-operator feature. Make sure a **Club / Station Callsign** is set in Setup (Chapter 3) and the JS8Call module is enabled.
- *Tapping the tile opens a blank page or won't connect.* The address may be wrong, or JS8Call isn't running. Confirm the Windows laptop is on, JS8Call is open, and its web/API server is enabled on **port 2442**. Re-enter the laptop's address by tapping the tile.
- *I don't know the laptop's IP address.* On the Windows laptop, open a Command Prompt and run `ipconfig`; use the address on the same `192.168.50.x` network as FieldCommand.
- *I set it up on my tablet but my phone still says “tap to configure IP.”* The address is remembered per device. Enter it once on each device you use.
- *Messages aren't showing up in the incident record.* That's expected for now — JS8Call traffic is copied into an ICS-213 or the Net Control logger by hand. Direct ingestion is planned for a future release.
- *I can read messages but can't send.* Transmitting requires a licensed amateur operator and a properly configured radio. Reading is open to anyone; keying the radio is not.


# 30. National Traffic System (NTS) Radiogram Generator

*The form that turns a plain message into a properly formatted ARRL radiogram — the standard way hams pass written traffic when phones and internet are down.*

> **QUICK VERSION** — Open **NTS Radiogram Generator**. Fill in the **message number**, **precedence**, **station of origin**, **place** and **date/time**, the **addressee**, and the **message text** (25 words max — the count fills in for you). Click **Generate Radiogram** to see the finished form, then **Print** it, **Save to Log**, or **Copy Text** to read it on the air. Passing traffic on the air requires a licensed operator with a callsign.


## What This Is / What It Is For

A **radiogram** is a short written message sent in a fixed, standard format so any amateur-radio operator can copy it exactly and pass it along — word for word — until it reaches the person it's meant for. It's the format of the **National Traffic System (NTS)**, the long-running amateur-radio message-relay network run under the American Radio Relay League (ARRL). During disasters, when telephones and internet are out, radiograms carry health-and-welfare messages (*“we're safe, everyone's fine”*) and priority traffic out of the affected area.

The **NTS Radiogram Generator** is a fill-in-the-blanks form. You type the parts of the message; it lays them out in the exact radiogram order, counts the words for you, and produces a clean copy you can print, save, read on the air, or hand to a relay operator. It saves you from memorizing the format and from miscounting words.

> **A HAM TRAFFIC-HANDLING FEATURE** — Anyone can *fill in* a radiogram, but **sending it on the air is amateur radio** and requires a properly licensed operator with a callsign (for example **your club callsign**). The form is signed with a station-of-origin callsign for that reason.


## Opening the Generator

1. From the dashboard (or the Net Control page), open **NTS Radiogram** — or go to `http://192.168.50.1/nts.html`.
2. The **📋 NTS Radiogram Generator** page opens. It's a form in four cards — **Preamble**, **Address**, **Message Text**, **Signature** — with the finished radiogram and a saved-message log below.
3. The top-right has two quick buttons: **↺ New Form** clears everything to start fresh, and **📂 Load Saved** jumps down to your saved radiograms.

> _[Figure: The NTS Radiogram Generator with the Preamble, Address, Message Text, and Signature cards]_


## The Preamble (Header)

The first card, **Preamble (Header)**, is the message's routing label — the numbers and codes every relay operator reads first. Starred fields are required.

| Field | What to type |
| --- | --- |
| **Message Number** * | A number for this message (for example `001`). Use the **🔢 Auto-fill Msg #** button to get the next number automatically. |
| **Precedence** * | How urgent this message is — Routine, Welfare, Priority, or Emergency (see the table below). |
| **Handling Instructions** | An optional code (HXA–HXG) telling the delivering station how to handle it (see the table below). |
| **HX Supplement** | Extra detail some handling codes need — a number of hours or a name. |
| **Station of Origin** * | The callsign of the station that first put this message into the system. Typed in capitals automatically. |
| **Check (word count)** * | The number of words in the message text. **You don't type this** — it counts itself as you write. |
| **Place of Origin** * | Where the message started, like `your city your state`. |
| **Date / Time Filed** * | When the message was filed, like `0930 JUN 7`. The **⏰ Auto-fill Date/Time** button fills the current time for you. |


### Precedence — How Urgent Is It?

Pick the one that matches the message. When you choose, a plain-language reminder of what it means appears just below the field.

| Choice | Use it for |
| --- | --- |
| **R — Routine** | Normal message traffic with no urgency. Most messages. |
| **W — Welfare** | A message about the health and welfare of a person — the classic *“we're okay”* traffic sent after a disaster. |
| **P — Priority** | Important messages with some urgency; official or government traffic. |
| **E — Emergency** | Life-or-death urgency, a disaster declaration, or official emergency government communications. Use sparingly. |


### Handling Instructions (Optional)

These optional **HX** codes tell whoever finally delivers the message how to handle it. Leave it on **None** unless you specifically need one. If a code needs a detail (like a number of hours), put that in the **HX Supplement** box.

| Code | Means |
| --- | --- |
| HXA | Collect on delivery (a reply may be collected). |
| HXB | Cancel the message if not delivered within a set number of hours. |
| HXC | Report the date and time the message was delivered. |
| HXD | Report the identity of the station that delivered it, back to the originating station. |
| HXE | The delivering station should get and pass back a reply. |
| HXF | Hold the message for arrival of a person/date. |
| HXG | Deliver by mail or phone if convenient; otherwise cancel — no expense. |


## Address, Message Text, and Signature

The **Address** card is who the message is going to: **Addressee Name** (required), plus optional **Phone Number**, **Street Address**, **City**, and **State / Zip** — enough for the delivering station to make contact.

The **Message Text** card is the message itself, and it has one firm rule:

> **25 WORDS, AND SPELL OUT PUNCTUATION** — Radiogram text is limited to **25 words**. As you type, a live counter shows **Word count: N / 25 max** and turns **red** with an *“over limit”* note if you go over — and the generator won't finish until you're back to 25 or fewer. Use plain words and avoid punctuation: the traditional way to mark a full stop is to say the word **X** in place of a period. Example: `ARRIVED SAFELY X EVERYONE FINE X WILL CALL WHEN SETTLED X LOVE`.

The **Signature** card is who the message is from: **Sender Name / Callsign** and an optional **Phone / Email**. If you leave the signature name blank, the finished radiogram uses the station-of-origin callsign instead.


## The Helper Buttons and the Automatic Check

Three buttons under the form save you typing and arithmetic:

- *⏰ Auto-fill Date/Time.* Fills the **Date / Time Filed** field with the current time in the radiogram's usual format.
- *🔢 Auto-fill Msg #.* Looks at your saved radiograms and fills **Message Number** with the next one in sequence.
- *The Check counts itself.* The **Check (word count)** field is read-only and updates automatically from the message text — you never count words by hand.


## Generating, Printing, and Saving

When the form is filled in, click **📋 Generate Radiogram**. The form is hidden and a clean, black-on-white **radiogram preview** appears, headed *ARRL NATIONAL TRAFFIC SYSTEM — RADIOGRAM*, with the preamble, precedence, address, message text, signature, and a small received/sent/relay footer for handling operators to fill in. (If a required field is missing or the text is over 25 words, it tells you instead of generating.) A row of buttons appears with it:

| Button | What it does |
| --- | --- |
| **🖨 Print Radiogram** | Prints just the radiogram (the form and menus drop away) — good for a paper traffic form. |
| **💾 Save to Log** | Saves this radiogram to the on-page log (and sends a copy to the server) so you can reopen it later. |
| **📋 Copy Text** | Copies the radiogram as plain text to your clipboard — handy for reading it on the air or pasting elsewhere. |
| **📻 Send to Net Log** | A pointer to log this message's traffic over in the Net Control page's Traffic Log. |
| **← Edit** | Returns to the form to make changes. |


## The Saved-Radiogram Log

At the bottom, **Saved Radiograms** is a table of everything you've saved on this device — showing the message number, a colored **precedence** badge, the addressee (**To**), the **origin**, the **date filed**, and the **check**. Each row has a **Load** button to pull that message back into the form (to resend or adjust) and an **✕** to delete it. A **Clear All** button empties the whole list. The list holds your most recent radiograms so a busy traffic session stays organized.

> **SAVED ON THIS DEVICE** — The saved log lives in the browser on the device you're using (a copy is also sent to the server when you save). If you switch to a different tablet or laptop, its own saved list may look different. Print or copy anything you must not lose.


## Troubleshooting

- *Generate Radiogram won't do anything / it pops up a message.* A required field is empty. Fill in **Message #**, **Station of Origin**, **Addressee Name**, and **Message Text**, then try again.
- *It says the text is over the limit.* Radiogram text is capped at **25 words**. Shorten it — drop non-essential words and use the word **X** for periods — until the count is 25 or fewer.
- *The Check field won't let me type in it.* That's correct — the check is the word count and fills itself from the message text.
- *The Precedence reminder doesn't match what I meant.* Re-pick the Precedence; the plain-language reminder below the field updates to match your choice.
- *A saved radiogram is gone / looks different on another device.* The saved log is stored per device. Use **Print** or **Copy Text** for anything you need to keep for certain.
- *I need to actually pass this on the air.* Sending traffic is a licensed-operator activity. The form prepares the message; a licensed amateur transmits it, typically through a net (see the Net Control chapter).


# 31. Repeater Database

*A searchable, filterable list of the VHF/UHF repeaters in your area — loaded from a free RepeaterBook export — that feeds the radio plan, the channel library, and the maps.*

> **QUICK VERSION** — Open **http://192.168.50.1/repeaters.html**. Log in at **repeaterbook.com** (free), search your county, and click **Export → CSV**. Back in FieldCommand, drag that CSV file onto the big drop box. Your repeaters appear in a table you can search, filter, and sort. Click any row to see full details, and use **+ Channel Lib** to send a repeater into the radio plan.


## What This Is / What It Is For

The **Repeater Database** is FieldCommand's local list of the VHF/UHF (Very High Frequency / Ultra High Frequency) repeaters near your operating area — the frequencies, tones, and access details operators need to actually make contact on a repeater. A repeater is a radio station on a tower or building that re-transmits signals to give handheld and mobile radios far more range than they'd have talking directly to each other.

You load the data once, from a free export, and FieldCommand keeps it. From then on that same repeater list feeds three other places in the app: the **ICS-205** communications plan channel picker, the **Channel Library** (Chapter 32), and the **Repeaters** overlay on the tactical and resource maps. Getting good repeater data in here means every other radio-planning tool is already stocked with real, local frequencies.

> **IT ALL WORKS OFFLINE** — Once the data is loaded, the Repeater Database needs no internet. It is stored right in your browser and on the server, so you can search and plan on a dead-quiet network. You only need the internet for the one-time download of the export file — and you can do that at home before you ever deploy.


## Opening the Page and Choosing a Source

Open a browser on the FieldCommand Wi-Fi and go to **http://192.168.50.1/repeaters.html**, or reach it from the dashboard. The page opens with a header reading **📻 REPEATER DATABASE** and a row of **source tabs** just below it. The source tabs decide where the repeater list comes from:

| Source tab | What it does | When to use it |
| --- | --- | --- |
| **📁 Offline File** | Loads repeaters from a file you export from RepeaterBook and drop onto the page. This is the normal, recommended way. | Almost always. It works with any free account and needs no internet after the download. |
| **🔬 Demo Data** | Shows a handful of fake sample repeaters so you can see how the page looks and behaves. | Just for practice. These are clearly-marked placeholders — never use them on the air. |



## Loading a RepeaterBook CSV (the Normal Way)

On the **📁 Offline File** tab, the page shows a large dashed **drop box** titled *Load RepeaterBook Offline Export*. Getting your data in is a five-minute job:

1. On any device with internet, log in at **repeaterbook.com** (a free account is all you need).
2. Search for your county or area, then click **Export → CSV**. A file downloads to that device.
3. Alternatively, use the **RepeaterBook mobile app** → **Export → Share file** to get the same kind of file.
4. Get that file onto a device connected to the FieldCommand Wi-Fi (copy it over, email it to yourself, or use a USB stick).
5. On the Repeater Database page, **drag the file onto the drop box** — or click the drop box (or the **Load file** picker at the top right) to browse for it.
6. A progress box reads *Importing RepeaterBook Data*, then *Loaded N repeaters!* The table appears.

> _[Figure: The Offline File tab with the dashed drop box and the numbered 'how to get the export file' instructions]_

> **CSV, JSON, OR FIELDCOMMAND'S OWN FILE** — The drop box accepts a **RepeaterBook CSV**, a **RepeaterBook JSON**, or a FieldCommand `repeaters.json` file. CSV (comma-separated values — a plain spreadsheet-style file) is the easiest and most common. FieldCommand figures out the format for you and matches up the columns automatically.

> **IT REMEMBERS YOUR DATA** — After a successful import, the repeater list is saved in your browser. Next time you open the page it loads straight from that saved copy — no need to drop the file again. To swap in fresh data, use the **⬆ Load different file** button in the banner, or re-drop a newer CSV. Refresh the export before each activation so tones and status are current.


## Reading the Repeater Table

Once data is loaded, the main table fills the page. Each row is one repeater. The columns, left to right:

| Column | What it shows |
| --- | --- |
| **Output** | The frequency you **listen** on (the repeater's transmit frequency), in MHz. Shown in green. |
| **Input** | The frequency you **transmit** on. Your radio usually sets this automatically from the offset. |
| **Callsign** | The repeater's licensed callsign — its identity on the air. |
| **Tone** | The CTCSS/DCS tone or code needed to open the repeater's receiver (see the note below). Shown as a green badge. |
| **Mode** | How the repeater operates: **FM** (plain analog), **D-STAR**, **C4FM** (Fusion), **DMR**, or **P25**. Each mode gets its own colored badge. |
| **City** | The nearest city or town the repeater covers. |
| **State** | The state (or province) it's in. |
| **EmComm** | Emergency-communications affiliations — **ARES**, **RACES**, **SKY** (SKYWARN), **CAN** (CANWARN) — shown as badges when the repeater is affiliated. |
| **Links** | Internet-linking systems the repeater carries — **EL** (EchoLink), **AS** (AllStar), **WX** (Wires-X). |
| **Use** | Whether the repeater is **OPEN** to all, **CLOSED**, or **PRIVATE**. |
| **Status** | A colored dot: green = on the air, red = off the air. |
| **Dist** | How far the repeater is from your station, in miles. This column only appears when you turn on distance sorting (below). |

> **WHAT A 'TONE' IS** — Many repeaters ignore your signal unless you send a quiet sub-audible tone along with your voice — this keeps them from being triggered by noise or distant stations. **CTCSS** (Continuous Tone-Coded Squelch System) uses a tone in Hertz like *103.5*; **DCS** (Digital-Coded Squelch) uses a numeric code like *D023*. Program the tone shown here into your radio or the repeater simply won't hear you.

Click any column heading (for example **Callsign ↕** or **Output ↕**) to sort by that column; click again to reverse the order. The sorted column turns green.


## Searching, Filtering, and Sorting by Distance

A big county export can hold hundreds of repeaters. The **toolbar** above the table narrows it down. It only appears after data is loaded.

| Control | What it does |
| --- | --- |
| **Search** box | Type a callsign, city, frequency, tone, or word from the notes to instantly narrow the list. |
| **Band** | Limit to one amateur band — 10m, 6m, 2m, 1.25m, 70cm, 33cm, or 23cm. |
| **Mode** | Show only FM, D-STAR, C4FM/Fusion, DMR, or P25 repeaters. |
| **Status** | Show only on-air or only off-air repeaters. |
| **State** | Filter to a single state (the list is built from your loaded data). |
| **Use** | Show only Open, Closed, or Private repeaters. |
| **EmComm** | Show only ARES, SKYWARN, or RACES repeaters. |
| **Sort by distance** | Choose **Nearest first** or **Farthest first**. Turning this on reveals the **Dist** column showing miles from your station. |

Filters stack — set a Band **and** a Mode **and** an EmComm affiliation to zero in on exactly the repeaters you want. The status bar at the bottom always shows how many repeaters match out of the total. To the right of the toolbar sit four buttons: **➕ Add Repeater**, **🗺 Map View**, **⬇ CSV** (export the current filtered list to a file), and **🖨 Print**.


## The Detail Panel

Click any row and a **detail panel** slides in from the right with everything known about that repeater. At the top: the output frequency in large green type, the callsign, and its band/city/state. Below that, a row of affiliation and mode badges, then a list of details:

| Detail row | Meaning |
| --- | --- |
| **Input** | The transmit frequency in MHz. |
| **CTCSS (out)** | The tone your radio must send to open the repeater. Shows *None / CSQ* if none is needed. |
| **CTCSS (in)** | The tone the repeater sends back, if different (often the same). |
| **Offset** | The gap between input and output frequency (for example −0.600 MHz). |
| **Digital Code** | The color code or digital ID, for digital repeaters. |
| **County** | The county the repeater serves. |
| **Distance** | Miles from your station. |
| **Status** | On-air (green) or off-air (red). |
| **Use** | Open, Closed, or Private. |
| **Trustee/Sponsor** | Who owns or runs the repeater. |
| **Last Updated** | When the RepeaterBook record was last touched. |
| **Website** | A link to the sponsor's page, if listed. |

Four buttons sit at the bottom of the panel:

- **📋 Copy** — copies a one-line summary of the repeater to your clipboard, handy for pasting into a message or log.
- **📡 Program** — shows a plain **Programming Summary** (RX, TX, offset, both tones, mode, name) laid out for hand-programming a radio.
- **🖨** — prints the panel.
- **+ Channel Lib** — adds this repeater to the **Channel Library** as a channel, so it's available in the ICS-205 radio plan. A brief **✓ Added** confirms it worked.


## Adding a Repeater by Hand

For a machine that isn't in RepeaterBook — a local club repeater, a temporary machine, or one you just want on the list — click **➕ Add Repeater**. A form opens. **Output Freq (MHz)** is the only required field; fill in whatever else you know:

| Field | What to enter |
| --- | --- |
| **Callsign** | The repeater's callsign (typed in automatically as capitals). |
| **Output Freq (MHz)** *(required)* | The listen frequency, e.g. `146.940`. |
| **Input Freq (MHz)** | The transmit frequency. Leave blank for auto/simplex. |
| **Tone / PL (Hz)** | The access tone, e.g. `103.5`. |
| **Mode** | FM, D-STAR, C4FM, DMR, P25, or NXDN. |
| **City / State** | Where the repeater is. |
| **Latitude / Longitude** | Decimal coordinates, so it can appear on the map. |
| **Notes** | Anything useful, e.g. *EOC primary, wide-area coverage*. |
| **ARES / RACES / SKYWARN** | Check any emergency affiliations that apply. |

Click **Add to List** and the repeater joins the table immediately. A hand-added repeater lives in the current list only — use the **⬇ CSV** button to export and keep it if you want it permanently.


## Map View — Repeaters on a Map

Click **🗺 Map View** in the toolbar to open a full-screen map plotting every repeater in the **current filtered view** that has coordinates. The button shows a count in parentheses, e.g. *🗺 Map View (247)*, so you know how many will plot. Because it follows your filters, you can set a Band or an EmComm filter first, then open the map to see exactly those repeaters.

Pins are colored by mode, matching the legend across the top: green FM, blue D-STAR, orange C4FM/Fusion, purple DMR, red P25, and amber for any ARES/RACES-affiliated repeater (the amber overrides the mode color). Click a pin for a popup with the frequency, offset, mode, tone, location, sponsor, and affiliation badges — plus a **+ Add to Channel Library** button to import it on the spot. Press **Escape** or click **✕ Close** to return to the table.

> **ONLY REPEATERS WITH COORDINATES PLOT** — A RepeaterBook CSV includes latitude and longitude for every repeater, so nearly all of them plot. Repeaters you added by hand without coordinates still appear in the table but not on the map — the map status line tells you how many were left off. The same repeater data also powers the **📡 Repeaters** layer on the Tactical Map and Resource Map.


## Troubleshooting

- *I opened the page and there's no table, just a drop box.* That's the normal empty state — no data is loaded yet. Follow *Loading a RepeaterBook CSV* above to drop in an export file.
- *The import failed with an error.* Make sure the file is a genuine **RepeaterBook CSV or JSON export**, not a spreadsheet you re-saved in another format. Re-download the export and drop it again.
- *Map View says 'No repeaters with coordinates'.* The repeaters currently shown have no latitude/longitude. Clear your filters, or load a RepeaterBook CSV (which includes coordinates for every entry).
- *My hand-added repeater disappeared.* Manually-added repeaters aren't saved permanently. Click **⬇ CSV** to export the list, then re-import that file to keep them.
- *The Dist column is missing.* It only appears when **Sort by distance** is set to *Nearest first* or *Farthest first*. Turn that on and the column appears.
- *The distances look wrong.* Distances are measured from the station's set coordinates. If they're off, the station location may need updating in Setup (Chapter 3).


# 32. Channel Library

*Your agency's own list of radio channels — repeaters, interop, tactical, and public-safety frequencies — that drop straight into the ICS-205 communications plan with one click.*

> **QUICK VERSION** — Open **http://192.168.50.1/channel_library.html**. Click **+ Add Channel**, type a **name** and an **RX frequency**, pick a **Function** color, and **Save**. Your channel is now available in the **ICS-205 Channel Library picker** on every radio plan. Universal channels (National Simplex, APRS, mutual aid) are already there — you only add your own agency's channels.


## What This Is / What It Is For

The **Channel Library** is your organization's curated list of the radio channels you actually use on an incident — your local repeaters, interoperability channels, tactical talk-around frequencies, public-safety talkgroups, medical channels, and any satellite or data channels. Each entry is stored with everything a radio plan needs: a name, the receive and transmit frequencies, the tone, the mode, and which part of the operation it's for.

Its whole purpose is to feed the **ICS-205 Incident Radio Communications Plan**. When someone builds an ICS-205 for an incident, they don't retype frequencies — they pick from this library, and the details fill themselves in. Set the library up once for your jurisdiction and every radio plan afterward is a few clicks instead of a research project.

> **CHANNEL LIBRARY vs. REPEATER DATABASE** — These two are cousins. The **Repeater Database** (Chapter 31) is a big, imported list of *every* repeater in your region — a reference you search. The **Channel Library** is a short, hand-picked list of the specific channels *you plan to use*, including non-repeater channels like simplex, interop, and public-safety talkgroups. You can send a repeater from the database straight into this library with its **+ Channel Lib** button.


## Opening the Page

Open a browser on the FieldCommand Wi-Fi and go to **http://192.168.50.1/channel_library.html**, or reach it from the dashboard. The page opens with a **COMMS** badge and the title **CHANNEL LIBRARY**. Across the top-right sit the main buttons: **+ Add Channel**, **📥 Import CSV**, **📤 Export CSV**, and a **← Dashboard** link. Below the header, a blue notice reminds you that universal channels are always available and you only need to add your agency-specific ones. The full list of channels fills the page in a table.

> **UNIVERSAL CHANNELS ARE ALWAYS THERE** — Common national channels — National Simplex, APRS, NIFOG (National Interoperability Field Operations Guide) channels, and standard mutual-aid frequencies — are built in and always available in the ICS-205 picker automatically. You do **not** need to add them here. Use this page only for your own local repeaters, interop channels, and tactical frequencies. Built-in channels are marked with a small **seed** tag so you can tell them from ones you added.


## Reading the Channel Table

Each row is one channel. The columns, left to right:

| Column | What it shows |
| --- | --- |
| **Channel Name** | The plain-language name, e.g. *County Command*. Built-in channels carry a **seed** tag. |
| **Alpha Tag** | A short radio-display name (up to 10 characters), e.g. *MHCO CMD* — the label your radio screen shows. |
| **RX Freq** | The frequency you **listen** on, in MHz. Shown in green. |
| **TX Freq** | The frequency you **transmit** on. Shows **= RX** when it's the same as the receive frequency (a simplex channel). |
| **PL/DCS** | The access tone or digital code — CTCSS in Hertz (e.g. *100.0*) or DCS (e.g. *D023N*). |
| **Mode** | How the channel operates: FM, NFM (narrow FM), P25, DMR, D-STAR, C4FM, AM, SSB, or Analog. |
| **Function** | A colored badge grouping the channel by role — Command, Tactical, Interop, and so on (explained below). |
| **Division** | Which incident division or group the channel is assigned to, e.g. *Div A*, *Grp SAR*, or *All*. |
| **Notes** | Free text — repeater location, coverage, special instructions. |
| **(actions)** | A **✏** button to edit the channel and a **✕** button to delete it. |

> **WHAT 'RX' AND 'TX' MEAN** — **RX** is receive — the frequency you listen on. **TX** is transmit — the frequency you talk on. On a repeater they differ (the repeater listens on one and sends on the other). On a **simplex** channel — radio-to-radio with no repeater — they're the same, and the table shows **= RX** for the transmit frequency.


## Searching and Filtering

A filter bar sits above the table. The **Search** box narrows the list as you type — it matches any word in the name, frequency, or function. Next to it, the **All Functions** dropdown limits the list to a single function category. The count of matching channels shows on the right. That's the whole filter set — the library is meant to stay short, so you rarely need more.


## Adding or Editing a Channel

Click **+ Add Channel** to create one, or the **✏** button on any row to edit an existing one. The same form opens (titled **+ ADD CHANNEL** or **✏ EDIT CHANNEL**). Fill it in:

| Field | What to enter | Required? |
| --- | --- | --- |
| **Channel Name** | A clear name, e.g. *County Command*. | Yes |
| **Alpha Tag** | A short (10-character) radio-display label, e.g. *MHCO CMD*. | No |
| **Function** | The channel's role — pick from the list (see below). | No (defaults to Tactical) |
| **RX Frequency (MHz)** | The listen frequency, e.g. *155.3400*. | Yes |
| **TX Frequency (MHz)** | The transmit frequency. Leave blank if it's the same as RX. | No |
| **PL Tone / DCS** | The access tone or code, e.g. *100.0 Hz* or *D023N*. | No |
| **Mode** | FM, NFM, P25, DMR, D-STAR, C4FM, AM, SSB, or Analog. | No (defaults to FM) |
| **Division / Group Assignment** | Where the channel is used, e.g. *Div A*, *Grp SAR*, *All*. | No |
| **Notes** | Repeater location, coverage area, or special instructions. | No |

Only **Channel Name** and **RX Frequency** are required. Click **SAVE CHANNEL** to store it, or **Cancel** to back out. Deleting a channel (the **✕** button) asks you to confirm first; built-in seed channels are hidden rather than erased, so a delete is reversible if you ever need it back.


## The Function Categories

The **Function** is a color-coded label that groups channels by their role on the incident. It's what makes a printed ICS-205 easy to scan. The choices:

| Function | What it's for |
| --- | --- |
| **Command** | Command-and-control channels — the Incident Commander and command staff. |
| **Tactical** | Field/operations working channels for the crews doing the work. |
| **Interop** | Interoperability channels shared with other agencies (fire, EMS, law). |
| **Medical** | Channels for medical coordination, hospitals, and aid stations. |
| **Data** | Digital/data channels — APRS, packet, Winlink, telemetry. |
| **Amateur** | General amateur-radio repeaters and simplex frequencies. |
| **Calling** | National calling and monitoring frequencies used to make initial contact. |
| **Mutual Aid** | Regional mutual-aid channels for cross-jurisdiction response. |
| **Air** | Air-to-ground and aviation-coordination channels. |


## Import and Export (CSV)

The Channel Library moves in and out as a **CSV** (comma-separated values — a plain spreadsheet-style file), so you can share a channel plan between systems or edit it in a spreadsheet.

- **📤 Export CSV** downloads the whole library as `channel_library.csv`. Keep it as a backup, or hand it to another FieldCommand system.
- **📥 Import CSV** opens a file picker; choose a CSV and each row with a name and RX frequency is added. Columns are matched by their header names (`name`, `rx_freq`, `tx_freq`, `pl_tone`, `mode`, `function`, `division`, `notes`). When it's done, a message tells you how many channels imported.

> **SET IT UP AT HOME** — Because it exports and imports cleanly, the fastest way to build a big channel plan is in a spreadsheet on a regular computer, then import the CSV here. Do it before you deploy, export a backup, and you can restore the same plan onto any FieldCommand system in seconds.


## Importing from RadioReference (Optional)

The blue notice at the top has a **📡 Import from RadioReference →** link. RadioReference is an online database of public-safety and commercial frequencies. Clicking the link opens the **RADIOREFERENCE IMPORT** panel, where you can pull a county's channels in directly. This is optional and needs a paid account.

1. Enter your own **RadioReference Premium** username and password (they're used only for this one request and are never stored).
2. Type your **ZIP Code** and click **🔍 Lookup ZIP** to find your **County ID** automatically.
3. Optionally pick a **Filter by Tag** — Fire Dispatch, EMS, Law, Interop, Emergency Ops, Amateur, and so on — to limit what comes back.
4. Click **📥 Fetch Channels**. The results appear in a checklist on the right.
5. Review the list, uncheck anything you don't want, then click **Import Selected** — or **Import All** to take everything.

> **A RADIOREFERENCE PREMIUM SUBSCRIPTION IS REQUIRED** — This feature only works with a paid **RadioReference Premium** subscription and your own login. FieldCommand uses your credentials solely to make the request you asked for and does not save them. If you don't have a subscription, skip this — building channels by hand or importing a CSV works just as well.


## How Channels Reach the Radio Plan

Everything in this library flows into the **ICS-205 Communications Plan**. When an operator builds an ICS-205 for an incident, the form's Channel Library picker lists every channel here — the ones you added plus the built-in universal channels. Selecting a channel copies its name, frequencies, tone, mode, and function straight onto the form, so the radio plan is built by picking rather than typing. That is why it pays to keep this library accurate: it is the single source every radio plan draws from.


## Troubleshooting

- *The table says 'Cannot reach server'.* The Channel Library talks to a server on the FieldCommand Pi. Make sure the Pi is powered up and your device is on the FieldCommand Wi-Fi, then reload the page.
- *Save won't work / it says a field is required.* **Channel Name** and **RX Frequency** are both required. Fill them in, then click **SAVE CHANNEL** again.
- *A channel I deleted is still showing / one I want is gone.* Deletes hide the channel rather than erasing it, and built-in **seed** channels can't be permanently removed. Reload the page; if a channel you need is missing, re-add it or re-import your CSV backup.
- *My channels aren't showing up in the ICS-205 picker.* Confirm they saved here first (they should appear in this table). If they're here but not on the form, reload the ICS-205 page so it re-reads the library.
- *The RadioReference import says 'Error' or 'Enter credentials'.* It needs a valid **RadioReference Premium** username and password, and a County ID (use **Lookup ZIP** to fill that in). Without a paid subscription this feature won't return data — build channels by hand or import a CSV instead.
- *I want the same channels on another system.* Use **📤 Export CSV** here, then **📥 Import CSV** on the other system.


# 33. Hospital Proximity & Facilities Directory

*Two address books for an incident: one that ranks nearby hospitals by how fast you can get a patient there (by air or road), and one that keeps every EOC, shelter, staging area, and command post at your fingertips.*

> **QUICK VERSION** — **Hospital Proximity** ranks the hospitals you've entered by how quickly you can reach each one from the incident. Type the **incident latitude/longitude** (or tap **📍 Use GPS**), pick a **helicopter type**, and the list re-sorts by air miles, flight time, and drive time. **Facilities Directory** is a separate address book for EOCs, shelters, staging areas, and command posts — search, filter by type, and tap a card for full details. Add hospitals and facilities with the **+ Add** buttons; both can import and export a spreadsheet (CSV) file.


## What This Is / What It Is For

During an incident you often need two different kinds of location list. The first answers *"where do we take a patient, and how fast can we get there?"* — that's the **Hospital Proximity** page. The second answers *"where is the shelter / the staging area / the command post, and what's its phone and radio?"* — that's the **Facilities Directory**. They're separate pages with separate jobs, so this chapter covers each in turn.

Both are built to work fully offline on the local FieldCommand server — no internet needed to store or read your data. One optional feature on the hospital page (importing from a public federal database) does reach out to the internet, and it's clearly marked; everything else runs on the Pi.


## Hospital Proximity — Setting the Incident Location

Open **Hospital Proximity** (the **MEDICAL** badge in the header). The magic of this page is distance sorting, and that only works once it knows *where the incident is*. The **📍 Incident Location** bar near the top is how you tell it:

| Control | What it does |
| --- | --- |
| **Latitude / Longitude** fields | Type the incident's decimal coordinates here. The list re-ranks the instant you enter them. |
| **↓ From General Info** button | Pulls the coordinates already entered on the incident's General Info form, so you don't retype them. |
| **📍 Use GPS** button | Asks your device for its current GPS position and fills in the coordinates automatically — handy when the device is at or near the scene. |
| **Status text** | Confirms *✓ Distances calculated from …* once coordinates are set, or reminds you to enter them. |

> **NO COORDINATES, NO DISTANCE SORT** — Until you set an incident location, the page still lists your hospitals but can't rank them by distance — the air-miles and drive-time numbers stay blank. Enter coordinates (any of the three ways above) to unlock the sorting.


## Air Transport — Picking a Helicopter

The **🚁 Air Transport** bar sets which aircraft the flight-time estimate assumes. The **Helicopter Type** dropdown lists common air-ambulance models with their cruising speeds — for example *Air Methods Standard (Bell 407) — 155 mph* — or choose **Custom speed…** to type your own miles-per-hour. Whatever you pick, the page adds a realistic **8 minutes** for scene liftoff and **5 minutes** for the hospital approach on top of the raw flight time, so the **Helo Time** figure is a door-to-door estimate rather than pure air time.

> **THE NUMBERS ARE ESTIMATES** — Air miles are straight-line ("as the crow flies"). Ground miles assume roads are about 1.3× the straight-line distance, and drive time assumes roughly 45 mph average. These are planning estimates to compare options quickly — not dispatch-grade routing.


## Sorting and Filtering the List

The **Sort by** row of buttons re-orders the hospital list. Whichever is active is highlighted, and each card gets a **#rank** number once a location is set:

| Sort button | Orders hospitals by |
| --- | --- |
| **✈ Air Miles** | Straight-line distance from the incident (the default) |
| **🚁 Air Time** | Estimated door-to-door helicopter time |
| **🚗 Ground Miles** | Estimated road distance |
| **⏱ Drive Time** | Estimated driving time |
| **🏥 Trauma Level** | Trauma designation, Level I first, ties broken by distance |
| **🔥 Burn Center First** | Burn centers to the top, then by trauma level |

On the right side of that row are extra filters: a **Search** box (matches any text on a card), a **Helipad only** checkbox, and a **Trauma only** checkbox. Combine them to narrow a long list — for example, *helipad-equipped Level I centers, sorted by air time.*


## Reading a Hospital Card

Each hospital shows as a card with a colored left edge by trauma level (red = Level I, amber = Level II, blue = Level III). The card packs in:

- **Name** and, once a location is set, its **#rank** in the current sort.
- **Capability badges** — quick chips such as *Trauma Level I*, *🔥 Burn Center*, *🚁 Helipad*, *👶 Peds Trauma*, *🧠 Stroke*, *❤️ Cardiac*, and *ICU* — so you can see a facility's strengths at a glance.
- **Distance block** — four figures: **Air Miles**, **Helo Time**, **Ground Mi**, and **Drive Est** (only shown once an incident location is set).
- **Phone chips** — tap the green **📞** chip to dial the switchboard, or the red **🚑 ED** chip to dial the emergency department directly.
- **Address, county, and any notes** you've recorded (diversion status, special capabilities, and the like).

> _[Figure: A hospital card showing the name with a rank badge, capability chips, the four-cell distance block, and tap-to-call phone chips]_


## Adding, Importing, and Exporting Hospitals

The page starts empty until you add the hospitals in your response area. There are three ways to get them in, all reached from buttons in the header:

- **+ Add Hospital** — opens a form. Only the **Hospital Name** is required; everything else (address, phone, direct ED line, latitude/longitude, trauma level, and the capability checkboxes for burn, helipad, peds, stroke, cardiac) is optional but makes the sorting and badges more useful. The same form appears when you click **✏ Edit** on a card, with a **Delete** button added.
- **📥 Import CSV** — bulk-load hospitals from a spreadsheet file. The importer flexibly matches columns (a *name* column is the only must-have) so a registry export from your state Emergency Medical Services (EMS) office usually just works.
- **📤 Export CSV** — save your current hospital list out to a spreadsheet file, for backup or to share with another FieldCommand server.

There's also a **🏛 Import from CMS** button. This pulls hospital names, addresses, and phone numbers from the public **Centers for Medicare & Medicaid Services (CMS)** provider dataset — no account needed, but it does require internet. You search by **State** (required) and optional **County**, choose **Acute Care** and/or **Critical Access** types, review the results, and import all or just the ones you tick.

> **CMS DATA HAS NO COORDINATES OR TRAUMA LEVEL** — The CMS dataset does **not** include latitude/longitude or trauma level — those come from a different authority (trauma designations are maintained by the American College of Surgeons, not CMS). So hospitals imported from CMS will have **blank coordinates and blank trauma level**, and won't sort by distance until you edit each one and fill those in. For ready-to-use geocoded, trauma-rated data, ask your state EMS office for their registry and import it as a CSV instead.


## Facilities Directory — What It Holds

The **Facilities Directory** (the 🏥 link) is the second page — a broader address book for every operational location that isn't a hospital-you're-transporting-to. It groups facilities by type, each with its own color accent:

| Type | Typical use |
| --- | --- |
| **EOC** | Emergency Operations Center — the coordination hub |
| **Hospital** | A medical facility recorded here for reference/contact |
| **Shelter** | Mass-care or evacuation shelter |
| **Staging Area** | Where resources gather before assignment |
| **Supply Depot** | Materials and equipment cache |
| **Command Post** | The on-scene Incident Command Post |
| **Other** | Anything that doesn't fit the categories above |

The **toolbar** across the top lets you **Search** by name/address/notes, filter by **Type**, and filter by **Status** — **Active** (green dot), **Standby** (amber), or **Inactive** (gray). Two buttons on the right export the list to a spreadsheet (**⬇ CSV**) or send it to the printer (**🖨 Print**).


## Reading and Editing a Facility

Facilities show as cards grouped under type headings. Each card shows the name, address, a status dot, and quick chips for its **radio frequency** (📻), **phone** (📞), **generator** (⚡), **ADA** accessibility (♿), and **capacity** (👥). Click any card to open its **detail panel** with the full record — coordinates, both phone numbers (tap-to-dial), primary and secondary frequencies with tone, capacity, contact person, on-site ham callsign, and notes. From the detail panel you can **✏ Edit**, **🗑 Delete**, or **📋 Copy Address** to the clipboard.

Click **+ Add Facility** (or **✏ Edit** on an existing one) to open the form. Only the **Facility Name** and **Type** are required. The form is radio-aware — beyond the usual address and phone fields it captures **Primary/Secondary Frequency (MHz)**, a **CTCSS Tone**, an on-site **Ham Callsign**, plus **Generator** and **ADA Accessible** status — which is exactly the information a communications team needs when standing up a site. Click **💾 Save** to store it.

> **SAVED ON THE SERVER, CACHED ON YOUR DEVICE** — Facilities live on the FieldCommand server so every device sees the same list, and a copy is cached in your browser so the page still works if the server is briefly unreachable. A fresh server seeds a few example facilities to show the layout — edit or delete them and add your own.


## Troubleshooting

- *My hospitals show up but with no distances or ranking.* You haven't set an incident location. Enter **Latitude/Longitude** in the Incident Location bar, or use **↓ From General Info** or **📍 Use GPS**. Distances also need each hospital to have its own coordinates saved.
- *A hospital I imported from CMS won't sort by distance.* CMS data comes in without coordinates or trauma level. Click **✏ Edit** on that hospital, add its **Latitude/Longitude** (and trauma level if you know it), and Save — it will then rank with the rest.
- *The Import from CMS search fails.* That feature needs the internet. Confirm you have a WAN connection (Chapter 24), enter a valid 2-letter **State** code, and pick at least one hospital type. For offline use, import a CSV instead.
- *The helicopter times seem off.* Check the **Helicopter Type** dropdown — a slower or faster aircraft shifts every estimate. Remember the figure includes a fixed 8-minute liftoff and 5-minute approach on top of flight time, and that air miles are straight-line.
- *I don't see the facility I just added.* Check the **Type** and **Status** filters in the toolbar — an active filter can hide it. Clear the search box and set both filters to *All*.
- *My facilities disappeared on another device.* Facilities sync through the server; if a device was offline when you added one, it may only be in that device's local cache. Reopen the page while connected to the FieldCommand server so it can sync.
- *Cannot reach server.* Both pages talk to the local FieldCommand server. Make sure your device is on the FieldCommand Wi-Fi and the Pi is powered up, then reload the page.


# 34. Reference Tools — Grid, Cheat Sheets, Resources, Print Center

*Four everyday utility pages: a grid-square calculator, printable radio and ICS cheat sheets, a searchable reference document library, and a one-stop print center. All work fully offline.*

> **QUICK VERSION** — Four utility pages you'll reach for constantly. **Grid** (`grid.html`) converts between coordinates and grid squares and measures distance/bearing. **Cheat Sheets** (`cheatsheets.html`) are printable quick-reference cards — phonetics, Q-codes, prowords, band plans. **Reference Library** (`refs.html`) stores and searches your PDFs and manuals. **Print Center** (`printcenter.html`) prints any form or card and builds an incident cover sheet. Every one works with no internet.


## What These Are / What They Are For

FieldCommand bundles a handful of reference and utility pages that don't belong to any one incident — they're tools you use over and over, before and during an activation. This chapter covers four of them. None needs the internet: they run entirely on the FieldCommand server and your browser, so they work the same on a dead-quiet field network as they do at home.


## The Grid Square Calculator

Open **http://192.168.50.1/grid.html**. The **📡 GRID SQUARE CALCULATOR** converts between two ways of naming a spot on Earth — plain latitude/longitude and the **Maidenhead grid locator** hams use — and measures the distance and direction between two grid squares. A grid locator is a short code like `EN52wa` that packs a location into a few characters, easy to say over the radio.


### Coordinates to Grid, and Grid to Coordinates

The page has two panels side by side:

| Panel | You enter | You get back |
| --- | --- | --- |
| **📍 Lat / Lon → Grid Square** | Latitude and longitude in decimal degrees (fill them in, or tap **📡 Use My Location (GPS)** to pull them from the device). | The 6-character and 4-character grid, plus the field, square, and subsquare broken out, and the position in DMS (degrees-minutes-seconds). |
| **🔤 Grid Square → Lat / Lon** | A Maidenhead locator, 4 or 6 characters (e.g. `EN90ab`). | The center latitude and longitude of that grid, in decimal and DMS. |

Click **Calculate Grid** or **Decode Grid** to run each one. The big amber result shows the answer; the rows beneath break it down.


### Distance and Bearing Between Two Grids

The **📐 Distance & Bearing Between Two Grids** panel takes two grid squares — **Grid 1** and **Grid 2** — and, on **Go**, reports the great-circle distance between them in both kilometers and miles, plus the compass bearing each way (for example *247° WSW*). This is how you answer *how far and which way* is a repeater, a served facility, or another station.


### The Grid Map and Reference

Below the calculators, a **🗺 Grid Square Map (North America)** shows the grid overlaid on the continent — click or tap anywhere on it to look up that spot, and your current result is highlighted with an amber box. At the bottom, a **📋 Maidenhead Grid Reference** table explains the precision levels (field, square, subsquare, extended) and how the letters and digits are assigned, for anyone who wants to understand the code rather than just use it.

> **WHY YOU'D USE THIS** — Grid squares turn a mouthful of coordinates into a short code you can pass by voice without errors. Use this page to find your own grid for the Setup screen, to decode a grid another station gives you, or to measure the distance and heading to a facility or repeater. **Use My Location** needs the browser's location permission and a device that can supply it.


## The Radio Cheat Sheets

Open **http://192.168.50.1/cheatsheets.html**. The **📖 RADIO CHEAT SHEETS** page is a stack of printable quick-reference cards for common radio and Incident Command System (ICS) tasks. A row of tabs across the top switches between them; the **🖨 Print All** button prints every card at once, each on its own page, ready to laminate.

| Tab | What's on it |
| --- | --- |
| **Phonetic Alphabet** | The full NATO phonetic alphabet (Alpha, Bravo, Charlie…) with pronunciation, plus the ITU way of pronouncing numbers. |
| **Q-Codes** | Common HF/amateur Q-codes (QRM, QSY, QTH…) and a separate set of net/EmComm Q-codes (QNI, QNC, QTC…). |
| **Prowords** | Procedure words — SAY AGAIN, ROGER, WILCO, OVER, OUT, CORRECTION, BREAK — with meanings and example use. |
| **Band Plan** | The 2-meter and 70-centimeter band plans (simplex, repeater, calling, APRS segments), HF emergency frequencies, and special-service bands (MURS, FRS, GMRS, marine, aviation). |
| **NTS Precedence** | The message-precedence levels — EMERGENCY, PRIORITY, WELFARE, ROUTINE — plus the ICS triage priorities (Immediate, Delayed, Minor, Expectant). |
| **ICS Structure** | The ICS organization chart (Incident Commander, command staff, the four sections) and a table of the key ICS forms and what each is for. |
| **CTCSS / DCS** | The full CTCSS tone table (all 40-plus tones in Hertz) and common DCS digital codes. |
| **Signal Reports** | The RST readability/strength scale, P25 signal-quality guide, plain-voice FM report shorthand, and a dBm-to-watts reference. |

> **BUILT TO PRINT** — These cards are designed to fit on a single sheet each. Print the ones your operators need, laminate them, and clip them to a go-kit or a position binder. **🖨 Print All** lays every card out one-per-page in a single job. You can also jump to a specific card from the **Print Center** (below).


## The Reference Library

Open **http://192.168.50.1/refs.html**. The **📚 REFERENCE LIBRARY** is where your organization stores the documents an operation depends on — radio manuals, ICS forms and plans, agency and government documents, training materials, and standard operating guides — so they're available on the field network with no internet. Think of it as your deployable filing cabinet.


### Finding a Document

Three tabs across the top split the collection by audience: **📻 Amateur Radio**, **🏛 ICS / Emergency Mgmt**, and **📂 All Documents** (a document can be cross-referenced onto both tabs). Down the left side, a sidebar filters by **Category** — Radio Manuals, ICS Forms & Plans, Agency/Government, Training Materials, Plans & Procedures, Other — and by **Tags**, with a **Sort By** dropdown (newest, title, source, most downloaded). The **🔍 search** box at the top matches titles, descriptions, sources, and tags. Toggle between a card **grid** (**⊞**) and a compact **list** (**☰**) with the buttons on the right.


### Opening and Downloading

Click any document to open its detail window, which shows the file name, size, source, what it applies to, revision, expiry, and description. From there, **⬇ Download** saves the file to your device, **✏ Edit** changes its details, **🗑 Delete** removes it, and **🔗** adds it to (or removes it from) both tabs. PDFs show a thumbnail preview on their card.


### Uploading a Document

Click **⬆ Upload Document** to open the upload panel. Drag a file onto the drop zone (or click to browse — PDF, Word, Excel, PowerPoint, images, KML, or ZIP, up to 200 MB), then fill in the details:

| Field | What to enter |
| --- | --- |
| **Title** *(required)* | A clear name, e.g. *IC-7300 Operating Manual*. |
| **Category** *(required)* | The kind of document — Radio Manual, ICS Form/Plan, Agency, Training, Plan/Procedure, or Other. |
| **Show on tab(s)** *(required)* | Check Amateur Radio, ICS, or both. |
| **Source / Publisher** | Who produced it, e.g. *Icom, ARRL, FEMA*. |
| **Applies To** | Where it applies, e.g. a county, state, or *Statewide*. |
| **Description** | A short note on the contents and when to use it. |
| **Tags** | Comma-separated keywords for searching, e.g. *HF, NIMS, mutual aid*. |
| **Revision / Version** | The revision, e.g. *Rev 3* or *v2.1*. |
| **Expiry Date** | When the document goes stale, if applicable — expired documents are flagged. |

Click **⬆ Upload Document** to store it. A progress bar tracks the upload, and the new document appears in the library.

> **STOCK IT BEFORE YOU DEPLOY** — The Reference Library is only as useful as what you put in it, and it needs no internet once stocked — so load it in advance. Upload your radio manuals, your agency's plans, blank ICS forms, and frequency guides while you're on a normal connection, and every operator can pull them up in the field. Tag them well so they're easy to find when it matters.


## The Print Center

Open **http://192.168.50.1/printcenter.html**. The **🖨 PRINT CENTER** gathers the app's printable forms and reference cards in one place and adds a cover-sheet builder. It's grouped into sections:

- **📋 ICS / NTS Forms** — cards for the ICS-213 General Message, ICS-214 Activity Log, ICS-309 Communications Log, an NTS Radiogram, and a Pre-Flight (deployment readiness) Checklist. Each card has **Open Form** and **Preview**.
- **📖 Reference Cards** — quick links to print the cheat-sheet cards (phonetics, Q-codes and prowords, ICS structure and forms, CTCSS/DCS and signal reports).
- **📻 Operations** — print current logs and boards straight from the live pages: Net Control and public service logs (as ICS-309), the member Roster, and the Resource Board.

Each card's **Preview** button loads that document in a preview pane on the same page, with its own **🖨 Print** button, so you can check a form before committing it to paper.


### The Incident Cover Sheet Generator

The **📄 Incident Cover Sheet Generator** builds a clean cover page for an incident packet. Fill in the fields — Incident Name, Incident Number, Date/Time, Incident Commander, Agency, Operational Period, Location/Jurisdiction, Net Frequency, and a Situation Summary — then click **📄 Generate Cover Sheet** to see the formatted result, and **🖨 Print** to print it. **✕ Clear** empties the form.

> **PRINTING USES YOUR DEVICE'S OWN PRINTER** — Every **Print** button opens your device's normal browser print dialog. That means you can print to any printer that device can reach — or choose *Save as PDF* to keep a copy as a file. There is no central print server, so printing works from any laptop, tablet, or phone on the FieldCommand network, using whatever printer that device already knows about.


## Troubleshooting

- *Grid: 'Use My Location' does nothing or errors.* The browser needs permission to share location, and the device needs a way to determine it. Grant the permission when asked, or type your coordinates in by hand.
- *Grid: the distance/bearing panel says 'Invalid grid(s)'.* One of the two grid squares isn't a valid Maidenhead locator. Enter at least a 4-character grid (e.g. `EN52`) in each box.
- *Cheat Sheets: a card prints cut off.* Use **🖨 Print All** (which paginates each card cleanly), or in the print dialog choose landscape orientation or *Fit to page* for the wider tables.
- *Reference Library: it says the server is unavailable.* The library runs on the FieldCommand Pi. Confirm the Pi is powered on and your device is on the FieldCommand Wi-Fi, then click **⟳** to retry.
- *Reference Library: my upload failed.* Check the file is a supported type and under 200 MB, and that you gave it a **Title** and picked at least one tab. Then try the upload again.
- *Print Center: nothing happens when I click Print.* Your browser may have blocked the print pop-up. Allow pop-ups for the FieldCommand address, or open the form with **Open Form** and print from there.
- *Print Center: the printer I want isn't listed.* Printing uses the device you're on. If that device can't see the printer, connect to it first (or use another device that can), then print — or choose *Save as PDF* and print the file elsewhere.


# 35. Network Hardware — Routers, Switch, and Coverage Extension

*The Wi-Fi router, wired switch, internet sources, and power that carry FieldCommand across a deployment site — what the recommended parts are, how they connect, and how to extend coverage.*

> **QUICK VERSION** — FieldCommand runs on its own private Wi-Fi network called **EMCOMM-NET**. An **ASUS RT-BE58 Go** router broadcasts that Wi-Fi; a **UniFi Switch Lite 16 PoE** ties everything together with cables; a cellular modem (primary internet) and a satellite link (fallback internet) provide the (optional) link to the outside world; and everything runs off a generator or battery. Add more RT-BE58 Go units as **AiMesh nodes** to blanket a bigger site with signal. None of this needs a wall outlet or an internet provider to work.


## What This Is / What It Is For

FieldCommand is a self-contained system: the server, the operator machines, and all the radio gear talk to each other over a small private network that you carry in with you. This chapter describes the recommended network hardware — the router that makes the Wi-Fi, the switch that wires everything together, the two internet sources, and the power that runs it all — and how the pieces connect.

The important idea is that this network is **local first**. Operators connect to the FieldCommand Wi-Fi (**EMCOMM-NET**) and reach the server at **http://192.168.50.1** whether or not any internet is present. Cellular and satellite are there to bridge to the outside world when it helps, but the incident-management work never depends on them. Set the network up once, and it comes up the same way every deployment.

> **YOU DON'T HAVE TO BUILD ALL OF IT** — This is the full recommended build. A small activation might use only the router, one operator machine, and a battery — no switch, no satellite, no mesh nodes. Add pieces as your group grows. The parts and prices here come from the FieldCommand Bill of Materials (`docs/hardware/FieldCommand_BOM.pdf`), which lists everything with current pricing.


## How the Network Fits Together

At the center is the **UniFi Switch Lite 16 PoE**, a wired hub that everything plugs into with network cables. The **ASUS RT-BE58 Go** router connects to the switch and broadcasts the EMCOMM-NET Wi-Fi that operators join. The FieldCommand server (a Raspberry Pi at **192.168.50.1**) and the 44Net gateway (a second Pi at **192.168.50.2**) plug into the switch, as do the operator workstations. The two internet sources — a cellular modem (primary internet) and a satellite link (fallback internet) — feed into the router's two WAN (Wide Area Network) ports. Power comes from a generator or battery through regulated supplies.

> _[Figure: A simple diagram of the FieldCommand network: internet sources into the router, router and Pis and workstations into the central switch, Wi-Fi radiating to operator devices]_

| Piece | Role | Address |
| --- | --- | --- |
| **ASUS RT-BE58 Go** (router) | Makes the EMCOMM-NET Wi-Fi; connects the two internet sources. | Admin at 192.168.50.254 |
| **UniFi Switch Lite 16 PoE** | The wired hub everything plugs into. | — |
| **FieldCommand server** (Pi) | Runs the incident-management app. | 192.168.50.1 |
| **44Net gateway** (Pi) | Handles amateur-radio internet (AMPRNet) routing. | 192.168.50.2 |
| **Raspberry Pi 500** units | Operator workstations. | Assigned automatically |
| **a cellular modem (primary internet)** | Primary internet. | Router WAN port 1 |
| **a satellite link (fallback internet)** | Backup internet, automatic failover. | Router WAN port 2 |


## The Recommended Router — ASUS RT-BE58 Go

The **ASUS RT-BE58 Go** is the recommended router for FieldCommand. It's a compact, portable Wi-Fi 7 travel router built for exactly this kind of mobile use: it runs on USB-C power (no dedicated brick and no wall outlet required), it has **two WAN ports** so it can take a cellular and a satellite source at the same time, and it supports **AiMesh** to extend coverage with more of the same unit. It streets for around $119.

| Spec | ASUS RT-BE58 Go |
| --- | --- |
| **Wi-Fi standard** | Wi-Fi 7 (802.11be) — works with all older devices too |
| **Bands** | 2.4 GHz + 5 GHz dual-band |
| **WAN ports** | 2 — one for cellular/primary, one for satellite/secondary |
| **Power** | USB-C — runs from any 65-watt USB-C adapter or battery bank |
| **AiMesh** | Yes — extends EMCOMM-NET with additional RT-BE58 Go units |
| **Typical range** | About 2,500 square feet indoors, more in the open |

> **WHY TWO WAN PORTS MATTER** — A **WAN port** is where the router's link to the outside world plugs in. Having two lets FieldCommand keep a cellular modem (primary internet) plugged into one and a satellite link (fallback internet) into the other, and switch over automatically if the primary drops. That redundancy is the whole point in an emergency — if the cell network is congested or down, satellite carries on without anyone touching a cable.


## Extending Coverage with AiMesh

**AiMesh** is ASUS's mesh-networking feature. If one router can't cover your whole site — a large building, multiple floors, or a spread-out field location — you add more RT-BE58 Go units as **AiMesh nodes**. Every node broadcasts the *same* EMCOMM-NET name and password, so operator devices roam from one to the next automatically, without anyone reconnecting or noticing. The recommended build carries one primary router plus two spare units ready to serve as nodes.

For best performance, connect each node back to the primary router with a network cable through the UniFi switch (a *wired backhaul*), rather than relying on node-to-node Wi-Fi. To add a node:

1. Connect the AiMesh node to the UniFi switch with an Ethernet cable, and power it on with USB-C.
2. Open the primary router's admin interface at **http://192.168.50.254** (or the ASUS Router phone app). The new node appears there.
3. Go to **AiMesh** and click **Add AiMesh Node**. The node is detected automatically.
4. Click **Connect**. The node joins the mesh and starts broadcasting EMCOMM-NET within about a minute.
5. Place nodes so their coverage overlaps by roughly 20–30 percent — that overlap is what lets devices roam smoothly between them.

> _[Figure: The ASUS router admin AiMesh screen showing the primary router and an added node]_

> **SAME NAME, SEAMLESS ROAMING** — Because every node uses the same Wi-Fi name and password, operators join **EMCOMM-NET** once and stay connected as they walk the site. There's nothing for them to switch between — the mesh hands their device off from node to node behind the scenes.


## The Wired Backbone — UniFi Switch Lite 16 PoE

The **UniFi Switch Lite 16 PoE** is the recommended wired hub — the box every cable plugs into. It has 16 gigabit ports, 8 of which supply **PoE** (Power over Ethernet), meaning they send power *and* data down a single cable so devices like antennas, cameras, or access points don't need their own power adapters. Its management interface shows each port's link status, speed, and power draw, which is a real help when you're tracking down why something won't connect in the field.

| Ports | Recommended use |
| --- | --- |
| **1–2** | FieldCommand server (Pi at 192.168.50.1) and 44Net gateway (Pi at 192.168.50.2) |
| **3–4** | ASUS RT-BE58 Go primary router and AiMesh node uplinks |
| **5–8** (PoE) | Cellular antenna, satellite PoE injector, and any PoE cameras |
| **9–16** | Operator workstations (Raspberry Pi 500 units, a Windows laptop, tablets) |

> **WHAT 'PoE' BUYS YOU** — **Power over Ethernet** means one cable does two jobs — it carries the network and the power. For gear mounted up high or out at the edge of a site (a cellular antenna on a mast, a camera on a pole), that's one cable to run instead of two, and no need for an outlet wherever the device sits. Reserve the 8 PoE ports for those powered devices; use the plain ports for everything else.


## Internet Sources — Cellular and Satellite

FieldCommand's link to the outside world uses two sources, plugged into the router's two WAN ports:

- **a cellular modem (primary internet)** — the primary link, plugged into WAN port 1. A cellular modem/antenna pulls internet from mobile networks. Fast and easy where there's coverage.
- **a satellite link (fallback internet)** — the backup link, plugged into WAN port 2. A satellite dish provides internet where there's no cell service at all, and takes over automatically if the primary drops.

Because both feed the router at once, the system fails over on its own — no one has to reconnect anything if the cellular link degrades. And remember: **the incident-management work does not need either one.** Operators reach the server and do their jobs on the local network regardless; internet only adds outside connectivity (Winlink over the internet, weather feeds, remote coordination) when it's available.

> **THE APP WORKS WITH NO INTERNET AT ALL** — It's worth stating plainly: FieldCommand is offline-first. If both a cellular modem (primary internet) and a satellite link (fallback internet) are unavailable, everything on the server still runs — the dashboard, forms, logs, maps, and radio tools all work over EMCOMM-NET. The internet sources are a convenience layer, never a requirement.


## Powering the System in the Field

With no wall power available, the whole system runs off a generator or a battery. The Raspberry Pis and radios are fed through **Astron RS-35M-AP** regulated linear power supplies — the recommended build uses two, one per Pi cluster — driven from a portable generator, or from a high-capacity LiFePO4 (lithium iron phosphate) battery with a pure-sine inverter.

| Question | Answer |
| --- | --- |
| How much power does it draw? | The complete system pulls roughly 80–120 watts under typical load. |
| How long on a battery? | A 100 amp-hour 12-volt LiFePO4 battery gives about 8–10 hours of runtime. |
| What powers the router? | The ASUS RT-BE58 Go runs on USB-C — any 65-watt USB-C adapter or battery bank works. |
| What powers the field radios? | The Astron RS-35M-AP supplies provide clean, regulated 13.8 volts for the station gear. |

> **SIZE POWER FOR THE MISSION** — For a short activation, a single battery and the USB-C-powered router may be all you need. For a long or multi-day operation, plan for a generator (or a battery you can recharge) and budget around the 80–120-watt draw. Because the router sips USB-C power, a laptop power bank can keep the Wi-Fi alive even while you swap the main battery.


## Running Other Software on the Workstations (LibreOffice & More)

The operator workstations (the **Raspberry Pi 500**) are not locked-down appliances — they are **complete Raspberry Pi desktop computers** running Raspberry Pi OS (a full version of Linux). FieldCommand is simply something you open in a **web browser** on them; it does not take the computer over. So you can run other everyday programs right alongside it.


### An office suite (LibreOffice)

The obvious one is an **office suite** for the documents and spreadsheets the app doesn't cover — a press release, a sign-in sheet, a custom worksheet, a flyer. The best fit is **LibreOffice** (Writer for documents, Calc for spreadsheets, Impress for slideshows, Draw for diagrams):

- It is **free and open-source**, and runs **entirely offline** — no internet needed to use it, which matches FieldCommand's offline-first design.
- It is **usually already installed** — the Raspberry Pi OS “with desktop” image ships LibreOffice by default. If a workstation doesn't have it, install it once (while you have internet) with one command: `sudo apt install libreoffice`.
- It **opens and saves Microsoft formats** (`.docx`, `.xlsx`, `.pptx`), so you can trade files with an agency that uses Microsoft Office.
- The **Raspberry Pi 500** has plenty of memory and speed to run it smoothly.


### It uses the same printer

Anything you print from LibreOffice goes through the **same Linux print system** that FieldCommand's own **Print Center** uses — **CUPS (the Common Unix Printing System)**. Set a printer up once on the workstation (Raspberry Pi OS **Print Settings**, or the CUPS page at `http://localhost:631`), or point it at a shared network printer on EMCOMM-NET, and **both** LibreOffice and the app can print to it. There is no separate print setup for each program.


### Keep your work in the incident record

> **ATTACH IT TO THE INCIDENT** — A document you create in LibreOffice lives only on that one workstation until you do something with it. Because FieldCommand **saves and archives everything attached to an incident**, the durable move is to **attach your LibreOffice file to the active incident** — then it is backed up and archived with the rest of the incident record, not stranded on one machine.


### Other programs, too

The same is true for any Linux software — a **Portable Document Format (PDF) viewer**, an image editor like **GIMP**, an email client, mapping tools. Install them from Raspberry Pi OS's software (the **Add/Remove Software** tool, or `sudo apt install …`). Do it on the **workstations**, not the always-on server, and — because the field is offline-first — **install anything you'll need before deployment, while you still have internet** (or bake it into the SD card image).

> **INSTALL ON THE WORKSTATIONS, NOT THE SERVER** — Add extra desktop software to the operator **Raspberry Pi 500** computers. Leave the always-on FieldCommand **server** lean — it is an appliance running the services, so keep it uncluttered and reliable rather than loading it with desktop apps.


## Troubleshooting

- *Operators can't see the EMCOMM-NET Wi-Fi.* Confirm the ASUS RT-BE58 Go router is powered (USB-C connected) and its link cable to the switch is seated. Watch the switch's port light for that cable, or check the port in the UniFi interface.
- *A far corner of the site has weak or no signal.* Add an RT-BE58 Go as an **AiMesh node** (see *Extending Coverage*), cabled back through the switch, and place it so its coverage overlaps the primary by 20–30 percent.
- *A new AiMesh node won't join.* Make sure it's cabled to the switch and powered, then open the router admin at **http://192.168.50.254**, go to **AiMesh**, and click **Add AiMesh Node**. Give it about a minute after **Connect** to start broadcasting.
- *A PoE device (antenna/camera) has no power.* It must be on one of the switch's **8 PoE ports (5–8)**, not a plain port. Move its cable to a PoE port and check the port's power draw in the UniFi interface.
- *The internet dropped mid-activation.* With both WAN sources plugged in, the router should fail over on its own. Verify a cellular modem (primary internet) is in WAN port 1 and a satellite link (fallback internet) in WAN port 2. Either way, the local app keeps working — the outage only affects outside connectivity.
- *The system won't power up in the field.* Check the battery charge or generator output and that the Astron supplies are on and set to the right voltage. Remember the full system needs roughly 80–120 watts; an undersized battery or bank may not carry it.
- *A workstation is plugged in but can't reach 192.168.50.1.* Reseat its cable at the switch and confirm the port shows a link. If the port is dark, try a different port (9–16) or a known-good cable.


# 36. Appendix — Quick Reference & Administration

*A one-page map of every screen and task, plus the housekeeping an administrator handles: preflight and health checks, backups to the external drive, and archiving finished incidents.*

> **QUICK VERSION** — Everything in FieldCommand starts from the **dashboard** at **http://192.168.50.1**. Pick the **mode** you're working in at the top (**Amateur Radio**, **Public Safety**, or **ICS / Incident Command**), then click the card for the task you want. Before an activation, open **Preflight** for a GO / NO-GO readiness check. When an incident is over, open **Incident Management** to **Archive to USB** and then delete it from the MEM-042. That's the whole day.


## What This Is / What It Is For

This appendix is the page you flip to when you know *what* you want to do but not *which screen* does it. It has three parts: a quick-reference of the main screens by task, a tour of how the dashboard is laid out, and the short list of administration jobs — backups, archiving, and the readiness checks — that one person handles to keep your organization ready. Nothing here is new functionality; it's a map of what the earlier chapters covered, gathered in one place so you don't have to hunt.

You do not need to read this front to back. Skim the first table, find your task, and go. Come back to the Administration sections when you're the person standing the server up or tearing it down.


## Quick Reference — Screens by Task

Find the job you're trying to do in the left column; the middle column names the screen, and the right column is the web address you'd type if you wanted to jump straight there. Every one of these is also a labeled **card** on the dashboard, so you rarely need the address.

| I want to… | Open this screen | Address (after http://192.168.50.1/) |
| --- | --- | --- |
| See everything at a glance | Main Dashboard | index.html |
| Check we're ready to activate | Preflight Deployment Checklist | preflight.html |
| Start or manage the incident | Incident Command Section | incident.html |
| Archive, restore, or delete an incident | Incident Management | incident_mgmt.html |
| Run an amateur-radio net | Amateur Net Control Logger | netcontrol.html |
| Run a public service net | Public Safety Net Logger | starcom.html |
| Watch a net without editing it | Observer Mode | observer.html |
| Check people in | Manual Check-In (ICS-211) | checkin.html |
| Check people in by scanning a code | Scan Check-In | scan_checkin.html |
| Look up who's on the team | Member Roster | roster.html |
| Track resources on a T-card board | T-Card Resource Board | ics/operations.html |
| See resources on a map | GPS-Tracked Resource Map | resource_map.html |
| Fill out an ICS-213 message | ICS-213 General Message | ics213.html |
| Keep an ICS-214 activity log | ICS-214 Activity Log | ics214.html |
| Keep an ICS-309 comms log | ICS-309 Communications Log | ics309.html |
| Build the Incident Action Plan | IAP Assembly (Planning Section) | iap.html |
| Look up an amateur callsign | FCC Callsign Lookup | callsign.html |
| Write an NTS radiogram | NTS Radiogram Generator | nts.html |
| See weather radar | Animated NEXRAD Radar | radar.html |
| Print anything | Print Center | printcenter.html |
| Read a manual or reference | Reference Library | refs.html |
| Change the organization settings | Organization Setup | setup.html |


## A Tour of the Dashboard

The dashboard (`index.html`) is the home screen. Three bands run across the top, and everything below them is a grid of clickable **cards**.

| Part of the screen | What it is / what it does |
| --- | --- |
| **Hero bar** (top) | A dark strip showing your Wi-Fi name (default `EMCOMM-NET`), the system name and version, and a live clock. Amateur mode shows Coordinated Universal Time (UTC) big and local time small; the other modes flip that around. |
| **Mode switcher** (three buttons) | **📻 Amateur Radio**, **🚔 Public Safety**, and **🏛 ICS / Incident Command**. Clicking one changes which cards are shown below, so each kind of operator sees the tools that fit their job. It does not turn anything off — it just re-arranges the screen. |
| **Weather + Radar row** | A National Weather Service (NWS) alerts box and a radar shortcut. These need internet; offline they simply say they're waiting for a connection. |
| **Section labels** (e.g. ⚡ Operations) | Short headings that group the cards beneath them by purpose. |
| **Cards** | Each labeled tile opens one screen. A card shows an icon, a name, a one-line description, and sometimes a small port or source note in the corner. |

> **WHY SOME CARDS AREN'T THERE** — If a card you expect is missing, it's usually one of two things: you're in a different **mode** (switch modes at the top), or that feature was left off in **Setup** under Active Modules. The amateur-radio cards also stay grayed out if no callsign was entered during Setup. See Chapter 3 (Organization Setup) and the Troubleshooting chapter.

> _[Figure: The FieldCommand dashboard: the hero bar, the three-way mode switcher, and the card grid below]_


## Full Page & Address Reference

Every screen in FieldCommand, with the web address you'd type after `http://192.168.50.1/`. You almost never need to type these — click the cards — but it's handy for bookmarks or when someone reads an address to you over the radio. Acronyms are spelled out on first use here for quick lookup.

| Address | What the screen is |
| --- | --- |
| index.html | Main Dashboard |
| incident.html | Incident Management / Command Section |
| incident_mgmt.html | Incident Archive, Restore, Delete |
| event_templates.html | Pre-Planned Event Templates |
| resources.html | Resource Board (flat list) |
| ics/operations.html | T-Card Resource Board (drag-and-drop) |
| resource_map.html | Global Positioning System (GPS)-Tracked Resource Map |
| resource_types.html | National Incident Management System (NIMS) Resource Typing Library |
| checkin.html | Manual Check-In (ICS-211) |
| scan_checkin.html | Quick Response (QR) code / Barcode Scan Check-In |
| roster.html | Member Roster and QR Code Generator |
| netcontrol.html | Amateur Radio Net Control Logger |
| starcom.html | Public Safety Net Logger |
| observer.html | Observer Mode — Read-Only Net View |
| deadmans.html | Dead Man's Switch (net inactivity monitor) |
| iap.html | Incident Action Plan (IAP) Assembly — Planning Section |
| iap_compile.html | IAP One-Click Portable Document Format (PDF) Compilation |
| ics-form.html | Incident Command System (ICS) Form Suite — all forms |
| ics213.html | ICS-213 General Message |
| ics214.html | ICS-214 Activity Log |
| ics309.html | ICS-309 Communications Log |
| fema_costs.html | Federal Emergency Management Agency (FEMA) Public Assistance cost documentation |
| cost_dashboard.html | Real-Time Cost Dashboard |
| wan_settings.html | Wide Area Network (WAN) source configuration |
| wan-status.html | WAN status detail page |
| radar.html | Animated Next Generation Radar (NEXRAD) |
| propagation.html | High Frequency (HF) propagation data |
| tactical.html | Tactical Automatic Packet Reporting System (APRS) map |
| callsign.html | Federal Communications Commission (FCC) callsign lookup |
| amprgate.html | Amateur Packet Radio Network (AMPRNet / 44Net) gateway status |
| nts.html | National Traffic System (NTS) radiogram generator |
| winlink-import.html | Winlink form import |
| hospitals.html | Hospital proximity directory |
| facilities.html | Facilities directory |
| repeaters.html | Repeater database |
| channel_library.html | Channel library |
| cheatsheets.html | Radio / ICS cheat sheets |
| grid.html | Grid square calculator |
| position_checklists.html | ICS position checklists |
| meetings.html | Meeting scheduler |
| printcenter.html | Print Center |
| preflight.html | Preflight Deployment Checklist |
| refs.html | Reference Library |
| setup.html | Organization Setup |
| general_info.html | General Info / ICS-201 |


## Administration — The Preflight Check

The **Preflight Deployment Checklist** (`preflight.html`, the **Preflight** card) is your go/no-go readiness review before an activation. It walks eight groups — **Data Readiness**, **Power Systems**, **Communications Equipment**, **Computing & Software**, **Personnel & Staffing**, **Logistics & Supplies**, **Safety & Security**, and **Agency Coordination** — and for each item you tap one of three buttons: **✓** (GO), **⚠** (CAUTION), or **✕** (NO-GO).

1. Open the **Preflight** card from the dashboard.
2. The **Data Readiness** group at the top **auto-checks itself** — FieldCommand asks the server whether the organization is set up, the FCC database is loaded, the roster has members, and so on, and marks those items for you. Click **↺ Auto-Check** to re-run it.
3. Work down the other groups, tapping ✓, ⚠, or ✕ for each item. A small **red dot** marks items that must be GO before the system will clear you.
4. Watch the big **verdict banner** at the top. It reads **GO**, **CAUTION**, or **NO-GO** and explains why.
5. Use **💾 Save Progress** to keep your answers on the device, **🖨 Print Report** for a paper copy, or **⬇ Export JSON** to save the results as a file.

| Verdict | What it means |
| --- | --- |
| **GO** (green) | Every required item is confirmed and nothing is marked NO-GO. Cleared to activate. |
| **CAUTION** (amber) | No hard failures, but some items are marked caution or aren't checked yet. Review before activating. |
| **NO-GO** (red) | At least one required item is unconfirmed or marked NO-GO. Fix it before you activate. |

> **PREFLIGHT ANSWERS STAY ON YOUR DEVICE** — Your ✓/⚠/✕ choices and notes are saved in the browser you're using (via **Save Progress**), not centrally. Do the preflight on the device you'll keep with you, or print/export it for the record.


## Administration — System Health

FieldCommand runs several small background programs (services). A built-in **health monitor** keeps an eye on them and on the hardware — processor load, memory, disk space, and whether each service is answering. The dashboard surfaces the important parts; the Preflight **Computing & Software** group lists the same services so you can confirm each is green before an activation.

| If this is unhealthy… | What to check |
| --- | --- |
| Web server (nginx) | Nothing loads at all — the MEM-042 may still be booting, or needs a restart. This is the program that serves every page. |
| FCC lookup / config server | Callsign lookups, the roster, nets, and Setup won't save. It's the service behind most data screens. |
| Health monitor | The health readout itself is blank. The rest of the system can still work. |
| Map tile server | Maps show blank tiles. Offline map imagery comes from this service. |
| Disk space low | Archive and delete old incidents (below) to free room before you run out. |

> **GREEN ON THE DASHBOARD IS THE SHORT ANSWER** — You don't need to memorize service names. If the dashboard loads and the Preflight **Computing & Software** items auto-check green, the system is healthy. The service names matter only when something is red and a technically minded person is fixing it.


## Administration — Backups to the External Drive

FieldCommand backs its data up **automatically every night** to an external Universal Serial Bus (USB) drive, if one is connected. The drive must be labeled **FIELDCOMMAND**; the MEM-042 writes incident archives to it under the `incidents` folder. Your job as administrator is simply to **keep that drive plugged in** and to glance at the connection badge now and then.

1. Plug the labeled **FIELDCOMMAND** USB drive into the MEM-042.
2. Open **Incident Management** (`incident_mgmt.html`). At the top, a badge reads **USB Backup Drive Connected ✓** when the drive is seen, or **USB Backup Drive Not Detected** when it isn't.
3. Leave the drive connected. The nightly backup runs on its own — you don't start it by hand.

> **NO DRIVE MEANS NO NIGHTLY BACKUP** — If the badge says **Not Detected**, the nightly backup has nowhere to write and your data lives only on the MEM-042's internal storage. Connect the FIELDCOMMAND drive so the automatic backup can run. For a real activation, having the external drive attached is part of a complete Preflight.


## Administration — Archiving Finished Incidents

When an incident is over, you don't delete it outright — you **archive it to the USB drive first**, confirm the copy is good, and only then remove it from the MEM-042 to free space. The **Incident Management** screen handles all three steps and keeps them in a safe order.

1. Open **Incident Management** (`incident_mgmt.html`).
2. Find the finished incident in the list and click **💾 Archive to USB**. (The button is disabled until the FIELDCOMMAND drive is connected.) A full copy is written to the drive.
3. The incident moves into **Archived on Pi — awaiting deletion**. It's now safe on the drive but still taking up space on the MEM-042.
4. Confirm the archive completed, then click **🗑 Delete from Pi** to reclaim the space. The copy on the USB drive remains.
5. To bring an archived incident back later, find it under **Archives on USB Backup Drive** and click **↩ Restore to Pi**.

> **ARCHIVE BEFORE YOU DELETE** — **Delete from Pi** is permanent for the copy on the MEM-042. Only use it *after* you've archived to the USB drive and confirmed the archive is there. If the drive isn't connected, don't delete — you'd have no backup.

> _[Figure: The Incident Management screen: the USB Backup Drive badge at top, the active incidents with Archive to USB buttons, and the archived-awaiting-deletion list]_


## For Administrators — Behind the Scenes

You do not need any of this to operate FieldCommand — the cards and the dashboard are the whole user experience. This section is only for the technically minded person maintaining the MEM-042, so they know which program answers on which network port. Each service starts automatically at boot and restarts itself if it stops.

| Port | Program | What it handles |
| --- | --- | --- |
| 80 | nginx (web server) | Serves every page and image |
| 5050 | fcc_lookup_server.py | Callsign lookups, nets, roster, hospitals, repeaters, facilities, GPS / dead-man switch, WAN config |
| 5051 | health_monitor.py | System health — processor, memory, disk, service and connectivity status |
| 5055 | ics_platform_server.py | ICS forms, incidents, T-cards, check-ins, IAP, FEMA costs |
| 5056 | reference_server.py | Offline reference library (renders PDFs) |
| 8083 | tile_server.py | Offline map tiles |
| 9000 / 9001 | amprgate_status.py | 44Net gateway status (read-only) and tunnel control (local only), on the gateway MEM-042 |

| Background service | What it keeps running |
| --- | --- |
| ics-platform.service | ICS platform server (port 5055) |
| fcc-lookup.service | FCC lookup and config server (port 5050) |
| health-monitor.service | System health monitor (port 5051) |
| fieldcommand-refs.service | Offline reference library (port 5056) |
| fieldcommand-tiles.service | Offline map tile server (port 8083) |
| deadmans.service | Per-net dead-man switch monitor |
| wan-monitor.service | WAN source monitoring and failover |
| aprs-rf.service | RF APRS receive via a Terminal Node Controller (TNC) |
| kiwix.service | Offline reference library server (Wikipedia, ARRL docs) |
| backup.service / backup.timer | Nightly backup to the USB drive |


## Copyright & License

FieldCommand IMS v1.0 — Copyright © 2026 James Rospopo, KE4CON. Developed for emergency-management and amateur-radio organizations. Source code is released under the MIT License; this documentation under Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0). Project home: `https://github.com/KE4CON/FieldCommand-IMS`.


## Troubleshooting

- *A card I need isn't on the dashboard.* Check the **mode** switch at the top (Amateur / Public Safety / ICS) — cards are grouped by mode. If it's still missing, the feature may be turned off in **Setup ▸ Active Modules**, or the amateur cards are grayed out because no callsign was entered.
- *Preflight says NO-GO but I think we're ready.* Scroll for the item with a **red dot** that's marked ✕ or left unchecked — a required item that isn't confirmed forces NO-GO. Set it correctly, and the banner updates.
- *The Archive to USB button is grayed out.* The **FIELDCOMMAND** USB drive isn't connected or mounted. Plug it in and wait for the **USB Backup Drive Connected ✓** badge, then try again.
- *I archived an incident but it's still in the list.* That's expected — it moves to **Archived on Pi — awaiting deletion** so you can verify the USB copy first. Click **Delete from Pi** once you've confirmed the archive.
- *The nightly backup didn't run.* The USB drive was probably unplugged overnight. Reconnect the FIELDCOMMAND drive; the backup runs on its own the next night, or you can archive incidents manually anytime from Incident Management.
- *Health shows a red service.* Note which one from the tables above and hand it to your technical contact; the service names map directly to what stopped working.


# 37. Glossary

*Plain-language definitions of every term, acronym, and bit of jargon used across FieldCommand and this manual — the incident-command words, the radio words, and the network words, all in one place.*

> **QUICK VERSION** — Ran into a word you don't know — on a screen, in a chapter, or over the radio? It's almost certainly here. Terms are listed **alphabetically** in two plain-language tables. You don't have to read it through; just look up the one word that's bugging you and move on.


## What This Is / What It Is For

Emergency management and amateur radio each come with a wall of abbreviations, and FieldCommand sits right where the two overlap — so its screens use both. This glossary exists so you never have to guess what a label means. Skim it once to get your bearings, then come back whenever a term in another chapter, or on a button in the app, leaves you unsure.

Definitions here are short and practical — what the word means when you're actually operating, not textbook-perfect wording. Where a term names something FieldCommand can *do*, the entry says so, and points you at the chapter that covers it in depth.

> **HOW TERMS ARE WRITTEN** — The first time any acronym appears in a chapter, it's spelled out in full with the short form in parentheses — for example *Incident Command System (ICS)* — and then the short form is used after that. This glossary gives you the same spelled-out form plus a plain-language explanation of what it actually means.


## Terms A through I

| Term | Meaning |
| --- | --- |
| **44Net (AMPRNet)** | The **Amateur Packet Radio Network** — a large block of internet addresses (the `44.x.x.x` range) set aside for amateur radio. FieldCommand can show the status of a 44Net gateway that links your local network to this amateur internet. Ham feature; requires a licensed operator. |
| **Accountability** | Knowing who is on scene, where they are, and that they're safe. In FieldCommand, check-ins and the roster feed accountability so a leader can produce a headcount on demand. |
| **APRS** | **Automatic Packet Reporting System** — an amateur-radio system for sharing positions, short messages, and objects over the air and the internet. FieldCommand's tactical map plots APRS stations. Ham feature. |
| **Callsign** | The unique station identifier the government issues to a licensed radio operator — for example `KE4CON`. FieldCommand uses it to identify operators, look them up in the FCC database, and stamp records. If your group has no licensed operators, the callsign is left blank and the ham features stay off. |
| **Check-in** | The act of an operator or resource reporting in — to a net, or to an incident — so they're logged as present and accounted for. FieldCommand records check-ins by hand (ICS-211 screen) or by scanning a QR code. |
| **Dead man's switch** | A safety timer that watches a net for activity. If nothing is logged for a set number of minutes, it raises an alert — the assumption being that a silent net control station may need help. Named after the railroad brake that stops the train if the operator lets go. |
| **EMCOMM** | **Emergency Communications** — amateur radio operators providing communications support during emergencies and drills. `EMCOMM-NET` is also the default name of FieldCommand's own Wi-Fi network. |
| **EOC** | **Emergency Operations Center** — the physical or virtual room where an agency coordinates its response. Your group may support an EOC or check in with one. |
| **FCC** | **Federal Communications Commission** — the U.S. agency that licenses amateur radio operators. FieldCommand carries an offline copy of the FCC license database so you can look up any callsign without internet. |
| **FEMA** | **Federal Emergency Management Agency** — the federal disaster agency. FieldCommand can document costs in the format FEMA's Public Assistance grant program expects, in case your effort is later reimbursed. |
| **Grid square (Maidenhead)** | A short code such as `EN52wa` that names a rectangle on the globe — the Maidenhead locator system hams use as a compact way to state location. FieldCommand has a calculator to convert between grid squares and latitude/longitude. |
| **IAP** | **Incident Action Plan** — the document that says what the response will do during the next operational period: objectives, assignments, communications, and safety notes. FieldCommand's Planning tools assemble an IAP from ICS forms and compile it to a single PDF. |
| **ICS** | **Incident Command System** — the standard, scalable way the United States organizes any emergency response, from a small event to a disaster. It defines roles (Command, Operations, Planning, Logistics, Finance) and a common set of forms. FieldCommand is built around ICS. |
| **ICS-211** | The ICS **check-in** form — the running list of everyone and everything that arrived at the incident. FieldCommand's Check-In screen produces it. |
| **ICS-213** | The ICS **General Message** form — a simple, standard way to send a written message and get a written reply. FieldCommand has a fill-in-the-blanks ICS-213 screen. |
| **ICS-214** | The ICS **Activity Log** — a time-stamped diary of what a person or unit did during their shift. Kept for the record and for after-action review. |
| **ICS-309** | The ICS **Communications Log** — the official record of radio traffic on a net: who called whom, when, and about what. FieldCommand's net loggers export directly to ICS-309. |
| **Incident** | Any event that needs a coordinated response — a storm, a search, a public-service event, or a drill. In FieldCommand, an **incident** is the container that ties together the nets, forms, resources, and logs for one activation. |


## Terms J through Z

| Term | Meaning |
| --- | --- |
| **JS8Call** | A digital mode and program that sends short keyboard messages over long-distance HF radio, even when signals are too weak for voice. Reachable from FieldCommand as an amateur-radio tool. Ham feature. |
| **Net** | A scheduled on-air meeting of radio operators run to a set procedure — for example a check-in net or a traffic net. FieldCommand logs nets so there's a written record of who participated and what was passed. |
| **Net control (NCS)** | The **Net Control Station** — the operator who runs a net: recognizes stations, keeps order, and logs traffic. FieldCommand's net loggers are the tools that operator uses. |
| **NIMS** | **National Incident Management System** — the nationwide framework that ICS is part of, including standard ways to **type** (categorize by capability) resources. FieldCommand includes a NIMS resource-typing library. |
| **NTS radiogram** | A message formatted to the **National Traffic System** standard — the long-running amateur relay network's fixed format for passing written messages accurately from station to station. FieldCommand generates properly formatted radiograms. Ham feature. |
| **Operational period** | The block of time an IAP covers — often 12 or 24 hours. At the end of each period, planners write a fresh plan for the next one. |
| **Public Safety** | FieldCommand's **public service** dashboard mode and net logger — the tools for logging a public service radio net, with radio IDs and unit tracking, alongside the amateur and ICS tools. Selected from the mode switcher at the top of the dashboard. |
| **QR code** | **Quick Response code** — the square barcode you scan with a camera. FieldCommand can put a member's details in a QR code so check-in is a quick scan instead of typing. |
| **Repeater** | A radio station, usually on a hilltop or tower, that receives on one frequency and re-transmits on another to extend the range of handheld and mobile radios. FieldCommand keeps a searchable database of local repeaters. |
| **Roster** | The list of your group's members — names, callsigns, certifications, and equipment. FieldCommand's roster also generates each member's check-in QR code. |
| **T-card** | A physical or on-screen card, shaped like a **T**, that represents one resource (a person, a team, a vehicle) and slots into a status board. FieldCommand's T-Card board lets you drag resources between columns to track their status at a glance. |
| **Tactical map** | FieldCommand's live operations map — it plots APRS stations, GPS-tracked resources, and shapes you draw, over offline map tiles so it works with no internet. |
| **Talkgroup** | On a digital or trunked radio system, a virtual channel that a group of radios shares — the digital equivalent of a channel. Relevant when your group works alongside a public service system. |
| **TNC** | **Terminal Node Controller** — the hardware (or software) modem that turns radio tones into data and back, so a computer can send and receive packet radio such as APRS. FieldCommand receives RF APRS through a TNC. Ham feature. |
| **WAN** | **Wide Area Network** — in plain terms, the internet connection. FieldCommand is offline-first, but when a WAN source (cellular, satellite, or wired) is available it unlocks online extras like live weather radar. FieldCommand can monitor and fail over between WAN sources. |
| **Winlink** | A system for sending and receiving email over radio when the internet is down, using amateur or government stations as relays. FieldCommand links to Winlink and can import Winlink forms. Ham feature. |

> **ICS FORMS AT A GLANCE** — Four form numbers cover most of what you'll touch: **ICS-211** is the check-in list (who's here), **ICS-213** is a message (say something, get a reply), **ICS-214** is an activity log (what I did on my shift), and **ICS-309** is the communications log (what crossed the net). Learn those four and the rest follow the same pattern.


## Where to Learn More

- For how the dashboard, modes, and cards fit together, see the Appendix (Quick Reference) and Chapter 1 (System Overview).
- For the amateur-radio features — APRS, Winlink, JS8Call, 44Net, NTS — see their dedicated chapters; all of them require a licensed operator and a callsign entered in Setup.
- For running a net and producing an ICS-309, see the Net Control Logger chapter.
- For check-ins, the roster, and accountability, see the roster and check-in chapters.
- Any term marked **Ham feature** stays grayed out unless a callsign is set during Organization Setup (Chapter 3) — that's by design, because those features legally require a licensed operator.


# 38. Troubleshooting & Frequently Asked Questions

*The common problems and questions from across FieldCommand, answered in one place — symptom, cause, and the fix, grounded in how the system actually behaves.*

> **QUICK VERSION** — Most problems are one of three things: **you're on the wrong Wi-Fi** (join **EMCOMM-NET**, then go to **http://192.168.50.1**), **you're in the wrong mode** (switch **Amateur / Public Safety / ICS** at the top of the dashboard), or **a feature is off in Setup** (turn it on under **Active Modules**). Almost everything else is a variation on those. Your data is saved on the MEM-042 automatically — you don't have to.


## What This Is / What It Is For

This chapter is where to start when something isn't working, or when you just have a quick question. It gathers the most common issues from across FieldCommand — can't reach the site, a missing feature, no radar, can't log a net, printing trouble, "where's my data" — into one list. Each answer names the exact screen or setting so you can fix it and get back to work.

Almost everything here is safe to try. Reading screens, switching modes, and opening tools don't change anyone else's view or put anything on the air. When a fix does change a shared setting, the entry says so.

> **TWO CHECKS SOLVE MOST OF IT** — Before you dig in: (1) confirm your device is on the **EMCOMM-NET** Wi-Fi, and (2) confirm you typed the address exactly — **http://192.168.50.1**, including the `http://`. Those two account for the large majority of "it's broken" reports.


## Can't Reach http://192.168.50.1


### The page won't load at all. What do I check?

A blank or "can't connect" page almost always means your device isn't actually talking to the MEM-042 yet — not that the system is down. FieldCommand serves its pages only to devices joined to its own Wi-Fi, so the fix is nearly always about the network, not the app. Work through it in order:

1. Open your device's Wi-Fi settings and confirm you're joined to **EMCOMM-NET** (or whatever your group named the network in Setup). Being near it isn't enough — you have to be **connected** to it.
2. Type the address exactly: **http://192.168.50.1**. Include the `http://`. Don't add `www`, and don't let the browser turn it into a search.
3. If your browser jumps to `https://` (with an `s`) and shows a security warning, retype it with plain `http://`. FieldCommand is a local system and uses `http`.
4. Turn off mobile data on a phone temporarily. Some phones see "no internet" on EMCOMM-NET and silently switch to cellular, which can't reach the MEM-042.
5. Still nothing? The MEM-042 may still be booting (give it a minute or two after power-on) or need a restart. If other people can reach it and you can't, the problem is your device; if nobody can, it's the MEM-042.

> **"NO INTERNET" ON EMCOMM-NET IS NORMAL** — Your phone or laptop may warn that EMCOMM-NET has **no internet access**. That's expected — FieldCommand is an offline system. Choose to **stay connected** anyway (phones often ask). The dashboard and every offline feature work perfectly with no internet; only the few online extras, like weather radar, need a connection.


## A Feature or Card Is Missing


### A screen I expected isn't on the dashboard. Where did it go?

Nothing is deleted — it's almost always hidden on purpose, for one of three reasons. Check them in this order:

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| A whole group of cards changed | You're in a different **mode** | Use the mode switcher at the top: **📻 Amateur Radio**, **🚔 Public Safety**, or **🏛 ICS**. Each mode shows a different set of cards. |
| One optional feature is gone | It was turned off in **Setup ▸ Active Modules** | Open **Setup**, switch that module on, and **Save**. It reappears on the dashboard. |
| The ham cards (APRS, Winlink, 44Net, JS8Call) are grayed out and won't open | No **callsign** was entered in Setup | Enter a valid **Club / Station Callsign** in Setup and **Save**. The ham features unlock. (They stay off without a callsign by design — they legally require a licensed operator.) |
| An online card (radar, alerts) looks dead | You're **offline** — no internet | Expected. Those need a WAN connection; everything else works offline. See the next section. |

> **GRAYED-OUT HAM TOOLS ARE NOT A BUG** — If your group has **no licensed amateur-radio operator**, the amateur features are meant to stay off — the app won't let an unlicensed group transmit on ham bands. Leaving the callsign blank in Setup keeps that whole side of the app tidily out of the way. Enter a callsign only if you actually hold a license for it.


## No Internet Features (Radar, Alerts)


### The weather radar and NWS alerts are blank. Is something broken?

No. FieldCommand is **offline-first** — it's designed to run on a MEM-042 with no internet, and the vast majority of it does. A small number of features pull live data from the internet, and those simply wait quietly when there's no connection:

- **NWS weather alerts** and **animated NEXRAD radar** — need live National Weather Service data.
- **Live map basemaps beyond the offline tiles** — the offline tiles always work; extra online detail does not.
- **FCC callsign lookups are the exception** — they run against a copy of the database stored **on the MEM-042**, so they keep working with no internet at all.

If you want these live features, connect a **WAN** (Wide Area Network — an internet source): a cellular modem (primary internet) as the usual connection, with a satellite link (fallback internet) as a backup. Configure and monitor sources on the **WAN Status** / **WAN Source Configuration** screens. The moment a connection is up, radar and alerts fill in on their own.

> **OFFLINE IS THE POINT** — Running with no internet is not a degraded mode — it's the design. Nets, check-ins, the roster, ICS forms, the IAP, maps on offline tiles, callsign lookups, and printing all work with the MEM-042 sitting on a table and nothing plugged into the wall but power.


## Can't Log a Net


### I opened a net logger but I can't add stations / it's the wrong kind of net.

FieldCommand has more than one net logger because amateur nets and public service nets record different things. Make sure you're in the right one:

| You're logging… | Use this screen | Reached from |
| --- | --- | --- |
| An amateur-radio net | **Amateur Net Control Logger** (`netcontrol.html`) | Amateur Radio mode ▸ the **Amateur Net Control** card |
| A public service net | **Public Safety Net Logger** (`starcom.html`) | Public Safety mode ▸ the net logger card |
| Just watching, no editing | **Observer Mode** (`observer.html`) | A read-only view of a running net — you can't add stations here by design |

- *I can see the net but every field is read-only.* You're in **Observer Mode**. Open the matching logger (Amateur or Public Safety) to actually record traffic.
- *The amateur logger won't let me set my station.* Confirm a **callsign** is entered in Setup — the amateur tools need one.
- *Nothing I log seems to save.* Check the dashboard is otherwise loading. If pages load but data won't save, the config/data service on the MEM-042 may be down — see the Appendix's health section, or restart the MEM-042.


## Printing and PDF


### How do I print a form or save it as a PDF?

FieldCommand prints two ways. Most forms and reports have their own print or **export PDF** button, and there's a central **Print Center** (`printcenter.html`) that gathers the common outputs — ICS-309, the roster, ICS forms, and the full IAP package — in one place.

1. For a single form (an ICS-213, an ICS-309, a preflight report), use that screen's own **Print** or **Export PDF** / **Compile PDF** button.
2. For the standard outputs together, open the **Print Center** card and pick what you want.
3. To save as a PDF instead of putting ink on paper, choose **Save as PDF** (or **Microsoft Print to PDF**) as the destination in your browser's print dialog.

- *The print dialog shows the dashboard menus / clutter.* Use the screen's own **Print** button rather than the browser menu where possible — those pages are laid out to drop the navigation and print clean.
- *I have no printer.* You don't need one. Choose **Save as PDF** in the print dialog and keep or share the file. The IAP tools compile straight to PDF with one click.
- *The printer isn't found.* Printing goes through the MEM-042's print service; confirm the printer is on, connected, and added. Printing needs the printer reachable from the MEM-042, not from your phone.


## Where's My Data — Is It Saved?


### Do I have to save my work? Where does it live?

Your incident data — nets, check-ins, roster, ICS forms, the IAP — is saved **on the MEM-042 automatically** as you go. There's no "save the whole session" button to forget. Every operator's device is just a window onto the one shared copy on the MEM-042, so what one person logs, everyone sees.

| Kind of data | Where it lives | Saved how |
| --- | --- | --- |
| Nets, check-ins, roster, ICS forms, incidents | On the **MEM-042** (the server) | Automatically, and shared to everyone connected |
| Nightly full backup | External **FIELDCOMMAND** USB drive | Automatically overnight, when the drive is connected |
| Finished incidents you archive | External **FIELDCOMMAND** USB drive | When you click **Archive to USB** in Incident Management |
| Your **Preflight** checklist answers | In **your browser**, on your device | When you click **Save Progress** — not shared centrally |

> **THE ONE THING THAT'S PER-DEVICE** — The **Preflight** checklist is the exception — your ✓/⚠/✕ answers are stored in the browser you used, not on the MEM-042. Do the preflight on the device you'll keep, or **Print Report** / **Export JSON** for the record. Everything else is central and automatic.

> **IS MY DATA BACKED UP?** — Keep the **FIELDCOMMAND** USB drive plugged into the MEM-042 and the nightly backup takes care of itself. No drive means no automatic backup — your data then lives only on the MEM-042's internal storage until you connect one. See the Appendix (Administration) for archiving and backups.


## A Few More Quick Answers


### Is it safe to click around while I'm learning?

Yes. Opening screens, switching modes, reading logs, and browsing the reference library change nothing and put nothing on the air. A brand-new MEM-042, before Setup is even done, shows **everything** on purpose so you can explore. The things that have real-world effect — sending traffic, deleting an archived incident — take a deliberate, clearly labeled action.


### Two of us edited the same thing — whose wins?

Because everyone shares the one copy on the MEM-042, the most recent save is what sticks, and everyone's screen catches up to it. For net logging, that's why one person is **net control** at a time; others can ride along in **Observer Mode**.


### The reference library or a manual won't open.

The reference library is served by its own program on the MEM-042. If a document won't open but the rest of the dashboard works, that reference service may be down — note it for whoever maintains the MEM-042 (see the Appendix's service tables), and restart the MEM-042 if you can.


## Troubleshooting

- **http://192.168.50.1 won't load.** You're probably not joined to the **EMCOMM-NET** Wi-Fi, or your phone slipped to mobile data. Join the network, keep the connection despite the "no internet" warning, and retype the address with `http://`.
- **The browser forces https:// and warns.** Retype plain **http://192.168.50.1** — FieldCommand is a local `http` system.
- **A card or feature is missing.** Check the **mode** switch first, then **Setup ▸ Active Modules**. Ham cards need a callsign in Setup.
- **Ham tools (APRS/Winlink/44Net/JS8Call) are grayed out.** By design when no callsign is set. Enter one in Setup and Save — only if you actually hold the license.
- **Radar/alerts are blank.** You're offline; that's expected. Connect a WAN source to enable them; everything else works offline.
- **Can't add to a net.** You may be in **Observer Mode**, or the wrong logger for the net type. Open the Amateur or Public Safety logger to match your net.
- **Print shows menus / no printer.** Use the page's own **Print/Export** button; choose **Save as PDF** if you have no printer; confirm the printer is reachable from the MEM-042.
- **"Did my work save?"** Yes — incident data saves automatically on the MEM-042 and is shared to everyone. Only the **Preflight** checklist is per-device (Save Progress / Export).
- **Is my data backed up?** Only if the **FIELDCOMMAND** USB drive is connected for the nightly backup. Keep it plugged in.
- **A document or reference won't open.** The reference service on the MEM-042 may be down; note it and restart the MEM-042 if the rest works.


## Can I run other programs on the workstations, like an office suite?

**Yes.** The operator workstations (the **Raspberry Pi 500**) are full Raspberry Pi desktop computers running Linux, and FieldCommand is just a web app you open in a browser on them — it does not take the machine over, so you can run other everyday software right beside it.

- For documents and spreadsheets, use **LibreOffice** (Writer / Calc / Impress) — free, fully **offline**, and **usually already installed** on Raspberry Pi OS; if not, `sudo apt install libreoffice`. It reads and writes `.docx` / `.xlsx` for sharing with Microsoft Office users.
- It **prints to the same printer** as the app: all printing goes through Linux's **CUPS (Common Unix Printing System)**, so a printer set up on the workstation works for both LibreOffice and FieldCommand's Print Center.
- **Attach documents you create to the active incident** so they are saved and archived with the rest of the record instead of stranded on one machine.
- Install extra software (a PDF viewer, GIMP, etc.) on the **workstations**, not the always-on server, and do it **before deployment while you have internet**, since the field runs offline.

> **FULL WALKTHROUGH** — The **Network Hardware** chapter covers this in detail under “Running Other Software on the Workstations.”
