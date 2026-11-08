# Using it

## JS8Call + CommStat: a session, start to finish

1. **Start the station.** Run `websdr-js8-start` in a terminal, or use *Start WebSDR
   JS8Call + CommStat* from your applications menu or Desktop. It creates two
   virtual audio devices, starts JS8Call, waits for its API port, then starts
   CommStat.
2. **Play a web SDR.** In your browser, open a WebSDR (e.g. from websdr.org) or a
   KiwiSDR, start its audio, and tune it to a JS8 frequency in **USB** mode.
3. **Route the audio.** Back in the launcher window press Enter and choose the
   browser stream from the menu (it looks like *Firefox - the page title*). From
   now on that tab plays into JS8Call instead of your speakers - you won't hear it;
   that's expected.
4. **Watch it decode.** JS8Call shows decoded traffic; CommStat, which connected
   to JS8Call automatically, shows heard stations and any STATREPs on its map and
   lists.
5. **Stop.** `websdr-js8-stop` (or the *Stop* shortcut). It closes both apps and
   removes the virtual audio devices, so the browser plays through your speakers again.

You can close the launcher's terminal window at any time; JS8Call and CommStat keep
running until you stop them.

## Tuning the web SDR

JS8 is a weak-signal mode sent as audio tones, so the SDR must be in **USB** with a
passband wide enough to carry roughly 500-2500 Hz of audio (a normal USB passband,
about 300-2700 Hz or wider, is fine). Set the SDR's dial to the JS8 dial frequency;
signals then appear at their audio offsets in JS8Call's waterfall.

JS8Call's standard dial frequencies (all USB):

| Band | MHz | | Band | MHz |
|---|---|---|---|---|
| 160 m | 1.842 | | 17 m | 18.104 |
| 80 m | 3.578 | | 15 m | 21.078 |
| 40 m | 7.078 | | 12 m | 24.922 |
| 30 m | 10.130 | | 10 m | 28.078 |
| 20 m | 14.078 | | 6 m | 50.318 |

Activity varies with the band and time of day; 40 m and 20 m are good places to start.
JS8Call has no radio to tune, so the frequency it displays is only informational:
set its band to match what you tuned the SDR to.

**Audio level:** adjust the volume on the WebSDR/KiwiSDR page (or the browser tab),
not in the launcher. The level meter beside JS8Call's waterfall should sit roughly in
the middle of its range - not pinned at the top, and not near zero.

## CommStat

CommStat's connector is created for you (named `WebSDR`, auto-connect on, RF Ack off).
The first time, you may want to:

- Use CommStat's **Manage Groups** dialog to add the groups/nets you follow, so their
  messages are shown.
- Optionally add a **QRZ** login (QRZ Settings) for callsign look-ups.

(These dialogs are in CommStat's menus; the exact menu layout can change between CommStat versions.)

CommStat connects to JS8Call **once, at startup**, so JS8Call has to be running first -
`websdr-js8-start` takes care of that order. If you restart JS8Call on its own, open
CommStat's *JS8 Connectors* dialog, select the `WebSDR` row and click **Reconnect**.

## Options

| Command | Effect |
|---|---|
| `websdr-js8-start --no-route` | Start the apps but skip the audio-routing step (you'll route it yourself). |
| `websdr-js8-start --no-commstat` | JS8Call only. |
| `websdr-js8-start` again | Safe at any time: everything already running is reused (handy to re-route audio after changing sites). |

## Changing settings

Settings live in `~/.config/websdr-js8/config` (plain `KEY=VALUE` lines): the JS8Call
profile name, the virtual-device names, the JS8Call API ports, the FLDIGI station's
folders, devices and ports (`FLDIGI_DIR`, `NBEMS_DIR`, `FL_SINK`, `FL_TXVOID`,
`FL_XMLRPC_PORT`, `FL_ARQ_PORT`, `FL_KISS_IO_PORT`, `FL_KISS_OUT_PORT`), and your callsign
and grid. Environment variables named `WEBSDR_JS8_<KEY>` override them (for example
`WEBSDR_JS8_TCP_PORT=2500 websdr-js8-start`). Callsign, grid and state are also stored
inside JS8Call's and CommStat's own settings; change them there.

## FLDIGI + FLMSG + FLAMP: a session, start to finish

1. **Start the station.** Run `websdr-fldigi-start`, or use *Start WebSDR FLDIGI +
   FLMSG/FLAMP* from your applications menu or Desktop. The first time, it creates the
   station's own settings: a copy of `~/.fldigi` (so your macros, frequency list and
   modem settings carry over) in `~/.fldigi-websdr`, and FLMSG/FLAMP settings in
   `~/.nbems-websdr`. If you've never run FLDIGI, it starts from fresh settings with
   the callsign and grid you gave the installer.
2. Every start then switches off rig control, PTT and spotting, creates two virtual
   audio devices, and starts FLDIGI, which opens FLMSG and FLAMP.
3. **Play and tune a web SDR** in **USB** mode, to the dial frequency you'd use on a
   radio. Signals appear at their audio offsets in FLDIGI's waterfall (for example an
   AmRRON net on 7.110 MHz dial with Contestia at 900 Hz).
4. **Route the audio**: press Enter in the launcher window and pick the browser stream.
5. **Watch it decode.** Click a signal in the waterfall, or let RSID switch the mode
   for you. Received FLMSG forms open in FLMSG; FLAMP collects received files in
   `~/.nbems-websdr/FLAMP/rx`.
6. **Stop.** `websdr-fldigi-stop` closes FLAMP, FLMSG and FLDIGI (asking FLDIGI to
   close itself, so it saves its settings) and removes its virtual audio devices.

Both stations can run at the same time: they use different audio devices and ports.
Play each in its own browser tab (one per frequency) and pick the right tab in each
launcher. The FLDIGI station can also run beside a normal, radio-connected FLDIGI.

| Command | Effect |
|---|---|
| `websdr-fldigi-start --no-route` | Start FLDIGI, FLMSG and FLAMP but skip the audio-routing step. |
| `websdr-fldigi-start` again | Safe at any time: re-routes the audio and reuses everything already running. |

## Trying the FLDIGI station: the one-click receive test

No web SDR, no net on the air? `amrron-rx-test` (the *AmRRON Receive Test* icon) tests the
whole FLDIGI + FLMSG + FLAMP chain with recorded transmissions from AmRRON's "Receiving HF
Digital" videos on YouTube:

1. Click the icon. It stops the FLDIGI station if it's running, checks FLDIGI's control
   port is free, starts the station set to Contestia 4/250 at 900 Hz with AFC, reverse and
   TxID off, and adds a speaker loopback so you hear the test.
2. Open one of these in your browser and play it from the time shown:

   | Test | Video |
   |---|---|
   | FLDIGI (Contestia, then MFSK-32 by RSID) | <https://youtu.be/ChaHOpwouJw?t=997> |
   | FLMSG form | <https://youtu.be/8W7oApIU4O8?t=737> |
   | FLAMP file | <https://youtu.be/TFRbFlx2uZo?t=928> |

   While the test runs, every new audio stream from the browser is moved into FLDIGI (no
   menu to pick from), and AFC is switched back off if it gets turned on.
3. Watch FLDIGI decode. A received form opens in FLMSG; FLAMP shows the file in its
   *Receive* tab (select it and click *Save*, or let FLAMP save it).
4. Press Enter in the test window (or close it). The browser goes back to your speakers,
   its saved routing is cleared so the next video plays normally, the station is stopped,
   and files received in the last hour are listed.

Don't click in the waterfall during the test (a middle-click toggles AFC, a left-click
moves the carrier). If the squelch hides weak text, lower it.

## SDRangel instead of a browser

[SDRangel](https://www.sdrangel.org/) can listen to a KiwiSDR directly, with better
filters and AGC than a browser tab. This project doesn't install it; if you have it, the
installer adds start/stop shortcuts for each station:

| Command (and icon) | Does |
|---|---|
| `sdrangel-js8-start` / `sdrangel-js8-stop` | JS8Call + CommStat fed by SDRangel |
| `sdrangel-fldigi-start` / `sdrangel-fldigi-stop` | FLDIGI + FLMSG + FLAMP fed by SDRangel |

**Once, before the first use:** open SDRangel, add a KiwiSDR receiver (the *+* / *Add Rx
device* button, then *KiwiSDR*), type a server address as `host:8073` and tune it. SDRangel
remembers it. Find servers on the map at <http://rx.linkfanel.net> or <https://kiwisdr.com>;
use a server's own `host:8073` address - in testing, `*.proxy.kiwisdr.com` addresses gave
SDRangel an error.

**What start does, in order:**

1. Starts the station (`websdr-js8-start --no-route` or `websdr-fldigi-start --no-route`),
   which creates its virtual audio device.
2. Starts SDRangel. This has to come second: SDRangel lists audio devices only when it
   starts, so it can't use a device created after it opened.
3. Over SDRangel's REST API (127.0.0.1:8091) it points the SSB demodulator's audio at the
   station's device - adding a demodulator (USB, 300-3000 Hz, AGC on, volume 0.15) if
   there isn't one - and starts the KiwiSDR stream.
4. Adds a speaker loopback (`SDRangel-monitor` in the sound mixer) so you hear it too.
   Its volume doesn't affect the decoder. `SDRANGEL_LISTEN=0` turns it off;
   `SDRANGEL_LISTEN_GAIN=20dB` makes it quieter.

**One station at a time:** SDRangel's demodulator feeds one decoder, so starting one
station stops the other (and restarts SDRangel). **Stop** closes SDRangel the normal way,
so it saves its settings, before the station's device is removed.

**Levels:** AGC on with volume 0.15 gives about 38 dB on JS8Call's meter - right in the
middle. With AGC off at full volume it clips (87 dB). An existing demodulator keeps your
own volume and filter; only its audio output is changed.

**Tuning:** set the KiwiSDR device's frequency in SDRangel to the dial frequency (e.g.
7.078 MHz for JS8, 7.110 MHz for an AmRRON 40 m net) with the demodulator in USB at 0 Hz
offset. Neither decoder has rig control here, so if you change band in SDRangel, change
the dial frequency shown in JS8Call or FLDIGI to match.

If SDRangel was already open before you clicked start, the launcher says so and stops:
close SDRangel and click again.

## Setting FLDIGI up for an AmRRON net

AmRRON's frequencies, modes and net schedule come from its **Communications SOI** and the
**AIB White Paper**, which members get from AmRRON. The SOI may only be shared with its
author's permission, so this project doesn't include it. Here is how to put your copy's
settings into FLDIGI. Do it with FLDIGI **closed** (it rewrites its files when it exits),
in `~/.fldigi-websdr` for this station and in `~/.fldigi` for your radio FLDIGI.

- **Frequency list** (`frequencies2.txt`, FLDIGI's *Open List*): one line per entry,

  ```
  rfcarrier rig_mode carrier mode_name usage
  7110000 USB 900 Cont-4/250 Check-in
  ```

  where `rfcarrier` is the dial frequency in Hz and `carrier` is the audio offset on the
  waterfall. `mode_name` must be FLDIGI's short mode name exactly (`Cont-4/250`, `MFSK32`,
  `MFSK64`, `BPSK31`, `MT63-2KL`, `FSQ`, ...). FLDIGI silently turns a name it doesn't know
  into BPSK31. Back up the file first.
- **Waterfall position:** use the offset your SOI gives. Untick *Configure > Modems >
  Start new modems at sweet spot*, or FLDIGI moves every new mode to its own default.
- **AFC off** (the *AFC* button, saved at exit), especially for MFSK-32 traffic.
- **RxID on, TxID off** for listening. The station switches TxID off at every start.
- **FLMSG:** the SOI's custom forms go in `~/.nbems-websdr/CUSTOM` (copied from
  `~/.nbems/CUSTOM` at first start).
