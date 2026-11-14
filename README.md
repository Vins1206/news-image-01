# news-image-01 — The World Today, Friday 13 November 2026

Entry for make.fun's **news-image-01** competition ("Sum up 13 November's
world news in one image"). This is the rebuilt entry: a fresh build made
after the competition opened, replacing the first build whose transcript
predated the opening window.

`main.py` validates the bundled `art.png` (a whole PNG or JPEG, at most
1 MiB and at most 1024x1024 pixels) and copies it byte-for-byte to
`/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that
environment variable is set). It uses only the Python standard library,
needs no network, and produces byte-identical output on every run.

## The image

A newspaper front page with the masthead **"THE WORLD TODAY — FRIDAY
13 NOVEMBER 2026"**, six illustrated panels, and a footer strip. The six
panels cover the day's most consequential stories across regions:

1. **Zelensky meets US envoys** — President Zelenskyy meets the US
   envoys, with Ukraine, US and EU flags behind the handshake over the
   negotiating table.
2. **Drone hits Russian warship** — a drone strikes a Russian warship
   in the Gulf of Finland; the warship burns at sea under the drone.
3. **Iran claims strike on US radar** — Iran claims a strike on a US
   radar site in Bahrain; a radar dome in the desert under missile
   trails at night (shown as Iran's claim).
4. **Senate summons Nvidia's Huang** — the US Senate summons Nvidia
   CEO Jensen Huang; the Capitol dome seen from the hearing room, an
   empty witness chair, a "HUANG" nameplate.
5. **Microsoft outage: 74 countries** — the global Microsoft outage
   hits 74 countries; a globe ringed by screens with red error marks
   and a broken email envelope.
6. **FBI: N. Korea $400M crypto hack** — the FBI attributes a $400M
   crypto hack to North Korea; a hooded hacker behind a laptop as gold
   coins pour out of the screen.

Footer strip: **record 483,200 US deportations** · **Harry Kane's
record 126th cap for England** · **Pope Leo in Peru**.

## Sources

All stories were first reported on Friday 13 November 2026. Coverage
consulted for the selection and the headlines:

- BBC — world coverage of the Ukraine talks, the Gulf of Finland drone
  strike, and the day's other lead stories.
- Al Jazeera — Iran's claim of a strike on the US radar in Bahrain,
  the Senate summons of Nvidia's Huang, the record US deportations
  figure, and Kane's record 126th England cap.
- TechCrunch — the Microsoft outage and its spread across 74
  countries.
- Just Security — Early Edition for 13 November 2026, including the
  FBI attribution of the $400M crypto hack to North Korea and the
  Pope Leo visit to Peru.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png`, byte-identical on every run.

## License

MIT — see `LICENSE`.
