# Edge E10 — Hotel-only request, no handling anchor

> ⚠️ Fictional email. Real ICAO (LEMD). A known operator (Solaris, registry `default_services` =
> handling only) asks for a **crew hotel with no handling request and no live trip thread**.
> Every hotel hard-field is present — the block is not missing detail, it is the missing **anchor**:
> there is no operation to attach the service to. Expected outcome: **ESCALATE** `NO_ANCHOR_SERVICE`.

```
From:    Solaris Jet Group Ops <ops@solarisjet.example>
To:      info@apextrip.example
Date:    Wed, 10 Jun 2026 16:20 +0200
Subject: Crew hotel Madrid (LEMD) — 21–23 JUN — 2 rooms

Hi,

Could you book a crew hotel near Barajas for us? Two of our crew are positioning
into Madrid commercially.

  - 2 rooms, 2 guests (Capt. R. Ostrander, FO L. Meirelles)
  - Check-in 21 JUN, check-out 23 JUN
  - 4–5 star, close to the airport

No movement with you on this one — just the rooms.

Thanks,
Solaris Jet Group — Ops
```
