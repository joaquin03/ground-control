# Sample Inbound 07 — Multi-leg trip, handling at two airports

> ⚠️ Fictional email. Real ICAOs (LFPB, EGGW; KMIA/LEMD as origin/destination). One reference,
> two handling stations → two provider lookups, two drafts. Expected outcome: **HANDLE**.

```
From:    Solaris Ops <ops@solarisjet.example>
To:      info@apextrip.example
Date:    Tue, 09 Jun 2026 12:25 +0100
Subject: M-SJGX | LFPB + EGGW | HANDLING — 2 STOPS | 18–20 JUN

Hi team,

Please arrange handling for a two-stop trip:

  Operator:  Solaris Jet Group (Private, Part 91)
  Aircraft:  Falcon 8X, reg M-SJGX, callsign SJG12
  POB:       4 PAX / 2 CREW

  Leg 1 — PARIS:   arrive LFPB 18 JUN 1000Z (from KMIA), depart LFPB 20 JUN 0900Z
                   → handling for the Paris stop, plus crew ground transport on
                     arrival (FBO → city hotel, 2 crew).
  Leg 2 — LONDON:  arrive EGGW 20 JUN 0945Z (from LFPB)
                   → handling for the London arrival.

One trip, please keep it under a single reference. Card on file.

Thanks,
Priya — Solaris Ops
```
