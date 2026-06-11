# Sample Inbound 12 — EGGW arrival, handling + catering (no catering provider on file)

> ⚠️ Fictional email. Real ICAO (EGGW). EGGW has a `handling` and a `ground_transport` provider in
> the database but **no `catering` row**. Expected outcome: **HANDLE handling; FLAG catering** as
> no-provider-on-file. Tests the lookup-miss path using only known airports/services.

```
From:    Solaris Ops <ops@solarisjet.example>
To:      info@apextrip.example
Date:    Tue, 09 Jun 2026 11:05 +0100
Subject: M-SJGZ | EGGW | ARRIVAL 22 JUN — HANDLING + CATERING

Hi team,

London Luton arrival:

  Operator:  Solaris Jet Group (Private, Part 91)
  Aircraft:  Falcon 8X, M-SJGZ, callsign SJG20
  Arrival:   EGGW 22 JUN, ETA 0930Z, inbound from LEMD
  POB:       3 PAX / 2 CREW

Please arrange handling, and a light catering uplift for 3 pax on the turnaround.

Card on file.

Thanks,
Priya — Solaris Ops
```
