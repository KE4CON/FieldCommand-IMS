# FieldCommand IMS — One‑Command Field Server Setup (Quick Start)

*A complete, start‑to‑finish walkthrough of building a FieldCommand application server with the automated setup script. Written to be followed literally, in order, with nothing assumed.*

---

## In a nutshell (read this first)

You are building **one** small computer — a **Raspberry Pi 5** in a **Pironman 5 MAX** case with **two** solid‑state drives — into the FieldCommand server. The finished server hands the whole dashboard to any phone, tablet, or laptop that joins a private Wi‑Fi network called **EMCOMM‑NET** and opens a web browser to **`https://192.168.50.1`**.

The whole build is five moves:

1. **Set up the Wi‑Fi router first** (the ASUS router — it makes EMCOMM‑NET).
2. **Flash** Raspberry Pi OS onto a microSD card and boot the Pi from it.
3. **Run one command:** `sudo bash fieldcommand-setup.sh`, answer a few questions.
4. The script **mirrors the two drives, copies the system onto them, reboots, and installs FieldCommand by itself.**
5. **Plug the Pi into the router with an Ethernet cable**, join EMCOMM‑NET on your iPad, and open `https://192.168.50.1`.

> **THE ONE THING PEOPLE GET WRONG** — **The Raspberry Pi does NOT create the Wi‑Fi.** The **ASUS router** creates EMCOMM‑NET. The Pi plugs into that router with a network cable and answers at `192.168.50.1`. If you skip the router, no EMCOMM‑NET network appears and no device can reach the server — even though the Pi installed perfectly. Set the router up **first** (Part 1 below).

**Acronyms, in plain words:** **OS** = Operating System (the Pi's base software). **SSD** = Solid‑State Drive (fast storage, no moving parts). **NVMe** = the fast way those SSDs plug in. **RAID 1** = two drives kept as identical mirror copies, so one can die with no data lost. **SSID** = the name of a Wi‑Fi network. **DHCP** = the router feature that automatically hands out network addresses. **IP address** = a device's number on the network, like `192.168.50.1`.

---

## Part 0 — What you need before you start

Gather all of this **before** you begin. Missing one item is the most common reason a build stalls.

| Item | What exactly | Why |
|---|---|---|
| Raspberry Pi 5 (16 GB) | The main computer | Runs all FieldCommand tools |
| Pironman 5 MAX case | The tower enclosure that holds two SSDs, a fan, and a small screen | Houses the drives and cooling |
| **Two** NVMe SSDs | 2 × 1 TB M.2 NVMe drives, both installed in the Pironman | The mirror (RAID 1) needs two |
| microSD card | 16 GB or larger | You flash the OS here and boot from it to run setup |
| Official Pi 5 power supply | 27 W USB‑C | The Pi 5 needs the real supply, not a phone charger |
| Monitor, keyboard, mouse | Any HDMI monitor and USB keyboard/mouse | To type the one command on first boot |
| Ethernet (network) cable | One CAT‑6 patch cable | Connects the Pi to the router |
| **ASUS RT‑BE58 Go router** | The travel Wi‑Fi router | **Makes the EMCOMM‑NET Wi‑Fi.** Required for any device to reach the server |
| Internet, during setup only | Home Wi‑Fi or a wired internet connection | The install downloads software, maps, and libraries |
| The FieldCommand files | The `FieldCommand-IMS` folder (about 7 MB) | Contains `fieldcommand-setup.sh` |

> **INTERNET IS NEEDED ONLY WHILE INSTALLING** — The finished FieldCommand system works with **no internet at all**. But the *install* downloads packages, and optionally map tiles and the offline library, so connect the Pi to your home internet (Wi‑Fi or a cable) while you run setup. You disconnect it from home internet afterward; the field network (EMCOMM‑NET) stands on its own.

---

## Part 1 — Set up the ASUS router first (this makes the Wi‑Fi)

**Do this before touching the Pi.** This is the step that was missing before. You are telling the router to broadcast **EMCOMM‑NET** and to live at a network address that will not collide with the server.

You configure the router from a phone or laptop, following ASUS's own first‑time setup (their app or the `router.asus.com` web page). Set these four things:

| Setting | Value to use | Why |
|---|---|---|
| **Wi‑Fi network name (SSID)** | `EMCOMM-NET` | This is the network your iPad and phones join. Use this exact name so it matches the server's default. |
| **Wi‑Fi password** | Your choice — write it down | The password devices type once to join. Use the **same** value you give the setup script later. |
| **Router LAN IP address** | `192.168.50.254` | Deliberately different from the server's `192.168.50.1`, so the two never collide. This is also where you reach the router's own settings page later. |
| **DHCP address pool** | `192.168.50.100` to `192.168.50.200` | The range the router hands out to phones and tablets. It leaves `192.168.50.1` free for the server. |

> **WHY `.254` FOR THE ROUTER AND `.1` FOR THE SERVER** — Many routers default to `192.168.50.1`. So does the FieldCommand server. If you leave the router at `.1`, the two fight over the same address and nothing works. Putting the router at **`192.168.50.254`** keeps the address people type for the tools (`192.168.50.1`) clean and reserved for the server. Do not skip this.

> **WHAT IF `192.168.50.x` IS ALREADY IN USE NEARBY?** — A **separate** nearby Wi‑Fi that happens to use the same `192.168.50.x` numbers is **not a problem**: each Wi‑Fi network is isolated, a device joins only one at a time, and addresses only collide *within* one network. You only have a real conflict when the same subnet appears on the **same wiring** — specifically: (a) the **home internet you plug the Pi into during install** is itself `192.168.50.x` (its router, usually at `.1`, collides with the server), or (b) you **feed a `192.168.50.x` internet line into the ASUS router's WAN port** (router LAN and WAN on the same subnet breaks routing). Fix either one by using a different internet source while installing, **or** move FieldCommand to another range: set **Server IP** to `192.168.150.1`, the **router LAN** to `192.168.150.254`, and **DHCP** to `192.168.150.100–200`. Everything adapts automatically — even the HTTPS certificate is built from whatever Server IP you pick. Just keep the three values on the **same** new range.

When you finish, the router should be broadcasting a Wi‑Fi network named **EMCOMM‑NET**. Confirm your iPad can *see* EMCOMM‑NET in its Wi‑Fi list (you don't have to join yet). If you can see it, the router half is done.

*(Have more than one ASUS router for a big building? Set up just the primary one now; add the others as AiMesh nodes later — see the full Installation Guide, Network Hardware chapter.)*

---

## Part 2 — Flash the microSD card

1. On any computer, install the **Raspberry Pi Imager** from `raspberrypi.com/software`.
2. Insert your microSD card.
3. Open Raspberry Pi Imager. Click **CHOOSE DEVICE** → **Raspberry Pi 5**.
4. Click **CHOOSE OS** → **Raspberry Pi OS (64‑bit)** — pick the **full / Desktop** version (the one with the desktop, not "Lite").
5. Click **CHOOSE STORAGE** → select your microSD card. **Double‑check you picked the card and not another drive** — this erases it.
6. Click **NEXT**. If it offers **OS customization / Edit Settings**, you may set a username, password, and your home Wi‑Fi here so the Pi has internet on first boot. That's optional but convenient.
7. Click **WRITE** and wait for it to finish and verify.

**Put the FieldCommand files where the Pi can reach them.** Two easy options:

- **Simplest:** after flashing, the card shows a drive called **`bootfs`** on your computer. Copy the entire `FieldCommand-IMS` folder onto that `bootfs` drive. It will be waiting on the Pi at `/boot/firmware/`.
- **Or:** copy the `FieldCommand-IMS` folder onto a USB stick and plug it into the Pi after it boots.

> **OPTIONAL — FULLY UNATTENDED INSTALL** — If you want the script to run without asking questions, copy the file `scripts/fieldcommand.conf.sample`, rename the copy to **`fieldcommand.conf`**, edit your answers into it (Wi‑Fi name, password, coordinates, map/library sizes), and drop it onto the `bootfs` drive next to the folder. The setup script finds it automatically and runs hands‑off. If you skip this, the script simply asks you each question on screen — that is perfectly fine.

---

## Part 3 — First boot and the one command

1. Put the microSD card in the Pi. Connect the **monitor, keyboard, mouse**, and the **Ethernet cable to your home internet** (or make sure the home Wi‑Fi you set in the Imager is in range). Plug in power.
2. Let it boot to the desktop. If it asks first‑run questions (language, password), answer them.
3. Open a **Terminal** (the black `>_` icon in the top bar, or menu → Accessories → Terminal).
4. Go to the folder with the files and run the one command. If you copied the folder to `bootfs`, that is `/boot/firmware/FieldCommand-IMS`:

```bash
cd /boot/firmware/FieldCommand-IMS
sudo bash scripts/fieldcommand-setup.sh
```

*(If you put the folder somewhere else — a USB stick or your home folder — `cd` to that location instead. The command is always `sudo bash scripts/fieldcommand-setup.sh`.)*

> **TIP — DO A DRY RUN FIRST** — To see every action the script *would* take without changing a single thing, add `--dry-run`:
> ```bash
> sudo bash scripts/fieldcommand-setup.sh --dry-run
> ```
> Nothing is erased, nothing is installed. When you're satisfied, run it again without `--dry-run`.

### The questions it asks (once, at the start)

You will see a short list of questions. Press **Enter** to accept the value in brackets, or type your own. Here is every one:

| Question | What to do |
|---|---|
| `Install profile [1=Full, default]` | Press **Enter** for **1 (Full)** — the complete server. |
| `Station callsign — leave blank if no amateur operators` | If your group has a licensed amateur‑radio operator, type the callsign. **If not, leave it blank and press Enter** — the ham features stay switched off and everything else still works. |
| `Station latitude` / `Station longitude` | Your location. Press Enter to accept the McHenry County defaults, or type your own (for example `41.8781` and `-87.6298`). |
| `WiFi SSID [EMCOMM-NET]` | **This just records the network name for the server's own display — the Pi does not broadcast it; your ASUS router does.** Type the **same** name you set on the router in Part 1 (`EMCOMM-NET`). |
| `WiFi password` | Again, this is recorded for reference. Type the **same** password you set on the router. |
| `Server IP [192.168.50.1]` | Press **Enter**. Leave it at `192.168.50.1` unless you truly know you need something else. |
| `Download FCC amateur database? (~600MB)` | Type **y** only if you have amateur operators and want callsign lookups offline; otherwise press Enter for **N**. |
| `Offline map tiles [0..3]` | `1` (Essential, ~8 MB) is a good default. `0` skips them. |
| `Kiwix offline library tier [0..3]` | `1` (~2.5 GB) gives an offline medical + Wikipedia library. `0` skips it. Larger tiers take much longer. |

### What happens after you answer

The script now runs on its own. In order, it will:

1. **Update the Pi's bootloader** to a known‑good version (needs internet; skips quietly if offline).
2. **Check that both SSDs are visible.** The Pironman routes both drives through a PCIe switch that must be switched on. If the Pi sees fewer than two drives, the script adds two lines to the boot config and **reboots once**. After that reboot it **picks up where it left off** and continues. *(Your typed answers were saved, so it does not ask again.)*
3. **Ask you to confirm erasing the two SSDs.** It lists the exact drives (size, model, serial) and waits for you to type **`YES`** in capital letters. Nothing is erased until you do. This is the point of no return for the two SSDs.
4. **Build the RAID 1 mirror**, copy the running system onto it, set the Pi to boot from the SSDs (keeping the SD card as a backup), and **reboot into the SSD system.**
5. On that **first SSD boot**, a one‑time service automatically runs the FieldCommand installer (`install.sh`) with your answers — installing all the services, the web server, and switching the site to secure **HTTPS**. This part can take a while if you chose large map/library downloads.

> **THE `YES` PROMPT IS THE SERIOUS ONE** — Typing `YES` erases both SSDs completely. On a brand‑new build that's exactly what you want. Just make sure no drive in the case holds anything you need.

---

## Part 4 — Let the automatic install finish

After the reboot into the SSDs, leave the Pi alone for several minutes (longer if you chose big map or library downloads). When it's done, the services are running and the site is live at **`https://192.168.50.1`**.

You can watch progress if you like. Open a Terminal on the Pi and run:

```bash
journalctl -u fc-firstboot.service -f
```

Press **Ctrl+C** to stop watching. When it reports finishing, the install is complete.

---

## Part 5 — Connect the Pi to the router and verify

Now the two halves meet.

1. **Plug the Ethernet cable from the Pi into the ASUS router** (or into a network switch that connects to the router). The Pi holds the fixed address `192.168.50.1` on that wired connection.
2. On your **iPad**, open **Settings → Wi‑Fi** and join **EMCOMM‑NET** with the password you set.
3. Open a web browser and type the address exactly, including the `https://`:

```
https://192.168.50.1
```

4. The FieldCommand dashboard appears. **Done.**

> **THE FIRST TIME: A CERTIFICATE WARNING** — Because the server uses its own private security certificate, the very first visit may show a "not private" or "not secure" warning. That's expected on a private, offline network. You can tap **Advanced → Proceed** to continue. To clear the warning for good on a device, join EMCOMM‑NET and download the certificate from `https://192.168.50.1/fieldcommand-ca.crt`, then install/trust it — see the full Installation Guide's HTTPS section. This is optional; the tools work either way.

---

## Part 6 — The pull‑a‑drive test (do this once, it matters)

The whole point of two mirrored drives is that one can fail and you lose nothing. **A mirror you have not tested by pulling a drive is a mirror you cannot rely on.** Test it once, on the bench, before the field:

1. `sudo poweroff`. Remove the **microSD card** and **one SSD**. Power on. → The Pi must boot and FieldCommand must come up on the **remaining** SSD alone.
2. Power off. Put that SSD back, remove the **other** one. Power on. → It must boot on the other drive alone.
3. Power off, reinsert **both** drives, power on, then re‑add the drive that was out and watch it re‑sync:

```bash
sudo mdadm /dev/md0 --add /dev/nvme1n1p2
cat /proc/mdstat
```

*(Use whichever drive was out — `nvme0n1p2` or `nvme1n1p2`. `cat /proc/mdstat` shows the mirror rebuilding.)*

---

## Part 7 — Starting over: wiping the drives to re‑test

Yes, you can wipe everything and run the whole setup again. There is a script made for exactly this: **`fc-reset-drives.sh`**. It erases the mirror and both SSDs and clears the setup's saved state so the next run starts clean.

**The one catch: you must run it from the microSD card, not from the SSD system** — you cannot erase the drive you are currently booted from. Because setup told the Pi to boot the SSDs first, do this:

1. **Boot back to the microSD card.** Put the microSD card back in, then tell the Pi to try the SD first. On the Pi (booted from the SSD), run:
   ```bash
   sudo rpi-eeprom-config --edit
   ```
   Change the `BOOT_ORDER` line to `BOOT_ORDER=0xf461` (SD first), save, and reboot. *(In the editor, save with **Ctrl+O**, Enter, then exit with **Ctrl+X**.)*
2. Once you're booted from the SD card, run the wipe:
   ```bash
   cd /boot/firmware/FieldCommand-IMS
   sudo bash scripts/fc-reset-drives.sh
   ```
   It lists the drives and waits for you to type **`YES`**. Add `--dry-run` first if you want to see what it will do without changing anything.
3. Now run the setup again from the top of Part 3:
   ```bash
   sudo bash scripts/fieldcommand-setup.sh
   ```

> **DO YOU EVEN NEED TO WIPE?** — If the only problem you saw was "**EMCOMM‑NET doesn't appear** and my devices can't reach the server," that is almost always the **router** (Part 1), not a bad install. Wiping the Pi will not create the Wi‑Fi. Set up the router and connect the Pi to it first; wipe only if you want a clean end‑to‑end test of the script itself.

---

## Troubleshooting (symptom → fix)

| What you see | What it means and what to do |
|---|---|
| **EMCOMM‑NET does not appear on my iPad** | The **router** is not broadcasting it. The Pi never makes the Wi‑Fi. Go back to **Part 1** and set the router's Wi‑Fi name to `EMCOMM-NET`. Confirm the router has power and finished its own setup. |
| **The Pi is still on my home network** | Expected during install — the installer only pins the **wired Ethernet** address (`192.168.50.1`); it never touches the Pi's Wi‑Fi. For field use, connect the Pi to the ASUS router by **Ethernet cable**; you can then disconnect the home Wi‑Fi. |
| **I can't reach `https://192.168.50.1`** | (1) Is your device joined to **EMCOMM‑NET** (not your home Wi‑Fi or cellular)? (2) Is the Pi plugged into the router by Ethernet and powered on? (3) Did you set the **router's** own address to `192.168.50.254` (Part 1) so it doesn't collide with the server? (4) Type the full address including `https://`. |
| **The browser searched the web instead of loading the page** | Some browsers treat `192.168.50.1` as a search term. Type the full **`https://192.168.50.1`**. |
| **"Only 1 NVMe drive detected" and it stops** | Both SSDs aren't seated. Power off, re‑seat both M.2 drives firmly, check the Pironman's PCIe ribbon (FFC) cable at both ends, and run the setup again. |
| **The setup rebooted and I'm not sure it came back to setup** | That reboot is normal (it turns on the second drive slot). Open a Terminal and just run the same command again: `sudo bash scripts/fieldcommand-setup.sh`. Your answers were saved; it resumes and asks you to confirm the erase. |
| **The Pironman power button, fan, or OLED screen don't work** | These are **not** FieldCommand features — the Pironman case's power button, fans, and screen are run by **SunFounder's own Pironman software**, which FieldCommand does not install by default. You can turn it on: answer **y** to the "Install SunFounder Pironman case software" question during setup (or set `INSTALL_PIRONMAN="y"` in `fieldcommand.conf`). To install it by hand on the Pi at any time: first run `sudo raspi-config` → **Advanced Options → Shutdown Behaviour → Full Power Off** and reboot, then run the command below, and reboot again. After that the fan, OLED, and a single-press safe shutdown all work. |
| **The Raspberry Pi OS Shutdown / Reboot menu items do nothing at all (screen doesn't change)** | This is a Raspberry Pi OS desktop issue, separate from the Pironman software and from FieldCommand. First test from a terminal: run `sudo reboot`. If that restarts the Pi, the problem is only the desktop menu (a session or permission issue) — updating Raspberry Pi OS (`sudo apt update && sudo apt full-upgrade`) and rebooting usually fixes it. If `sudo reboot` in a terminal *also* does nothing, capture `systemctl status systemd-logind` and the last lines of `journalctl -b` and ask for help. |
| **Networking is flaky / the Pi can't reach the internet during install, and my home network is also `192.168.50.x`** | Your home network and the FieldCommand server are using the same address range on the same wiring — they collide. Either install using a different internet source, or move FieldCommand to a new range (Server IP `192.168.150.1`, router LAN `192.168.150.254`, DHCP `192.168.150.100–200`). See the "What if `192.168.50.x` is already in use nearby?" note in Part 1. |
| **I want to see the install log** | It's saved at `/var/log/fieldcommand-setup.log` and `/var/log/fieldcommand-install.log`. The last 50 lines of each are the most useful when asking for help. |

**Pironman case software — the by‑hand install command** (run on the Pi, with internet, after setting Full Power Off in `raspi-config`):

```bash
curl -sSL "https://raw.githubusercontent.com/sunfounder/pironman5/v1/install.sh" | sudo bash -s -- --variant max
```

Reboot after it finishes. This is SunFounder's own software for the Pironman 5 case; it is optional and unrelated to the FieldCommand tools.

---

## The short version, one more time

1. **Router first** — ASUS router broadcasts `EMCOMM-NET`, router at `192.168.50.254`, DHCP `.100–.200`.
2. **Flash** microSD with Raspberry Pi OS (64‑bit, Desktop); copy the `FieldCommand-IMS` folder to `bootfs`.
3. **Boot the Pi from SD, open Terminal:** `cd /boot/firmware/FieldCommand-IMS` then `sudo bash scripts/fieldcommand-setup.sh`.
4. Answer the questions, type **`YES`** to erase the drives; let it build the mirror, reboot, and install itself.
5. **Ethernet‑cable the Pi to the router**, join **EMCOMM‑NET**, open **`https://192.168.50.1`**.
6. Do the **pull‑a‑drive test**. To re‑test from scratch: boot the SD card and run **`fc-reset-drives.sh`**, then start over.

*The Raspberry Pi does not make the Wi‑Fi. The router does. That one fact is the difference between "it didn't work" and "it works."*
