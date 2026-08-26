/**
 * FieldCommand — Server-Synced Clock  (clock.js)
 *
 * WHY THIS EXISTS
 * Every connected device (phone, tablet, laptop) has its own clock, and those
 * clocks disagree — a laptop at staging could be minutes off. If ICS forms and
 * logs auto-filled time from the device, the same incident would carry
 * conflicting timestamps. This helper makes every device read ONE clock: the
 * Pi server's (which, offline, is disciplined to GPS/UTC by chrony).
 *
 * HOW IT WORKS
 * On load it fetches /api/time from the server, measures the network round-trip,
 * and computes an offset between the server clock and this device's clock. From
 * then on, FC_TIME.date() returns a Date corrected by that offset — the server's
 * time, ticking smoothly on the device without hammering the server. It re-syncs
 * every few minutes and whenever the tab regains focus. If the server is
 * unreachable, it falls back to the device clock (offset 0) so nothing breaks.
 *
 * PUBLIC API
 *   FC_TIME.date()      → Date corrected to server time (use in place of new Date())
 *   FC_TIME.nowMs()     → server-corrected epoch milliseconds
 *   FC_TIME.iso()       → full ISO-8601 string, e.g. 2026-08-26T14:03:00.000Z
 *   FC_TIME.isoMinute() → "YYYY-MM-DDTHH:MM" (UTC) — for datetime-local defaults
 *   FC_TIME.isoDate()   → "YYYY-MM-DD" (UTC)
 *   FC_TIME.timeHHMM()  → "HH:MM" (device-local time-of-day)
 *   FC_TIME.stamp()     → localized date+time string (for printed footers)
 *   FC_TIME.isSynced()  → true once a successful sync has happened
 *   FC_TIME.offsetMs()  → current server-minus-device offset in ms
 *   FC_TIME.sync()      → force a resync now (returns Promise<boolean>)
 *   FC_TIME.onSync(fn)  → callback fired after each successful sync
 */
const FC_TIME = (() => {
    const API          = '/svc/5050';
    const RESYNC_MS    = 5 * 60 * 1000;   // background resync every 5 minutes
    const TIMEOUT_MS   = 3000;

    let _offset  = 0;      // serverEpochMs - deviceEpochMs
    let _synced  = false;
    let _lastTry = 0;
    let _cbs     = [];

    async function sync() {
        _lastTry = Date.now();
        try {
            const t0 = Date.now();
            const r  = await fetch(`${API}/api/time`,
                { cache: 'no-store', signal: AbortSignal.timeout(TIMEOUT_MS) });
            const t1 = Date.now();
            if (!r.ok) return false;
            const j = await r.json();
            if (!j || !j.epoch_ms) return false;
            // Assume the server sampled its clock at the midpoint of the round-trip.
            const rtt = t1 - t0;
            _offset = j.epoch_ms + Math.round(rtt / 2) - t1;
            _synced = true;
            _cbs.forEach(fn => { try { fn({ offset: _offset }); } catch (e) {} });
            return true;
        } catch (e) {
            return false;   // offline / unreachable — keep using the device clock
        }
    }

    function nowMs()     { return Date.now() + _offset; }
    function date()      { return new Date(nowMs()); }
    function iso()       { return date().toISOString(); }
    function isoMinute() { return date().toISOString().slice(0, 16); }
    function isoDate()   { return date().toISOString().slice(0, 10); }
    function timeHHMM()  { return date().toTimeString().slice(0, 5); }
    function stamp()     { return date().toLocaleString(); }

    // Initial sync + periodic resync + resync on tab focus.
    function init() {
        sync();
        setInterval(() => sync(), RESYNC_MS);
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && Date.now() - _lastTry > 30000) sync();
        });
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    return {
        date, nowMs, iso, isoMinute, isoDate, timeHHMM, stamp, sync,
        isSynced:  () => _synced,
        offsetMs:  () => _offset,
        onSync:    fn => { _cbs.push(fn); },
    };
})();
