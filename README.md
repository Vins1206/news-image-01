# news-image-01 — The World Today, Friday 13 November 2026

Entry for make.fun's **news-image-01** competition ("Sum up 13 November's
world news in one image"). `main.py` validates the bundled `art.png` (a whole
PNG or JPEG, at most 1 MiB and 1024x1024 pixels) and copies it byte-for-byte
to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).

## The image

A newspaper front page — masthead "THE WORLD TODAY / FRIDAY 13 NOVEMBER
2026" — with six illustrated panels and a footer strip, summing up the day's
most consequential stories across regions and fields:

1. **Zelensky meets US envoys** — President Zelenskyy met US envoys Witkoff
   and Kushner in Ireland after their Moscow talks; Europe is brought into
   the next round of Ukraine peace talks and work begins on the war's
   largest prisoner exchange.
2. **Drone hits Russian warship** — a Ukrainian drone struck the Russian
   Buyan-M corvette *Naro-Fominsk* in the Gulf of Finland, the first such
   strike in an open stretch of the Baltic; Finland's military detected it.
3. **Iran claims strike on US radar** — Iran's Revolutionary Guards said
   they destroyed a US early-warning radar in Bahrain, as tankers were hit
   in the Strait of Hormuz (reported as Iran's claim, unverified).
4. **Senate summons Nvidia's Huang** — the US Senate Banking Committee
   summoned former Nvidia CEO Jensen Huang (who resigned the day before)
   and Commerce Secretary Lutnick to testify.
5. **Microsoft outage: 74 countries** — a global Microsoft 365 outage took
   Outlook, Teams and Copilot down in at least 74 countries; Microsoft said
   it was not a cyberattack and worked through Friday to restore service.
6. **FBI: N. Korea $400M crypto hack** — the FBI attributes a $400M crypto
   theft worked through fake video calls to North Korean hackers, and the
   Justice Department won court approval to seize $1.2B from the Binance
   hack blamed on North Korea.

Footer: **record 483,200 US deportations in 2026** · **Harry Kane's record
126th England cap** (he scored the winner in a 2-1 Nations League win over
Croatia) · **Pope Leo meets abuse survivors in Peru**.

## Sources (all first reported 13 November 2026)

- BBC World / Al Jazeera, via the competition kit's story list:
  https://www.aljazeera.com/news/2026/11/13/nvidias-huang-lutnick-summoned-to-testify-to-us-senate
  https://www.bbc.co.uk/news/articles/ckn80j9jv3jxo
  https://www.bbc.co.uk/news/articles/cmn0d33zz34zo
  https://www.aljazeera.com/news/2026/11/13/iran-says-it-struck-us-radar-site-in-bahrain
  https://www.bbc.co.uk/news/articles/cqdj1ellpd70o
  https://www.aljazeera.com/news/2026/11/13/us-reports-record-number-of-deportations-and-arrests-in-2026
  https://www.aljazeera.com/sports/2026/11/13/harry-kane-england-appearance-record-126-croatia-nations-league-quarterfinals
- TechCrunch, "Microsoft's latest email outage turned into a full-blown
  global cloud crisis" (13 Nov 2026):
  https://techcrunch.com/2026/11/13/microsoft-latest-email-outage-turned-into-a-full-blown-global-cloud-crisis/
- Just Security, Early Edition: November 13, 2026:
  https://www.justsecurity.org/164357/early-edition-november-13-2026/

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png`, byte-identical on every run.

## License

MIT — see `LICENSE`.
