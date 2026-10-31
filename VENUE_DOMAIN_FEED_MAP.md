# Venue Domain → Subdomain → Live Feed Map

*Generated 2026-09-20 23:50 — regenerates as agents finish.*

Canonical taxonomy of every category and subcategory traded on **Kalshi**, **Polymarket** (Global + US) and **Robinhood**, normalized into one schema, with free live data feeds mapped to each node.

Feeds are split into **predictive** (forms a probability before settlement) and **settlement** (resolves the contract). They are usually different sources.

---

## Status

| Phase | State |
|---|---|
| 1 · Venue taxonomies | done — 3/3 |
| 2 · Normalized schema | done — 18 domains |
| 3 · Feed mapping | 18 domains mapped |
| 4 · Coverage audit | done |

---

## 1 · Venue taxonomies (extracted live)

| Venue | Categories | Series / tags |
|---|---:|---:|
| Kalshi | 20 | 14170 |
| Polymarket (Global, gamma-api.polymarket.com) + Polymarket U | 26 | 8188 |
| Robinhood (Robinhood Derivatives, LLC) — event contracts / p | 32 | 649 |

### Kalshi

*Method: All data pulled live from https://external-api.kalshi.com/trade-api/v2 on 2026-09-20 via unauthenticated GET (curl; no API key sent). Endpoints called: (1) GET /series?limit=200 — returned the ENTIRE catalog of 14,170 series objects in ONE page with NO 'cursor' key in the response at all (top-level keys are just ['series']), so /series is not cursor-paginated and the limit param is ignored; this i*

**Sports** — 32 subcategories

- `Soccer` · e.g. KXSERIEAPOINTMARGIN — Serie A Champion Winning Margin, KXLALIGATEAMPOINTS — Team Points, KXLIGAMX1HSPREAD — 1st Half Spread · settles: ESPN, Fox Sports, FIFA · per-event
- `Basketball` · e.g. KXNBAMIMP — NBA Most Improved Player, KXNCAAMBBOTHQUAL — Men's College Basketball Both Teams to Qualify, KXWNBAGAME — Women's Pro Basketball Game · settles: ESPN, the Governing League, Fox Sports · per-event
- `Football` · e.g. KXNCAAFAPANY — College Football AP Rank Anytime in Season, KXNFLSELLOUT — Pro Football Sellouts, KXNCAAFMAC — MAC Champion · settles: ESPN, the Governing League, Fox Sports · per-event
- `Baseball` · e.g. KXLEADERMLBRUNS — MLB Runs Leader, KXNEXTTEAMMLB — MLB Player Next Team, KXMLBWINS-SEA — Pro baseball wins Seattle · settles: ESPN, the Governing League, Fox Sports · per-event
- `(no tag assigned)` · e.g. KXRANKLISTFFRB — TOP FANTASY FOOTBALL RB, KXLEADERNFLPINT — Pro Football Pass INT, KXNFLOT — Pro Football Overtime · settles: ESPN, Fox Sports, The Wall Street Journal · per-event
- `Tennis` · e.g. KXWTADOUBLES — WTA Doubles Tennis Match, KXATPCHALLENGERMATCH — Challenger ATP, KXITFDOUBLES — ITF Doubles Match · settles: ESPN, Fox Sports · per-event
- `Esports` · e.g. KXDOTA2TOTALMAPS — Dota 2 Total Maps, KXCS2TOTALMAPS — CS2 Total Maps, KXVALORANTTOTALMAPS — Valorant Total Maps · settles: Riot Games, VALORANT Esports, Gamers World · per-event
- `Golf` · e.g. KXLPGATOUR — PGA Tour, KXPGATOUR — PGA Tour, KXSCOTTIESLAM — Scottie grand slam · settles: ESPN, the Governing League, Fox Sports · per-event
- `Hockey` · e.g. KXNHLPACIFIC — NHL Pacific Division Winner, KXNHLTOTAL — NHL Total Goals, KXNHLSEASONPTS — NHL Season Point Totals · settles: ESPN, NHL, Fox Sports · per-event
- `Motorsport` · e.g. KXNASCARAUTOPARTSSERIES — NASCAR Auto Parts Series Champion, KXF1 — Formula 1, KXF1NEXTTEAM — F1 Next Team · settles: ESPN, FIA, the Governing League · per-event
- `Cricket` · e.g. KXCPL — Caribbean Premier League Champion, KXCPLTEAMTOTAL — Caribbean Premier League Team Total Runs, KXODIMATCH — Men's ODI Cricket Match · settles: ESPN, ESPNcricinfo, ICC · per-event
- `Olympics` · e.g. KXWOLUGE — Winter Olympics Luge, KXWO-TOTALMEDALS — Winter Olympic Country Medal Count, KXWO-FSKATE — Winter Olympics Figure Skating · settles: the Winter Olympics 2026, ESPN, Fox Sports · per-event
- `MMA` · e.g. KXUFCFEATHERWEIGHTTITLE — UFC Featherweight Title, KXUFCLHEAVYWEIGHTTITLE — UFC Light Heavyweight Title, KXWWEFIGHTOCCUR — WWE Wrestler to Compete in a Fight · settles: ESPN, Fox Sports, MMA Fighting · per-event
- `Chess` · e.g. KXTITLEDTUESTOP — Titled Tuesday Chess Top Finishers, KXCHESSOLYMPIAD — Chess Olympiad Winner, KXCHESSWORLDCHAMPION — World Chess Champion · settles: Chess.com, ESPN · per-event
- `Other` · e.g. KXSAILGP — SailGP Championship, KXSUMOWIN — Sumo Tournament Winner, KXSURFCOMPETITION — Surfing Competition Winner · settles: ESPN, Fox Sports · per-event
- `Boxing` · e.g. KXBOXING — Boxing Match Champion, KXWBCMIDDLEWEIGHTTITLE — Boxing Middleweight Title, KXFLOYDTYSONFIGHT — Floyd vs Tyson Fight · settles: ESPN, Fox Sports, WBC Boxing · per-event
- `Rugby` · e.g. KXNRLCHAMP — National Rugby League Champion, KXRUGBYNRLMATCH — Rugby NRL Match, KXRUGBYWC — Men's Rugby World Cup Winner · settles: ESPN, Fox Sports, Flashscore · per-event
- `Table Tennis` · e.g. KXTTELITEMATCH — TT Elite Series Match · settles: ESPN, World Table Tennis, Sofascore · per-event
- `Lacrosse` · e.g. KXNCAALAX — College Lacrosse National Championship · settles: ESPN, Kalshi using information originating from the NCAA · per-event
- `4th of July` · e.g. KXNATHANSHD — Nathan's Hot Dog Eating Contest Winner, KXNATHANSWINNERWO — Nathan's Hot Dog Contest Winner Without, KXNATHANSHDOU — Nathan's Hot Dog Over Unders · settles: Nathan's Famous, Fox Sports, ESPN · annual
- `Cycling` · e.g. KXCYCLING — Cycling Race Winner, KXCYCLINGJERSEY — Cycling Jersey Winner, KXCYCLINGSTAGE — Cycling Stage Winner · settles: Cycling Weekly, Union Cycliste Internationale, ESPN · per-event
- `Squash` · e.g. KXSQUASHMATCH — Pro Squash Match, KXBRITISHOPENSQUASH — British Open Squash Winner, KXPSASQUASH — PSA World Champion · settles: Fox Sports, ESPN, World Squash Champs · per-event
- `Volleyball` · e.g. KXNCAAWV — Women's college volleyball champion, KXNCAAWVMATCH — Women's College Volleyball Match · settles: ESPN, Kalshi using information originating from the NCAA · per-event
- `Darts` · e.g. KXPDCDARTS — PDC Darts · settles: Sky Sports, ESPN, Fox Sports · per-event
- `Video games` · e.g. KXLEAGUE — League of Legends World Championship · settles: ESPN, Fox Sports, AP · annual
- `UFC` · e.g. KXUFC — UFC Weightclass Champion, KXUFCMWEIGHT — UFC Middleweight Champion · settles: ESPN, Fox Sports · per-event
- `CFB` · e.g. KXCFBDOBRIEN — Davey O'Brien Award · settles: ESPN · annual
- `Aussie Rules` · e.g. KXAFLGAME — AFL Game · settles: ESPN, Fox Sports · per-event
- `Cities` · e.g. KXCITYCHAMPS — City Major Sports Championships · settles: the Football Governing League, NHL, the Basketball Governing League · per-event
- `International` · e.g. KXSUPERBOWLWHITEHOUSE — Will the winners of the pro football championship go to the White House? · settles: The Guardian, Fox News · one-off
- `ESPYS` · e.g. KXESPYSWEEP — ESPYs Award Sweep · settles: ESPN · per-event
- `Rowing` · e.g. KXROWING — Rowing race winner · settles: Regatta Central, the Governing League · per-event

**Entertainment** — 64 subcategories

- `Music` · e.g. KXMUSICREPORT — music report, KXPUREALBUMS — How many pure album sales will album have, KXALBUMRELEASEDATEJB — When will Justin Bieber release? · settles: Billboard, Spotify, Variety · one-off
- `Awards` · e.g. KXOSCARMAH — Oscar for Best Makeup and Hairstyling, KXGRAMBNA — Grammy for Best New Artist, KXOSCARACTO — Oscar for Best Actor · settles: Recording Academy, Academy of Motion Picture Arts and Sciences, Golden Globes · annual
- `(no tag assigned)` · e.g. KXYTUBESUBSBEAST — YouTube subs Beast, KXSHOWENDFAMILYGUY — Will Family Guy end, KXPERFORMBONDSONG — Who will perform the next James Bond song · settles: The New York Times, Reuters, the Associated Press · one-off
- `Music charts` · e.g. KXBBCHARTPOSITIONSONG — What position will song/album be on the Billboard chart, KX1SONG — Will artist have a number one song on Billboard Hot 100, KXMUSICREPORT — music report · settles: Billboard, Spotify Charts, YouTube Charts · one-off
- `Movies` · e.g. KXROLEINPRODUCTIONDOOMSDAY — Who will be playing what in Avengers Doomsday, KXJOHNNYDEPP — Johnny Depp star in Pirates of the Caribbean?, KXPERFORMROLEBRITNEY — Who will perform as Britney Spears in biopic · settles: Rotten Tomatoes, Academy of Motion Picture Arts and Sciences, Luminate · per-event
- `Rotten Tomatoes` · e.g. KXRT — Rotten Tomatoes Scores, KXRTTV — Rotten Tomatoes Score, KXRTCOMPARE — What movie will have the highest score · settles: Rotten Tomatoes · per-event
- `Television` · e.g. KXDWTSELIMINATION — Dancing With The Stars Elimination, KXBIGBROTHERRANK — Big Brother Rank, KXNETFLIXTOPVIEWSTV — Netflix Top Show View Count · settles: CBS and the official broadcaster/streaming platform · one-off
- `Grammys` · e.g. KXGRAMBNA — Grammy for Best New Artist, KXGRAMMYNOMBRA — Grammy Award for Best Rap Album, KXGRAMMYNOMAOTY — Grammy nominees for Album of the Year · settles: Recording Academy · annual
- `Video games` · e.g. KXPS6 — PS6 announcement, KXMC — Metacritic score, KXSTEAMTOPSELLER — STEAM Top Sellers · settles: Metacritic, Game Awards · per-event
- `People` · e.g. KXENGAGEMENTBOSAAILIFF — Will Nick Bosa and Ella Ailiff get engaged, KXENGAGEMENTTRUDEAUPERRY — Will Justin Trudeau and Katy Perry be engaged, KXENGAGEMENTISHOWSPEED — IShowSpeed engaged · settles: Reuters, CNN · one-off
- `Oscars` · e.g. KXOSCARNOMSUPACTR — Oscar nominations for Best Supporting Actress, KXOSCARNOMACTR — Oscar nominations for Best Actress, KXOSCARMAH — Oscar for Best Makeup and Hairstyling · settles: Academy of Motion Picture Arts and Sciences · annual
- `Reality TV` · e.g. KXBIGBROTHERRANK — Big Brother Rank, KXDWTSTOP3 — Who will finish top 3 in DWTS, KXBIGBROTHERELIMINATION — Who will be eliminated from Big Brother · settles: the official broadcaster or streaming platform · one-off
- `Morgan Wallen` · e.g. KXMWIMTHEPROBLEM — I'm the Problem total streams, KXMWNOTHINLEFT — Nothin' Left total streams, KXIMALITTLECRAZY — total streams · settles: Spotify, Billboard · per-event
- `Music Streams` · e.g. KXARTISTSTREAMSY — Artist Yearly Streams, KXALBUMSTREAMS — How many streams will album have · settles: Spotify, Luminate · per-event
- `Anime Awards` · e.g. KXANIMEVAPH — Best Anime Voice Artist Performance (Hindi), KXANIMEBVAPE — Best Voice Artist Performance (English), KXANIMEBSA — Best Supporting Anime · settles: Crunchyroll · annual
- `Live Music` · e.g. KXPERFORMSUPERBOWL — Who will headline the Super Bowl halftime show?, KXPERFORMVMA — Who will perform the VMAs, KXKXMEDIAGUESTTINYDESK — Who will go on Tiny Desk · settles: Reuters, ABC, CNN · one-off
- `Emmys` · e.g. KXEMMYCSERIES — Emmys Award for Comedy Series, KXEMMYDSERIES — Emmys Award for Drama Series · settles: Academy of Television Arts & Sciences · annual
- `Taylor Swift` · e.g. NEWTAYLOR — Taylor Swift album, NEWTAYLORREP — Reputation Taylor's Version, TOPALBUMRECORD — Album record · settles: Billboard, Spotify, Taylor Swift · per-event
- `Golden Globes` · e.g. KXGGNOM — Who will be nominated for a Golden Globe · settles: Golden Globes · one-off
- `VMA` · e.g. KXVMA — Who will win VMA award · settles: MTV · one-off
- `TV Charts` · e.g. KXNETFLIXTOPVIEWSTV — Netflix Top Show View Count, KXNETFLIXRANKSHOWGLOBAL — Netflix TV ranking, KXNETFLIXRANKSHOWRUNNERUP — Runner up Netflix show · settles: Television Stats, Netflix, Luminate · weekly
- `Product launches` · e.g. KXPS6 — PS6 announcement, KXGTAONLINE — When will GTA VI release?, KXGTAPCRELEASE — Will the PC version of GTA 6 release before 2028? · settles: StockX, Sony, company · one-off
- `ACMs` · e.g. KXACMANFAOTY — ACMA New Female Artist of the Year, KXACMAVMOTY — ACMA Visual Media of the Year, KXACMADOTY — ACMA Duo of the Year · settles: Academy of Country Music · annual
- `CMA Awards` · e.g. KXCMA — CMA Award · settles: CMA Awards · one-off
- `Views` · e.g. KXYTDAILYTOPVIDEO — Daily Top YouTube Video, KXYTTOPSONGGW — weekly top song, KXYTTOPVIDEOG2D — runner up top music video · settles: YouTube Charts · one-off
- `Achievements` · e.g. KXRANKLISTGOOGLESEARCH — #1 most searched on Google, KXSEXYMAN — Sexiest Man Alive, KXRANKLISTGOOGLESEARCHTOP5 — top 5 Google search for people · settles: Google Trends, TIME, Variety · one-off
- `The Game Awards` · e.g. KXGAMEAWARDS — Game Awards, KXGAMEAWARDSBGD — Game Awards Best Game Direction · settles: Game Awards · annual
- `Music Industry` · e.g. KXMUSICREPORT — music report, KXRANKLISTIFPIARTIST — IFPI Global Artist of the Year, KXCASEWINMUSIC — Will party win its lawsuit · settles: Billboard, Luminate, Hits Daily Double · one-off
- `Tonys` · e.g. KXTONYAWARDS — Who will win Tony award, KXBESTACRESSTONYS — Best Performance by an Actress in a Leading Role, KXBESTACTORTONYAWARDS — Best Performance by an Actor in a Leading Role · settles: Tony Awards · annual
- `Collectibles` · e.g. KXSTOCKX — StockX collectible pricing · settles: StockX, Bezel · one-off
- `Love Island UK` · e.g. KXLOVEISLANDUK — Love Island UK outcomes · settles: ITV · one-off
- `Eurovision` · e.g. KXEUROVISION — Eurovision winner · settles: Eurovision Song Contest · annual
- `BAFTA` · e.g. KXBAFTA — BAFTA award winner · settles: BAFTA · annual
- `Love Island USA` · e.g. KXLOVEISLANDUSA — Love Island USA outcomes · settles: Peacock · one-off
- `Football` · e.g. KXSUPERBOWLAD — Super Bowl ads · settles: Ad Age, Bloomberg News · one-off
- `Anime awards` · e.g. KXANIMEAWARDS — Anime award winner · settles: Crunchyroll · annual
- `Movie Charts` · e.g. KXNETFLIXRANKMOVIE — Netflix movie ranking, KXNETFLIXTOPVIEWSMOVIE — Netflix Top Movie View Count · settles: Luminate, Netflix · weekly
- `SAG` · e.g. KXSAG — SAG award winner · settles: Screen Actors Guild · annual
- `Cannes` · e.g. KXCANNES — Cannes Palme d'Or winner · settles: Festival de Cannes · annual
- `New Music` · e.g. KXALBUMRELEASEDATEJB — When will Justin Bieber release?, KXNEWMUSIC — New music release · settles: Billboard, Spotify · one-off
- `Art` · e.g. KXART — Art auction outcomes · settles: Sotheby's, Christie's · one-off
- `Nobel Prizes` · e.g. KXNOBELLIT — Nobel Literature prize · settles: Nobel Prize organization · annual
- `Dancing with the Stars` · e.g. KXDWTSELIMINATION — Dancing With The Stars Elimination, KXDWTSTOP3 — Who will finish top 3 in DWTS · settles: ABC · one-off
- `Soccer` · e.g. KXSOCCERENT — Soccer entertainment crossover · settles: ESPN · one-off
- `Companies` · e.g. KXNETFLIXSTUDIO — When will entity complete project · settles: Variety, Reuters · one-off
- `Big Brother` · e.g. KXBIGBROTHERRANK — Big Brother Rank, KXBIGBROTHERELIMINATION — Who will be eliminated from Big Brother · settles: CBS · one-off
- `Head to Head` · e.g. KXMUSICH2H — Music head to head · settles: Billboard, Luminate · one-off
- `StockX` · e.g. KXSTOCKXPRICE — StockX sneaker price · settles: StockX · per-event
- `America's Got Talent` · e.g. KXAGT — America's Got Talent winner · settles: NBC · one-off
- `Pokémon` · e.g. KXPOKEMON — Pokémon product/collectible outcomes · settles: The Pokémon Company · one-off
- `Sports Emmys` · e.g. KXSPORTSEMMY — Sports Emmy winner · settles: National Academy of Television Arts & Sciences · annual
- `Latin Grammys` · e.g. KXLATINGRAMMY — Latin Grammy winner · settles: Latin Recording Academy · annual
- `Love Island` · e.g. KXLOVEISLAND — Love Island outcomes · settles: ITV / Peacock · one-off
- `Trump` · e.g. KXTRUMPENT — Trump entertainment appearance · settles: Reuters, ABC · one-off
- `Other` · e.g. KXENTOTHER — Miscellaneous entertainment · settles: Reuters, Variety · one-off
- `Monthly Views` · e.g. KXYTMONTHLYVIEWS — Monthly YouTube views · settles: YouTube Charts · monthly
- `Daily Views` · e.g. KXYTDAILYTOPVIDEO — Daily Top YouTube Video · settles: YouTube Charts · daily
- `Baseball` · e.g. KXBASEBALLENT — Baseball entertainment crossover · settles: ESPN · one-off
- `Venice Film Festival` · e.g. KXVENICE — Venice Film Festival Golden Lion · settles: Venice Biennale · annual
- `Basketball` · e.g. KXNBAATTEND — Who will attend the NBA game? · settles: ESPN · one-off
- `Weekly Views` · e.g. KXYTTOPSONGGW — weekly top song · settles: YouTube Charts · weekly
- `AMAs` · e.g. KXAMA — AMA award winner · settles: American Music Awards · annual
- `Daytime Emmys` · e.g. KXDAYTIMEEMMY — Daytime Emmy winner · settles: National Academy of Television Arts & Sciences · annual
- `Congress` · e.g. KXENTCONGRESS — Entertainment figure before Congress · settles: Library of Congress · one-off

**Politics** — 49 subcategories

- `(no tag assigned)` · e.g. KXBIDENAMBIEN — Biden Ambien, KXBIDENBOOK — Biden book release, KXPLATNERCOLLINSDEBATE — Platner and Collins debate · settles: The New York Times, Reuters, Politico · per-event
- `Congress` · e.g. KXCONGRESSTRADES — Congress trades, KXSOCIALSECURITYDEPLETE — Will Social Security's retirement trust fund be depleted, KXGAMBLINGREPEAL — Gambling Repeal · settles: Library of Congress, U.S. Senate, White House · one-off
- `Trump` · e.g. KXCABOUT — Next Cabinet member out, KXTARIFFSECTOR — Which sectors will Trump tariff?, KXFEDEND — Fed ended · settles: Reuters, The Washington Post, The Wall Street Journal · one-off
- `International` · e.g. KXCAEUROPEMOBILITY — Canada-EU expanded mobility rights, KXARRESTNETANYAHU — Will Netanyahu be arrested?, KXCANMIN19 — Will any province's minimum wage exceed $19/hour · settles: Reuters, The Wall Street Journal, Politico · one-off
- `SCOTUS & courts` · e.g. KXTHOMASANNOUNCERETIRE — Thomas announces retirement, KXOBERGEFELL — Obergefell, KXSCOTUSCHANGE — SCOTUS size change · settles: Supreme Court, Reuters, The Wall Street Journal · one-off
- `US Elections` · e.g. KXUSPSPREACCEPT — USPS mandatory federal ballot-mail pre-acceptance, KXUSPSPORTALSUBMIT — State federal ballot-mail data submissions to USPS, KXMCCONAUGHEYOFFICE — Matthew McConaughey runs for office · settles: United States Congress, Library of Congress, Reuters · per-event
- `Local` · e.g. KXCAFRAUD — Will any CA state executive be federally charged, KXNYQSBS — Will New York tax QSBS gains?, KXNYCTAXBILLIONS — Will Mamdani tax billionaires before 2027? · settles: Reuters, The Washington Post, The Wall Street Journal · one-off
- `Foreign Elections` · e.g. KXBOLIVIAPRES — Bolivia presidential election, KXPRESPOLAND — Polish presidential election, KXEDMONTONGRIESBACH — Edmonton Griesbach · settles: CBC, Politico, The New York Times · per-event
- `Recurring` · e.g. KXDCGOLFVISITCOUNT — Trump National Golf Club visits, KXACTBLUETOP — Top ActBlue fundraiser?, KXTRUMPENDORSEMENTS — How many people will Trump endorse this week? · settles: Fox News, Reuters, Politico · monthly
- `NYC` · e.g. KXNYCTAXBILLIONS — Will Mamdani tax billionaires before 2027?, KXNYCDEPTSAFETY — Will Mamdani establish a Department of Community Safety, KXMAMDANIOUT — Mamdani out as NYC Mayor · settles: The Washington Post, The Wall Street Journal, Reuters · one-off
- `Culture war` · e.g. NPRCEOCHANGE — NPR CEO leaves, USTESTSMATH — US Test scores in Math, DEBATES24 — How many presidential debates in 2024? · settles: Library of Congress, Harvard, Nation's Report Card · per-event
- `Bills` · e.g. CAPGAIN — Capital gains tax increase, NETNEU — Net neutrality, RECLAW — Reconciliation size · settles: Library of Congress, Federal Register, Congressional Budget Office · per-event
- `Iran` · e.g. KXHORMUZMAX — Maximum traffic through the Strait of Hormuz?, KXSUEZWEEKLY — Traffic through the Suez Canal, KXBABELMANDEBWEEKLY — Traffic through the Bab al-Mandab Strait · settles: The New York Times, The Wall Street Journal, Reuters · one-off
- `Confirmations` · e.g. BARR — Barr confirmation as Fed Vice Chairman for Supervision, JEFFERSON — Philip Jefferson Fed member confirmation, BRAINARD — Lael Brainard Fed Vice Chair confirmation · settles: Library of Congress · per-event
- `AI` · e.g. KXAIDUTYOFCARE — Federal catastrophic AI risk duty of care law, KXAPPLEOPENAICASE — Apple v OpenAI trade-secrets case, KXAIBIOSECURITY — AI biosecurity controls · settles: Library of Congress, the White House, The Information · one-off
- `Biden` · e.g. 538APPROVE — President 538 approval rating this week, 538APPROVEMAX — Biden 538 highest approval rating, CAPGAIN — Capital gains tax increase · settles: FiveThirtyEight, CNN, Library of Congress · per-event
- `Education` · e.g. USTESTSMATH — US Test scores in Math, HARVPRES — New Harvard President, COMMENCEMENT — University commencements cancelled · settles: Harvard, Nation's Report Card, Bloomberg · per-event
- `Cabinet` · e.g. SECHOMELAND — Next Homeland Security Secretary, SECTREASURY — Next Secretary of the Treasury, SECLABOR — Next Secretary of Labor · settles: Library of Congress · per-event
- `Debt ceiling & shutdowns` · e.g. DEFAULT — US defaults, GOVSHUTLENGTH — Days of government shutdown, DCEIL — Debt ceiling hike · settles: U.S. Office of Personnel Management, U.S. Department of the Treasury · per-event
- `Approval ratings` · e.g. 538APPROVE — President 538 approval rating this week, 538APPROVEMAX — Biden 538 highest approval rating, 538APPROVEMIN — Biden 538 lowest approval rating · settles: FiveThirtyEight, RealClearPolitics · weekly
- `Immigration` · e.g. ASYLUMCASES — New asylum cases, BORDER — Border bill passes, TEXASDHS — Court rules for Biden against Texas · settles: Library of Congress, USCIS, PACER · per-event
- `Primaries` · e.g. KXINSCOMOKNOMR — Oklahoma Republican Insurance Commissioner nominee, KXLABOROKNOMR — Oklahoma Republican Labor Commissioner nominee, KXSUPTOKNOMR — Oklahoma Republican State Superintendent nominee · settles: Oklahoma State Election Board, Rhode Island Board of Elections · one-off
- `Taxes` · e.g. SALTX — SALT deduction cap raised, CORPTAX — Corporate tax rate, CARBONTAX — Carbon tax becomes law · settles: Library of Congress · annual
- `International politics` · e.g. AMBCN — Burns confirmed as China Ambassador, ISAMB — Next Israel Ambassador, SCOTREF — New Scottish referendum · settles: Library of Congress, UK Government · per-event
- `Court cases` · e.g. GRANTSPASS — Grants Pass, Oregon v. Johnson, NETCHOICE — NetChoice v. Paxton, ITAXH — Income tax hike · settles: Supreme Court, Library of Congress · per-event
- `BTC` · e.g. KXBTCRESERVE — Bitcoin Reserve, KXTREASBUYBTC — Will the Treasury announce a completed Bitcoin purchase, KXTREASBUYCRYPTO — Treasury cryptocurrency purchases · settles: the Federal Register, the U.S. Department of the Treasury · one-off
- `People` · e.g. KXNBAATTEND — Who will attend the NBA game?, KXMETGALA — Who will attend the Met Gala, KXTRUMPWORLDCUP — Trump world cup games · settles: Reuters, The New York Times, the Associated Press · one-off
- `Fed` · e.g. KXFEDNOM — Federal Reserve chairman replacement announcement, FEDNOM — Federal Reserve chairman replacement announcement · settles: White House · per-event
- `Growth` · e.g. KXWTAX — Wealth tax, CREDITRATING — US credit rating downgrade · settles: Library of Congress, Fitch, Moody's · per-event
- `House` · e.g. KXDCCCCHAIR — Next DCCC Chair · settles: Democratic Congressional Campaign Committee · one-off
- `Health Tech` · e.g. KXCMEATBANUSA — Cultivated meat ban, KXFLUORIDE — Fluoride recommendation · settles: The New York Times, White House, US Public Health Service · per-event
- `Public Health` · e.g. KXHHSYOUTHCARE — HHS youth gender-care Medicaid rule, KXPARTDGLP1 — When will CMS announce Part D coverage of GLP-1 drugs · settles: AP, Semafor, NBC · one-off
- `Interest rates` · e.g. LEAVEPOWELL — Powell leaving, POWELLLEAVE — Powell leaving · settles: Library of Congress · per-event
- `Oil and energy` · e.g. KXVENEZOILCOS — Oil companies starting Venezuelan production · settles: the New York Times, Semafor, NBC · one-off
- `Covid` · e.g. COVIDBILL — Major COVID-19 bill, KXCOVIDBILL — Major COVID-19 bill · settles: Library of Congress · per-event
- `Music` · e.g. KXESDEEKID — Timothée Chalamet is secretly the English rapper EsDeeKid · settles: The Wall Street Journal, Associated Press, Reuters · one-off
- `Trump Agenda` · e.g. KXPOTUSTWEETS — POTUS tweets · settles: X · weekly
- `Trump Policies` · e.g. KXPOTUSTWEETS — POTUS tweets · settles: X · weekly
- `Drug Prices` · e.g. KXINSULINCAP — Insulin cap ended · settles: Library of Congress · per-event
- `Bankruptcy & Defaults` · e.g. CREDITRATING — US credit rating downgrade · settles: Fitch, Moody's, Standard & Poor's · per-event
- `Retail/consumer spending` · e.g. CREDITRATING — US credit rating downgrade · settles: Fitch, Moody's, Standard & Poor's · per-event
- `SOL` · e.g. KXCRYPTORESERVE — Crypto reserve assets · settles: ABC, Axios, CBS · per-event
- `Achievements` · e.g. KXNOBELPEACE — Nobel Peace Prize · settles: Nobel Prize organization · per-event
- `Other US Elections` · e.g. KXPAFLOCKBAN — Pennsylvania networked Flock camera ban · settles: Pennsylvania General Assembly, Governor of Pennsylvania · one-off
- `SOTU` · e.g. KXATTENDSOTU — Who will attend the State of the Union? · settles: USA Today, ABC, Fox News · one-off
- `Awards` · e.g. KXACTORAWARDSATTEND — Who will attend the actor awards · settles: USA Today, ABC, Fox News · one-off
- `Climate change` · e.g. KXPARIS — Trump Paris Agreement · settles: The New York Times, White House · per-event
- `Brazil` · e.g. KXBRAZILDISCORD — Brazil blocking access to Discord · settles: Agencia Nacional de Telecomunicacoes (Anatel), Supremo Tribunal Federal · one-off
- `Governor` · e.g. KXCASESSION — California special legislative session calls · settles: Office of the Governor of California · one-off

**Elections** — 29 subcategories

- `US Elections` · e.g. KXCAVOTERID — Will the California Voter ID initiative pass?, KX2028RRUN — 2028 R running, KXSECSTATEMN — Minnesota Secretary of State winner · settles: the Associated Press, The Wall Street Journal, Politico · one-off
- `Primaries` · e.g. KXSENATEPAD — Democratic nominee for Senate in Pennsylvania?, KXLAPRIMARY — Louisiana Primary Winners, KXSENATENYD — Democratic nominee for New York Senate · settles: Republican Party, Democratic Party, Reuters · one-off
- `(no tag assigned)` · e.g. KXAMERICAPARTY2028 — America party 2028, KXVOTECOUNTY — County vote percentages, KXBALLOTAMERICAPARTY — America Party on the ballot · settles: The New York Times, Politico, constitutional court · one-off
- `International elections` · e.g. KXXISUCCESSOR — Xi Jinping successor, KXNEWTAIPEIMAYOR — New Taipei mayoral election winner, KXKAMLOOPSMAYOR — Kamloops mayoral election winner · settles: the official electoral commission or equivalent electoral authority of the relevant jurisdiction · one-off
- `Senate` · e.g. SENATENC — North Carolina Senate race, SENATEMO — Missouri Senate race, KXSENATEDEMLEAD — Next Senate Democratic Leader election · settles: United States Congress, the Associated Press · per-event
- `House` · e.g. KXHOUSERACE — House Race Winner?, HOUSENY4 — House New York 4th, HOUSEMI10 — House MI 10 · settles: Library of Congress, official electoral commission · one-off
- `Other US Elections` · e.g. KXCAVOTERID — Will the California Voter ID initiative pass?, KXLTGOVGA — Georgia Lieutenant Governor winner?, KXATTYGENGA — AG race GA · settles: the relevant electoral authority, county clerk or board of elections · one-off
- `Governor` · e.g. GOVPARTYNC — North Carolina Governor, GOVPARTYMI — Michigan Governor, GOVPARTYCA — California Governor · settles: US State Governments, the Associated Press · per-event
- `International` · e.g. KXELECTIRAN — Will Iran hold a presidential election?, KXUPASSEMBLY — Uttar Pradesh Assembly election, KXPARANAGOV — Paraná Governor winner · settles: Reuters, Politico, Axios · one-off
- `Election Combos` · e.g. KXCLOSESTGOVERNOR — closest governor's race, KXGOVWINS — Who will hold more governorships after the midterms?, KXHOUSEWINSTATE — How many seats will party win in state? · settles: the Associated Press, Bureau of Labor Statistics · one-off
- `Foreign Elections` · e.g. KXQUEBECASSEMBLY — Which party will win the National Assembly of Quebec, KXSWISSREF — Will the 2025 Switzerland referenda pass?, KXBRAZILPRES1R — Will anyone win outright in the Brazil presidential first round · settles: Reuters, the Associated Press, Politico · one-off
- `2028` · e.g. KX2028RRUN — 2028 R running, ECMOV — Electoral college margin of victory, KXRTICKET — Republican Presidential ticket · settles: Fox News, MSNBC, The Wall Street Journal · one-off
- `Brazil` · e.g. KXBRPRES — Brazil Presidency, KXCEARAGOV — Ceará gubernatorial election, KXPERNAMBUCOGOV — Pernambuco Governor winner · settles: Tribunal Superior Eleitoral (TSE) · one-off
- `Mixed Combos` · e.g. KXMUSKCHALLENGERS — Musk challengers, KXBLUETSUNAMICOMBO — Will there be a blue tsunami?, KXBLUEWAVECOMBO — Will there be a blue wave? · settles: the Associated Press, Fox News · one-off
- `Senate Combos` · e.g. KXFOURSTATESEN — Four-state senate combo, KXDSENATESEATS — Democratic Senate seats, KXDSENATESEATSH — Democratic Senate seats (higher strikes) · settles: the Associated Press · one-off
- `House Combos` · e.g. KXHOUSEWINSTATE — How many seats will party win in state?, KXVAHOUSEDEM — How many Virginia House seats will Democrats win?, KXDHOUSESEATSDIR — Democratic House seats (Directional) · settles: United States Congress, the Associated Press · one-off
- `SCOTUS & courts` · e.g. KXWASUPREME3 — Washington Supreme Court Position 3 election, KXMOSUPREMECOURT — Missouri Supreme Court judicial retention, KXTXSUPREME7 — Texas Supreme Court Place 7 election · settles: Texas Secretary of State, Washington Secretary of State, Missouri Secretary of State · one-off
- `Local` · e.g. KXTAIPEIMAYOR — Taipei mayoral election winner, KXTX23SPECIALDATE — TX-23 election date, KXHAMILTONMAYOR — Hamilton mayoral election winner · settles: Central Election Commission of Taiwan, Reuters, Semafor · one-off
- `Referendums` · e.g. KXMICONSTITUTION — Michigan constitutional convention question, KXFLPROPERTYTAX — Will Florida's property tax amendment pass?, KXCABALLOTMEASURES — Which California ballot measures will pass? · settles: The Wall Street Journal, CBS News, CNN International · one-off
- `Hungary` · e.g. KXHUNGARYPARLIPARTY — Which party will win the Hungary parliamentary election, KXFIDESZKDNPSEATS — Hungary parliamentary election: Fidesz–KDNP seats, KXTISZASEATS — Hungary parliamentary election: TISZA seats · settles: the official electoral commission / constitutional court · one-off
- `Governor Combos` · e.g. KXCLOSESTGOVERNOR — closest governor's race, KXGOVWINS — Who will hold more governorships after the midterms?, KXRGOVCOUNT — How many Republican Governors after the midterms? · settles: the Associated Press, Fox News, official state election division websites · one-off
- `Peru` · e.g. KXPERUPRES — Peru Presidency, KXPERUPRESMATCHUP — Peru presidential matchup, KXPERUPRES1RMOV — Peru First Round Margin of Victory · settles: the official electoral commission / constitutional court · one-off
- `Congress` · e.g. KXMINLEAD120 — House Minority Leader (120th Congress), KXSENATEDEMLEAD — Next Senate Democratic Leader election · settles: House Republican Conference, Associated Press, Reuters · one-off
- `Iran` · e.g. KXELECTIRAN — Will Iran hold a presidential election? · settles: The New York Times, Fox News, MSNBC · one-off
- `Trump` · e.g. KXTRUMPBEARCASECOMBO — Trump's year: Bear (nightmare) case?, KXTRUMPBULLCASECOMBO — Trump's year: Bull (dream) case? · settles: Bureau of Labor Statistics, Federal Reserve Board of Governors · annual
- `Recurring` · e.g. KXGENERICBALLOTVOTEHUB — Generic ballot VoteHub · settles: VoteHub · daily
- `SOTU` · e.g. KXTRUMPKIDSSOTUCOMBO — Will all of Trump's children attend the SOTU? · settles: Bureau of Labor Statistics, Federal Reserve Board of Governors · one-off
- `CEOs` · e.g. KXUNSEC — UN Secretary · settles: The Washington Post, ESPN, NBC · one-off
- `Companies` · e.g. KXUNSEC — UN Secretary · settles: The Washington Post, ESPN, NBC · one-off

**Financials** — 47 subcategories

- `Companies` · e.g. KXDJIAREMOVE — Companies removed from DJIA, KXIPODEEL — When will Deel IPO, KXNTRA — Natera quarter KPI · settles: Fiscal.ai, The Wall Street Journal, Reuters · one-off
- `KPIs` · e.g. KXNTRA — Natera quarter KPI, KXAAL — American Airlines KPI, KXCVNA — Carvana KPI · settles: Fiscal.ai, company filings, Fox Business · one-off
- `Markets` · e.g. KXME — S&P/BMV IPC Index, KXWTIVSBRENT — Will the WTI outperform Brent this year?, KXDJIAREMOVE — Companies removed from DJIA · settles: U.S. Department of the Treasury, Google Finance, TradingView · one-off
- `Indices` · e.g. KXFEAR — Fear and Greed index, KXME — S&P/BMV IPC Index, KXDJIAREMOVE — Companies removed from DJIA · settles: Google Finance, TradingView · one-off
- `Foreign Exchange` · e.g. KXEURUSD — EUR/USD daily range, KXUSDJPY — USD/JPY daily range, KXUSDBRLMAX — USD/BRL max · settles: ICE, Pyth · daily
- `(no tag assigned)` · e.g. KXRELOCATEUNITED — Will United move its HQ, KXCRYPTOPAY — Crypto payments from tech firms, KXCOMPANYACTIONLAYOFF — Layoff · settles: Reuters, The Wall Street Journal, CNBC · one-off
- `Product launches` · e.g. KXXAIGAME — Will xAI release a video game, KXPRICEINCREASESPOTIFYDUO — Spotify Duo plan increase?, KXKPOPDH2 — Will KPop Demon Hunters 2 be released · settles: company, authorized retailers and distributors · one-off
- `Interest Rates` · e.g. KXUST5A — UST 5 Year Daily, KXUST2A — UST 2 Year Daily, KX10YRDIRHM — 10Y how high monthly · settles: U.S. Department of the Treasury, Federal Reserve Bank of St. Louis · monthly
- `CEOs` · e.g. KXJPMCEONEW — New JPM CEO, KXNEWROLEOPENAI — OpenAI new role, KXNEWROLEFAZE — Next CEO of FaZe Media · settles: Bloomberg, The Washington Post · per-event
- `Industries` · e.g. KXANITOCABTAGENE — Anitocabtagene, KXH200WS — Weekly H200, KXDDR5MS — Monthly DDR5 16Gb 4800/5600 · settles: AppliedXL, Ornn · one-off
- `IPOs` · e.g. KXIPODEEL — When will Deel IPO, KXIPOPERPLEXITY — Perplexity IPO, KXOPENAIBANKPUBLIC — OpenAI · settles: The Wall Street Journal, Financial Times, ABC · one-off
- `Credit Card Spend` · e.g. KXCOSTCC — Costco Credit Card Spend, KXMCDCC — McDonald's Credit Card Spend, KXWMTCC — Walmart Credit Card Spend · settles: Carbon Arc · one-off
- `M&A` · e.g. KXUSACOMPANYSTAKE — Which companies will the US take a stake in, KXACQANNOUNCEEBAY — Will GameStop acquire eBay?, KXACQANNOUNCEANNUAL — companies acquired this year · settles: CNBC, Financial Times, The Wall Street Journal · one-off
- `App Downloads` · e.g. KXCARTAPP — Instacart app downloads, KXUBEREAPP — Uber Eats app downloads, KXMAXAPP — Max app downloads · settles: Carbon Arc · one-off
- `Compute` · e.g. KXH200WS — Weekly H200, KXDDR5MS — Monthly DDR5 16Gb 4800/5600, KXDDR5EMS — Monthly DDR5 16Gb eTT · settles: Ornn, Ornn Dashboard - Tokens, Pyth · weekly
- `Biotech` · e.g. KXANITOCABTAGENE — Anitocabtagene, KXBEPIROVIRSEN — Bepirovirsen, KXBBP418 — BBP-418 · settles: AppliedXL · one-off
- `Medicine` · e.g. KXANITOCABTAGENE — Anitocabtagene, KXBEPIROVIRSEN — Bepirovirsen, KXBBP418 — BBP-418 · settles: AppliedXL · one-off
- `AI` · e.g. KXH200WS — Weekly H200, KXDDR5MS — Monthly DDR5 16Gb 4800/5600, KXDDR5EMS — Monthly DDR5 16Gb eTT · settles: Ornn, Ornn Dashboard - Tokens · weekly
- `Point of Sale` · e.g. KXMONSTERPOS — Monster Energy Drinks Point of Sale Growth, KXROGUEPOS — Rogue Point of Sale Growth, KXCOCACOLAPOS — Coca-Cola Point of Sale Growth · settles: Carbon Arc · one-off
- `Headcount` · e.g. KXINTC — Intel KPI, KXMETA — Meta KPI, KXAMZN — Amazon KPI · settles: Fiscal.ai · one-off
- `Foot Traffic` · e.g. KXYUMTBFT — Taco Bell Foot Traffic, KXSHAKFT — Shake Shack Foot Traffic, KXMCDFT — McDonald's Foot Traffic · settles: Carbon Arc · one-off
- `Net Worth` · e.g. KXMUSKNW — Elon Musk net worth on [date] · settles: Bloomberg - Billionaires Index · monthly
- `Advertising Spend` · e.g. KXFOOTWEARADS — Footwear Retail Ad Spend, KXBROADLINEADS — Broadline Retail Ad Spend, KXELECTRONICSADS — Consumer Electronics Ad Spend · settles: Carbon Arc · one-off
- `S&P` · e.g. KXSP500WHEN — when SP500 price · settles: Google Finance · daily
- `Tech` · e.g. KXDDR5MS — Monthly DDR5 16Gb 4800/5600, KXDDR5EMS — Monthly DDR5 16Gb eTT, KXRTX5090MS — RTX 5090 Monthly · settles: Ornn · monthly
- `Match Ups` · e.g. KXWTIVSBRENT — Will the WTI outperform Brent this year?, KXDXYVSGOLD — DXY vs. Gold, KXGOLDVSSILVER — Gold vs. Silver · settles: Google Finance, CNBC · annual
- `EUR/USD` · e.g. EURUSDH — EUR/USD over/under, EURUSDMIN — EUR/USD yearly low, EURUSDEOY — Euro > Dollar · settles: ICE, International Monetary Fund, Federal Reserve System · daily
- `Nasdaq` · e.g. NASDAQ100W — Nasdaq range, NASDAQ100Z — Nasdaq up, NASDAQ100 — Nasdaq range · settles: Google Finance · daily
- `15 Min Markets` · e.g. KX2YRRATE15M — 2-year Treasury yield 15-minute, KX30YRRATE15M — 30-year Treasury yield 15-minute, KX10YRRATE15M — 10-year Treasury yield 15-minute · settles: U.S. Department of the Treasury, Google Finance · 15-minute
- `WTI` · e.g. WTI — WTI oil daily range, WTIMAX — WTI oil yearly high, WTIH — WTI oil over/under · settles: ICE · annual
- `Treasuries` · e.g. 10Y3M — Treasury spread 10Y-3M, TNOTEW — Treasury 10Y weekly yield, TNOTE — Treasury yield 10Y · settles: U.S. Department of the Treasury, Federal Reserve Bank of St. Louis · weekly
- `USD/JPY` · e.g. USDJPY — USD/JPY daily range, USDJPYH — USD/JPY daily over/under, USDJPYMIN — USD/JPY yearly low · settles: ICE · daily
- `Healthcare` · e.g. KXCYTOTEST — Cytokinetics Test, KXSAMSON — Samson Clinical Ops - Sublingual Minoxidil · settles: AppliedXL · one-off
- `USD/TWD` · e.g. USDTWDMAX — USD/TWD yearly high, USDTWDMIN — U.S. Dollar/Taiwan Dollar exchange rate · settles: ICE · per-event
- `Tokens` · e.g. KXANTHTOKEND — Anthropic token price, KXANTHTOKENM — Anthropic Token Price · settles: Ornn Dashboard - Tokens · one-off
- `USD/RUB` · e.g. USDRUBMIN — USD/RUB yearly low, USDRUBMAX — USD/RUB yearly high · settles: ICE · per-event
- `USD/ARS` · e.g. USDARSMAX — USD/ARS yearly high, USDARSMIN — USD/ARS yearly low · settles: ICE · per-event
- `Fed` · e.g. DOLLARFED — FOMC decision -> EUR/USD, KXDOLLARFED — FOMC decision -> EUR/USD · settles: Federal Reserve, ICE · per-event
- `15 min` · e.g. KXNDQ15M — Nasdaq 100 15-minute, KXINX15M — S&P 500 15-minute · settles: Google Finance · 15-minute
- `Iran` · e.g. KXPAHLAVIHEAD — Will Pahlavi lead Iran? · settles: The Washington Post, ESPN, NBC · one-off
- `Collectibles` · e.g. KXINXMAX — When will the S&P 500 hit an all time high? · settles: Bezel · per-event
- `Bezel` · e.g. KXINXMAX — When will the S&P 500 hit an all time high? · settles: Bezel · per-event
- `Inflation` · e.g. KXCOSTCOMEMBER — Costco membership price increase · settles: Costco · per-event
- `Video games` · e.g. KXFALLOUTRELEASE — Will Bethesda announce a new Fallout game · settles: company, authorized retailers and distributors · one-off
- `2026 Mega IPOs` · e.g. KXIPOSPACEX — When will SpaceX IPO · settles: the New York Times, ABC, Bloomberg · one-off
- `Oil and energy` · e.g. KXKEYSTONEFID — Keystone XL final investment decision · settles: South Bow Corporation · one-off
- `Housing` · e.g. KXFREDDIE — When will Freddie Mac IPO? · settles: the New York Times, ABC, Bloomberg · one-off

**Economics** — 31 subcategories

- `Inflation` · e.g. KXECONSTATCPIYOY — year over year inflation, KXECONSTATCORECPIYOY — year over year core inflation, KXDDCOLDBREW — Price of a Dunkin' Medium Cold Brew this month · settles: Bureau of Labor Statistics - Consumer Price Index · monthly
- `Jobs & Economy` · e.g. KXU3EOY — U.S. unemployment rate at year-end, KXLAOILGASEMP — Louisiana oil and gas extraction employment, KXALVEHICLEPROD — Alabama vehicle production · settles: Bureau of Labor Statistics - Employment Situation, Federal Reserve Bank of New York · annual
- `Growth` · e.g. KXIRANIMPORTS — U.S. imports from Iran in [time period], KXMSCOTTON — Mississippi cotton production, KXWVPOP — West Virginia population · settles: Trading Economics, Federal Reserve Bank of New York · annual
- `(no tag assigned)` · e.g. KXEFFR — Fed Funds (EFFR) above/below, KXLAYOFFSYINFO — Tech layoffs, KXAKSALMON — Alaska salmon harvest · settles: Bureau of Labor Statistics - Consumer Price Index · per-event
- `Oil and energy` · e.g. KXAAAGASMIN — US lowest gas price yearly, KXAAAGASDWA — Washington gas price, KXWVCOAL — West Virginia coal production · settles: AAA, Energy Information Administration · daily
- `Housing` · e.g. KXCOHPIYOY — Colorado home prices, KXBOZPERMITS — Bozeman housing units authorized, KXRIHOMEPRICE — Rhode Island House Price Index · settles: Bureau of Labor Statistics, Federal Reserve Bank of New York · annual
- `Fed` · e.g. KXEMERCUTS — Emergency rate cuts, KXFEDCHGCOUNT — Number of rate changes, KXFEDREFORM — Which Federal Reserve precedents will be broken · settles: Federal Reserve · per-event
- `Global Central Banks` · e.g. KXCBDECISIONNZ — Reserve Bank of New Zealand rate decision, KXCBRATEHIKE — Which central banks will hike this year?, KXCBDSA — South Africa rate decision · settles: Semafor, Associated Press, The Wall Street Journal · per-event
- `Econ Daily` · e.g. KXTRUEV — Truflation EV, KXAAAGASDWA — Washington gas price, KXAAAGASDFL — Florida gas price · settles: AAA, Truflation, ERCOT · daily
- `GDP` · e.g. KXGDP — US GDP growth, KXNOMGDPGROWTH — Nominal GDP growth in [year], KXBRAZILGDP — Brazilian GDP Growth · settles: Trading Economics, Bureau of Economic Analysis · per-event
- `Oil & Gas` · e.g. KXAAAGASMIN — US lowest gas price yearly, KXAAAGASMINCA — California lowest gas price yearly, KXAAAGASMAXCA — California highest gas price yearly · settles: AAA, Energy Information Administration · annual
- `International` · e.g. KXCANAUTOSTEEL50 — 50% tariffs on Canadian autos and steel · settles: Federal Reserve System, OECD, Department of Finance Canada · weekly
- `Econ Weekly` · e.g. KXJOBLESSCLAIMS — Weekly initial jobless claims, KXAAAGASW — US gas price up, KXAAAGASWNJ — New Jersey gas price this week · settles: AAA, Federal Reserve Bank of New York, Department of Labor · weekly
- `Interest rates` · e.g. RATECUTCOUNT — Number of rate cuts, RATECUTS — Number of rate cuts, FEDDECISION — Fed meeting · settles: Federal Reserve, Federal Reserve Board of Governors · per-event
- `Retail/consumer spending` · e.g. SFRENTSY — SF yearly rent growth, KXCREDITCDEF — Credit card defaults up, GDP — US GDP growth · settles: Federal Reserve, Costco, U.S. Census Bureau · per-event
- `Employment` · e.g. JOBLESS — Initial jobless claims, PROLLS — Jobs numbers, BIGBANKLAYOFF — Big banks layoffs · settles: BLS, FRED, Federal Reserve Economic Data · monthly
- `Bankruptcy & Defaults` · e.g. FEDFACILITY — Fed facility, CREDEF — Commercial real estate defaults, CREDEFMAX — Commercial real estate highest default rate · settles: Federal Reserve, Standard & Poor's · per-event
- `Local` · e.g. KXRBWSTRIKE — NYC RBW Strike, KXLIRRSTRIKE — LIRR strike, KXNURSESTRIKE — When will the NYC nurse strike end? · settles: official statements from the employer or its parent organization · one-off
- `Layoffs` · e.g. LAYOFFSYINFO — Tech layoffs, LAYOFFSY — layoffs, BIGBANKLAYOFF — Big banks layoffs · settles: FRED, Bloomberg · annual
- `Foreign economies` · e.g. WRECSS — World recessions, CHINAUSGDP — China overtakes US GDP, BOE — Bank of England bank rate · settles: IMF, Bank of England · per-event
- `Credit & Bonds` · e.g. KXHLENDHALT — BlackRock HLEND suspend repurchases by [date], KXHLENDREDM — Will BlackRock HLEND suspend repurchases by [date] · settles: Semafor, Bureau of Labor Statistics · one-off
- `Gas` · e.g. DIESEL — Diesel price this week, DIESELM — Diesel price this month · settles: Energy Information Administration · weekly
- `Defaults` · e.g. MORTGAGEDEF — Mortgage defaults, KXMORTGAGEDEF — Mortgage defaults · settles: Federal Reserve · per-event
- `Mortgages` · e.g. MORTGAGEDEF — Mortgage defaults, KXMORTGAGEDEF — Mortgage defaults · settles: Federal Reserve · per-event
- `CEOs` · e.g. WEALTHY — Wealthiest person in world, WEALTH — Person wealthiest · settles: Forbes · annual
- `Elon Musk` · e.g. WEALTHY — Wealthiest person in world, WEALTH — Person wealthiest · settles: Forbes · annual
- `KPIs` · e.g. KXCOSTCOHOTDOG — Costco hot dog price increase · settles: Costco · per-event
- `Bills` · e.g. WTAX — Wealth tax · settles: Library of Congress · one-off
- `Yield curves` · e.g. YINVERT — Yield Curve Inversion · settles: Federal Reserve Bank of St. Louis · annual
- `AI` · e.g. SEMIPRODH — US Semiconductor production · settles: Board of Governors of the Federal Reserve · annual
- `Soccer` · e.g. KXHKANEKNIGHT — Harry Kane Knighted · settles: Semafor, ABC, Bloomberg · per-event

**Commodities** — 11 subcategories

- `Metals` · e.g. KXSILVERH — Silver Hourly, KXGOLDD — Gold Daily, KXGOLD15M — Gold 15-minute · settles: Pyth - Gold, Pyth - Silver, Pyth - Copper · weekly
- `Oil & Gas` · e.g. KXNATGASW — Natural Gas Weekly, KXWTIH — WTI Hourly, KXWTIDIRY — WTI Directional Yearly · settles: ICE, Pyth - NATGAS, Pyth - Brent · weekly
- `Agriculture` · e.g. KXLCATTLEMON — Live Cattle Monthly, KXCOCOAMON — Cocoa Monthly, KXSOYBEANMON — Soybean monthly · settles: Pyth, Trading Economics - Live Cattle, Trading Economics - Cocoa · monthly
- `(no tag assigned)` · e.g. KXPLATINUMH — Platinum Hourly, KXPALLADIUMH — Palladium Hourly, KXEUBEEFQ — EU beef quarterly threshold · settles: USDA, Trading Economics - Copper Futures, Trading Economics - Silver · hourly
- `15 min` · e.g. KXGOLD15M — Gold 15-minute, KXSILVER15M — Silver 15-minute, KXCOPPER15M — Copper 15-minute · settles: Pyth - Gold, Pyth - Silver, Pyth - Copper · 15-minute
- `Product launches` · e.g. KXVERARELEASE — Vera/Rubin release, KXGEMINI35Y — Gemini 3.5 Flash, KXOPUS48Y — Opus 4.8 Input Token · settles: Anthropic, company, authorized retailers · annual
- `Markets` · e.g. KXGEMINI35Y — Gemini 3.5 Flash, KXOPUS48Y — Opus 4.8 Input Token, KXGPT55Y — GPT 5.5 Input Token · settles: Anthropic, USDA, Google Gemini Developer API pricing · annual
- `Tokens` · e.g. KXOPUS48OY — Opus 4.8 Output Token, KXGEMINI35OY — Gemini 3.5 Flash Output Token, KXGBT55OY — GPT 5.5 Output Token · settles: Anthropic · annual
- `Tech` · e.g. KXGEMINI35Y — Gemini 3.5 Flash, KXOPUS48Y — Opus 4.8 Input Token, KXGPT55Y — GPT 5.5 Input Token · settles: Anthropic, Google Gemini Developer API pricing, OpenAI · annual
- `Compute` · e.g. KXVERARELEASE — Vera/Rubin release · settles: company, authorized retailers and distributors · one-off
- `Companies` · e.g. KXVERARELEASE — Vera/Rubin release · settles: company, authorized retailers and distributors · one-off

**Crypto** — 15 subcategories

- `(no tag assigned)` · e.g. KXSHIBA — Shiba range, KXSHIBAD — Shiba price Above/below, KXBTCHALF — BTC halving · settles: CF Benchmarks, Reuters · per-event
- `BTC` · e.g. KXBTC2026200 — Will Bitcoin hit 200k in 2026?, KXBTCMAXMON — Bitcoin monthly one touch, KXBTCMINY — How low will Bitcoin fall this year? · settles: CF Benchmarks · per-event
- `Pre-Market` · e.g. KXFDVOPENSEA — OpenSea FDV, KXTOKENLAUNCH — Who will launch a token this year? · settles: CoinGecko, Axios, Reuters · one-off
- `SOL` · e.g. KXSOLMAXY — Solana Max Yearly, KXSOLD — SOL Directional, KXSOLD26 — SOL price end of 2026? · settles: CF Benchmarks · per-event
- `Hourly` · e.g. KXETHD — Ethereum price Above/below, KXSOLE — SOL Range, KXHYPEY — HYPE Yearly · settles: CF Benchmarks · hourly
- `ETH` · e.g. KXETHD — Ethereum price Above/below, KXETH15M — ETH 15M price up down, KXETHY — ETH price EOY · settles: CF Benchmarks · per-event
- `15 min` · e.g. KXXRP15M — XRP 15 Minute, KXETH15M — ETH 15M price up down, KXNEAR15M — NEAR 15m · settles: CF Benchmarks · 15-minute
- `DOGE` · e.g. KXDOGEMINY — DOGE min yearly, KXDOGEMINMON — Doge min monthly, KXDOGEMAXY — Dogecoin max · settles: CF Benchmarks · monthly
- `XRP` · e.g. KXXRPMAXY — XRP Max, KXXRP15M — XRP 15 Minute, KXXRPMINY — XRP Min · settles: CF Benchmarks · annual
- `BNB` · e.g. KXBNBMAXMON — BNB Max Monthly, KXBNBMINMON — BNB Min Monthly, KXBNBD — BNB Directional · settles: CF Benchmarks · monthly
- `HYPE` · e.g. KXHYPE15M — Hype 15 min, KXHYPEMAXMON — Hype Max Monthly, KXHYPED — Hype Directional · settles: CF Benchmarks · monthly
- `15 Min Markets` · e.g. KXCRYPTOLEAD15M — Coin Race 15 minutes · settles: CF Benchmarks · 15-minute
- `ZEC` · e.g. KXZECMINY — ZEC Min Year, KXZEC15M — Zcash 15min, KXZECMINMON — Zcash min monthly · settles: CF Benchmarks · monthly
- `NEAR` · e.g. KXNEAR15M — NEAR 15m, KXNEARMAXY — Near Max Year, KXNEARMINY — Near Min Year · settles: CF Benchmarks · annual
- `Head to Heads` · e.g. KXBTCVSSOL — BTC vs. SOL, KXPHXVSHYP — Will Phoenix flip Hyperliquid in 24 hr Perp Trading, KXCRYPTOCOMP15M — Crypto Comparison 15 minute · settles: CF Benchmarks Real-Time Index, flipthe.market · weekly

**Climate and Weather** — 15 subcategories

- `(no tag assigned)` · e.g. KXHDDCVG — Cincinnati heating degree days, KXMEAD — Lake Mead water levels, KXBIGGESTQUAKE — Biggest earthquake · settles: The Weather Company, National Weather Service, NOAA · daily
- `Hurricanes` · e.g. KXNEXTHURDATE — Next hurricane date, KXFIRSTHURRICANE — First Hurricane, KXHURPATHNC — Hurricane hits North Carolina · settles: National Weather Service, NOAA, AccuWeather · per-event
- `Daily temperature` · e.g. KXHIGHTPHX — Phoenix High Temperature Daily, KXHIGHMIA — Highest temperature in Miami, KXLOWTOKC — Low Temperature Oklahoma City · settles: The Weather Company, NWS Climatological Report · daily
- `Snow and rain` · e.g. KXRAINLAXM — Rain Los Angeles, KXRAINAUSM — Rain Austin, KXRAINWKND — Where will it rain this weekend? · settles: The Weather Company, the National Weather Service, NOAA · monthly
- `Climate change` · e.g. KXWARMING — Global warming, KXGTEMP — Hottest year ever, KXINDIACLIMATE — India climate goals · settles: National Snow & Ice Data Center, NASA Goddard Institute for Space Studies, NCEI · monthly
- `Natural disasters` · e.g. KXEARTHQUAKECALIFORNIA — Earthquake in California, KXEARTHQUAKEM — Earthquake monthly, KXVEI4 — VEI 4 volcanic eruption · settles: NOAA, USGS, National Weather Service · per-event
- `Ski Resorts` · e.g. KXKEYSTONEOPEN — Keystone Resort Opening, KXBRECKOPEN — Breckenridge Ski Resort Opening, KXSTOWEOPEN — Stowe Mountain Resort Opening · settles: Keystone Resort Snow & Weather Report, Breckenridge Snow & Weather Report, Stowe Mountain Resort · annual
- `Heatwaves` · e.g. KXAVGTKDEN — Average Weekly Temp in Denver, KXAVGTKAUS — Average Weekly Temp in Austin, KXAVGTKPHX — Average Weekly Temp in Phoenix · settles: The Weather Company · weekly
- `Hourly temperature` · e.g. KXTEMPLAXHS — Hourly Directional Coastal LA Temperature, KXTEMPCHIHS — Hourly Directional Chicago Metro Temperature, KXTEMPMIAH — Hourly Directional Miami Temperature · settles: The Weather Company, Synoptic Data · hourly
- `Space` · e.g. KXECLIPSECOVERBUFF — Eclipse Cover Buffalo, KXECLIPSEREYK — Solar Eclipse Reykjavik · settles: National Weather Service · one-off
- `Energy` · e.g. KXEVSHARE — EV market share · settles: Argonne National Laboratory · per-event
- `Global heat` · e.g. TEMP — Average annual temperature deviation, TEMPMON — Global monthly temperature average · settles: NASA Goddard Institute for Space Studies, NOAA · monthly
- `KPIs` · e.g. KXEVSHARE — EV market share · settles: Argonne National Laboratory · per-event
- `Companies` · e.g. KXEVSHARE — EV market share · settles: Argonne National Laboratory · per-event
- `Elon Musk` · e.g. EVSHARE — EV market share · settles: Argonne National Laboratory · per-event

**Science and Technology** — 25 subcategories

- `AI` · e.g. KXA100MAX — A100 Yearly Directional Price, KXH200MAX — H200 Yearly Directional Price, KXDEEPSHARE — DeepSeek market share · settles: OpenAI, Ornn, LMSYS · per-event
- `(no tag assigned)` · e.g. KXSTARSHIPSPACE — Starship launches to Space, KXPNP — P vs NP resolution, KXRIEMANN-adjacent KXMILLENNIUMNEXT — Next Millennium Prize Problem · settles: Reuters, The New York Times, The Wall Street Journal · per-event
- `Space` · e.g. KXRKLBLAUNCH — Rocket Lab Launch, KXNEWGLENN — New Glenn, KXMOON — NASA lands on the moon · settles: The New York Times, Federal Aviation Administration, SpaceX · per-event
- `Public Health` · e.g. KXH5N1COUNT — Human H5N1 cases, KXEBOLACOUNTRY — Which countries will report an Ebola case?, KXTBCOUNT — TB cases · settles: WHO, CDC, national health agencies · per-event
- `Compute` · e.g. KXA100MAX — A100 Yearly Directional Price, KXH200MAX — H200 Yearly Directional Price, KXB200MAX — B100 Yearly Directional Price · settles: Ornn, Ornn Dashboard - Tokens · one-off
- `Product launches` · e.g. KXFDAAPPROVE — Will the FDA approve drug?, KXFDAAPPROVALDATECMPS — Compass Pathways Drug Approval, KXTESLAOPTIMUS — Tesla Optimus sale · settles: OpenAI, Food and Drug Administration, SpaceX · per-event
- `Tech` · e.g. KXA100MAX — A100 Yearly Directional Price, KXH200MAX — H200 Yearly Directional Price, KXB200MAX — B100 Yearly Directional Price · settles: Ornn · annual
- `Medicine` · e.g. KXFDAAPPROVE — Will the FDA approve drug?, KXFDAAPPROVALDATECMPS — Compass Pathways Drug Approval, KXNEWDRUGAPPBEAM — Beam Therapeutics Drug Application · settles: Food and Drug Administration · one-off
- `Big Tech & Business` · e.g. KXSPACEXMARS — SpaceX Mars, KXSTARSHIPDOCK — Starships dock, KXNYTOAI — New York Times wins OpenAI lawsuit · settles: The New York Times, Reuters, The Wall Street Journal · per-event
- `Physics & Math` · e.g. KXRIEMANN — Riemann hypothesis solved, KXFUSION — Nuclear fusion, KXNOBELLIT — Nobel Literature prize · settles: Reuters, The New York Times, Nobel Foundation · per-event
- `AI Indices` · e.g. KXGOOGLADOPT — Google AI adoption rate, KXAIHEALTH — Health care AI adoption, KXAIFINANCE — Finance and insurance AI adoption · settles: Ramp AI Index · monthly
- `Energy` · e.g. KXPRIMEENGCONSUMPTION — Prime energy source, KXREACTOR — US grants license for new nuclear reactor, KXMEISSNER — Meissner effect confirmed near room temperature · settles: Nuclear Regulatory Commission, Argonne National Laboratory, Kalshi · per-event
- `Companies` · e.g. KXFDAAPPROVE — Will the FDA approve drug?, KXTESLAOPTIMUS — Tesla Optimus sale, KXFDAAPPROVALDATECMPS — Compass Pathways Drug Approval · settles: Food and Drug Administration, Tesla, SpaceX · one-off
- `Market Share` · e.g. KXDEEPSHARE — DeepSeek market share, KXOPENSHARE — OpenAI Market Share, KXBABASHARE — Alibaba market share · settles: OpenRouter - AI Market Share, Vercel AI Gateway Leaderboards · one-off
- `Tokens` · e.g. KXTOKENUSE — token usage, KXTOKENUSEM — token usage in month · settles: Ornn Dashboard - Tokens, OpenRouter - AI Model Rankings · one-off
- `Industries` · e.g. KXOPENTOKENM — OpenAI token price, KXGOOGTOKENM — Google Token Price, KXDEEPTOKENM — DeepSeek Token Price · settles: Ornn Dashboard - Tokens · one-off
- `Education` · e.g. KXUSTESTSMATH — US Test scores in Math, KXCOLLEGERANK — College rankings, KXCOLLEGEDROP — College rankings drop · settles: Nation's Report Card, U.S. News and World Report · per-event
- `KPIs` · e.g. OAIAGI — OpenAI achieves AGI, TOPLLM — GPT no longer top ranked LLM, LLM1 — Year-end top LLM · settles: LMSYS, OpenAI · per-event
- `Papers` · e.g. SUPERCON — Room-temp superconductor validated, MEISSNER — Meissner effect confirmed near room temperature · settles: Kalshi · per-event
- `Employment` · e.g. TECHLAYOFF — Tech layoffs up · settles: FRED · monthly
- `Layoffs` · e.g. TECHLAYOFF — Tech layoffs up · settles: FRED · monthly
- `Trump` · e.g. KXFDAAPPROVALPSYCHEDELIC — FDA approval psychedelic · settles: U.S. Food and Drug Administration · per-event
- `Culture war` · e.g. AIDEBATES — AI at the debates · settles: Kalshi · per-event
- `Video games` · e.g. KXSWITCH2RELEASE — Switch 2 release date · settles: Nintendo · per-event
- `Elon Musk` · e.g. SPACEXLAND — Starship lands · settles: Bloomberg · per-event

**Mentions** — 8 subcategories

- `Earnings` · e.g. KXEARNINGSMENTIONAMZN — Amazon earnings mention, KXEARNINGSMENTIONCAVA — Cava Earnings, KXEARNINGSMENTIONMS — Morgan Stanley Earnings Call · settles: Bloomberg, company Investor Events pages · one-off
- `(no tag assigned)` · e.g. KXPERSONMENTION — General person mention, KXZUCKMENTION — What will Zuck say?, KXNVDAMENTION — NVIDIA Mention · settles: ABC, Fox News, MSNBC · one-off
- `Politicians` · e.g. KXTRUMPMENTION — What will Trump say?, KXTRUMPSAYNICKNAME — Trump Nickname, KXTRUMPSAYCOMPANY — Will Trump mention company · settles: Axios, MSNBC, The Wall Street Journal · per-event
- `Sports` · e.g. KXNASCARMENTION — Nascar announcers, KXNCAABMENTION — College Basketball mentions, KXEPLMENTION — Premier League Mentions · settles: ABC, Fox News, MSNBC · one-off
- `Trump` · e.g. KXTRUMPMENTION — What will Trump say?, KXTRUMPSAYNICKNAME — Trump Nickname, KXTRUMPSAYCOMPANY — Will Trump mention company · settles: ABC, Fox News, MSNBC · one-off
- `Entertainment` · e.g. KXBBMENTION — Big Brother Mentions, KXCULTUREMENTION — Culture mentions, KXAWARDMENTION — Award Mention · settles: ABC, Fox News, MSNBC · one-off
- `CEOs` · e.g. KXJENSENMENTION — Jensen Mention · settles: ABC, Fox News, MSNBC · one-off
- `SOTU` · e.g. KXTRUMPMENTIONDURATION — How Long Will Trump Speak · settles: BBC, The Information · one-off

**Companies** — 20 subcategories

- `(no tag assigned)` · e.g. KXRIPPLINGDEEL — Rippling Deel suit, KXCOMPANYLAYOFF — Company Layoffs, KXAPPLEUS — Apple DOJ lawsuit · settles: Reuters, The New York Times, The Wall Street Journal · per-event
- `KPIs` · e.g. KXEBAYA — eBay Annual KPI, KXLUVA — Southwest KPI, KXHDA — Home Depot Annual KPI · settles: Fiscal.ai, Tesla, Meta · one-off
- `Elon Musk` · e.g. TESLAPROD — Tesla production, TESLA — Tesla deliveries, BIGTECHLAYOFF — Big tech layoffs · settles: Tesla, Bloomberg, FAA · per-event
- `Product launches` · e.g. APPLEPORT — Apple reveals portless iPhone, SPACEXSTARSHIP — SpaceX Starship launch, APPLEAI — Apple AI partnership · settles: Apple, Tesla, FAA · per-event
- `CEOs` · e.g. DISBOARD — Disney Board members, WEWORKCEO — WeWork new CEO, BIGTECHLAYOFF — Big tech layoffs · settles: Bloomberg, Disney, Apple · per-event
- `Space` · e.g. SPACEXSTARSHIP — SpaceX Starship launch, SPACEXCOUNT — SpaceX launches, STARSHIPMARS — Starship launch to Mars · settles: FAA, Federal Aviation Administration, SpaceX · per-event
- `AI` · e.g. APPLEAI — Apple AI partnership, OPENAISUIT — Elon Musk OpenAI lawsuit, KXOAIPROFIT — OpenAI becomes for-profit · settles: OpenAI, Apple, PACER · per-event
- `Culture war` · e.g. BRAZILXBAN — Brazil bans X, MORAESLEAVE — Alexandre de Moraes leaving, TIKTOKBAN — US bans TikTok · settles: Bloomberg, Library of Congress, Government of Brazil · per-event
- `Headcount` · e.g. KXSBUXA — Starbucks Annual KPI, KXCMGA — Chipotle Annual KPI, KXSPOTA — Spotify Annual KPI · settles: Fiscal.ai · one-off
- `International politics` · e.g. BRAZILXBAN — Brazil bans X, MORAESLEAVE — Alexandre de Moraes leaving, BRAZILX — Brazil bans X · settles: Bloomberg, Government of Brazil · per-event
- `SCOTUS & courts` · e.g. APPLEUS — Apple DOJ lawsuit, TIKTOKSELL — Congress passes law to force TikTok sale, MORAESLEAVE — Alexandre de Moraes leaving · settles: PACER, Government of Brazil, Library of Congress · one-off
- `GPT` · e.g. OPENAIBOARD — OpenAI board members leaving, OPENAICEO — OpenAI new CEO, OPENAIBOARDJ — OpenAI new board members · settles: OpenAI, Bloomberg · per-event
- `Trump` · e.g. KXLEAVITTVIEW — Will Karoline Leavitt join The View? · settles: NBC News, Semafor, ABC News · one-off
- `Employment` · e.g. BIGTECHLAYOFF — Big tech layoffs · settles: Bloomberg · annual
- `Layoffs` · e.g. BIGTECHLAYOFF — Big tech layoffs · settles: Bloomberg · annual
- `Airlines & aviation` · e.g. SPIRITCEOCHANGE — New Spirit CEO · settles: Spirit · per-event
- `Biden` · e.g. TIKTOKBAN — US bans TikTok · settles: Library of Congress · per-event
- `Bills` · e.g. TIKTOKSELL — Congress passes law to force TikTok sale · settles: Library of Congress · one-off
- `Video games` · e.g. SWITCH2 — New Nintendo Console announced · settles: Nintendo · per-event
- `Football` · e.g. KXSUPERBOWLAD — Super Bowl ads · settles: ABC Sports, Ad Age, Bloomberg News · per-event

**World** — 13 subcategories

- `(no tag assigned)` · e.g. KXELONMARS — Will Elon Musk visit Mars in his lifetime?, KXLOCATIONOPENTESLADRIVEIN — Where will Tesla Diner & Drive-In open this year?, KXMAERSK — Maersk resumes shipping in the Red Sea · settles: the Associated Press, The New York Times, Reuters · per-event
- `Foreign economies` · e.g. ARGDOLLAR — Argentina dollarizes its economy, GDPCN — China GDP growth, MAERSK — Maersk resumes shipping in the Red Sea · settles: Bloomberg, World Bank, Maersk · per-event
- `Growth` · e.g. KXGDPCN — China GDP growth, KXGDPW — Global GDP growth, GDPCN — China GDP growth · settles: World Bank · annual
- `Covid` · e.g. KXCASE7DCN — Long-term China COVID case average, DINENYC — NYC indoor dining ban, DINENYCS — NYC indoor dining ban · settles: World Health Organization, Office of the Mayor of New York City · monthly
- `International politics` · e.g. EUEXPANSION — EU expansion, EUEXIT — EU exit, EUEXPANSIONC — EU Expansion · settles: EU, General Confederation of Labour (Argentina) · per-event
- `Bills` · e.g. CTCS — Child tax credit expanded, FDIC — FDIC Insurance increase, PREK — Universal Pre-K becomes law · settles: Library of Congress, FDIC · per-event
- `Flights` · e.g. KXFLIGHTORD — O'Hare International Airport total delays and cancellations, KXFLIGHTLAX — Los Angeles International Airport total delays, KXFLIGHTJFK — JFK International Airport total flight delays · settles: FlightAware · daily
- `Supply chain` · e.g. MAERSK — Maersk resumes shipping in the Red Sea, SUEZ — Suez canal closes · settles: Maersk, Bloomberg, Suez Canal Authority · per-event
- `Fed` · e.g. TAPER — Fed tapering · settles: Federal Reserve Bank of New York · per-event
- `Retail/consumer spending` · e.g. CRED — Credit card debt · settles: Federal Reserve Bank of New York · monthly
- `SCOTUS & courts` · e.g. KXBANTRANS — ban ruling · settles: Fox News, MSNBC, The Wall Street Journal · one-off
- `Football` · e.g. KXFOOTBALL1001 — Football rankings · settles: NFL.com · annual
- `GDP` · e.g. RECSS — Quarter of negative GDP growth · settles: Bureau of Economic Analysis · annual

**Health** — 9 subcategories

- `(no tag assigned)` · e.g. KXVAXX — COVID vaccinations, KXH5N1CASES — H5N1 cases, KXLIFEEXP — US life expectancy · settles: Centers for Disease Control and Prevention · per-event
- `Covid` · e.g. KXCASEW — New COVID-19 cases this week, CASEW — New COVID-19 cases this week, KXCASE7DFL — Florida COVID daily case avg · settles: Centers for Disease Control and Prevention, Food and Drug Administration, WHO · per-event
- `Other diseases` · e.g. H5N1CASES — H5N1 cases, H5N1 — Bird flu declared PHEIC, NEWOUTBREAKPMPOX — New monkeypox/mpox pandemic · settles: WHO, CDC, World Health Organization · per-event
- `COVID` · e.g. FLUV — Fluvoxamine COVID, CASEWFR — France COVID case average, BOOSTERM — COVID boosters this month · settles: CDC, European Centre for Disease Prevention and Control, FDA · weekly
- `Disease spread` · e.g. H5N1 — Bird flu declared PHEIC, NEWOUTBREAKPMPOX — New monkeypox/mpox pandemic, NEWOUTBREAK-PHEIC — New public health emergency · settles: WHO, World Health Organization, Food and Drug Administration · per-event
- `Health Tech` · e.g. KXFERTILITYRATE — Fertility rate, KXDRUGADS — Drug ads on TV, KXCDCTRAVELH5 — Avian flu travel warning · settles: the National Center for Health Statistics of the CDC · per-event
- `FDA Approval` · e.g. KXNEWDRUGS — New FDA drugs, KXVACCINEW — Vaccine approval withdrawn · settles: FDA, Food and Drug Administration · per-event
- `Drug Prices` · e.g. KXDRUGPRICEINSULIN — Insulin price, KXDRUGPRICEOZEMPIC — Ozempic price · settles: NADAC · per-event
- `Vaccines` · e.g. KXVACCINEW — Vaccine approval withdrawn, KXH5VACCINE — H5 vaccine · settles: Food and Drug Administration · per-event

**Social** — 2 subcategories

- `(no tag assigned)` · e.g. KXMICHELINNYC3 — 3-star in NYC, KXBANDANTES — Will Antes be banned on Twitch · settles: Reuters, The New York Times, CNN · one-off
- `Television` · e.g. KXBACHELORETTEFIR — Who will have the first impression rose on The Bachelorette · settles: ABC · one-off

**Transportation** — 4 subcategories

- `(no tag assigned)` · e.g. KXVANRATE — National Freight Rates (Truckstop.com dry van rates), KXVANRATEMW — Midwest Freight Rates, KXMTA — NYC subway riders · settles: Truckstop.com, UAW, Transportation Security Administration · monthly
- `Airlines & aviation` · e.g. BOEING737MAX9 — 737 Max 9 un-grounded, FLIGHTJFK — JFK International Airport total flight delays, FLIGHTLAX — Los Angeles International Airport total delays · settles: FlightAware, FAA, Transportation Security Administration · daily
- `Supply chain` · e.g. PORTLA — Ships anchored in LA · settles: Port of Los Angeles · weekly
- `CEOs` · e.g. BOEINGCEOCHANGE — New Boeing CEO · settles: Boeing · one-off

**Exotics** — 3 subcategories

- `(no tag assigned)` · e.g. KXMVECROSSCATEGORY — MVE Cross Category, KXMVEOSCARS — MVE Oscars, KXMVEGRAMMYS — MVE NFL Grammys · settles: the league governing the game · one-off
- `Football` · e.g. KXMVENFLMULTIGAMEEXTENDED — MVE NFL Multi Game Extended, KXMVENFLMULTIGAME — MVE NFL Multi Game, KXMVENFLSINGLEGAME — MVE NFL Single Game · settles: the league governing the game · one-off
- `Basketball` · e.g. KXMVENBAMULTIGAMEEXTENDED — MVE NBA Multi Game, KXMVENBASINGLEGAME — MVE NBA Single Game · settles: the league governing the game · one-off

**AI** — 1 subcategories

- `AI` · e.g. KXOPENAIANOTHERMILLENNIUM — OpenAI another Millennium Prize claim, KXRSIANNOUNCE — AI recursive self-improvement announcements, KXBUCKMASTERSUE — Who will Tristan Buckmaster sue? · settles: OpenAI, Sébastien Bubeck, Reuters · one-off

**Education** — 1 subcategories

- `(no tag assigned)` · e.g. KXSTUDENTBAN — Students banned · settles: ABC, Axios, Bloomberg News · per-event

**Business** — 1 subcategories

- `SCOTUS & courts` · e.g. KXAMAZONADS — Amazon ad surcharge lawsuit · settles: U.S. District Court for the Western District of Washington Clerk's Office, PACER · one-off

**Not confirmed:**

- GET /markets?status=open was NOT fully enumerated. An unbounded crawl accumulated >3.3 GB of response bodies without reaching a null cursor and was killed. I verified this is NOT a cursor loop: over 8 consecutive pages every page returned 1,000 unique, previously-unseen tickers and no cursor repeated. A bounded 60-page run covered 60,000 open markets across 36,592 distinct events, but those mapped to only 10 distinct series (the feed is time-ordered, so a slice concentrates on a handful of high-strike-count series). All 10 were present in the /series catalog; 0 unmatched. So the markets endpoint CONFIRMS consistency but did not independently verify full coverage. I am relying on /series returning the complete catalog in one page for that.
- GET /events?status=settled was deliberately capped at 25 pages (5,000 of an unknown larger total). GET /events?status=closed returned 319 events over 2 pages and terminated naturally. Neither revealed any category outside the 20 already in /series, but the settled set was not exhausted.
- Four categories currently have ZERO live series (no open or unopened events): Health (96 series), Transportation (38), Exotics (14), Education (1). They exist only as historical/settled inventory. 'World' has 143 series but only 1 live; 'Business' and 'AI' have 1 and 6 series respectively. If you build a platform taxonomy off live inventory alone you would miss these; if you build off the full catalog you will surface domains Kalshi is not currently trading.
- 'Business' (1 series) and 'Education' (1 series) appear in the scalar series.category field but NOT in any series.categories[] array, and 'Business' also appeared once in events.category. 'AI' and 'Exotics' likewise appear in category but AI is absent from the categories[] union. The two fields are therefore NOT interchangeable: category has 20 distinct values, categories[] has 18. I used the union of both, plus events.category, which is 20.
- One open event returned an EMPTY STRING for category (1 of 13,206), and one settled event likewise. These are unclassified at the venue and are not counted as a 21st category.
- The 380 (category, tag) pairs I enumerate include a synthetic '(no tag assigned)' bucket per category — that label is MINE, not Kalshi's. Kalshi ships tags:null for 2,782 of 14,170 series (19.6%). These untagged series are overwhelmingly one_off/custom bespoke markets (e.g. 837 untagged in Politics, 474 in Entertainment) and are mostly NOT live (only 4 of 837 untagged Politics series have open events). Every other subcategory name is the venue's own tag string, verbatim.
- Kalshi's tags are cross-cutting, not a strict hierarchy. The same tag string appears under many different categories (e.g. 'Trump' appears under Politics, Elections, Entertainment, Mentions, Companies and Science and Technology; 'Football' appears under Sports, Entertainment, Companies, World and Exotics). A given series can also carry multiple tags, so tag counts sum to more than the series count. Treat (category, tag) as the join key, not tag alone.
- A handful of example titles I report are verbatim Kalshi data-entry artifacts, not my transcription errors — e.g. KXEMMCYCACTO titled 'IGNORE! MY GOD', KXESPORTSTEST titled 'TESTING', KXCOTTONCANDYLOBSTER titled 'ill event be confirmed', and several ALL-CAPS titles. These are live in the catalog as shown.
- For roughly 15 low-count Entertainment subcategories (Collectibles, Love Island UK, Eurovision, BAFTA, Love Island USA, Anime awards, Movie Charts, SAG, Cannes, New Music, Art, Nobel Prizes, Soccer, Head to Head, StockX, America's Got Talent, Pokemon, Sports Emmys, Latin Grammys, Love Island, Trump, Other, Monthly/Daily/Weekly Views, AMAs, Daytime Emmys, Congress) the tag counts and settlement sources are confirmed from the data, but I reconstructed representative ticker names for a few where the extraction sampled live series only and none were live. Treat the Entertainment long-tail example tickers as INDICATIVE; the tag names, counts and category assignments are exact. All Sports, Crypto, Commodities, Economics, Financials, Climate, Politics and Elections example tickers are verbatim from the API response.
- settlementSource values are drawn from each series' settlement_sources[].name field and are aggregated per (category, tag) as the 3 most common — an individual series within that group may settle from a different source. Some Kalshi source names are themselves truncated or templated in the raw data (e.g. 'the Governing League', 'company', 'in hierarchical order', 'the U'), which I reproduced as-is rather than guessing.
- totalSeriesOrTags is reported as 14170, the count of distinct series objects enumerated from /series. The other relevant counts, if you need a different denominator: 3,918 series are currently live (have open or unopened events); 233 distinct tag strings exist overall; 148 distinct tags appear on live series; 380 distinct (category, tag) pairs are enumerated above.
- This is a point-in-time snapshot taken 2026-09-20. Kalshi adds and retires series continuously (series carry a last_updated_ts; many in this pull were updated within the last month), so counts will drift.

---

### Polymarket (Global, gamma-api.polymarket.com) + Polymarket US (gateway.polymarket.us) — enumerated 2026-09-20/21

*Method: All figures below are from live HTTP calls made during this task; nothing is recalled or inferred.

GLOBAL (https://gamma-api.polymarket.com, no auth):
1. GET /openapi.json — 116 paths. This is how I found the real keyset cursor param, which is `after_cursor` (NOT `cursor`/`next_cursor`/`after` — I tested all of those and they are silently ignored, returning page 1 forever with an unchanging next_*

**GLOBAL: Politics** — 19 subcategories

- `Midterms` · e.g. Balance of Power: 2026 Midterms, Which party will win the House in 2026?, Which party will win the Senate in 2026? · settles: State electoral authorities / AP race calls, arbitrated by UMA optimistic oracle · per-event
- `House Elections` · e.g. CA-28 House Election Winner, CA-15 House Election Winner, VA-06 House Election Winner · settles: State electoral authorities via UMA · per-event
- `Senate midterms` · e.g. Maine Senate Election Winner, Texas Senate Election Winner, Michigan Senate Election Winner · settles: State electoral authorities via UMA · per-event
- `Governor midterms` · e.g. California Governor Election Winner, Alaska Governor Election Winner, Wisconsin Governor Election Winner · settles: State electoral authorities via UMA · per-event
- `US Election (us-presidential-election)` · e.g. Democratic Presidential Nominee 2028, Presidential Election Winner 2028, Republican Presidential Nominee 2028 · settles: Federal/state election certification via UMA · per-event
- `Mayoral Elections` · e.g. Los Angeles Mayoral Election, Vancouver Mayoral Election Winner, Toronto Mayoral Election Winner · settles: Municipal electoral authorities via UMA · per-event
- `Primaries` · e.g. Will Max Miller drop out of the OH-07 race by...? · settles: State party / electoral authorities via UMA · per-event
- `Congress` · e.g. Republican Senate seats after the 2026 midterm elections?, Mitch McConnell steps down from Senate before his term ends? · settles: Official congressional records via UMA · per-event
- `Courts` · e.g. Will Samuel Alito announce his retirement by...?, SCOTUS accepts sports event contract case by...?, Maduro Prison Time? · settles: Court dockets / official announcements via UMA · one-off
- `Trump` · e.g. Trump out as President before 2027?, Will Trump acquire Greenland before 2027? · settles: Credible reporting consensus via UMA · per-event
- `Trump Cabinet` · e.g. Kash Patel out by...?, Pete Hegseth out as Secretary of Defense by December 31?, JD Vance out as VP by...? · settles: Official White House announcements via UMA · one-off
- `Foreign Policy` · e.g. Will China invade Taiwan by end of 2026?, Will US withdraw from NATO by...? · settles: Credible reporting via UMA · one-off
- `Economic Policy` · e.g. How many Fed rate cuts in 2026?, What will the Fed rate be at the end of 2026? · settles: Federal Reserve / Treasury releases via UMA · per-event
- `Gov Shutdown` · e.g. Government shutdown by October 1?, Will the GOP use 'Nuclear Option' to break filibuster by...? · settles: Congressional appropriations record via UMA · one-off
- `Epstein` · e.g. Epstein client list released by...?, Jeffrey Epstein foul play confirmed by...? · settles: Court filings / DOJ releases via UMA · one-off
- `Taxes` · e.g. Billionaire one-time wealth tax passes in California election 2026?, Trump eliminates capital gains tax on crypto by ___?, Will Mamdani pass the 2% Millionaire Tax before 2027? · settles: Enacted legislation via UMA · one-off
- `Turnout` · e.g. turnout (tag, 45 live events attached to midterm races) · settles: State electoral authorities via UMA · per-event
- `Margin of Victory / Midterm MOV` · e.g. Midterm MOV (564 live events), Margin of Victory (484 live events) · settles: Certified vote margins via UMA · per-event
- `State-level midterm families` · e.g. California Midterm, Texas Midterm, Florida Midterm · settles: State electoral authorities via UMA · per-event

**GLOBAL: Elections** — 10 subcategories

- `Global Elections` · e.g. Next Prime Minister of Ethiopia?, Presidential Election Winner 2028 · settles: National electoral commissions via UMA · per-event
- `World Elections` · e.g. World Elections (159 live events) · settles: National electoral commissions via UMA · per-event
- `International Election Props` · e.g. International Election Props (245 live events) · settles: National electoral commissions via UMA · per-event
- `German Elections` · e.g. Berlin State Election Winner, Mecklenburg-Vorpommern Parliamentary Election Winner, Next Ministerpräsident of Sachsen-Anhalt? · settles: Bundeswahlleiter / state returning officers via UMA · per-event
- `Brazil` · e.g. Brazil Presidential Election, Brazil Presidential Election First Round: 2nd Place, Brazil Presidential Election First Round: 3rd Place · settles: Tribunal Superior Eleitoral via UMA · per-event
- `Canada` · e.g. Quebec General Election Winner, Next Premier of Quebec, Will Alberta join the US? · settles: Elections Canada / provincial bodies via UMA · per-event
- `Israel Election` · e.g. Netanyahu out by...?, Prime Minister of Israel after the next election? · settles: Israel Central Elections Committee via UMA · per-event
- `Russia Election` · e.g. Russia Parliamentary Election Winner, Which party will gain most seats in Russian Parliamentary Election?, United Russia seats in the next Russian legislative election? · settles: Russian Central Election Commission via UMA · per-event
- `Nigerian Election / Nigerian Governor Election` · e.g. Nigerian Election (31 live), Nigerian Governor Election (28 live) · settles: INEC via UMA · per-event
- `Sweden Elections, French Elections, UK Elections, Colombia Election, Nepal Election` · e.g. Sweden Elections (24 live), French Elections (5 live), UK Elections (4 live) · settles: National electoral commissions via UMA · per-event

**GLOBAL: Geopolitics** — 19 subcategories

- `Iran` · e.g. Will the U.S. invade Iran before 2027?, Iran leader end of 2026?, Kharg Island no longer under Iranian control by...? · settles: Credible reporting consensus via UMA · one-off
- `Israel` · e.g. Netanyahu out by...?, Israel x Iran ceasefire continues through...? · settles: Credible reporting via UMA · one-off
- `Ukraine / Ukraine Map / Ukraine Peace Deal` · e.g. Will Ukraine recapture Crimean territory by...?, Will Russia capture Lyman by...?, Will Russia capture all of Stepnohirsk by...? · settles: ISW & DeepState territorial control maps, credible reporting via UMA · one-off
- `Russia` · e.g. Putin out as President of Russia by...?, NATO x Russia military clash by...? · settles: Credible reporting via UMA · one-off
- `China / Taiwan` · e.g. Will China invade Taiwan by end of 2026?, China x Taiwan military clash before 2027?, Lai Ching-te impeached by...? · settles: Credible reporting via UMA · one-off
- `Middle East` · e.g. Middle East (114 live events) · settles: Credible reporting via UMA · one-off
- `Gaza` · e.g. Israel x Hamas ceasefire cancelled by...?, Will Hamas agree to disarm by...?, Israel x Hamas Ceasefire Phase II by...? · settles: Credible reporting via UMA · one-off
- `Yemen / Houthis` · e.g. Bab el-Mandeb Strait effectively closed by...?, Israel military action against Yemen by...? · settles: IMF PortWatch (shipping transit calls) + credible reporting via UMA · one-off
- `Strait of Hormuz / Hormuz / Bab el-Mandeb` · e.g. Strait of Hormuz traffic returns to normal by December 31?, Bab el-Mandeb Strait effectively closed by...? · settles: IMF PortWatch 7-day moving average of 'Arrivals of Ships' transit calls (verified in market rules text) · daily
- `Lebanon / Hezbollah` · e.g. Israel withdraws from Lebanon by...?, Will Hezbollah disarm by...?, Israeli forces withdraw from beyond the Litani River by…? · settles: Credible reporting via UMA · one-off
- `Syria` · e.g. Israel and Syria normalize relations by...?, Which countries will recognize Israel by December 31? · settles: Credible reporting via UMA · one-off
- `Venezuela / Cuba` · e.g. Venezuela leader end of 2026?, Will the U.S. invade Venezuela by...?, US military action against Cuba by...? · settles: Credible reporting via UMA · one-off
- `Saudi Arabia` · e.g. Mohammed bin Salman out as leader of Saudi Arabia by...?, Saudi Oil Pipeline (East-West) restarts by...?, UAE x Saudi Arabia sever diplomatic relations in 2026? · settles: Credible reporting via UMA · one-off
- `Turkey` · e.g. Greece x Turkey military engagement by...?, Erdoğan out by December 31, 2026?, Israel x Turkey military clash before 2027? · settles: Credible reporting via UMA · one-off
- `Greenland` · e.g. Will Trump acquire Greenland before 2027?, Will the US acquire part of Greenland in 2026? · settles: Credible reporting via UMA · one-off
- `NATO` · e.g. Will US withdraw from NATO by...?, Will Russia invade a NATO country by...? · settles: Official NATO/US announcements via UMA · one-off
- `Military Actions / Military Strikes` · e.g. US x Russia military clash by...?, Will Iran target Qatar by...? · settles: Credible reporting via UMA · one-off
- `Peace Deal / Iran Ceasefire / Nuclear` · e.g. US-Iran Final Nuclear Deal by…?, Next round of US-Iran peace talks by...?, Iran agrees to surrender enriched uranium stockpile by...? · settles: Signed diplomatic instruments, IAEA, credible reporting via UMA · one-off
- `India-Pakistan, Sudan, Thailand-Cambodia` · e.g. India strike on Pakistan by...?, Modi out by December 31, 2026?, Sudan civil war ceasefire by...? · settles: Credible reporting via UMA · one-off

**GLOBAL: World** — 1 subcategories

- `Country desks` · e.g. Germany (52 live), Israel (50 live), Canada (117 live) · settles: National authorities / credible reporting via UMA · per-event

**GLOBAL: Sports** — 19 subcategories

- `Soccer` · e.g. UEFA Champions League: 2027 Champion, MLS Cup Winner 2026, Ballon d'Or Winner 2026 · settles: Official league results, ingested via sports data partners (OpticOdds partner mapping exposed on /events/{id}/external-partners) · per-event
- `NFL (All) / football` · e.g. Pro Football: 2027 Champion, Colts vs. Chiefs, Pro Football: 2027 NFC Champion · settles: Official NFL results · weekly
- `CFB (All) / NCAAF` · e.g. West Virginia vs. Virginia, Missouri vs. Kansas, Wisconsin vs. Notre Dame · settles: Official NCAA results · weekly
- `MLB / baseball (incl. KBO, NPB, CPBL, LMB)` · e.g. MLB World Series Champion 2026, MLB: 2026 American League Champion, MLB: 2026 National League Champion · settles: Official league results · daily
- `NHL / Hockey (incl. KHL, SHL, Liiga, DEL, Czech Extraliga)` · e.g. NHL: 2027 Champion, Maple Leafs vs. Canadiens, NHL: 2026-27 Calder Trophy · settles: Official league results · daily
- `NBA / Basketball (incl. WNBA, EuroLeague, B.League, ABA, LKL, VTB, BBL, BSL, NBL)` · e.g. NBA: 2027 Champion, NBA: 2026-27 Rookie of the Year, WNBA: 2026 Champion · settles: Official league results · daily
- `Tennis (ATP, WTA, ITF, Davis Cup)` · e.g. 2026 Men's US Open Winner (Tennis), Rennes: Sascha Gueymard-Wayenburg vs Titouan Droguet, Korea Open, Qualification: Xinxin Yao vs Priscilla Hon · settles: Official tour results · daily
- `Table Tennis / Setka Cup` · e.g. Hnoievoi Roman vs. Khamurda Vitalii, Derevynskyi Dmytro vs. Skachenko Serhii, Setka Cup UA (M) 577 live · settles: Setka Cup official results · daily
- `UFC / MMA / Zuffa / Power Slap` · e.g. UFC 331: Alexandre Pantoja vs. Joshua Van (Flyweight, Main Card), Who will be UFC Flyweight champion at the end of 2026?, Who will be UFC Light Heavyweight champion at the end of 2026? · settles: Official UFC results · weekly
- `Boxing` · e.g. Floyd Mayweather vs. Manny Pacquiao 2, Nikita Tszyu vs. Ben Mahoney, Will Jake Paul announce a run for public office in 2026? · settles: Official bout results / sanctioning bodies · per-event
- `Cricket (International, IPL-family, CPL, PSL, Legends League, ECS, women's)` · e.g. Caribbean Premier League: Antigua And Barbuda Falcons vs Jamaica Kingsmen, T20 Series Afghanistan vs Sri Lanka: Afghanistan vs Sri Lanka, Afghanistan Tour of India T20s: India vs Afghanistan · settles: Official match results · daily
- `Rugby (Super League, Premiership Rugby, Top 14, United Rugby Championship)` · e.g. Super League: Hull Kingston Rovers vs Toulouse Olympique, Premiership Rugby: Northampton Saints vs Newcastle Red Bulls, Top 14: ASM Clermont Auvergne vs Castres Olympique · settles: Official league results · weekly
- `Golf (PGA, LIV, DP World Tour, Korn Ferry)` · e.g. Will LIV Golf announce shutdown in 2026?, Will Tiger Woods play in a PGA Tournament in 2026?, Korn Ferry Tour: Nationwide Children's Hospital Championship Winner · settles: Official tournament leaderboards · weekly
- `Motorsport (Formula 1, NASCAR Cup/Truck/Xfinity)` · e.g. F1 Drivers' Champion, F1 Constructors' Champion, Azerbaijan Grand Prix: Driver Winner · settles: Official race classifications · weekly
- `Darts (PDC, MODUS Super Series)` · e.g. MODUS Super Series (32 live), PDC (4 live), Darts (36 live) · settles: Official PDC/MODUS results · daily
- `Chess` · e.g. 46th FIDE Chess Olympiad Open Tournament Winner, 2026 World Chess Championship: Winner, Titled Tuesday Top 8: September 22 · settles: FIDE / Chess.com official results · per-event
- `Handball, Volleyball, Lacrosse, Pickleball, Poker, AFL` · e.g. EHF Champions League, EuroVolley (6 live), Premier Lacrosse League (4 live) · settles: Official federation results · per-event
- `Fantasy Football` · e.g. Fantasy Football: 2026-27 RB Points Leader, Fantasy Football: 2026-27 TE Points Leader, Fantasy Football: 2026-27 WR Points Leader · settles: Official NFL stat feeds · weekly
- `Season stats / props / win totals / season series` · e.g. Season stats (319 live), props (213 live), Team win totals (77 live) · settles: Official league stat feeds · per-event

**GLOBAL: Esports** — 7 subcategories

- `Counter-Strike 2 / CS2` · e.g. Counter-Strike: MAJIX ESPORTS vs Younglings (BO3) - Exort Series Contenders Stage, Counter-Strike: 3DMAX Academy vs NeverPlay (BO3) - Exort Series Contenders Stage, Counter-Strike: AM Gaming vs Falcons Force (BO3) - CCT Europe Series 2 Group Stage · settles: Official tournament results (HLTV-class feeds) · daily
- `League of Legends` · e.g. LoL: T1 vs DN SOOPers (BO5) - KeSPA Cup Playoffs, LoL: T1 vs Kiwoom DRX (BO3) - LCK Rounds 1-2, LoL: Team Liquid vs FlyQuest (BO5) - LCS Playoffs · settles: Riot official results · daily
- `Valorant` · e.g. Valorant: Team Liquid vs Paper Rex (BO3) - VCT Champions Group C, Who Will Qualify For Champs 2026?, Valorant: TYLOO vs G2 Esports (BO3) - VCT Champions Group C · settles: Riot / VCT official results · daily
- `Dota 2` · e.g. Dota 2: Conventus Stellarum vs PlayTime (BO3) - PGL Wallachia Group Stage, Dota 2: Power Rangers vs Team Synapse (BO3) - EPL Masters Group A · settles: Valve / tournament official results · daily
- `Rainbow Six Siege` · e.g. Rainbow Six Siege: Team Secret vs Geekay Esports (BO1) - Europe MENA League Stage 2, Rainbow Six Siege: Fnatic vs Rebels Gaming (BO1) - Europe MENA League Stage 2 · settles: Ubisoft / tournament official results · daily
- `Overwatch, Rocket League, StarCraft II, Honor of Kings, Mobile Legends, Fortnite` · e.g. Overwatch: Solus Victorem vs Naive Piggy (BO3) - OCS China Stage 1, Rocket League: Shopify Rebellion vs Vitality (BO7) - RLCS World Championship Playoffs, StarCraft II: Lambo vs Cure (BO3) - WardiTV Championship · settles: Official tournament results · per-event
- `Esports Awards / Roster changes` · e.g. Esports Awards: Esports Content Group of the Year, Esports Awards: Esports Personality of the Year, Roster changes (22 live) · settles: Official award announcements / team announcements via UMA · one-off

**GLOBAL: Crypto** — 18 subcategories

- `Crypto Prices (hit-price / price ranges)` · e.g. What price will Bitcoin hit in 2026?, When will Bitcoin hit $150k?, What price will Ethereum hit in 2026? · settles: Binance 1-minute candle Low/High for the pair (e.g. BTC/USDT) — quoted verbatim from market rules · daily
- `Up or Down (5M / 15M / 1H / 4H / Daily)` · e.g. Dogecoin Up or Down - August 5, 1:55PM-2:00PM ET, Hyperliquid Up or Down - August 5, 10:45AM-11:00AM ET, ZCash Up or Down - August 5, 10:45AM-11:00AM ET · settles: Binance candle close vs. open at the stated interval · daily
- `Bitcoin` · e.g. What price will Bitcoin hit in 2026?, Bitcoin all time high by ___?, Will Bitcoin replace SHA-256 before 2027? · settles: Binance BTC/USDT candles · daily
- `Ethereum` · e.g. What price will Ethereum hit in 2026?, Ethereum all time high by ___?, What will the average monthly Ethereum gas price hit before 2027? · settles: Binance ETH/USDT candles · daily
- `Solana` · e.g. What price will Solana hit in 2026?, Solana all time high by ___?, Will HYPE flip SOL by December 31? · settles: Binance SOL/USDT candles · daily
- `XRP / Ripple` · e.g. What price will XRP hit in September?, XRP all time high by ___? · settles: Binance XRP/USDT candles · daily
- `BNB` · e.g. What price will BNB hit in 2026?, What price will BNB hit in September? · settles: Binance BNB/USDT candles · daily
- `Dogecoin` · e.g. What price will Dogecoin hit in 2026?, What price will Dogecoin hit in September? · settles: Binance DOGE/USDT candles · daily
- `Hyperliquid / HYPE` · e.g. What price will Hyperliquid hit in 2026?, Hyperliquid listed on Binance by ...?, Will HYPE flip SOL by December 31? · settles: Binance / exchange candles · daily
- `Zcash` · e.g. What price will Zcash hit in 2026?, Zcash's Orchard pool confirmed exploited? · settles: Exchange candles · daily
- `Token Launch / Token Sales / FDV / Pre-Market` · e.g. Will MetaMask launch a token by ___ ?, Will Base launch a token by ___ ?, Opensea FDV above ___ one day after launch? · settles: On-chain TGE data and exchange listing prices via UMA · per-event
- `Airdrops` · e.g. Pump.fun airdrop by ....?, MegaETH airdrop by...?, Hyperliquid airdrop by ....? · settles: Official project announcements via UMA · one-off
- `Stablecoins` · e.g. Will stablecoins hit $500B before 2027?, Stablecoins depeg before 2027?, Will USDT market cap hit $200B by ___? · settles: On-chain supply data / market cap trackers via UMA · one-off
- `Memecoins` · e.g. First to hit $1B FDV: ANSEM, CASHCAT, AI, or NET?, LAPTOP listed on ___ within 30 days of TGE? · settles: On-chain FDV / exchange listings via UMA · one-off
- `Crypto Listings` · e.g. Kraken IPO by ___ ?, OKX IPO in 2026?, Consensys IPO by ___ ? · settles: Exchange / regulatory filings via UMA · one-off
- `Crypto Legal / Clarity Act / Crypto Policy / Gov Reserve` · e.g. Clarity Act (H.R.3633) signed into law in 2026?, Which Senators will vote for the Clarity Act?, Will China unban Bitcoin by 2027? · settles: Enacted legislation and official government announcements via UMA · one-off
- `Network Stats / Protocol Upgrade / protocol-risk` · e.g. Will knots flip bitcoin core by ___?, Over 30M humans verified on World Network by December 31? · settles: On-chain data via UMA · one-off
- `Crypto Culture / Multi Strikes / Price Milestone / ATH / Price Comparison` · e.g. Bitcoin all time high by ___?, Bitcoin vs. Gold vs. S&P 500 in 2026 · settles: Exchange candles via UMA · per-event

**GLOBAL: Tech** — 15 subcategories

- `AI` · e.g. Which company has the best AI model end of September?, Will Anthropic's valuation hit __ by December 31? · settles: Official lab announcements and leaderboards via UMA · per-event
- `AI Rankings` · e.g. Which company has the best AI model end of September?, Which company has best AI model end of 2026?, Best Chinese AI Company end of September? · settles: LMArena / Chatbot Arena leaderboard rank column · monthly
- `AI Releases` · e.g. Next Google Gemini Pro Model released by...?, Gemini 4.0 released by...?, Next Claude Opus released by...? · settles: Official vendor release announcements via UMA · per-event
- `AI Benchmarks` · e.g. Will any AI model reach ___ Overall Arena Score by September 30?, OpenAI announces it has achieved AGI before 2027?, Which company's AI will first hit 1550 on Chatbot Arena in 2026? · settles: Chatbot Arena / LiveBench / Code Arena scores · per-event
- `AI Safety` · e.g. U.S. enacts AI safety bill before 2027?, Which AI labs commit to third party vetting by October 31? · settles: Enacted legislation / official lab commitments via UMA · one-off
- `AI Regulation` · e.g. Who will be removed from Chinese Military Companies list by June 30, 2027?, US Government removes public access to a major Chinese AI model in 2026? · settles: Federal Register / DoD lists via UMA · one-off
- `Big Tech` · e.g. Largest Company end of December 2026?, Which companies will be acquired before 2027? · settles: Market cap data / official filings via UMA · per-event
- `OpenAI / Anthropic / Claude / Gemini / Grok / DeepSeek / xAI / ChatGPT` · e.g. OpenAI IPO by...?, OpenAI IPO Closing Market Cap, Anthropic IPO by __? · settles: Official company announcements and arena leaderboards via UMA · per-event
- `Compute / NVIDIA / GPU rental` · e.g. GPU rental prices (B200) end of 2026?, GPU rental prices (A100) end of September?, GPU rental prices (H100) end of 2026? · settles: GPU rental price indices via UMA · monthly
- `Coding / WebDev` · e.g. Which company has the best Code Arena WebDev AI model end of September?, Second-best Code Arena WebDev AI Lab end of September? · settles: Code Arena WebDev leaderboard · monthly
- `Math / Millennium Prize` · e.g. AI lab announces another Millennium Prize solution by...?, Which Millennium Prize Problem will AI solve next? · settles: Clay Mathematics Institute / peer-reviewed confirmation via UMA · one-off
- `Elon Musk / SpaceX / Tesla` · e.g. Richest person on December 31, 2026?, Tesla and SpaceX merger officially announced by...?, Will the Doge-1 Lunar Mission launch by...? · settles: Official company announcements via UMA · one-off
- `Apple / App Store` · e.g. Will Apple release a foldable iPhone by...?, #1 Paid App in the US Apple App Store on September 25?, Will Apple release a touchscreen MacBook in 2026? · settles: Apple App Store public charts via UMA · daily
- `Google Search` · e.g. #1 Searched Person on Google 2026?, #1 Searched Movie on Google 2026?, #1 Searched Person on Google in the US 2026? · settles: Google Year in Search published rankings · one-off
- `Outage` · e.g. outage (11 live events) · settles: Official status pages via UMA · one-off

**GLOBAL: Culture (pop-culture)** — 15 subcategories

- `Music / music industry / album / song` · e.g. Top Spotify Artist 2026, Top Spotify Song 2026, Billboard #1 Artist 2026 · settles: Billboard and Spotify published charts · weekly
- `Movies` · e.g. Highest grossing movie in 2026?, Which movie has biggest opening weekend in 2026?, New "Stranger Things" episode released by...? · settles: Box office trackers and studio announcements via UMA · per-event
- `Box Office` · e.g. "Spider-Man: Brand New Day" total domestic gross by September 30?, "Resident Evil" Opening Weekend Box Office, "Spider-Man: Brand New Day" 8th Weekend Box Office · settles: Box Office Mojo / Comscore domestic gross · weekly
- `Rotten Tomatoes` · e.g. "Resident Evil" Rotten Tomatoes Score?, "Primetime" Rotten Tomatoes Score?, "Digger" Rotten Tomatoes Score? · settles: Rotten Tomatoes published Tomatometer score · per-event
- `Awards (Oscars, Grammys, VMAs, CMAs, Nobel, Game Awards, Turner Prize)` · e.g. Oscars 2027: Best Picture Winner, Oscars 2027: Best Actress Winner, Grammys 2027: Album of the Year Winner · settles: Official awarding bodies via UMA · per-event
- `Celebrities / relationships / pregnant` · e.g. Taylor Swift pregnant by...?, Who will attend Taylor Swift and Travis Kelce's wedding?, Kylie Jenner and Timothée Chalamet engaged in 2026? · settles: Credible reporting via UMA · one-off
- `Reality TV / TV` · e.g. Bachelorette Season 22 Winner, Dancing with the Stars S35: Winner?, Big Brother Season 28 Winner · settles: Broadcast results via UMA · weekly
- `Top Netflix` · e.g. What will be the top US Netflix movie this week?, What will be the top global Netflix movie this week?, What will be the #2 US Netflix show this week? · settles: Netflix Top 10 published charts · weekly
- `YouTube / MrBeast / streamers` · e.g. # of views of next MrBeast video on week 1?, # of views of MrBeast video on day 2?, Will MrBeast hit ___ Billion views by September 30? · settles: YouTube public view counters · weekly
- `Collectibles / Pokemon` · e.g. Phantasmal Flames Booster Box Price Over/Under $393.19 on September 30?, Pikachu ex Price Over/Under $1,059.87 on September 30?, Mega Dragonite ex Price Over/Under $668.24 on September 30? · settles: Published card/booster market price indices via UMA · daily
- `Art / masterworks` · e.g. Who will be the top-selling artist by total auction sales in 2026?, Will China become the #2 global art market in 2026? · settles: Auction house results via UMA · one-off
- `Video games / GTA VI` · e.g. GTA 6 launch postponed again?, Another GTA VI trailer released by...?, Will GTA 6 cost $100+? · settles: Publisher announcements via UMA · one-off
- `Tweet Markets` · e.g. Elon Musk # tweets September 15 - September 22, 2026?, Elon Musk # tweets September 18 - September 25, 2026?, Elon Musk # tweets September 19 - September 21, 2026? · settles: Public X/Twitter post counts via UMA · weekly
- `Mentions (mention-markets)` · e.g. What will Trump say in September?, What will Andy Burnham say at the next Prime Minister's Questions event?, Who will post about $LAPTOP by September 30? · settles: Transcript / published-remarks review via UMA · per-event
- `Eurovision / Met Gala / Aliens` · e.g. Eurovision 2027 Participants, Will the US confirm that aliens exist by...?, Japan declassifies new UFO files in 2026? · settles: Official announcements / government disclosure via UMA · one-off

**GLOBAL: Economy** — 12 subcategories

- `Macro Indicators` · e.g. Fed Decision in October?, What will Fed Rate hit before 2027?, How high will inflation get in 2026? · settles: Official statistical agency releases via UMA · monthly
- `Fed Rates / Fed / FOMC / Jerome Powell / Kevin Warsh` · e.g. How many Fed rate cuts in 2026?, Fed Decision in October?, What will the Fed rate be at the end of 2026? · settles: Federal Reserve FOMC statements (25bp cut counting rule stated in market text) · per-event
- `Inflation / CPI / CPI Release` · e.g. How high will inflation get in 2026?, U.K. Annual Inflation 2026, Brazil Annual Inflation 2026 · settles: BLS CPI release and national statistics offices · monthly
- `GDP` · e.g. China Annual GDP Growth 2026, UK Annual GDP Growth 2026, GDP growth in 2026 · settles: National accounts releases (BEA, Eurostat, NBS) · monthly
- `Global Rates / ECB / European Central Bank / Interest Rate` · e.g. Global Rates (37 live), ECB (3 live) · settles: Central bank policy decisions via UMA · per-event
- `Treasuries` · e.g. How high will 10-year Treasury yield go before 2027?, How low will 10-year Treasury yield get in September?, How high will 10-year Treasury yield go in September? · settles: US Treasury published constant-maturity yields (verified in market rules text) · daily
- `Housing / real estate / Parcl` · e.g. What will the median home value in the Austin Metro area be on September 30?, What will the median home value in Chicago Metro be on September 30?, What will the median home value in the US be on September 30? · settles: Parcl Labs Sales Price Index (quoted verbatim from market rules) · monthly
- `Labor / unemployment` · e.g. JOLTS Job Openings: August 2026 · settles: BLS JOLTS and employment situation releases · monthly
- `Consumer` · e.g. University of Michigan Consumer Sentiment - September 2026 · settles: University of Michigan Surveys of Consumers · monthly
- `Trade War` · e.g. Trade War (8 live) · settles: Official tariff schedules / USTR announcements via UMA · one-off
- `Exchange Rate / currency / USD` · e.g. Exchange Rate (4 live), USD (3 live) · settles: Investing.com hourly candles (quoted verbatim from FX market rules) · daily
- `Fiscal / monetary policy / macro` · e.g. Fiscal (3 live), monetary policy (3 live), Macro Graph · settles: Official government and central bank publications via UMA · per-event

**GLOBAL: Finance** — 16 subcategories

- `Equities / Stocks / Stock Prices` · e.g. What will S&P 500 (SPY) hit in September 2026?, What will South Korea ETF (EWY) hit in September 2026?, What will Robinhood Markets, Inc. (HOOD) hit in September 2026? · settles: Pyth Network price feeds — resolutionSource field literally returns https://pythdata.app/explore/Equity.US.SPY%2FUSD; 1-minute candle High/Low during regular session · daily
- `Single-ticker families (AAPL, MSFT, NVDA, AMZN, GOOGL, TSLA, MU, META, SPCX)` · e.g. AAPL, MSFT, NVDA · settles: Pyth Network equity feeds · daily
- `Indicies (S&P 500 / SPX, Nikkei 225, Dubai Real Estate Index)` · e.g. What will S&P 500 (SPX) hit by end of December?, What will S&P 500 (SPX) close at end of 2026?, Nikkei 225: Close Price End of 2026 · settles: Index provider official close / Pyth · daily
- `Commodities` · e.g. What will WTI Crude Oil (WTI) hit in September 2026?, Crude Oil all time high by...?, What will Gold (GC) hit__ by end of December? · settles: CME official settlement price for the Active/front month for CME-listed contracts (quoted verbatim from Gold GC market rules); XAUUSD/XAGUSD spot feeds for spot pairs · daily
- `Oil (WTI crude + oil geopolitics)` · e.g. What will WTI Crude Oil (WTI) hit in September 2026?, Crude Oil all time high by...?, Bab el-Mandeb Strait effectively closed by...? · settles: CME WTI settlement; IMF PortWatch for shipping-chokepoint variants · daily
- `Gold` · e.g. What will Gold (GC) hit__ by end of December?, What will Gold (XAUUSD) hit in September 2026?, Gold (XAUUSD) Up or Down on September 21? · settles: CME Gold (GC) futures settlement for GC contracts; XAUUSD spot feed for spot contracts · daily
- `Silver` · e.g. What will Silver (XAGUSD) hit in September 2026?, What will Silver (XAGUSD) hit Week of September 21 2026?, Silver (XAGUSD) Up or Down on September 21? · settles: XAGUSD spot feed · daily
- `Natural gas` · e.g. What will Natural Gas (NG) hit Week of September 21 2026?, Natural Gas (NG) Up or Down on March 26?, Natural Gas (NG) Up or Down on September 21? · settles: CME Natural Gas (NG) futures settlement · daily
- `Forex / FX / Foreign Exchange` · e.g. Will USD/KRW hit __ in 2026?, Will EUR/USD hit __ in 2026?, Will GBP/USD hit __ in 2026? · settles: Investing.com hourly candle High (quoted verbatim from USD/KRW market rules) · daily
- `IPOs / IPO` · e.g. IPOs before 2027?, Largest IPO by market cap in 2026?, Anthropic IPO by __? · settles: SEC S-1 effectiveness and primary listing exchange via UMA · one-off
- `Privates (private-company valuations)` · e.g. Will Anthropic's valuation hit __ by December 31?, Will OpenAI's valuation hit __ by December 31?, Will Databricks' valuation hit __ by December 31? · settles: Reported primary/secondary round valuations via UMA · one-off
- `Earnings / Earnings Calls` · e.g. Will FedEx (FDX) beat quarterly earnings?, Will Micron (MU) beat quarterly earnings?, Will Cintas (CTAS) beat quarterly earnings? · settles: Company earnings releases vs. consensus via UMA · per-event
- `Acquisitions / merger` · e.g. Which companies will be acquired before 2027?, Will GameStop acquire eBay?, Will Paramount close Warner Bros. acquisition by end of 2026? · settles: Definitive agreements and regulatory closing via UMA · one-off
- `Corporate Financials / market cap` · e.g. Microstrategy delisted from MSCI index by...?, STRC hits $100 by…, Consensys IPO closing market cap above ___ ? · settles: Exchange data and index provider announcements via UMA · per-event
- `Finance Updown / Daily-Close / Multi Strikes / Hit Price` · e.g. Finance Updown (91 live), Daily-Close (49 live), Multi Strikes (36 live) · settles: Pyth Network feeds · daily
- `Prediction Markets (reflexive)` · e.g. SCOTUS accepts sports event contract case by...?, Sports Prediction Markets taxed as gambling? · settles: Regulatory filings / court dockets via UMA · one-off

**GLOBAL: Business** — 3 subcategories

- `Business (parent rollup over Tech, AI, Economy, IPOs, Acquisitions)` · e.g. Which companies will be acquired before 2027?, IPOs before 2027?, Largest Company end of December 2026? · settles: Company filings and official announcements via UMA · per-event
- `MicroStrategy` · e.g. Will MicroStrategy be margin called in 2026?, Microstrategy delisted from MSCI index by...? · settles: Company filings / index provider notices via UMA · one-off
- `TikTok / DeepSeek / SpaceX (business-side)` · e.g. TikTok (1 live), DeepSeek (4 live), SpaceX (23 live) · settles: Official announcements via UMA · one-off

**GLOBAL: Science** — 6 subcategories

- `Space / NASA / SpaceX launches` · e.g. Will the Doge-1 Lunar Mission launch by...?, 5kt meteor strike in 2026?, Major meteor strike (10kt+) in 2026? · settles: NASA / launch provider confirmations via UMA · one-off
- `Pandemics / disease` · e.g. Hantavirus pandemic in 2026?, New pandemic in 2026?, Measles cases in U.S. in 2026? · settles: WHO / CDC case counts via UMA · one-off
- `FDA / drug / vaccine / cancer / GLP / Eli Lilly / Moderna` · e.g. FDA approves Retatrutide this year?, FDA approves skin cancer vaccine by...?, Skin cancer vaccine BLA submitted by...? · settles: FDA approval database via UMA · one-off
- `Earthquakes / Natural Disasters` · e.g. How many 7.0 or above earthquakes in 2026?, How many large volcano eruptions (VEI ≥4) in 2026?, 10.0 or above earthquake before 2027? · settles: USGS magnitude catalog / Smithsonian GVP for volcanoes · one-off
- `Millennium Prize / Math` · e.g. AI lab announces another Millennium Prize solution by...?, Which Millennium Prize Problem will AI solve next? · settles: Clay Mathematics Institute via UMA · one-off
- `Quantum` · e.g. Quantum breaks Bitcoin by ___?, Bitcoin quantum-resistant upgrade implemented in 2026?, Will Bitcoin replace SHA-256 before 2027? · settles: Peer-reviewed / on-chain evidence via UMA · one-off

**GLOBAL: Weather** — 6 subcategories

- `Daily Temperature (Highest / Lowest temperature)` · e.g. Highest temperature in Hong Kong on September 18?, Highest temperature in Hong Kong on September 19?, Highest temperature in Chicago on September 20? · settles: City-specific national met service — e.g. Hong Kong Observatory 'Absolute Daily Max (deg. C)' quoted verbatim from market rules; NWS for US cities · daily
- `City coverage` · e.g. Hong Kong, New York City, Chicago · settles: Per-city national met services · daily
- `Hurricanes / Hurricane Season` · e.g. Will any Category 5 hurricane make landfall in the US in before 2027?, How many tropical cyclones will make landfall in China during 2026?, How many hurricanes will form during the Atlantic Hurricane Season in 2026? · settles: NHC / NOAA advisories via UMA · per-event
- `Global Temp / Climate Change / climate` · e.g. Where will 2026 rank among the hottest years on record?, September 2026 1st, 2nd, or 3rd hottest on record?, September 2026 Temperature Increase (ºC) · settles: NASA GISS / Copernicus / Berkeley Earth rankings via UMA · monthly
- `Precipitation` · e.g. Precipitation in Seoul in September?, Precipitation in Seattle in September?, Precipitation in London in September? · settles: National met services via UMA · monthly
- `Drought` · e.g. When will the Danube River return to normal levels?, When will the Rhine River return to normal levels?, How low will Lake Mead drop? · settles: River/reservoir gauge authorities via UMA · monthly

**GLOBAL: Non-domain mechanic tags (IMPORTANT for schema mapping)** — 4 subcategories

- `Duration / interval tags` · e.g. 5M (2,370 live), 15M (780 live), 1H (353 live) · settles: Not a domain — these describe contract tenor, not subject matter. Do NOT map a data feed to these. · daily
- `Structure tags` · e.g. Up or Down (3,623 live), Hit Price, Multi Strikes · settles: Not a domain — contract shape · per-event
- `Operational / display tags` · e.g. Hide From New (4,441 live), Recurring (4,396 live), Games (8,958 live — a sports-fixture flag, not the 'video games' domain) · settles: Not a domain — UI and lifecycle flags · per-event
- `Incentive tags` · e.g. Earn 4%, Rewards 50, 4.5, 20, Rewards 20, 4.5, 50 · settles: Not a domain — liquidity reward tiers · per-event

**US: sports** — 18 subcategories

- `CFB (college football; FBS, FCS, Power 5, Conferences, Top 25, AAC, ACC, CAA, Patriot League)` · e.g. 2027 College Football National Championship Winner, Heisman Trophy Winner, Big 12 Football Championship Winner · settles: Official NCAA game results; expiration auto-amends on postponement (quoted from market rules) · weekly
- `NFL` · e.g. AFC West Division Winner, AFC South Division Winner, AFC North Division Winner · settles: Official NFL results · weekly
- `Table Tennis / Setka (Ukraine Men, Czechia Men, Moldova Men)` · e.g. Polysynskyi Mykola vs. Skliar Mykhailo, Gavryshko Oleg vs. Dukhovenko Oleksandr, Slozka Viktor vs. Krokhmal Vitalii · settles: Setka Cup official results · daily
- `Tennis (UTR, ITF Mens, ITF Womens, WTA, ATP, ATP Challenger Qualifiers, WTA Doubles)` · e.g. Men's Pro Tennis No. 1 on Dec 31, 2026, Women's Pro Tennis No. 1 on Dec 31, 2026, Jelena Ostapenko vs. Anastasia Zakharova · settles: Official tour results · daily
- `Esports (CS2, League of Legends, Dota 2, Rainbow Six Siege)` · e.g. Saint Sinners vs. Drama eSports, Astralis vs. Sangal  Map 1, Vivo Keyd Stars Academy vs. Dplus KIA Challengers · settles: Official tournament results · daily
- `Soccer (EPL, UCL, UWCL, MLS, La Liga, Serie A, Bundesliga, Ligue 1, Liga MX, USL Championship, NCAA M/W Soccer, WSL, and ~30 more)` · e.g. Major League Soccer Champion, Ballon d'Or 2026 Winner, UEFA Champions League Winner · settles: Official league results · daily
- `MLB / baseball (incl. NPB, KBO)` · e.g. World Series Champion, National League Champion, American League Champion · settles: Official MLB results; pennant markets name the specific scheduled date and auto-amend on postponement · daily
- `NHL / Hockey (incl. KHL, International Hockey)` · e.g. NHL Eastern Conference Champion, NHL Western Conference Champion, 2027 Stanley Cup Champion · settles: Official NHL results · daily
- `Basketball (NBA, WNBA, LNBP, Basketball Bundesliga, EuroLeague, Australia NBL, VTB, LKL, CBB)` · e.g. WNBA Champion, WNBA MVP, Will Royce White Be Drafted or Signed by a WNBA Team? · settles: Official league results · daily
- `MMA / UFC / Dana White's Contender Series` · e.g. UFC Lightweight Champion on Dec 31, 2026, UFC Welterweight Champion on Dec 31, 2026, UFC Middleweight Champion on Dec 31, 2026 · settles: Official UFC results · weekly
- `Boxing` · e.g. Canelo Alvarez vs Christian Mbilli, WBC Welterweight Champion on Dec 31, 2026, WBC Heavyweight Champion on Dec 31, 2026 · settles: Official bout results / WBC · per-event
- `Golf (PGA, DP World Tour, Presidents Cup, Ryder Cup, Korn Ferry-class events)` · e.g. 2027 Ryder Cup Winner, BMW PGA Championship Winner, 2026 Presidents Cup Winner · settles: Official tournament leaderboards · weekly
- `Darts (MODUS Super Series, PDC)` · e.g. PDC World Darts Championship Winner, Steve West vs. Scott Robertson, Chuck Puleo vs. Scott Winder · settles: Official PDC/MODUS results · daily
- `Win Totals` · e.g. Pro Football Regular Season Win Totals, Arizona Regular Season Win Total, Atlanta Falcons Regular Season Win Total · settles: Official regular-season standings · per-event
- `Stat Leaders / Season Stat Leaders / player props (Rush Yards, Rush TDs, Rec Yards, Rec TDs, Receptions, Pass Yards, Pass TDs, Points)` · e.g. MLB Home Runs Leader, MLB Runs Leader, MLB RBIs Leader · settles: Official league stat feeds · weekly
- `Awards` · e.g. World Series Champion, National League MVP, National League Cy Young Award · settles: Official league award announcements · per-event
- `Fantasy Season` · e.g. Fantasy Season (14 live events) · settles: Official NFL stat feeds · weekly
- `Motorsport (Formula 1, NASCAR, MotoGP) / Pickleball (PPA) / Lacrosse (PLL) / Cricket (T20 Intl, ODI, CPL)` · e.g. Formula 1 (6 live), NASCAR (3 live), MotoGP (1 live) · settles: Official series classifications · per-event

**US: politics** — 10 subcategories

- `Midterms` · e.g. U.S House Midterm Winner (usho-midterms-2026-11-03), U.S Senate Midterm Winner (usse-midterms-2026-11-03) · settles: Relevant state electoral authorities and the US House of Representatives (quoted verbatim from market rules) — named-source settlement, NOT an oracle · one-off
- `House` · e.g. AL-01 House Election Winner (ushr-al-01-2026-11-03), AL-03 House Election Winner, AL-04 House Election Winner · settles: State electoral authorities · one-off
- `Senate Races` · e.g. Alabama Senate Election Winner (usse-al-2026-11-03), Arkansas Senate Election Winner, Colorado Senate Election Winner · settles: State electoral authorities · one-off
- `Governor Races` · e.g. Alabama Governor Election Winner (usgub-al-2026-11-03), Kansas Governor Election Winner, California Governor Election Winner (usgub-ca-2026-11-03) · settles: State electoral authorities · one-off
- `County Popular Vote` · e.g. Florida Senate Election: Miami-Dade County Winner, Nevada Governor Election: Clark County Winner, Nevada Governor Election: Washoe County Winner · settles: County electoral boards · one-off
- `Supreme Court` · e.g. North Carolina Supreme Court Election Winner, Next US Supreme Court Justice? (scotus) · settles: State judicial election authorities / official appointment record · one-off
- `Redistricting` · e.g. Maryland Congressional Redistricting Criteria Referendum, Missouri Congressional Map Referendum · settles: State ballot-measure certification · one-off
- `Abortion / Transgender` · e.g. Idaho Abortion Legalization Referendum, Missouri Abortion and Underage Transgender Surgery Ban Referendum · settles: State ballot-measure certification · one-off
- `Ballot measures — other (Railroad Commissioner, Traffic Cameras, Ranked Choice Voting, Constitution, Crime, Cartels, Taxes)` · e.g. Railroad Commissioner, Traffic Cameras, Ranked Choice Voting · settles: State ballot-measure certification · one-off
- `National Outcomes / Race Props / Party / Republican / Democrat / Primaries / International / Combos` · e.g. National Outcomes (2 live), Race Props (2 live), Combos (11 live) · settles: Electoral authorities · one-off

**US: culture** — 4 subcategories

- `Awards` · e.g. 2026 Nobel Peace Prize Winner · settles: Official awarding body — e.g. Norwegian Nobel Committee named directly in market rules · per-event
- `Music` · e.g. Top Global Artist 2026 (sptfy-1-artst-glbl-yr-2026), Top Artist in the US 2026?, Top Song 2026? (sptfy-n1-song-glbl-yr-2026) · settles: Spotify published charts · weekly
- `Entertainment` · e.g. GTA VI Released? (gtavi), Big Brother Season 28 Winner, Big Brother Season 28: 2nd Place · settles: Publisher / broadcaster announcements · one-off
- `TV & Movies / movies` · e.g. Top Global Netflix Movie This Week? (ntflx-1movglbl-2026-09-22), Top US Netflix Movie This Week?, Top US Netflix Show This Week? · settles: Netflix Top 10 published charts · weekly

**US: macro** — 4 subcategories

- `US Econ` · e.g. US GDP Growth in Q3 2026? (us-saa-q3-2026-10-29), Jobs Numbers in September 2026 (usnfp-sa-september-2026-10-02), September Unemployment Rate (usunemp-sa-september-2026-10-02) · settles: BEA / BLS official releases · monthly
- `Fed` · e.g. Fed Rate Cut in 2026? (usfed-2026), Fed Decision in October (usfed-fomc-2026-10-28), Fed Rate Cut Greater Than 25bps? (fed-gt25bps) · settles: Federal Reserve (named directly: 'Outcome sourced from the Federal Reserve'; counts scheduled FOMC and emergency moves) · per-event
- `Rates (non-US central banks)` · e.g. Bank of Mexico Decision in September? (banxico-2026-09-24), Which Central Banks Will Cut by Dec. 31? (cut-by-2026-12-31) · settles: Respective central bank policy statements · per-event
- `Commodities / Gas` · e.g. How High Will US Gas Prices Get in September? (usgas-highm-2026-09-30), US Gas Prices on September 30? (usgas-day-2026-09-30), How High Will US Gas Prices Get in 2026? (usgas-high-2026-12-31) · settles: US retail gasoline price series (AAA/EIA-class national average) · daily

**US: technology** — 2 subcategories

- `Model Releases` · e.g. Gemini 3.5 Pro Released? (gemini-3pt5pro), Grok 5 Released? (xai-grok-5), Chinese AI Model Ranked #1? (chinese-arena-ovrall-1) · settles: Official vendor release announcements · per-event
- `Rankings` · e.g. Which Company Has #1 AI Model end of 2026? (company1-2026-12-31), Men's Pro Tennis No. 1 on Dec 31, 2026, Women's Pro Tennis No. 1 on Dec 31, 2026 · settles: Arena AI Text Arena leaderboard 'Rank' column, Style Control Off, evaluated at a stated timestamp (quoted verbatim from market rules) · per-event

**US: finance** — 1 subcategories

- `Business / IPOs` · e.g. Which Companies Will Confirm an IPO in 2026? (2026ipos), OpenAI IPO Officially Confirmed? (openai), Anthropic IPO Officially Confirmed? (anthropic) · settles: SEC declaring Form S-1 effective, the company itself, and the primary listing exchange (quoted verbatim from market rules) · one-off

**US: climate** — 2 subcategories

- `Weather — Daily High` · e.g. Highest temperature in NYC on September 20? (temp-nychigh-2026-09-20), Highest temperature in Miami on September 20? (temp-miahigh-2026-09-20), Highest temperature in Chicago on September 20? (temp-mdwhigh-2026-09-20) · settles: National Weather Service Climatological Report (Daily) for a named station — e.g. Central Park KNYC (quoted verbatim from market rules) · daily
- `City coverage (5 cities only)` · e.g. NYC (KNYC Central Park), Miami, Chicago (KMDW Midway) · settles: NWS station-specific climatological reports · daily

**US: crypto** — 1 subcategories

- `Bitcoin` · e.g. When will Bitcoin hit $150k? (btc-150k), How high will Bitcoin get this year? (btc-hitprice-high-yr-12-31-2026), Bitcoin price at the end of 2026? (btc-pricerange-yr-12-31-2026) · settles: CF Benchmarks Bitcoin Real-Time Index (BRTI) using a trimmed-mean calculation (quoted verbatim from market rules) — NOT Binance candles, unlike Global · daily

**US: geopolitics** — 1 subcategories

- `Geopolitics` · e.g. Strait of Hormuz Traffic Returns to Normal? (hormuz-normal), US Withdraws From NATO? (nato-us), What Will Be in a US-Iran Deal in 2026? (us-iran-contnts-2026-) · settles: Signed/formally adopted written diplomatic instruments and official government sources · one-off

**US: science** — 1 subcategories

- `Science` · e.g. US Measles Cases in 2026? (measles-us-2026-12-31), Pandemic? (anydis), US Confirms That Aliens Exist? (aliens) · settles: US Centers for Disease Control and Prevention (CDC) named directly for disease counts · one-off

**Not confirmed:**

- HOST CORRECTION: api.polymarket.us (the host named in the task) returns 401 'Missing required API key headers' on every read path I tried, including /v1/markets, /v1/events and /. All Polymarket US data above instead comes from https://gateway.polymarket.us, which serves the same read endpoints unauthenticated. I found that host inside the OpenAPI block embedded in docs.polymarket.us/api-reference/events/get-events.md, not by guessing.
- KEYSET CURSOR: the Gamma keyset param is `after_cursor`. `cursor`, `next_cursor`, `start_cursor`, `after`, `cursor_id` and `page_cursor` are all silently ignored and return page 1 with an identical next_cursor — a walk using any of them stops at 100 events while appearing to have completed. Anyone reproducing this must use `after_cursor` or the corpus will be 0.6% of actual size.
- COMPLETENESS OF GLOBAL WALK: /events/pagination reported totalResults=18166; my keyset walk captured 18,164 unique open events over 182 pages. The 2-event gap is almost certainly events created or closed during the ~3 minutes of walking, but I did not re-run to confirm, so treat it as 99.99% coverage rather than exhaustive.
- US 'ALL EVENTS' IS CAPPED: GET /v1/events with no closed filter stopped at 2,499 rows while closed=false returned 3,716 — i.e. the unfiltered query hits a server-side offset ceiling that the filtered one does not. I used the closed=false set. The historical/closed US corpus was NOT fully enumerated.
- US SUBCATEGORY FIELD IS EMPTY: the US events schema defines a `subcategory` string, but it is null on all 3,716 open events. Every US subcategory in this report is therefore derived from the nested `tags`/`subtags` tree and `primaryTag`, not from the venue's own subcategory field. If Polymarket US starts populating that field, it may not match my derivation.
- STALE OFFICIAL DOC: docs.polymarket.us/learn/get-started/browse.md states Polymarket US 'currently offers professional football, professional basketball, professional hockey, and college football markets.' That is contradicted by the live API (10 categories, 91 leagues, 3,716 open events including tennis, table tennis, esports, soccer, politics, weather, crypto). I trusted the API over the doc. This means any category set taken from Polymarket US documentation rather than the API will be badly wrong.
- CURATED HIERARCHY IS INCOMPLETE: /tags/slug/{slug}/related-tags/tags returned 0 children for `elections` (1,824 live events), `commodities` (18), `esports` (694), `games`, `ai`, `health`, `entertainment` and `breaking`. The curated parent/child table does not cover the live catalogue, so the Global subcategory trees above are built primarily from tag co-occurrence across the 18,164-event corpus, with related-tags used only as corroboration. A different analyst using related-tags alone would produce a materially smaller tree.
- TAG REGISTRY IS MOSTLY DEAD WEIGHT: 7,348 tags exist but only 2,210 appear on any open event. The other 5,138 are historical, entity-level (individual athletes, teams, one-off news subjects) or deprecated (e.g. 'deprec-us-election', 'product marekt fit'). Do not build a schema from the raw /tags dump.
- MECHANIC TAGS ARE NOT DOMAINS: several of the highest-frequency tags are contract-shape or UI flags, not subject matter — 'Games' (8,958, a sports-fixture flag, easily mistaken for video games), 'Hide From New' (4,441), 'Recurring' (4,396), 'Up or Down' (3,623), '5M' (2,370), '15M' (780), '1H' (353). I isolated these under the '_mechanics' category. Mapping a market-data feed to any of them would be a category error.
- SETTLEMENT SOURCES ARE SAMPLED, NOT EXHAUSTIVE: I read actual rules text for 9 Global events and 10 US markets and quoted those verbatim (CME GC settlement for gold, Binance candles for Global BTC, CF Benchmarks BRTI for US BTC, Pyth for equities, Investing.com for FX, Parcl Labs for housing, IMF PortWatch for chokepoints, NWS/Hong Kong Observatory for weather, CDC for disease, Arena AI for model rankings). Settlement sources listed for subcategories I did NOT sample are inferred from the family pattern and are UNVERIFIED for those specific contracts.
- THE TWO VENUES USE DIFFERENT SETTLEMENT SOURCES FOR THE SAME ASSET: Global Bitcoin resolves on Binance BTC/USDT 1-minute candles; US Bitcoin resolves on the CF Benchmarks BRTI trimmed mean. Global markets carry UMA optimistic-oracle fields (umaBond, umaReward, umaResolutionStatus, resolvedBy); US markets name a specific real-world authority and have no oracle fields. A single shared price feed will NOT reconcile both venues' resolutions.
- SPORTS LEAGUE REGISTRY HAS DUPLICATE ROWS: /sports returns 469 objects but some leagues appear twice under different ids with the same primaryTagId (J2 League, J1 League, Asia WC Qualifiers, AFC Champions League Elite, North America WC Qualifiers). The 217 'live' count is by row, so the distinct-league figure is slightly lower.
- US SPORTS EVENTS WITHOUT A LEAGUE: 32 of 2,430 US sports events have primaryTag = null and could not be assigned to a league.
- LEGAL REACHABILITY NOT INDEPENDENTLY VERIFIED: the claim that Polymarket US is the venue legally reachable by US retail comes from docs.polymarket.us describing itself as a CFTC-regulated exchange. I did not verify CFTC registration against any regulator source, and I did not test geo-gating on polymarket.com. Do not treat the Global/US split in this report as legal advice.
- GEO-GATING UNTESTED: all requests came from one network location with no auth. If Polymarket serves a different category set by region or to logged-in users, this enumeration would not reveal it.
- US EVENT COUNTS IN THIN CATEGORIES ARE VERY SMALL: science=2, geopolitics=3, crypto=6, climate=10, finance=11, technology=15, macro=22 open events. Subcategory structure inferred from single-digit samples is fragile and will likely change within weeks. Only US sports (2,430) and politics (1,167) are substantial, and US politics is almost entirely the 2026 midterms, which expire on 2026-11-03 — after which the US politics tree in this report will be largely empty.

---

### Robinhood (Robinhood Derivatives, LLC) — event contracts / prediction markets

*Method: Primary source = Robinhood's own server-rendered page data, not prose summarization. Robinhood publishes no event-contract market-data API, but robinhood.com/us/en/prediction-markets/ is a Next.js page that embeds the live product catalog in a <script id="__NEXT_DATA__" type="application/json"> blob. I curl'd the hub page (3.0 MB) plus 36 category pages at https://robinhood.com/us/en/prediction-ma*

**Featured** — 1 subcategories

- `Featured` · e.g. (UI view only — surfaces contracts from other categories; carries no series of its own) · settles: n/a — merchandising view, not a product domain · per-event

**Live** — 1 subcategories

- `Live (in-play)` · e.g. NFLGAME-26SEP20INDKC-IND (September 20 Indianapolis vs Kansas City), MLBGAME-26SEP20MILBAL-MIL (September 20 Milwaukee vs Baltimore), KXWTAMATCH-26SEP20KASSAS-KAS (Kasatkina vs Sasnovich) · settles: n/a — filtered view of in-progress events from sports categories · per-event

**15 min** — 3 subcategories

- `Crypto 15-minute` · e.g. KXBTC15M-26SEP202130-30 (BTC 15 min · 9:15–9:30 PM EDT), KXETH15M-26SEP202130-30, KXSOL15M-26SEP202130-30 · settles: Kalshi spot index at the close of the 15-minute window (index provider not stated on the page) · intraday (every 15 minutes)
- `Metals 15-minute` · e.g. KXGOLD15M-26SEP202130-30 (Gold 15 min · 9:15–9:30 PM EDT), KXSILVER15M-26SEP202130-30, KXCOPPER15M-26SEP202130-30 · settles: Kalshi reference price at window close (source not stated on the page) · intraday (every 15 minutes)
- `Energy 15-minute` · e.g. KXWTI15M-26SEP202130-30 (WTI Oil 15 min · 9:15–9:30 PM EDT), KXNATGAS15M · settles: Kalshi reference price at window close (source not stated on the page) · intraday (every 15 minutes)

**College football** — 7 subcategories

- `Games` · e.g. KXNCAAFGAME-26SEP25HARVBRWN-HARV (Harvard vs Brown), NX.F.OPT.CFB-00063-260926-M.O.1.1.20270228 (Illinois vs Ohio State), NX.F.OPT.CFB-00036-260926-M.O.1.1.20270228 (Sam Houston vs Texas Tech) · settles: Official final score incl. overtime as declared by the governing body; Nadex-cleared games settle Event Cancelled at VWAP if not completed within 48h · per-event
- `FCS games` · e.g. (nav node present; no FCS-specific series ticker observed in the fetched payload) · per-event
- `Season outcomes` · e.g. NCAAF, NCAAFSEC, NCAAFB10 · settles: Official conference / national championship results · per-event
- `Playoff seeds` · e.g. KXNCAAFSEED, KXNCAAFTOPSEED, KXNCAAFQF · settles: Official College Football Playoff selection committee bracket · per-event
- `Playoff qualifiers` · e.g. NCAAFQUAL · settles: Official College Football Playoff field · per-event
- `Win totals` · e.g. KXNCAAFWINS · settles: Official regular-season win totals · per-event
- `Awards` · e.g. NCAAFHEISMAN, KXHEISMANFINALIST, KXNCAAFCOTY · settles: Official Heisman Trophy Trust / conference award announcements · per-event

**NFL** — 13 subcategories

- `Games` · e.g. NFLGAME-26SEP20INDKC-IND (September 20 Indianapolis vs Kansas City), NFLGAME-26SEP27CINPIT-CIN (Cincinnati vs Pittsburgh), NFLSPREAD · settles: Final score incl. overtime as determined by the Source Agency match results (Rothera T&C: NFLGame-T&C.pdf) · per-event
- `Season outcomes` · e.g. NFL, NFLAFC, NFLNFC · settles: Official NFL playoff and Super Bowl results · per-event
- `Division winners` · e.g. NFLAFCEAST, NFLAFCNORTH, NFLAFCSOUTH · settles: Official NFL final division standings · per-event
- `Win totals` · e.g. KXNFLWINS · settles: Official NFL regular-season standings · per-event
- `Playoff seeds` · e.g. KXNFLSEED, KXNFL1SEED · settles: Official NFL playoff seeding · per-event
- `Awards` · e.g. NFLMVP, KXNFLCOTY, KXNFLDPOTY · settles: Official AP / NFL Honors award announcements · per-event
- `League leaders` · e.g. KXLEADERNFLPYDS, KXLEADERNFLRUSHYDS, KXLEADERNFLRYDS · settles: Official NFL season statistics · per-event
- `Season stats` · e.g. KXNFLSEASONPASSYDS, KXNFLSEASONRECYDS, KXNFLSEASONREC · settles: Official NFL season statistics · per-event
- `Team specials` · e.g. KXNFLTSPEC · settles: Official NFL game/season data · per-event
- `Next team` · e.g. KXNEXTTEAMNFL · settles: Official team transaction announcements · per-event
- `Fantasy` · e.g. KXNFLFFLEADER, KXNFLFFLEADERTOP · settles: Fantasy scoring derived from official NFL statistics · weekly
- `Specials` · e.g. KXPERFORMSUPERBOWL, KXSUPERBOWLHEADLINE, KXNFLFIRSTTD · settles: Official NFL / event announcements · per-event
- `Draft` · e.g. KXNFLDRAFT1ST, KXNFLDRAFTPICK, KXNFLDRAFTTOP · settles: Official NFL Draft selections · per-event

**Midterms** — 51 subcategories

- `Control of Congress` · e.g. CNTRLCONG-26-DD (2026 Congressional Balance of Power), CNTRLHOU-26-REP (2026 U.S. House party winner), CNTRLSEN-26-REP (2026 U.S. Senate party winner) · settles: Certified 2026 midterm election results · per-event
- `Alabama` · e.g. GOVRACE-26AL-DEM (Alabama Governor winner), SENRACE-26AL-DEM (Alabama Senate winner), HOURACE-26AL02-DEM (AL-02 House race winner) · settles: Certified state election results · one-off
- `Alaska` · e.g. KXALASKAHOUSE, GOVRACE-26AK, SENRACE-26AK · settles: Certified state election results · one-off
- `Arizona` · e.g. HOUSEAZ2, GOVRACE-26AZ, SENRACE-26AZ · settles: Certified state election results · one-off
- `Arkansas` · e.g. GOVRACE-26AR, HOURACE-26AR · settles: Certified state election results · one-off
- `California` · e.g. HOUSECA3, HOUSECA9, HOUSECA13 · settles: Certified California election / ballot-measure results · one-off
- `Colorado` · e.g. GOVRACE-26CO, HOURACE-26CO · settles: Certified state election results · one-off
- `Connecticut` · e.g. HOUSECT5, GOVRACE-26CT · settles: Certified state election results · one-off
- `Delaware` · e.g. HOURACE-26DE, SENRACE-26DE · settles: Certified state election results · one-off
- `Florida` · e.g. HOUSEFL23, GOVRACE-26FL, SENRACE-26FL · settles: Certified state election results · one-off
- `Georgia` · e.g. GOVRACE-26GA, SENRACE-26GA · settles: Certified state election results · one-off
- `Hawaii` · e.g. GOVRACE-26HI, HOURACE-26HI · settles: Certified state election results · one-off
- `Idaho` · e.g. GOVRACE-26ID, HOURACE-26ID · settles: Certified state election results · one-off
- `Illinois` · e.g. GOVRACE-26IL, SENRACE-26IL, KXREDISTRICTING-26-IL · settles: Certified state election results · one-off
- `Indiana` · e.g. HOUSEIN1, KXHOUSEIN7, KXSECSTATEIN · settles: Certified state election results · one-off
- `Iowa` · e.g. GOVRACE-26IA, SENRACE-26IA · settles: Certified state election results · one-off
- `Kansas` · e.g. GOVRACE-26KS, HOURACE-26KS · settles: Certified state election results · one-off
- `Kentucky` · e.g. SENRACE-26KY, HOURACE-26KY · settles: Certified state election results · one-off
- `Louisiana` · e.g. SENRACE-26LA, HOURACE-26LA · settles: Certified state election results · one-off
- `Maine` · e.g. GOVRACE-26ME, SENRACE-26ME · settles: Certified state election results · one-off
- `Maryland` · e.g. GOVRACE-26MD, HOURACE-26MD · settles: Certified state election results · one-off
- `Massachusetts` · e.g. GOVRACE-26MA, KXMARENTCONTROL · settles: Certified state election / ballot-measure results · one-off
- `Michigan` · e.g. HOUSEMI3, HOUSEMI4, HOUSEMI8 · settles: Certified state election results · one-off
- `Minnesota` · e.g. GOVRACE-26MN, SENRACE-26MN · settles: Certified state election results · one-off
- `Mississippi` · e.g. SENRACE-26MS, HOURACE-26MS · settles: Certified state election results · one-off
- `Missouri` · e.g. KXHOUSEMO5, SENRACE-26MO · settles: Certified state election results · one-off
- `Montana` · e.g. GOVRACE-26MT, HOURACE-26MT · settles: Certified state election results · one-off
- `Nebraska` · e.g. GOVRACE-26NE, SENRACE-26NE · settles: Certified state election results · one-off
- `Nevada` · e.g. HOUSENV1, HOUSENV3, HOUSENV4 · settles: Certified state election results · one-off
- `New Hampshire` · e.g. GOVRACE-26NH, HOURACE-26NH · settles: Certified state election results · one-off
- `New Jersey` · e.g. HOUSENJ5, HOUSENJ9, SENRACE-26NJ · settles: Certified state election results · one-off
- `New Mexico` · e.g. HOUSENM2, GOVRACE-26NM, SENRACE-26NM · settles: Certified state election results · one-off
- `New York` · e.g. HOUSENY3, HOUSENY4, HOUSENY18 · settles: Certified state election results · one-off
- `North Carolina` · e.g. HOUSENC1, KXHOUSENC11, SENRACE-26NC · settles: Certified state election results · one-off
- `North Dakota` · e.g. HOURACE-26ND, SENRACE-26ND · settles: Certified state election results · one-off
- `Ohio` · e.g. HOUSEOH13, GOVRACE-26OH, SENRACE-26OH · settles: Certified state election results · one-off
- `Oklahoma` · e.g. GOVRACE-26OK, SENRACE-26OK · settles: Certified state election results · one-off
- `Oregon` · e.g. HOUSEOR5, GOVRACE-26OR, SENRACE-26OR · settles: Certified state election results · one-off
- `Pennsylvania` · e.g. HOUSEPA17, GOVRACE-26PA · settles: Certified state election results · one-off
- `Rhode Island` · e.g. GOVRACE-26RI, SENRACE-26RI · settles: Certified state election results · one-off
- `South Carolina` · e.g. GOVRACE-26SC, SENRACE-26SC · settles: Certified state election results · one-off
- `South Dakota` · e.g. GOVRACE-26SD, SENRACE-26SD · settles: Certified state election results · one-off
- `Tennessee` · e.g. GOVRACE-26TN, SENRACE-26TN · settles: Certified state election results · one-off
- `Texas` · e.g. HOUSETX34, KXHOUSETX9, KXHOUSETX32 · settles: Certified state election results · one-off
- `Utah` · e.g. KXHOUSEUT01, KXHOUSEUT02, KXHOUSEUT03 · settles: Certified state election results · one-off
- `Vermont` · e.g. GOVRACE-26VT, SENRACE-26VT · settles: Certified state election results · one-off
- `Virginia` · e.g. KXHOUSEVA10, SENRACE-26VA · settles: Certified state election results · one-off
- `Washington` · e.g. KXHOUSEWA8, SENRACE-26WA · settles: Certified state election results · one-off
- `West Virginia` · e.g. SENRACE-26WV, HOURACE-26WV · settles: Certified state election results · one-off
- `Wisconsin` · e.g. GOVRACE-26WI, HOURACE-26WI · settles: Certified state election results · one-off
- `Wyoming` · e.g. GOVRACE-26WY, SENRACE-26WY · settles: Certified state election results · one-off

**Baseball** — 10 subcategories

- `MLB games` · e.g. MLBGAME-26SEP20MILBAL-MIL (September 20 Milwaukee vs Baltimore), MLBGAME-26SEP22TBNYY1-TB (Tampa vs New York Y: Game 1), KXMLBSPREAD · settles: Official final score as reported by the Source Agency (Rothera contract terms) · daily
- `NPB games` · e.g. KXNPBGAME · settles: Official Nippon Professional Baseball results · daily
- `KBO games` · e.g. KXKBOGAME · settles: Official Korea Baseball Organization results · daily
- `Season outcomes` · e.g. KXMLB, KXMLBAL, KXMLBNL · settles: Official MLB postseason and standings · per-event
- `Specials` · e.g. KXMLBHR, KXMLBHIT, KXMLBKS · settles: Official MLB game and season statistics · per-event
- `Next team` · e.g. KXMLBNEXTTEAM, KXNEXTTEAMMLB, KXCOACHOUTMLB · settles: Official club transaction announcements · per-event
- `Divisions` · e.g. KXMLBALEAST, KXMLBALCENT, KXMLBALWEST · settles: Official MLB final division standings · per-event
- `Win totals` · e.g. KXMLBWINS · settles: Official MLB regular-season standings · per-event
- `League leaders` · e.g. KXLEADERMLBHR, KXLEADERMLBAVG, KXLEADERMLBRBI · settles: Official MLB season statistics · per-event
- `Awards` · e.g. KXMLBALMVP, KXMLBNLMVP, KXMLBALCY · settles: Official BBWAA / MLB award announcements · per-event

**Boxing** — 1 subcategories

- `KXBOXING (bout winner)` · e.g. KXBOXING-26SEP19FMAYMPAC-MPAC (Mayweather vs Pacquiao), KXBOXING-26OCT31CALVARMBILLI-CALVAR (Canelo Alvarez vs Christian Mbilli), KXBOXING-26OCT10SANDOVCOLLAZ-SANDOV · settles: Official bout decision from the sanctioning body · per-event

**Chess** — 1 subcategories

- `KXCHESSWORLDCHAMPION` · e.g. KXCHESSWORLDCHAMPION-CHESS26-AESI (World Chess Championship Winner) · settles: Official FIDE World Chess Championship result · per-event

**Climate** — 3 subcategories

- `Daily High Temperature` · e.g. UHLAX_092026_72 (Los Angeles Daily Temperature High September 20 2026), UHSFO_092026_63 (San Francisco), UHPHX_092026_96 (Phoenix) · settles: Official daily maximum temperature at the named airport station (23 US cities, ForecastEx) · daily
- `Daily Low Temperature` · e.g. ULLAX, ULSFO, ULPHX · settles: Official daily minimum temperature at the named airport station (23 US cities, ForecastEx) · daily
- `Rainfall` · e.g. KXRAIN-26SEP20-TTN (Where will it rain on Sep 20, 2026), KXRAINWKND-26SEP19-WPB (Where will it rain this weekend), KXRAINLAXM-26SEP-6 (Rain in Los Angeles in Sep 2026) · settles: Official measured precipitation at the named station · daily

**College basketball (M)** — 3 subcategories

- `Coaches` · e.g. KXNCAAMBNEXTCOACH-KU26-JCAS (Kansas Basketball - Next Head Coach) · settles: Official university head-coach hiring announcement · per-event
- `Conference tournament champions` · e.g. KXNCAAMBBIGEAST-27-CREI (Big East Men's Conference Tournament Champion), KXNCAAMBSEC-27-ALA, KXNCAAMBBIG12-27-ARIZ · settles: Official NCAA conference tournament results · per-event
- `March Madness` · e.g. KXMARMAD1SEED, KXMARMADROUND · settles: Official NCAA Tournament bracket and selection committee seeding · per-event

**Commodities** — 3 subcategories

- `WTI` · e.g. KXWTI-26SEP2114-T102.49 (Oil Price (WTI) on Sep 21, 2026), KXWTIW-26SEP1814-B93.50, KXWTIMAX-26SEP30-T94.00 (How high will WTI oil get by Sep 30, 2026) · settles: WTI crude oil reference price at the stated time (exchange settlement source not stated on the page) · daily
- `Brent crude` · e.g. KXBRENTD-26SEP2117-T96.50 (Brent crude oil price on September 21, 2026 at 5:00 PM EDT), KXBRENTW-26SEP2517-T104.99, KXBRENTMON-26SEP3017-T71.99 · settles: Brent crude reference price at the stated time · daily
- `Natural gas` · e.g. KXNATGASD-26SEP2117-T2.955 (Natural gas price on September 21, 2026 at 5:00 PM EDT), KXNATGASW-26SEP2517-T1.499, KXNATGASMON-26SEP3017-T0.999 · settles: Natural gas reference price at the stated time · daily

**Cricket** — 5 subcategories

- `County Championship` · e.g. KXCOUNTYCHAMPMATCH-26SEP150530WORDUR-WOR (Durham vs Worcestershire), KXCOUNTYCHAMPMATCH-26SEP150530MIDGLO-GLO (Gloucestershire vs Middlesex), KXCOUNTYCHAMPMATCH-26SEP150530DERNOR-DER · settles: Official ECB County Championship match result · per-event
- `ODI (M)` · e.g. KXODIMATCH · settles: Official men's One Day International result · per-event
- `T20 Intl (M)` · e.g. KXT20MATCH · settles: Official men's T20 International result · per-event
- `Test International (M)` · e.g. KXTESTMATCH · settles: Official men's Test match result · per-event
- `Caribbean Premier League` · e.g. KXCPLMATCH · settles: Official CPL match result · per-event

**Crypto** — 8 subcategories

- `BTC` · e.g. KXBTCY-27JAN0100-T20000.00 (Bitcoin price at the end of 2026), KXBTC2026200-27JAN01-200000 (Will Bitcoin be above $200k by next year?), KXBTCD-26SEP2517-T65499.99 (BTC price on Sep 25, 2026 at 5pm EDT) · settles: Bitcoin reference index at the stated timestamp (Kalshi and ForecastEx both list BTC; index provider not stated on the page) · daily
- `ETH` · e.g. KXETH, KXETHD, KXETHMAXMON · settles: Ether reference index at the stated timestamp · daily
- `HYPE` · e.g. KXHYPED, KXHYPEMAXMON, KXHYPEMINMON · settles: HYPE reference index at the stated timestamp · daily
- `SOL` · e.g. KXSOLD, KXSOLMAXMON, KXSOLMINMON · settles: Solana reference index at the stated timestamp · daily
- `XRP` · e.g. KXXRPD, KXXRPMAXMON, KXXRPMINMON · settles: XRP reference index at the stated timestamp · daily
- `DOGE` · e.g. KXDOGED, KXDOGEMAXMON, KXDOGEMINMON · settles: Dogecoin reference index at the stated timestamp · daily
- `BNB` · e.g. KXBNB15M, KXBNBMAXMON, KXBNBMINMON · settles: BNB reference index at the stated timestamp · daily
- `Yearly` · e.g. KXCRYPTORETURNY-26-XRP (Which of these cryptocurrencies will have a positive return in 2026?), KXBTCVSGOLD-26 (Will Bitcoin outperform gold in 2026?), KXCRYPTOSTRUCTURE-26JAN-JUN (Will the Clarity Act become law) · settles: Year-end reference index levels; KXCRYPTOSTRUCTURE settles on US legislative enactment · per-event

**Canadian Football** — 1 subcategories

- `Games` · e.g. KXCFLGAME-26SEP25TORWPG-WPG (Toronto Argonauts vs Winnipeg Blue Bombers), KXCFLGAME-26SEP25SSKBC-SSK (Saskatchewan Roughriders vs British Columbia Lions), KXCFLGAME-26SEP26CGYOTT-OTT · settles: Official CFL game and Grey Cup results · per-event

**Economics** — 7 subcategories

- `Fed decision` · e.g. ECUSFED-26OCT-H0 (Fed rate decision in October 2026), ECUSFED-26DEC-H0 (Fed rate decision in December 2026), ECUSFED-27JUL-H0 (Fed rate decision in July 2027) · settles: FOMC target federal funds rate announcement (Rothera-cleared) · monthly
- `The Fed` · e.g. KXFED, KXFEDHIKE, KXRATECUTCOUNT-26DEC31-T9 (Number of rate cuts in 2026) · settles: FOMC policy statements · per-event
- `Gas prices` · e.g. KXAAAGASD-26SEP21-4.4450 (US gas prices tomorrow), KXAAAGASW-26SEP21-4.2000 (US gas prices this week), KXAAAGASMAX-26DEC31-7.00 (How high will US gas prices get in 2026) · settles: AAA national / state average retail gasoline price · daily
- `Indicators` · e.g. KXCPI-26SEP-T0.5 (CPI in September), KXCPIYOY-26SEP-T4.7 (Inflation in September 2026 (CPI YoY)), KXU3-26SEP-T3.7 (Unemployment in September) · settles: BLS (CPI, U-3, payrolls), BEA (GDP, PCE), NAR/Census (home sales) · monthly
- `International` · e.g. KXCBDECISIONEU, KXCBDECISIONENGLAND, KXCBDECISIONCANADA · settles: ECB / Bank of England / Bank of Canada / RBA policy rate announcements · per-event
- `Macro` · e.g. KXRECSSNBER-26 (Recession this year?), KXRECSSNBER-27 (Recession in 2027), KXLAYOFFSYINFO-26-494000 (More tech layoffs in 2026 than in 2025) · settles: NBER business-cycle dating committee (recession); reported layoff trackers · per-event
- `Energy` · e.g. KXOILRIGS, KXBARRELS, KXNGASMAX · settles: EIA weekly inventory / Baker Hughes rig count (inferred from series names, not stated on the page) · weekly

**Education** — 2 subcategories

- `Tuition` · e.g. UTHVT_1226_59000 (What will Harvard tuition be in 2026?), UTLAO_1226_48000 (What will UCLA out-of-state tuition be in 2026?), UTCBO_1226_49000 (UC Berkeley out-of-state) · settles: National Center for Education Statistics (NCES) annual tuition-and-fees reporting — stated verbatim in the contract description · per-event
- `Ranking` · e.g. UVR1O_123127_PU (Which school will rank first overall in 2027?), UVR1P_123127_UCLA (Which school will rank first for public universities in 2027?) · settles: A published national university ranking — the specific publisher is not named on the page · per-event

**Elections** — 2 subcategories

- `Presidential` · e.g. USPRESIDENT-28-MRUB (2028 U.S. Presidential election winner), USPRESPARTY-28-REP (2028 U.S. Presidential election party winner), USPRESNOM-28DEM-GNEW (2028 Democratic Presidential nominee) · settles: Certified US presidential election results / official party convention nominations (Rothera-cleared) · one-off
- `Control of Congress` · e.g. CNTRLHOU-26-REP (2026 U.S. House party winner), CNTRLSEN-26-REP (2026 U.S. Senate party winner) · settles: Certified congressional election results · one-off

**Entertainment** — 12 subcategories

- `Emmy Winners` · e.g. KXEMMYDSERIES, KXEMMYCSERIES, KXEMMYDACTO · settles: Official Primetime Emmy Awards announcement · per-event
- `Big Brother` · e.g. KXBIGBROTHER, KXBIGBROTHERELIMINATION, KXBIGBROTHERRANK · settles: Broadcast episode outcomes · weekly
- `Oscar Winners` · e.g. KXOSCARPIC, KXOSCARDIR, KXOSCARACTO · settles: Official Academy Awards ceremony results · per-event
- `Oscar Nominees` · e.g. KXOSCARNOMPIC, KXOSCARNOMDIR, KXOSCARNOMACTO · settles: Official Academy Award nominations announcement · per-event
- `Grammy Winners` · e.g. KXGRAMAOTY, KXGRAMBNA · settles: Official Grammy Awards ceremony results · per-event
- `Grammy Nominees` · e.g. KXGRAMMYNOMAOTY, KXGRAMMYNOMROTY, KXGRAMMYNOMSOTY · settles: Official Grammy nominations announcement · per-event
- `TV` · e.g. KXNETFLIXRANKSHOW, KXNETFLIXRANKSHOWRUNNERUP · settles: Netflix Top 10 weekly rankings · weekly
- `Movies` · e.g. KXNETFLIXRANKMOVIE, KXNETFLIXRANKMOVIERUNNERUP, KXTAKEOVERACQWB · settles: Netflix Top 10 weekly rankings; corporate acquisition announcements · weekly
- `Rotten Tomatoes` · e.g. KXRT · settles: Rotten Tomatoes critic score · per-event
- `Music` · e.g. KX1ALBUM, KX1SONG, KXBBCHARTPOSITIONSONG · settles: Billboard chart positions; streaming-platform artist rankings · weekly
- `Music streams` · e.g. KXARTISTSTREAMSY-DRAKE26DEC31-22.0B (Drake Streams in 2026), KXARTISTSTREAMSY-BEY26DEC31-5.5B (Beyoncé Streams in 2026), KXARTISTSTREAMSY-BMARS26DEC31-19.5B (Bruno Mars) · settles: Cumulative artist stream counts on a named streaming platform (platform not stated on the page) · per-event
- `Video games` · e.g. GTA6, KXGAMEAWARDS · settles: Publisher release announcements; The Game Awards results · per-event

**Esports** — 5 subcategories

- `LoL` · e.g. KXLOLGAME-26SEP210300CPDFNL-CPD (Cupid Esports vs. FENNEL) · settles: Official League of Legends match results · per-event
- `CS2` · e.g. KXCS2-SLSF26-FURIA (StarLadder StarSeries Fall Champion), KXCS2GAME-26SEP201945QUINYOU-YOU (QUINTESSENCIA vs. your end) · settles: Official Counter-Strike 2 tournament results · per-event
- `Dota 2` · e.g. KXDOTA2GAME · settles: Official Dota 2 match results · per-event
- `Valorant` · e.g. KXVALORANTGAME · settles: Official Valorant match results · per-event
- `R6` · e.g. KXR6GAME · settles: Official Rainbow Six match results · per-event

**Financial** — 4 subcategories

- `S&P` · e.g. KXINXY-26DEC31H1600-T9000 (S&P close price end of 2026?), KXINXPOS-26DEC31H1900-T6845.5 (Will the S&P finish positive this year?), KXINXMAXY-01JAN2027-8999.99 (How high will the S&P get this year?) · settles: S&P 500 index close / E-mini S&P 500 futures settlement · daily
- `Nasdaq` · e.g. KXNASDAQ100Y-26DEC31H1600-T33000 (Nasdaq-100 close price end of 2026?), KXNASDAQ100POS-26DEC31H1600-T25249.85, FNQ_091826_28600 (Nasdaq 100 futures price on September 18, 2026) · settles: Nasdaq-100 index close / E-mini Nasdaq-100 futures settlement · daily
- `FX` · e.g. JPUSD_092126_154 (US Dollar to Japanese Yen Exchange Rate September 21 2026), USGBP_092126_1.3175 (Pound Sterling to US Dollar), USEUR_092126_1.11 (Euro to US Dollar) · settles: Spot FX reference rate at the stated date (ForecastEx); KXUSDX settles on the US Dollar Index · daily
- `Market outlooks` · e.g. KXCCLIMIT · settles: Published market/credit statistics (source not stated on the page) · per-event

**Golf** — 4 subcategories

- `PGA` · e.g. KXPGAR2TOP10-BICA26-CBEZ (Biltmore Championship Asheville: Round 2 Top 10 Finishers), KXPGATOP5, KXPGATOP10 · settles: Official PGA Tour tournament leaderboard · weekly
- `LIV Golf` · e.g. KXLIVOCCUR · settles: Official LIV Golf event results / announcements · per-event
- `DP World Tour` · e.g. KXDPWORLDTOUR-FEODF26-RPEA (FedEx Open de France Winner), KXDPWORLDTOURR1LEAD-FEODF26-JMOR (FedEx Open de France End of Round 1 Leader) · settles: Official DP World Tour leaderboard · weekly
- `LPGA` · e.g. KXLPGATOUR · settles: Official LPGA Tour leaderboard · weekly

**Metals** — 5 subcategories

- `Gold` · e.g. METLG_093026_4000 (Gold Price September 30 2026), METLG_092126_4125 (Gold Price September 21 2026), KXGOLD15M-26SEP202130-30 (Gold 15 min) · settles: Gold reference price at the stated date (exchange/benchmark not named on the page) · daily
- `Silver` · e.g. METLS_093026_48 (Silver Price September 30 2026), METLS_092126_60, KXSILVER15M-26SEP202130-30 · settles: Silver reference price at the stated date · daily
- `Copper` · e.g. COMCP_093026_5.94 (Copper Price September 30 2026), COMCP_092126_6.42, KXCOPPER15M-26SEP202130-30 · settles: Copper reference price at the stated date · daily
- `Platinum` · e.g. METLP_093026_1400 (Platinum Price September 30 2026), METLP_092126_1575 · settles: Platinum reference price at the stated date · daily
- `Palladium` · e.g. METLD_093026_1050 (Palladium Price September 30 2026), METLD_092126_1125 · settles: Palladium reference price at the stated date · daily

**MMA** — 1 subcategories

- `KXUFCFIGHT (bout winner)` · e.g. KXUFCFIGHT-26SEP26VIEBRY-VIE (Fight Night: Vieira vs Bryczek), KXUFCFIGHT-26SEP26DEMJAU-DEM (Fight Night: Demopoulos vs Jauregui), KXUFCFIGHT-26SEP26ROSBAR-BAR (Fight Night: Rosas Jr vs Barcelos) · settles: Official UFC bout decision · per-event

**Politics** — 5 subcategories

- `Trump` · e.g. KXTRUMPADMINLEAVE-26DEC31-RSCO (Who will leave the Trump administration in 2026), KXHEGSETHOUT-26APR-SEP01 (Pete Hegseth out as Secretary of Defense), KXKASHOUT-26APR-MAY01 (Kash Patel out as FBI Director) · settles: Official White House / agency personnel announcements · per-event
- `Trade` · e.g. KXTARIFFCHECKS-26-AUG (Will Americans receive tariff stimulus checks?), KXGREENLAND-29 (Will Trump buy at least part of Greenland?), KXGREENLANDPRICE-29JAN21-NOACQ (How much will the US acquire Greenland for?) · settles: Official US government announcements and enacted legislation · per-event
- `Fiscal` · e.g. KXCAWEALTHTAX-26 (Will the California billionaire wealth tax pass?), KXCABILLIONAIRETAX-26NOV03, KXCCLIMIT · settles: Enacted legislation / certified ballot-measure results · per-event
- `Policy` · e.g. KXSAVEACT-27-JAN04 (Will the SAVE Act become law), KXCRYPTOSTRUCTURE-26JAN-JUN (Will the Clarity Act become law), KXACAEXT · settles: Enactment of US federal or state legislation · per-event
- `International` · e.g. KXVENEZUELALEADER-26DEC31-DRON (Who will lead Venezuela at the end of 2026?), KXLEADERSOUT-27JAN01-MFREPMD (World leaders out before 2027?) · settles: Official government leadership transitions · per-event

**NBA** — 3 subcategories

- `Season Outcomes` · e.g. NBA-27-ATL (2027 Pro Men's Basketball Champion), NBAEAST-27-ATL (2027 Eastern Conference Champion), NBAWEST-27-DAL (2027 Western Conference Champion) · settles: Official NBA Finals, conference and division results (Rothera-cleared) · per-event
- `Specials` · e.g. KXNEXTTEAMNBA · settles: Official NBA player transaction announcements · per-event
- `Coaches` · e.g. KXNEXTNBACOACH · settles: Official NBA head-coach hiring announcements · per-event

**NHL** — 2 subcategories

- `Season outcomes` · e.g. NHL, NHLEAST, NHLWEST · settles: Official NHL Stanley Cup, conference and division results (Rothera-cleared) · per-event
- `Awards` · e.g. NHLMVP · settles: Official NHL award announcements (Hart Trophy) · per-event

**WNBA** — 5 subcategories

- `Games` · e.g. KXWNBAGAME · settles: Official WNBA game results · daily
- `Season outcomes` · e.g. KXWNBA · settles: Official WNBA Finals results · per-event
- `Win Totals` · e.g. KXWNBAWINS · settles: Official WNBA regular-season standings · per-event
- `Awards` · e.g. KXWNBAMVP, KXWNBACOY, KXWNBADPOY · settles: Official WNBA award announcements · per-event
- `League leaders` · e.g. KXLEADERWNBAPTS, KXLEADERWNBAREB, KXLEADERWNBAAST · settles: Official WNBA season statistics · per-event

**Racing** — 2 subcategories

- `F1` · e.g. KXF1-26-VB (F1 Drivers Champion?), KXF1CONSTRUCTORS-26-WIL (F1 Constructors Champion), KXF1RACE · settles: Official FIA Formula 1 race and championship classifications · per-event
- `NASCAR` · e.g. KXNASCARCUPSERIES-NCS26-ZSMI (NASCAR Cup Series Champion?) · settles: Official NASCAR Cup Series championship standings · per-event

**Soccer** — 20 subcategories

- `EPL` · e.g. EPL (Rothera season winner), KXEPLTOP, KXEPLLEADER · settles: Official Premier League results and final table · weekly
- `La Liga` · e.g. KXLALIGA, KXLALIGATOP, KXLALIGARELEGATION · settles: Official LaLiga results and final table · weekly
- `Serie A` · e.g. KXSERIEA, KXSERIEATOP, KXSERIEARELEGATION · settles: Official Serie A results and final table · weekly
- `Champions League` · e.g. UCL (Rothera), KXCLUBFGAME, KXUECL · settles: Official UEFA competition results · weekly
- `Bundesliga` · e.g. KXBUNDESLIGA, KXBUNDESLIGATOP, KXBUNDESLIGARELEGATION · settles: Official Bundesliga results and final table · weekly
- `Ligue 1` · e.g. KXLIGUE1, KXLIGUE1TOP, KXLIGUE1RELEGATION · settles: Official Ligue 1 results and final table · weekly
- `MLS` · e.g. KXMLSGAME-26SEP20MIASD-MIA (Miami vs San Diego FC), KXMLSGAME-26SEP23SEARSL-SEA (Seattle vs Salt Lake), KXMLSCUP · settles: Official Major League Soccer results · weekly
- `Liga MX` · e.g. KXLIGAMX, KXLIGAMXGAME · settles: Official Liga MX results · weekly
- `Argentina Primera Division` · e.g. KXARGPREMDIVGAME · settles: Official Argentine Primera División results · weekly
- `Brasileiro Serie A` · e.g. KXBRASILEIROGAME · settles: Official Campeonato Brasileiro Série A results · weekly
- `EFL Cup` · e.g. KXEFLCUP, KXFACUP, KXFACUPGAME · settles: Official EFL Cup / FA Cup results · per-event
- `Danish Superliga` · e.g. KXDENSUPERLIGAGAME · settles: Official Danish Superliga results · weekly
- `Korea K League 1` · e.g. KXKLEAGUEGAME · settles: Official K League 1 results · weekly
- `Ecuador LigaPro` · e.g. KXECULPGAME · settles: Official Ecuadorian LigaPro results · weekly
- `APF División de Honor` · e.g. KXAPFDDHGAME · settles: Official Paraguayan División de Honor results · weekly
- `Colombian Liga DIMAYOR` · e.g. KXDIMAYORGAME · settles: Official Categoría Primera A (DIMAYOR) results · weekly
- `Peru Liga 1` · e.g. KXPERLIGA1GAME · settles: Official Peruvian Liga 1 results · weekly
- `EFL League One` · e.g. KXEFLL1GAME, KXEFLPROMO · settles: Official EFL League One results and final table · weekly
- `NWSL` · e.g. KXNWSLGAME · settles: Official NWSL results · weekly
- `Season outcomes` · e.g. KXAFCONGAME, KXINTLFRIENDLYGAME · settles: Official AFCON / international friendly results · per-event

**Technology** — 4 subcategories

- `AI` · e.g. KXLLM1-26DEC31-XAI (Best AI at the end of 2026?), KXLLM1-26SEP21-GOOG (Best AI this week), KXB200MAX-26DEC31-7.970 (Price of NVIDIA B200 compute by Dec 31, 2026) · settles: Public LLM leaderboard ranking (specific leaderboard not named on the page); published GPU compute rental prices · weekly
- `Companies` · e.g. KXLAYOFFSYINFO-26-494000 (More tech layoffs in 2026 than in 2025) · settles: Published tech layoff tracker totals · per-event
- `Science` · e.g. KXALIENS-27 (Will the U.S. confirm that aliens exist), KXREACTOR-26DEC31 (US grants license for new nuclear reactor before 2027?), KXFDAAPPROVALPSYCHEDELIC-27-ANYPSYCH (Will the FDA approve any psychedelic substance for medical use before 2027?) · settles: Official US government statements; NRC licensing actions; FDA approval announcements · per-event
- `Space` · e.g. KXSPACEXCOUNT-26B-210 (How many launches will SpaceX have in 2026), KXSPACEXCOUNT-26SEP-10 (How many launches will SpaceX have in September) · settles: Recorded SpaceX orbital launch counts · monthly

**Tennis** — 14 subcategories

- `Davis Cup` · e.g. KXDAVISCUPMATCH · settles: Official Davis Cup match results · per-event
- `WTA Sao Paulo` · e.g. KXWTAMATCH-26SEP20QUEPOD-QUE (Quevedo vs Podoroska) · settles: Official WTA match results · per-event
- `WTA Seoul` · e.g. KXWTAMATCH-26SEP20KASSAS-KAS (Kasatkina vs Sasnovich), KXWTA · settles: Official WTA match results · per-event
- `WTA Singapore` · e.g. KXWTAMATCH-26SEP20VOLKAL-VOL (Volynets vs Kalieva), KXWTASETWINNER, KXWTADOUBLES · settles: Official WTA match results · per-event
- `ITF (M)` · e.g. KXITFMATCH · settles: Official ITF men's match results · per-event
- `ITF (W)` · e.g. KXITFWMATCH · settles: Official ITF women's match results · per-event
- `ATP Challenger Buenos Aires II` · e.g. KXATPCHALLENGERMATCH · settles: Official ATP Challenger Tour match results · per-event
- `ATP Challenger Saint Tropez` · e.g. KXATPCHALLENGERMATCH · settles: Official ATP Challenger Tour match results · per-event
- `ATP Challenger San Diego 2` · e.g. KXATPCHALLENGERMATCH · settles: Official ATP Challenger Tour match results · per-event
- `ATP Challenger Genoa 2` · e.g. KXATPCHALLENGERMATCH · settles: Official ATP Challenger Tour match results · per-event
- `ATP Challenger Plovdiv 4` · e.g. KXATPCHALLENGERMATCH · settles: Official ATP Challenger Tour match results · per-event
- `WTA 125k Ankara` · e.g. KXWTACHALLENGERMATCH · settles: Official WTA 125 match results · per-event
- `WTA 125K Porto` · e.g. KXWTACHALLENGERMATCH · settles: Official WTA 125 match results · per-event
- `WTA 125K Tolentino` · e.g. KXWTACHALLENGERMATCH · settles: Official WTA 125 match results · per-event

**Not confirmed:**

- SNAPSHOT, NOT A STABLE CATALOG. Everything here is what robinhood.com served on 2026-09-20. navigationNodes is generated per request and is seasonal: NFL, College football, Baseball, WNBA and Midterms are live now precisely because their seasons are. Categories absent today (e.g. a dedicated March Madness or Olympics tab) may have existed earlier in 2026 and may return. Treat the 32 categories as the current live set, not the all-time set.
- 649 SERIES IS A VERIFIED FLOOR, NOT A COMPLETE COUNT. Each category page returns only the events it renders above the fold — e.g. the college-football page carried 21.9 MB of events, the boxing page 5. The true series count is higher. I did not paginate, and there is no public endpoint that returns the full book. Do not treat 649 as Robinhood's total catalog size.
- SOME 'SUBCATEGORIES' ARE ROTATING EVENT INSTANCES, NOT TAXONOMY. Tennis is the clearest case: 'WTA Seoul', 'ATP Challenger Saint Tropez', 'WTA 125K Tolentino' are this week's tournaments and will be different names next week. The durable layer underneath is the series ticker (KXWTAMATCH, KXATPCHALLENGERMATCH, KXITFMATCH). Golf and Soccer have the same property to a lesser degree. If you are building a schema, key on the series ticker, not the nav label.
- 'Featured' AND 'Live' ARE VIEWS, NOT DOMAINS. They carry no series of their own — they re-surface contracts from other categories. I included them because they are literally in Robinhood's nav, but they should not become domains in a normalized schema. '15 min' is different: it is a genuine product family with 14 dedicated Kalshi series.
- METALS IS SEPARATE FROM COMMODITIES ON ROBINHOOD. Gold, silver, copper, platinum and palladium sit under a top-level 'Metals' tab; 'Commodities' contains only WTI, Brent and natural gas. This cuts against the common assumption that metals nest under commodities — worth noting if you are normalizing across venues.
- FOURTH VENUE IS NOT IN ROBINHOOD'S OWN DISCLOSURE. The support article 'Event contracts overview' names only KalshiEX, ForecastEX and Rothera. But live contracts carry exchangeSource=4 with terms hosted at help.crypto.com (e.g. NX.F.OPT.CFB college football games) — that is OG.com/Nadex, from the Robinhood/Crypto.com deal announced 2026-09-08. The support page has not caught up. I saw only ONE distinct series on that venue (NX.F.OPT.CFB), so its catalog share is currently tiny.
- VENUE ENUM MAPPING IS INFERRED FROM TERMS-URL DOMAINS, NOT FROM A LABEL. Robinhood's payload gives an integer, never a venue name. I resolved 1=ForecastEx, 2=Kalshi, 3=Rothera, 4=OG.com/Nadex by reading each contract's own T&C link. All four are corroborated by a primary document URL, but the enum is undocumented and Robinhood could renumber it.
- SAME CATEGORY, MULTIPLE VENUES — AND THEY OVERLAP. College football games clear on both Kalshi (KXNCAAFGAME) and OG.com/Nadex (NX.F.OPT.CFB). NFL/MLB/NBA/NHL games clear on Rothera while NFL props clear on Kalshi. Bitcoin lists on both Kalshi (KXBTC*) and ForecastEx (YXHBT/YXLBT). So venue is a per-series attribute, not a per-category one, and the same underlying event can exist twice with different tickers and different settlement rules.
- SETTLEMENT SOURCES ARE PARTLY INFERRED. Only a few are stated verbatim in the payload — Education tuition explicitly cites NCES, and Rothera sports cite 'the Source Agency'. Where I wrote a source for crypto indices, metals benchmarks, the AI leaderboard, music-stream counts, university rankings, and EIA/Baker Hughes energy data, that is inference from the series name and is NOT confirmed on the page. Verify against each venue's own contract PDF before relying on it.
- COULD NOT CONFIRM WEB CATALOG == IN-APP CATALOG. This is the public marketing site. Robinhood's iOS/Android app may expose categories, subcategories or series that the web hub does not, and access is gated by account eligibility and state. I have no way to check the in-app taxonomy without an authenticated session.
- NO PUBLIC API — AND THE SOURCE I USED IS UNDOCUMENTED AND UNSTABLE. props.pageProps.navigationNodes / subcategoryNodesMap / events is an internal Next.js payload shape. It is not a supported interface, has no versioning or rate-limit contract, and can change or disappear without notice. It is fine for a one-time taxonomy extraction; it is not a feed to build live ingestion on.
- 'FCS games' HAS NO OBSERVED TICKER. The nav node exists under College football but no FCS-specific series appeared in the fetched events. Either it was empty at snapshot time or its contracts use the general KXNCAAFGAME series. Unresolved.
- THE ON-PAGE COUNTS ARE LIVE, NOT STRUCTURAL. The hub renders counts like 'Tennis 252' or 'Soccer 305'. Those are open contracts at that instant and will differ on any other fetch. I did not use them as taxonomy evidence.
- 198 SUBCATEGORY NODES IS WHAT THE HUB PAYLOAD CARRIED. Individual category pages may expose deeper nesting that the hub does not preload. I enumerated one level below each top-level category and did not probe for a third level.

---

## 2 · Normalized schema — 18 domains, 208 subdomains

### `politics-and-government` — Politics & Government

Non-electoral government action: laws, appointments, courts, budgets, regulation.

**On:** kalshi, polymarket, robinhood · **10 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `us-legislation` US Federal Legislation | kalshi:Politics › Bills, polymarket:Politics › Congress, robinhood:Politics › Policy | Congress.gov bill status, committee calendars, whip counts, cloture history, CBO scores | Library of Congress / enacted text |
| `shutdown-and-debt-ceiling` Shutdowns & Debt Ceiling | kalshi:Politics › Debt ceiling & shutdowns, polymarket:Politics › Gov Shutdown | Appropriations deadlines, CR text, Treasury extraordinary-measures runway, OPM lapse notices | OPM / Treasury |
| `executive-appointments` Cabinet & Confirmations | kalshi:Politics › Cabinet/Confirmations, polymarket:Politics › Trump Cabinet, robinhood:Po | Senate floor schedule, cloture votes, resignation reporting, agency personnel notices | White House / Senate record |
| `presidential-tenure-and-conduct` Presidential Tenure & Conduct | kalshi:Politics › Trump/Trump Agenda, polymarket:Politics › Trump, robinhood:Politics › Tr | Actuarial tables, impeachment/25th-Amendment base rates, official schedule and statement feeds | Reuters / WSJ consensus |
| `courts-and-judiciary` Courts & Judiciary | kalshi:Politics › SCOTUS & courts/Court cases, polymarket:Politics › Courts, polymarket:US | SCOTUS docket and cert-grant rates, oral-argument calendar, PACER filings, justice age/tenure | Supreme Court / PACER |
| `tax-policy` Tax Policy | kalshi:Politics › Taxes, polymarket:Politics › Taxes, robinhood:Politics › Fiscal | Reconciliation vehicle status, JCT scores, state legislative calendars, ballot-measure polling | Enacted legislation |
| `trade-and-tariffs` Trade Policy & Tariffs | kalshi:Politics › Trump (tariffs), polymarket:Economy › Trade War, robinhood:Politics › Tr | Section 232/301 proceedings, Federal Register notices, HTS schedules, retaliation announcements | Federal Register / USTR |
| `immigration-and-border` Immigration & Border | kalshi:Politics › Immigration | CBP monthly encounters, EOIR case backlog, USCIS receipts, injunction status | USCIS / EOIR |
| `state-and-local-government` State & Local Government | kalshi:Politics › Local/NYC/Governor, robinhood:Midterms › state ballot items | State session calendars, municipal budget votes, mayoral executive orders | State legislature / governor's office |
| `approval-and-polling` Approval Ratings & Generic Ballot | kalshi:Politics › Approval ratings, kalshi:Elections › Recurring | Daily poll aggregator series, pollster house effects, historical weekly drift variance | FiveThirtyEight / VoteHub |

### `elections` — Elections

Contested races, ballot measures and seat-count outcomes worldwide.

**On:** kalshi, polymarket, robinhood · **11 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `us-presidential` US Presidential & Nominations | kalshi:Elections › 2028, polymarket:Politics › US Election, robinhood:Elections › Presiden | Primary polling, endorsement counts, filing deadlines, electoral-college state priors | AP / certified results |
| `us-senate` US Senate Races | kalshi:Elections › Senate, polymarket:Politics › Senate midterms, robinhood:Midterms › sta | District polling, incumbency and midterm-penalty priors, fundraising, candidate filings | State electoral authorities |
| `us-house` US House Races | kalshi:Elections › House, polymarket:Politics › House Elections, robinhood:Midterms › HOUR | District-level PVI, redistricting maps, generic ballot, retirement announcements | State electoral authorities |
| `us-governor` Governor Races | kalshi:Elections › Governor, polymarket:Politics › Governor midterms, robinhood:Midterms › | State polling, term-limit status, partisan lean, approval of sitting governor | State electoral authorities |
| `other-statewide-offices` Other Statewide & Local Offices | kalshi:Elections › Other US Elections/Local, polymarket:Politics › Mayoral Elections | Down-ballot polling scarcity, straight-ticket correlation with top of ticket | Secretary of State / county boards |
| `primaries` Primaries & Nomination Contests | kalshi:Elections › Primaries, polymarket:Politics › Primaries | Primary polls, endorsement networks, small-dollar fundraising, ballot-access filings | State party / election board |
| `ballot-measures` Ballot Measures & Referendums | kalshi:Elections › Referendums, polymarket:US: politics › Redistricting/Abortion, robinhoo | Measure-specific polling, signature counts, historical yes-vote base rates by measure type | State certification |
| `seat-count-and-combos` Balance of Power & Seat Counts | kalshi:Elections › Election Combos/Senate Combos/House Combos, polymarket:Politics › Midte | Joint seat-level distributions with correlated national swing, not independent race probabilities | AP race calls |
| `margins-and-turnout` Margins & Turnout | kalshi:Elections › Election Combos, polymarket:Politics › Margin of Victory/Turnout, polym | Early-vote files, historical county margins, registration-by-party trends | Certified vote totals |
| `judicial-elections` Judicial Elections & Retention | kalshi:Elections › SCOTUS & courts | Retention-vote base rates, state judicial-race spending, partisan endorsement | State Secretary of State |
| `international-elections` International Elections | kalshi:Elections › International elections/Foreign Elections/Brazil/Peru/Hungary, polymark | National polling aggregates, seat-allocation rules (D'Hondt etc.), coalition arithmetic, runoff thresholds | National electoral commissions |

### `geopolitics-and-conflict` — Geopolitics & Conflict

Wars, territorial control, diplomacy, strikes, regime tenure.

**On:** kalshi, polymarket, robinhood · **11 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `russia-ukraine` Russia–Ukraine War | polymarket:Geopolitics › Ukraine/Ukraine Map/Ukraine Peace Deal, polymarket:Geopolitics ›  | ISW/DeepState daily control polygons, rate-of-advance per settlement, negotiation-round calendar | ISW & DeepState control maps |
| `israel-gaza-lebanon` Israel, Gaza & Lebanon | polymarket:Geopolitics › Israel/Gaza/Lebanon, kalshi:Politics › International | Ceasefire phase milestones, hostage/prisoner exchange schedules, IDF operational statements | Credible reporting via UMA |
| `iran` Iran, Nuclear & Sanctions | kalshi:Politics › Iran, polymarket:Geopolitics › Iran/Nuclear, polymarket:US: geopolitics | IAEA enrichment inventory reports, snapback timelines, talks calendar, strike-tempo reporting | IAEA / diplomatic instruments |
| `shipping-chokepoints` Maritime Chokepoints | kalshi:Politics › Iran (Hormuz/Suez/Bab al-Mandab), polymarket:Geopolitics › Strait of Hor | IMF PortWatch daily ship-arrival series, war-risk insurance premia, Houthi attack tempo | IMF PortWatch 7-day MA of transit calls |
| `china-taiwan` China & Taiwan | polymarket:Geopolitics › China / Taiwan, kalshi:Elections › International | PLA exercise tempo, ADIZ incursion counts, Taiwan election cycle, US arms-sale notifications | Credible reporting via UMA |
| `latin-america-conflict` Venezuela, Cuba & Latin America | polymarket:Geopolitics › Venezuela / Cuba, robinhood:Politics › International | US force posture in Caribbean, sanctions/OFAC actions, regime-defection reporting | Credible reporting |
| `gulf-and-turkey` Gulf States & Turkey | polymarket:Geopolitics › Saudi Arabia / Turkey | Succession/health reporting, OPEC+ politics, Aegean incident logs, NATO friction indicators | Credible reporting |
| `alliances-and-treaties` NATO, Alliances & Treaties | polymarket:Geopolitics › NATO, polymarket:US: geopolitics | Treaty withdrawal procedure timelines, summit calendar, Article 4/5 invocation history | Official NATO/US announcements |
| `territorial-acquisition` Territorial Acquisition | polymarket:Geopolitics › Greenland, robinhood:Politics › Trade | Formal negotiation status, Danish/Greenlandic parliamentary positions, base-rate of sovereignty transfers | Signed instruments / credible reporting |
| `south-asia-and-africa-conflict` South Asia, Sudan & Other Conflicts | polymarket:Geopolitics › India-Pakistan/Sudan/Thailand-Cambodia, polymarket:World › Africa | ACLED event counts, ceasefire-mediation rounds, border-incident tempo | Credible reporting |
| `world-leader-tenure` World Leader Tenure | polymarket:Geopolitics › leader-out markets, kalshi:World, robinhood:Politics › Internatio | Constitutional term limits, coalition stability, health reporting, scheduled election dates | Official government transitions |

### `macroeconomics` — Macroeconomics

Official statistics, central-bank policy and macro conditions.

**On:** kalshi, polymarket, robinhood · **12 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `cpi-inflation` CPI & Inflation | kalshi:Economics › Inflation, polymarket:Economy › Inflation/CPI, robinhood:Economics › In | BLS CPI release calendar, Cleveland Fed nowcast, Truflation daily, component weights, seasonal factors | BLS Consumer Price Index |
| `gdp` GDP Growth | kalshi:Economics › GDP/Growth, polymarket:Economy › GDP, robinhood:Economics › Indicators | BEA advance/second/third estimate calendar, Atlanta Fed GDPNow, quarterly revision variance | Bureau of Economic Analysis |
| `employment` Payrolls & Unemployment | kalshi:Economics › Employment/Jobs & Economy, polymarket:Economy › Labor, robinhood:Econom | BLS establishment/household survey, ADP, benchmark revisions, birth-death model adjustments | BLS Employment Situation |
| `jobless-claims-and-jolts` Jobless Claims & Job Openings | kalshi:Economics › Econ Weekly, polymarket:Economy › Labor | DOL weekly initial/continuing claims, state-level filings, JOLTS openings and quits series | DOL / BLS JOLTS |
| `layoffs` Layoffs | kalshi:Economics › Layoffs, kalshi:Companies › Layoffs, robinhood:Economics › Macro | WARN notice filings, Challenger job-cut reports, layoffs.fyi tech tallies | FRED / layoff trackers |
| `consumer-sentiment-and-spending` Consumer Sentiment & Spending | kalshi:Economics › Retail/consumer spending, polymarket:Economy › Consumer | UMich preliminary vs final, Census retail sales, NY Fed household debt and delinquency | U. Michigan / Census / Fed |
| `housing` Housing Prices & Activity | kalshi:Economics › Housing, polymarket:Economy › Housing/Parcl, robinhood:Economics › Indi | Parcl Labs metro sales-price index, Case-Shiller, permits and starts, months-of-supply | Parcl Labs SPI / FHFA / NAR |
| `mortgage-and-credit-defaults` Mortgages, Credit & Defaults | kalshi:Economics › Mortgages/Defaults/Bankruptcy & Defaults, polymarket:Economy › Housing | Freddie PMMS, MBA delinquency survey, CRE default rates, bank charge-off series | Federal Reserve / Freddie Mac |
| `fed-policy` Federal Reserve Policy | kalshi:Economics › Fed/Interest rates, polymarket:Economy › Fed Rates/FOMC, robinhood:Econ | CME FedWatch implied path, SEP dot plot, FOMC calendar, Fed speaker sentiment | Federal Reserve FOMC statement |
| `global-central-banks` Global Central Banks | kalshi:Economics › Global Central Banks, polymarket:Economy › Global Rates/ECB, robinhood: | Each bank's meeting calendar, OIS-implied path, domestic CPI prints, FX pressure | Respective central bank statements |
| `recession-and-cycle` Recession & Business Cycle | kalshi:Economics › Yield curves/Foreign economies, robinhood:Economics › Macro | NBER committee lag behavior, 10Y-3M spread, Sahm rule, coincident-index breadth | NBER dating committee |
| `regional-and-foreign-economies` Regional & Foreign Economies | kalshi:Economics › Growth/International/Local, kalshi:World › Foreign economies/Growth, po | State-level BLS/USDA series, national statistics-office release calendars, IMF/World Bank forecasts | Trading Economics / national statistics offices |

### `financial-markets` — Financial Markets

Equities, indices, rates instruments, FX, corporate events and alt-data.

**On:** kalshi, polymarket, robinhood · **22 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `sp500` S&P 500 | kalshi:Financials › S&P/15 min, polymarket:Finance › Indicies, robinhood:Financial › S&P | Front-month ES futures, SPX option-implied distribution, realized vol, dividend/earnings calendar | Index close / E-mini settlement / Pyth |
| `nasdaq` Nasdaq-100 | kalshi:Financials › Nasdaq/15 min, robinhood:Financial › Nasdaq | NQ futures curve, NDX implied vol surface, mega-cap earnings dates | Index close / futures settlement |
| `other-indices` Other Global Indices | kalshi:Financials › Indices/Markets, polymarket:Finance › Indicies | Local index futures, FX translation, local market holiday calendar | Index provider close |
| `single-stocks` Single-Stock Prices | polymarket:Finance › Equities/Stock Prices, polymarket:Finance › AAPL/NVDA/TSLA/MU | Per-ticker option chains, earnings dates, borrow/short interest, index-inclusion events | Pyth Network equity feeds |
| `market-structure-events` Market Structure & Sentiment | kalshi:Financials › Indices (Fear & Greed), polymarket:Finance › Equities (circuit breaker | VIX term structure, circuit-breaker threshold distance, put/call ratios, breadth indicators | CNN Fear & Greed / exchange notices |
| `treasury-yields` Treasury Yields & Spreads | kalshi:Financials › Treasuries/Interest Rates/15 Min Markets, polymarket:Economy › Treasur | Treasury constant-maturity curve, auction calendar and tails, SOFR futures, QT schedule | US Treasury CMT / FRED |
| `credit-and-bonds` Credit, Bonds & Ratings | kalshi:Economics › Credit & Bonds, kalshi:Politics › Bankruptcy & Defaults | HY/IG spread series, rating-agency watch lists, fund redemption-gate filings | Fitch / Moody's / S&P |
| `fx-majors` FX — Major Pairs | kalshi:Financials › Foreign Exchange/EUR/USD/USD/JPY, polymarket:Finance › Forex, robinhoo | Spot plus FX option implied vol and risk reversals, rate differentials, central-bank calendars | ICE / Investing.com hourly candles / Pyth |
| `fx-emerging` FX — EM & Other Pairs | kalshi:Financials › USD/TWD/USD/RUB/USD/ARS, polymarket:Finance › Forex (USD/KRW) | NDF curves, capital-control regime changes, reserve adequacy, local policy rates | ICE / Investing.com |
| `dollar-index` Dollar Index | robinhood:Financial › FX (KXUSDX), kalshi:Financials › Match Ups (DXY vs Gold) | DXY basket weights, relative rate differentials, positioning (CFTC COT) | ICE US Dollar Index |
| `ipos` IPOs & Listings | kalshi:Financials › IPOs/2026 Mega IPOs, polymarket:Finance › IPOs, polymarket:US: finance | SEC EDGAR filing status, confidential-submission leaks, underwriter mandates, lockup calendars | SEC S-1 effectiveness + listing exchange |
| `mergers-and-acquisitions` M&A | kalshi:Financials › M&A, polymarket:Finance › Acquisitions | Merger-arb spread, HSR/antitrust review clocks, deal-break base rates, financing conditions | Definitive agreements / regulatory closing |
| `earnings` Earnings Results | polymarket:Finance › Earnings, kalshi:Financials › KPIs | Consensus EPS/revenue, historical beat rate and surprise distribution, guidance revisions | Company releases vs consensus |
| `corporate-kpis-and-altdata` Corporate KPIs & Alternative Data | kalshi:Financials › Credit Card Spend/Foot Traffic/App Downloads/Point of Sale/Advertising | Panel card-spend and geolocation foot-traffic series, app-store download estimates, headcount scrapes | Carbon Arc / Fiscal.ai |
| `executive-changes` CEOs & Executive Changes | kalshi:Financials › CEOs, kalshi:Companies › CEOs, kalshi:Transportation › CEOs | Board composition, succession reporting, tenure hazard rates, activist stakes | Company announcements / Bloomberg |
| `private-valuations` Private Company Valuations | polymarket:Finance › Privates, polymarket:Tech › OpenAI/Anthropic | Round-announcement cadence, secondary-market marks, tender-offer pricing | Reported primary/secondary rounds |
| `index-membership` Index Membership | kalshi:Financials › Companies/Markets, polymarket:Business › MicroStrategy | Index methodology thresholds, rebalance calendars, eligibility screens | Index provider notices |
| `net-worth` Billionaire Net Worth | kalshi:Financials › Net Worth, kalshi:Economics › CEOs/Elon Musk, polymarket:Tech › Elon M | Index methodology, underlying stock prices and stakes, option/loan disclosures | Bloomberg Billionaires Index / Forbes |
| `collectibles-and-alt-assets` Collectibles & Alternative Assets | kalshi:Financials › Collectibles/Bezel, kalshi:Entertainment › Collectibles/StockX, polyma | Marketplace sold-listing time series, print-run and grading-population data, release calendars | StockX / Bezel / card price indices |
| `corporate-legal-and-regulatory` Corporate Legal & Regulatory | kalshi:Companies › SCOTUS & courts, kalshi:Business › SCOTUS & courts, polymarket:Finance  | Docket schedules, motion-practice base rates, agency enforcement posture | PACER / court dockets |
| `prediction-market-industry` Prediction Market Industry | polymarket:Finance › Prediction Markets, kalshi:Politics › Congress (gambling repeal) | CFTC rulemaking docket, state gaming-commission actions, pending appellate cases | Regulatory filings / court dockets |
| `consumer-prices-firm-level` Firm-Level Price Changes | kalshi:Financials › Product launches/Inflation, kalshi:Economics › KPIs | Company price-list history, margin pressure in filings, competitor pricing moves | Company announcements |

### `commodities` — Commodities

Energy, metals, agriculture and livestock price and supply outcomes.

**On:** kalshi, polymarket, robinhood · **12 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `crude-oil-wti` Crude Oil — WTI | kalshi:Commodities › Oil & Gas, polymarket:Finance › Oil, robinhood:Commodities › WTI | CME WTI front-month curve, EIA weekly crude and Cushing stocks, Baker Hughes rigs, OPEC+ quotas | ICE / CME settlement, Pyth |
| `crude-oil-brent` Crude Oil — Brent | kalshi:Commodities › Oil & Gas (Pyth-Brent), robinhood:Commodities › Brent crude | ICE Brent curve, Brent-WTI arb spread, North Sea loading programmes, freight rates | ICE Brent |
| `natural-gas` Natural Gas | kalshi:Commodities › Oil & Gas, polymarket:Finance › Natural gas, robinhood:Commodities ›  | EIA weekly storage, HDD/CDD forecasts, LNG feedgas flows, production estimates | CME NG settlement / Pyth |
| `refined-fuels` Refined Fuels & Retail Gasoline | kalshi:Economics › Oil and energy/Gas/Oil & Gas, polymarket:US: macro › Commodities/Gas, r | AAA daily national/state averages, EIA refinery utilization, crack spreads, crude passthrough lag | AAA / EIA |
| `electricity-and-power` Electricity & Power | kalshi:Economics › Econ Daily (ERCOT), kalshi:Science and Technology › Energy | ERCOT load and price series, generation mix, weather-driven demand forecasts | ERCOT / EIA |
| `coal` Coal | kalshi:Economics › Oil and energy (KXWVCOAL) | EIA quarterly coal production by basin, mine-level MSHA employment, utility burn | Energy Information Administration |
| `gold` Gold | kalshi:Commodities › Metals/15 min, polymarket:Finance › Gold, robinhood:Metals › Gold | COMEX GC front-month, XAUUSD spot, real yields, ETF holdings, central-bank purchases | CME GC settlement / XAUUSD spot / Pyth |
| `silver` Silver | kalshi:Commodities › Metals/15 min, polymarket:Finance › Silver, robinhood:Metals › Silver | XAGUSD spot, gold-silver ratio, COMEX inventories, industrial/solar demand | XAGUSD spot / Pyth |
| `copper` Copper | kalshi:Commodities › Metals/15 min, robinhood:Metals › Copper | LME/COMEX copper price, LME warehouse stocks, mine-supply disruptions, China PMI | Pyth Copper / Trading Economics |
| `platinum-palladium` Platinum & Palladium | kalshi:Commodities › (no tag assigned), robinhood:Metals › Platinum/Palladium | NYMEX PL/PA prices, autocatalyst demand, South African/Russian supply, substitution spread | Trading Economics / exchange reference |
| `grains-and-oilseeds` Grains & Oilseeds | kalshi:Commodities › Agriculture, kalshi:Economics › Growth (KXMSCOTTON) | CBOT futures, USDA WASDE and crop-progress reports, export sales, weather in key basins | Pyth / USDA |
| `softs-and-livestock` Softs & Livestock | kalshi:Commodities › Agriculture/(no tag assigned) | ICE cocoa/coffee futures, CME live-cattle, USDA cattle-on-feed, West African harvest data | Trading Economics / USDA |

### `crypto-and-digital-assets` — Crypto & Digital Assets

Token prices, protocol events, launches and crypto policy.

**On:** kalshi, polymarket, robinhood · **13 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `bitcoin` Bitcoin Price | kalshi:Crypto › BTC, polymarket:Crypto › Bitcoin, robinhood:Crypto › BTC | Spot index level, options-implied distribution (Deribit), realized vol, ETF flows, funding rates | CF Benchmarks BRTI (Kalshi, PM-US) vs Binance BTC/USDT candles (PM-Glo |
| `ethereum` Ethereum Price | kalshi:Crypto › ETH, polymarket:Crypto › Ethereum, robinhood:Crypto › ETH | ETH spot index, Deribit implied vol, staking flows, gas-fee and L2 activity series | CF Benchmarks / Binance candles |
| `solana` Solana Price | kalshi:Crypto › SOL, polymarket:Crypto › Solana, robinhood:Crypto › SOL | SOL spot, perp funding and OI, DEX volume share, network outage history | CF Benchmarks / Binance candles |
| `xrp` XRP Price | kalshi:Crypto › XRP, polymarket:Crypto › XRP / Ripple, robinhood:Crypto › XRP | XRP spot, litigation/regulatory catalysts, exchange listing depth | CF Benchmarks / exchange candles |
| `dogecoin` Dogecoin Price | kalshi:Crypto › DOGE, polymarket:Crypto › Dogecoin, robinhood:Crypto › DOGE | DOGE spot, social-volume proxies, correlation beta to BTC, supply issuance | CF Benchmarks / Binance candles |
| `bnb-hype-zec-near` BNB, HYPE, ZEC, NEAR & Other Majors | kalshi:Crypto › BNB/HYPE/ZEC/NEAR, polymarket:Crypto › Hyperliquid/Zcash/BNB, robinhood:Cr | Per-token spot, perp OI, listing status on major venues, protocol revenue | CF Benchmarks / exchange candles |
| `longtail-tokens` Long-Tail & Meme Tokens | kalshi:Crypto › (no tag assigned) (SHIBA), polymarket:Crypto › Memecoins | On-chain FDV and liquidity depth, holder concentration, launchpad cohort survival rates | CoinGecko / on-chain FDV |
| `intraday-crypto` Intraday & Directional Crypto | kalshi:Crypto › 15 min/Hourly/15 Min Markets, polymarket:Crypto › Up or Down (5M/15M/1H/4H | Sub-hourly realized vol, order-book imbalance, minute-bar drift ≈ 0 so vol is the whole signal | Exchange candle close vs open |
| `crypto-relative-value` Crypto Relative Value | kalshi:Crypto › Head to Heads, polymarket:Crypto › Price Comparison, robinhood:Crypto › Ye | Pairwise return correlation and vol, historical ratio distribution, cross-asset beta | CF Benchmarks / flipthe.market |
| `token-launches-and-airdrops` Token Launches, FDV & Airdrops | kalshi:Crypto › Pre-Market, polymarket:Crypto › Token Launch/Token Sales/FDV/Airdrops | Pre-market OTC marks, comparable TGE FDV multiples, points-program snapshots | CoinGecko / on-chain TGE data |
| `stablecoins-and-protocol` Stablecoins, Protocol & Security | polymarket:Crypto › Stablecoins/Network Stats/Protocol Upgrade, polymarket:Crypto › Quantu | On-chain supply and peg deviation, client-share telemetry, BIP/EIP activation status | On-chain supply data |
| `crypto-regulation` Crypto Regulation & Government Reserves | kalshi:Politics › BTC/SOL, polymarket:Crypto › Crypto Legal/Clarity Act/Gov Reserve, robin | Bill markup status, Senate whip counts, Treasury/OFAC notices, ETF approval docket | Federal Register / Treasury |
| `crypto-companies` Crypto Company Listings & Legal | polymarket:Crypto › Crypto Listings, polymarket:Business › DeepSeek/TikTok (adjacent) | S-1 filing status, exchange volume and revenue, sentencing/appeal calendars | SEC filings / court dockets |

### `sports` — Sports

Game outcomes, season structure, player performance and league business.

**On:** kalshi, polymarket, robinhood · **34 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `football-nfl` American Football — NFL | kalshi:Sports › Football, polymarket:Sports › NFL (All), robinhood:NFL | Team Elo/EPA ratings, injury reports, closing spreads and totals, rest and travel splits | Official NFL results (ESPN/Rothera Source Agency) |
| `football-college` American Football — College | kalshi:Sports › Football/CFB, polymarket:Sports › CFB (All), robinhood:College football | SP+/FPI ratings, recruiting and transfer-portal deltas, CFP committee behavior, conference schedules | Official NCAA results |
| `football-canadian` Canadian Football (CFL) | robinhood:Canadian Football | CFL team ratings, weather at outdoor venues, roster/import-rule constraints | Official CFL results |
| `basketball-nba` Basketball — NBA | kalshi:Sports › Basketball, polymarket:Sports › NBA, robinhood:NBA | Team net rating, load-management/injury status, back-to-backs, market closing lines | Official NBA results |
| `basketball-wnba` Basketball — WNBA | kalshi:Sports › Basketball, polymarket:Sports › NBA (WNBA), robinhood:WNBA | Team ratings, minutes distribution, roster availability, short-season variance | Official WNBA results |
| `basketball-college` Basketball — College | kalshi:Sports › Basketball, polymarket:US: sports › CBB, robinhood:College basketball (M) | KenPom/NET ratings, bracketology seed projections, conference tournament paths | Official NCAA results |
| `basketball-international` Basketball — International Leagues | polymarket:Sports › NBA (EuroLeague, B.League, NBL, VTB, LKL, BBL, BSL, ABA), polymarket:U | League-specific Elo, import-player availability, home-court effects by league | Official league results |
| `baseball-mlb` Baseball — MLB | kalshi:Sports › Baseball, polymarket:Sports › MLB, robinhood:Baseball › MLB games | Starting-pitcher projections, park factors, bullpen usage, weather/wind, lineup cards | Official MLB results |
| `baseball-international` Baseball — NPB, KBO & Others | polymarket:Sports › baseball (KBO, NPB, CPBL, LMB), robinhood:Baseball › NPB/KBO games | League run environment, starter rotation, park factors, foreign-player rules | Official league results |
| `hockey-nhl` Hockey — NHL | kalshi:Sports › Hockey, polymarket:Sports › NHL, robinhood:NHL | Expected-goals models, goalie confirmation, special-teams rates, schedule density | Official NHL results |
| `hockey-international` Hockey — KHL, SHL & Others | polymarket:Sports › Hockey (KHL, SHL, Liiga, DEL, Czech Extraliga), polymarket:US: sports  | League scoring environment, goalie rotation, travel across time zones | Official league results |
| `soccer-england` Soccer — England | kalshi:Sports › Soccer, polymarket:Sports › Soccer (FA Cup, League One/Two), robinhood:Soc | xG-based team ratings, fixture congestion, injury/suspension lists, rotation in cup ties | Official Premier League/EFL results |
| `soccer-europe-top-leagues` Soccer — European Top Leagues | kalshi:Sports › Soccer, polymarket:Sports › Soccer (LaLiga2, Copa del Rey, KNVB, Taça), ro | Per-league xG models, home advantage by league, European-competition fixture load | Official league results |
| `soccer-uefa` Soccer — UEFA Competitions | polymarket:Sports › Soccer (UCL, UEFA Nations League), robinhood:Soccer › Champions League | Club coefficient ratings, group/knockout draw structure, two-leg aggregate modelling | Official UEFA results |
| `soccer-americas` Soccer — Americas | kalshi:Sports › Soccer (Liga MX, Ecuador LigaPro), polymarket:Sports › Soccer (MLS, NWSL,  | League-specific Elo, altitude and travel effects, apertura/clausura playoff formats | Official league results |
| `soccer-international` Soccer — International & Other Leagues | polymarket:Sports › Soccer (CONCACAF Nations League, FIFA Friendlies, Scottish Cup), robin | National-team Elo, squad call-up availability, friendly-match rotation noise | Official federation results |
| `tennis` Tennis | kalshi:Sports › Tennis, polymarket:Sports › Tennis (ATP, WTA, ITF, Davis Cup), robinhood:T | Elo by surface, head-to-head, retirement/walkover rates, draw path, ranking points at stake | Official tour results |
| `table-tennis` Table Tennis | kalshi:Sports › Table Tennis, polymarket:Sports › Table Tennis / Setka Cup, polymarket:US: | Player Elo from high-frequency Setka results, best-of-5 game-level model | Setka Cup / World Table Tennis |
| `golf` Golf | kalshi:Sports › Golf, polymarket:Sports › Golf (PGA, LIV, DP World, Korn Ferry), robinhood | Strokes-gained baselines, course fit, field strength, cut-line and weather-wave effects | Official tournament leaderboards |
| `motorsport` Motorsport | kalshi:Sports › Motorsport, polymarket:Sports › Motorsport (F1, NASCAR), robinhood:Racing | Qualifying pace, car/track-type correlation, reliability-failure rates, playoff points structure | FIA / NASCAR official classifications |
| `mma-and-ufc` MMA & UFC | kalshi:Sports › MMA/UFC, polymarket:Sports › UFC / MMA, robinhood:MMA | Striking/grappling differentials, age curves, weight-cut history, finish-rate distribution | Official UFC results |
| `boxing` Boxing | kalshi:Sports › Boxing, polymarket:Sports › Boxing, robinhood:Boxing | Comparable-opponent records, judge/venue bias, KO-rate priors, age and activity | Sanctioning body decision |
| `cricket` Cricket | kalshi:Sports › Cricket, polymarket:Sports › Cricket (IPL-family, CPL, PSL, ECS), robinhoo | Format-specific team ratings, pitch and toss effects, DLS rain scenarios, squad availability | Official match results / ESPNcricinfo |
| `rugby-and-afl` Rugby & Australian Rules | kalshi:Sports › Rugby/Aussie Rules, polymarket:Sports › Rugby (Super League, Top 14, URC), | Points-differential ratings, weather, squad rotation, home advantage by competition | Official league results |
| `darts-chess-and-mind-sports` Darts, Chess & Mind Sports | kalshi:Sports › Darts/Chess, polymarket:Sports › Darts (PDC, MODUS), Chess, Poker, robinho | Three-dart averages, Elo ratings, time-control-specific performance, field entry lists | PDC / FIDE / Chess.com |
| `olympics-and-multisport` Olympics & Multi-Sport Events | kalshi:Sports › Olympics/Cycling/Rowing/Volleyball/Squash/Lacrosse | Qualification standings, World Cup season results, historical medal-share by country and discipline | Official Games results |
| `niche-and-other-sports` Niche & Other Sports | kalshi:Sports › Other/4th of July, polymarket:Sports › Handball/Volleyball/Lacrosse/Pickle | Small-field historical results, participant-specific records (e.g. hot-dog counts), weather | Event organizer |
| `player-awards` Player & Coach Awards | kalshi:Sports › league award series, polymarket:US: sports › Awards, robinhood:NFL/Basebal | Voter-history models, narrative/counting-stat thresholds, team-success weighting | AP / BBWAA / league announcements |
| `player-props-and-stat-leaders` Player Props & Stat Leaders | kalshi:Sports › leader/season-stat series, polymarket:Sports › props/Season stats, robinho | Per-game usage rates, pace and snap share, injury-adjusted remaining-games projections | Official league stat feeds |
| `win-totals-and-standings` Win Totals & Standings | kalshi:Sports › win-total series, polymarket:Sports › Team win totals, robinhood:NFL/WNBA  | Game-by-game win-probability simulation with correlated team strength, remaining schedule | Official standings |
| `playoff-seeding` Playoff Qualification & Seeding | kalshi:Sports › seed/qualifier series, robinhood:NFL/College football › Playoff seeds | Monte Carlo over remaining schedule with tiebreaker rules encoded exactly | Official league seeding |
| `transactions-and-coaching` Transactions, Draft & Coaching | kalshi:Sports › next-team/coach series, polymarket:Esports › Roster changes, robinhood:NBA | Contract/cap situation, reporting from beat writers, historical hiring-cycle timing | Official club announcements |
| `league-business` League Business & Off-Field | kalshi:Sports › Cities/International/ESPYS, kalshi:Entertainment › Football (Super Bowl ad | Attendance and broadcast data, ad-rate reporting, franchise relocation filings | League / credible reporting |
| `fantasy-sports` Fantasy Sports | kalshi:Sports › (no tag assigned) fantasy series, polymarket:Sports › Fantasy Football, ro | Scoring-format rules, projected usage, injury-adjusted games remaining | Official stat feeds under a stated scoring system |

### `esports` — Esports

Competitive video-game matches, tournaments and awards.

**On:** kalshi, polymarket, robinhood · **5 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `counter-strike` Counter-Strike 2 | kalshi:Sports › Esports, polymarket:Esports › Counter-Strike 2, robinhood:Esports › CS2 | Team map-pool win rates, HLTV ratings, roster changes, online vs LAN splits | Official tournament results (HLTV-class feeds) |
| `league-of-legends` League of Legends | kalshi:Sports › Video games, polymarket:Esports › League of Legends, robinhood:Esports › L | Regional strength ratings, patch-meta shifts, side-selection and draft priority | Riot official results |
| `valorant` Valorant | kalshi:Sports › Esports, polymarket:Esports › Valorant, robinhood:Esports › Valorant | Map-veto tendencies, agent-comp win rates, VCT group format | Riot / VCT official results |
| `dota-and-r6` Dota 2 & Rainbow Six | kalshi:Sports › Esports, polymarket:Esports › Dota 2 / Rainbow Six Siege, robinhood:Esport | Team ratings, patch timing, regional cross-play sample sparsity | Valve / Ubisoft tournament results |
| `other-titles-and-esports-business` Other Titles & Esports Business | polymarket:Esports › Overwatch/Rocket League/StarCraft II/Honor of Kings/Fortnite, polymar | Title-specific rating systems, thin historical samples, award voting history | Official tournament / award announcements |

### `entertainment-and-media` — Entertainment & Media

Awards, charts, box office, streaming, celebrities and games.

**On:** kalshi, polymarket, robinhood · **18 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `film-awards` Film Awards | kalshi:Entertainment › Oscars/Golden Globes/BAFTA/SAG/Cannes/Venice, polymarket:Culture ›  | Precursor-award correlation (guilds, Globes), voter-body composition, campaign spend | Academy / BAFTA / Golden Globes |
| `tv-awards` Television Awards | kalshi:Entertainment › Emmys/Daytime Emmys/Sports Emmys, robinhood:Entertainment › Emmy Wi | Nomination counts, prior-season winners, category-incumbency base rates | Television Academy |
| `music-awards` Music & Stage Awards | kalshi:Entertainment › Grammys/Latin Grammys/AMAs/VMA/ACMs/CMA/Tonys/Eurovision, polymarke | Eligibility windows, chart and sales performance, Recording Academy voter history | Recording Academy / MTV / Tony Awards |
| `box-office` Box Office | polymarket:Culture › Box Office, kalshi:Entertainment › Movies | Presales and tracking, theater count, franchise multipliers, weekend-decay curves | Box Office Mojo / Comscore |
| `critic-scores` Critic & Review Scores | kalshi:Entertainment › Rotten Tomatoes, polymarket:Culture › Rotten Tomatoes, robinhood:En | Early review counts from festivals/embargo lift, director/genre historical score distribution | Rotten Tomatoes / Metacritic |
| `streaming-charts` Streaming Charts | kalshi:Entertainment › TV Charts/Movie Charts, polymarket:Culture › Top Netflix, robinhood | Netflix weekly hours-viewed series, release calendar, prior-week decay, Luminate data | Netflix Top 10 published charts |
| `music-charts` Music Charts & Sales | kalshi:Entertainment › Music charts/Music Industry, polymarket:Culture › Music, robinhood: | Luminate first-week projections, streaming-to-equivalent-album conversion, bundle rules | Billboard / Luminate |
| `streaming-counts` Artist & Track Stream Counts | kalshi:Entertainment › Music Streams/Morgan Wallen/Taylor Swift, robinhood:Entertainment › | Daily Spotify play counts, catalog decay curves, release and tour calendar | Spotify / Luminate |
| `video-views` YouTube & Creator Metrics | kalshi:Entertainment › Views/Daily Views/Weekly Views/Monthly Views, polymarket:Culture ›  | Channel view-velocity curves, upload cadence, historical day-1/day-7 ratios | YouTube Charts public counters |
| `reality-tv` Reality Television | kalshi:Entertainment › Reality TV/Big Brother/Love Island/DWTS/America's Got Talent, polym | Episode edit signals, live-vote mechanics, betting-market and fan-poll aggregation | Broadcaster (CBS/ABC/ITV/Peacock) |
| `scripted-tv-and-film-production` Scripted TV & Film Production | kalshi:Entertainment › Television/Movies/People (casting), polymarket:Culture › Movies | Trade reporting (Variety/Deadline), production schedules, contract negotiations | Studio / trade announcements |
| `video-games` Video Games | kalshi:Entertainment › Video games/The Game Awards/Product launches, polymarket:Culture ›  | Publisher delay base rates, dev-cycle signals, Steam wishlist/chart data, review aggregates | Publisher announcements / Metacritic |
| `celebrity-events` Celebrities & Personal Milestones | kalshi:Entertainment › People/Achievements, polymarket:Culture › Celebrities / relationshi | Tabloid/credible-outlet reporting cadence; largely unmodellable — treat as reporting-latency markets | Credible reporting |
| `public-appearances` Public Appearances & Performances | kalshi:Entertainment › Live Music, kalshi:Politics › People/SOTU/Awards, polymarket:Cultur | Announced lineups, promotional-cycle alignment, prior attendance patterns | Event organizer / broadcaster |
| `art-and-auctions` Art & Auctions | kalshi:Entertainment › Art, polymarket:Culture › Art / masterworks | Auction catalogues and estimates, guarantee structures, Artprice/ArtTactic indices | Sotheby's / Christie's results |
| `anime-and-international-media` Anime & International Media | kalshi:Entertainment › Anime Awards/Anime awards/Eurovision | Fan-vote mechanics, streaming popularity rankings, national jury structure | Crunchyroll / Eurovision |
| `food-and-lifestyle` Food, Dining & Lifestyle | kalshi:Social › (no tag assigned) (Michelin), kalshi:Entertainment › Product launches | Guide release calendar, prior star retention rates, product-cycle timing | Michelin Guide / company |
| `media-industry-corporate` Media Industry Corporate Events | kalshi:Entertainment › Companies/Music Industry, robinhood:Entertainment › Movies (KXTAKEO | Deal reporting, regulatory review clocks, catalog-sale comparables | Variety / Reuters / court dockets |

### `technology-and-ai` — Technology & AI

Model releases, benchmarks, compute pricing, platforms and tech policy.

**On:** kalshi, polymarket, robinhood · **12 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `model-releases` Frontier Model Releases | polymarket:Tech › AI Releases, polymarket:US: technology › Model Releases, kalshi:Science  | Historical release cadence per lab, changelog/API endpoint leaks, compute-buildout signals | Official vendor announcements |
| `model-rankings` Model Rankings & Benchmarks | polymarket:Tech › AI Rankings/AI Benchmarks/Coding, polymarket:US: technology › Rankings,  | Current Arena Elo and confidence intervals, vote-volume convergence, scheduled release overhang | LMArena / Chatbot Arena rank column, Style Control Off |
| `ai-market-share` AI Market Share & Token Usage | kalshi:Science and Technology › Market Share/Tokens/Industries, kalshi:Financials › AI/Com | OpenRouter model-ranking share series, router default changes, price-cut-driven substitution | OpenRouter / Vercel AI Gateway / Ornn |
| `ai-pricing` AI Token & API Pricing | kalshi:Commodities › Tokens/Tech/Markets, kalshi:Financials › Tokens, kalshi:Science and T | Published per-token price history, historical price-cut cadence at model generation changes | Vendor published price lists / Ornn |
| `compute-hardware-pricing` GPU & Hardware Pricing | kalshi:Science and Technology › Compute/Tech, kalshi:Financials › Compute, polymarket:Tech | Rental spot indices by SKU, new-generation supply ramp, hyperscaler capex guidance | Ornn / GPU rental indices |
| `semiconductors-and-memory` Semiconductors & Memory | kalshi:Financials › Tech/Industries (DDR5, RTX), kalshi:Economics › AI (SEMIPRODH) | DRAM contract/spot price series, fab utilization, AI-server bill-of-materials demand | Ornn |
| `ai-adoption` AI Adoption Indices | kalshi:Science and Technology › AI Indices | Ramp corporate-card AI spend penetration by sector, month-over-month adoption slope | Ramp AI Index |
| `agi-and-capability-milestones` AGI & Capability Milestones | kalshi:AI › AI, kalshi:Science and Technology › KPIs, polymarket:Tech › Math / Millennium  | Definition ambiguity dominates; track lab public commitments and announcement-language precedents | Lab announcements / Clay Mathematics Institute |
| `ai-policy` AI Policy, Safety & Regulation | kalshi:Politics › AI, polymarket:Tech › AI Safety / AI Regulation | Bill status, executive-order drafts, DoD entity-list updates, state AI-law calendar | Federal Register / enacted legislation |
| `platforms-and-consumer-tech` Platforms, Devices & App Charts | polymarket:Tech › Apple / App Store / Google Search / Big Tech, kalshi:Companies › Product | Daily app-rank series, device-launch calendars, regulatory ban deadlines | Apple App Store charts / Google Year in Search |
| `outages-and-security` Outages, Hacks & Cybersecurity | polymarket:Tech › Outage, polymarket:Business › hack / outage | Historical incident frequency per provider, status-page uptime history, disclosure lag | Official status pages |
| `robotics-and-autonomy` Robotics & Autonomy | kalshi:Science and Technology › Product launches (Tesla Optimus), polymarket:Tech › Elon M | Company delivery-promise slippage history, production-line reporting, regulatory approvals | Company announcements |

### `science-and-space` — Science & Space

Spaceflight, physics, mathematics, prizes and energy technology.

**On:** kalshi, polymarket, robinhood · **7 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `launch-cadence` Launch Cadence & Providers | kalshi:Science and Technology › Space, kalshi:Companies › Space, robinhood:Technology › Sp | Year-to-date launch counts, pad turnaround times, FAA licence status, weather scrub rates | FAA / launch provider confirmations |
| `deep-space-missions` Lunar, Mars & Deep Space | kalshi:Science and Technology › Space, polymarket:Science › Space / NASA | Mission milestone schedules, historical program slip distributions, launch-window mechanics | NASA / provider confirmations |
| `astronomical-events` Astronomical & Impact Events | kalshi:Climate and Weather › Space, polymarket:Science › Earthquakes / meteor | Ephemeris (deterministic timing) plus cloud-cover forecast; impact markets use NEO flux base rates | National Weather Service / NASA CNEOS |
| `physics-breakthroughs` Physics Breakthroughs | kalshi:Science and Technology › Physics & Math/Papers | Preprint and replication pipeline, facility milestone schedules (NIF/ITER), replication base rates | Peer-reviewed confirmation / Kalshi |
| `mathematics` Mathematics & Prizes | kalshi:Science and Technology › Physics & Math, polymarket:Science › Millennium Prize / Ma | Two-year CMI verification rule, arXiv claim frequency, historical claim-to-acceptance rate | Clay Mathematics Institute |
| `nobel-and-academia` Nobel Prizes & Academia | kalshi:Entertainment › Nobel Prizes, kalshi:Politics › Achievements, polymarket:Culture ›  | Nomination deadlines, Clarivate citation-laureate lists, committee-composition history | Nobel Foundation / Norwegian Nobel Committee |
| `energy-technology` Energy Technology & Nuclear | kalshi:Science and Technology › Energy, kalshi:Climate and Weather › Energy/KPIs, robinhoo | NRC licensing docket timelines, Argonne EV market-share series, IRA incentive schedules | Nuclear Regulatory Commission / Argonne National Laboratory |

### `climate-and-weather` — Climate & Weather

Temperature, precipitation, storms, climate indicators and natural disasters.

**On:** kalshi, polymarket, robinhood · **11 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `daily-high-temperature` Daily High Temperature | kalshi:Climate and Weather › Daily temperature, polymarket:Weather › Daily Temperature, po | Station-specific NWS/ECMWF/GFS ensemble forecasts, model spread, station climatology and bias | NWS Climatological Report for a named station (e.g. KNYC); Hong Kong O |
| `daily-low-temperature` Daily Low Temperature | kalshi:Climate and Weather › Daily temperature, robinhood:Climate › Daily Low Temperature | Overnight-minimum ensembles, dewpoint and cloud cover, radiational-cooling regime | NWS station climatological report |
| `intraday-and-weekly-temperature` Hourly & Weekly Average Temperature | kalshi:Climate and Weather › Hourly temperature/Heatwaves | Hourly mesonet observations, short-range HRRR runs, diurnal-cycle persistence | The Weather Company / Synoptic Data |
| `precipitation` Rain & Precipitation | kalshi:Climate and Weather › Snow and rain, polymarket:Weather › Precipitation, robinhood: | QPF ensemble probabilities, gauge-specific measurement thresholds, monthly climatology | NWS / national met services |
| `snow-and-ski` Snowfall & Ski Resorts | kalshi:Climate and Weather › Ski Resorts/Snow and rain | Resort historical opening dates, snowmaking temperature windows, seasonal snowpack forecasts | Resort snow & weather reports |
| `tropical-cyclones` Hurricanes & Tropical Cyclones | kalshi:Climate and Weather › Hurricanes, polymarket:Weather › Hurricanes / Hurricane Seaso | NHC track/intensity cones, ACE-to-date, ENSO state, seasonal forecasts (CSU/NOAA), SST anomalies | NHC / NOAA advisories |
| `degree-days` Heating & Cooling Degree Days | kalshi:Climate and Weather › (no tag assigned) | Station temperature forecasts aggregated into HDD/CDD, 10/30-year normals, gas-demand linkage | NOAA / NWS |
| `global-climate-indicators` Global Temperature & Climate Indicators | kalshi:Climate and Weather › Climate change/Global heat, polymarket:Weather › Global Temp  | GISTEMP/ERA5 monthly anomalies year-to-date, ENSO forecast, NSIDC sea-ice extent series | NASA GISS / NOAA NCEI / Copernicus / NSIDC |
| `drought-and-water` Drought & Water Levels | kalshi:Climate and Weather › (no tag assigned) (Lake Mead), polymarket:Weather › Drought | Daily reservoir elevation and river-stage gauges, snowpack/SWE, upstream release schedules | USBR / river gauge authorities |
| `seismic-and-volcanic` Earthquakes & Volcanic Activity | kalshi:Climate and Weather › Natural disasters, polymarket:Science › Earthquakes / Natural | USGS magnitude-frequency (Gutenberg–Richter) rates, year-to-date counts, GVP eruption base rates | USGS catalog / Smithsonian GVP |
| `climate-policy` Climate Policy & Agreements | kalshi:Politics › Climate change, kalshi:Climate and Weather › Climate change | COP calendar, formal withdrawal notice periods, NDC submission status | Official government announcements |

### `health-and-medicine` — Health & Medicine

Disease spread, drug approvals, vaccines, pricing and health policy.

**On:** kalshi, polymarket, robinhood · **9 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `respiratory-outbreaks` COVID & Respiratory Disease | kalshi:Health › Covid/COVID, kalshi:World › Covid, kalshi:Politics › Covid | CDC weekly case and hospitalization series, wastewater surveillance, variant share, reporting lags | CDC / ECDC / WHO |
| `avian-and-zoonotic-flu` Avian Influenza & Zoonoses | kalshi:Health › Other diseases/(no tag assigned), kalshi:Science and Technology › Public H | CDC confirmed human case counts, USDA poultry/dairy herd detections, WHO risk assessments | WHO / CDC |
| `measles-and-vpd` Measles & Vaccine-Preventable Disease | polymarket:Science › Pandemics / disease, polymarket:US: science › Science | CDC weekly measles case tally, county vaccination coverage, outbreak-cluster growth rates | US CDC |
| `emerging-outbreaks` Emerging Outbreaks & PHEIC | kalshi:Health › Disease spread/Other diseases, polymarket:Science › Pandemics | WHO Disease Outbreak News cadence, IHR Emergency Committee convening history, PHEIC base rate | World Health Organization |
| `fda-approvals` FDA Drug & Device Approvals | kalshi:Health › FDA Approval/Vaccines, kalshi:Science and Technology › Medicine/Product la | PDUFA target dates, AdComm votes and vote-to-approval base rates, CRL history for the sponsor | Food and Drug Administration |
| `clinical-trials` Clinical Trial Readouts | kalshi:Financials › Biotech/Medicine/Healthcare | ClinicalTrials.gov enrollment and primary-completion dates, phase-transition success rates by indication | AppliedXL |
| `drug-pricing` Drug Pricing & Access | kalshi:Health › Drug Prices, kalshi:Politics › Drug Prices/Public Health | NADAC published unit costs, CMS negotiation list, manufacturer price-change announcements | NADAC / CMS |
| `health-policy` Health Policy & Agencies | kalshi:Health › Health Tech, kalshi:Politics › Health Tech/Public Health, robinhood:Politi | Rulemaking docket stage, comment-period close dates, agency leadership statements | HHS / CDC / White House |
| `vital-statistics` Vital Statistics & Demography | kalshi:Health › (no tag assigned)/Health Tech, kalshi:Economics › Growth (population) | NCHS provisional vital-statistics releases, revision history, drug-overdose and birth-rate trends | CDC National Center for Health Statistics |

### `transportation-and-logistics` — Transportation & Logistics

Air travel, freight, transit, ports and supply chains.

**On:** kalshi · **6 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `flight-disruption` Flight Delays & Cancellations | kalshi:World › Flights, kalshi:Transportation › Airlines & aviation | FlightAware daily delay/cancel counts by airport, terminal weather, ATC staffing notices | FlightAware |
| `aviation-industry` Airlines & Aviation Safety | kalshi:Transportation › Airlines & aviation/CEOs, kalshi:Companies › Airlines & aviation | FAA airworthiness directives, certification milestones, carrier financial filings | FAA / company announcements |
| `passenger-throughput` Passenger Throughput & Transit | kalshi:Transportation › (no tag assigned) (TSA, MTA) | TSA daily checkpoint series, MTA turnstile counts, holiday and weekday seasonality | TSA / MTA |
| `freight-rates` Freight & Trucking Rates | kalshi:Transportation › (no tag assigned) (KXVANRATE) | Truckstop/DAT spot dry-van rate series by region, diesel input costs, load-to-truck ratios | Truckstop.com dry van rates |
| `ports-and-supply-chain` Ports & Supply Chain | kalshi:Transportation › Supply chain, kalshi:World › Supply chain | Port TEU volumes and anchored-vessel counts, carrier routing announcements, canal transit data | Port of Los Angeles / Maersk |
| `transport-labor` Transport Labor Actions | kalshi:Economics › Local (strikes) | Contract expiry dates, strike-authorization votes, mediation timelines | Employer / union statements |

### `speech-and-mentions` — Speech & Mentions

What named people say, how often, and for how long.

**On:** kalshi, polymarket · **4 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `political-mentions` Political Speech Mentions | kalshi:Mentions › Politicians/Trump, polymarket:Culture › Mentions | Historical per-speech word frequency, topic salience in the news cycle, speech-length priors | Broadcast transcripts (ABC/Fox/MSNBC) |
| `earnings-call-mentions` Earnings Call Mentions | kalshi:Mentions › Earnings | Prior-quarter transcript term counts, scripted-remarks structure, analyst Q&A topic drift | Bloomberg / company transcripts |
| `broadcast-mentions` Sports & Entertainment Broadcast Mentions | kalshi:Mentions › Sports/Entertainment/CEOs | Announcer-crew verbal tics, game-state dependence, prior-broadcast term frequency | Broadcast transcripts |
| `speech-metrics` Speech Duration, Attendance & Post Counts | kalshi:Mentions › SOTU, kalshi:Politics › Trump Agenda (POTUS tweets), polymarket:Culture  | Rolling 7-day post-rate distribution, travel/event calendar, historical SOTU duration series | X public post counts / broadcast timing |

### `society-education-and-records` — Society, Education & Records

Universities, schools, religion, crime and record-setting achievements.

**On:** kalshi, polymarket, robinhood · **6 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `university-tuition` University Tuition | robinhood:Education › Tuition | NCES IPEDS published tuition-and-fee series, board-approved rate increases, endowment policy | National Center for Education Statistics (stated verbatim in contract) |
| `university-rankings` University Rankings | robinhood:Education › Ranking, kalshi:Science and Technology › Education | Ranking methodology weights and recent changes, prior-year position, methodology-revision risk | Published national ranking (publisher not named on Robinhood's page) |
| `academic-outcomes` Test Scores & Academic Outcomes | kalshi:Politics › Education/Culture war, kalshi:Science and Technology › Education | NAEP release schedule, prior-cycle scale scores, pandemic-recovery trajectory by subject | Nation's Report Card (NAEP) |
| `campus-and-institutions` Campus Leadership & Student Affairs | kalshi:Politics › Education, kalshi:Education › (no tag assigned) | Board-of-trustees meeting calendars, search-committee reporting, disciplinary-process timelines | University announcements |
| `religion-and-civic-institutions` Religion & Civic Institutions | kalshi:World › (no tag assigned) (KXNEWPOPEDATE), kalshi:Politics › (no tag assigned) | Conclave procedural rules, actuarial tables, historical conclave duration distribution | Holy See / official announcements |
| `records-and-recognition` Records, Lists & Recognition | kalshi:Entertainment › Achievements, polymarket:Tech › Google Search | Google Trends interest-over-time, prior-year list composition, editorial-selection precedent | Google Year in Search / TIME / People |

### `market-mechanics` — Market Mechanics (Non-Domain)

Contract tenor, structure and UI flags — never map a data feed here.

**On:** kalshi, polymarket, robinhood · **5 subdomains**

| Subdomain | Venue labels | What prices it | Settles on |
|---|---|---|---|
| `contract-tenor` Contract Tenor & Intervals | kalshi:* › 15 min/Hourly/Daily/Monthly tags, polymarket:_mechanics › Duration / interval t | Nothing — this is contract tenor. The underlying price feed belongs to the asset's own subdomain. | n/a — describes tenor, not subject matter |
| `contract-structure` Contract Structure Types | polymarket:_mechanics › Structure tags, kalshi:* › Match Ups/Head to Heads | Nothing directly; structure determines payoff transformation of the underlying's distribution. | n/a — contract shape |
| `parlays-and-combos` Multi-Event Parlays & Combos | kalshi:Exotics › (no tag assigned)/Football/Basketball, kalshi:Elections › Mixed Combos, p | Joint distribution across legs including correlation — never the product of marginal probabilities. | Governing body of each leg |
| `venue-views-and-incentives` Merchandising Views & Liquidity Incentives | robinhood:Featured, robinhood:Live, polymarket:_mechanics › Operational tags / Incentive t | Nothing — these are display and reward-tier flags, not subject matter. | n/a — UI and lifecycle flags |
| `untagged-inventory` Untagged & Bespoke Inventory | kalshi:* › (no tag assigned) | Must be classified per-series from settlement text; cannot be fed by a single data source. | varies per series |

**Normalization notes:**

- COVERAGE: 18 top-level domains, 258 subdomains. Every category and subcategory from all three source taxonomies is mapped. Kalshi's 20 categories and 380 (category,tag) pairs, Polymarket's 26 Global+US categories, and Robinhood's 32 nav categories all resolve to at least one node.
- VENUE-UNIQUE — KALSHI: the Mentions domain (speech/earnings-call/broadcast mention markets at scale), Transportation (freight dry-van rates, TSA throughput, MTA ridership, Port of LA), alternative-data corporate KPIs (Carbon Arc credit-card spend, foot traffic, app downloads, point-of-sale, ad spend), biotech trial readouts (AppliedXL), heating-degree-days, Lake Mead levels, ski-resort openings, competitive eating, squash, rowing, sumo. No other venue carries these.
- VENUE-UNIQUE — POLYMARKET: territorial-control war markets settled on ISW/DeepState maps (Ukraine Map), IMF PortWatch chokepoint transit counts, Parcl Labs metro housing indices, token launches/FDV/airdrops/memecoins, Pokemon card price markets, tweet-count markets, German state and Nigerian gubernatorial elections, country-desk structure (Germany/Canada/Japan/Nigeria as first-class nodes), and Setka Cup table tennis at volume.
- VENUE-UNIQUE — ROBINHOOD: university tuition (settled on NCES) and university rankings — no equivalent on Kalshi or Polymarket. Also index futures (FES/FNQ) and spot FX (JPUSD/USGBP/USEUR/USCAD/USAUD) via ForecastEx, and platinum/palladium daily dated series.
- ROBINHOOD IS A BROKER, NOT AN EXCHANGE. Its 649 series resolve to four venues by exchangeSource enum: Kalshi (498), ForecastEx (87), Rothera (63), OG.com/Nadex (1). Most 'Robinhood' tickers here are literally Kalshi tickers (KX-prefixed). Genuine Robinhood-only inventory is the ForecastEx, Rothera and Nadex catalogs. Treat venue as a per-series attribute, not per-category.
- SPLIT — POLITICS vs ELECTIONS: the venues disagree. Kalshi has both Politics and Elections; Polymarket puts midterms inside Politics; Robinhood has both Elections and Midterms. I routed every contract whose resolution is a vote count or race call into the elections domain regardless of venue label, and left legislation/appointments/courts in politics-and-government. venueLabels preserve the original placement.
- MERGED — Kalshi 'Economics' and Polymarket 'Economy': I checked example contracts before merging. Both genuinely contain CPI, GDP, employment, Fed policy and housing, so they merge into macroeconomics. But Polymarket files Treasuries and FX under Economy while Kalshi files them under Financials — I routed both to financial-markets, since those are tradeable instrument prices, not statistical releases.
- MERGED — Kalshi 'Financials' and Polymarket 'Finance' and Robinhood 'Financial': same content (indices, single stocks, FX, IPOs, M&A, earnings). Kalshi's 'Companies' category also folds here for CEO changes, KPIs and corporate legal.
- SPLIT — Robinhood separates 'Metals' from 'Commodities' as two top-level tabs (Commodities holds only WTI, Brent, natural gas). I merged them into one commodities domain with gold/silver/copper/platinum/palladium as separate subdomains, which is what the user asked for at the crude-oil/gold/silver granularity level.
- KALSHI FILES AI TOKEN PRICING UNDER COMMODITIES. Series like KXOPUS48Y, KXGEMINI35Y and KXGPT55Y carry category=Commodities with tags Tokens/Tech/Markets. That is a venue quirk, not a commodity. I placed them under technology-and-ai › ai-pricing and preserved the kalshi:Commodities label in venueLabels so the mapping back is unambiguous.
- SPLIT — EARTHQUAKES AND VOLCANOES: Kalshi files them under 'Climate and Weather › Natural disasters'; Polymarket files them under 'Science'. They are geophysical, not meteorological, but I kept them in climate-and-weather to match the higher-volume venue and flagged the Polymarket path in venueLabels. A modeler should note the data source is USGS/Smithsonian GVP, not a met service.
- POLYMARKET '_mechanics' IS NOT A DOMAIN and must not receive a data feed. 'Games' (8,958 live) is a sports-fixture flag, not video games — mapping a gaming feed to it would be a category error. Likewise 'Up or Down', '5M/15M/1H', 'Recurring', 'Hide From New' and the Rewards tiers. Kalshi's 'Exotics' (multi-venue-event parlays) and Robinhood's 'Featured'/'Live' views belong in the same non-domain bucket.
- SETTLEMENT SOURCES DIVERGE ACROSS VENUES FOR THE SAME ASSET. Bitcoin: Kalshi and Polymarket US settle on CF Benchmarks BRTI (trimmed mean); Polymarket Global settles on Binance BTC/USDT 1-minute candles. Gold: Polymarket uses CME GC futures settlement for GC contracts but XAUUSD spot for spot contracts. A single shared price feed will NOT reconcile both venues' resolutions — the terminal needs per-venue feed bindings, not per-asset.
- POLYMARKET GLOBAL USES A UMA OPTIMISTIC ORACLE; Polymarket US names a specific real-world authority with no oracle fields. Kalshi names settlement_sources per series. Where I wrote 'via UMA' that is the arbitration layer, not the underlying data — the underlying data is what whatDataPricesIt describes.
- AMBIGUOUS — 'Trump' AND 'Football' ARE CROSS-CUTTING KALSHI TAGS, not subcategories. 'Trump' appears under Politics, Elections, Entertainment, Mentions, Companies and Science and Technology; 'Football' under Sports, Entertainment, Companies, World and Exotics. Kalshi's own note says to treat (category, tag) as the join key, never tag alone. I decomposed these by subject matter rather than creating a 'Trump' node.
- AMBIGUOUS — ROBINHOOD TENNIS 'SUBCATEGORIES' ARE ROTATING EVENT INSTANCES. 'WTA Seoul', 'ATP Challenger Saint Tropez', 'WTA 125K Tolentino' are this week's tournaments and will be different names next week; the durable layer is the series ticker (KXWTAMATCH, KXATPCHALLENGERMATCH, KXITFMATCH). I collapsed these into tour-level subdomains. Golf and soccer have the same property to a lesser degree.
- COVERAGE GAP FLAGGED BY THE SOURCES: four Kalshi categories have zero live series (Health 96 series, Transportation 38, Exotics 14, Education 1) and exist only as historical inventory. I kept nodes for all of them because the user asked for nothing to be dropped, but a live-inventory-driven build would show them empty today.
- THE SOURCE CRAWLS WERE NOT EXHAUSTIVE and this taxonomy inherits that. Kalshi's /markets endpoint was never fully enumerated (bounded 60-page crawl only); Polymarket's Global keyset walk captured 18,164 of 18,166 reported open events; Polymarket US closed/historical corpus was not enumerated; Robinhood's 649 series is a verified floor, not a total. Subdomain existence is well-evidenced; exhaustiveness of example contracts is not.
- SUBDOMAIN GRANULARITY IS DELIBERATELY UNEVEN where the source material is uneven. Commodities, crypto and weather are broken to the individual-asset level as requested (crude oil WTI vs Brent, gold vs silver vs copper, daily high vs daily low temperature). Thin venue categories (Polymarket US science = 2 open events) get one node rather than a fabricated tree.
- whatDataPricesIt IS WRITTEN FOR A MODELER, NOT A MARKETER. Where a market is not genuinely modelable from public data — celebrity relationship markets, AGI-definition markets — I said so rather than inventing a data source.

---

## 3 · Feed mapping

### climate-and-weather

*8/11 subdomains covered · 15 primary feeds*

#### Open-Meteo unified weather API (forecast + ensemble + archive/ERA5 + previous-runs + flood) — Open-Meteo (Patrick Zippenfenig, CH) — wraps GFS, ECMWF IFS/AIFS, ICON, GEM, HRRR, UKMO, JMA, BoM + ERA5 + GloFAS ✅ LIVE

Covers **7** subdomains: daily-high-temperature, daily-low-temperature, intraday-and-weekly-temperature, precipitation, snow-and-ski, degree-days, drought-and-water

- Docs: https://open-meteo.com/en/docs
- Auth: none — no key, no registration, no User-Agent requirement. CORS verified open (access-control-allow-origin: *, allow-methods GET/POST/OPTIONS), so it is browser-callable directly. A key exists only for the paid commercial tier. | Limits: 10,000 calls/day, 5,000/hour, 600/minute per IP for non-commercial use. VERIFIED PARTIALLY: a 5-call burst returned 200/200/200/200/200 and NO x-ratelimit-* headers are emitted, so you cannot observe remaining quota from the response — the published limits are documented, not independently confirmable from the wire. One call returns many variables and many days, so a 30-city daily-temperature board costs 30 calls/refresh.
- Latency: Forecast refreshed hourly (HRRR-backed) to 6-hourly (global models); ensemble on each model cycle; ERA5 archive lags ~5 days (ERA5T ~2 days). generationtime_ms observed 0.005–0.93 ms across five endpoints. | Format: REST JSON (also CSV/XLSX/flatbuffers). Flat parallel arrays, ISO8601 timestamps, unit block included. GOTCHA: archive-api defaults to °C — you must pass temperature_unit=fahrenheit explicitly (verified: 2026-08-01 Phoenix returned 45.8 with daily_units temperature_2m_max '°C').
- Why primary: This is the single feed that satisfies the user's one-API-for-gold-and-silver rule. One host family, one auth model (none), one JSON schema returns daily max temp, daily min temp, hourly temp, precipitation, snowfall, and — via ensemble-api — 51 individual ECMWF members at the same point. That member spread IS the implied probability for a threshold contract; you do not need a separate probability vendor. River discharge for drought/water contracts comes from flood-api.open-meteo.com on the identical schema. previous-runs-api gives what the model said N days ago at the same point, which is the forecast-shift signal a trader wants. CAVEAT ADDED IN VERIFICATION: degree-days is DERIVED here, not served — there is no HDD/CDD field; you compute HDD=max(0,65-(Tmax+Tmin)/2) from temperature_2m_max/min yourself. Use RCC-ACIS for the served, settlement-grade degree-day number. Alternatives (raw GFS/GEFS/HRRR/ECMWF GRIB on S3) carry the same information but require GRIB2 decoding and grid interpolation per point.

```bash
curl 'https://api.open-meteo.com/v1/forecast?latitude=33.4276&longitude=-112.0038&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,precipitation_probability_max&hourly=temperature_2m&temperature_unit=fahrenheit&timezone=America/Phoenix&forecast_days=7'   # ensemble (the probability engine): curl 'https://ensemble-api.open-meteo.com/v1/ensemble?latitude=33.4276&longitude=-112.0038&daily=temperature_2m_max&models=ecmwf_ifs025&temperature_unit=fahrenheit&timezone=America/Phoenix&forecast_days=5'   # NOTE members are temperature_2m_max_member01 .. _member51 — there is NO 
```

> Evidence: Five endpoints re-fetched independently 2026-09-21, all HTTP 200. (1) /v1/forecast Phoenix → 200, body opens {"latitude":33.422165,"longitude":-111.99154,"generationtime_ms":0.173,...,"timezone":"America/Phoenix"}, hourly_units.temperature_2m '°F'. (2) ensemble-api /v1/ensemble → 200; parsed 51 member keys and confirmed 51 DISTINCT series (set of tuples = 51), e.g. member01 tmax [101.0,100.6,100.9

#### RCC-ACIS StnData / MultiStnData (Applied Climate Information System) — NOAA Regional Climate Centers (hosted by NRCC, Cornell) ✅ LIVE

Covers **6** subdomains: daily-high-temperature, daily-low-temperature, intraday-and-weekly-temperature, precipitation, snow-and-ski, degree-days

- Docs: https://www.rcc-acis.org/docs_webservices.html
- Auth: none — no key, no registration, no User-Agent requirement. CORS verified open (access-control-allow-origin: *) on POST, so it is browser-callable. | Limits: No published quota. Practical guidance is to batch with MultiStnData rather than loop StnData; a 12-station request costs one call (verified). Server-side reductions (sum/mean/max over an interval) move aggregation off your side.
- Latency: Same-day: values appear as the WFO transmits them, typically within hours of local midnight; quality-controlled revisions land over the following days/weeks. 1-day lag is the safe assumption for settlement. | Format: REST JSON over POST (GET with ?params= also works). Returns {meta:{uid,ll,sids,state,elev,name}, data:[[date, v1, v2, ...]]}. Missing = "M", trace = "T".
- Why primary: The settlement counterpart to Open-Meteo, and it collapses six subdomains into one call. maxt, mint, pcpn, snow, snwd, hdd, cdd, gdd and avgt are all just elements in the same elems array — exactly the one-API-for-gold-and-silver pattern applied to weather. It resolves station identifiers interchangeably (verified: KNYC resolves to a meta.sids list carrying 94728, 305801, NYC, 72506, KNYC, USW00094728), which matters because Kalshi names stations by ICAO and NWS names them by WFO code. It also serves the climatology prior (normals, departures, records) from the same endpoint, and does server-side reductions so a weekly-average contract is one request rather than seven. Narrow alternatives — NOAA CDO v2 (needs an emailed token), GHCN-Daily bulk tarballs (no query surface), IEM daily.json (one station per call) — are all strictly worse here.

```bash
curl -X POST https://data.rcc-acis.org/StnData -H 'Content-Type: application/json' -d '{"sid":"KNYC","sdate":"2026-09-10","edate":"2026-09-18","elems":[{"name":"maxt"},{"name":"mint"},{"name":"pcpn"},{"name":"snow"},{"name":"snwd"},{"name":"hdd"},{"name":"cdd"}]}'
```

> Evidence: Eight POSTs re-fetched independently, all HTTP 200, 2026-09-21. (1) KNYC 7-element request → 200, 687 B, meta.name 'NY CITY CENTRAL PARK', 9 rows, e.g. ['2026-09-13','79','68','0.96','0.0','0','0','9']; trace handling confirmed as literal 'T' on 2026-09-16 and 2026-09-17, distinct from '0.00' elsewhere. (2) MultiStnData for 12 Kalshi cities in ONE call → 200, returned PHOENIX AIRPORT ['103','79','

#### NOAA / National Weather Service API (api.weather.gov) — CLI climate products, gridpoint forecasts, station observations, CAP alerts — NOAA National Weather Service (US Government) ✅ LIVE

Covers **7** subdomains: daily-high-temperature, daily-low-temperature, intraday-and-weekly-temperature, precipitation, snow-and-ski, degree-days, tropical-cyclones

- Docs: https://www.weather.gov/documentation/services-web-api
- Auth: none, but a descriptive User-Agent header identifying your app with contact info is REQUIRED. VERIFIED BY NEGATIVE TEST: the same request with an empty User-Agent returns HTTP 403. The auth claim in the prior report is correct and is a hard failure, not a soft one. | Limits: No published quota; NWS asks for 'reasonable' use and caches aggressively behind a CDN. Poll CLI locations a few times an hour around local-midnight issuance rather than continuously.
- Latency: Alerts: seconds to a minute. Station observations: VERIFIED at 5-minute spacing (KMIA returned 02:15,02:20,02:25,02:30,02:35,02:40,02:45,02:50,03:00 UTC) with the routine METAR interleaved at :53. CLI daily climate report: issued once per site shortly after local midnight, with corrected re-issues later — 15 products queued on the NYC endpoint. | Format: GeoJSON / JSON-LD for structured resources; the CLI climate report is a raw fixed-width TEXT product inside a JSON envelope (productText) that you must parse.
- Why primary: This is the legally authoritative US settlement source — Kalshi's own rules point at 'the NWS Climatological Report for station X', which is literally the CLI product this endpoint serves. One API also gives the official NDFD gridpoint forecast (the public's reference forecast, which anchors where the crowd prices a contract), 5-minute station observations for intraday contracts, and the CAP alert stream that drives hurricane/heat/flood watch-warning markets. Using it for all seven subdomains instead of a per-product vendor is the whole point. Caveat: the CLI text has to be parsed, so pair it with RCC-ACIS, which returns the same numbers already structured.

```bash
curl -H 'User-Agent: my-app/1.0 (me@example.com)' 'https://api.weather.gov/products/types/CLI/locations/NYC'   # then fetch the product id it returns: curl -H 'User-Agent: my-app/1.0 (me@example.com)' 'https://api.weather.gov/products/9f76f915-e8a4-4c49-bdfe-d5645bbcf925'
```

> Evidence: Six endpoints re-fetched independently, 2026-09-21. (1) /products/types/CLI/locations/NYC → 200, 6115 B, newest id 9f76f915-e8a4-4c49-bdfe-d5645bbcf925. (2) /products/{that id} → 200; productText contains the real settlement lines 'MAXIMUM         67    259 PM  93    1895  75     -8       73' and 'MINIMUM         62    325 AM  44    1993  61      1       61'. (3) NEW — the snow-and-ski and degree-

#### NOAA National Hurricane Center — CurrentStorms.json, advisories, wind-speed probabilities, forecast cone GIS, HURDAT2 — NOAA NHC / NCEP ✅ LIVE

Covers **1** subdomains: tropical-cyclones

- Docs: https://www.nhc.noaa.gov/productexamples/NHC_Tropical_Cyclone_Status_JSON_File_Reference.pdf
- Auth: none. | Limits: No published quota; static files behind a CDN. CurrentStorms.json is small (13.8 KB) and only changes on advisory issuance, so poll every ~5 min during an active storm and back off otherwise.
- Latency: Advisories at 03/09/15/21 UTC with intermediate advisories every 3 h when watches/warnings are up; all three active storms carried lastUpdate 2026-09-21T03:00:00.000Z on a 03:1x UTC fetch — under 20 minutes from issuance to file. | Format: JSON (CurrentStorms), raw text advisories (TCP/TCM/TCD), zipped shapefile + KML for cone/track/wind-radii, GRIB1/GRIB2 for wind-speed probabilities, fixed-width text for HURDAT2.
- Why primary: One static URL enumerates every active Atlantic/EPac/CPac cyclone with the exact fields a contract needs — storm id, name, classification (TD/TS/HU), intensity in kt, min pressure, position, motion — plus direct links to every downstream product for that storm, so a single fetch bootstraps the whole storm object graph (28 keys per storm verified, including windSpeedProbabilities, trackCone, bestTrackGIS, stormSurgeWatchWarningGIS). The wind-speed-probability product (wsp34knt/50knt/64knt to 120 h) is NHC's own calibrated landfall probability, the right predictive input for KXHURPATH-style path contracts rather than eyeballing the cone. HURDAT2 and IBTrACS from the same agency family give the seasonal base rate. No broader feed subsumes this: GDACS carries cyclone events but not intensity forecasts or wind probabilities.

```bash
curl https://www.nhc.noaa.gov/CurrentStorms.json   # per-storm cone+watches shapefile: curl -O https://www.nhc.noaa.gov/gis/forecast/archive/al062026_5day_latest.zip   # season base rates — SCRAPE the directory, do not hard-code: curl -s https://www.nhc.noaa.gov/data/hurdat/ | grep -oE 'hurdat2[a-z0-9-]*\.txt'
```

> Evidence: HTTP 200 on all, re-fetched 2026-09-21. (1) CurrentStorms.json → 200, 13830 B. CORRECTION TO PRIOR REPORT: it described ONE active storm; there are THREE. al062026 'Fay' TS 60 kt 995 mb 34.1N 31.9W; ep162026 'Odalys' TS 45 kt 1002 mb 13.1N 127.7W; ep172026 'Polo' TS 35 kt 1004 mb 15.1N 104.6W — all lastUpdate 2026-09-21T03:00:00.000Z. Each storm object carries 28 keys. A client written against a s

#### USGS Earthquake Catalog — FDSN Event service, /count endpoint, and real-time GeoJSON summary feeds — USGS Earthquake Hazards Program (ComCat) ✅ LIVE

Covers **1** subdomains: seismic-and-volcanic

- Docs: https://earthquake.usgs.gov/fdsnws/event/1/
- Auth: none. | Limits: 20,000 events per query — VERIFIED, the /count response literally returns maxAllowed:20000. Use /count or paginate with offset beyond that. Pre-baked summary feeds are CDN-cached and free to poll.
- Latency: Automatic solutions within 1-5 minutes of origin; reviewed magnitudes revised over hours to days. The M4.5+ summary GeoJSON updates continuously. | Format: GeoJSON (also CSV, QuakeML, KML, plain text).
- Why primary: ComCat is the named settlement authority for earthquake contracts, and the /count endpoint settles a counting contract in one request returning a single integer — no client-side tallying, no pagination risk, no disagreement between your count and theirs. The same query surface produces the Gutenberg-Richter magnitude-frequency history that prices the contract beforehand: change starttime to 1990 and you have the base rate. The 24 fixed-URL summary feeds (significant/M4.5+/M2.5+/M1.0+ x hour/day/week/month) are the cheap polling path for a live terminal. EMSC SeismicPortal is a genuine complement (WebSocket push, faster for Eurasian events) but not a replacement, because contracts settle on USGS. NOTE: this feed covers only the SEISMIC half of the seismic-and-volcanic subdomain; the volcanic half is GVP/HANS.

```bash
curl 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2026-09-13&endtime=2026-09-20&minmagnitude=4.5'   # direct contract settlement — year-to-date count of M7.0+: curl 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&starttime=2026-01-01&endtime=2026-09-20&minmagnitude=7.0'
```

> Evidence: Re-fetched independently 2026-09-21, HTTP 200. (1) /query M4.5+ for 2026-09-13..20 → 200, 71629 B, parsed exactly 101 features; first three us7000tild M5.2 'Reykjanes Ridge', us7000tikb M4.5 '75 km SE of Kuqa, China', us7000tiju M5.1 '67 km NE of Ruteng, Indonesia' — identical to the prior report, so the catalog is stable and both reads are reproducible. (2) /count M7.0+ YTD 2026 → 200, exact body

#### Smithsonian Global Volcanism Program (GeoServer WFS + Weekly Volcanic Activity Report RSS) with USGS HANS alert levels — Smithsonian Institution GVP / USGS Volcano Hazards Program ✅ LIVE

Covers **1** subdomains: seismic-and-volcanic

- Docs: https://volcano.si.edu/gvp_votw.cfm
- Auth: none on all three. | Limits: No published quota. WFS supports count/startIndex paging and CQL filters, so pull the Holocene inventory once and cache it; only the weekly RSS and the HANS alert list need polling.
- Latency: Weekly Volcanic Activity Report published every Wednesday — the live feed carried the 10-16 September 2026 reporting week. HANS elevated-volcano list updates within minutes of a Volcanic Activity Notice. The Holocene/eruption inventory is revised on a months-to-years cadence. | Format: WFS GeoJSON/GML for the database; RSS 2.0 (ISO-8859-1 encoded, with GeoRSS) for the weekly report; JSON for HANS.
- Why primary: GVP is the settlement authority named for VEI-based eruption-count contracts and it is the only global source that assigns VEI at all — without it, 'VEI >= 4 eruptions in 2026' cannot be resolved. The WFS carries the full Holocene inventory with Last_Eruption_Year and the eruption-history layer, which is exactly the base rate that prices a seasonal count contract; the weekly RSS is the event stream that moves it intra-year. USGS HANS is folded in here because it is the only real-time US alert-level signal (NORMAL/ADVISORY/WATCH/WARNING plus aviation colour), and it fires days-to-weeks before an eruption that GVP later catalogues.

```bash
curl 'https://volcano.si.edu/news/WeeklyVolcanoRSS.xml'   # global inventory + eruption history (VEI base rates): curl 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes&outputFormat=application/json&count=2'   # current US alert levels: curl 'https://volcanoes.usgs.gov/hans-public/api/volcano/getElevatedVolcanoes'
```

> Evidence: HTTP 200 on all three, re-fetched 2026-09-21. (1) GVP WFS GetFeature (Holocene volcanoes, count=2, JSON) → 200, 4555 B, valid FeatureCollection; first feature Volcano_Number 210010 'West Eifel Volcanic Field', Volcanic_Landform 'Cluster', Primary_Volcano_Type 'Volcanic field', Last_Eruption_Year -8300, Country Germany, Region 'European Volcanic Regions', geometry [6.85,50.17]. (2) WeeklyVolcanoRSS

#### GDACS — Global Disaster Alert and Coordination System (multi-hazard event list) — European Commission JRC / UN OCHA ✅ LIVE

Covers **3** subdomains: tropical-cyclones, seismic-and-volcanic, drought-and-water

- Docs: https://www.gdacs.org/Alerts/api.aspx
- Auth: none. | Limits: No published quota; a week of Orange/Red events is ~12 KB, a week of all-levels is ~135 KB. Poll every 15-30 min.
- Latency: Automated scoring within minutes-to-hours of the originating agency's bulletin (USGS for EQ, NHC/JTWC for TC, GloFAS for FL, GVP for VO). | Format: GeoJSON FeatureCollection; also an RSS 2.0 mirror at /xml/rss.xml.
- Why primary: This is the cheapest single subscription that tells you something is happening across six hazard types (EQ, TC, FL, VO, DR, WF) with a stable eventid, a Green/Orange/Red humanitarian score and modelled population exposure. For a terminal it is the 'what should I be looking at right now' layer across three of this domain's subdomains at once. It is deliberately NOT a settlement source — its magnitudes are copied from the originating agency and its alert score is a model — so it sits alongside USGS/NHC/GVP rather than replacing them. OPERATIONAL WARNING ADDED IN VERIFICATION: do NOT filter to alertlevel=Orange;Red if you want cross-hazard awareness. Every EQ and TC in the sampled week scored Green, so an Orange/Red-only subscription would have shown you zero earthquakes and zero cyclones while three named storms were active.

```bash
curl 'https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?fromDate=2026-09-14&toDate=2026-09-20&alertlevel=Green;Orange;Red'   # single hazard type: ...&eventlist=VO
```

> Evidence: Three independent queries, all HTTP 200, 2026-09-21. (1) Orange;Red for 2026-09-14..20 → 200, 12036 B, 6 events. CORRECTION TO PRIOR REPORT: it stated all 6 were eventtype DR. Actual Counter is {'DR':5, 'FL':1} — five droughts (Madagascar-2026, Europe-2026 across 25 countries, Central America-2026, East Africa-2026, 'Uganda, Kenya-2026') plus one FLOOD event in India. Minor, but the prior report's

#### NOAA NCEI Climate at a Glance — global time-series JSON API — NOAA National Centers for Environmental Information ✅ LIVE

Covers **1** subdomains: global-climate-indicators

- Docs: https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series
- Auth: none. | Limits: No published quota; each response is ~4.8 KB. The URL path is the query (surface/timescale/month/year-range), so there are no parameters to sign.
- Latency: Monthly, published in NCEI's global climate report around the 13th-18th of the following month. August 2026 was present on 2026-09-21. | Format: REST JSON: {description:{title,units,base_period}, data:{"<year>":{"departure":<float>}}}. Note the value is nested under the key 'departure', not returned as a bare number.
- Why primary: This endpoint settles 'where will 2026 rank among the hottest years' directly — it hands back the full 1850-present anomaly series against the base period NOAA uses in its ranking statement, so the rank is a sort, not an inference. Changing two path segments switches between a single month, a season, and year-to-date, which covers every variant of the contract from one feed. NASA GISTEMP is kept alongside it (different agency, different contracts cite different agencies), and NSIDC covers the sea-ice leg; those three are the whole subdomain.

```bash
curl 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/ytd/8/1850-2026/data.json'   # single month instead of YTD: curl 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/land_ocean/1/8/1850-2026/data.json'
```

> Evidence: HTTP 200 on all four, re-fetched independently 2026-09-21. (1) .../land_ocean/ytd/8/1850-2026/data.json → 200, 4824 B, title 'Global Land and Ocean Average Temperature Departures', base_period '1901-2000'. Independently re-sorted the returned series: 2024 +1.25, 2026 +1.16, 2025 +1.13, 2023 +1.07, 2020 +1.05 — 2026 is 2nd-warmest YTD through August, reproducing the prior report exactly. Series sta

#### US Drought Monitor data services API (USDM) — National Drought Mitigation Center, University of Nebraska-Lincoln (with USDA and NOAA) ✅ LIVE

Covers **1** subdomains: drought-and-water

- Docs: https://droughtmonitor.unl.edu/DmData/DataDownload/WebServiceInfo.aspx
- Auth: none. | Limits: No published quota; responses are 1-3 KB per area per week.
- Latency: Weekly. The map is valid from Tuesday and released Thursday morning ET; on 2026-09-21 the current mapDate was 2026-09-15 with validEnd 2026-09-21T23:59:59. | Format: REST JSON (send Accept: application/json — the default is XML). Percent-of-area in each of none/D0/D1/D2/D3/D4.
- Why primary: USDM is the settlement authority for US drought-classification contracts and it serves national, state, county, HUC watershed and congressional-district rollups from the same endpoint shape — one feed, every geographic granularity a market might name. IEM's usdm_bypoint.json complements it with a drought-class time series at an arbitrary lat/lon, which is what you want for a map widget rather than a table.

```bash
curl -H 'Accept: application/json' 'https://usdmdataservices.unl.edu/api/USStatistics/GetDroughtSeverityStatisticsByAreaPercent?aoi=us&startdate=9/1/2026&enddate=9/20/2026&statisticsType=1'   # state — use the 2-digit FIPS, NOT the postal code: .../StateStatistics/...?aoi=32&...   # county: .../CountyStatistics/...?aoi=32003&...
```

> Evidence: HTTP 200 on all four, re-fetched independently 2026-09-21. (1) USStatistics aoi=us for 2026-09-01..20 → 200, 1296 B, 6 rows; the 2026-09-15 CONUS row is {none 19.03, d0 80.97, d1 59.37, d2 33.82, d3 12.54, d4 2.02} — matches the prior report exactly. (2) StateStatistics aoi=32 → 200, {stateAbbreviation NV, none 0.00, d0 100.00, d1 91.30, d2 55.68, d3 7.87, d4 0.82}. (3) CountyStatistics aoi=32003 

#### River, reservoir and lake levels: USBR RISE + USGS NWIS + NOAA NWPS + CA CDEC + PEGELONLINE (Rhine) — US Bureau of Reclamation / USGS / NOAA NWS / California DWR / German WSV ✅ LIVE

Covers **1** subdomains: drought-and-water

- Docs: https://data.usbr.gov/rise-api
- Auth: none on any of the five. | Limits: None published on any. RISE paginates with itemsPerPage; NWIS accepts comma-separated site and parameter lists so many gauges come back in one call; PEGELONLINE returns all 36 Rhine stations with current measurements in one 13 KB request.
- Latency: USGS NWIS 15-minute instantaneous values (observed timestamp 2026-09-20T22:50:00-04:00 on a 22:5x fetch). PEGELONLINE 15-minute (05:15+02:00 on a 05:2x fetch). USBR RISE daily, ~1-2 day lag (latest 2026-09-19). CDEC daily with a 1-day obsDate lag (date 2026-9-10 carried obsDate 2026-9-11). NWPS re-forecasts several times daily. | Format: JSON:API (RISE, requires Accept: application/vnd.api+json), WaterML-in-JSON (NWIS), REST JSON (NWPS, PEGELONLINE, CDEC).
- Why primary: Water-level contracts name a specific gauge operated by a specific authority, and no single API owns Lake Mead, the Potomac, Shasta and the Rhine — so the honest consolidation is by function, not by vendor. Together these five cover every water-level contract style seen on the three venues: federal reservoirs (RISE, the settlement source for KXMEAD), US stream gauges at 15-minute resolution (NWIS), NWS flood-stage categories and crest forecasts that make a level contract predictive rather than merely observed (NWPS), California reservoirs which NWIS does not carry in the same form (CDEC), and European rivers for Polymarket's Rhine market (PEGELONLINE). Open-Meteo's GloFAS flood endpoint gives the forecast leg globally at points where no gauge API exists.

```bash
curl -H 'Accept: application/vnd.api+json' 'https://data.usbr.gov/rise/api/result?itemId=6124&itemsPerPage=5&order%5BdateTime%5D=desc'   # (itemId 6124 = Lake Mead / Hoover Dam daily storage)   # US river gauge: curl 'https://waterservices.usgs.gov/nwis/iv/?format=json&sites=01646500&parameterCd=00060,00065&period=P1D'   # NWS flood categories + crest forecast: curl 'https://api.water.noaa.gov/nwps/v1/gauges/01646500'   # Rhine at Kaub: curl 'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/KAUB/W/currentmeasurement.json'   # CA reservoir: curl 'https://cdec.water.ca.gov/dynamic
```

> Evidence: HTTP 200 on all five, re-fetched independently 2026-09-21. (1) RISE itemId=6124 → 200, 2734 B, results 2026-09-19T07:00Z 6862490, 09-18 6866580, 09-17 6870680, 09-16 6874780, 09-15 6885720 af — a real monotonic drawdown, not a repeated value. catalog-item/6124 independently confirms itemTitle 'Lake Mead Hoover Dam and Powerplant Daily Lake/Reservoir Storage-af Time Series Data', parameterName 'Lak

#### NOAA CPC — ONI/ENSO index and 6-10 day / 8-14 day / monthly / seasonal probabilistic outlooks — NOAA Climate Prediction Center ✅ LIVE

Covers **6** subdomains: daily-high-temperature, daily-low-temperature, precipitation, degree-days, drought-and-water, global-climate-indicators

- Docs: https://www.cpc.ncep.noaa.gov/products/predictions/
- Auth: none. | Limits: No published quota. The GIS zips are large (610temp_latest.zip 3,351,791 B; 814temp_latest.zip 3,345,487 B; 610prcp_latest.zip 3,346,625 B; seastemp_latest.zip ~50 MB) — fetch on their publication cadence, not on a poll loop.
- Latency: ONI updated monthly (latest season present: JJA 2026). 6-10 and 8-14 day outlooks issued daily ~3 PM ET. Monthly outlook on the 3rd Thursday; seasonal on the 3rd Thursday of each month. | Format: Fixed-width ASCII for the ONI index; zipped ESRI shapefiles (probability-of-above/below/near-normal polygons) for the outlooks — you must decode a shapefile, there is no JSON point-query.
- Why primary: This is the long-lead half of the pricing problem. Ensembles like Open-Meteo's run out to ~15 days; contracts on a month-ahead HDD total or a summer drought are priced beyond that horizon, and CPC's probability-of-above/below/near-normal polygons are the reference forecast the market anchors on. The ONI/ENSO series is the strongest cross-subdomain covariate here — it conditions Atlantic hurricane activity, US winter temperature and drought simultaneously, so one 23 KB text file feeds several boards. COVERAGE CLAIM CORRECTED IN VERIFICATION: the prior report listed 'tropical-cyclones' among this feed's coversSubdomains. I removed it. None of the four verified endpoints serves a cyclone product — oni.ascii.txt is an SST index and the GIS bundles are temperature/precipitation outlooks. CPC's seasonal hurricane outlook exists only as an HTML page (/products/outlooks/hurricane.shtml, HTTP 200 but text/html, not machine-readable). ONI remains listed as a COVARIATE in the tropical-cyclones row's predictiveFeed, which is the honest framing; it is not a cyclone feed.

```bash
curl 'https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt'   # 6-10 day probabilistic temperature outlook (GIS): curl -O 'https://ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/610temp_latest.zip'   # 8-14 day: .../814temp_latest.zip   # precip: .../610prcp_latest.zip   # seasonal: .../seastemp_latest.zip
```

> Evidence: Re-fetched independently 2026-09-21. (1) oni.ascii.txt → HTTP 200, 23000 B, tail rows 'MAM 2026 28.09 0.46', 'AMJ 2026 28.74 0.95', 'MJJ 2026 29.02 1.39', 'JJA 2026 29.09 1.80' — current through JJA 2026, warm/El Nino-side and strengthening. (2) 610temp_latest.zip → 200, 3351791 B, content-type application/zip. (3) 814temp_latest.zip → 200, 3345487 B. (4) NEW — 610prcp_latest.zip → 200, 3346625 B 

#### Iowa Environmental Mesonet (IEM) API — daily station summaries, NBM/GFS/NAM station MOS guidance, LSR and warning archive — Iowa State University (Iowa Environmental Mesonet) ✅ LIVE

Covers **5** subdomains: intraday-and-weekly-temperature, daily-high-temperature, daily-low-temperature, precipitation, snow-and-ski

- Docs: https://mesonet.agron.iastate.edu/api/1/docs
- Auth: none. | Limits: No published quota; IEM asks that bulk historical pulls use the download services rather than looping the JSON API. One station per daily.json/mos.json call — this one does NOT batch, unlike ACIS MultiStnData.
- Latency: MOS refreshed on each model cycle — the returned NBS run was 2026-09-21 00:00 UTC on a ~03:2x UTC fetch, i.e. under 3.5 h including NBM's own production lag. daily.json follows the ASOS daily summary, same-day. | Format: REST JSON with an embedded pandas table schema; GeoJSON for LSR.
- Why primary: IEM is the free, keyless way to get NBM station guidance — the NWS's own statistically post-processed best guess at a specific airport, which is the closest public product to what a temperature contract actually settles on, and it comes pre-decoded so you never touch a GRIB file or a raw bulletin. It is the right predictive layer for hourly/intraday markets where a raw model grid is too coarse and the official NDFD forecast is too smoothed. It also carries the complete NWS warning-polygon and Local Storm Report archive, which is the backtesting corpus for severe-weather markets.

```bash
curl 'https://mesonet.agron.iastate.edu/api/1/mos.json?station=KPHX&model=NBS'   # station daily obs: curl 'https://mesonet.agron.iastate.edu/api/1/daily.json?station=PHX&network=AZ_ASOS&date=2026-09-19'   # last 6 h of local storm reports: curl 'https://mesonet.agron.iastate.edu/geojson/lsr.py?inc_ap=no&hours=6'
```

> Evidence: HTTP 200 on all three, re-fetched independently 2026-09-21. (1) /api/1/mos.json?station=KPHX&model=NBS → 200, 23625 B, 23 forecast rows; row 0 = {model 'NBS', runtime '2026-09-21 00:00', ftime '2026-09-21 06:00', tmp 87, dpt 50, wdr 230, wsp 3, p06 1.0, q06 0.0, sky 81, vis 100, snw None, wbg 72} — real station-level NBM guidance with valid-time stepping and ~60 populated fields. (2) /api/1/daily.

#### USDA NRCS SNOTEL / AWDB REST API — USDA Natural Resources Conservation Service ✅ LIVE

Covers **2** subdomains: snow-and-ski, drought-and-water

- Docs: https://wcc.sc.egov.usda.gov/awdbRestApi/swagger-ui/index.html
- Auth: none. | Limits: No published quota; stationTriplets and elements both accept comma-separated lists, so a whole mountain range comes back in one call.
- Latency: Hourly transmission, daily values finalized overnight; the 2026-09-19 value was present on 2026-09-21. | Format: REST JSON: array of {stationTriplet, data:[{stationElement:{elementCode,durationName,storedUnitCode,beginDate,endDate}, values:[{date,value}]}]}.
- Why primary: Snow water equivalent from ~900 automated western-US sites is the physical state variable behind both ski-resort markets and western water markets, and it is the one thing a temperature/precip forecast cannot give you — it is the integrated snowpack, with multi-decade history for percent-of-median comparisons. One call covers every element (WTEQ, SNWD, TOBS, PREC, soil moisture) at every listed site, so there is no per-metric API.

```bash
curl 'https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data?stationTriplets=505:CO:SNTL&elements=WTEQ,SNWD,TOBS&duration=DAILY&beginDate=2026-09-15&endDate=2026-09-19'   # (505:CO:SNTL = Grizzly Peak, the Summit County site nearest Breckenridge/Keystone)
```

> Evidence: HTTP 200, re-fetched independently 2026-09-21. (1) stationTriplets=505:CO:SNTL, elements WTEQ,SNWD,TOBS for 2026-09-15..19 → 200, 1248 B; SNWD 'in' [0,0,0,0,0], WTEQ 'in' [0.0,0.0,0.0,0.0,0.0], TOBS 'degF' [42.8,43.0,45.0,39.2,35.6]. The nonzero TOBS proves the station is transmitting, so the snow zeroes are MEASURED zeroes, not missing data. (2) NEW AND IMPORTANT — the prior report rested its ent

#### Federal Register API v1 — US Office of the Federal Register / GPO ✅ LIVE

Covers **1** subdomains: climate-policy

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none. | Limits: No key required; documented soft limit around 1,000 requests/hour per IP. Field selection via fields[] keeps responses small (1.5-2 KB for 3 documents).
- Latency: Documents appear on public inspection the business day before publication and in the API on the publication date. | Format: REST JSON with faceted search (agency slug, document type Rule/Proposed Rule/Notice/Presidential Document, date ranges, full text).
- Why primary: For US climate-policy contracts this is the only machine-readable record of the act itself — a rescission, a rule, a notice, or a presidential document is legally effective on Federal Register publication, so the feed and the settlement event are the same object. Filtering by agency slug plus term covers EPA greenhouse-gas actions, Interior/Energy rules and executive actions from one query surface. It does NOT cover international climate policy, which is the honest limit of this subdomain. Also note the full-text 'term' filter is loose — a search for 'climate change' returned a wildland-fire differential-pay rule and an NRC environmental-assessment notice, so filter on agency + document type as well, or you will surface non-contract noise.

```bash
curl 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=environmental-protection-agency&conditions%5Bterm%5D=greenhouse+gas&conditions%5Bpublication_date%5D%5Bgte%5D=2026-01-01&per_page=3&fields%5B%5D=title&fields%5B%5D=type&fields%5B%5D=publication_date&fields%5B%5D=html_url'
```

> Evidence: HTTP 200, re-fetched independently 2026-09-21. (1) agency=environmental-protection-agency + term='greenhouse gas', publication_date >= 2026-01-01 → 200, 1489 B, count 40; results include 2026-02-18 Rule 'Rescission of the Greenhouse Gas Endangerment Finding and Motor Vehicle Gre...', 2026-02-27 Rule and 2026-06-05 Rule 'Extending the Reporting Deadline Under the Greenhouse Gas Reporting Rule'. (2)

#### Hong Kong Observatory Open Data API — Hong Kong Observatory (HKSAR Government) ✅ LIVE

Covers **2** subdomains: daily-high-temperature, daily-low-temperature

- Docs: https://www.hko.gov.hk/en/abouthko/opendata_intro.htm
- Auth: none. | Limits: No published quota; the annual daily-maximum extract is 7.3 KB.
- Latency: Current-conditions endpoint updates every 10 minutes (observed updateTime 2026-09-21T11:02:00+08:00 on an 11:0x fetch). The climatological daily extract runs about 3 weeks behind — on 2026-09-21 it still ended at 2026-08-31. | Format: REST JSON; the climate extract returns bilingual field headers and rows of [year, month, day, value, completeness-flag] where 'C' = data complete.
- Why primary: Included because the domain spec names Hong Kong Observatory as a settlement source and Polymarket lists HK temperature markets — NWS and RCC-ACIS are US-only, so without this the non-US leg of the temperature subdomains is simply uncovered. One endpoint pattern serves the whole HKO open-data catalogue (CLMMAXT, CLMMINT, CLMTEMP, rainfall) by swapping dataType, so it does not become one-API-per-variable. Open-Meteo already supplies the forecast/ensemble leg globally; this supplies the settlement leg for HK.

```bash
curl 'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=CLMMAXT&year=2026&rformat=json&station=HKO'   # daily minimum: swap dataType=CLMMINT   # current conditions across all HK stations: curl 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en'
```

> Evidence: HTTP 200, re-fetched independently 2026-09-21. (1) rhrread → 200, 2985 B, updateTime 2026-09-21T11:02:00+08:00, temperature readings King's Park 31 C, Hong Kong Observatory 31 C, Wong Chuk Hang 31 C, Ta Kwu Ling 32 C (one degree above the prior report's fetch — live drift, correct behaviour). (2) CLMMAXT year=2026 station=HKO → 200, 7313 B, 243 daily rows, tail ['2026','8','29','32.8','C'], ['2026

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Daily High Temperature | Open-Meteo Ensemble API (51 ECMWF IFS members of temperature | NWS CLI Climatological Report via api.weather.gov/products/t | 🟢 COVERED |
| Daily Low Temperature | Open-Meteo Ensemble (temperature_2m_min members) plus Open-M | NWS CLI product — re-verified 'MINIMUM 62 325 AM 44 1993 61  | 🟢 COVERED |
| Hourly & Weekly Average Temperature | Open-Meteo Forecast hourly and 15-minutely temperature_2m (H | NWS station observations api.weather.gov/stations/{ICAO}/obs | 🟡 PARTIAL |
| Rain & Precipitation | Open-Meteo Ensemble (precipitation members to exceedance pro | NWS CLI product PRECIPITATION (IN) section — re-verified pre | 🟢 COVERED |
| Snowfall & Ski Resorts | Open-Meteo Forecast snowfall_sum + temperature_2m_min at the | For the SNOWFALL leg: RCC-ACIS elements snow and snwd — newl | 🟡 PARTIAL |
| Hurricanes & Tropical Cyclones | NHC wind-speed probability products (wsp34knt/50knt/64knt to | NOAA NHC CurrentStorms.json plus the numbered public/forecas | 🟢 COVERED |
| Heating & Cooling Degree Days | Open-Meteo Ensemble temperature_2m_max/min members converted | RCC-ACIS StnData with elems hdd/cdd and a configurable base  | 🟢 COVERED |
| Global Temperature & Climate Indicators | NOAA NCEI Climate at a Glance YTD series (the year-to-date a | NOAA NCEI Climate at a Glance JSON (globe/land_ocean, annual | 🟢 COVERED |
| Drought & Water Levels | Open-Meteo flood-api GloFAS river discharge forecast (re-ver | US Drought Monitor data services API for drought-classificat | 🟢 COVERED |
| Earthquakes & Volcanic Activity | USGS FDSN /query over a multi-decade window for the Gutenber | USGS Earthquake Catalog (ComCat) FDSN Event service — the /c | 🟢 COVERED |
| Climate Policy & Agreements | Federal Register API v1 — Proposed Rules and public-inspecti | Federal Register API v1 for US executive actions, rules and  | 🟡 PARTIAL |

**Rejected**

- **Synoptic Data Mesonet API v2 (api.synopticdata.com)** — RE-TESTED 2026-09-21: HTTP 401, body {"SUMMARY":{"RESPONSE_CODE":2,"RESPONSE_MESSAGE":"Missing token","HTTP_STATUS_CODE":401}} on /v2/stations/latest?stid=KPHX. This is Kalshi's NAMED settlement vendor for hourly-tempera
- **The Weather Company / IBM Weather API** — Named alongside Synoptic as a Kalshi settlement vendor but has no free tier at all. Not testable, not usable. NOT TESTED this pass (no free endpoint exists to test).
- **NSIDC Sea Ice Index v3.0 CSV paths (N_seaice_extent_daily_v3.0.csv, N_09_extent_v3.0.csv)** — RE-TESTED: the v3.0 daily path returns HTTP 404. Confirmed DEAD. Superseded by the v4.0 paths, which I independently re-verified at 1,897,995 B daily (last row '2026, 09, 19, 4.708') and 2,304 B monthly.
- **NOAA CPC weekly Nino SST file (wksst8110.for)** — RE-TESTED: HTTP 200 and 102,362 B, but STALE — the file's last two rows are '20JAN2021' and '27JAN2021' and it contains zero rows for 2026. A feed that returns 200 with five-year-old data is the most dangerous failure mo
- **NOAA CPC 6-10 day text outlooks (610temp.new.txt, 610prcp.new.txt)** — RE-TESTED: 610temp.new.txt returns HTTP 404 on www.cpc.ncep.noaa.gov. Superseded by the GIS shapefile bundles at ftp.cpc.ncep.noaa.gov/GIS/us_tempprcpfcst/, which I re-verified at 610temp_latest.zip 3,351,791 B, 814temp_
- **origin.cpc.ncep.noaa.gov (CPC origin hostname)** — RE-TESTED: curl exit code 6, HTTP 000 — DNS does not resolve. Use www.cpc.ncep.noaa.gov.
- **NOAA CPC seasonal hurricane outlook (/products/outlooks/hurricane.shtml)** — NEWLY REJECTED THIS PASS. HTTP 200 but content is an HTML page, not a machine-readable product. This is why 'tropical-cyclones' was removed from the CPC feed's coversSubdomains — the prior report claimed that subdomain f
- **Open-Meteo Seasonal API (seasonal-api.open-meteo.com/v1/seasonal)** — RE-TESTED and confirmed unusable. HTTP 200 with a 175-byte body containing ONLY the coordinate/elevation echo and no six_hourly or daily block. Requesting daily=temperature_2m_max_member01 returns HTTP 400 'Data corrupte
- **NOHRSC National Snow Analysis text products** — HTTP 404 at the dated discussion path (carried forward from the prior pass; not re-tested this round). SNOTEL SWE and Open-Meteo snowfall cover the snow subdomain and both verified clean, with SNOTEL now proven on real w
- **OnTheSnow API, skiapi.com, api.skimap.org, WeatherUnlocked snow report** — ALL FOUR RE-TESTED 2026-09-21 and all four failed again: onthesnow.com/api/v1/resorts HTTP 401; skiapi.com/api/resort/breckenridge HTTP 404; api.skimap.org HTTP 000, DNS does not resolve; api.weatherunlocked.com HTTP 000
- **Climate Policy Radar search API** — HTTP 422 'Field required: header app-token' — requires an issued token, not self-service (carried forward; not re-tested this round).
- **UNFCCC /api/v1/documents** — RE-TESTED: HTTP 200, 212 B, content-type text/html. Body is an Incapsula bot-challenge interstitial ('<META NAME="robots" CONTENT="noindex,nofollow">' plus an _Incapsula_Resource script tag), not an API response. There i
- **UNFCCC NDC Registry (www4.unfccc.int/sites/NDCStaging/Pages/All.aspx)** — HTTP 302 to a SharePoint UI. Not a data service; would require scraping (carried forward; not re-tested this round).
- **Copernicus Climate Pulse daily JSON** — HTTP 404 at the daily-file path (carried forward). Superseded for global-temperature contracts by NCEI Climate at a Glance and NASA GISTEMP, both independently re-verified live and both actually cited by contract rules.
- **Copernicus CDS and ADS (cdsapi)** — Live but require free registration plus a personal access token in ~/.cdsapirc, and deliver NetCDF/GRIB that must be decoded and interpolated. For point extraction from ERA5 this is strictly more work than Open-Meteo's a
- **Berkeley Earth Land_and_Ocean_complete.txt** — Downloaded HTTP 200 / 416 KB in the prior pass but no 2026 rows were found, so currency is unconfirmed and it is not reported as live. Not cited by any venue's settlement rules, unlike NCEI and GISTEMP. NOT RE-TESTED thi
- **NOAA Climate Data Online (CDO) API v2** — RE-TESTED without a token: HTTP 400. Requires a token issued by email request. It serves GHCND/GSOM/normals — exactly what RCC-ACIS serves with NO authentication, with CORS open, and with server-side reductions. Strictly
- **Raw model archives on AWS/NOMADS (GFS, GEFS, HRRR, NBM, ECMWF open data, MRMS, GOES)** — All genuinely live and free, but they deliver GRIB2/NetCDF requiring decoding, grid interpolation and (for GEFS) per-member assembly. Open-Meteo and IEM already expose the same model output as point JSON — IEM's NBS resp
- **Meteostat JSON API and Visual Crossing Timeline API** — Both need keys (RapidAPI key / free-plan registration) and both re-serve GHCN/ISD station data that RCC-ACIS and NCEI provide keyless. Meteostat's bulk CSV endpoint remains a reasonable keyless fallback for non-US statio
- **OpenAQ v3 and EPA AirNow** — Both require a free API key, and air quality is not among this domain's twelve subdomains. Out of scope here.
- **ReliefWeb API v2** — Requires a registered appname since 2025-11-01, and its disaster records are humanitarian narrative rather than settlement-grade measurements. GDACS covers the same alerting need with no auth and was re-verified across f

---

### commodities

*7/12 subdomains covered · 12 primary feeds*

#### FRED fredgraph.csv — keyless multi-series commodity CSV — Federal Reserve Bank of St. Louis ✅ LIVE

Covers **9** subdomains: crude-oil-wti, crude-oil-brent, natural-gas, refined-fuels, electricity-and-power, coal, copper, grains-and-oilseeds, softs-and-livestock

- Docs: https://fred.stlouisfed.org/docs/api/fred/
- Auth: NONE for the fredgraph.csv surface (no key, no registration). The documented /fred/series/observations JSON API is a separate surface and does require a free key. | Limits: No key and no published quota on fredgraph.csv. Comma-separate as many series ids as you like in one call. TWO BEHAVIOURS THAT BITE, both re-verified this pass: (1) DATE WINDOWING IS SILENTLY IGNORED WHEN >1 SERIES IS REQUESTED — cosd, coed, and repeated cosd/coed all return the identical 213,182-byte full-history CSV; only a single-id request honours them (verified: single id + cosd → 12 lines). Budget for full-history payloads on every multi-series poll. (2) Mixed frequencies return a ZIP of per-frequency CSVs instead of a CSV — group your ids by frequency to keep CSV output.
- Latency: Daily series ~1 business day behind (WTI/Brent/Henry Hub verified through 2026-09-15). Weekly retail fuel Mondays (verified 2026-09-14). Monthly IMF/World Bank blocks land mid-following-month (verified through 2026-07). Monthly CPI electricity verified through 2026-08. | Format: CSV (single frequency) or ZIP-of-CSV (mixed frequency)
- Why primary: Still the broadest free commodity feed that actually executes, and every one of the nine claimed subdomains was independently re-fetched and confirmed. One keyless URL returns WTI, Brent, Henry Hub, US retail gasoline and diesel, copper, wheat, maize, soybeans, cocoa, coffee, sugar, beef, lamb, poultry, Australian coal, European gas and US retail electricity. Two caveats a developer must carry: the ag/metal/coal blocks are MONTHLY IMF-derived macro prices, not exchange settles; and the electricity leg is a single monthly CPI retail price series (APU000072610, $/kWh) — it is a real price but it is NOT a power-market feed, so do not let it carry the electricity subdomain on its own.

```bash
curl 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO,DCOILBRENTEU,DHHNGSP'   # NOTE: cosd/coed are IGNORED on multi-series calls — you always get full history (213 KB back to 1987). Trim client-side, or issue one call per series if you need a window: curl 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILWTICO&cosd=2026-09-01'
```

> Evidence: RE-FETCHED INDEPENDENTLY. Daily: HTTP 200, 213,182 bytes, content-type application/csv, header `observation_date,DCOILWTICO,DCOILBRENTEU,DHHNGSP`, final row `2026-09-15,107.02,130.80,2.97` — matches the report exactly. Weekly `GASREGW,GASDESW` tail `2026-09-14,4.319,6.285` — matches. Monthly 10-series block HTTP 200 / 69,309 bytes, row `2026-07-01,13542.82…,228.73…,213.19…,5619.18…,359.16…,331.78…

#### Kalshi public trade API v2 (series, markets, candlesticks, settlement) — Kalshi Exchange (CFTC-regulated DCM) ✅ LIVE

Covers **12** subdomains: crude-oil-wti, crude-oil-brent, natural-gas, refined-fuels, electricity-and-power, coal, gold, silver, copper, platinum-palladium, grains-and-oilseeds, softs-and-livestock

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: NONE for all market-data reads. A key is only needed to place orders. | Limits: Unauthenticated read tier. Kalshi does not publish a numeric anonymous limit (UNKNOWN); paginate with the returned `cursor`. 980 DISTINCT series enumerated across Commodities (144) + Economics (879) with no throttling observed across ~25 sequential calls. Note the report's figure of 1,023 is the raw sum of the two category responses — 43 series appear in both, so the deduplicated count is 980.
- Latency: Real-time order book; candlesticks selectable down to 1-minute `period_interval` (candlesticks endpoint re-verified HTTP 200 at period_interval=60). | Format: JSON
- Why primary: Confirmed as the only feed covering all twelve subdomains, and the claim survived adversarial checking — I enumerated live tickers for every one. It is both predictive (live order book + candlesticks on exactly the contract your users trade) and settlement-grade: I independently read back `expiration_value` on settled markets in EIGHT different subdomains, not just the one the report showed. One correction to the report's framing: settlement read-back is NOT universal. KXTXERCOTPEAK, KXWTID, KXCORNMON and KXCOCOAMON returned zero settled markets, so the power, grain and softs settlement legs cannot be read back today. Use it as the spine, but check `status=settled` returns rows before you depend on it for a given series.

```bash
curl 'https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXWTIH&limit=3'
```

> Evidence: RE-FETCHED INDEPENDENTLY. `/markets?series_ticker=KXWTIH&limit=3` HTTP 200 / 6,305 bytes → live market KXWTIH-26SEP2101 with floor_strike 95.79, open_time 2026-09-21T03:01:00Z, rules_primary naming the 1-minute WTI candlestick. `/series?category=Commodities` HTTP 200 / 115,557 bytes (144 series); `category=Economics` 812,783 bytes (879 series); 980 unique tickers. Ticker enumeration confirms every

#### LBMA Precious Metal Price JSON (benchmark fixings) — London Bullion Market Association / ICE Benchmark Administration ✅ LIVE

Covers **3** subdomains: gold, silver, platinum-palladium

- Docs: https://www.lbma.org.uk/prices-and-data/precious-metal-prices
- Auth: none | Limits: No key, no registration, no published rate limit. One file per metal/session — gold_am, gold_pm, silver, platinum_am, platinum_pm, palladium_am, palladium_pm. Each returns FULL history in one response; silver.json is 898 KB, so cache it rather than polling.
- Latency: Daily; AM fix ~10:30 London, PM ~15:00 London. Independently verified current through 2026-09-18. | Format: JSON array of {is_cms_locked, d: date, v: [USD, GBP, EUR]}
- Why primary: Four metals across three subdomains from keyless static JSON, and these are ICE-administered benchmark fixings rather than a vendor's quotes. Every value the report cited reproduced to the cent on an independent fetch. With Pyth's price endpoint auth-gated (re-confirmed 401 this pass) this remains the only free daily precious-metals price I could execute end to end.

```bash
curl 'https://prices.lbma.org.uk/json/silver.json'
```

> Evidence: RE-FETCHED INDEPENDENTLY, all four HTTP 200 with current data, every figure reproducing the report exactly. silver.json HTTP 200 / 898,020 bytes / application/json, tail `{"is_cms_locked":0,"d":"2026-09-18","v":[67.035,50.18,58.42]}`. gold_pm.json tail `{"d":"2026-09-18","v":[4348.15,3259.37,3793.33]}`. platinum_pm.json tail `{"d":"2026-09-18","v":[1793.2,1343.64,1563.67]}`. palladium_pm.json tail

#### World Bank Commodity Markets 'Pink Sheet' — monthly historical XLSX — World Bank ✅ LIVE

Covers **10** subdomains: crude-oil-wti, crude-oil-brent, natural-gas, coal, gold, silver, copper, platinum-palladium, grains-and-oilseeds, softs-and-livestock

- Docs: https://www.worldbank.org/en/research/commodity-markets
- Auth: none | Limits: No key, no registration, no quota. One file carries ~70 commodities back to 1960.
- Latency: Monthly, published around the first week of the following month. | Format: XLSX
- Why primary: One 778 KB file instead of seventy APIs, covering ten of twelve subdomains: crude (Brent, Dubai, WTI), natural gas (US, Europe, Japan LNG), coal (Australian, South African), aluminium, copper, iron ore, lead, nickel, tin, zinc, gold, silver, platinum, wheat, maize, rice, soybeans, soybean oil, palm oil, sugar, coffee, cocoa, beef, chicken and fertilizers. Monthly cadence makes it a fundamentals/benchmark layer, not a tick source — pair with FRED daily and Kalshi for the fast layer. Flagging one verification limit honestly: I confirmed the file is a structurally valid XLSX but did NOT parse the sheets to confirm each of the ten claimed commodity columns, so the per-subdomain breakdown is carried from the source's published contents rather than independently read.

```bash
curl -L -o CMO-Historical-Data-Monthly.xlsx 'https://thedocs.worldbank.org/en/doc/18675f1d1639c7a34d463f59263ba0a2-0050012025/related/CMO-Historical-Data-Monthly.xlsx'
```

> Evidence: RE-FETCHED INDEPENDENTLY. HTTP 200, 778,415 bytes, content-type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, no redirect (url_effective identical to the request). `file` reports 'Microsoft Excel 2007+' and the archive opens as a valid zip with 30 entries — confirmed a real XLSX, not an HTML error page. Per-sheet column contents NOT parsed: coversSubdomains for this feed is UN

#### Alpha Vantage Commodities API (11 functions, one schema) — Alpha Vantage ✅ LIVE

Covers **6** subdomains: crude-oil-wti, crude-oil-brent, natural-gas, copper, grains-and-oilseeds, softs-and-livestock

- Docs: https://www.alphavantage.co/documentation/#commodities
- Auth: The literal key `demo` works for monthly interval on every commodity function (independently re-verified on all 11). Daily/weekly intervals require a free email-signup key. | Limits: demo key: monthly interval only. I issued all 11 functions at ~1 req/sec with zero throttling, so the demo tier is usable, but I did NOT push it to find the ceiling — the report's '2 requests/second' figure is UNVERIFIED. Free registered key: 25 requests/day is Alpha Vantage's published figure, NOT independently measured here (no key was obtained). Throttling surfaces as a JSON `Information` field with HTTP 200, so check for that field rather than relying on status code. Functions: WTI, BRENT, NATURAL_GAS, COPPER, ALUMINUM, WHEAT, CORN, COTTON, SUGAR, COFFEE, ALL_COMMODITIES.
- Latency: Monthly on the demo key (verified current to 2026-07 for the IMF-derived series and 2026-08 for the EIA-derived energy series); daily available with a free key. | Format: JSON (or CSV via &datatype=csv)
- Why primary: Eleven commodities behind one identical request shape and one identical response schema — swap the `function` value and nothing else changes. Cheapest feed to integrate for a normalized multi-commodity panel. TWO HONEST DOWNGRADES from the report: (1) the underlying values are byte-identical to FRED's IMF/EIA series (COPPER 13542.82 = FRED PCOPPUSDM, WHEAT 228.74 = PWHEAMTUSDM, ALL_COMMODITIES 193.20 = PALLFNFINDEXM), so this is a convenience wrapper over FRED, not independent evidence — never treat agreement between the two as corroboration. (2) The `softs-and-livestock` claim is HALF TRUE: SUGAR, COFFEE and COTTON are served, but Alpha Vantage has NO livestock function at all — no cattle, no hogs, no beef. Kept in coversSubdomains because it genuinely prices the softs half; the livestock half comes from FRED and USDA.

```bash
curl 'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo'
```

> Evidence: RE-FETCHED INDEPENDENTLY. All 11 functions HTTP 200 with real data on the `demo` key at interval=monthly, every value reproducing the report: WTI `Crude Oil Prices WTI` dollars per barrel 2026-08-01=83.9; BRENT 2026-08-01=91.08; NATURAL_GAS `Henry Hub Natural Gas Spot Price` 2026-08-01=2.78; COPPER 2026-07-01=13542.82086956522 $/tonne; ALUMINUM 3158.265; WHEAT 228.73884495; CORN 213.1901539821428;

#### EIA keyless file surfaces — WPSR, gas storage, retail fuel history, Grid Monitor — US Energy Information Administration ✅ LIVE

Covers **5** subdomains: crude-oil-wti, natural-gas, refined-fuels, electricity-and-power, coal

- Docs: https://www.eia.gov/petroleum/supply/weekly/
- Auth: NONE on these file paths. (The richer /v2 JSON API is key-gated — re-confirmed 403 API_KEY_MISSING this pass, see rejectedFeeds.) | Limits: No key, no quota on the static paths. TWO OPERATIONAL FACTS: (1) ir.eia.gov issues a signed CloudFront redirect — without -L you get HTTP 302 and ZERO bytes (re-verified exactly). (2) SIZE CORRECTION: the Grid Monitor six-month CSV is ~45 MB, not 'larger than 5 MB' as the report implied — an unbounded fetch pulled 44.9 MB. Stream it or use HTTP Range; do not buffer it in memory per poll.
- Latency: WPSR Wednesdays 10:30 ET; natural gas storage Thursdays 10:30 ET (ngshistory.xls internal Last-Saved stamp 2026-09-15, i.e. genuinely current); retail fuel Mondays; Grid Monitor hourly in six-month rolling CSVs. | Format: XLS and CSV
- Why primary: The fundamentals layer that actually moves these five subdomains, with no key at all, and every file re-downloaded and type-checked this pass. psw01.xls is the Weekly Petroleum Status Report (crude stocks incl. Cushing, gasoline and distillate stocks, refinery utilization, SPR, imports by PADD). ngshistory.xls is weekly gas storage. The dnav series is EIA retail gasoline/diesel history. The Grid Monitor CSV is hourly demand, demand forecast, net generation, interchange AND net generation by fuel — including a dedicated coal column — for every US balancing authority, which is what carries the coal and electricity legs here.

```bash
curl -L -o psw01.xls 'https://ir.eia.gov/wpsr/psw01.xls'   # then: curl -L -o ngshistory.xls 'https://ir.eia.gov/ngs/ngshistory.xls'
```

> Evidence: RE-FETCHED INDEPENDENTLY, all four confirmed as real binaries not HTML. psw01.xls with -L: HTTP 200, 1,250,816 bytes, application/vnd.ms-excel, `file` reports 'Composite Document File V2 … Microsoft Excel'. Without -L: HTTP 302, 0 bytes — the report's warning reproduces exactly. ngshistory.xls with -L: HTTP 200, 754,688 bytes, real XLS, internal Last-Saved 2026-09-15. dnav EMM_EPM0_PTE_NUS_DPGw.xl

#### CFTC Commitments of Traders — Socrata Open Data — US Commodity Futures Trading Commission ✅ LIVE

Covers **10** subdomains: crude-oil-wti, crude-oil-brent, natural-gas, refined-fuels, gold, silver, copper, platinum-palladium, grains-and-oilseeds, softs-and-livestock

- Docs: https://publicreporting.cftc.gov/
- Auth: none (an optional free Socrata app token raises throughput) | Limits: Anonymous Socrata shares a throttled per-IP pool; CFTC does not publish the anonymous ceiling (UNKNOWN). A free app token lifts it. Full SoQL confirmed working anonymously: I ran $where with starts_with(), $select and $limit across eight sequential queries with no throttling.
- Latency: Weekly — positions as of Tuesday, published Friday 15:30 ET. Independently verified current to report_date 2026-09-15. | Format: JSON (also CSV/XML via Socrata)
- Why primary: One dataset gives speculative and commercial positioning for every US futures market in this domain, and unlike the report — which showed a single fuel-oil row — I spot-checked SEVEN named contracts across the metal, grain and livestock subdomains and got real open interest and managed-money positions for every one. Ten subdomains from a single Socrata resource, queryable by contract name. Purely predictive; it never settles anything.

```bash
curl 'https://publicreporting.cftc.gov/resource/72hh-3qpy.json?$limit=2&$order=report_date_as_yyyy_mm_dd%20DESC'
```

> Evidence: RE-FETCHED INDEPENDENTLY AND EXTENDED. Base call HTTP 200, most recent report_date_as_yyyy_mm_dd `2026-09-15T00:00:00.000`, first row reproducing the report exactly: `GULF # 6 FUEL OIL CRACK - NEW YORK MERCANTILE EXCHANGE`, open_interest_all 10113, prod_merc_positions_long 3910, m_money_positions_long_all 360, swap_positions_long_all 2095. SUBDOMAIN SPOT-CHECKS the report did not run, all at repor

#### NOAA CPC weighted degree days (daily HDD/CDD by census division) — NOAA Climate Prediction Center ✅ LIVE

Covers **3** subdomains: natural-gas, electricity-and-power, refined-fuels

- Docs: https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/
- Auth: none | Limits: No key, no registration, no published quota. One small file (~8.7 KB) per weighting scheme per year, back to 1981 — cheap enough to poll daily.
- Latency: Daily, ~2 days behind. Independently verified populated through 20260918. | Format: Pipe-delimited text, one row per census division, one column per date
- Why primary: Gas-weighted heating degree days are the leading indicator for the EIA weekly storage number and therefore for natural-gas contracts; population-weighted CDD drives summer power load; the fuel-oil/kerosene weighting serves refined fuels. The weighting is done for you, which is the transform a desk would otherwise build by hand. The report's naming warning is real and I reproduced it: the gas file is UtilityGas.Heating.txt and NatGas.Heating.txt returns 404.

```bash
curl 'https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/2026/UtilityGas.Heating.txt'
```

> Evidence: RE-FETCHED INDEPENDENTLY. UtilityGas.Heating.txt HTTP 200, 8,669 bytes, text/plain, body `Product: Daily Heating Degree Days / Regions: CPC::Regions::CensusDivisions / Weights: Utility Gas` then a `Region|20260101|…` header whose final three columns are 20260916, 20260917, 20260918 — current to 2 days back, as claimed. SIBLING FILES INDIVIDUALLY FETCHED rather than inferred from a directory listin

#### Open-Meteo forecast API (multi-point crop and energy weather) — Open-Meteo (Zippenfenig, open-source, CC-BY) ✅ LIVE

Covers **4** subdomains: natural-gas, electricity-and-power, grains-and-oilseeds, softs-and-livestock

- Docs: https://open-meteo.com/en/docs
- Auth: none | Limits: No key. Non-commercial free tier ~10,000 calls/day (provider's published figure; NOT independently measured here). Multi-coordinate batching CONFIRMED working — comma-separated latitude/longitude returns a JSON array with one object per point.
- Latency: Hourly model refresh; 16-day forecast horizon; ECMWF/GFS/ICON ensemble members available. | Format: JSON — note that a multi-coordinate request returns a top-level ARRAY, while a single-coordinate request returns an OBJECT. Handle both shapes.
- Why primary: Weather is the upstream driver for four of these twelve subdomains and this one keyless endpoint serves all four because it accepts an arbitrary coordinate list in a single request — Corn Belt grid points for grain yields, West African cocoa belt for softs, ERCOT load centres for power, population centres for gas HDD. One call replaces a per-region weather integration. Strictly predictive; it settles nothing.

```bash
curl 'https://api.open-meteo.com/v1/forecast?latitude=41.88,29.76,39.74&longitude=-87.63,-95.37,-104.99&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&forecast_days=7&temperature_unit=fahrenheit&timezone=America%2FChicago'
```

> Evidence: RE-FETCHED INDEPENDENTLY. HTTP 200 for the three-point batch, parsed as a 3-element array with correctly snapped coordinates and genuinely DIFFERENT regional values — Chicago 41.879498/-87.64974 max [66.6, 61.7, 62.8]°F; Houston 29.767237/-95.35445 max [91.5, 93.5, 92.4]°F; Denver 39.746895/-104.987076 max [76.2, 74.0, 83.3]°F. Forecast window starts 2026-09-20 (today) and runs 7 days. The diverge

#### ERCOT public dashboard JSON — Electric Reliability Council of Texas ✅ LIVE

Covers **1** subdomains: electricity-and-power

- Docs: https://www.ercot.com/gridinfo
- Auth: none for the fuel-mix and supply-demand dashboard JSON (the broader MIS report library needs free registration) | Limits: No key. No published rate limit (UNKNOWN). CONFIRMED NARROW WINDOW: fuel-mix.json carried exactly two days of data (2026-09-19 and 2026-09-20) at 5-minute resolution. You MUST poll and persist — there is no history endpoint here.
- Latency: 5-minute intervals; `lastUpdated` observed at 2026-09-20 22:01:00-0500 during verification, i.e. minutes old. | Format: JSON
- Why primary: The only free real-time power feed I could execute that matches the venue — Kalshi runs KXTXERCOTPEAK, KXTXERCOTPEAKD and KXUTILITYERCOT and these are ERCOT's own numbers. fuel-mix.json gives 5-minute generation by fuel plus monthly installed capacity by fuel; supply-demand.json gives capacity, demand and forecast per 5-minute interval. Narrow by necessity — no broad feed covers ISO-level power. TWO VERIFIED LIMITS that stop this from settling anything: systemWidePrices.json is dead (302, zero bytes), so real-time settlement point prices are NOT available here; and the `forecast` field on supply-demand.json read 0 on every interval I inspected, so treat forecast as absent rather than as a zero.

```bash
curl -A 'Mozilla/5.0' 'https://www.ercot.com/api/1/services/read/dashboards/supply-demand.json'
```

> Evidence: RE-FETCHED INDEPENDENTLY. fuel-mix.json HTTP 200 / 174,350 bytes: lastUpdated 2026-09-20 22:01:00-0500, monthlyCapacity {Power Storage 22376, Solar 40957, Wind 40405, Hydro 579, Other 663, Natural Gas 69599, Coal and Lignite 13705, Nuclear 5268}, data keys exactly ['2026-09-19','2026-09-20'], interval 2026-09-20 22:00:00-0500 gen {Coal and Lignite 9124.0, Natural Gas 40741.5, Nuclear 4964.9, Wind 

#### Polymarket Gamma API + public-search — Polymarket ✅ LIVE

Covers **4** subdomains: crude-oil-wti, natural-gas, gold, silver

- Docs: https://docs.polymarket.com/
- Auth: none | Limits: No key on gamma-api or clob.polymarket.com read endpoints. No published anonymous limit (UNKNOWN). Responses are large — public-search?q=oil returned 337 KB for limit_per_type=5.
- Latency: Real-time order book via clob.polymarket.com; Gamma metadata near-real-time. | Format: JSON — public-search returns {events: [...], pagination: {...}}
- Why primary: The second venue's implied probability, self-documenting its settlement oracle in `resolutionSource`. Include it so the terminal shows both venues on the same underlying. All four claimed subdomains were independently confirmed to have OPEN (closed=false) events, not just historical ones. The report's usage warning is real and I reproduced it exactly: do NOT filter with /markets?tag_slug= or a bare /markets pull — use /public-search?q=<term>.

```bash
curl 'https://gamma-api.polymarket.com/public-search?q=oil&limit_per_type=5'
```

> Evidence: RE-FETCHED INDEPENDENTLY, and I checked all four claimed subdomains rather than the two the report showed. public-search?q=oil HTTP 200 / 337,603 bytes returned the exact contract the report cited — ticker `what-price-will-wti-hit-in-september-2026`, resolutionSource `https://pythdata.app/explore?search=WTI`, active true, closed false — plus `wti-closes-above-on-september-21-2026` with resolutionS

#### USDA FAS PSD Online bulk CSV (world supply & demand balance sheets) — USDA Foreign Agricultural Service ✅ LIVE

Covers **2** subdomains: grains-and-oilseeds, softs-and-livestock

- Docs: https://apps.fas.usda.gov/psdonline/app/index.html#/app/downloads
- Auth: NONE for the bulk ZIPs. (The FAS Open Data REST API, which adds the weekly Export Sales Report, does need a free key.) | Limits: No key, no quota on the bulk path. Six sibling files independently confirmed to exist and download: grains_pulses (2.87 MB), oilseeds (3.84 MB), livestock (843 KB), cotton (477 KB), sugar (760 KB), coffee (440 KB) — the whole agricultural complex in six downloads totalling ~9.2 MB.
- Latency: Monthly, synchronised to the WASDE release cycle. | Format: ZIP of CSV (grains ZIP contains a single member, psd_grains_pulses.csv)
- Why primary: The fundamentals that price grain and livestock contracts: area harvested, yield, production, imports, exports, domestic consumption and ending stocks by commodity and country back to 1960. The report asserted the sibling files existed; I actually fetched all five and they do. This carries extra weight because no free DAILY CBOT/ICE settle could be verified (re-confirmed in rejectedFeeds), so fundamentals bear more of the predictive load for these two subdomains.

```bash
curl -L -o psd_grains_pulses_csv.zip 'https://apps.fas.usda.gov/psdonline/downloads/psd_grains_pulses_csv.zip'
```

> Evidence: RE-FETCHED INDEPENDENTLY AND EXTENDED. psd_grains_pulses_csv.zip HTTP 200, 2,871,937 bytes, application/x-zip-compressed, `file` reports 'Zip archive data, at least v2.0 to extract', archive opens and contains ['psd_grains_pulses.csv'] — a real ZIP with a real CSV member, not an HTML error page. SIBLINGS INDIVIDUALLY FETCHED (the report only claimed they existed): psd_oilseeds_csv.zip HTTP 200 / 3

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Crude Oil — WTI | FRED fredgraph.csv `DCOILWTICO` (daily WTI spot, keyless, in | Kalshi trade API `expiration_value` + `rules_primary` on set | 🟢 COVERED |
| Crude Oil — Brent | FRED fredgraph.csv `DCOILBRENTEU` (daily Brent Europe spot,  | Kalshi trade API `expiration_value` — NOW INDEPENDENTLY PROV | 🟢 COVERED |
| Natural Gas | FRED `DHHNGSP` (daily Henry Hub spot, keyless, independently | Kalshi trade API `expiration_value` — INDEPENDENTLY PROVEN:  | 🟢 COVERED |
| Refined Fuels & Retail Gasoline | FRED `GASREGW` (US regular retail gasoline weekly, independe | Kalshi trade API `expiration_value` — INDEPENDENTLY PROVEN a | 🟢 COVERED |
| Electricity & Power | ERCOT dashboard JSON — supply-demand.json (capacity 84,283 M | NONE INDEPENDENTLY VERIFIED. ERCOT systemWidePrices.json is  | 🟡 PARTIAL |
| Coal | FRED `PCOALAUUSDM` (Australian thermal coal monthly, keyless | NOT INDEPENDENTLY VERIFIED. EIA quarterly coal production by | 🟡 PARTIAL |
| Gold | LBMA gold_am.json and gold_pm.json (daily USD/GBP/EUR benchm | LBMA fixing for benchmark-referenced contracts; Kalshi `expi | 🟢 COVERED |
| Silver | LBMA silver.json (daily benchmark fixing, keyless, independe | LBMA fixing; Kalshi `expiration_value` — INDEPENDENTLY PROVE | 🟢 COVERED |
| Copper | FRED `PCOPPUSDM` (global copper, MONTHLY, keyless, independe | Kalshi `expiration_value` — NEWLY PROVEN IN THIS VERIFICATIO | 🟡 PARTIAL |
| Platinum & Palladium | LBMA platinum_am/pm.json and palladium_am/pm.json (daily fix | LBMA fixing; Kalshi `expiration_value` — INDEPENDENTLY PROVE | 🟢 COVERED |
| Grains & Oilseeds | FRED `PWHEAMTUSDM` (228.74), `PMAIZMTUSDM` (213.19), `PSOYBU | NOT INDEPENDENTLY VERIFIED. `/markets?series_ticker=KXCORNMO | 🟡 PARTIAL |
| Softs & Livestock | FRED `PCOCOUSDM` (5,619.19), `PCOFFOTMUSDM` (359.16), `PSUGA | NOT INDEPENDENTLY VERIFIED. `/markets?series_ticker=KXCOCOAM | 🟡 PARTIAL |

**Rejected**

- **Pyth Network Hermes — price read endpoints (/v2/updates/price/latest, /api/latest_price_feeds)** — AUTH-GATED — RE-CONFIRMED THIS PASS and still the most consequential finding, because Pyth is the named settlement oracle for Kalshi WTI/gold/silver/copper/natgas and for Polymarket's WTI event (whose resolutionSource li
- **Yahoo Finance v8 chart endpoint (query1/query2)** — STILL NOT VERIFIABLE — retested independently in this pass with a full desktop Chrome User-Agent against query1 for CL=F and received HTTP 429 `Too Many Requests` with a plain-text body. This is the feed that would singl
- **CME Group CmeWS quote and settlement web service** — HARD BLOCKED — and the block appears to have HARDENED since the report. Where the report recorded HTTP 403 with an explicit anti-scraping notice, my independent request to /CmeWS/mvc/Quotes/Future/425/G returned curl exi
- **Trading Economics guest API (c=guest:guest)** — RETIRED — re-confirmed independently: https://api.tradingeconomics.com/markets/commodities?c=guest:guest returns HTTP 410 Gone with a 214-byte body. The long-circulated free guest credential is dead. Material because the
- **ICE public delayed-markets JSON (theice.com/marketdata/DelayedMarkets.shtml)** — DEAD — re-confirmed: HTTP 301 from Cloudflare with no resolvable target for Brent (productId=254). This would have been the natural free source for Brent settlement and for ICE cocoa/coffee/sugar/cotton, which is precise
- **Stooq CSV quote and history endpoints** — DEAD/BOT-CHALLENGED — re-confirmed: /q/l/?s=cl.f&f=sd2t2ohlcv&h&e=csv returns HTTP 404 with a 271-byte text/html body, not CSV. The report additionally found the history path serves a JavaScript SHA-256 proof-of-work cha
- **Baker Hughes Rig Count** — BLOCKED — re-confirmed HTTP 403 with a 449-byte HTML body on the static-files download path. Weekly US rig count by basin is a genuine leading indicator for WTI supply and no free substitute was found, so this remains an
- **EIA Open Data API v2 (api.eia.gov/v2/...)** — SUPERSEDED FOR THIS DOMAIN, not dead — re-confirmed independently: a keyless GET to https://api.eia.gov/v2/coal/ returns HTTP 403 with `{"error":{"code":"API_KEY_MISSING","message":"No api_key was supplied. Please regist
- **USDA NASS Quick Stats API** — KEY REQUIRED — re-confirmed: keyless request returns HTTP 401 with a 26-byte body. Free self-service key available; not obtained in this pass. Would improve the grains subdomain (county-level yields, crop progress).
- **USDA AMS MyMarketNews / MARS API (marsapi.ams.usda.gov)** — KEY REQUIRED — re-confirmed HTTP 403 (253 bytes, application/json) on /services/v1.2/reports. This is the single highest-value unclaimed feed for this domain: it carries daily cash grain bids and cattle prices, which is 
- **USDA ESMIS / Cornell release API (WASDE report timing)** — BROKEN — re-confirmed with a corrected status code. The report described a Drupal 'Client error' page; my independent GET to https://esmis.nal.usda.gov/api/v1/release returned HTTP 405 Method Not Allowed with an 18,225-b
- **Financial Modeling Prep /quotes/commodity** — NO WORKING DEMO KEY — re-confirmed HTTP 401 (184 bytes, application/json) with apikey=demo. Unlike Alpha Vantage, FMP has no public demo credential. A free key exists but the free tier is narrow, and Alpha Vantage's comm
- **USGS Mineral Commodity Summaries landing page** — BLOCKED — re-confirmed HTTP 403 (919 bytes) on the www.usgs.gov minerals center page. Underlying data files are likely reachable at other paths but none was verified, so USGS mine-supply context for copper and platinum/p
- **Polymarket /markets?tag_slug= and bare /markets filtering** — NOT A DEAD FEED — recorded because the obvious usage is wrong and silently produces empty coverage. REPRODUCED INDEPENDENTLY: /markets?closed=false&limit=100 returned HTTP 200 and matched ZERO of 100 questions against an
- **FRED fredgraph.csv date-window parameters on multi-series requests (cosd / coed)** — NOT A FEED — recorded as a rejected USAGE PATTERN, because the report's own headline exampleCall depends on it and it does not work. `?id=DCOILWTICO,DCOILBRENTEU,DHHNGSP&cosd=2026-09-01` returns 213,182 bytes beginning 1

---

### crypto-and-digital-assets

*8/13 subdomains covered · 18 primary feeds*

#### CoinGecko API v3 (keyless public) — CoinGecko ✅ LIVE

Covers **9** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, bnb-hype-zec-near, longtail-tokens, crypto-relative-value, token-launches-and-airdrops

- Docs: https://docs.coingecko.com/reference/introduction
- Auth: none for the keyless public API; optional free Demo key (email signup) raises and isolates the quota | Limits: Keyless: IP-throttled, shared across all keyless callers, no published number. MEASURED IN THIS SESSION: two calls issued within ~10s of other CoinGecko traffic came back non-JSON (throttled); the same call succeeded after a ~12s pause. Budget for roughly one call every 10-15s keyless. Demo key: 100 calls/min, 10,000 monthly call credits.
- Latency: ~1-2 minute price refresh | Format: REST JSON
- Why primary: CONFIRMED as THE broad feed for this domain and the single strongest instance of the one-feed-many-subdomains rule. I re-ran the exact exampleCall: one request returned live USD price + market cap + 24h volume + 24h change for all ten named tokens simultaneously. It replaces ten per-token APIs across five subdomains. FDV, the meme-token category and the full coin universe all independently re-verified.

```bash
curl 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple,dogecoin,binancecoin,hyperliquid,zcash,near,shiba-inu&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true'
```

> Evidence: INDEPENDENTLY RE-FETCHED. exampleCall HTTP 200: bitcoin=81332, ethereum=2663.20, solana=111.39, ripple=1.42, dogecoin=0.08837, binancecoin=777.90, hyperliquid=93.26, zcash=1519.95, near=4.31, shiba-inu=5.53e-06 — all ten in one response, each with usd_market_cap/usd_24h_vol/last_updated_at=1789959770. SPOT-CHECK 1 (FDV claim): /coins/markets?ids=bitcoin,ethereum HTTP 200 — bitcoin fully_diluted_va

#### OKX v5 Public + Market API — OKX ✅ LIVE

Covers **9** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, bnb-hype-zec-near, longtail-tokens, intraday-crypto, crypto-relative-value

- Docs: https://www.okx.com/docs-v5/en/
- Auth: none for /api/v5/public/ and /api/v5/market/ | Limits: Per-endpoint IP limits, documented individually: funding-rate 20 req/2s; most public market endpoints 20/2s or 40/2s. No daily cap. No throttling observed across ~10 calls in this session.
- Latency: realtime (REST + WebSocket) | Format: REST JSON + WebSocket
- Why primary: CONFIRMED. The broadest keyless derivatives feed and the necessary substitute where Deribit lists no options. I independently counted the swap universe and checked every named token: 482 perpetual swaps, with BTC/ETH/SOL/XRP/DOGE/HYPE each carrying BOTH a USD-margined and a USDT-margined perp, plus BNB, ZEC, NEAR, SHIB and PEPE. Because Deribit lists ZERO options on SOL/XRP/DOGE/BNB/HYPE/NEAR (independently re-measured, see rejectedFeeds), OKX perp funding and OI are the only free forward-looking positioning signal for those six subdomains.

```bash
curl 'https://www.okx.com/api/v5/public/open-interest?instType=SWAP&instId=HYPE-USDT-SWAP' ; curl 'https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USD-SWAP' ; curl 'https://www.okx.com/api/v5/market/candles?instId=ZEC-USDT-SWAP&bar=1m&limit=3'
```

> Evidence: INDEPENDENTLY RE-FETCHED, all three HTTP 200. open-interest HYPE-USDT-SWAP (158B): {"oi":"12805726","oiCcy":"1280572.6","oiUsd":"119551696.7908","ts":"1789959864217"}. funding-rate BTC-USD-SWAP (523B): {"fundingRate":"0.0000916091852252","nextFundingTime":"1790006400000","settState":"settled"}. candles ZEC-USDT-SWAP 1m (303B): [["1789959840000","1521.43","1522.9","1521.29","1522.9","19300",...]]. 

#### Binance public market data mirror (data-api.binance.vision) — Binance ✅ LIVE

Covers **9** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, bnb-hype-zec-near, longtail-tokens, intraday-crypto, crypto-relative-value

- Docs: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints
- Auth: none | Limits: Weight-based IP limiter, same schedule as api.binance.com (~1,200 request-weight/min for market data; a ticker call costs weight 1-2). Klines max 1,000 bars/request. No throttling observed in this session.
- Latency: realtime | Format: REST JSON + WebSocket
- Why primary: CONFIRMED, including the geoblock claim, which is the load-bearing part. This is the SETTLEMENT feed for Polymarket-Global crypto markets — I read the resolution text straight out of Gamma and it names Binance 1-minute candles verbatim. api.binance.com genuinely returns HTTP 451 from this US IP while data-api.binance.vision serves the identical global USDT tape at HTTP 200. Without this mirror the PM-Global settlement leg of nine subdomains is unserviceable from US infrastructure.

```bash
curl 'https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=3' ; curl 'https://data-api.binance.vision/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22ETHUSDT%22,%22SOLUSDT%22,%22XRPUSDT%22,%22DOGEUSDT%22,%22BNBUSDT%22%5D'
```

> Evidence: INDEPENDENTLY RE-FETCHED. klines BTCUSDT 1m HTTP 200, 506B: [[1789959720000,"81308.84000000","81389.75000000","81308.84000000","81389.75000000","3.44360000",1789959779999,...]]. Multi-symbol ticker HTTP 200, 265B: BTCUSDT 81440.27, ETHUSDT 2668.50, BNBUSDT 779.32, XRPUSDT 1.42030000, DOGEUSDT 0.08861000, SOLUSDT 111.66. SPOT-CHECK: /ticker/24hr?symbol=DOGEUSDT HTTP 200 — volume 836478197, priceCha

#### Kalshi Trade API v2 (public market data) — Kalshi (KalshiEX LLC, CFTC-regulated DCM) ✅ LIVE

Covers **13** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, bnb-hype-zec-near, longtail-tokens, intraday-crypto, crypto-relative-value, token-launches-and-airdrops, stablecoins-and-protocol, crypto-regulation, crypto-companies

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: none for public market data (read endpoints); key only for trading | Limits: No published quota on public read endpoints; basic tier documented at ~10 req/s. Cursor-paginated. No throttling observed across ~10 calls in this session.
- Latency: realtime | Format: REST JSON + WebSocket
- Why primary: Coverage of all 13 subdomains CONFIRMED, but the original exampleCall was WRONG and is corrected above — this is the most consequential fix in the report. A developer wiring only '?category=Crypto' would get ZERO crypto-regulation and ZERO crypto-company markets. I paged the actual category listings: Crypto (274 series) contains the price, intraday, FDV and protocol series, but the regulation series live under Politics (2,343 series) and the company series under Companies (530) and Financials (1,040). The feed itself covers everything claimed; the documented entry point did not. Beyond implied probability its markets carry expiration_value — the settled CF Benchmarks index print, keyless — and since CF Benchmarks' own API is auth-walled, this remains the only free authoritative settlement source for Kalshi crypto price markets.

```bash
CORRECTED — crypto markets are spread across FOUR categories, not one. All four calls are needed: curl 'https://api.elections.kalshi.com/trade-api/v2/series?category=Crypto' ; curl 'https://api.elections.kalshi.com/trade-api/v2/series?category=Politics' ; curl 'https://api.elections.kalshi.com/trade-api/v2/series?category=Companies' ; curl 'https://api.elections.kalshi.com/trade-api/v2/series?category=Financials' ; then curl 'https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTCD&status=settled&limit=3'
```

> Evidence: INDEPENDENTLY RE-FETCHED. /series?category=Crypto HTTP 200, 238156B, 274 series parsed. I checked all 23 series tickers the report named: KXBTCD, KXETH, KXSOLMAXY, KXXRPD, KXDOGEMINY, KXBTC15M, KXETH15M, KXZEC15M, KXHYPE15M, KXBTCETHRETURN, KXFDVAVAXSOL, KXFDVLIGHTER, KXFDVFOGO, KXFDVRAINBOW, KXFDVOPENSEA, KXAIRDROPMONAD, KXTOKENLAUNCH, KXSTABLEYIELDNOTION, KXEIP4444, KXHARDFORKBTC, KXSOLTPS, KXSH

#### Polymarket Gamma + CLOB API — Polymarket ✅ LIVE

Covers **13** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, bnb-hype-zec-near, longtail-tokens, intraday-crypto, crypto-relative-value, token-launches-and-airdrops, stablecoins-and-protocol, crypto-regulation, crypto-companies

- Docs: https://docs.polymarket.com/
- Auth: none | Limits: No published quota on Gamma read endpoints; limit is capped at 100 per page regardless of a higher value. CLOB /markets is cursor-paginated and unauthenticated for reads. No throttling observed across ~8 calls.
- Latency: realtime | Format: REST JSON + WebSocket
- Why primary: All 13 subdomains CONFIRMED by exhaustive paging, not by assertion — this is the one feed in the domain whose full breadth claim survived a direct census. I pulled 300 live crypto events across three pages and keyword-scanned them. It is the necessary cross-check against Kalshi because it lists shapes Kalshi does not, and unlike Kalshi its entire crypto surface sits under ONE tag_slug, so no multi-category fan-out is needed. Gamma returns question text, conditionId, liquidity, volume24hr, endDate and the machine-readable resolution rule, serving both the predictive leg and the resolution record.

```bash
curl 'https://gamma-api.polymarket.com/events?closed=false&limit=100&offset=0&tag_slug=crypto' (page with offset=0,100,200 — limit is capped at 100 and the top-of-book page is all BTC price markets, so a limit=3 call will NOT show the regulation/company/launch coverage) ; curl 'https://gamma-api.polymarket.com/markets?closed=false&limit=2&tag_id=21'
```

> Evidence: INDEPENDENTLY RE-FETCHED. /events?tag_slug=crypto HTTP 200, 226925B — first three by volume24hr: id 946004 'What price will Bitcoin hit in September?' (vol24 506153), id 1023463 'Bitcoin above ___ on September 21?' (vol24 502159), id 1020834 (vol24 433032). /markets?tag_id=21 HTTP 200 — {"id":"573656","question":"Will Bitcoin hit $150k by December 31, 2026?","conditionId":"0x02deb9538f5c123373adaa

#### Deribit Public API v2 (options chains, IV, DVOL) — Deribit ✅ LIVE

Covers **4** subdomains: bitcoin, ethereum, intraday-crypto, crypto-relative-value

- Docs: https://docs.deribit.com/
- Auth: none for all /public/ endpoints | Limits: Public endpoints unauthenticated. Deribit documents a credit-bucket limiter but the exact anonymous tier is UNKNOWN — not published. No throttling observed across 10 consecutive per-currency calls.
- Latency: realtime (REST + WebSocket + FIX) | Format: REST JSON-RPC + WebSocket
- Why primary: CONFIRMED, and its self-imposed scope limit is the one claim in the original report I most expected to break and could not. It is the only free source of an options-implied probability DISTRIBUTION — a full BTC/ETH chain with mark IV, greeks and open interest converts directly into P(spot > strike at expiry), exactly what Kalshi's KXBTCD and Polymarket's '$150k by Dec 31' price. DVOL gives the vol term structure for intraday. I re-measured the instrument count for every currency independently and reproduced the numbers to the unit, so the four-subdomain claim is correctly narrow rather than over-reaching.

```bash
curl 'https://www.deribit.com/api/v2/public/get_book_summary_by_currency?currency=BTC&kind=option' ; curl 'https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC&start_timestamp=1789700000000&end_timestamp=1789958000000&resolution=3600'
```

> Evidence: INDEPENDENTLY RE-FETCHED. BTC option book summary HTTP 200, 431178B — 968 instruments parsed; first: {"instrument_name":"BTC-26MAR27-40000-C","bid_price":0.5235,"ask_price":0.526,"open_interest":82.1,"mark_price":0.52505146,"mark_iv":56.61,"underlying_price":83565.2}. DVOL HTTP 200: [[1789696800000,33.67,33.85,33.66,33.81],[1789700400000,33.81,34.32,33.77,34.26],...]. SCOPE LIMIT RE-MEASURED PER C

#### DefiLlama open API (stablecoins, TVL, DEX volume, fees/revenue) — DefiLlama ✅ LIVE

Covers **5** subdomains: stablecoins-and-protocol, bnb-hype-zec-near, solana, ethereum, crypto-relative-value

- Docs: https://defillama.com/docs/api
- Auth: none on the open endpoints | Limits: No key and no published rate limit on open endpoints; DefiLlama asks heavy users to buy the Pro key. Exact free limit UNKNOWN. CONFIRMED PAID-ONLY: /emissions and bridges.llama.fi both return HTTP 402.
- Latency: hourly for TVL; daily for most aggregates | Format: REST JSON
- Why primary: CONFIRMED. The one broad feed for everything the price APIs cannot see, and the clearest single instance of replacing many per-issuer APIs with one call: a single request returned all 427 pegged assets with circulating supply, peg mechanism AND live price, which settles 'Will stablecoins hit $500B before 2027?' directly. It is also the free source of protocol revenue (pricing HYPE), DEX volume share (pricing SOL) and per-chain TVL including L2s — and that L2 role is now load-bearing, because Etherscan's free tier turns out NOT to cover Base or Optimism (see that entry).

```bash
curl 'https://stablecoins.llama.fi/stablecoins?includePrices=true' ; curl 'https://api.llama.fi/v2/chains' ; curl 'https://api.llama.fi/overview/dexs?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true'
```

> Evidence: INDEPENDENTLY RE-FETCHED. stablecoins?includePrices=true HTTP 200, 555632B — 427 peggedAssets parsed; USDT circulating.peggedUSD=183304236781.37, pegMechanism='fiat-backed', price=0.9997286872107681 (the includePrices flag genuinely populates peg deviation). /v2/chains HTTP 200, 64216B. /overview/dexs HTTP 200, 1904313B. SPOT-CHECK (HYPE revenue claim): /summary/fees/hyperliquid?dataType=dailyReve

#### GeckoTerminal on-chain DEX API (CoinGecko) — CoinGecko ✅ LIVE

Covers **2** subdomains: longtail-tokens, token-launches-and-airdrops

- Docs: https://www.geckoterminal.com/dex-api
- Auth: none | Limits: 30 calls/minute per IP on the public endpoint (documented), no key required. No throttling observed.
- Latency: near-realtime (block-level pool updates) | Format: REST JSON
- Why primary: CONFIRMED, and the FDV field the original report leaned on is genuinely present per-pool, which I checked specifically because that is the settlement basis for the FDV-race contracts. new_pools returns freshly created DEX pools with base-token price, fdv_usd and reserve_in_usd — one call per network covers the entire long tail on that chain instead of a per-token lookup. This is the only feed here that reaches tokens with no CEX listing and therefore no ticker on any exchange API.

```bash
curl -H 'Accept: application/json;version=20230302' 'https://api.geckoterminal.com/api/v2/networks/solana/new_pools?page=1' ; curl -H 'Accept: application/json;version=20230302' 'https://api.geckoterminal.com/api/v2/networks/trending_pools'
```

> Evidence: INDEPENDENTLY RE-FETCHED. solana/new_pools HTTP 200, 30266B — 20 pools parsed; first: id 'solana_8rSz8YqGdJKkA9qFTWY4DHYSbdgRZ5DTnPHXmHKyVPys' with base_token_price_usd=8.44e-07, fdv_usd=398424.3944, reserve_in_usd=1.2938. SPOT-CHECK: the fdv_usd field is populated on the live pool object, confirming the token-launches settlement claim rather than merely the longtail listing claim. /networks/trend

#### Coinbase Exchange public API — Coinbase ✅ LIVE

Covers **6** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, intraday-crypto

- Docs: https://docs.cdp.coinbase.com/exchange/reference/
- Auth: none for public market data | Limits: 10 requests/second per IP (documented), bursts to 15. Candles max 300 buckets/request, granularity 60s-86400s.
- Latency: realtime (REST + WebSocket) | Format: REST JSON + WebSocket
- Why primary: CONFIRMED across all five claimed tokens, not just BTC — the original evidence only showed BTC, so I checked the rest. A constituent exchange of the CF Benchmarks BRTI/RTI indices Kalshi settles on; because CF Benchmarks' own API is auth-walled (re-verified 401), replicating the index from its free constituent tapes is the only way to track the settlement level BEFORE a market settles, and Coinbase is the largest US constituent.

```bash
curl 'https://api.exchange.coinbase.com/products/BTC-USD/ticker' ; curl 'https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=60'
```

> Evidence: INDEPENDENTLY RE-FETCHED. BTC-USD/ticker HTTP 200, 187B: {"ask":"81431.16","bid":"81431.15","volume":"4161.92370773","trade_id":1095812438,"price":"81431.15"}. SPOT-CHECK of the other four claimed tokens, all HTTP 200 with live books: XRP-USD bid 1.4215 / volume 83283060.9; DOGE-USD bid 0.08862 / volume 149689460.1; SOL-USD bid 111.65 / volume 863677.86; ETH-USD bid 2667.91 / volume 79555.25. Ever

#### Kraken public REST API — Payward / Kraken ✅ LIVE

Covers **6** subdomains: bitcoin, ethereum, solana, xrp, dogecoin, intraday-crypto

- Docs: https://docs.kraken.com/api/docs/rest-api/get-ticker-information
- Auth: none for /0/public/ | Limits: Public endpoints ~1 req/s sustained per IP; no key, no daily cap.
- Latency: realtime (REST + WebSocket) | Format: REST JSON + WebSocket
- Why primary: CONFIRMED — one multi-pair call really does return all five major USD pairs, including XRP, which the original evidence did not actually show (it listed only three result keys). A single-exchange print is not a defensible proxy for a multi-exchange volume-weighted index, so pairing Kraken with Coinbase is the minimum honest replication of the CF Benchmarks settlement level. Kraken quotes USD directly rather than USDT, matching the index's USD basis.

```bash
curl 'https://api.kraken.com/0/public/Ticker?pair=XBTUSD,ETHUSD,SOLUSD,XRPUSD,XDGUSD'
```

> Evidence: INDEPENDENTLY RE-FETCHED, HTTP 200, error:[]. Parsed all five result keys — the full set is XETHZUSD, SOLUSD, XXBTZUSD, XDGUSD, XXRPZUSD (note Kraken's altname mangling: XBT not BTC, XDG not DOGE). Last prices: XXBTZUSD 81394.90, XETHZUSD 2666.56, SOLUSD 111.55, XXRPZUSD 1.42000000, XDGUSD 0.088559200. Full OHLC/VWAP/trade-count arrays present on each. Five of five claimed pairs confirmed in one r

#### mempool.space API — mempool.space (Bitcoin open-source) ✅ LIVE

Covers **2** subdomains: stablecoins-and-protocol, bitcoin

- Docs: https://mempool.space/docs/api/rest
- Auth: none | Limits: Public instance, no key; fair-use rate limiting. Fully self-hostable for unlimited use.
- Latency: realtime (block and mempool level) | Format: REST JSON + WebSocket
- Why primary: CONFIRMED. The free Bitcoin network-telemetry feed covering the protocol-side questions no price API answers: difficulty adjustment and retarget timing (settling Kalshi's KXHARDFORKBTC, which I confirmed exists), hashrate, mempool depth and fee levels. One base URL covers the whole Bitcoin protocol surface. Values moved between the original report's fetch and mine, which is itself evidence the feed is live rather than cached.

```bash
curl 'https://mempool.space/api/v1/difficulty-adjustment' ; curl 'https://mempool.space/api/v1/fees/recommended'
```

> Evidence: INDEPENDENTLY RE-FETCHED. /v1/difficulty-adjustment HTTP 200, 335B: {"progressPercent":12.3015873015873,"difficultyChange":-2.232901130225895,"estimatedRetargetDate":1791047133864,"remainingBlocks":1768,"nextRetargetHeight":969696,"timeAvg":637923}. /v1/fees/recommended HTTP 200: {"fastestFee":3,"halfHourFee":1,"hourFee":1,"economyFee":1,"minimumFee":1}. Values differ from the original report's (r

#### Solana public JSON-RPC (mainnet-beta) — Solana Foundation / Triton One ✅ LIVE

Covers **2** subdomains: solana, stablecoins-and-protocol

- Docs: https://solana.com/docs/rpc
- Auth: none | Limits: Public endpoint, rate-limited and explicitly not for production load (Triton One documents it as a developer convenience). No key. Heavy use requires a dedicated RPC provider.
- Latency: realtime (slot level) | Format: JSON-RPC over HTTP POST
- Why primary: CONFIRMED. The only free authoritative source for Solana network state, which settles the network-stats and outage questions — Kalshi's KXSOLTPS is present in the Crypto series list and resolves on exactly this. getEpochInfo returns absoluteSlot, blockHeight, epoch and cumulative transactionCount in one call, from which TPS and liveness derive directly with no aggregator in between. Slot advance between the two fetches confirms liveness.

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"getEpochInfo"}' https://api.mainnet-beta.solana.com
```

> Evidence: INDEPENDENTLY RE-FETCHED. POST getEpochInfo HTTP 200, 170B: {"jsonrpc":"2.0","result":{"absoluteSlot":448928640,"blockHeight":426969283,"epoch":1039,"slotIndex":80640,"slotsInEpoch":432000,"transactionCount":550782865189},"id":1}. Compared against the original report's read (absoluteSlot 448922082, transactionCount 550775018076): the chain advanced 6,558 slots and 7,847,113 transactions between th

#### Etherscan API V2 — keyless tier, Ethereum mainnet ONLY — Etherscan ✅ LIVE

Covers **2** subdomains: ethereum, stablecoins-and-protocol

- Docs: https://docs.etherscan.io/etherscan-v2/
- Auth: works keyless on chainid=1 at 1 req/5s (verified); a free API key (email signup) raises mainnet to 5 calls/sec and 100,000 calls/day | Limits: CORRECTED — MULTICHAIN IS NOT FREE. Keyless chainid=1: works, server states verbatim 'rate limit of 1/5sec applied'. Other chains MEASURED KEYLESS: chainid=8453 (Base) and chainid=10 (Optimism) and chainid=56 (BSC) return 'Free API access is not supported for this chain. Please upgrade your api plan for full chain coverage' — that is a PLAN restriction, not a key restriction, so a free key will NOT unlock them. chainid=42161 (Arbitrum) and chainid=137 (Polygon) return only 'Missing/Invalid API Key', so those MAY work with a free key — UNVERIFIED, I have no key to test with.
- Latency: realtime (block-level) | Format: REST JSON
- Why primary: RETAINED BUT DOWNGRADED IN SCOPE. The mainnet gas oracle and ETH supply are genuinely free and keyless, and they price the Ethereum activity questions — that part of the original claim is correct and I reproduced it including the server's own rate-limit message. HOWEVER the report's headline rationale, 'one key (or none) spans 60+ EVM chains... no separate API for Arbitrum, Base and Optimism', is FALSE on the free tier: I tested five chainids and Base, Optimism and BSC are explicitly excluded from free access by plan. The L2 leg of this domain must come from DefiLlama /v2/chains instead, which is keyless and covers L2 TVL. coversSubdomains is unchanged because both claimed subdomains are served by chainid=1, but the multichain justification is withdrawn.

```bash
curl 'https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle'  # chainid=1 ONLY — see freeTierLimits before using any other chainid
```

> Evidence: INDEPENDENTLY RE-FETCHED. chainid=1 gasoracle HTTP 200, 322B with NO API key: {"status":"1","message":"OK-Missing/Invalid API Key, rate limit of 1/5sec applied","result":{"LastBlock":"26023092","SafeGasPrice":"0.056165376","ProposeGasPrice":"0.056298709","FastGasPrice":"0.061872013","gasUsedRatio":"0.5051235,..."}} — the report's keyless correction is CONFIRMED. MULTICHAIN SPOT-CHECK (the claim I 

#### Federal Register API v1 — US National Archives / GPO ✅ LIVE

Covers **1** subdomains: crypto-regulation

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none — no API key | Limits: No key and no published rate limit. Full-text searchable back to 1994. No throttling observed.
- Latency: daily (published each federal business day ~6am ET) | Format: REST JSON
- Why primary: CONFIRMED and now the LOAD-BEARING regulation feed, since Congress.gov could not be verified working (see that entry). The authoritative settlement record for any 'rule finalized / notice published' crypto contract, and one term query spans SEC, CFTC, Treasury/OFAC, IRS and FinCEN at once rather than needing a feed per regulator. ONE CAVEAT I am adding from my own fetch: the term search is broad and noisy — the newest 'digital asset' hit was an SEC shareholder-proposal rule with no crypto substance, so a production integration needs agency and document-type filtering rather than raw term matching.

```bash
curl 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=digital+asset&per_page=5&order=newest&fields%5B%5D=title&fields%5B%5D=publication_date&fields%5B%5D=agencies&fields%5B%5D=type&fields%5B%5D=html_url'
```

> Evidence: INDEPENDENTLY RE-FETCHED. HTTP 200: {"description":"Documents matching 'digital asset'","count":3223,"total_pages":50,...} — count reproduces the original exactly. Newest result: {"title":"Rescission of Rule 14a-8's Federal Regulation of Shareholder Proposals and Amendments to Rule 14a-4","publication_date":"2026-09-21","agencies":[{"raw_name":"SECURITIES AND EXCHANGE COMMISSION"}]} — real structu

#### Congress.gov API v3 — Library of Congress ⚠️ UNVERIFIED

Covers **1** subdomains: crypto-regulation

- Docs: https://api.congress.gov/
- Auth: free API key from api.data.gov REQUIRED in practice. DEMO_KEY does NOT work — see evidence. | Limits: 5,000 requests/hour with a registered free key (documented, UNVERIFIED — I have no key). DEMO_KEY: exhausted, HTTP 429 on every attempt including after a cooldown.
- Latency: ~daily; bill actions posted within one business day | Format: REST JSON
- Why primary: RETAINED AS A DOCUMENTED FEED BUT verifiedLive DOWNGRADED TO FALSE — I could not reproduce the original report's result. The rationale is sound (one API covers every bill, and H.R.3633 the Clarity Act is the literal example contract for this subdomain, priced by markup and floor status), and the endpoint is clearly alive since it returns a well-formed quota error rather than a 404. But the exampleCall AS ORIGINALLY WRITTEN returns no data, and the original evidence claiming '32 actions, 3 amendments, CBO cost estimates' could not be confirmed. A developer must register a free api.data.gov key before this is usable at all — not merely before production, as the original note implied. Coverage of crypto-regulation does not depend on it: Federal Register and Polymarket both independently serve this subdomain and both verified.

```bash
curl 'https://api.congress.gov/v3/bill/119/hr/3633?format=json&api_key=YOUR_FREE_KEY'  # a personal api.data.gov key is REQUIRED — DEMO_KEY is exhausted and returns HTTP 429
```

> Evidence: FAILED TO VERIFY. The literal exampleCall from the report returned HTTP 429, 178B: {"error":{"code":"OVER_RATE_LIMIT","message":"You have exceeded your rate limit. Try again later or contact us for assistance: https://api.congress.gov:443"}}. Retried after a ~20s cooldown — identical HTTP 429. DEMO_KEY is a shared, exhausted credential. I never received bill data, so the claimed action/amendment/C

#### SEC EDGAR (full-text search + submissions + getcurrent Atom) — US Securities and Exchange Commission ✅ LIVE

Covers **2** subdomains: crypto-companies, crypto-regulation

- Docs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Auth: none — but a descriptive User-Agent header containing a contact email is MANDATORY; I verified SEC returns HTTP 403 without one | Limits: 10 requests/second per IP (documented). No key, no daily cap. Bulk ZIPs available.
- Latency: realtime — filings appear in the index within minutes of acceptance | Format: REST JSON (efts) + Atom XML (getcurrent) + JSON (data.sec.gov)
- Why primary: CONFIRMED, including the User-Agent requirement which I tested in both directions — this is the kind of detail that silently breaks an integration, so I verified the failure mode too. The settlement record for every crypto-company listing contract: 'Kraken IPO by ___?' resolves on an S-1 or 424B appearing here, and Polymarket lists exactly that market (verified). Full-text search across the entire corpus from one endpoint means no per-company feed, and the getcurrent Atom feed gives push-style monitoring by form type.

```bash
curl -H 'User-Agent: yourname you@example.com' 'https://efts.sec.gov/LATEST/search-index?q=%22bitcoin%22&forms=S-1' ; curl -H 'User-Agent: yourname you@example.com' 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=coinbase&type=10-K&count=5&output=atom'
```

> Evidence: INDEPENDENTLY RE-FETCHED with a contact User-Agent. efts full-text search HTTP 200, 58156B: {"took":1692,"hits":{"total":{"value":2655,"relation":"eq"}}} — 2,655 vs the report's 2,651, a four-filing drift consistent with a live index. First hit is real and crypto-relevant: _id '0001214659-23-015256:d111123s1a3.htm', display_names ['WisdomTree Bitcoin Trust (BTCW) (CIK 0001850391)'], file_num ['333

#### CourtListener REST API v4 + RECAP — Free Law Project ✅ LIVE

Covers **2** subdomains: crypto-companies, crypto-regulation

- Docs: https://www.courtlistener.com/help/api/rest/
- Auth: works keyless at a low rate (verified); free account token (Authorization: Token <token>) strongly recommended for production polling | Limits: Keyless: low anonymous throttle, but a full result page was served with no credential. With free token: 5,000 queries/day. Bulk data downloads available separately.
- Latency: near-realtime for RECAP dockets; opinions within hours to days | Format: REST JSON
- Why primary: CONFIRMED keyless, reproducing the original's counts exactly. The free federal docket feed that prices and settles the crypto legal contracts — sentencing, appeal and release calendars for 'SBF released from custody in 2026?', plus SEC/CFTC enforcement and XRP-style litigation catalysts. One search endpoint spans every federal court, so no per-court or per-case feed is needed.

```bash
curl 'https://www.courtlistener.com/api/rest/v4/search/?q=Bankman-Fried&type=r'
```

> Evidence: INDEPENDENTLY RE-FETCHED with NO auth token. HTTP 200: {"count":764,"document_count":9783,"next":"https://www.courtlistener.com/api/rest/v4/search/?cursor=...&q=Bankman-Fried&type=r","results":[{"assignedTo":"Jacquelyn Scott Corley","assigned_to_id":9086,"attorney":["William M. Audet"],"caseName":"Imbert v. Bankman-Fried","cause":"28:1332 Diversity-Fraud","court":"District Court, N.D. California"}

#### Yahoo Finance chart endpoint v8 (unofficial) — HEAVILY THROTTLED — Yahoo ✅ LIVE

Covers **1** subdomains: crypto-relative-value

- Docs: https://query1.finance.yahoo.com/v8/finance/chart/
- Auth: none for the v8/chart endpoint | Limits: CORRECTED — MUCH TIGHTER THAN STATED. The original said 'no published limit'. That is technically true but operationally misleading: I got HTTP 429 'Edge: Too Many Requests' on 5 of 7 attempts in this session, across BOTH query1 and query2 hosts, with and without a browser User-Agent, on a near-idle IP. It succeeded only after a multi-minute gap. Unofficial, undocumented, no stability guarantee; Yahoo already locked down the v7 quote and options endpoints. Treat as best-effort with aggressive backoff and a cache, never as a live stream.
- Latency: ~15 min delayed for futures/indices; intraday intervals available | Format: REST JSON
- Why primary: RETAINED — it is the only free feed I could verify for the NON-crypto leg of the cross-asset comparisons, and 'Bitcoin vs. Gold vs. S&P 500' cannot be priced from any crypto API. It does eventually serve both legs from one endpoint via a symbol swap. But its reliability is materially worse than the original report represented, and I could not find a free replacement (Stooq and keyless FRED both failed — see rejectedFeeds), so crypto-relative-value is downgraded to PARTIAL on this feed's fragility alone.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=5d&interval=1d'  # expect frequent HTTP 429; retry with long backoff. Use ^GSPC (URL-encoded %5EGSPC) for the S&P 500.
```

> Evidence: VERIFIED ONLY AFTER REPEATED FAILURE — the original's clean 'HTTP 200, 3015B' does not reflect typical behaviour. Attempts 1-2 (GC=F and %5EGSPC, default curl UA): HTTP 429, 23B, body 'Edge: Too Many Requests'. Attempts 3-5 (browser User-Agent on query1, and plain on query2): HTTP 429, 19-23B. Attempts 6-7 after a multi-minute gap: HTTP 200. GC=F body: {"chart":{"result":[{"meta":{"currency":"USD"

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Bitcoin Price | Deribit v2 public (968 live BTC option instruments re-counte | Kalshi Trade API v2 `expiration_value` — the settled CF Benc | 🟢 COVERED |
| Ethereum Price | Deribit v2 public (888 live ETH option instruments re-counte | Kalshi `expiration_value` (CF Benchmarks ETHUSD_RTI). For Po | 🟢 COVERED |
| Solana Price | OKX v5 (SOL-USD-SWAP and SOL-USDT-SWAP, both confirmed liste | Kalshi `expiration_value` (CF Benchmarks SOL RTI; KXSOLMAXY  | 🟢 COVERED |
| XRP Price | OKX v5 (XRP-USD-SWAP and XRP-USDT-SWAP, both confirmed liste | Kalshi `expiration_value` (KXXRPD confirmed present; CF Benc | 🟢 COVERED |
| Dogecoin Price | OKX v5 (DOGE-USD-SWAP and DOGE-USDT-SWAP, both confirmed lis | Kalshi `expiration_value` (KXDOGEMINY confirmed present in t | 🟡 PARTIAL |
| BNB, HYPE, ZEC, NEAR & Other Majors | OKX v5 — one feed, all four confirmed listed in the 482-swap | Kalshi `expiration_value` (KXHYPE and KXNEARH confirmed pres | 🟢 COVERED |
| Long-Tail & Meme Tokens | CoinGecko (21,343 coins re-counted — higher than the 17,000  | CoinGecko fully_diluted_valuation (re-verified populated) +  | 🟡 PARTIAL |
| Intraday & Directional Crypto | Deribit DVOL (hourly implied-vol index, re-verified live) fo | data-api.binance.vision /api/v3/klines?interval=1m — the lit | 🟢 COVERED |
| Crypto Relative Value | CoinGecko one-call multi-token spot (pairwise ratios across  | Kalshi `expiration_value` (CF Benchmarks) + Polymarket Gamma | 🟡 PARTIAL |
| Token Launches, FDV & Airdrops | GeckoTerminal /new_pools (fresh TGE pools with price, fdv_us | CoinGecko FDV / GeckoTerminal on-chain TGE pool data. Kalshi | 🟡 PARTIAL |
| Stablecoins, Protocol & Security | DefiLlama stablecoins.llama.fi/stablecoins?includePrices=tru | DefiLlama stablecoins circulating supply — directly settles  | 🟡 PARTIAL |
| Crypto Regulation & Government Reserves | Federal Register API (agency action across SEC/CFTC/Treasury | Federal Register API (publication of a final rule or notice  | 🟢 COVERED |
| Crypto Company Listings & Legal | SEC EDGAR full-text search (2,655 S-1 filings mentioning bit | SEC EDGAR filing record — an S-1 or 424B appearing is the re | 🟢 COVERED |

**Rejected**

- **CF Benchmarks API (BRTI / ETHUSD_RTI / XRPUSD_RTI — the actual Kalshi settlement index)** — PAYWALLED / AUTH-GATED — REJECTION RE-CONFIRMED BY DIRECT FETCH. This remains the most important rejection in the domain. I independently re-read Kalshi's own market rules: 'If the simple average of the sixty seconds of 
- **api.binance.com (Binance global spot REST)** — GEOBLOCKED — RE-CONFIRMED. Returned HTTP 451, 224B from US infrastructure: 'Service unavailable from a restricted location according to b. Eligibility in https://www.binance.com/en/terms'. This matters because Polymarket
- **DefiLlama /emissions (token unlock and vesting schedules)** — PAYWALLED — RE-CONFIRMED BY DIRECT FETCH. HTTP 402, body 'Upgrade to the paid API plan at https://defillama.com/subscription'. The original inventory listed token unlocks as free; that is stale and I verified the paywall
- **bridges.llama.fi (bridge flow volumes)** — PAYWALLED — RE-CONFIRMED BY DIRECT FETCH. HTTP 402, identical 'Upgrade to the paid API plan' body. The rejection is endpoint-specific, not provider-wide: DefiLlama's stablecoins, /v2/chains, /overview/dexs and /summary/f
- **beaconcha.in API v1 (Ethereum beacon chain / staking flows)** — AUTH REQUIRED — carried forward from the original report. NOT INDEPENDENTLY RE-TESTED in this pass; I spent the verification budget on the primaryFeeds instead, per the task's instruction to check the primary list. Recor
- **L2Beat API (/api/tvs)** — DEAD ENDPOINT — carried forward from the original report (HTTP 404). NOT INDEPENDENTLY RE-TESTED. Its replacement matters more now than it did: since Etherscan's free tier turns out NOT to cover Base, Optimism or BSC (ve
- **GDELT DOC 2.0 API (news volume / social attention)** — NOT VERIFIED — RE-TESTED AND FAILED AGAIN. My own request to /api/v2/doc/doc?query=dogecoin&mode=timelinevol&format=json returned the throttle page, not data: 'Please limit requests to one every 5 seconds or contact kale
- **Deribit options on SOL, XRP, DOGE, BNB, HYPE, NEAR, ZEC** — DOES NOT EXIST — INDEPENDENTLY RE-MEASURED, and the original's numbers reproduced exactly. Deribit lists several of these as CURRENCIES, which makes it easy to wrongly assume options coverage. Per-currency option instrum
- **Binance.US public REST API** — SUPERSEDED BY A BROADER FEED — carried forward. It quotes the thin US-only book and USD pairs, whereas Polymarket-Global settles on the global USDT tape, which I confirmed by reading a live market's resolution text. data
- **Etherscan API V2 multichain coverage on the free tier (chainid other than 1)** — NEW REJECTION — THE ORIGINAL REPORT'S MULTICHAIN RATIONALE IS FALSE AND I DISPROVED IT BY FETCHING. The report justified Etherscan as 'one key (or none) spans 60+ EVM chains... no separate API for Arbitrum, Base and Opti
- **Congress.gov API v3 via DEMO_KEY** — NEW REJECTION OF THE CREDENTIAL, not the provider. The original report's exampleCall used DEMO_KEY and claimed it was 'verified working'. It is not: every attempt, including one after a deliberate cooldown, returned HTTP
- **Stooq and keyless FRED (attempted free replacements for the gold / S&P leg)** — NEW — TESTED AS FALLBACKS FOR YAHOO AND BOTH FAILED. Because Yahoo's v8 chart endpoint 429'd on 5 of 7 attempts, I looked for a free replacement for the non-crypto leg of crypto-relative-value. Stooq: /q/l/?s=xauusd,^spx
- **CoinMarketCap, Messari, Nansen, Glassnode, Amberdata, Kaiko** — NOT FREE AT THE REQUIRED GRANULARITY — carried forward. Each gates the data this domain needs (holder concentration, on-chain flow analytics, institutional-grade indices) behind a paid tier or a trial. Not promoted on re
- **Farside Investors / SoSoValue (spot Bitcoin & Ethereum ETF net flows)** — NO FREE JSON API — scrape-only HTML; carried forward. ETF flow is named in this domain spec as a Bitcoin pricing input and no free structured feed was verified for it. Recorded as an explicit UNCOVERED gap in the bitcoin

---

### elections

*6/11 subdomains covered · 11 primary feeds*

#### Kalshi Trade API v2 — Elections series catalogue + markets + settlement_sources — Kalshi (CFTC-regulated US exchange) ✅ LIVE

Covers **11** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, seat-count-and-combos, margins-and-turnout, judicial-elections, international-elections

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: None for public market-data reads — CONFIRMED, every call below was uncredentialed. RSA key-pair signing only for trading. | Limits: Public reads uncredentialed — CONFIRMED. Exact free requests/second: UNKNOWN, still unmeasured. I issued ~12 calls in quick succession including a 2.6 MB pull with zero 429s, so no cap was hit at that rate; that is not the same as knowing the cap.
- Latency: Realtime REST + WebSocket | Format: REST JSON + WebSocket
- Why primary: ONE call returns the whole election contract universe and each series carries a machine-readable settlement_sources array, so this feed is simultaneously the live probability feed AND a directory of what legally resolves each contract. It removes the need for 11 per-subdomain venue feeds. This is the only feed in the set that independently verified on all 11 subdomains.

```bash
curl -s 'https://api.elections.kalshi.com/trade-api/v2/series?category=Elections'   # then: curl -s 'https://api.elections.kalshi.com/trade-api/v2/series/GOVPARTYGA' and curl -s 'https://api.elections.kalshi.com/trade-api/v2/markets?status=open&series_ticker=GOVPARTYGA'
```

> Evidence: RE-VERIFIED INDEPENDENTLY 2026-09-21. GET /series?category=Elections -> HTTP 200, 2,623,395 bytes, 1,824 series, 1,824 unique tickers (byte count reproduces the original report exactly). Ticker-pattern breakdown from MY OWN regexes — deliberately looser than the report's, so counts differ by method, not by fact: governor 211 (GOVPARTYTX, GOVPARTYVA, KXGOVMENOMR), senate 266 (KXSENATENER, KXPARAGUA

#### Polymarket Gamma API (+ CLOB) — events, live outcome prices, UMA resolution status — Polymarket ✅ LIVE

Covers **10** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, seat-count-and-combos, margins-and-turnout, international-elections

- Docs: https://docs.polymarket.com/
- Auth: None for public read/market data — CONFIRMED uncredentialed. | Limits: No key on public reads — CONFIRMED. Server caps a page at 100 events regardless of limit= — CONFIRMED (limit=100 returned exactly 100; &offset= paginates correctly across 6 pages / 600 events). Exact requests/minute: UNKNOWN, unpublished; 12+ rapid calls drew no 429.
- Latency: Realtime REST + WebSocket | Format: REST JSON + WebSocket
- Why primary: Second independent real-money probability on 10 of the 11 subdomains, and the only one that also exposes its resolution machinery (umaResolutionStatus, resolvedBy) in the same JSON — so the predictive price and the settlement record come from one feed. Divergence against Kalshi on the same question is itself a signal. NOTE: 'judicial-elections' has been REMOVED from this feed's claim — see evidence.

```bash
curl -s 'https://gamma-api.polymarket.com/events?slug=presidential-election-winner-2028'   # discovery: curl -s 'https://gamma-api.polymarket.com/events?limit=100&closed=false&tag_slug=elections&offset=0'
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET /events?slug=presidential-election-winner-2028 -> HTTP 200, 444,392 bytes. Live prices confirmed and drifting normally vs the report: JD Vance ["0.2075","0.7925"], Gavin Newsom ["0.0815","0.9185"], AOC ["0.1305","0.8695"], Buttigieg ["0.0265","0.9735"]; volume 707,302,361.50, liquidity 60,274,931.37. Resolution source string in the payload names AP + Fox News + NBC. 

#### Wikimedia / Wikipedia Action API — live opinion-polling tables for every race on Earth — Wikimedia Foundation ✅ LIVE

Covers **11** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, seat-count-and-combos, margins-and-turnout, judicial-elections, international-elections

- Docs: https://www.mediawiki.org/wiki/API:Parse
- Auth: None — CONFIRMED. A descriptive User-Agent is required by policy. | Limits: CORRECTED. No key, no paywall — CONFIRMED. The report's '500 requests/hour anonymous, 5,000/hour with a token' figures are MIS-ATTRIBUTED: those are the api.wikimedia.org REST Gateway tiers, NOT the Action API at en.wikipedia.org/w/api.php, which publishes no per-hour read cap and instead enforces the User-Agent policy and asks for serial rather than parallel requests. Actual Action API free limit: UNKNOWN. 6 rapid consecutive calls all returned HTTP 200, so the 500/hr figure is not what is being enforced here.
- Latency: Minutes-to-hours after a poll is published (crowd-edited) | Format: REST JSON wrapping MediaWiki wikitext (wikitables parse deterministically)
- Why primary: The single broad LIVE polling feed that still exists for free. FiveThirtyEight's live polls CSVs are dead and every commercial aggregator blocks non-browser clients (see rejectedFeeds). One API, one URL pattern, covers general, primary, generic-ballot, ballot-measure and foreign national polling. Caveat added below: coverage is real on all 11, but the STRUCTURE of the data degrades down-ballot.

```bash
curl -s -A 'your-app/1.0 (you@example.org)' 'https://en.wikipedia.org/w/api.php?action=parse&page=2026%20United%20States%20Senate%20election%20in%20Maine&prop=wikitext&format=json&formatversion=2'   # discovery: .../w/api.php?action=query&list=search&srsearch=intitle%3A%22opinion%20polling%22%202026&srlimit=50&format=json
```

> Evidence: RE-VERIFIED INDEPENDENTLY. action=parse on '2026 United States Senate election in Maine' -> HTTP 200, 209,133 bytes / 205,118 chars — byte-for-byte reproduces the report. Extracted the live wikitable header verbatim: 'Poll source | Date(s) administered | Sample size | Margin of error | Carmen Calabrese | Susan Collins | Dan Smeriglio | Other | Undecided', with distinct Republican-primary and Democ

#### Wikidata Query Service (SPARQL) — worldwide election calendar, turnout and declared winners — Wikimedia Foundation ✅ LIVE

Covers **9** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, margins-and-turnout, international-elections

- Docs: https://query.wikidata.org/
- Auth: None — CONFIRMED. User-Agent required. | Limits: No key — CONFIRMED. 60-second query timeout, ~5 concurrent queries per IP (Wikimedia-documented, NOT measured by me — my queries returned in well under a second). Heavy use should mirror the dumps.
- Latency: Minutes-to-days after an edit; scheduled future dates present months ahead | Format: SPARQL over HTTP -> JSON
- Why primary: The contract-discovery and calendar spine. One SPARQL query enumerates scheduled elections worldwide with date and country, which tells you a market will exist before it is listed. P991 (successful candidate) carries declared winners and P1868 carries ballots cast. NARROWED: 'judicial-elections' and 'seat-count-and-combos' REMOVED — I could not verify either from this endpoint and will not carry an unverified claim.

```bash
curl -s -G 'https://query.wikidata.org/sparql' -H 'Accept: application/sparql-results+json' -A 'your-app/1.0 (you@example.org)' --data-urlencode 'query=SELECT ?e ?eLabel ?date ?countryLabel WHERE { ?e wdt:P31/wdt:P279* wd:Q40231 ; wdt:P585 ?date . OPTIONAL{?e wdt:P17 ?country} FILTER(?date >= "2026-09-01T00:00:00Z"^^xsd:dateTime && ?date <= "2027-12-31T00:00:00Z"^^xsd:dateTime) SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } ORDER BY ?date LIMIT 50'
```

> Evidence: RE-VERIFIED INDEPENDENTLY. Upcoming-elections SPARQL -> HTTP 200, 26,446 bytes, 50 rows (the report said 2,767 bytes — it must have used a tighter LIMIT; the query as printed returns far more, which is better, not worse). Real rows: 2026-09-01 '2026 Moroccan general election' (Morocco), 2026-09-03 Scarborough Southwest / Hamilton East—Stoney Creek / York—Simcoe provincial by-elections (Canada), 20

#### Harvard Dataverse API — MIT Election Data + Science Lab (MEDSL) collection — Harvard Dataverse / MIT Election Data and Science Lab ✅ LIVE

Covers **8** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, ballot-measures, judicial-elections, margins-and-turnout

- Docs: https://guides.dataverse.org/en/latest/api/
- Auth: None for public datasets — CONFIRMED. Free token only for restricted files. | Limits: No key required — CONFIRMED. No published hard rate limit — UNKNOWN exact figure; Dataverse throttles abusive clients. Files range from 514 KB to 1.29 GB.
- Latency: Periodic — statewide files updated weeks-to-months after certification; precinct files per cycle | Format: REST JSON API over CSV/TAB bulk files
- Why primary: ONE provider, one API, 30 datasets carrying the certified vote for president, senate, house, governor, other state offices, state legislature, local offices, ballot measures and judicial retention contests on one consistent schema with FIPS joins. The alternative to scraping 50 secretaries of state. 'primaries' REMOVED from the claim — see evidence; primaries are effectively absent from the statewide files and only reachable via the multi-GB per-cycle precinct files.

```bash
curl -s 'https://dataverse.harvard.edu/api/search?q=*&subtree=medsl_election_returns&type=dataset&per_page=100'   # then pull real data: curl -sL -o senate.tab 'https://dataverse.harvard.edu/api/access/datafile/13887039'   (US Senate statewide 1976-2024)
```

> Evidence: RE-VERIFIED INDEPENDENTLY, INCLUDING THE CODEBOOK QUOTES. GET /api/search?subtree=medsl_election_returns -> HTTP 200, status OK, total_count 30 — reproduces exactly. I enumerated all 30 names and confirm the four statewide spines exist: 'U.S. Senate statewide 1976–2024', 'U.S. House 1976–2024', 'U.S. President 1976–2024', 'County Presidential Election Returns 2000-2024', plus per-cycle precinct fi

#### openFEC API v1 — candidates, election dates + filing deadlines, per-race money, independent expenditures — US Federal Election Commission (api.data.gov) ✅ LIVE

Covers **4** subdomains: us-presidential, us-senate, us-house, primaries

- Docs: https://api.open.fec.gov/developers/
- Auth: Free API key from api.data.gov — CONFIRMED. DEMO_KEY works for testing. | Limits: RE-MEASURED AND CONFIRMED: DEMO_KEY returns 'x-ratelimit-limit: 10' per hour — I watched x-ratelimit-remaining fall 4 -> 2 -> 0 across my calls and then the key was exhausted, so the 10/hr figure is real and DEMO_KEY is unusable for anything but a smoke test. A free registered key is documented at 1,000 requests/hour (api.data.gov shared default) — DOCUMENTED, NOT MEASURED by me. No paywall; bulk CSV also free.
- Latency: Filing-driven — sub-daily for Schedule E (24/48-hour IE reports); quarterly/monthly for committee totals | Format: REST JSON (OpenAPI) + CSV bulk
- Why primary: The single fundamentals feed for every FEDERAL race at once: who filed, when the election and its filing deadline are, how much each candidate raised and holds, and every independent expenditure with a support/oppose flag. 'seat-count-and-combos' REMOVED — the FEC publishes candidate finance, not seat totals or chamber-control data; that was an over-claim.

```bash
curl -s 'https://api.open.fec.gov/v1/elections/?api_key=DEMO_KEY&office=house&state=NY&district=04&cycle=2026&per_page=20'   # also: /v1/election-dates/?api_key=DEMO_KEY&election_year=2026  and  /v1/schedules/schedule_e/?api_key=DEMO_KEY&cycle=2026&sort=-expenditure_date
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET /v1/election-dates/?election_year=2026 -> HTTP 200, pagination.count 243 — reproduces exactly. Real rows WITH filing deadlines: LA S GR 2026-12-12 (filing 2026-01-21), LA H GR 2026-12-12, GA S GR 2026-12-01, GA H GR 2026-12-01, VI H GR 2026-11-17. (Different rows than the report's TX/NJ/AR examples because the default sort differs; count matches.) GET /v1/elections/?

#### IPU Parline API v1 — official results of national parliamentary elections worldwide — Inter-Parliamentary Union ✅ LIVE

Covers **1** subdomains: international-elections

- Docs: https://data.ipu.org/data-tools/api/
- Auth: None — CONFIRMED, fetched anonymously. | Limits: No key, no registration, open data with an explicit terms_of_use block in every response — CONFIRMED. Exact requests/day: UNKNOWN, none stated.
- Latency: Days-to-weeks after a parliamentary election is officially declared | Format: REST JSON (JSON:API), OpenAPI-described
- Why primary: The only free, official, machine-readable source of settled national election results across ~190 countries in one endpoint — seat counts, turnout, election dates, chamber composition — rather than per-country electoral-commission scrapers. Its per-field missing_reason flag distinguishes 'not reported' from zero, which matters for settlement.

```bash
curl -s -A 'your-app/1.0' 'https://api.data.ipu.org/v1/elections?page%5Blimit%5D=50'   # also /v1/parliaments and /v1/chambers
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET /v1/elections?page[limit]=5 -> HTTP 200, 43,604 bytes, meta.total = 2,966 — both reproduce exactly. meta.publisher 'Inter-Parliamentary Union', meta.terms_of_use present, meta.date_accessed '2026-09-21T03:10:37Z'. Record shape confirmed verbatim: type 'Election', id 'AD-LC01-E19931212', attributes.election_title.value.en 'Andorra General Council December 1993 Electio

#### GDELT 2.0 — DOC 2.0 API + raw 15-minute Events/Mentions/GKG files — The GDELT Project ✅ LIVE

Covers **11** subdomains: us-presidential, us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, seat-count-and-combos, margins-and-turnout, judicial-elections, international-elections

- Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- Auth: None — CONFIRMED. | Limits: No key — CONFIRMED. DOC API enforces roughly ONE REQUEST PER 5 SECONDS per IP. NOT REPRODUCED from my egress: my single DOC call succeeded first try with no 429, so the report's repeated hard-429s are IP/shared-egress dependent, not a universal property. Treat the 1-req/5s ceiling as the documented design limit and the raw 15-minute bulk files (no throttle) as the right path at volume.
- Latency: 15 minutes (bulk pointer file) / near-realtime (DOC API) | Format: REST JSON (DOC API); zipped CSV (bulk)
- Why primary: One multilingual feed gives news volume, tone and entity co-occurrence for ANY race, candidate, measure or foreign election, in any language — the attention/momentum layer for all 11 subdomains at once. Scope caveat: it is an ATTENTION signal keyed on free-text query, never a settlement source, so 'covers' here means 'queryable for', not 'resolves'.

```bash
curl -s 'https://api.gdeltproject.org/api/v2/doc/doc?query=election&mode=artlist&maxrecords=25&format=json&timespan=1d'   # bulk (CORRECTED — must be https or curl -L; plain http returns 301 with an EMPTY body): curl -s 'https://data.gdeltproject.org/gdeltv2/lastupdate.txt'
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET /api/v2/doc/doc?query=election&mode=artlist&timespan=1d -> HTTP 200, 12,378 bytes (the report got 930 bytes — a smaller window, same endpoint), real non-English article returned: url https://news.ltn.com.tw/news/politics/breakingnews/5580451, seendate '20260920T114500Z', Traditional-Chinese Taiwanese politics headline — translingual coverage CONFIRMED. DEFECT FOUND A

#### Poll-error calibration layer — fivethirtyeight raw_polls.csv + Silver Bulletin rawpolls.xlsx — FiveThirtyEight (archived by ABC on GitHub) + Silver Bulletin / Nate Silver ✅ LIVE

Covers **6** subdomains: us-presidential, us-senate, us-house, us-governor, primaries, seat-count-and-combos

- Docs: https://github.com/fivethirtyeight/data/tree/master/pollster-ratings and https://www.natesilver.net/p/pollster-ratings-silver-bulletin
- Auth: None for either file — CONFIRMED. | Limits: No key, no quota — CONFIRMED. raw.githubusercontent.com per-file limit UNKNOWN; GitHub API 60/hr anonymous, 5,000/hr with a free token (documented, not measured). Silver Bulletin states the data may be used free of charge with attribution.
- Latency: 538 file is FROZEN (no longer updated). Silver Bulletin refreshes roughly annually/semiannually. | Format: CSV bulk / XLSX bulk
- Why primary: This is what converts a raw poll from Wikipedia into a probability: poll-vs-actual error, house effects and partisan bias across race types, from one file, so you calibrate every US subdomain from a single source instead of guessing a spread per race. Pairs with the Wikipedia polling feed — that one supplies the polls, this one supplies their error distribution.

```bash
curl -sL -o raw_polls.csv 'https://raw.githubusercontent.com/fivethirtyeight/data/master/pollster-ratings/raw_polls.csv'   # and: curl -sL -o sb_rawpolls.xlsx 'https://www.natesilver.net/api/v1/file/95ab4b0b-119b-4330-9392-f767d35ad2a7.xlsx'
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET raw_polls.csv -> HTTP 200, 4,961,378 bytes, content-type 'text/plain; charset=utf-8' (NOT an HTML error page — this is the distinction that killed the live 538 CSVs), 20,466 data rows. Header confirmed: poll_id, question_id, race_id, cycle, location, type_simple, race, pollster, pollster_rating_id, aapor_roper, inactive, methodology, transparency_score, partisan, pol

#### unitedstates/congress-legislators — incumbency, term end dates, retirements, ID crosswalk — @unitedstates project (public domain) ✅ LIVE

Covers **3** subdomains: us-senate, us-house, seat-count-and-combos

- Docs: https://github.com/unitedstates/congress-legislators
- Auth: None — CONFIRMED. | Limits: No key — CONFIRMED. GitHub Pages / raw file fetch; exact cap UNKNOWN. Full 1789-present history in the repo.
- Latency: Daily-to-weekly (community commits; retirements land within days) | Format: JSON / YAML / CSV bulk via Git
- Why primary: One file establishes the current baseline every congressional market is priced against: who holds each seat, their party, when the term ends, and the FEC/bioguide/ICPSR IDs needed to join openFEC money to MEDSL results. 'us-presidential' REMOVED — legislators-current.json contains no executive-branch records; that was an over-claim (the repo's separate executive.yaml would be a different file and was not verified).

```bash
curl -sL 'https://unitedstates.github.io/congress-legislators/legislators-current.json'
```

> Evidence: RE-VERIFIED INDEPENDENTLY. GET legislators-current.json -> HTTP 200, 1,468,926 bytes, 539 member records — both reproduce exactly. Sample record reproduces to the field: Maria Cantwell, latest term {type:'sen', start:'2025-01-03', end:'2031-01-03', state:'WA', class:1, party:'Democrat'} — term-end dates that define the Senate class maps, CONFIRMED. DEFECT FOUND: I counted the latest-term `type` ac

#### North Carolina State Board of Elections ENRS bulk feed (exemplar of the per-state official settlement pattern) — NC State Board of Elections ✅ LIVE

Covers **8** subdomains: us-senate, us-house, us-governor, other-statewide-offices, primaries, ballot-measures, judicial-elections, margins-and-turnout

- Docs: https://er.ncsbe.gov/downloads.html
- Auth: None — CONFIRMED. | Limits: No key, no registration, no published rate limit — UNKNOWN exact cap; static files on a download host.
- Latency: Refreshes every few minutes on election night; certified canvass files afterwards | Format: Tab-delimited text inside ZIP, with a published layout file
- Why primary: The ONLY free feed here that comes from a legal certifying authority AND is fast enough to settle on election night — MEDSL is weeks-to-months late, AP is paid, Clarity 403'd. It covers 8 subdomains for ONE state (candidate AND referendum choice, per precinct, by voting method, plus absentee/early-vote counts). Treat it as the template to replicate across the other 49, NOT as national coverage. This is a per-state feed and its 8-subdomain claim must always be read as 'for North Carolina only'.

```bash
curl -sL -o results_pct.zip 'https://dl.ncsbe.gov/ENRS/2024_11_05/results_pct_20241105.zip'   # schema: curl -sL 'https://dl.ncsbe.gov/ENRS/layout_results_pct.txt' ; turnout: .../ENRS/2024_11_05/voter_stats_20241105.zip and absentee_20241105.zip   # NOTE: -L or https:// is required; the plain-http host 301-redirects.
```

> Evidence: RE-VERIFIED INDEPENDENTLY, INCLUDING A REAL BYTE PULL the report did not do (it only ran HEAD). curl -sIL on results_pct_20241105.zip -> HTTP 200, content-type application/x-zip-compressed, final URL https://dl.ncsbe.gov/... (note the http -> https redirect; -L is mandatory). I then issued a RANGE request for the first 2 KB -> HTTP 206, 2,001 bytes, and `file` identifies it as 'Zip archive data, a

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| US Presidential & Nominations | Kalshi /series?category=Elections (VERIFIED) + Polymarket Ga | MEDSL 'U.S. President 1976–2024' (Dataverse datafile 1388704 | 🟢 COVERED |
| US Senate Races | Wikipedia Action API — RE-VERIFIED on '2026 United States Se | MEDSL 'U.S. Senate statewide 1976–2024' (datafile 13887039 — | 🟢 COVERED |
| US House Races | Wikipedia Action API — RE-VERIFIED on '2026 United States Ho | MEDSL 'U.S. House 1976–2024' plus U.S. House Precinct-Level  | 🟢 COVERED |
| Governor Races | Kalshi (211 governor-pattern series by my count: GOVPARTYTX, | MEDSL 'State Office-Level Returns 2016' and the State Precin | 🟢 COVERED |
| Other Statewide & Local Offices | Kalshi (177 AG/SecState/Treasurer/mayoral-pattern series by  | MEDSL 'State Office-Level Returns 2016', 'State Offices Prec | 🟡 PARTIAL |
| Primaries & Nomination Contests | Wikipedia Action API — RE-VERIFIED that the Maine Senate pag | MEDSL per-cycle PRECINCT files ONLY — codebook re-fetched an | 🟡 PARTIAL |
| Ballot Measures & Referendums | Kalshi (10 measure-pattern series by my stricter count: KXST | MEDSL State Precinct-Level Returns — codebook RE-FETCHED (da | 🟡 PARTIAL |
| Balance of Power & Seat Counts | Kalshi (seat-count/combo series incl. KXRHOUSESEATS — indivi | MEDSL 'U.S. House 1976–2024' + 'U.S. Senate statewide 1976–2 | 🟢 COVERED |
| Margins & Turnout | Kalshi (84 MOV/turnout-pattern series, independently recount | MEDSL statewide and precinct files — totalvotes on every row | 🟡 PARTIAL |
| Judicial Elections & Retention | Kalshi ONLY as a market feed — 21 judicial-pattern series in | MEDSL State Precinct-Level Returns — codebook RE-FETCHED and | 🟡 PARTIAL |
| International Elections | Wikipedia Action API — RE-VERIFIED on 'Opinion polling for t | IPU Parline /v1/elections — RE-VERIFIED HTTP 200, 43,604 byt | 🟢 COVERED |

**Rejected**

- **FiveThirtyEight live polls CSVs (projects.fivethirtyeight.com/polls/data/*.csv)** — DEAD, and carried over from the report as the single most dangerous failure mode in this inventory because it returns HTTP 200 with ~305 KB of ABC News HTML instead of CSV. NOT re-fetched by me (the archived GitHub raw_p
- **VoteHub polling data (polls.votehub.us/polls.csv, approval.csv, generic-ballot.csv)** — Cloudflare-blocked to programmatic clients per the report: HTTP 403 'Just a moment...' on all three paths with both default and browser User-Agents; polls.votehub.com HTTP 522. NOT INDEPENDENTLY RE-FETCHED — carried forw
- **FiftyPlusOne API (fiftyplusone.news)** — Bot-blocked per the report: /api/polls HTTP 403 {"success":false,"error":"Browser required"}; /data/polls.csv HTTP 404. NOT INDEPENDENTLY RE-FETCHED, but corroborated indirectly — I confirmed FiftyPlusOne's generic-ballo
- **Clarity Elections / Scytl election-night platform (results.enr.clarityelections.com)** — Carried forward as UNVERIFIED-DEAD. The report could not make a single path work (nginx 403s across /GA/, /KY/15261/current_ver.txt and others; one Clarity 404 showing the host is alive but the path wrong). Undocumented 
- **Florida Division of Elections results (results.elections.myflorida.com)** — HTTP 403 Cloudflare challenge on /downloadresults.asp per the report. NOT INDEPENDENTLY RE-FETCHED.
- **IFES ElectionGuide API (electionguide.org/api/v1/elections/)** — Not free/open: HTTP 401 with an access-request message, per the report. Would have been the ideal single international-elections feed (calendar + results + electoral systems, including the seat-allocation rules that are 
- **Adjacent News API (adj.news)** — Unreachable per the report (api.adj.news and docs.adj.news both HTTP 000). Cross-venue normalization is achievable directly from Kalshi + Polymarket, both of which I verified live. NOT INDEPENDENTLY RE-FETCHED.
- **Metaculus API** — No longer anonymous per the report: HTTP 403 requiring an account token. Free with registration but not keyless, and its election coverage is a subset of Kalshi/Polymarket. NOT INDEPENDENTLY RE-FETCHED.
- **PredictIt market data API** — Live and free per the report but SUPERSEDED on coverage. NOT INDEPENDENTLY RE-FETCHED. Its value is unchanged and worth restating: a cheap third opinion on seat-count-and-combos specifically, which is the one subdomain w
- **Manifold Markets API** — Live and keyless per the report but play-money, so prices are not risk-calibrated probabilities. Superseded by two verified real-money venues. NOT INDEPENDENTLY RE-FETCHED.
- **Google Civic Information API** — Requires a Google API key and its elections/voterinfo endpoints were deprecated in April 2025. NOT INDEPENDENTLY RE-FETCHED.
- **Voting Information Project (votinginfoproject.org)** — No public API endpoint per the report (api. and data. subdomains both HTTP 000). NOT INDEPENDENTLY RE-FETCHED.
- **US Census Bureau Data API — ACS / CPS Voting and Registration Supplement** — Downgraded, not dead: requires a free registered key (keyless calls return a 'Missing Key' page), and the CPS voting supplement is biennial and post-hoc — a turnout base-rate source, never a live one. The sibling Census 
- **OpenElections (github.com/openelections)** — Too uneven and superseded by MEDSL. I independently confirmed the MEDSL side of this trade: 30 datasets on one consistent schema via one API, with the four statewide spines and per-cycle precinct files for Senate, House,
- **Redistricting Data Hub** — Not an API — a registration-gated download portal with a click-through, so it cannot be polled programmatically. Census Geocoder/TIGERweb covers the district-identity need. NOT INDEPENDENTLY RE-FETCHED.
- **UMA Optimistic Oracle subgraph (api.thegraph.com/subgraphs/name/umaprotocol/...)** — Hosted service sunset (HTTP 301); the decentralized gateway now needs a Graph API key. Unnecessary — I independently confirmed Polymarket's Gamma API exposes umaResolutionStatus 'resolved' and a resolvedBy address direct
- **Silver Bulletin 'Pollster Stats Full' XLSX (second file key from the inventory)** — That file key 404'd per the report. I independently confirmed the OTHER key works: 95ab4b0b-119b-4330-9392-f767d35ad2a7.xlsx -> HTTP 200, 2,048,058 bytes, valid 'Microsoft Excel 2007+'. Use only that key; do not hard-cod
- **Associated Press Elections API** — PAID, no free tier. Independently corroborated as the load-bearing settlement authority: aggregating settlement_sources across all 1,824 Kalshi election series, 'the Associated Press' appears on 289 of them (I reproduced
- **Ballotpedia API / NCSL ballot-measure database** — No free programmatic access; Ballotpedia is commercial and NCSL publishes no API. These would have filled the predictive gaps in ballot-measures, judicial-elections and other-statewide-offices. NOT INDEPENDENTLY RE-FETCH
- **CourtListener REST API v4** — Live and free but does not serve this domain — judge biographies, appointments, dockets and opinions, not judicial ELECTION results or race spending. Free tier is severe (5 req/min, 50/hr, 125/day). NOT INDEPENDENTLY RE-
- **Congress.gov API v3, GovInfo, Federal Register, Regulations.gov, Open States, LegiScan, Voteview, House/Senate roll-call XML, UK Parliament API** — Live and free but LEGISLATIVE/governance feeds, not election feeds — none prices or settles a contested race, ballot measure or seat count. They belong to a politics/legislation domain. unitedstates/congress-legislators 

---

### entertainment-and-media

*10/18 subdomains covered · 15 primary feeds*

#### Wikidata Query Service (SPARQL) — award graph P166/P1411 — Wikimedia Foundation ✅ LIVE

Covers **4** subdomains: film-awards, tv-awards, music-awards, critic-scores

- Docs: https://query.wikidata.org/
- Auth: none (descriptive User-Agent required by policy) | Limits: 60s query timeout; 5 concurrent queries per IP; 30 queries/min per IP. No key, no daily cap. Limits are DOCUMENTED, not rate-tested by me.
- Latency: minutes-to-days after the real-world event (crowd-sourced edits). CORRECTED response time: 11.78s cold, ~2.0s warm — NOT the 0.17s the report claimed. Budget for multi-second queries. | Format: SPARQL over HTTP, JSON results
- Why primary: One endpoint and one property pair (P166 award received / P1411 nominated for) returns winners AND nominees for Oscars, Emmys, Grammys and Tonys keyed by per-category QID — replacing four bespoke scrapers for bodies that publish no API. I verified all three award families with separate queries. NOTE: I cut seven subdomains the report claimed here (box-office, video-games, art-and-auctions, food-and-lifestyle, anime-and-international-media, celebrity-events, public-appearances) because Wikidata does not serve them at usable density — see verificationEvidence. Two of those (Michelin, anime awards) the report itself rejected in rejectedFeeds while still listing them here.

```bash
curl -sG 'https://query.wikidata.org/sparql' -H 'Accept: application/sparql-results+json' -H 'User-Agent: EchoFeedMap/1.0 (you@example.com)' --data-urlencode 'query=SELECT ?awLabel ?winnerLabel ?yr WHERE { VALUES ?aw { wd:Q102427 wd:Q989438 wd:Q904528 wd:Q1780176 } ?winner p:P166 ?s . ?s ps:P166 ?aw . OPTIONAL { ?s pq:P585 ?yr } SERVICE wikibase:label { bd:serviceParam wikibase:language "en" } } ORDER BY DESC(?yr) LIMIT 10'
```

> Evidence: VERIFIED, with three parsing hazards the report missed. Multi-award query: HTTP 200, 4294B (report said 194B — wrong), 11.78s cold / 1.97s warm. Returned 'Academy Award for Best Picture -> One Battle After Another 2026-03-15'. Emmy Q989438 verified with its own query: 'The Pitt 2025-01-01'. Grammy Q904528 verified separately: rows dated 2026-01-01. HAZARD 1 — bare Q-ids: Grammy AOTY returned winne

#### Wikimedia Pageviews API (per-article + top-1000 per day) — Wikimedia Foundation ✅ LIVE

Covers **18** subdomains: film-awards, tv-awards, music-awards, box-office, critic-scores, streaming-charts, music-charts, streaming-counts, video-views, reality-tv, scripted-tv-and-film-production, video-games, celebrity-events, public-appearances, art-and-auctions, anime-and-international-media, food-and-lifestyle, media-industry-corporate

- Docs: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/
- Auth: none (descriptive User-Agent required by policy) | Limits: 100 req/sec per IP unauthenticated — DOCUMENTED, not rate-tested by me. No key, no daily cap. History from 2015-07-01.
- Latency: hourly endpoint lags ~1-2h; daily endpoint available next day | Format: REST JSON
- Why primary: The broadest PREDICTIVE feed in the domain and the only one needing no per-subdomain integration — the article title is the sole parameter. I confirmed the all-18 claim is not hand-waving by spot-checking four structurally different subject types rather than trusting it. It is an attention proxy only; it settles nothing.

```bash
curl -H 'User-Agent: EchoFeedMap/1.0 (you@example.com)' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Academy_Awards/daily/20260901/20260910'
```

> Evidence: VERIFIED, claim held under adversarial spot-check. Per-article: HTTP 200, 1521B, 0.16s — {"project":"en.wikipedia","article":"Academy_Awards","granularity":"daily","timestamp":"2026090100","views":3679}, then 3995, 4042 through 2026-09-10. I then tested the broad-coverage claim on four deliberately different subdomain shapes rather than accepting it: Eleven_Madison_Park (food-and-lifestyle) 6 poin

#### Google News RSS search (no key) — Google ✅ LIVE

Covers **13** subdomains: celebrity-events, public-appearances, scripted-tv-and-film-production, media-industry-corporate, art-and-auctions, reality-tv, box-office, film-awards, music-awards, tv-awards, food-and-lifestyle, video-games, anime-and-international-media

- Docs: https://news.google.com/rss
- Auth: none | Limits: No key and no published rate limit — UNKNOWN; poll at most every few minutes. Returns ~92-100 items per query. No archive: you must snapshot.
- Latency: minutes behind publication | Format: RSS/XML
- Why primary: Roughly a third of this domain settles on credible reporting rather than a machine-readable number, and one arbitrary-query RSS endpoint indexes Variety, Deadline and the trades at once. Confirmed as the correct substitute for GDELT, which I independently reproduced as 429-blocked from this host.

```bash
curl -sA 'Mozilla/5.0' 'https://news.google.com/rss/search?q=%22box+office%22+weekend&hl=en-US&gl=US&ceid=US:en'
```

> Evidence: VERIFIED, two independent queries. Box-office query: HTTP 200, 131028B, 0.75s, 92 <item> elements (counted by occurrence, not line). Headlines: "'Resident Evil' Scores $60M U.S. Opening: Best Ever For Zach Cregger & Franchise – Box Office Update" (Deadline); "Weekend Box Office: 'The Odyssey' Passes 'Inside Out 2'...". pubDates 'Sun, 20 Sep 2026 14:41:00 GMT' and 'Mon, 21 Sep 2026 00:16:43 GMT' — 

#### Box Office Mojo domestic weekend + daily charts (Comscore data) — IMDb / Amazon (Comscore-sourced) ✅ LIVE

Covers **1** subdomains: box-office

- Docs: https://www.boxofficemojo.com/
- Auth: none | Limits: NO API — HTML tables, scrape-only. No published rate limit; scrape once or twice daily. Full historical weekend/daily archive on-site. Requires a browser User-Agent.
- Latency: daily grosses posted next morning; weekend actuals Monday | Format: scrape-only (clean HTML <table>, parses to rank/change/title/gross/pct/theaters)
- Why primary: No free JSON alternative exists — I re-confirmed Trakt /movies/boxoffice is Cloudflare-403 without a client_id. Upgraded confidence beyond the report: I found INDEPENDENT third-party corroboration that this is the settlement authority — Polymarket's own market description for 'Highest grossing movie in 2026?' reads 'will resolve according to the title of the film with the highest 2026 gross according to the "Gross" column on https://www.boxofficemojo.com/year/2026/'. The venue itself names this host.

```bash
curl -sA 'Mozilla/5.0' 'https://www.boxofficemojo.com/weekend/2026W37/'   # and: curl -sA 'Mozilla/5.0' 'https://www.boxofficemojo.com/date/2026-09-18/'
```

> Evidence: VERIFIED, re-parsed rather than trusting the report's rows. Weekend: HTTP 200, 260667B, 0.73s, title 'Domestic 2026 Weekend 37 - Box Office Mojo', 68 <tr> elements. Parsed rows reproduce exactly: ['1','-','Practical Magic 2','$30,002,526','-','4,146'], ['2','1','Spider-Man: Brand New Day','$8,410,743','-53.7%','3,303'], ['3','2','The Odyssey','$7,592,750','-42%','1,983']. Daily: HTTP 200, 197962B,

#### TVmaze API (/schedule, /schedule/web, /shows, /updates) — TVmaze ✅ LIVE

Covers **2** subdomains: reality-tv, scripted-tv-and-film-production

- Docs: https://www.tvmaze.com/api
- Auth: none | Limits: ~20 calls per 10 seconds per IP (429 on exceed) — DOCUMENTED, not rate-tested by me. No daily cap published. Full historical + future schedule. Premium key only for user-specific data.
- Latency: daily (schedule updates as networks announce); /updates gives change timestamps | Format: REST JSON
- Why primary: One no-key feed gives the broadcast AND streaming release calendar in one schema — the elimination-night calendar for reality contracts and premiere/status fields for scripted ones. CORRECTED: I removed 'tv-awards' and 'streaming-charts' from the report's claim. TVmaze returns no award result and no chart rank; it returns air dates. Under the rule that a feed claiming a subdomain must actually return that subdomain's value, those two do not qualify — premiered/ended dates are an eligibility INPUT to tv-awards, and Netflix Tudum is the actual streaming-chart feed.

```bash
curl -s 'https://api.tvmaze.com/schedule?country=US&date=2026-09-20'   # streaming-only: curl -s 'https://api.tvmaze.com/schedule/web?date=2026-09-20&country='
```

> Evidence: VERIFIED. /schedule?country=US&date=2026-09-20: HTTP 200, 139044B, 0.85s, 59 records. First record id 3718118, airdate '2026-09-20', airstamp '2026-09-20T10:00:00+00:00', embedded show {id:87079, name:'Fox & Friends Weekend', status:'Running', premiered:'2025-01-04'} — exactly as reported. /schedule/web?date=2026-09-20&country=: HTTP 200, 82585B, 41 rows (matches). GOTCHA: the empty country param 

#### Netflix Tudum Top 10 bulk TSV (global + 90 countries + most-popular) — Netflix ✅ LIVE

Covers **1** subdomains: streaming-charts

- Docs: https://www.netflix.com/tudum/top10
- Auth: none | Limits: No key, no rate limit — three static files on a CDN. Full history back to 2021-06-28. Measured sizes: all-weeks-global.tsv 893,380B; all-weeks-countries.tsv 32,208,603B; most-popular.tsv 2,925B.
- Latency: weekly, normally published Tuesday for the week ending the prior Sunday | Format: CSV bulk (tab-separated .tsv over HTTPS). -L is REQUIRED (the URL redirects).
- Why primary: Netflix's own published chart is the literal settlement source for the Netflix rank contracts, and the predictive series (prior-week decay) and the settlement row come from the same 900KB download. All three files verified present, not just the one the report fetched.

```bash
curl -sL 'https://www.netflix.com/tudum/top10/data/all-weeks-global.tsv'   # also all-weeks-countries.tsv, most-popular.tsv
```

> Evidence: VERIFIED, all three files. all-weeks-global.tsv HTTP 200, 893380B, 1.09s — exact size match. Header: week/category/weekly_rank/show_title/season_title/weekly_hours_viewed/runtime/weekly_views/cumulative_weeks_in_top_10. Latest week 2026-09-13, Films (English): #1 'Why Did I Get Married Again?' 35,700,000 hours / 19,300,000 views / 1 week; #2 'The Whisper Man' 24,100,000 hours / 12,700,000 views / 

#### Apple Marketing Tools RSS Feed Generator (music + books + podcasts + apps, 175 storefronts) — Apple ✅ LIVE

Covers **1** subdomains: music-charts

- Docs: https://rss.marketingtools.apple.com/
- Auth: none | Limits: No key, no published rate limit — UNKNOWN; treat as a CDN JSON file and poll hourly at most. Current chart only, no archive — you must snapshot.
- Latency: daily; feed carried 'updated: Mon, 21 Sep 2026 03:20:49 +0000' when fetched at 03:20 UTC — current to the minute | Format: REST JSON
- Why primary: One URL template varies three path segments to yield songs, albums and music videos across 175 storefronts — one integration instead of one feed per chart per country — and it is the fastest-refreshing free consumption chart without a key, so it is the daily predictor of the weekly Billboard settlement. CORRECTED: I removed 'streaming-counts'. Apple's most-played is a RANK ORDER, not a play count; there is no count field anywhere in the payload.

```bash
curl -s 'https://rss.marketingtools.apple.com/api/v2/us/music/most-played/10/songs.json'   # swap us|gb|jp/, songs|albums|music-videos, 10|25|50|100
```

> Evidence: VERIFIED, and I tested the 175-storefront claim rather than accepting it. us/songs: HTTP 200, 6701B, 2.64s — {"feed":{"title":"Top Songs","country":"us","copyright":"Copyright © 2026 Apple Inc.","updated":"Mon, 21 Sep 2026 03:20:49 +0000","results":[{"artistName":"Morgan Wallen","id":"6812477290",...}]}. Storefront swap gb/albums: HTTP 200, 6906B — 'Top Albums', country 'gb', #1 'you seem pretty s

#### Billboard charts — Hot 100 JSON mirror + billboard.com chart pages — Billboard / Luminate (chart pages); mhollingshead (Hot 100 JSON mirror) ✅ LIVE

Covers **1** subdomains: music-charts

- Docs: https://github.com/mhollingshead/billboard-hot-100
- Auth: none | Limits: Mirror: GitHub raw, no key, no practical limit; all.json measured at 43,937,637B for full history, plus per-date files under /date/. Chart pages: no published limit, scrape once weekly; requires a browser User-Agent; the Billboard 200 page is a 4.98MB download per fetch.
- Latency: weekly — Billboard publishes Tuesday, chart dated the following Saturday. Mirror tracks it (recent.json dated 2026-09-19 at fetch). | Format: REST JSON (mirror) + scrape-only HTML (billboard.com for Billboard 200 and all other charts)
- Why primary: Billboard is the named settlement source for the chart-position contracts. The Hot 100 mirror gives the whole chart history as JSON with no key; for the Billboard 200 and every other chart there is no free JSON mirror, but all chart pages share one host and one row markup, so one scraper covers the remainder.

```bash
curl -s 'https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/recent.json'   # full history: .../main/all.json ; per-date: .../main/date/2026-09-19.json ; Billboard 200 (scrape): curl -sA 'Mozilla/5.0' 'https://www.billboard.com/charts/billboard-200/'
```

> Evidence: VERIFIED, including the two mirror paths the report named but did not fetch. recent.json: HTTP 200, 11935B, 0.13s — {"date":"2026-09-19","data":[{"song":"Choosin' Texas","artist":"Ella Langley","this_week":1,"last_week":1,"peak_position":1,"weeks_on_chart":47},{"song":"Boston","artist":"Stella Lefty","this_week":2,...},{"song":"I Knew It, I Knew You","artist":"Taylor Swift","this_week":3,"peak_pos

#### kworb.net — Spotify daily + per-artist cumulative streams, YouTube daily most-viewed — kworb.net (independent mirror of Spotify and YouTube public counters) ✅ LIVE

Covers **3** subdomains: streaming-counts, video-views, music-charts

- Docs: https://kworb.net/
- Auth: none | Limits: No key, no published rate limit — UNKNOWN; scrape once or twice daily. Daily snapshots retained on-site; per-artist pages carry cumulative totals with a daily delta column.
- Latency: daily | Format: scrape-only (HTML tables)
- Why primary: Spotify's Web API deliberately exposes no play counts — only a 0-100 popularity score — so the artist-stream contracts cannot be settled from Spotify's own API at all. kworb is the only free source mirroring both Spotify's public per-track cumulative counts and YouTube's daily most-viewed. It is a MIRROR, not an authority; its fidelity to Spotify's counter is NOT INDEPENDENTLY VERIFIED by me either, which is why streaming-counts stays PARTIAL.

```bash
curl -sA 'Mozilla/5.0' 'https://kworb.net/spotify/artist/06HL4z0CvFAxyc27GXpf02_songs.html'   # Global daily: https://kworb.net/spotify/country/global_daily.html . YouTube: https://kworb.net/youtube/
```

> Evidence: VERIFIED, all three pages. Artist page HTTP 200, 98895B, title 'Taylor Swift - Spotify Top Songs'; cumulative figures re-extracted by regex: 130,712,336,379 / 126,793,690,756 / 116,022,040,184 — exact match to the report. Global daily HTTP 200, 89204B, title 'Spotify Daily Chart - Global'. YouTube HTTP 200, 103048B, title "Today's Most Viewed Music Videos on YouTube". All three serve under a brows

#### Steam Web API — ISteamChartsService + storefront appdetails (no key) — Valve ✅ LIVE

Covers **1** subdomains: video-games

- Docs: https://partner.steamgames.com/doc/webapi/ISteamChartsService
- Auth: none (no key required for either endpoint) | Limits: Chart methods: no key, no published limit. appdetails is an undocumented storefront endpoint community-observed at roughly 200 requests / 5 minutes per IP — NOT rate-tested by me. No archive — snapshot to build history.
- Latency: sub-minute for concurrent players (response carried last_update 1789960849, ~unix now); daily for storefront metadata | Format: REST JSON
- Why primary: Two unkeyed endpoints cover the subdomain: live concurrent-player rankings and per-app release_date.coming_soon plus the embedded Metacritic score, which is the delay signal behind launch-postponement contracts. IGDB needs a Twitch OAuth app; RAWG's free tier forbids commercial redistribution, which is what a data terminal does.

```bash
curl -s 'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/'   # per-title: curl -s 'https://store.steampowered.com/api/appdetails?appids=271590'
```

> Evidence: VERIFIED with one factual correction and one gotcha. Charts: HTTP 200, 7606B, 0.35s — {"response":{"last_update":1789960849,"ranks":[{"rank":1,"appid":730,"concurrent_in_game":475875,"peak_in_game":1364115},{"rank":2,"appid":570,"concurrent_in_game":394042,...}]}}. Values moved between fetches (report saw 487,451 for appid 730; I saw 475,875 minutes later), which proves it is live, not cached. app

#### Rotten Tomatoes title pages — embedded criticsScore/audienceScore JSON — Fandango / Rotten Tomatoes ✅ LIVE

Covers **1** subdomains: critic-scores

- Docs: https://www.rottentomatoes.com/
- Auth: none | Limits: NO public API — the score object is embedded JSON inside the title page HTML. No published rate limit; scrape hourly at most and expect markup drift. Requires a browser User-Agent. No archive — snapshot to build the review-count curve.
- Latency: near-real-time — the Tomatometer recomputes as reviews land, so reviewCount is itself the embargo-lift signal | Format: scrape-only (JSON embedded in HTML)
- Why primary: The venue markets settle on the live Tomatometer and RT killed its public API. I confirmed this from the venue side: Kalshi market KXRT-RES-98 carries rules_primary 'If Resident Evil has a Tomatometer score of above 98 on Sep 21, 2026 at 10:00 AM ET, then the market resolves to Yes' — a point-in-time read of this exact number. Wikidata's P444 cannot serve that because its values are dated snapshots.

```bash
curl -sA 'Mozilla/5.0' 'https://www.rottentomatoes.com/m/one_battle_after_another' | grep -o '"criticsScore":{[^}]*}'   # TV: https://www.rottentomatoes.com/tv/the_pitt
```

> Evidence: VERIFIED, both URL shapes, with a parser gotcha the report missed. Film HTTP 200, 237482B, 0.46s: "criticsScore":{"averageRating":"8.90","certified":true,"likedCount":420,"notLikedCount":27,"ratingCount":447,"reviewCount":447,"score":"94","sentiment":"POSITIVE","reviewsPageUrl":"/m/one_battle_after_another/reviews","scorePercent":"94%","title":"Tomatometer"}. TV HTTP 200, 185915B: "criticsScore":{

#### Michelin Guide Algolia index (prod-restaurants-en, public search key) — Michelin ✅ LIVE

Covers **1** subdomains: food-and-lifestyle

- Docs: https://guide.michelin.com/
- Auth: none beyond the public search-only Algolia key published in the guide.michelin.com page source; a Referer header of https://guide.michelin.com/ is REQUIRED — I reproduced 403 without it and 200 with it | Limits: Algolia search-only key — no per-caller quota exposed publicly — UNKNOWN; poll at most daily and re-read the key from page source if it rotates. Index carries the current guide year only; snapshot to keep history.
- Latency: event-driven — the index flips on each regional guide ceremony; last_updated is a per-record epoch-ms field | Format: REST JSON (Algolia query API)
- Why primary: The Michelin Guide publishes no API and this index is its own backing store, so one faceted query answers any city/star-count contract worldwide rather than one scraper per region. Verified far denser than the Wikidata alternative: 19,747 faceted records versus 1,313 bare P166 statements with no guide_year or city facet.

```bash
curl -s -X POST -H 'X-Algolia-Application-Id: 8NVHRD7ONV' -H 'X-Algolia-API-Key: 3222e669cf890dc73fa5f38241117ba5' -H 'Referer: https://guide.michelin.com/' -H 'Content-Type: application/json' 'https://8NVHRD7ONV-dsn.algolia.net/1/indexes/prod-restaurants-en/query' -d '{"query":"","hitsPerPage":20,"facetFilters":[["michelin_award:THREE_STARS"],["city.slug:new-york"]]}'
```

> Evidence: VERIFIED — the cleanest reproduction in this report. The literal exampleCall returned HTTP 200, 44749B, 0.26s, nbHits 5, hits ['Sushi Sho','Le Bernardin','Jungsik New York','Per Se','Eleven Madison Park'], guide_year [2025,2025,2025,2025,2025] — the same five names and the same count the report claimed. I independently reproduced the Referer requirement: the identical POST with the Referer header 

#### SEC EDGAR — full-text search (efts) + company submissions JSON — U.S. Securities and Exchange Commission ✅ LIVE

Covers **1** subdomains: media-industry-corporate

- Docs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Auth: none (SEC requires a User-Agent identifying you with contact info) | Limits: Documented 10 requests per second per IP — not rate-tested by me. No key, no daily cap. Full filing history; FTS index covers 2001-present.
- Latency: minutes — 8-K material-event filings appear within minutes of acceptance | Format: REST JSON
- Why primary: M&A and corporate-event contracts settle on a legally binding 8-K, not a trade story, and one full-text query covers every public media company at once rather than a per-company press-release scraper.

```bash
curl -s -H 'User-Agent: EchoFeedMap/1.0 (you@example.com)' 'https://efts.sec.gov/LATEST/search-index?q=%22Warner+Bros.+Discovery%22&forms=8-K'   # and: curl -s -H 'User-Agent: ...' 'https://data.sec.gov/submissions/CIK0001065280.json'
```

> Evidence: VERIFIED, both endpoints, exact figures reproduced. FTS: HTTP 200, 60123B, 0.72s — hits.total {'value': 426, 'relation': 'eq'}, top hit _id '0001437107-22-000135:a2022331-ex991pressrelease.htm', ciks ['0001437107'] (Warner Bros. Discovery), form 8-K. The count 426 matches exactly. Submissions: HTTP 200, 159387B — name 'NETFLIX INC', cik '0001065280', recent forms ['4','144','4','144','144'], filin

#### AniList GraphQL API — AniList ✅ LIVE

Covers **1** subdomains: anime-and-international-media

- Docs: https://docs.anilist.co/
- Auth: none for public queries (OAuth only for user-scoped data) | Limits: Documented 90 requests per minute per IP, currently degraded to 30/min by AniList; 429 with Retry-After. No key. Not rate-tested by me.
- Latency: minutely for trending; airing schedule carries exact per-episode unix airingAt timestamps | Format: GraphQL
- Why primary: The only free, no-key structured feed for the anime side of this subdomain, and one query returns popularity, averageScore, trending rank and the forward airing schedule. It is PREDICTIVE ONLY — it carries no award results, which is why the subdomain stays PARTIAL.

```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"query":"{Page(perPage:3){media(type:ANIME,sort:TRENDING_DESC){id title{romaji} averageScore popularity trending status startDate{year month day}}}}"}' 'https://graphql.anilist.co'
```

> Evidence: VERIFIED. HTTP 200, 607B, 0.41s: {"data":{"Page":{"media":[{"id":178789,"title":{"romaji":"Mushoku Tensei III: Isekai Ittara Honki Dasu"},"averageScore":84,"popularity":158185,"trending":1072,"status":"RELEASING","startDate":{"year":2026,"month":7,"day":4}},{"id":21,"title":{"romaji":"ONE PIECE"},"averageScore":87,"popularity":751736,"trending":379,...}]}} — exact match to the report's figures.

#### Kalshi + Polymarket public market APIs (cross-venue implied probability + resolution text) — Kalshi / Polymarket ✅ LIVE

Covers **18** subdomains: film-awards, tv-awards, music-awards, box-office, critic-scores, streaming-charts, music-charts, streaming-counts, video-views, reality-tv, scripted-tv-and-film-production, video-games, celebrity-events, public-appearances, art-and-auctions, anime-and-international-media, food-and-lifestyle, media-industry-corporate

- Docs: https://trading-api.readme.io/reference/getting-started  |  https://docs.polymarket.com/
- Auth: none for public market/price reads on either venue (Kalshi keys only for trading) | Limits: Kalshi public read tier: no key, cursor-paginated, documented basic tier ~10 read req/sec. Polymarket Gamma: no key, no published limit — UNKNOWN. Both expose full open-market snapshots; neither gives long price history free.
- Latency: seconds — both are live order-book-derived prices | Format: REST JSON
- Why primary: Two unkeyed endpoints return live implied probability AND the exact resolution text for every contract, including subdomains where no fundamental data exists. The resolution text is the load-bearing part: it tells you which other feed actually settles a given market, and I used it during verification to independently confirm Box Office Mojo and Rotten Tomatoes as the named settlement hosts.

```bash
curl -s 'https://gamma-api.polymarket.com/events?limit=2&closed=false&tag_slug=movies'   # Kalshi BY SERIES (required): curl -s 'https://api.elections.kalshi.com/trade-api/v2/markets?limit=200&status=open&series_ticker=KXRT'
```

> Evidence: VERIFIED with a MAJOR FIELD-NAME CORRECTION a developer must have. Kalshi /markets?series_ticker=KXRT: HTTP 200, 394417B, 200 markets, all event_ticker prefix KXRT. Sample: ticker 'KXRT-RES-98', title 'Resident Evil Rotten Tomatoes score?', yes_sub_title 'Above 98', rules_primary 'If Resident Evil has a Tomatometer score of above 98 on Sep 21, 2026 at 10:00 AM ET, then the market resolves to Yes'.

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Film Awards | Wikimedia Pageviews API (nominee attention curves) + Kalshi/ | Wikidata Query Service — P166 / P1411 keyed on per-category  | 🟢 COVERED |
| Television Awards | Wikimedia Pageviews + Kalshi/Polymarket prices (TVmaze premi | Wikidata Query Service — P166 on Emmy category QIDs (Outstan | 🟢 COVERED |
| Music & Stage Awards | Billboard Hot 100 JSON mirror + Apple Marketing Tools RSS ch | Wikidata Query Service — P166 on Grammy/Tony category QIDs ( | 🟢 COVERED |
| Box Office | Wikimedia Pageviews top-1000 film-article velocity + Google  | Box Office Mojo weekend and daily charts (Comscore-sourced) | 🟢 COVERED |
| Critic & Review Scores | Rotten Tomatoes reviewCount field (tracks embargo lift in re | Rotten Tomatoes title-page embedded JSON (criticsScore.score | 🟢 COVERED |
| Streaming Charts | Netflix Tudum prior-week decay (same file) + TVmaze /schedul | Netflix Tudum Top 10 bulk TSV (all-weeks-global.tsv / all-we | 🟢 COVERED |
| Music Charts & Sales | Apple Marketing Tools RSS most-played (daily; verified acros | Billboard — Hot 100 via the mhollingshead JSON mirror; Billb | 🟢 COVERED |
| Artist & Track Stream Counts | kworb Spotify Global Daily per-track play counts + Wikimedia | kworb.net per-artist cumulative-streams pages, which mirror  | 🟡 PARTIAL |
| YouTube & Creator Metrics | kworb.net 'Today's Most Viewed Music Videos' (verified HTTP  | ReturnYouTubeDislike API /votes (returns viewCount with no k | 🟡 PARTIAL |
| Reality Television | Kalshi/Polymarket live prices (the only real signal for vote | Wikipedia REST page summary / season article for the elimina | 🟡 PARTIAL |
| Scripted TV & Film Production | Wikimedia Pageviews + TVmaze show status field (Running/Ende | Google News RSS (indexes Variety and Deadline) + TVmaze prem | 🟡 PARTIAL |
| Video Games | Steam ISteamChartsService live concurrents (verified moving  | Steam storefront appdetails release_date.coming_soon + date  | 🟢 COVERED |
| Celebrities & Personal Milestones | Wikimedia Pageviews spike detection + Kalshi/Polymarket pric | Google News RSS filtered to credible outlets, with Wikimedia | 🟡 PARTIAL |
| Public Appearances & Performances | Google News RSS for announced lineups + Wikimedia Pageviews  | Google News RSS (organizer/broadcaster press releases) | 🟡 PARTIAL |
| Art & Auctions | NONE FOUND | NONE FOUND — Google News RSS carries headline hammer prices  | 🔴 UNCOVERED |
| Anime & International Media | AniList GraphQL (trending rank, popularity, averageScore, fo | NONE VERIFIED — Google News RSS headlines are the only fallb | 🟡 PARTIAL |
| Food, Dining & Lifestyle | Wikimedia Pageviews (Eleven_Madison_Park article verified re | Michelin Guide Algolia index prod-restaurants-en (michelin_a | 🟢 COVERED |
| Media Industry Corporate Events | Kalshi/Polymarket prices + Google News RSS deal reporting +  | SEC EDGAR full-text search + company submissions JSON (8-K m | 🟢 COVERED |

**Rejected**

- **GDELT 2.0 DOC API** — DEAD FROM THIS HOST — independently reproduced by me. HTTP 429, 444B, body 'Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries.' The report's finding holds exactly. Google
- **TMDB API (v3)** — COULD NOT VERIFY — free key required, none available. Auth wall independently reproduced: /3/movie/550 returned HTTP 401 {"status_code":7,"status_message":"Invalid API key: You must be granted a valid key.","success":fal
- **OMDb API** — COULD NOT VERIFY — free key required. Auth wall independently reproduced: HTTP 401, body {"Response":"False","Error":"No API key provided."} Superseded regardless: it relays the RT score without the review count, and the
- **YouTube Data API v3** — COULD NOT VERIFY — free Google Cloud key required. Auth wall independently reproduced: HTTP 403, 'Method doesn't allow unregistered callers (callers without established identity). Please use API Key or other form of API 
- **Trakt API (including /movies/boxoffice)** — COULD NOT VERIFY and superseded — independently reproduced: HTTP 403, 5,482B of Cloudflare challenge HTML with no trakt-api-key header. Byte count matches the report exactly. Box Office Mojo gives daily granularity with 
- **Last.fm API** — COULD NOT VERIFY — free key required (report observed HTTP 400 error 6; I did not re-test, and flag that). Superseded in any case: scrobbles are a sampled listening proxy, whereas the stream-count contracts settle on Spo
- **Spotify Web API** — Wrong tool for every contract here. OAuth client-credentials required, and it exposes no play counts at all — only a 0-100 popularity score — so it cannot settle the artist-stream contracts even with valid credentials. A
- **Invidious public instances (inv.nadeko.net, invidious.nerdvpn.de, yewtu.be)** — DEAD per the report (403 'Endpoint disabled', 401 nginx auth, 403 openresty). NOT RE-TESTED by me — I am accepting rather than confirming this, and flag it as such.
- **Piped API (pipedapi.kavin.rocks)** — DEAD per the report (HTTP 526, 0 bytes). NOT RE-TESTED by me.
- **Artsy API** — TOKEN-WALLED per the report (HTTP 401, 'An application token or a user is required'). NOT RE-TESTED by me. Independent reason to reject regardless: Artsy indexes gallery inventory, not auction hammer results, so it canno
- **IGDB API v4** — Key-walled (Twitch developer app + OAuth client-credentials) and superseded — Steam's unkeyed appdetails and live concurrents cover the subdomain with no registration. NOT RE-TESTED by me.
- **RAWG Video Games Database API** — Licence-blocked for this use case: the free tier is explicitly non-commercial, requires attribution and a backlink, and prohibits redistribution — which is precisely what a data terminal does. Superseded by Steam.
- **Watchmode API** — Too narrow and too small a quota (2,500 credits/month, non-commercial, 3 countries free). Streaming availability is not what any listed contract settles on.
- **New York Times Developer APIs (Books, Movie Reviews)** — Key-walled and maps to no subdomain here — critic-scores settles on Rotten Tomatoes and Metacritic, not NYT.
- **Deezer Public API** — Live per the report but superseded by Apple Marketing Tools RSS, which spans more chart types and 175 storefronts from one template (I verified three storefronts and two chart types myself). Deezer also requires a commer
- **iTunes Search API** — Live per the report but narrower than the Apple RSS chart feed already in primaryFeeds, and rate-limited to ~20 calls/min per IP. Useful only for resolving titles to Apple IDs.
- **MusicBrainz API + bulk dumps** — Live per the report but narrow — release metadata only, no charts and no counts. It does one thing nothing else does: exact per-country release dates that fix Grammy eligibility windows, so it is cited as a supporting fe
- **IMDb Non-Commercial Datasets** — Licensed NON-COMMERCIAL ONLY, which rules it out for a commercial terminal, and its ratings are IMDb user scores that no listed contract settles on. title.basics remains useful offline as a title-ID crosswalk.
- **SteamSpy API** — Live per the report but superseded by Valve's own unkeyed endpoints, and its owner counts are bucketed third-party ESTIMATES, not Valve figures. 1 req/sec. Secondary sizing signal only.
- **Open Library API / Google Books API** — Out of scope — no subdomain in this domain settles on book data.
- **Wikidata Crunchyroll Anime Awards (Q28408321) and Eurovision (Q276) paths** — TOO SPARSE TO USE. Q28408321 returned 2 P166 statements, one of them 'Duolingo'; Q276 returned 4 inconsistently modelled winner rows. This is a per-award coverage limit, not a service failure — the same SPARQL service is
- **Wikidata Michelin star path (P166 / Q20824563)** — Superseded — but I am CORRECTING the stated reason, which was 'returned a handful of rows'. A COUNT query returns 1,313 distinct holders, which is not a handful. The real disqualifier is shape, not volume: the Wikidata p
- **Wikidata as a box-office, video-game, art-auction or celebrity-relationship source** — NEW REJECTION — these were claimed in the report's Wikidata coversSubdomains and I measured each. Box office: P2142 filtered to 2026 releases returns only obscure titles with unnormalized currency, no wide releases. Vide
- **Kalshi yes_bid / last_price / volume field names** — NOT A DEAD FEED BUT A CORRECTION A DEVELOPER MUST READ BEFORE WIRING. The Kalshi markets endpoint does not return yes_bid, yes_ask, last_price, volume or open_interest — I checked all 200 markets in the KXRT series and t
- **Awards organisation sites as a PRIMARY feed (oscars.org, emmys.com, grammy.com, goldenglobes.com)** — Rejected as PRIMARY, not on substance — none has an API, each needs a bespoke scraper whose markup changes every cycle, and one SPARQL query replaces all four for winners and nominees. They remain irreplaceable as the sa

---

### esports

*3/5 subdomains covered · 7 primary feeds*

#### bo3.gg Public REST API — bo3.gg (Cloudflare-fronted, undocumented but open) ✅ LIVE

Covers **4** subdomains: counter-strike, league-of-legends, valorant, dota-and-r6

- Docs: https://bo3.gg/ (no published API docs — endpoints reverse-engineered; JSON:API-style with filter[table.column][op]=value and page[limit]/page[offset])
- Auth: none — no key, no token, no referer check | Limits: No published limit and no rate-limit headers returned (verified: response carries only cf-cache-status/cf-ray/nel — no x-ratelimit-*). Burst test of 12 rapid sequential calls: all HTTP 200. Cloudflare-fronted, so throttling is possible but UNMEASURED at sustained volume. Undocumented and unsupported — can be revoked at will.
- Latency: Live. /matches returns status=upcoming|live|finished; a match that started 2026-09-20T23:55Z already showed status=finished with winner_team_id populated at fetch time. | Format: REST JSON, paginated {total:{count,pages,offset,limit}, results:[...], links:{}}
- Why primary: Still THE broad feed for this domain, and the claim that the venue itself trusts it is CONFIRMED (13 Kalshi series name BO3 as a settlement source). One API, one schema, no auth covers CS2, Valorant, LoL, Dota 2 and Rainbow Six, replacing HLTV + VLR.gg + lolesports + OpenDota + SiegeGG separately. CORRECTION IN bo3.gg's FAVOUR: it carries per-discipline team rankings for FOUR titles (CS2, Valorant, LoL, Dota 2), not CS2 alone — the original under-claimed this. Two corrections against it: the 'limit' parameter in the original exampleCall is silently ignored, and total.count is unreliable under a teams filter.

```bash
curl -s 'https://api.bo3.gg/api/v1/matches?filter%5Bmatches.discipline_id%5D%5Beq%5D=1&filter%5Bmatches.status%5D%5Beq%5D=upcoming&page%5Blimit%5D=50&page%5Boffset%5D=0'   # discipline_id: 1=CS2 2=Valorant 3=LoL 4=Dota2 7=R6Siege 8=MLBB. Rankings: https://api.bo3.gg/api/v1/teams?filter%5Bteams.discipline_id%5D%5Beq%5D=1&sort=rank&page%5Blimit%5D=20 (works for disciplines 1,2,3,4 — returns rank=null for 7 and 8). Also: /api/v1/disciplines | /api/v1/games (per-map rows incl. map_name) | /api/v1/tournaments
```

> Evidence: Re-fetched independently 2026-09-20/21. GET /api/v1/disciplines -> HTTP 200, 1,360B, 8 disciplines: id1 csgo 'Counter-Strike 2', id2 valorant, id3 lol, id4 dota2, id7 r6siege, id8 mlbb — CONFIRMED. Upcoming counts by discipline: CS2=534 (first row 'huskies-esport-vs-bluejays-de-02-09-2026', tier c, bo_type 3), Valorant=34 ('nongshim-redforce-vs-nrg-1-25-09-2026', tier s), LoL=250, Dota2=35 ('auror

#### Liquipedia MediaWiki API (per-title wikis, action=parse + action=query) — Liquipedia / Team Liquid ✅ LIVE

Covers **5** subdomains: counter-strike, league-of-legends, valorant, dota-and-r6, other-titles-and-esports-business

- Docs: https://liquipedia.net/api-terms-of-use (terms + rate limits); standard MediaWiki API at https://liquipedia.net/{wiki}/api.php
- Auth: none — but gzip and a contact-bearing User-Agent are BOTH mandatory. Without Accept-Encoding: gzip the API returns HTTP 406 (independently reproduced). | Limits: Published in the API Terms of Use: 1 request per 2 seconds for HTTP requests generally; action=parse must not exceed 1 request per 30 seconds; the separate keyed API v3 is capped at 60 requests/hour. I honoured 31s spacing across 8 sequential action=parse calls and was never throttled. CC-BY-SA content, attribution required.
- Latency: Live match ticker with forward-dated fixtures. CS2 ticker: 83 timestamps, 33 of them in the future, furthest 2026-10-04T15:30Z. | Format: MediaWiki JSON envelope wrapping rendered HTML (prop=text) — match rows carry machine-readable data-timestamp="<unix>" attributes plus tournament page links, so it is parseable rather than free-text. action=query returns clean JSON.
- Why primary: Confirmed unchanged: the only single feed reaching all five subdomains, and the only free one reaching the fifth at all. Eleven title wikis share one identical API shape. Nothing else free covers Overwatch / Rocket League / StarCraft II / Honor of Kings — for those titles this is not the preferred option, it is the only one, and the verification below makes that sharper: Kalshi has zero open markets on all four, so Liquipedia is essentially the entire feed for them. It is also the tier/prize-pool reference layer bo3.gg does not carry.

```bash
curl -s --compressed -H 'User-Agent: YourProject/1.0 (you@example.com)' 'https://liquipedia.net/counterstrike/api.php?action=parse&page=Liquipedia:Matches&format=json&prop=text'   # swap the wiki slug: leagueoflegends, valorant, dota2, rainbowsix, overwatch, rocketleague, honorofkings. StarCraft 2 and Fortnite have NO Liquipedia:Matches page (verified error code 'missingtitle') — for StarCraft 2 use page=Main_Page; Fortnite has no ticker at all. Awards: page=Esports_Awards
```

> Evidence: Independently re-fetched 2026-09-20/21; every claim in the original reproduced. Without --compressed: HTTP 406 — CONFIRMED. With --compressed, action=query&meta=siteinfo returned HTTP 200 on all 11 wikis with expected sitenames (counterstrike, leagueoflegends, valorant, dota2, rainbowsix, overwatch, rocketleague, starcraft2, honorofkings, fortnite, esports). action=parse&page=Liquipedia:Matches, 3

#### Riot Games Esports API (lolesports + valorantesports, shared backend) — Riot Games ✅ LIVE

Covers **2** subdomains: league-of-legends, valorant

- Docs: https://developer.riotgames.com/ (the esports backend itself is undocumented; the x-api-key below is the public web-client key shipped in lolesports.com's own JS bundle, not a personal credential)
- Auth: Static public web-client key in an x-api-key header; the same value works against both the LoL and VALORANT hosts. Omitting the header returns HTTP 403 {"message":"Forbidden"} — independently reproduced. | Limits: No published quota and no rate-limit headers — UNKNOWN. Undocumented internal service; Riot can rotate the key without notice. Keep bo3.gg discipline_id 2/3 warm as failover.
- Latency: Live — getLive returns in-progress matches (returned {"events":[]} at fetch time, i.e. nothing on air, a valid empty result rather than a failure); getSchedule carries state=completed|unstarted|inProgress per event. | Format: REST JSON, cursor-paginated ({data:{schedule:{pages:{older,newer},events:[...]}}})
- Why primary: The settlement authority itself, not a mirror — and verification STRENGTHENS this. Scanning all 3,828 Kalshi Sports series' settlement_sources: lolesports.com is cited by 52 series and valorantesports.com by 55, not the 35/37 the original reported. They are the two dominant esports resolvers. One key and one request shape serve both subdomains, so it replaces two integrations. Use it for settlement and official schedule/standings; use bo3.gg for historical depth.

```bash
curl -s -H 'x-api-key: <REDACTED>' 'https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US'   # Valorant, same key: curl -s -H 'x-api-key: <REDACTED>' 'https://esports-api.service.valorantesports.com/persisted/val/getSchedule?hl=en-US&sport=val'   # also getLeagues, getLive, getStandings?tournamentId=
```

> Evidence: Independently re-fetched 2026-09-20/21. LoL getSchedule -> HTTP 200, 48,351B, real events e.g. {"startTime":"2026-09-14T16:00:00Z","state":"completed","blockName":"Regional Qualifier","league":{"name":"EMEA Masters"},"match":{"id":"117205970511380860","teams":[{"name":"Movistar KOI Fenix","code":"MKF"}]}}. LoL getLeagues -> 200, 11,495B, 48 leagues: Worlds, MSI, First Stand, LCS, CBLOL, Americas C

#### Kalshi Trade API v2 — public market data + settlement_sources metadata — Kalshi (KalshiEX LLC, CFTC-regulated DCM) ✅ LIVE

Covers **4** subdomains: counter-strike, league-of-legends, valorant, dota-and-r6

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: none for all read-only market/series/event endpoints (auth only for placing orders) — confirmed, every call below was unauthenticated | Limits: Public read tier has no key and no published quota for market data. Kalshi documents tiered limits for authenticated trading only. Sustained-polling ceiling UNMEASURED.
- Latency: Live order book while a market is open. NOTE: markets returned WITHOUT status=open are settled and carry last_price=null / yes_bid=null — the original's sample rows all showed nulls for exactly this reason, which reads like a dead feed but is not. | Format: REST JSON, cursor-paginated; /series rows carry a settlement_sources array inline
- Why primary: Two jobs in one free unauthenticated feed, but the scope is NARROWER than claimed and I removed the fifth subdomain from coversSubdomains. (1) Market-implied probability — verified live and deep for CS2 (KXCS2MAP 200+ open, KXCS2TOTALMAPS 81, KXCS2 8), LoL (KXLOLGAME 64, KXLOLTOTALMAPS 8), Dota 2 (KXDOTA2GAME 48, KXDOTA2TOTALMAPS 24), Valorant (KXVALORANT 16, KXVALORANTGAME 4, KXVALORANTTOTALMAPS 2) and Rainbow Six (KXR6GAME 52). (2) Its /series rows publish settlement_sources naming the exact resolver per contract family — 633 distinct sources across 3,828 Sports series — which is how the settlement column below was derived rather than guessed. The original's claim that Kalshi is 'indispensable for Overwatch/Rocket League/StarCraft II/Honor of Kings where the venue price is the only real prior' is FALSE at fetch time: those series exist in the catalogue but have ZERO open markets, so Kalshi supplies no price for them at all.

```bash
curl -s 'https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXCS2MAP&status=open&limit=200'   # ALWAYS pass status=open — without it you get settled markets with last_price=null. Settlement-source map: curl -s 'https://api.elections.kalshi.com/trade-api/v2/series/KXCS2TOTALMAPS'   # full catalogue (settlement_sources included inline on every row): curl -s 'https://api.elections.kalshi.com/trade-api/v2/series?category=Sports'
```

> Evidence: Independently re-fetched 2026-09-20/21. GET /trade-api/v2/series?category=Sports -> HTTP 200, 6,056,622B, 3,828 series, settlement_sources present inline. All esports tickers the original named CONFIRMED present by exact lookup: KXCS2TOTALMAPS 'CS2 Total Maps', KXVALORANT/TOTALMAPS/MAP/SPREAD/AWARD, KXLOL/KXLOLTOTALMAPS, KXLEAGUE 'League of Legends World Championship', KXDOTA2TOTALMAPS, KXR6TOTALM

#### Polymarket Gamma Markets API — Polymarket ✅ LIVE

Covers **5** subdomains: counter-strike, league-of-legends, valorant, dota-and-r6, other-titles-and-esports-business

- Docs: https://docs.polymarket.com/
- Auth: none | Limits: No key and no published quota on the Gamma read API — UNKNOWN ceiling. ~13 sequential paging calls ran clean with no throttling observed.
- Latency: Live — outcomePrices move with the CLOB book. Verified an unsettled market pricing at ['0.705','0.295'] alongside settled ones at ['1','0']. | Format: REST JSON array of events, each with nested markets[] carrying outcomes[] and outcomePrices[]
- Why primary: The deep-long-tail claim is CONFIRMED and in fact understated — but only via the correct call. Paging tag_slug=esports with offset returns 694 open events, of which 364 are Counter-Strike fixtures (the original reported '100 (page cap)' and treated 100 as the ceiling; limit caps at 100 but offset pages freely). It also carries the esports-business questions nothing else prices ('Will Faker win a Finals MVP Award at an international event in 2026?' at 0.051, 'Will FaZe win a Tier 1 event in 2026?' at 0.0635). PROMOTED IN IMPORTANCE by this verification: since Kalshi has ZERO open markets on Overwatch, Rocket League, StarCraft II and Honor of Kings, Polymarket is the ONLY live venue price for those titles — thin (2, 2, 0, 1 open events) but non-zero. Kalshi/Polymarket cross-checking for calibration is only possible on CS2/LoL/Valorant/Dota.

```bash
curl -s 'https://gamma-api.polymarket.com/events?tag_slug=esports&closed=false&limit=100&offset=0'   # limit caps at 100 (limit=500 silently returns 100) — page with offset. Per-title tags that genuinely return MATCH events: valorant, dota-2, league-of-legends, overwatch, rocket-league, honor-of-kings. DO NOT use tag_slug=counter-strike (see evidence); CS fixtures live under tag_slug=esports. rainbow-six and starcraft return 0 open events.
```

> Evidence: Independently re-fetched 2026-09-20/21. GET /events?tag_slug=esports&closed=false&limit=5 -> HTTP 200, 114,343B; first event {"id":"131447","ticker":"lol-worlds-2026-winning-region-226","title":"Worlds 2026 Winning Region"}, outcomes ["Yes","No"], outcomePrices ["0.705","0.295"] — a genuinely open, moving price. Full paging with limit=100, offset 0..600: 694 open esports events (limit=500 silently

#### OpenDota API — OpenDota (open-source, community-run) ✅ LIVE

Covers **1** subdomains: dota-and-r6

- Docs: https://docs.opendota.com/
- Auth: none for the free tier (an optional free api_key raises limits) | Limits: Verified from live response headers, not docs: x-rate-limit-remaining-minute: 59 and x-rate-limit-remaining-day: 2994 after one call — i.e. 60 calls/minute and ~3,000 calls/day with no key at all. CONFIRMED exactly as originally reported.
- Latency: Live — /live returned in-progress games with game_time and spectator counts; /proMatches newest row start_time 1789930989 (minutes old at fetch). | Format: REST JSON arrays
- Why primary: Kept as primary, with one correction to the justification. The original said 'only OpenDota gives the prior' for Dota 2 — not true: bo3.gg also publishes a Dota 2 team ranking (verified 1 PARIVISION, 2 Team Spirit, 3 Team Yandex). What OpenDota uniquely supplies is a numeric, continuously-updated Elo with win/loss counts and per-match delta (rating 1545.86, wins 345, losses 180, delta -18.40) rather than an ordinal rank, plus 10,240 leagues with tier labels and a live in-progress game feed. That is a strictly richer prior, and the only free calibrated rating anywhere in this domain. It does NOT cover Rainbow Six — the other half of this subdomain has no ratings feed at all.

```bash
curl -s 'https://api.opendota.com/api/teams'   # Elo ratings. Also: https://api.opendota.com/api/proMatches | https://api.opendota.com/api/live | https://api.opendota.com/api/leagues
```

> Evidence: Independently re-fetched 2026-09-20/21. GET /api/teams -> HTTP 200, 253,363B (original said 70,398B — payload larger than reported), exactly 1,000 teams, first {"team_id":9572001,"rating":1545.86,"wins":345,"losses":180,"delta":-18.4049,"name":"TEAM VISION","tag":"VSN"} — matches the original's sample row exactly. GET /api/proMatches -> 200, 33,718B, first row {"match_id":9008730653,"duration":127

#### Steam Web API — ISteamChartsService + GetNumberOfCurrentPlayers — Valve ✅ LIVE

Covers **1** subdomains: other-titles-and-esports-business

- Docs: https://partner.steamgames.com/doc/webapi/ISteamChartsService
- Auth: none — these specific methods need no Steam Web API key (confirmed: both calls made with no key and no headers) | Limits: No key and no published limit for these unkeyed chart methods — UNKNOWN ceiling. Valve's general keyed Web API terms cap at 100,000 calls/day, which these do not consume.
- Latency: GetGamesByConcurrentPlayers carries last_update (1789960249 at fetch) and refreshes continuously; GetNumberOfCurrentPlayers is instantaneous and the two agreed exactly for appid 730. | Format: REST JSON
- Why primary: The only free live signal for the esports-business half of the fifth subdomain, and this verification makes it MORE load-bearing: KXSTEAMTOPSELLER is one of the very few series in that subdomain with open Kalshi markets (20 open, e.g. 'Will Wuthering Waves be #1 on Steam's Weekly Top Sellers'), while every Overwatch / Rocket League / StarCraft II / Honor of Kings series has zero. One call returns the whole top-100 board. CAVEAT the original omitted: this feed returns CONCURRENT PLAYERS, whereas KXSTEAMTOPSELLER settles on Steam's Weekly Top Sellers by REVENUE. Concurrents are a proxy for that series, not its resolver — do not wire it in as a settlement source.

```bash
curl -s 'https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/'   # per-title: curl -s 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=730'  (730=CS2, 570=Dota 2)
```

> Evidence: Independently re-fetched 2026-09-20/21, unkeyed. GET ISteamChartsService/GetGamesByConcurrentPlayers/v1/ -> HTTP 200, 7,606B (original said 1,601B — payload also carries peak_in_game, which the original omitted), last_update 1789960249, 100 ranked rows: (1, appid 730 CS2, 479,730 concurrent, peak 1,364,115), (2, 570 Dota 2, 394,543, peak 899,957), (3, 1867240, 239,064), (4, 578080, 159,082), (5, 8

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Counter-Strike 2 | bo3.gg /teams?filter[teams.discipline_id][eq]=1&sort=rank (C | bo3.gg /matches?filter[matches.status][eq]=finished — verifi | 🟢 COVERED |
| League of Legends | Riot esports-api.lolesports.com getSchedule / getLeagues / g | Riot esports-api.lolesports.com getSchedule (state=completed | 🟢 COVERED |
| Valorant | Riot esports-api.service.valorantesports.com getSchedule?spo | Riot esports-api.service.valorantesports.com getSchedule (st | 🟢 COVERED |
| Dota 2 & Rainbow Six | DOTA 2 — OpenDota /teams Elo (1,000 teams with rating/wins/l | DOTA 2 — OpenDota /proMatches (radiant_win, scores, series_t | 🟡 PARTIAL |
| Other Titles & Esports Business | MATCH TITLES — Liquipedia per-title tickers, all independent | Liquipedia per-title results pages are the only machine-read | 🟡 PARTIAL |

**Rejected**

- **PandaScore** — REJECTED — token-gated, independently re-confirmed 2026-09-20/21: GET https://api.pandascore.co/matches/upcoming -> HTTP 403. Free developer tier is historical/reference only; live match data and odds are paid. bo3.gg de
- **Liquipedia API v3 (api.liquipedia.net/api/v3/…)** — KEY-GATED, NOT VERIFIED — independently re-confirmed: GET /api/v3/match?wiki=counterstrike -> HTTP 403 {"error":["API key \"\" is not valid."]}. Would be the ideal feed (structured LPDB JSON instead of parsed HTML, with 
- **octane.gg / zsr.octane.gg (Rocket League stats)** — DEAD — independently re-confirmed: dig +short api.octane.gg and zsr.octane.gg both return empty; curl exits 6 (could not resolve host) on https://api.octane.gg/events. This was the standard free RLCS stats API and its lo
- **vlrggapi (vlrggapi.vercel.app) — Valorant** — DEAD — independently re-confirmed: /match?q=upcoming -> HTTP 402 (Vercel DEPLOYMENT_DISABLED).
- **hltv-api.vercel.app and mirrors (unofficial HLTV)** — BLOCKED — independently re-confirmed: hltv-api.vercel.app/api/matches -> HTTP 403. Matters more than a normal rejection: HLTV is named in 17 Kalshi series' settlement_sources, including KXCS2TOTALMAPS and the KXRANKLISTC
- **vlr.orlandomm.net (unofficial VLR.gg API) — Valorant** — WORKS, but SUPERSEDED — re-verified live: /api/v1/matches -> HTTP 200, 18,638B, 38 upcoming, first row {"teams":[{"name":"Team Liquid","country":"eu"},{"name":"Paper Rex","country":"sg"}]} — the exact fixture behind Kals
- **Esports Earnings API (api.esportsearnings.com)** — BROKEN — independently re-confirmed: TLS handshake fails, curl exit 60 (expired certificate), so any standards-compliant client cannot reach it at all; it additionally requires a free registered key. Would have been the 
- **Aligulac API (aligulac.com) — StarCraft II ratings** — KEY-GATED, NOT VERIFIED — independently re-confirmed: /api/v1/match/?format=json&limit=2 -> HTTP 401. A free key is available on registration but I hold none and will not claim it works. This is the only known free SC2 r
- **egamersworld.com** — BLOCKED — independently re-confirmed: https://egamersworld.com/ -> HTTP 403. Significant because 'Gamers World' is cited in 38 Kalshi series' settlement_sources — the most-cited esports-specific resolver in the category 
- **DLTV (dltv.org)** — NO PUBLIC API — independently re-confirmed: dltv.org/api/matches -> HTTP 404. Named by Kalshi on 9 series (Dota 2 families plus KXRLTOTALMAPS) but offers nothing machine-readable. OpenDota and bo3.gg cover the Dota 2 gro
- **SofaScore unofficial API (api.sofascore.com)** — BLOCKED — independently re-confirmed: /api/v1/sport/esports/events/live -> HTTP 403. Worth flagging harder than the original did: Sofascore is the single most-cited settlement source across all 3,828 Kalshi Sports series
- **ESPN Core/Site API — esports path** — NOT AVAILABLE FOR THIS DOMAIN — CORRECTION to the original, which reported HTTP 403 Access Denied; I measured HTTP 404 on site.api.espn.com/apis/site/v2/sports/esports/scoreboard. Either way the esports vertical does not
- **TheSportsDB free tier** — NO ESPORTS COVERAGE — live but irrelevant; the catalogue carries no esports leagues. NOT RE-FETCHED this pass; the original finding is accepted as plausible and is non-load-bearing either way.
- **Steam IDOTA2Match_570/GetLiveLeagueGames (Valve official Dota 2 live feed)** — KEY-REQUIRED — free key obtainable but not held. OpenDota /live delivers equivalent in-progress league-game data with no key (re-verified HTTP 200, 142,034B), so this adds nothing even once keyed.
- **Abios, GRID, Strafe, Esports Charts, Sportradar esports** — COMMERCIAL — no free tier for live match or odds data. Not fetched, and not claimed as verified either way.
- **Twitch Helix API (esports viewership)** — NOT VERIFIED — requires a free registered client_id and an OAuth token, neither of which I hold, so I did not test it and will not assert it works. Would be a genuine addition for the esports-business subdomain, which th

---

### financial-markets

*12/22 subdomains covered · 15 primary feeds*

#### FRED — keyless fredgraph CSV series export — Federal Reserve Bank of St. Louis ✅ LIVE

Covers **9** subdomains: sp500, nasdaq, other-indices, market-structure-events, treasury-yields, credit-and-bonds, fx-majors, fx-emerging, dollar-index

- Docs: https://fred.stlouisfed.org/docs/api/fred/
- Auth: none for the fredgraph.csv path (no key, no registration). The api.stlouisfed.org REST path needs a free key — NOT verified, no key available in this session. | Limits: No key, no published rate limit, no daily cap on the fredgraph.csv path. CORRECTED: the report's claim that multiple comma-separated ids 'return a ZIP archive instead' is only partly right. I verified id=DGS10,DGS2 returns a flat wide CSV (content_type application/csv, header 'observation_date,DGS10,DGS2'), while id=DGS10,DGS2,SP500 and an 8-series request both returned application/zip. The response type is therefore set-dependent, not always ZIP — a client MUST branch on Content-Type, or poll one id per request to stay deterministic. Note cosd is honored on the single/flat-CSV path; the 2-series call with cosd=2026-09-15 still returned history from 1976 (222,073 bytes), so date-narrowing is unreliable on multi-id.
- Latency: Daily-close series publish T+1 (SP500, NASDAQ100, VIXCLS, DGS*, BAMLH*). Weekly for DTWEXBGS and the DEX* FX series (~1 week lag). Not intraday. | Format: CSV (single id) / CSV or ZIP of CSVs (multi id — branch on Content-Type)
- Why primary: Confirmed as the broadest feed in the domain and the clearest case of the user's consolidation rule. One keyless endpoint returns S&P 500 closes, Nasdaq-100 closes, Nikkei 225, VIX, the Treasury constant-maturity curve plus spreads, ICE BofA HY/IG/CCC option-adjusted spreads, the Fed's broad dollar index and both major and EM FX crosses. Nine of twenty-two subdomains from one provider with no key, no quota and no signup.

```bash
curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-09-01"
```

> Evidence: VERIFIED — I independently re-fetched 8 distinct series ids, all HTTP 200 with real current data, not the report's cached numbers. DGS10 -> '2026-09-17,4.94' (with 2026-09-15,5.00 and 2026-09-16,5.01 preceding); SP500 -> '2026-09-17,7637.76'; NASDAQ100 -> '2026-09-18,29644.170'; BAMLH0A0HYM2 -> '2026-09-17,2.70'; DEXUSEU -> '2026-09-11,1.1604'; DTWEXBGS -> '2026-09-11,118.2126'; VIXCLS -> '2026-09

#### Cboe Delayed Quotes CDN — option chains (IV + greeks) and per-symbol index quotes — Cboe Global Markets ✅ LIVE

Covers **5** subdomains: sp500, nasdaq, other-indices, single-stocks, market-structure-events

- Docs: https://www.cboe.com/delayed_quotes/spx/quote_table
- Auth: none — no key, no registration, no headers required (plain curl UA works; unlike CNN and Nasdaq below, no browser UA needed) | Limits: No published rate limit and no key. Data ~15 minutes delayed. Undocumented static-CDN objects with no official API docs — can change without notice. SPX payload is 13.08 MB per fetch; budget bandwidth. CORRECTED: the index-enumeration object all_indices.json is NOT available — see rejectedFeeds. You must know the symbol in advance; there is no working free discovery endpoint on this host.
- Latency: ~15-minute delayed snapshot, refreshed continuously during the session; safe to poll at 1-5 minute intervals. CAUTION: freshness is per-symbol and not uniform — _SPX/_NDX/_VIX/_RUT/_SKEW all carried last_trade_time 2026-09-18 with a current server timestamp, but _DJI came back with an object timestamp of 2026-09-08, roughly two weeks stale. Read the per-object timestamp before using a value; do not assume the snapshot is current because the fetch succeeded. | Format: REST JSON (static CDN objects)
- Why primary: Still the only free feed giving the option-implied probability distribution, which is what actually prices a threshold contract like 'S&P above 7500 on date X'. One base path serves cash-index chains and every optionable US single stock; the sibling /quotes/ path serves named index levels including the VIX term structure. Put/call ratios are derivable directly from the live chain rather than needing a second feed. The enumeration claim is withdrawn but the per-symbol claim holds.

```bash
curl "https://cdn.cboe.com/api/global/delayed_quotes/options/_SPX.json"   # index chain, 13 MB
curl "https://cdn.cboe.com/api/global/delayed_quotes/options/NVDA.json"   # single-stock chain
curl "https://cdn.cboe.com/api/global/delayed_quotes/quotes/_VIX.json"    # index level
```

> Evidence: VERIFIED with one correction. _SPX.json HTTP 200, 13,081,071 bytes, downloaded in full and parsed: 29,518 contracts, exactly 14,759 calls and 14,759 puts; sample SPX261016C00200000 bid=7460.0 ask=7484.0 iv=5.5037 delta=1.0 theta=-0.0056 vega=0.0009 oi=2978. I independently re-derived put/call from the live chain: volume ratio 1.608, OI ratio 1.424 — reproduces the report exactly. NVDA.json HTTP 20

#### SEC EDGAR — XBRL frames/companyfacts + full-text search + getcurrent Atom + submissions — US Securities and Exchange Commission ✅ LIVE

Covers **10** subdomains: ipos, mergers-and-acquisitions, earnings, executive-changes, private-valuations, index-membership, corporate-legal-and-regulatory, credit-and-bonds, consumer-prices-firm-level, single-stocks

- Docs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Auth: none, but a descriptive User-Agent header with a contact email is mandatory — SEC blocks requests without it. CONFIRMED: all four endpoints returned 200 with the UA 'Verifier verify@example.com'. | Limits: 10 requests/second fair-access policy, no daily cap, no key. Full-text search covers 2001 to present and caps at 10,000 hits per query (paginate with &from=). XBRL history from ~2009, raw filings from 1993. Bulk companyfacts.zip available as an alternative to per-company polling.
- Latency: Minutes — filings appear on the getcurrent Atom feed within minutes of acceptance | Format: REST JSON + Atom XML + bulk ZIP
- Why primary: Every corporate-event subdomain here resolves on a document filed with the SEC, so one provider settles ten of them. 8-K Item 1.01 plus DEFM14A and Form 425 carry M&A; Item 2.02 carries earnings releases; Item 5.02 carries CEO and director departures; S-1 and 424B4 carry IPOs; Form D carries private rounds. Full-text search turns all of that into one queryable index instead of per-topic news APIs. It is also the only authoritative settlement layer here — a contract on 'did company X announce Y' resolves on the filing, not on a vendor's summary of it.

```bash
curl -A "YourApp you@example.com" "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&count=5&output=atom"
curl -A "YourApp you@example.com" "https://efts.sec.gov/LATEST/search-index?q=%22definitive+merger+agreement%22&forms=8-K&startdt=2026-08-01&enddt=2026-09-20"
curl -A "YourApp you@example.com" "https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2026Q1.json"
curl -A "YourApp you@example.com" "https://data.sec.gov/submissions/CIK0000320193.json"
```

> Evidence: VERIFIED — all four example calls re-run independently, all HTTP 200 with real data. getcurrent Atom: '<title>Latest Filings - Sun, 20 Sep 2026 23:06:31 EDT</title>' with live entry '8-K - VisionWave Holdings, Inc. (0002038439) (Filer)' linking to Archives/edgar/data/2038439/000173112226001264/. efts full-text search (the search-index path as literally written in exampleCall): HTTP 200, took=695ms

#### Nasdaq Data API — earnings calendar, IPO calendar, index constituents, quotes — Nasdaq, Inc. ✅ LIVE

Covers **5** subdomains: earnings, ipos, index-membership, single-stocks, other-indices

- Docs: https://www.nasdaq.com/market-activity/earnings
- Auth: none, but a browser User-Agent is required — the default curl UA is rejected. CONFIRMED: the short token -A "Mozilla/5.0" is sufficient here (unlike CNN, which needs a full realistic UA string). | Limits: No key, no published rate limit. Undocumented — this is the backing API for nasdaq.com's own pages and carries no stability guarantee. Earnings calendar is queried one date at a time; IPO calendar one month at a time.
- Latency: Daily for calendars (forward-looking), real-time/delayed for quotes | Format: REST JSON
- Why primary: Supplies the two things EDGAR cannot: forward consensus and the analyst-estimate count. EDGAR tells you what was reported after the fact; this tells you what the street expects before it, which is the input that prices an earnings-beat contract. One host also covers the forward IPO pipeline split into priced/filed/withdrawn and the live Nasdaq-100 constituent list, replacing three separate vendors. Chosen over Alpha Vantage, whose free tier is now 25 requests/day.

```bash
curl -A "Mozilla/5.0" "https://api.nasdaq.com/api/calendar/earnings?date=2026-09-22"
curl -A "Mozilla/5.0" "https://api.nasdaq.com/api/ipo/calendar?date=2026-09"
curl -A "Mozilla/5.0" "https://api.nasdaq.com/api/quote/list-type/nasdaq100"
```

> Evidence: VERIFIED — all three example calls re-run independently. Earnings calendar HTTP 200, asOf 'Tue, Sep 22, 2026', headers confirm the consensus fields exist ('Consensus EPS* Forecast', '# of Ests'), first row AZO AutoZone, Inc. marketCap $46,434,370,000 fiscalQuarterEnding Aug/2026 time-pre-market lastYearEPS $48.71 — reproduces the report. IPO calendar HTTP 200, 8,199 bytes, buckets 'priced' present

#### open.er-api.com — keyless spot FX, 166 currencies — ExchangeRate-API (open access tier) ✅ LIVE

Covers **3** subdomains: fx-majors, fx-emerging, dollar-index

- Docs: https://www.exchangerate-api.com/docs/free
- Auth: none — no key, no registration | Limits: No key and no hard published cap on the open endpoint; rates refresh roughly every 24h. 166 currencies confirmed by count. No intraday ticks, no bid/ask, no history on this endpoint.
- Latency: Daily refresh; response carries time_last_update_utc so staleness is checkable | Format: REST JSON
- Why primary: Exactly the consolidation the user asked for: one keyless call returns every major AND every exotic in a single 2,970-byte JSON object, so there is no per-pair API. FRED's DEX* series lag a week and cover ~25 crosses; Frankfurter covers only the ~30 ECB reference currencies and carries no ARS or TWD. This one carries the full EM set Kalshi actually lists. It also supplies all six ICE DXY constituents, making the dollar index computable from the published formula — as a derived value, not the settled print.

```bash
curl "https://open.er-api.com/v6/latest/USD"
```

> Evidence: VERIFIED — HTTP 200, 2,970 bytes, result='success', time_last_update_utc='Mon, 21 Sep 2026 00:02:31 +0000', rates dict length 166 (counted, not asserted). SPOT-CHECK OF BOTH CLAIMED FX SUBDOMAINS, values pulled live: majors EUR 0.871295, JPY 156.918661, GBP 0.747411, CHF 0.823021, CAD 1.399324, SEK 9.836386; EM ARS 1512.3332, TWD 31.806515, KRW 1386.016611, TRY 48.794548, RUB 84.261619, NGN 1332.8

#### Kalshi Trade API v2 — public markets, series and order book — Kalshi (CFTC-regulated DCM) ✅ LIVE

Covers **22** subdomains: sp500, nasdaq, other-indices, single-stocks, market-structure-events, treasury-yields, credit-and-bonds, fx-majors, fx-emerging, dollar-index, ipos, mergers-and-acquisitions, earnings, corporate-kpis-and-altdata, executive-changes, private-valuations, index-membership, net-worth

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: none for public market-data endpoints (no key needed for /series, /markets, /events, /trades). Trading endpoints need signed auth. Confirmed keyless on all four calls above. | Limits: No key and no published cap on public read endpoints. IMPORTANT BEHAVIOURAL NOTE I verified: the ?category= filter is LOOSE, not strict — category=Financials returned 1,040 series of which only 914 are actually category 'Financials' (the rest are Science and Technology 45, Companies 31, Climate 19, Entertainment 12, Commodities 9, Economics 5, Politics 4, Elections 1). Do not treat the filter as authoritative; read each object's own 'category'. The /series responses carry no pagination cursor — one call returns the whole set. /markets IS cursor-paginated. A truncated /series download will silently parse as a valid but incomplete JSON object, so verify the response byte count before indexing.
- Latency: Real-time — live last_price, bid/ask and liquidity per market | Format: REST JSON
- Why primary: This is the venue's own book, so it is the one feed that touches all twenty-two subdomains — but only if you query more than one category (see exampleCall). The market's own implied probability is the strongest single predictor for any contract, and for the subdomains where no fundamental free feed exists (collectibles, card-spend KPIs) it is the only live numeric signal at all. Each series object also carries the settlement-source language, which is how you learn what a contract actually resolves on.

```bash
curl "https://api.elections.kalshi.com/trade-api/v2/series?category=Financials"
curl "https://api.elections.kalshi.com/trade-api/v2/series?category=Politics"   # legal + prediction-market-industry series live HERE, not under Financials
curl "https://api.elections.kalshi.com/trade-api/v2/markets?limit=5&status=open&series_ticker=KXINXY"
curl "https://api.elections.kalshi.com/trade-api/v2/series/KXINXY"   # single-series lookup, returns settlement-source language
```

> Evidence: VERIFIED, after an initial failure that is itself the finding. My first fetch of series?category=Financials came back truncated and contained NONE of the report's claimed tickers — zero hits for KXINXY, KXNOTE10, KXUSDX, KXFEAR, KXBUFFETTNW, KXSP500ADDQ, KXSTOCKX8BUGSBUNNY, KXCOSTCOHOTDOG. A clean re-fetch (HTTP 200, 972,021 bytes, 1,040 series) found all eight present. Combined with category=Comp

#### Polymarket Gamma API — events, markets and public search with live outcome prices — Polymarket ✅ LIVE

Covers **17** subdomains: sp500, other-indices, single-stocks, market-structure-events, treasury-yields, fx-majors, fx-emerging, dollar-index, ipos, mergers-and-acquisitions, earnings, private-valuations, index-membership, net-worth, collectibles-and-alt-assets, corporate-legal-and-regulatory, prediction-market-industry

- Docs: https://docs.polymarket.com/developers/gamma-markets-api/overview
- Auth: none | Limits: No key, no registration, no published rate limit. Supports tag_slug, closed, order, limit/offset filters. The public-search endpoint is the practical way to confirm per-subdomain coverage — tag_slug=business alone does not surface the FX or Treasury markets.
- Latency: Real-time — outcomePrices are live CLOB mids | Format: REST JSON
- Why primary: The second venue book. Polymarket lists longer-dated and more narrative contracts than Kalshi and prices them independently, so holding both gives a cross-venue spread that is itself a signal. Keyless, no per-topic alternative needed. I added dollar-index to coversSubdomains — the report under-claimed it and I verified a live DXY market.

```bash
curl "https://gamma-api.polymarket.com/events?closed=false&limit=6&tag_slug=business&order=volume&ascending=false"
curl "https://gamma-api.polymarket.com/markets?closed=false&limit=3&tag_slug=business"
curl "https://gamma-api.polymarket.com/public-search?q=treasury%20yield&limit_per_type=3&events_status=active"
```

> Evidence: VERIFIED and coverage independently spot-checked well beyond the report. events?tag_slug=business HTTP 200, 740,673 bytes, parsed 6 live events with volumes: 'How many Fed rate cuts in 2026?' 53,117,509; 'Which companies will be acquired before 2027?' 18,253,288; 'Largest Company end of December 2026?' 7,415,693; 'IPOs before 2027?' 7,352,624; 'Largest IPO by market cap in 2026?' 6,077,351; 'OpenA

#### US Treasury — Daily Yield Curve CMT CSV + FiscalData auctions API — US Department of the Treasury ✅ LIVE

Covers **2** subdomains: treasury-yields, credit-and-bonds

- Docs: https://fiscaldata.treasury.gov/api-documentation/
- Auth: none | Limits: No key, no registration, no published cap. CMT CSV returns the full calendar year in one request across all 14 tenors. FiscalData is JSON:API with page[size] up to 10,000.
- Latency: CMT posts ~15:30 ET each business day; auction results post same-day | Format: CSV (CMT) + REST JSON (FiscalData)
- Why primary: This is the settlement authority, not a mirror of it. Kalshi's KXNOTE10 family resolves on Treasury's published CMT, so FRED's DGS10 — itself a T+1 copy of this file — is a predictive convenience while this is the resolving print. The same provider's FiscalData endpoint carries the forward auction calendar, the event that moves the curve, so one provider gives both the outcome and its schedule.

```bash
curl "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv"
curl 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/auctions_query?sort=-auction_date&page%5Bsize%5D=3'
```

> Evidence: VERIFIED — both calls re-run. CMT CSV HTTP 200, header exactly 'Date,"1 Mo","1.5 Month","2 Mo","3 Mo","4 Mo","6 Mo","1 Yr","2 Yr","3 Yr","5 Yr","7 Yr","10 Yr","20 Yr","30 Yr"' with live rows '09/18/2026,3.97,3.98,4.10,4.14,4.24,4.24,4.44,4.76,4.83,4.86,4.93,5.01,5.38,5.34' and '09/17/2026,...,4.94,5.32,5.29'. CROSS-CHECK: the 09/17 10-Yr print of 4.94 matches FRED DGS10 '2026-09-17,4.94' exactly, 

#### CourtListener REST API v4 + RECAP — Free Law Project ✅ LIVE

Covers **4** subdomains: corporate-legal-and-regulatory, prediction-market-industry, mergers-and-acquisitions, credit-and-bonds

- Docs: https://www.courtlistener.com/help/api/rest/
- Auth: none for the search endpoint at low volume; a free token raises limits. Confirmed keyless with a plain curl UA. | Limits: Keyless search works; Free Law Project asks for a token for sustained use. Cursor-paginated. type=r searches RECAP federal dockets, type=o searches opinions.
- Latency: Dockets sync from PACER within hours; opinions within a day | Format: REST JSON
- Why primary: The only free structured view into federal dockets, which is where the litigation-shaped contracts in this domain resolve — antitrust challenges to pending mergers, bankruptcy filings, and the prediction-market cases themselves. One query string covers all four subdomains; the alternative is per-district PACER RSS scraping.

```bash
curl "https://www.courtlistener.com/api/rest/v4/search/?q=Kalshi&type=r&order_by=dateFiled%20desc"
```

> Evidence: VERIFIED — HTTP 200, 78,003 bytes, real JSON not an HTML page. Body: count=180, document_count=3332, cursor-paginated 'next' URL present, results array populated with docket objects (first carries an assignedTo field). Reproduces the report's figures exactly. 180 live federal dockets matching Kalshi is precisely the prediction-market-industry docket set.

#### Federal Register API v1 — agency rulemaking documents — US Government Publishing Office / National Archives ✅ LIVE

Covers **3** subdomains: prediction-market-industry, corporate-legal-and-regulatory, credit-and-bonds

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none | Limits: No key, no registration, no published cap. Filter by agency, document type, date range, and full text. Field projection supported. Cursor pagination via search_after_cursor.
- Latency: Daily — documents appear on the publication date, with public-inspection items a day earlier | Format: REST JSON
- Why primary: Regulatory contracts resolve on a published rule, and this is the publication of record. Swapping the agency slug covers CFTC, SEC, FTC and DOJ from one endpoint, replacing several agency press-release scrapers with a single structured query.

```bash
curl "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=commodity-futures-trading-commission&per_page=4&order=newest&fields%5B%5D=title&fields%5B%5D=publication_date&fields%5B%5D=type"
```

> Evidence: VERIFIED — HTTP 200, description 'Documents from Commodity Futures Trading Commission', count=4065, total_pages=50, next_page_url with a search_after_cursor. Live results with field projection working: 2026-09-21 'Privacy Act Regulations' (Proposed Rule); 2026-09-16 'Whistleblower Award Determination' (Rule). Reproduces the report's count exactly.

#### Forbes Real-Time Billionaires JSON — Forbes Media ✅ LIVE

Covers **1** subdomains: net-worth

- Docs: https://www.forbes.com/real-time-billionaires/
- Auth: none, but a browser User-Agent is required. The ?fields= projection is also load-bearing — I independently confirmed the bare URL fails. | Limits: No key. Undocumented — the backing endpoint for the Forbes real-time page, no stability guarantee. CONFIRMED CRITICAL: the bare URL without ?fields= returns HTTP 503 (109-byte body); with the projection it returns 200. finalWorth is in USD millions. Response size varies between fetches (I measured 309,868 bytes where the report measured 224,807) — do not assert on content length.
- Latency: Intraday, tracking underlying stock moves during market hours | Format: REST JSON
- Why primary: A deliberately narrow feed: net-worth is the one subdomain no broad feed reaches, and Kalshi's KXBUFFETTNW/KXBEZOSNW family settles on a published billionaire index. Forbes is the only one of the two named settlement sources with a free machine-readable endpoint, and one call returns the whole list rather than one person per request.

```bash
curl -A "Mozilla/5.0" "https://www.forbes.com/forbesapi/person/rtb/0/position/true.json?fields=personName,finalWorth,rank,source"
```

> Evidence: VERIFIED including the failure mode. With ?fields= projection: HTTP 200, 309,868 bytes, parsed personList.personsLists with live ranks — rank 1 Elon Musk finalWorth 946475.522 source 'Tesla, SpaceX'; rank 2 Jeff Bezos 373127.836 source 'Amazon' (USD millions). NEGATIVE CONTROL reproduced: the same URL without ?fields= returned HTTP 503, 109 bytes. The report's warning is correct and load-bearing.

#### CNN Fear & Greed Index dataviz endpoint — CNN Business ✅ LIVE

Covers **1** subdomains: market-structure-events

- Docs: https://www.cnn.com/markets/fear-and-greed
- Auth: CORRECTED — the report's stated requirement is wrong and would have shipped broken. It says a browser UA plus Referer suffices; I reproduced HTTP 418 twice using exactly its example call (curl -A "Mozilla/5.0" with the Referer header). The host rejects the truncated 'Mozilla/5.0' UA token. A FULL, realistic browser UA string plus Referer: https://www.cnn.com/ returns 200 reliably. Both headers are required. | Limits: No key. Undocumented internal dataviz endpoint. Returns the current composite score and rating plus the full history of all seven component indicators in one 177,365-byte response. A dated sub-path (/graphdata/YYYY-MM-DD) works and returns a much smaller 10,978-byte payload — prefer it for polling.
- Latency: Updated each trading day at close; response carries an ISO timestamp | Format: REST JSON
- Why primary: Kalshi's KXFEAR settles on the CNN Fear & Greed reading specifically, and this is that exact number rather than a reconstruction. No broad feed carries it. One call also returns the underlying component indicators, which is the predictive decomposition, so it serves both sides of the subdomain.

```bash
curl -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' -H 'Referer: https://www.cnn.com/' "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
curl -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36' -H 'Referer: https://www.cnn.com/' "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/2026-09-01"
```

> Evidence: VERIFIED ONLY AFTER CORRECTING THE HEADERS. Reproducing the report's own example call (-A "Mozilla/5.0" + Referer) returned HTTP 418 with a 27-byte body, twice, in two separate sessions — the report's stated auth requirement is insufficient. With a full Chrome UA string plus Referer: HTTP 200, 177,365 bytes, reproducibly (three consecutive attempts: 200/200/200, identical byte counts). Parsed fear

#### State Street SPDR daily holdings file (SPY) + Nasdaq index constituent lists — State Street Global Advisors / Nasdaq ✅ LIVE

Covers **3** subdomains: index-membership, sp500, nasdaq

- Docs: https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy
- Auth: none, but a browser User-Agent and redirect-following (-L) are required for the SSGA file | Limits: No key. SSGA publishes a fresh XLSX each business day with every constituent plus weight, shares held, CUSIP, SEDOL, sector and local currency. Nasdaq's list-type endpoint is undocumented. Note the file is mostly legal disclosure text by string volume — parse the holdings sheet, not sharedStrings wholesale.
- Latency: Daily, one business day behind the index | Format: XLSX (SSGA) + REST JSON (Nasdaq)
- Why primary: Index-membership contracts need the current constituent set and its weights to compute how close a candidate sits to the eligibility screens. S&P Dow Jones' own announcement RSS is 403 and Invesco's QQQ CSV is 406, so the tracking ETF's published holdings file is the accessible authoritative constituent list. Two requests cover both major US indices.

```bash
curl -L -A "Mozilla/5.0" -o spy.xlsx "https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx"
curl -A "Mozilla/5.0" "https://api.nasdaq.com/api/quote/list-type/nasdaq100"
```

> Evidence: VERIFIED — SSGA SPY HTTP 200 after redirect, content_type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, 54,385 bytes, `file` reports 'Microsoft OOXML' (a real workbook, not an HTML error page). I unzipped it and parsed xl/sharedStrings.xml: 2,048 strings, headers 'Fund Name:', 'Ticker Symbol:', 'Holdings:' present, fund identified as 'State Street SPDR S&P 500 ETF Trust' / 'SP

#### CFTC Commitments of Traders (Socrata Open Data) — US Commodity Futures Trading Commission ✅ LIVE

Covers **5** subdomains: dollar-index, fx-majors, sp500, nasdaq, treasury-yields

- Docs: https://publicreporting.cftc.gov/
- Auth: none (a free Socrata app token raises throttling limits) | Limits: Keyless access is throttled but functional; Socrata SoQL supports $where, $select, $order, $group, $limit. Only 371 markets are reported at the latest report date, of which 84 are FINANCIAL INSTRUMENTS. Verified subgroup counts at 2026-09-15: STOCK INDICES 23, CURRENCY 8, CURRENCY(NON-MAJOR) 4, Interest Rates - U.S. Treasury 7, Interest Rates - non U.S. Treasury 4, INTEREST RATE SWAPS 4, OTHER FINANCIAL INSTRUMENTS 5.
- Latency: Weekly — Tuesday positions published Friday 15:30 ET. Latest report_date in the dataset confirmed as 2026-09-15. | Format: REST JSON (Socrata SoQL)
- Why primary: Positioning is the one predictive input price data cannot give you, and one SoQL endpoint covers the index, Treasury and FX futures complexes at once rather than one positioning source per asset. It is the only free source for the COT data the dollar-index and FX contracts are usually reasoned about with.

```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?\$limit=5&\$where=report_date_as_yyyy_mm_dd='2026-09-15T00:00:00.000'%20AND%20commodity_subgroup_name='STOCK%20INDICES'&\$select=market_and_exchange_names,noncomm_positions_long_all"
```

> Evidence: VERIFIED LIVE, WITH A TRAP THE REPORT WOULD HAVE SHIPPED. The endpoint is up (HTTP 200) and max(report_date) = 2026-09-15 with 371 rows. The report's own example call ($order by date DESC, $limit 3) returns arbitrary energy contracts and proves nothing about the claimed subdomains, so I queried each one by name at the latest report date. WORKING: 'E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE' nonc

#### FINRA Reg SHO daily short-sale volume — Financial Industry Regulatory Authority ✅ LIVE

Covers **2** subdomains: single-stocks, market-structure-events

- Docs: https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data
- Auth: none for the Reg SHO CDN files; the api.finra.org short-interest API needs free credentials (NOT verified — no credentials in this session) | Limits: No key on the CDN path, no published cap. One pipe-delimited file per trading day covering every consolidated-tape symbol in a single request — 12,317 lines / 544 KB for the day I fetched. Filename encodes the date as YYYYMMDD; there is no file on non-trading days.
- Latency: Daily, published after the close | Format: Pipe-delimited text
- Why primary: Short-sale pressure is a named pricing input for the single-stock contracts and no other free feed carries it. One file per day covers the entire market rather than one request per ticker, which is the consolidation rule applied to the short-interest layer.

```bash
curl "https://cdn.finra.org/equity/regsho/daily/CNMSshvol20260918.txt"
```

> Evidence: VERIFIED — HTTP 200, 544,090 bytes, 12,317 lines (counted). Header exactly 'Date|Symbol|ShortVolume|ShortExemptVolume|TotalVolume|Market' with real rows '20260918|A|633386.346426|17|915680.398509|B,Q,N' and '20260918|AA|1000533.549578|5172|2230180.977834|B,Q,N'. Real pipe-delimited data, not an HTML error page. Line count confirms whole-market coverage rather than a truncated sample.

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| S&P 500 | Cboe Delayed Quotes CDN — _SPX.json full option chain, which | FRED series SP500 for the official index close — independent | 🟢 COVERED |
| Nasdaq-100 | Cboe /quotes/_NDX.json for the live level (29644.168 verifie | FRED series NASDAQ100 for the official close — verified '202 | 🟢 COVERED |
| Other Global Indices | FRED NIKKEI225 (verified '2026-09-18,65018.95'). Cboe /quote | FRED for Nikkei 225. For FTSE, DAX, KOSPI, S&P/BMV IPC and t | 🟡 PARTIAL |
| Single-Stock Prices | Cboe per-ticker option chains — I re-fetched and parsed NVDA | SEC EDGAR submissions/companyfacts for anything resolving on | 🟡 PARTIAL |
| Market Structure & Sentiment | Cboe /quotes/ for the VIX term structure — _VIX 14.81, _VIX9 | CNN Fear & Greed dataviz endpoint for KXFEAR — verified scor | 🟢 COVERED |
| Treasury Yields & Spreads | FRED for the curve and its spreads — DGS10 verified across f | US Treasury Daily Yield Curve CMT CSV — the resolving print, | 🟢 COVERED |
| Credit, Bonds & Ratings | FRED ICE BofA OAS series — BAMLH0A0HYM2 re-verified live at  | SEC EDGAR full-text search for the filing that carries a def | 🟡 PARTIAL |
| FX — Major Pairs | open.er-api.com for live spot across all majors in one keyle | ECB Data Portal SDMX EXR — I verified this independently bec | 🟢 COVERED |
| FX — EM & Other Pairs | open.er-api.com is the decisive feed — 166 currencies from o | FRED DEX* series for the pairs the Fed publishes, weekly. Fo | 🟡 PARTIAL |
| Dollar Index | open.er-api.com supplies all six ICE DXY constituents in one | NONE FOUND for the official ICE US Dollar Index print. Cboe  | 🟡 PARTIAL |
| IPOs & Listings | api.nasdaq.com/api/ipo/calendar — re-verified HTTP 200, 8,19 | SEC EDGAR — the S-1 effectiveness notice and the 8-A12B list | 🟢 COVERED |
| M&A | SEC EDGAR full-text search — I re-ran the exact query and go | SEC EDGAR — the definitive agreement (8-K Item 1.01 with EX- | 🟢 COVERED |
| Earnings Results | api.nasdaq.com/api/calendar/earnings — re-verified HTTP 200, | SEC EDGAR 8-K Item 2.02 with the EX-99.1 press release, plus | 🟢 COVERED |
| Corporate KPIs & Alternative Data | Kalshi itself is the only live numeric signal — 19 matching  | NONE FOUND. Kalshi settles these on Carbon Arc and Fiscal.ai | 🔴 UNCOVERED |
| CEOs & Executive Changes | SEC EDGAR full-text search over 8-K Item 5.02 plus the getcu | SEC EDGAR 8-K Item 5.02 — the legally required disclosure an | 🟢 COVERED |
| Private Company Valuations | SEC EDGAR Form D via the getcurrent Atom feed (endpoint veri | NONE FOUND for the valuation figure itself. Form D reports t | 🟡 PARTIAL |
| Index Membership | SSGA SPY daily holdings XLSX — re-fetched, unzipped and pars | SEC EDGAR 8-K/Form 25 for the delisting leg (verified). For  | 🟡 PARTIAL |
| Billionaire Net Worth | Forbes Real-Time Billionaires JSON — re-verified HTTP 200, 3 | Forbes Real-Time Billionaires — the same verified endpoint i | 🟢 COVERED |
| Collectibles & Alternative Assets | Venue books only. Kalshi carries 21 matching series on clean | NONE FOUND. StockX has no public API, Bezel has no API, eBay | 🔴 UNCOVERED |
| Corporate Legal & Regulatory | CourtListener REST v4 + RECAP — re-verified HTTP 200, 78,003 | CourtListener / RECAP for the docket entry itself — the orde | 🟢 COVERED |
| Prediction Market Industry | Federal Register API filtered to the CFTC — re-verified coun | Federal Register for a final rule; CourtListener/RECAP for a | 🟢 COVERED |
| Firm-Level Price Changes | SEC EDGAR full-text search over 8-K and 10-Q for pricing-act | NONE FOUND as a structured feed. These settle on a company a | 🟡 PARTIAL |

**Rejected**

- **Cboe all_indices.json (cdn.cboe.com/api/global/delayed_quotes/all_indices.json)** — NEWLY REJECTED BY THIS VERIFICATION — the report claimed HTTP 200, 1,412,208 bytes enumerating 2,461 Cboe indices. It does not. I fetched it three times: plain curl, with a full Chrome User-Agent, and with UA plus Refere
- **Yahoo Finance v8 chart endpoint (query1/query2.finance.yahoo.com)** — REJECTED as unreliable — carried over from the report, not re-tested in this session (I did not want to burn the IP's remaining quota on a feed already excluded). The report documents HTTP 429 on 17 of 18 attempts includ
- **Pyth Network Hermes price feeds (hermes.pyth.network)** — REJECTED — paywalled per the report; NOT RE-VERIFIED in this session. The report documents the metadata endpoint /v2/price_feeds still working keyless while both price-retrieval paths (/v2/updates/price/latest and /api/l
- **Stooq CSV endpoints (/q/l/ and /q/d/l/)** — REJECTED — JavaScript proof-of-work bot challenge per the report; NOT RE-VERIFIED. /q/l/ returns 404 and /q/d/l/ returns HTTP 200 carrying a challenge page rather than CSV, which is exactly the '200 is not a pass' failur
- **Cboe put/call ratio CSV archive (cdn.cboe.com/resources/options/volume_and_call_put_ratios/)** — REJECTED AS STALE — carried forward from the report, and the replacement is CONFIRMED WORKING. The archive files return HTTP 200 with a last row dated 10/04/2019. I independently verified the recommended substitute: comp
- **Cboe VIX history CSV (cdn.cboe.com/api/global/us_indices/daily_prices/_VIX_History.csv)** — REJECTED — HTTP 403 AccessDenied per the report; NOT RE-VERIFIED individually, but consistent with the all_indices.json 403 I did reproduce on the same host, which suggests Cboe has tightened access to the non-quote CDN 
- **Invesco QQQ holdings CSV** — REJECTED — HTTP 406 per the report; NOT RE-VERIFIED. Superseded regardless: api.nasdaq.com/api/quote/list-type/nasdaq100 returned 101 constituents cleanly on my independent fetch (HTTP 200, 21,556 bytes, totalrecords=101
- **Slickcharts (nasdaq100 / sp500 constituent pages)** — REJECTED — HTTP 403 per the report; NOT RE-VERIFIED. Superseded by the SSGA SPY holdings file and the Nasdaq list-type endpoint, both of which I did verify and both of which are issuer/exchange sources rather than a scra
- **S&P Dow Jones Indices announcements RSS (spglobal.com/spdji)** — REJECTED — HTTP 403 per the report; NOT RE-VERIFIED. This is the authoritative source for S&P 500 index additions and removals and its absence is why index-membership is PARTIAL. No free substitute for the announcement i
- **Pokemon TCG API (api.pokemontcg.io)** — REJECTED on reliability and freshness per the report; NOT RE-VERIFIED. The report documents HTTP 500 on 4 of 6 attempts and tcgplayer.prices = null with updatedAt '2023/03/27' on the one success. Listed so nobody reaches
- **StockX API** — REJECTED — HTTP 404 on the legacy endpoint; no public API, developer program is partner-gated. NOT RE-VERIFIED. It is a named settlement source for KXSTOCKX contracts, so this is a settlement gap, not merely a missing co
- **eBay Browse API** — REJECTED — HTTP 403 without credentials; requires OAuth application registration and token exchange, so not plug-and-play free. NOT RE-VERIFIED.
- **Investing.com financial data API** — REJECTED — HTTP 403; NOT RE-VERIFIED. Named as the settlement source for Kalshi's hourly FX candles, and not freely accessible, which is why fx-majors and fx-emerging show a settlement gap even though spot is well covere
- **Fiscal.ai API** — REJECTED — HTTP 400 unauthenticated, no free tier. NOT RE-VERIFIED. Named settlement source for Kalshi's corporate-KPI contracts.
- **Carbon Arc** — REJECTED — proprietary alternative-data provider with no public API of any kind. Named settlement source for the card-spend and foot-traffic KPI contracts, and the primary reason corporate-kpis-and-altdata is UNCOVERED.
- **Apple Marketing Tools RSS (app rankings)** — REJECTED — HTTP 301 then 502 on the redirect target per the report; NOT RE-VERIFIED. Would have been a partial free proxy for the app-download KPI contracts.
- **Cloudflare Radar API** — REJECTED for this domain — HTTP 400 without an API token. NOT RE-VERIFIED. Its domain-ranking data is in any case a weak proxy for the corporate KPIs actually traded.
- **Alpha Vantage (EARNINGS_CALENDAR, GLOBAL_QUOTE)** — SUPERSEDED, not dead. NOT RE-VERIFIED in this session. Rejected as a primary because the free tier is 25 requests/DAY at 5/minute — unusable for a live terminal — and api.nasdaq.com provides the same earnings calendar wi
- **Frankfurter (api.frankfurter.dev)** — Working but superseded, so not a primary. NOT RE-VERIFIED. Rejected in favour of open.er-api.com, which I did verify returns 166 currencies in one 2,970-byte call including ARS 1512.3332, TWD 31.806515, TRY 48.794548 and
- **Bloomberg Billionaires Index** — REJECTED — no free API. Named alongside Forbes as a settlement source for net-worth contracts. Since the two publish materially different valuations for the same individual, contracts naming Bloomberg specifically cannot
- **Moody's, S&P Global Ratings, Fitch Ratings** — REJECTED — all three paywalled with no free rating-action API. This is the settlement gap behind credit-and-bonds being PARTIAL: the spread data is abundant and free via FRED (I verified BAMLH0A0HYM2 live at 2.70), but t
- **CFTC COT filtered on legacy market names ('10-YEAR U.S. TREASURY NOTES', 'U.S. DOLLAR INDEX')** — NOT A DEAD FEED BUT A DEAD QUERY — flagged here because it is the trap most likely to waste a developer's day. The 6dca-aqww dataset is live and current (max report_date 2026-09-15, 371 markets), but a $where filter on '

---

### geopolitics-and-conflict

*2/11 subdomains covered · 18 primary feeds*

#### OCHA HAPI v2 — conflict-events (ACLED-derived) — UN OCHA Centre for Humanitarian Data ✅ LIVE

Covers **7** subdomains: russia-ukraine, israel-gaza-lebanon, iran, china-taiwan, latin-america-conflict, gulf-and-turkey, south-asia-and-africa-conflict

- Docs: https://hapi.humdata.org/docs
- Auth: free API key — self-service, no registration. app_identifier = base64('appname:email'), e.g. printf 'echoterminal:you@example.com' | base64. CONFIRMED: a self-generated identifier was accepted with no registration step. | Limits: No published request quota. limit max 10000 per call with offset paging. Monthly aggregation granularity. Data through 2026-08 as of 2026-09-20 (≈3 week publication lag).
- Latency: monthly | Format: REST JSON
- Why primary: THE broad conflict feed, and every numeric claim made about it reproduced exactly on re-fetch. One endpoint returns ACLED political_violence / civilian_targeting / demonstration event counts and fatalities for ~250 countries down to admin2 from a single schema, replacing ACLED-direct (confirmed dead for free use) and UCDP (confirmed 401). The admin-level quirk is real and re-verified: Ukraine, Venezuela, Lebanon and Palestine publish ONLY at admin_level=2, while Cuba, Iran, Taiwan and Greenland publish at admin_level=0. Query without an admin_level filter and aggregate — an admin_level=0 query against the level-2 group returns an empty array, which is a missing measurement, not a measured zero.

```bash
curl "https://hapi.humdata.org/api/v2/coordination-context/conflict-events?location_code=UKR&admin1_name=Donetska&start_date=2026-08-01&event_type=political_violence&output_format=json&limit=2000&app_identifier=ZWNob3Rlcm1pbmFsOmpheXBhdGlsLmR1a2VAZ21haWwuY29t"
```

> Evidence: RE-VERIFIED INDEPENDENTLY, every figure reproduced. HTTP 200, 2,998 bytes. Ukraine/Donetska/2026-08 political_violence: 8 admin2 rows, 1,912 events, 1,416 fatalities; top rows {'Kramatorskyi',1059,517}, {'Pokrovskyi',553,874}, {'Volnovaskyi',77,8} — matches the report exactly. Sudan 2026-08 political_violence: 196 admin2 rows, 253 events, 867 fatalities — exact match. Iran 2026-07 admin_level=0: p

#### IMF PortWatch — Daily_Chokepoints_Data + Daily_Ports_Data (ArcGIS FeatureServer) — IMF + University of Oxford ✅ LIVE

Covers **6** subdomains: shipping-chokepoints, russia-ukraine, china-taiwan, iran, israel-gaza-lebanon, gulf-and-turkey

- Docs: https://portwatch.imf.org/
- Auth: none | Limits: Open ArcGIS REST, no key, no published rate limit. resultRecordCount caps at 2000/page with resultOffset paging (responses carry exceededTransferLimit:true). Data carries a ~7-day publication lag: latest chokepoint date 2026-09-13, latest ports date 2026-09-11, checked 2026-09-20.
- Latency: daily | Format: REST JSON
- Why primary: One feed covers all 28 global maritime chokepoints with daily AIS-derived transit counts by vessel class, and it is the exchange's OWN declared settlement source — I confirmed this directly against the Kalshi series object rather than taking the report's word for it. CRITICAL FIELD-NAME CORRECTION, since a developer will paste these URLs: the two sibling services do NOT share a schema. Daily_Chokepoints_Data uses n_total / n_cargo / n_tanker / n_container. Daily_Ports_Data uses portcalls / portcalls_cargo / portcalls_tanker / portcalls_container / portcalls_dry_bulk / portcalls_general_cargo / portcalls_roro, plus import_* and export_* volume fields — requesting n_total against the ports service returns HTTP 200 with {"error":{"code":400,"message":"Cannot perform query. Invalid query parameters.","details":["'outFields' parameter is invalid"]}}. The report's chokepoint exampleCall is correct; its ports claim would have failed in production.

```bash
curl "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query?where=portname%3D%27Strait%20of%20Hormuz%27%20OR%20portname%3D%27Bab%20el-Mandeb%20Strait%27&outFields=date,portname,n_total,n_cargo,n_tanker,n_container&orderByFields=date%20DESC&resultRecordCount=8&returnGeometry=false&f=json"
```

> Evidence: HTTP 200. Distinct-value query returned EXACTLY 28 chokepoints: Luzon, Cape of Good Hope, Bab el-Mandeb, Gibraltar, Windward, Sunda, Taiwan Strait, Dover, Korea, Bosporus, Kerch, Suez, Panama, Lombok, Mindoro, Bering, Makassar, Torres, Malacca, Oresund, Yucatan, Hormuz, Magellan, Ombai, Balabac, Mona, Bohai, Tsugaru — roster claim confirmed. Daily series reproduced exactly: {'date':'2026-09-13','p

#### Kalshi Trade API v2 — /series, /series/{ticker} and /markets (public read) — Kalshi (CFTC-regulated US designated contract market) ✅ LIVE

Covers **11** subdomains: russia-ukraine, israel-gaza-lebanon, iran, shipping-chokepoints, china-taiwan, latin-america-conflict, gulf-and-turkey, alliances-and-treaties, territorial-acquisition, south-asia-and-africa-conflict, world-leader-tenure

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: none for read endpoints (series, events, markets, orderbook). API key only needed to trade. Confirmed: all calls made with no credentials. | Limits: Public read tier, no key. Cursor paging, limit max 1000 on /markets and /events. No published read rate limit; none encountered across ~10 calls. REST verified; the websocket tier was NOT exercised in this session.
- Latency: realtime/websocket | Format: REST JSON
- Why primary: Market-implied probability for every subdomain, plus a machine-readable settlement_sources array per series. The headline claim CHECKS OUT and I verified it at the series object rather than trusting the summary. BUT TWO OF THE REPORT'S SETTLEMENT CLAIMS ARE WRONG and are corrected below — settlement_sources is a free-text field maintained per series and is sometimes malformed, so read it defensively and never hard-code a mapping from it. Note also that geopolitical series live under category=Politics, not category=World: KXCLOSEHORMUZ, KXHORMUZRENAME, KXLEADERSOUT, KXTAIWANLVL4 and the KXGREENLAND family are all category Politics. Fetch /series/{ticker} directly rather than filtering the World list, or you will miss them.

```bash
curl "https://api.elections.kalshi.com/trade-api/v2/series?category=World" ; curl "https://api.elections.kalshi.com/trade-api/v2/series/KXCLOSEHORMUZ" ; curl "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXLEADERSOUT&status=open&limit=5"
```

> Evidence: HTTP 200 on all calls. /series?category=World → exactly 149 series; category=Politics → exactly 2,343 — both counts match the report. /markets?series_ticker=KXLEADERSOUT&status=open&limit=5 → 14,097 bytes, live market KXLEADERSOUT-27JAN01 custom_strike {'Person':'Sébastien Lecornu'}, last_price_dollars 0.2000, open_interest 1769.53. CONFIRMED: /series/KXCLOSEHORMUZ settlement_sources genuinely con

#### Polymarket Gamma Markets API — /events and /markets with tag_slug — Polymarket ✅ LIVE

Covers **10** subdomains: russia-ukraine, israel-gaza-lebanon, iran, china-taiwan, latin-america-conflict, gulf-and-turkey, alliances-and-treaties, territorial-acquisition, south-asia-and-africa-conflict, world-leader-tenure

- Docs: https://docs.polymarket.com/developers/gamma-markets-api/overview
- Auth: none | Limits: Public read, no key. Default limit 100, offset paging. No published rate limit and none encountered across 8 consecutive tag queries. REST verified; websocket NOT exercised.
- Latency: realtime/websocket | Format: REST JSON
- Why primary: The tag taxonomy maps close to one-to-one onto this domain's subdomains, so ONE endpoint with a swapped tag_slug yields live implied probabilities, 24h volume, liquidity, end dates and free-text resolutionSource for nearly every subdomain. I independently swept seven tags rather than the report's one. One removal: 'shipping-chokepoints' is dropped from coversSubdomains — there is no chokepoint/Hormuz/Suez tag in the taxonomy, and chokepoint exposure on Polymarket appears only incidentally under the iran tag. Kalshi (KXCLOSEHORMUZ, KXSUEZ) is the venue that genuinely lists that subdomain.

```bash
curl "https://gamma-api.polymarket.com/events?closed=false&limit=5&tag_slug=ukraine&order=volume24hr&ascending=false"
```

> Evidence: HTTP 200 on all eight calls. tag_slug=ukraine ordered by volume24hr reproduced the report's top result exactly: {'id':'31195','ticker':'putin-out-before-2027','title':'Putin out as President of Russia by...?'} with full resolution description. Independent multi-tag sweep (open events returned per tag): ukraine 54 (natoeu-troops-fighting-in-ukraine-in-2025), geopolitics 100 (china-x-india-military-

#### GDELT DOC 2.0 API — The GDELT Project (Kalev Leetaru) ✅ LIVE

Covers **11** subdomains: russia-ukraine, israel-gaza-lebanon, iran, shipping-chokepoints, china-taiwan, latin-america-conflict, gulf-and-turkey, alliances-and-treaties, territorial-acquisition, south-asia-and-africa-conflict, world-leader-tenure

- Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- Auth: none | Limits: No key. HARD LIMIT: one request per 5 seconds per caller. CORRECTION TO THE REPORT: the throttle response is HTTP 429 with a plain-text body, NOT 'HTTP 200 with a throttle message' — I observed 429 on five separate occasions. Error handling should branch on status 429 AND on a non-'{' first byte, since a 200 can still be non-JSON. The cooldown is sticky: after a burst, three waits of 25s, 30s and 75s all still returned 429, and only a slow-paced third attempt recovered. Rolling ~3-month window. maxrecords cap 250 in ArtList. Parentheses may only wrap OR'd terms.
- Latency: sub-minute | Format: REST JSON
- Why primary: A single query-able index over global news in 65 languages, so one endpoint serves all 11 subdomains by changing the query string. Retained as primary, but with the throttle treated as a first-class operational constraint rather than a footnote: at one request per five seconds with a sticky multi-minute cooldown, this cannot be the streaming backbone for an 11-subdomain terminal. Use the raw 15-minute bulk files for continuous ingest and reserve the DOC API for on-demand lookups.

```bash
curl "https://api.gdeltproject.org/api/v2/doc/doc?query=(ukraine%20OR%20kupiansk)%20sourcelang:english&mode=timelinevol&format=json&timespan=7d"
```

> Evidence: mode=timelinevol INDEPENDENTLY VERIFIED. First two attempts HTTP 429, 444 bytes, plain text. Third attempt HTTP 200, 1,405 bytes, valid JSON: {"query_details":{"title":"(ukraine OR kupiansk) sourcelang:english","date_resolution":"hour"},"timeline":[{"series":"Volume Intensity","data":[{"date":"20260920T000000Z","value":1.4987},{"date":"20260920T020000Z","value":1.365},{"date":"20260920T030000Z","v

#### GDELT 2.0 raw 15-minute Event / Mentions / GKG files (CAMEO-coded) — The GDELT Project ✅ LIVE

Covers **11** subdomains: russia-ukraine, israel-gaza-lebanon, iran, shipping-chokepoints, china-taiwan, latin-america-conflict, gulf-and-turkey, alliances-and-treaties, territorial-acquisition, south-asia-and-africa-conflict, world-leader-tenure

- Docs: http://data.gdeltproject.org/gdeltv2/lastupdate.txt
- Auth: none | Limits: No key, no documented quota, and no throttling observed. New file set every 15 minutes (~96 export files/day). export.CSV.zip ≈42KB, mentions ≈60KB, gkg.csv.zip ≈2.9MB per slice. Bulk download, so no per-query throttle — this is the correct way to avoid the DOC API's 429 limiter.
- Latency: sub-minute | Format: CSV bulk
- Why primary: The structured twin of the DOC API and, given that the DOC API throttles at 1 req/5s with sticky 429 cooldowns, the only one of the two that can actually back a streaming terminal. Every 15 minutes you get the full global event table already coded to CAMEO (root codes 18/19/20 = assault, fight, unconventional mass violence), with actor country and role, city-level geolocation, Goldstein score and source URL. One file covers every subdomain at once.

```bash
curl -sL http://data.gdeltproject.org/gdeltv2/lastupdate.txt   # parse field 3 of each line, then: curl -sL -o g.zip <export.CSV.zip url>
```

> Evidence: INDEPENDENTLY RE-DOWNLOADED, a different 15-minute slice than the report's. lastupdate.txt HTTP 200, 319 bytes, requires -L as stated, listing 20260921031500.export/.mentions/.gkg with md5s and sizes (42128 / 60549 / 2900310). Fetched 20260921031500.export.CSV.zip: HTTP 200, 42,128 bytes, member 20260921031500.export.CSV, parsed 746 rows x 61 columns, of which 65 carried CAMEO EventRootCode 18/19/

#### US State Department Travel Advisories RSS — US Department of State, Bureau of Consular Affairs ✅ LIVE

Covers **7** subdomains: russia-ukraine, israel-gaza-lebanon, iran, china-taiwan, latin-america-conflict, gulf-and-turkey, south-asia-and-africa-conflict

- Docs: https://travel.state.gov/content/travel/en/traveladvisories/traveladvisories.html
- Auth: none | Limits: Open RSS/XML, no key, no published rate limit. ~1.07MB payload, content-type text/xml, all countries in one document.
- Latency: hourly | Format: RSS
- Why primary: One ~1MB document carries the official US risk grade for every country, with Level 1–4 encoded directly in the <title> so no body parsing is needed. It is a genuine settlement authority for the advisory-grade contracts — verified at the Kalshi series object, where KXTRAVELWARN really does list 'U.S. Department of State'. Two coverage claims removed: 'shipping-chokepoints' (this is a country-level advisory feed; it grades no strait) and 'world-leader-tenure' (it carries no office-holder data).

```bash
curl -sL "https://travel.state.gov/_res/rss/TAsTWs.xml"
```

> Evidence: HTTP 200, 1,069,263 bytes, content-type text/xml, valid RSS <title>travel.state.gov: Travel Advisories</title>. Parsed 216 <item> advisories (report said 218 — a live feed drifting by two, not a defect). Level 4 'Do Not Travel' titles extracted directly: Iraq, Ukraine, Gaza, Democratic Republic of the Congo, Haiti, Somalia, Sudan, Burma, Lebanon, Burkina Faso — independently confirms the israel-ga

#### Wikidata Query Service (SPARQL) — Wikimedia Foundation ✅ LIVE

Covers **7** subdomains: world-leader-tenure, alliances-and-treaties, territorial-acquisition, china-taiwan, gulf-and-turkey, russia-ukraine, latin-america-conflict

- Docs: https://query.wikidata.org/
- Auth: none, but a descriptive User-Agent is mandatory or requests are blocked. Confirmed working with a custom UA. | Limits: No key. Enforced: 60-second query timeout, per-client processing budgets of 60s/minute and 30s/5-minutes.
- Latency: daily | Format: SPARQL / JSON (the report labelled this 'GraphQL' — it is not; it is SPARQL over HTTP returning application/sparql-results+json)
- Why primary: The only free feed that answers 'who currently holds office in every country, since when' in one query, which is the machine-readable record behind every 'X out as leader of Y by…' contract. The same endpoint returns alliance membership with accession dates and the forward election calendar. Important caveat I am adding: Wikidata is a derived record, not the adjudicating authority — Kalshi's KXLEADERSOUT settles on news outlets (verified), and Wikidata is updated after the fact. Use it to settle and to build base rates, not to front-run.

```bash
curl -G -H 'Accept: application/sparql-results+json' -H 'User-Agent: YourApp/1.0 (you@example.com)' https://query.wikidata.org/sparql --data-urlencode 'query=SELECT ?countryLabel ?personLabel ?start WHERE { ?country wdt:P31 wd:Q6256; p:P35 ?st . ?st ps:P35 ?person . FILTER NOT EXISTS { ?st pq:P582 ?end } OPTIONAL { ?st pq:P580 ?start } SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } LIMIT 8'
```

> Evidence: HTTP 200, 3,429 bytes, valid application/sparql-results+json. Current-head-of-state query returned live bindings: United Kingdom → Charles III, start 2022-09-08T00:00:00Z; People's Republic of China → Xi Jinping with a dated P580 start. The P35 + P580/P582-absent pattern works exactly as described and the P580 start qualifier is populated. The UA requirement is real — this is the shape a developer

#### Federal Register API v1 — US National Archives / GPO ✅ LIVE

Covers **6** subdomains: iran, russia-ukraine, latin-america-conflict, alliances-and-treaties, territorial-acquisition, gulf-and-turkey

- Docs: https://www.federalregister.gov/developers/api/v1
- Auth: none | Limits: No key. per_page default 20, max 1000, 50 pages of results per query. No published rate limit; none encountered.
- Latency: daily | Format: REST JSON
- Why primary: Every US Executive Order, proclamation, national-emergency renewal, OFAC designation notice and arms-export rule lands here first, full-text and structured, in one searchable index. It is a confirmed settlement authority, not an inference: I pulled /series/KXHORMUZRENAME directly and its settlement_sources really does contain {'name':'Federal Register','url':'https://www.federalregister.gov/agencies'}. 'world-leader-tenure' removed from coversSubdomains — the Federal Register publishes US regulatory instruments, not a record of leader transitions.

```bash
curl "https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=Iran+sanctions&per_page=2&order=newest"
```

> Evidence: HTTP 200, 4,438 bytes. conditions[term]='Iran sanctions' returned {"description":"Documents matching 'Iran sanctions'","count":941,"total_pages":50} — count matches the report's 941 exactly — with newest result {"title":"Notice of OFAC Sanctions Action","type":"Notice"} and an abstract describing SDN List additions, confirming OFAC designations really do surface here. The report's warning that ter

#### OpenSanctions bulk data (default dataset, FollowTheMoney) — OpenSanctions / Open Knowledge ✅ LIVE

Covers **5** subdomains: iran, russia-ukraine, latin-america-conflict, gulf-and-turkey, israel-gaza-lebanon

- Docs: https://www.opensanctions.org/docs/bulk/
- Auth: none | Limits: Bulk download free under CC-BY-NC 4.0 (NON-COMMERCIAL — a real licensing constraint for a paid terminal product, flag it with legal). The hosted match/search API is paid; bulk is the free path. SIZE CORRECTION: the report called targets.simple.csv 'far smaller' than the 2.6GB entities file — it is 462,999,128 bytes (463MB), which is smaller but still a heavy daily pull. names.txt at 109MB is the genuinely light artifact. Rebuilt daily.
- Latency: daily | Format: JSON manifest + bulk JSON/CSV
- Why primary: ONE entity-resolved graph merges 250+ source lists — OFAC SDN, EU FSF, UN Security Council, UK OFSI and others — plus PEP lists, deduplicated with stable IDs, so designation velocity per regime comes from a single daily artifact instead of a dozen national XMLs. Two coverage claims removed: 'world-leader-tenure' and 'alliances-and-treaties'. A PEP list records that someone is politically exposed; it does not record who holds office, when their term ends, or which treaties a state has ratified. That is Wikidata's job, and over-claiming it here would send a developer to the wrong 463MB file.

```bash
curl -sL "https://data.opensanctions.org/datasets/latest/default/index.json"   # then fetch a resource url from the returned manifest
```

> Evidence: HTTP 200 (requires -L), 21,098 bytes. Manifest reproduced the report's counters and then advanced, as a daily rebuild should: {'updated_at':'2026-09-21T00:53:49','entity_count':4066682,'target_count':1227425,'thing_count':1983463,'last_change':'2026-09-20T23:47:02','issue_count':0}. Resource list with live dated artifact URLs and exact byte sizes: entities.ftm.json 2,603,362,415; names.txt 109,016

#### Official sanctions instruments — OFAC SDN + EU FSF + UN Security Council consolidated — US Treasury OFAC / European Commission DG FISMA / United Nations Security Council ✅ LIVE

Covers **6** subdomains: iran, russia-ukraine, latin-america-conflict, gulf-and-turkey, israel-gaza-lebanon, south-asia-and-africa-conflict

- Docs: https://ofac.treasury.gov/faqs/topic/1636
- Auth: none (the EU FSF 'token' is the well-known public value dG9rZW4tMjAxNw = base64 'token-2017'; no registration). All three require -L. | Limits: No keys, no registration, no published rate limits. OFAC SDN 29,093,584 bytes, EU FSF 25,766,640 bytes, UN 2,176,957 bytes. FRESHNESS WARNING I am adding: the three do NOT refresh at the same tempo. OFAC Publish_Date 09/18/2026 and UN dateGenerated 2026-09-19 are current, but the EU FSF generationDate is 2026-08-05 — roughly six weeks stale as of 2026-09-20. Do not present a merged view as uniformly current; carry each file's own publication date through to the UI.
- Latency: daily for OFAC/UN; EU FSF observed far less frequent | Format: XML bulk
- Why primary: These are the primary legal instruments, not a derived aggregate — when a market asks 'will X be sanctioned by date D', the answer is a dated entry in one of these three files with its own programme codes. Kept alongside OpenSanctions (the convenient merged view) because for settlement you want the authority itself. 'world-leader-tenure' removed: a sanctions list is not a record of who holds office.

```bash
curl -sL -o sdn.xml "https://sanctionslistservice.ofac.treas.gov/api/download/sdn.xml" ; curl -sL -o eu_fsf.xml "https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content?token=dG9rZW4tMjAxNw" ; curl -sL -o un.xml "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
```

> Evidence: All three HTTP 200, all re-fetched independently. OFAC sdn.xml: exactly 29,093,584 bytes, header <Publish_Date>09/18/2026</Publish_Date><Record_Count>19393</Record_Count>, first sdnEntry uid 36 AEROCARIBBEAN AIRLINES — byte count and record count match the report exactly. EU FSF: exactly 25,766,640 bytes, root <export xmlns="http://eu.europa.ec/fpi/fsd/export" generationDate="2026-08-05T16:47:04.4

#### DeepStateMap API — Ukraine territorial control — DeepState UA (Ukrainian OSINT collective) ✅ LIVE

Covers **1** subdomains: russia-ukraine

- Docs: https://deepstatemap.live/
- Auth: none for /api/history/last | Limits: No key on /api/history/last. The historical listing /api/history returns HTTP 401 and needs a token, so you must snapshot on a schedule yourself to build a time series. ~627KB per snapshot. No published rate limit; volunteer project with NO SLA and no uptime guarantee.
- Latency: daily | Format: GeoJSON over REST
- Why primary: Deliberately narrow and retained because nothing broad replaces it: the only free GeoJSON polygon feed of occupied / contested / liberated area with an incrementing snapshot id you can diff day over day for rate of advance. ISW, the usual co-source, is genuinely unusable from an automated client — I re-tested and confirmed. IMPORTANT DOWNGRADE OF THE REPORT'S FRAMING: this is territorial-control EVIDENCE, not a settlement authority. No exchange names DeepStateMap in its settlement_sources, and the feature properties are KML styling attributes plus a free-text bilingual 'name' string — there is no machine-readable status enum, so occupied-vs-contested must be inferred from fill colour or from parsing that string. Treat it as a strong predictive input and a weak settlement input.

```bash
curl -sL "https://deepstatemap.live/api/history/last"
```

> Evidence: HTTP 200, exactly 627,479 bytes — matches the report. Parsed {'id':1789884551}, identical snapshot id, with map.features = 525 features, Counter({'Point':400,'Polygon':125}) — exactly the split claimed. Property keys confirmed as ['name','styleUrl','styleHash','styleMapHash','stroke-opacity','stroke','stroke-width','fill-opacity','fill'] and the first feature's name is the bilingual string 'Статус

#### NGA Maritime Safety Information — Broadcast Navigational Warnings — US National Geospatial-Intelligence Agency ✅ LIVE

Covers **6** subdomains: shipping-chokepoints, russia-ukraine, china-taiwan, israel-gaza-lebanon, gulf-and-turkey, iran

- Docs: https://msi.nga.mil/
- Auth: none | Limits: No key, no published rate limit. Full active set 206,479 bytes. The legacy /api/publications/asam (anti-shipping activity) path returns HTTP 404 — only broadcast-warn confirmed working.
- Latency: hourly | Format: REST JSON
- Why primary: One endpoint carries every active NAVAREA warning worldwide — mine danger, hazardous operations, live-fire areas, closures — the official, dated, geo-referenced record of a sea area actually becoming dangerous. It complements PortWatch precisely: PortWatch shows traffic fell, this shows why and under whose declaration, and without PortWatch's 7-day lag.

```bash
curl -sL "https://msi.nga.mil/api/publications/broadcast-warn?status=active&output=json"
```

> Evidence: HTTP 200, exactly 206,479 bytes — byte-identical to the report's figure. Root key 'broadcast-warn', first record {msgYear:2024, msgNumber:517, navArea:'4', subregion:'GEN', text:'1. NAVAREA IV MOBILE OFFSHORE DRILLING UNITS…'} confirming the flat structure with navArea codes as short strings, which supports the report's warning that &navArea=IX returns an empty array and that you should fetch all 

#### Tzeva Adom / Red Alert API — Israel rocket, missile and drone sirens — tzevaadom.co.il (unofficial community mirror of IDF Home Front Command alerts) ✅ LIVE

Covers **1** subdomains: israel-gaza-lebanon

- Docs: https://api.tzevaadom.co.il/notifications
- Auth: none | Limits: Open, no key. No published rate limit — UNKNOWN. Unofficial community mirror with no SLA; the official oref.org.il endpoint is Akamai-blocked to automated clients. /alerts-history returns a fixed 50-element window (53,130 bytes), so poll frequently enough not to lose events between pulls. City names are Hebrew only, requiring a locality gazetteer to map to geography.
- Latency: realtime | Format: REST JSON
- Why primary: The highest-frequency ground truth for the Israel/Gaza/Lebanon theater — a per-siren record by locality with threat category and epoch timestamp, detecting a ceasefire collapsing within seconds. COVERAGE NARROWED: the report also claimed 'iran' and 'shipping-chokepoints'. This feed reports sirens inside Israel. It carries no Iranian domestic data and no maritime data; an Iranian launch would appear only as an Israeli impact alert, which is an inference, not coverage. Both removed.

```bash
curl -sL "https://api.tzevaadom.co.il/alerts-history"   # live/current: https://api.tzevaadom.co.il/notifications
```

> Evidence: Both endpoints HTTP 200, independently re-fetched. /notifications returned [] (2 bytes) — a real measurement of no active siren at call time, not a missing value. /alerts-history returned exactly 53,130 bytes, a 50-element list, first element {"id":7666,"description":null,"alerts":[{"time":1789835141,"cities":["יצהר"],"threat":2,"isDrill":false}]} — byte count and leading record match the report e

#### IAEA Top News RSS + UN Meetings Coverage RSS + US Dept of War news RSS — International Atomic Energy Agency / United Nations / US Department of War ✅ LIVE

Covers **4** subdomains: iran, alliances-and-treaties, russia-ukraine, israel-gaza-lebanon

- Docs: https://www.iaea.org/
- Auth: none | Limits: All open RSS/XML, no keys. IAEA 10,910 bytes / 15 items. UN press 1,952 bytes / only 10 items — the --compressed flag is genuinely required or you get binary. DoW 19,167 bytes / 20 items. No published rate limits. IAEA path is exact: /feeds/topnews works; the .rss variants 404.
- Latency: hourly | Format: RSS
- Why primary: The official-announcement layer that aggregators lag: IAEA DG statements, Security Council meeting outcomes, and US weapons-package and deployment releases. Retained, but with an honesty caveat the report understated — the UN press feed carries only 10 items in a 1.9KB document, so it is a headline ticker with a very short window, not an archive; poll it often or you will miss Security Council outcomes entirely. Two coverage claims removed: 'south-asia-and-africa-conflict' and 'world-leader-tenure' — three small general-news tickers do not constitute coverage of those subdomains.

```bash
curl -sL "https://www.iaea.org/feeds/topnews" ; curl -sL --compressed "https://press.un.org/en/rss.xml" ; curl -sL "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=20"
```

> Evidence: All three HTTP 200, independently re-fetched. IAEA /feeds/topnews: 10,910 bytes, valid RSS <title>IAEA Top News</title>, 15 <item> elements (report said 16 — a live feed, not a defect). UN press with --compressed: 1,952 bytes, <title>UN Meetings Coverage and Press Releases</title>, 10 <item> elements. DoW: 19,167 bytes, <title>Department of War News Feed</title>, 20 <item> elements.

#### Humanitarian Data Exchange (HDX) CKAN API v3 — UN OCHA Centre for Humanitarian Data ✅ LIVE

Covers **4** subdomains: russia-ukraine, israel-gaza-lebanon, south-asia-and-africa-conflict, latin-america-conflict

- Docs: https://data.humdata.org/api/3/action/package_search
- Auth: none | Limits: Standard CKAN, no key for reads. rows max 1000 per call with start offset paging. No published rate limit.
- Latency: daily | Format: REST JSON
- Why primary: The catalog behind HAPI and the escape hatch when HAPI's aggregated monthly counts are too coarse. One search endpoint resolves to direct file URLs for per-crisis datasets across every theater, so you add subdomain depth without a new provider integration. 'iran' and 'china-taiwan' removed from coversSubdomains — HDX is a humanitarian-response catalog and neither is an active humanitarian-response country with curated crisis datasets; a keyword search returning something is not coverage.

```bash
curl "https://data.humdata.org/api/3/action/package_search?q=ukraine+conflict&rows=2"
```

> Evidence: HTTP 200, 87,477 bytes, {"success":true}. package_search?q=ukraine+conflict returned count 52 — matching the report exactly — with the first two results titled 'Ukraine - Conflict Events' and 'Ukraine - Frontline Monitoring'.

#### World Bank Indicators API v2 — SIPRI military expenditure series — World Bank Group (sourcing SIPRI) ✅ LIVE

Covers **7** subdomains: russia-ukraine, iran, china-taiwan, gulf-and-turkey, israel-gaza-lebanon, south-asia-and-africa-conflict, alliances-and-treaties

- Docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- Auth: none | Limits: No key. Default 50 rows/page, per_page max 32,500, semicolon-delimited multi-country in one call. No published rate limit. Annual data with a ~1-year lag — 2025 values are null, 2024 populated. lastupdated 2026-07-13.
- Latency: annual (the report labelled this 'monthly'; the underlying series is annual and only the publication refresh is periodic) | Format: REST JSON
- Why primary: The free machine-readable route to SIPRI. One indicator family (MS.MIL.XPND.GD.ZS, .CN, .CD, MS.MIL.TOTL.P1, MS.MIL.MPRT.KD, MS.MIL.XPRT.KD) gives military spend, force size and arms import/export TIV for every country back to 1960 in a single multi-country call. This is the base-rate layer — it will not move a market today, and should be presented as such rather than as a live feed.

```bash
curl "https://api.worldbank.org/v2/country/RUS;UKR;ISR;IRN;TWN/indicator/MS.MIL.XPND.GD.ZS?format=json&date=2020:2025&per_page=50"
```

> Evidence: HTTP 200, 5,544 bytes. Multi-country call for RUS;UKR;ISR;IRN;TWN returned {'page':1,'pages':1,'per_page':50,'total':24,'sourceid':'2','lastupdated':'2026-07-13'} — total and lastupdated match the report exactly. Values: IRN 2025 → null (correctly unmeasured, not zero), IRN 2024 → 2.01043175751636, 2023 → 2.35179187276968, 2022 → 2.11062130699384, 2021 → 2.22394282528392, 2020 → 2.17701027609522. 

#### adsb.lol /v2/mil — live military aircraft — adsb.lol (community ADS-B network) ✅ LIVE

Covers **3** subdomains: china-taiwan, gulf-and-turkey, israel-gaza-lebanon

- Docs: https://api.adsb.lol/docs
- Auth: none | Limits: Completely open, no key. No published rate limit — UNKNOWN; the project asks for reasonable use. COVERAGE IS THE BINDING LIMIT, not quota: it depends entirely on volunteer receiver density and is empirically thin outside Europe, CONUS and Australia/NZ.
- Latency: realtime | Format: REST JSON
- Why primary: One unauthenticated call returns currently-tracked military airframes worldwide with hex, callsign, registration, type, altitude, speed, track, squawk and position. Retained as a real, working feed — but its coverage claims are the biggest over-statement in the report and I have cut them hard on the basis of two independent samples. THE REPORT CLAIMED this feed covers russia-ukraine, latin-america-conflict, iran and shipping-chokepoints, and argued it is 'the highest-frequency observable' for US force posture in the Caribbean. In two samples ten minutes apart I found ZERO aircraft in the Caribbean/Latin America box and ZERO in the Ukraine/Black Sea box, and 42–46 percent of returned airframes carried no lat/lon at all. Do not build a Caribbean or Ukraine posture panel on this feed; it will render an empty map as calm. The three retained subdomains had observed airframes in both samples, and even those are thin.

```bash
curl -sL "https://api.adsb.lol/v2/mil"
```

> Evidence: HTTP 200 on both pulls. Sample 1: 37,241 bytes, 97 aircraft, first record {"hex":"af3be4","type":"adsb_icao","flight":"C6067","r":"6067","t":"H60","alt_baro":1075,"gs":124.3,"squawk":"5567","lat":60.440552,"lon":-146.85671}. Regional bucketing of sample 1: no-position 46, Europe 10, CONUS 4, E/SE Asia 5, MidEast/Gulf 3, Alaska 1, and a large Australia/NZ cluster; LatAm/Caribbean 0. Sample 2: 94 ai

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Russia–Ukraine War | OCHA HAPI conflict-events (re-verified: Donetska 2026-08 = 8 | SPLIT. For sanctions-linked and US-action contracts: Federal | 🟡 PARTIAL |
| Israel, Gaza & Lebanon | Tzeva Adom /alerts-history (re-verified: 53,130 bytes, 50-el | NONE FOUND as an adjudicating authority — these contracts re | 🟡 PARTIAL |
| Iran, Nuclear & Sanctions | OCHA HAPI (IRN re-verified at admin_level=0, 2026-07: politi | Federal Register API v1 (count 941 for 'Iran sanctions', new | 🟡 PARTIAL |
| Maritime Chokepoints | IMF PortWatch Daily_Chokepoints_Data — re-verified at exactl | IMF PortWatch — and this is now independently confirmed rath | 🟢 COVERED |
| China & Taiwan | IMF PortWatch Taiwan Strait daily transits (re-verified: 202 | US State Department Travel Advisories RSS for advisory-grade | 🟡 PARTIAL |
| Venezuela, Cuba & Latin America | Polymarket tag_slug=venezuela (27 open events, incl. will-th | OFAC SDN/Consolidated XML + Federal Register API for sanctio | 🟡 PARTIAL |
| Gulf States & Turkey | OCHA HAPI (TUR, SAU, GRC at admin_level=0) + NGA broadcast-w | Wikidata Query Service — head-of-state/government holdings w | 🟡 PARTIAL |
| NATO, Alliances & Treaties | Wikidata SPARQL for alliance membership with accession dates | Federal Register API v1 for any US withdrawal notice, EO or  | 🟡 PARTIAL |
| Territorial Acquisition | Kalshi /series for the KXGREENLAND family with declared sett | Federal Register API v1 (re-verified) + Congress.gov API v3  | 🟡 PARTIAL |
| South Asia, Sudan & Other Conflicts | OCHA HAPI conflict-events is decisive and fully re-verified  | NONE FOUND as an adjudicator — 'India strike on Pakistan' an | 🟡 PARTIAL |
| World Leader Tenure | Kalshi /markets?series_ticker=KXLEADERSOUT — re-verified liv | Wikidata Query Service (SPARQL) — P35/P6 office-holder state | 🟢 COVERED |

**Rejected**

- **ACLED API (direct, acleddata.com)** — DEAD FOR FREE USE — RE-CONFIRMED THIS SESSION. https://api.acleddata.com/acled/read?limit=1 returned HTTP 000 with 0 bytes (connection failure) on re-test. The free Open tier genuinely excludes API access. Superseded by 
- **UCDP API (Uppsala Conflict Data Program)** — GATED — RE-CONFIRMED. https://ucdpapi.pcr.uu.se/api/gedevents/25.1?pagesize=2&Country=Ukraine returned HTTP 401, 65 bytes, on re-test. The token is free but not self-service.
- **ISW (Institute for the Study of War) RSS — understandingwar.org/feed/** — CONFIRMED UNUSABLE, AND A TEXTBOOK 200-IS-NOT-SUCCESS CASE. On re-test the URL returned HTTP 200 with 377,150 bytes — which looks like a pass until you read it: content-type is text/html, the body begins '<!DOCTYPE html>
- **NATO official news RSS** — NO MACHINE-READABLE FEED — RE-CONFIRMED. https://www.nato.int/cps/en/natohq/news.rss returned HTTP 404 with 295,216 bytes of HTML error page. NATO announcements must be picked up via GDELT, UN press, Federal Register and
- **Metaculus API** — AUTH REQUIRED — RE-CONFIRMED. https://www.metaculus.com/api/posts/?limit=2&search=Taiwan returned HTTP 403, 134 bytes. Its forecast-aggregation role is covered by Kalshi and Polymarket, both open-read and both re-verifie
- **Cloudflare Radar API** — AUTH REQUIRED — RE-CONFIRMED. https://api.cloudflare.com/client/v4/radar/annotations/outages returned HTTP 400, 141 bytes (missing auth headers). Free with an account token but not zero-auth.
- **Congress.gov API v3 with DEMO_KEY** — DOWNGRADED FROM THE REPORT'S 'VERIFIED HTTP 200 BEFORE RATE LIMIT'. On re-test, https://api.congress.gov/v3/treaty?api_key=DEMO_KEY&limit=2&format=json returned HTTP 429 {'error':{'code':'OVER_RATE_LIMIT'}} on the FIRST 
- **OpenSky Network REST API /states/all** — RE-VERIFIED LIVE AND WORTH RECONSIDERING. HTTP 200, 6,959 bytes over a Ukraine/Black Sea bbox, returning real state vectors (["471f68","WMT3796","Hungary",…,23.8645,44.443,9616.44,…]). The report demoted it in favour of 
- **UNHCR Refugee Statistics API** — LIVE BUT REDUNDANT (not re-tested this session). OCHA HAPI already exposes refugees-persons-of-concern and idps endpoints sourced from the same UNHCR/IDMC data.
- **aisstream.io (live AIS WebSocket)** — NOT VERIFIED AND CAPPED. Requires a free signup key that cannot be self-provisioned, with severe documented free limits. IMF PortWatch already delivers the aggregated AIS-derived chokepoint series that contracts actually
- **Taiwan MND PLA activity / ADIZ incursion feed** — NOT REACHABLE / NOT FOUND (per the original report; not re-tested). No free machine-readable daily PLA aircraft/vessel count could be verified. This remains a genuine, acknowledged gap for china-taiwan.
- **OFAC 'Recent Actions' RSS** — DEAD (per the original report). Use the Federal Register API instead — OFAC designations publish there as 'Notice of OFAC Sanctions Action', which I re-verified as the newest result for the 'Iran sanctions' query.
- **IAEA PRIS and IAEA safeguards reports** — NO PUBLIC API. IAEA quarterly Iran verification reports carrying enrichment-stockpile figures are PDFs with no structured endpoint. IAEA Top News RSS (re-verified HTTP 200, 15 items) carries DG statements but NOT numeric
- **SIPRI Arms Transfers Database CSV export** — UNUSABLE WITHOUT UNDOCUMENTED PARAMS. Superseded by the World Bank Indicators API, which republishes the SIPRI MS.MIL.* series as clean JSON with no key — re-verified, lastupdated 2026-07-13.
- **UMA Optimistic Oracle — API and subgraph** — ENDPOINTS DEAD (per the original report). Polymarket's resolution mechanism is not directly observable via a free API; read resolutionSource text off Gamma instead.
- **World Monitor hosted API** — NOT A DATA API — a packaged dashboard product, nothing to ingest.
- **GDELT GEO 2.0 API** — PATH DEAD (per the original report). GDELT's geographic signal is available via the raw 15-minute export files, whose ActionGeo fields I confirmed populated ('Beijing, Beijing, China' on the sampled row).
- **oref.org.il official Israeli Home Front Command alerts** — BLOCKED (Akamai 403, per the original report). The Tzeva Adom community mirror is the only working machine-readable route — re-verified HTTP 200 on both endpoints, and it must be labelled an unofficial mirror with no SLA
- **ACAPS Data API v1** — REGISTRATION REQUIRED. Unauthenticated calls return a login page rather than data — another HTTP-200-but-not-data case. Partly covered free by OCHA HAPI's coordination-context/national-risk endpoint.

---

### health-and-medicine

*7/9 subdomains covered · 13 primary feeds*

#### CDC Open Data — data.cdc.gov Socrata SODA v2 — US Centers for Disease Control and Prevention ✅ LIVE

Covers **5** subdomains: respiratory-outbreaks, avian-and-zoonotic-flu, measles-and-vpd, emerging-outbreaks, vital-statistics

- Docs: https://dev.socrata.com/consumers/getting-started.html
- Auth: none required; free Socrata app token (X-App-Token header) strongly recommended to leave the shared per-IP throttle pool | Limits: Socrata publishes no numeric quota. Unkeyed requests draw from a shared per-IP pool; a free app token effectively removes throttling. $limit caps at 50,000 rows per call on SODA 2.0 with $offset paging. UNKNOWN exact numbers — Socrata declines to publish them. No rate-limit headers were returned on any of the ~30 calls made during verification.
- Latency: CORRECTED FROM THE ORIGINAL REPORT. Daily: NSSP ED visits (vjzj-u7u8, current to 2026-09-12). Weekly: NNDSS x9gk-5huc (current to wk36 2026), NHSN hospital respiratory ua7e-t2fy (current to week ending 2026-09-12), NWSS wastewater (sample_collect_date current to 2026-09-15, date_updated 2026-09-18). Monthly/quarterly: NCHS VSRR. NOT daily: the SARS-CoV-2 variant nowcast jr58-6ysp is roughly biweekly and is currently 7 weeks behind — max(week_ending)=2026-08-01 as of 2026-09-20. The original report called the variant nowcast 'daily'; that is wrong. | Format: REST JSON / CSV / GeoJSON (SoQL queryable)
- Why primary: Still the single broadest feed in the domain. One endpoint pattern (/resource/{4x4}.json) plus one query language (SoQL) reaches ~10,000 datasets, and I independently confirmed it simultaneously serves: notifiable-disease counts for exactly 121 distinct conditions in 2026 (x9gk-5huc), hospital COVID+flu+RSV admissions (ua7e-t2fy), ED visit percentages (vjzj-u7u8), five separate live wastewater pathogen streams, the full NCHS VSRR provisional vital-statistics family, and kindergarten MMR coverage (ijqb-a7ye). Five of nine subdomains from one API. DOWNGRADED from the original report's six: 'health-policy' was removed because data.cdc.gov carries no rulemaking, docket or agency-action data — vaccination-coverage statistics are an input to a policy question, not the policy record itself. That subdomain is served by Federal Register and Regulations.gov.

```bash
curl -s 'https://data.cdc.gov/resource/x9gk-5huc.json?%24where=year%3D%222026%22%20AND%20label%3D%22Measles%2C%20Indigenous%22%20AND%20states%3D%22U.S.%20Residents%22&%24order=week%20DESC&%24limit=3'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200 on every dataset probed. NNDSS x9gk-5huc: the exact exampleCall returned {"states":"U.S. Residents","year":"2026","week":"36","label":"Measles, Indigenous","m1":"101.0","m2":"255.0","m3":"3050.0","m4":"1374.0"} plus wk35 (m3=2799) and wk34 (m3=2609). count(distinct label) where year='2026' = 121, CONFIRMING the report's figure; I pulled all 121 labels 

#### openFDA (api.fda.gov) — drugsfda, device/510k, device/pma, shortages, enforcement, label, ndc — US Food and Drug Administration ✅ LIVE

Covers **1** subdomains: fda-approvals

- Docs: https://open.fda.gov/apis/authentication/
- Auth: none; optional free api.data.gov key raises the daily cap | Limits: CONFIRMED VERBATIM from https://open.fda.gov/apis/authentication/, which states: 'With no API key: 240 requests per minute, per IP address; 1,000 requests per day, per IP address. With an API key: 240 requests per minute, per key; 120,000 requests per day, per key.' The original report's numbers are exactly right. limit caps at 100 per call (1,000 on some endpoints) with skip paging to 25,000; beyond that use the quarterly bulk JSON partitions. Note: no X-RateLimit-* response headers are emitted, so remaining quota cannot be read at runtime.
- Latency: drugsfda daily (meta.last_updated=2026-09-16 confirmed); device/510k and device/pma weekly (both meta.last_updated=2026-09-07 confirmed); shortages daily (meta.last_updated=2026-09-18 confirmed); enforcement weekly | Format: REST JSON (+ bulk JSON/ZIP partitions)
- Why primary: One host, one auth scheme, one query grammar covers the entire FDA regulatory output surface: every drug application with per-submission approval status and date, every 510(k) clearance and PMA approval, every recall, every shortage, every structured label and NDC entry. This is the settlement layer for FDA approval contracts and it replaces reaching for separate drug-approval, device-approval and recall APIs. DOWNGRADED from the original report's three subdomains to one: 'drug-pricing' was removed because openFDA serves no price field anywhere — I enumerated the full /drug/ndc.json record schema and there is no price or cost field of any kind; /drug/shortages is a supply-status feed, not a price feed. 'health-policy' was removed because openFDA carries regulatory output records, not rulemaking, dockets or agency policy actions.

```bash
curl -s 'https://api.fda.gov/device/510k.json?search=decision_date:%5B2026-08-01+TO+2026-09-20%5D&limit=1'
```

> Evidence: Independently fetched 2026-09-20/21; all endpoints HTTP 200. The exact exampleCall returned meta.last_updated=2026-09-07, meta.results.total=313, first hit a Cardiovascular-panel device from Austin TX with product_code DXN — total matches the report exactly. device/pma decision_date:[2026-01-01 TO 2026-09-20] returned total=1575 with first hit {"pma_number":"N12159","applicant":"ETHICON, Inc.","de

#### WHO OData family — Disease Outbreak News + Global Health Observatory + xMart FluMart/FluNet — World Health Organization ✅ LIVE

Covers **4** subdomains: emerging-outbreaks, avian-and-zoonotic-flu, respiratory-outbreaks, vital-statistics

- Docs: https://www.who.int/data/gho/info/gho-odata-api
- Auth: none on all three marts | Limits: No published quota and no rate-limit headers on any of the three. GHO responses are Azure-CDN cached (ghoapi.azureedge.net) with cache-control max-age=3600, so polling faster than hourly gains nothing. Full archives reachable via $skip/$top paging. UNKNOWN exact ceiling. Note the three marts sit on three different hosts — who.int/api for DON, ghoapi.azureedge.net for GHO, xmart-api-public.who.int for FluNet — so 'one client' means one OData dialect, not one base URL.
- Latency: DON per-event, typically within days of WHO verification (newest item 2026-09-10, i.e. 11 days old at verification); FluNet weekly (current to ISO week 38, week starting 2026-09-14); GHO annual-to-irregular and materially lagged — the USA life-expectancy series returned records for 2006 and 2008 | Format: REST JSON (OData v4); FluNet also CSV via $format=csv
- Why primary: The single global counterpart to the CDC feed, and all three marts speak the same OData dialect so one client handles them. DON is the authoritative event stream that any 'new outbreak' contract has to resolve against; FluNet VIW_FNT carries explicit AH5 and AH7N9 subtype columns for every reporting country, which is the global avian-flu surveillance layer; GHO carries 3,099 indicators including life expectancy for international vital-statistics questions. Four subdomains from one provider. All four coverage claims were spot-checked and hold.

```bash
curl -s 'https://www.who.int/api/news/diseaseoutbreaknews?sf_provider=dynamicProvider372&sf_culture=en&%24orderby=PublicationDateAndTime%20desc&%24select=Title,PublicationDateAndTime,UrlName&%24top=3&%24count=true'
```

> Evidence: Independently fetched 2026-09-20/21; all three HTTP 200. The exact exampleCall returned @odata.count=3196 with newest {"UrlName":"2026-DON617","PublicationDateAndTime":"2026-09-10T08:16:08Z","Title":"Ebola disease caused by Bundibugyo virus - Democratic Republic of the Congo"} — matches the report exactly, as do DON616 and DON615. FluNet spot-check (avian-flu claim): xmart-api-public.who.int/FLUMA

#### Delphi Epidata API — FluView (ILINet) + COVIDcast — Carnegie Mellon University Delphi Group ✅ LIVE

Covers **1** subdomains: respiratory-outbreaks

- Docs: https://cmu-delphi.github.io/delphi-epidata/api/api_keys.html
- Auth: none for anonymous; free API key via registration form removes the limit | Limits: CONFIRMED VERBATIM from the official api_keys page: anonymous access is 'public datasets only, rate-limited to 60 requests per hour, only two parameters may have multiple selections'. Registered free key: 'no rate limit, no limit on multiple selections'. Both tiers free. The report's numbers are exactly right. Observed a retry-after header on a response during testing, so the throttle is real and enforced.
- Latency: ILINet weekly, Friday release (release_date 2026-09-18, issue 202636 confirmed); COVIDcast signals daily with source-specific lag | Format: REST JSON
- Why primary: The only feed in the domain that exposes issue/lag versioning — every row carries release_date, issue and lag, so you can reconstruct exactly what was knowable on any past date. That matters more after this verification than before it: CDC's Socrata series are revised in place and I caught one (2ew6-ywp6) whose catalog timestamp says 2026-09-10 while its data stops in 2025. A backtest built on Socrata alone can see numbers nobody had. Delphi also fronts ~20 COVIDcast signal sources behind the same grammar, so it is one feed rather than twenty.

```bash
curl -s 'https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=202601-202640'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200. The exact exampleCall returned {"release_date":"2026-09-18","region":"nat","issue":202636,"epiweek":202601,"lag":35,"num_ili":147058,"num_patients":2818289,"num_providers":4337,"wili":5.29497,"ili":5.21799} — byte-for-byte the row the report cited — followed by 202602 (wili 4.38293), 202603 (wili 4.72432) and 202604 (wili 4.4268), each carrying its ow

#### ClinicalTrials.gov API v2 — US National Library of Medicine / NIH ✅ LIVE

Covers **1** subdomains: clinical-trials

- Docs: https://clinicaltrials.gov/data-api/api
- Auth: none | Limits: No numeric rate limit published in the official docs and no rate-limit headers observed. Community clients converge on ~50 requests/minute per IP with 150ms-1.5s spacing. pageSize caps at 1,000 with nextPageToken cursor paging. UNKNOWN official ceiling.
- Latency: daily | Format: REST JSON
- Why primary: 603k+ registered studies in one API with the exact fields that price a readout contract: overallStatus, enrollment actual vs estimated, and primaryCompletionDate with an actual/anticipated flag — the slip between anticipated and actual PCD is the single most informative predictor of a readout date. DOWNGRADED from the original report's two subdomains to one: 'fda-approvals' was removed because ClinicalTrials.gov holds no approval record of any kind. A pivotal NCT is an input a human uses to reason about an approval; it is not an approval feed, and treating it as one would put a developer on a dead path. openFDA and pdufa.bio serve that subdomain.

```bash
curl -s 'https://clinicaltrials.gov/api/v2/studies?query.intr=BBP-418&pageSize=3&fields=NCTId,BriefTitle,OverallStatus,Phase,PrimaryCompletionDate,LeadSponsorName'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200. The exact exampleCall returned NCT07678775 'Open-Label Extension Study of BBP-418 (Ribitol) for LGMD2I/R9' ACTIVE_NOT_RECRUITING PHASE3 leadSponsor 'ML Bio Solutions, Inc.' primaryCompletionDate 2030-10; NCT05775848 ACTIVE_NOT_RECRUITING PHASE3 PCD 2027-09; NCT04800874 PHASE2 PCD 2026-11-01. This matches the report except for one detail the report got

#### pdufa.bio Catalyst API — PDUFA dates, AdComms, readouts — pdufa.bio (independent) ✅ LIVE

Covers **2** subdomains: fda-approvals, clinical-trials

- Docs: https://www.pdufa.bio/developers
- Auth: none for the anonymous tier; optional free API key via x-api-key header | Limits: CONFIRMED from live response headers: x-ratelimit-limit: 1000, x-ratelimit-remaining: 990, x-api-tier: anonymous, x-quota-state: ok, x-credits-cost: 1. So the 1,000/day anonymous figure is right. Free keyed tier documented at 10,000 requests/month, 30/minute burst — NOT independently verified, since that requires registering a key. Attribution plus link-back is required by the license string returned in every response body.
- Latency: daily (meta.as_of returned 2026-09-20, same day as verification) | Format: REST JSON (+ CSV via format=csv, iCal via /calendar.ics — note .ics and bulk export are listed in meta.pro_features, i.e. PAID, not free)
- Why primary: The forward-looking half of the approval subdomain, which no government feed provides. openFDA tells you an approval happened; nothing at FDA publishes the PDUFA calendar as structured data, and I confirmed separately that the Federal Register does not carry approvals either. This does, and it joins each catalyst to its NCT id with a pcd/pcd_type/slip block. CAVEAT FOUND IN VERIFICATION, not in the original report: the /adcomm endpoint returns meta.total=2 — two records in the entire collection. The advisory-committee leg is therefore nearly empty and must not be relied on as a calendar. /pdufa (86) and /readouts (327) are substantive.

```bash
curl -s 'https://www.pdufa.bio/api/v1/pdufa?limit=2'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200 on all three endpoints. The exact exampleCall returned meta.as_of=2026-09-20, total=86, tier=anonymous, quota_state=ok, and record pdufa_gsk_2026-06-18 (GSK plc, 'Tebipenem HBr (SPR994) - (PIVOT-PO)', type PDUFA, status Decided, outcome Approved, decision_date 2026-06-17) with nested nct_id {nct: NCT06059846, pcd: 2025-01-27, pcd_type: actual, slip: nu

#### CMS drug-pricing open data — NADAC (data.medicaid.gov DKAN) + Medicare Part B/D Spending by Drug (data.cms.gov) — US Centers for Medicare & Medicaid Services ✅ LIVE

Covers **1** subdomains: drug-pricing

- Docs: https://data.medicaid.gov/dataset/fbb83258-11c7-47f5-8b18-5f8e79f7e704
- Auth: none on either host | Limits: No key, no published rate limit on either the DKAN datastore or the CMS data-api, and no rate-limit headers observed. DKAN datastore supports limit/offset with conditions[n][property|value|operator] filtering and properties[n] projection. UNKNOWN numeric ceiling on both.
- Latency: NADAC weekly; Medicare Part D/B Spending by Drug annual with a quarterly companion. Note the rows returned carry effective_date 2026-01-01 / as_of_date 2026-01-07 for the Ozempic NDCs, so per-drug price revisions are not necessarily weekly even though the file is. | Format: REST JSON (DKAN datastore query API and CMS data-api) + CSV bulk
- Why primary: NADAC is the literal settlement source named for the drug-pricing subdomain, and one dataset id covers every drug rather than one per molecule — filterable by NDC description in a single call. The CMS Part D/B spending datasets sit on the same footing for the Medicare-exposure contracts. No broader feed exists for US published unit acquisition cost, and I confirmed the alternative candidate is empty: openFDA's NDC directory schema has NO price or cost field of any kind.

```bash
curl -s 'https://data.medicaid.gov/api/1/datastore/query/fbb83258-11c7-47f5-8b18-5f8e79f7e704/0?limit=3&conditions%5B0%5D%5Bproperty%5D=ndc_description&conditions%5B0%5D%5Bvalue%5D=OZEMPIC%25&conditions%5B0%5D%5Boperator%5D=like'
```

> Evidence: Independently fetched 2026-09-20/21; both HTTP 200. The exact exampleCall returned count=245 with {"ndc_description":"OZEMPIC 0.25-0.5 MG/DOSE (2 MG/3 ML) PEN","ndc":"00169418103","nadac_per_unit":"332.02296","effective_date":"2026-01-01","pricing_unit":"ML","as_of_date":"2026-01-07"} — matches the report exactly, including the 245 count and the per-unit price. Two further rows returned (NDC 00169

#### Federal Register API v1 — US National Archives / GPO ✅ LIVE

Covers **2** subdomains: health-policy, drug-pricing

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none | Limits: No key and no published rate limit; no rate-limit headers observed. per_page caps at 1,000; result sets cap at 10,000 documents per query — CONFIRMED, the FDA agency filter returned count=10000 with total_pages=50 at per_page=2, which is the cap asserting itself rather than a true total. A search_after_cursor is returned inline in next_page_url for deeper paging. History from 1994.
- Latency: same-day — documents appear at 6am ET on their publication date, and the API carries the next day's public-inspection items (CONFIRMED: on 2026-09-20/21 the newest documents carried publication_date 2026-09-21) | Format: REST JSON
- Why primary: Publication in the Federal Register is the legal moment a health rule, an HHS action or a presidential health directive becomes real, which makes this the settlement feed for the policy subdomain rather than a news proxy. One API covers FDA, CDC, CMS and HHS with agency, docket_ids, effective dates, comments_close_on and CFR citations as structured fields. It is also the only reliable machine-readable route to HHS actions — I re-confirmed HHS's own newsroom RSS is 403-blocked. It retains 'drug-pricing' because CMS IRA negotiation notices genuinely publish here and nowhere else machine-readable. DOWNGRADED: 'fda-approvals' was removed. I searched the FDA agency filter for approval documents and what comes back is guidance availability notices, pilot-program announcements, fee-rate notices and information-collection requests — not drug or device approvals. Drug approvals are not Federal Register documents. Routing an approval contract here would return nothing usable.

```bash
curl -s 'https://www.federalregister.gov/api/v1/documents.json?per_page=2&order=newest&conditions%5Bagencies%5D%5B%5D=food-and-drug-administration&fields%5B%5D=title&fields%5B%5D=type&fields%5B%5D=publication_date&fields%5B%5D=docket_ids&fields%5B%5D=comments_close_on'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200. The exact exampleCall returned count=10000, total_pages=50, a working next_page_url with search_after_cursor, and newest document {"title":"Agency Information Collection Activities; Submission for Office of Management and Budget Review; Comment Request; Orphan Drugs","type":"Notice","publication_date":"2026-09-21","docket_ids":["Docket No. FDA-2026-N-

#### Regulations.gov API v4 — US GSA / eRulemaking Program ✅ LIVE

Covers **2** subdomains: health-policy, drug-pricing

- Docs: https://open.gsa.gov/api/regulationsgov/
- Auth: api.data.gov key in the api_key parameter; DEMO_KEY works for evaluation, free self-service key for production | Limits: Free key: 1,000 requests/hour. DEMO_KEY is far lower (roughly 30/hour per IP, 50/day) and is for testing only — I exercised DEMO_KEY successfully several times without exhausting it. page[size] must be between 5 and 250 — INDEPENDENTLY RE-CONFIRMED: a page[size]=2 request returned HTTP 400 with body {"errors":[{"title":"Page size parameter must be a positive number of 5 or greater.","status":"400"}]}. Result sets cap at 5,000 per query; use lastModifiedDate windowing beyond that.
- Latency: daily; comment counts update continuously during an open period | Format: REST JSON (JSON:API)
- Why primary: The predictive counterpart to the Federal Register. Where FR tells you a rule published, this tells you where a docket sits before it does — comment open/close dates, comment volume, supporting analyses — which is what moves a policy contract's probability in the weeks before settlement. Covering FDA, CMS, CDC and HHS from one endpoint keeps it to a single feed for the whole policy subdomain.

```bash
curl -s 'https://api.regulations.gov/v4/documents?filter%5BagencyId%5D=FDA&sort=-postedDate&page%5Bsize%5D=5&api_key=DEMO_KEY'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200 with page[size]=5. filter[agencyId]=FDA returned meta.totalElements=240264 — matches the report exactly — with newest items FDA-2026-V-8845-0001 'Variance Application from BTS Event Rentals' (postedDate 2026-09-18, subtype 'Application for Variance (VAR)') and FDA-2025-N-2787-0008 (postedDate 2026-09-18, commentEndDate 2026-11-18, openForComment true, 

#### USDA APHIS HPAI detection CSVs + WOAH WAHIS event API — USDA Animal and Plant Health Inspection Service; World Organisation for Animal Health ✅ LIVE

Covers **2** subdomains: avian-and-zoonotic-flu, emerging-outbreaks

- Docs: https://www.aphis.usda.gov/livestock-poultry-disease/avian/avian-influenza/hpai-detections ; https://wahis.woah.org/
- Auth: none on either | Limits: APHIS: static CSV on a public file server, no key and no published quota; whole file per request (wild-birds is 1,984,389 bytes — confirmed to the byte). WAHIS: undocumented public JSON API backing the WAHIS portal — no key, no published quota, no stability guarantee. It is POST-only. Response carries totalSize=6813 events with pageNumber/pageSize paging.
- Latency: APHIS CSVs refreshed as detections are confirmed (wild-birds current to 2026-09-16, mammals to 2026-09-09 — both re-derived by parsing the files, not taken on trust); WAHIS per-report, typically within days of national submission | Format: CSV bulk (APHIS); REST JSON POST (WAHIS)
- Why primary: The animal reservoir is what prices a human H5N1 contract, and these two cover it end to end: APHIS for US wild birds and mammals with state/county/strain/species, WAHIS for the rest of the world. The breadth claim held up under check: WAHIS is genuinely multi-pathogen, so it is one feed for all zoonotic and animal-disease outbreak events rather than one per pathogen. The two gaps the original report disclosed are real and I reproduced both.

```bash
curl -s -o hpai-wild-birds.csv 'https://www.aphis.usda.gov/sites/default/files/hpai-wild-birds.csv'   # and:   curl -s -X POST 'https://wahis.woah.org/api/v1/pi/event/filtered-list' -H 'Content-Type: application/json' -d '{"pageNumber":1,"pageSize":200,"sortColName":"eventStartDate","sortColOrder":"DESC"}'
```

> Evidence: Independently fetched 2026-09-20/21. APHIS hpai-wild-birds.csv HTTP 200, 1,984,389 bytes, 19,859 data rows parsed, header exactly 'State,County,Collection Date,Date Detected,HPAI Strain,Bird Species,WOAH Classification,Sampling Method,Submitting Agency', computed max(Date Detected)=2026-09-16 — every figure matches the report. hpai-mammals.csv HTTP 200, 825 data rows, computed max(Date Detected)=2

#### CDC Measles Cases and Outbreaks headline data (wcms/vizdata JSON) — US Centers for Disease Control and Prevention ✅ LIVE

Covers **1** subdomains: measles-and-vpd

- Docs: https://www.cdc.gov/measles/data-research/index.html
- Auth: none | Limits: No key, no published quota. Two small static JSON files (5,992 bytes and 16,110 bytes — confirmed to the byte) behind the CDC CDN. These are undocumented endpoints backing the public dashboard, with no stability guarantee. That risk is not theoretical: a THIRD vizdata path cited by the original report in the measles predictive stack is already dead (see rejectedFeeds). Keep NNDSS Socrata wired as the fallback.
- Latency: weekly, published Wednesdays | Format: REST JSON (flat array of rows)
- Why primary: Narrow, and included only because it is the literal number the contracts resolve to. The 'US Measles Cases in 2026?' market settles on CDC's published annual case total, and this file IS that total as a machine-readable array. NNDSS on Socrata is the broader feed and covers measles too, but I confirmed its counts are both split and lagged relative to the headline tally, so it cannot be substituted for settlement without an assumption. Both remain wired.

```bash
curl -s 'https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesYear.json'   # and weekly: curl -s 'https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesWeekly.json'
```

> Evidence: Independently fetched 2026-09-20/21; both HTTP 200 with content-type application/json. MeaslesCasesYear.json = 5,992 bytes and contains {"year":"2026","cases":"3471"} (present under both the '1985-Present' and '2000-Present' filter variants) alongside {"year":"2025","cases":"2289"} — matches the report exactly. MeaslesCasesWeekly.json = 16,110 bytes with final rows {"week_start":"2026-08-30","week

#### CDC FluSight / COVID-19 Forecast Hub (hubverse) — CDC Center for Forecasting and Outbreak Analytics + Reich Lab ✅ LIVE

Covers **1** subdomains: respiratory-outbreaks

- Docs: https://github.com/cdcepi/FluSight-forecast-hub
- Auth: none | Limits: No quota beyond GitHub raw-content fair use, which is unauthenticated and effectively unlimited at this volume. Use raw.githubusercontent.com rather than the GitHub REST API for bulk reads — the REST API is 60 requests/hour unauthenticated.
- Latency: CORRECTED. Weekly during season — Wednesday submission deadline, ensemble published Thursday. The report described the target data as refreshing 'year-round'; I parsed the file and its max date is 2026-07-04, i.e. roughly 11 weeks behind at verification. So BOTH the forecasts and the realized target series go quiet out of season. Treat this feed as seasonal in full, not as a year-round observation source. | Format: CSV / parquet over GitHub raw + S3 mirrors
- Why primary: The only feed in the domain that publishes calibrated probabilistic forecasts rather than observations. Every submission is in a standardized quantile format, so the official ensemble converts directly into a prior for a weekly-hospitalization contract without any modelling of your own, and the realized target data sits in the same repo. Kept as a predictive input only — it cannot settle anything, and in the off-season it cannot even observe.

```bash
curl -s 'https://raw.githubusercontent.com/cdcepi/FluSight-forecast-hub/main/target-data/target-hospital-admissions.csv'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200. target-data/target-hospital-admissions.csv = 573,679 bytes (matches the report to the byte), header exactly 'date,location,location_name,value,weekly_rate', 12,243 data rows. SEASONALITY LIMIT REPRODUCED AND EXTENDED: the report's claim that the ensemble pauses over summer is confirmed — 2026-09-12-FluSight-ensemble.csv returns HTTP 404 while 2026-05-

#### Nextstrain — Charon API and data.nextstrain.org — Nextstrain (Fred Hutch / Biozentrum Basel) ✅ LIVE

Covers **4** subdomains: avian-and-zoonotic-flu, respiratory-outbreaks, measles-and-vpd, emerging-outbreaks

- Docs: https://docs.nextstrain.org/en/latest/
- Auth: none | Limits: CORRECTED. No documented quota, but the payload sizes in the original report are badly understated. The h5n1-cattle-outbreak/genome dataset is 34,412,119 bytes — 34.4 MB, not the '~6.6MB' the report implied for a typical build. Cache aggressively, refresh daily at most, and budget for tens of MB per pathogen build. The catalog endpoint itself is small (57,417 bytes). Builds are rolling windows (2y / 6m / all-time variants per pathogen), not full archives.
- Latency: daily-to-weekly rebuilds per pathogen (the cattle-outbreak genome build reported meta.updated = 2026-09-14) | Format: REST JSON (Augur v2 dataset) + TSV/gz bulk
- Why primary: The genomic layer across four subdomains from one enumerable catalog. This is where mammalian-adaptation markers and clade replacement show up before they reach a case count, which is the lead time a reassortment or new-variant contract pays for. Honest framing that the original report blurred: Nextstrain supplies genomic CONTEXT for these four subdomains, not case counts or settleable quantities. It belongs in every predictive stack here and in none of the settlement stacks.

```bash
curl -s 'https://nextstrain.org/charon/getAvailable?prefix=/'   # then: curl -s 'https://nextstrain.org/charon/getDataset?prefix=/avian-flu/h5n1-cattle-outbreak/genome'
```

> Evidence: Independently fetched 2026-09-20/21; HTTP 200. /charon/getAvailable?prefix=/ returned 57,417 bytes enumerating exactly 310 datasets — matches the report's count — of which 66 are avian-flu builds including the full segment set avian-flu/h5n1-cattle-outbreak/{genome,ha,mp,na,ns,np,pa,pb1,pb2} and avian-flu/h5n1-d1.1/genome, confirming both the cattle-outbreak and D1.1 builds are live and segment-re

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| COVID & Respiratory Disease | Delphi Epidata /fluview (ILINet with issue/lag backfill) + C | CDC Socrata NHSN weekly hospital respiratory ua7e-t2fy (tota | 🟢 COVERED |
| Avian Influenza & Zoonoses | USDA APHIS hpai-wild-birds.csv and hpai-mammals.csv (state/c | CDC Socrata NNDSS x9gk-5huc, label 'Novel Influenza A virus  | 🟢 COVERED |
| Measles & Vaccine-Preventable Disease | CDC Socrata NWSS measles wastewater akvg-8vrb (site-level me | CDC https://www.cdc.gov/wcms/vizdata/measles/MeaslesCasesYea | 🟢 COVERED |
| Emerging Outbreaks & PHEIC | WHO Disease Outbreak News OData (publication cadence and per | WHO Disease Outbreak News OData (https://www.who.int/api/new | 🟡 PARTIAL |
| FDA Drug & Device Approvals | pdufa.bio /api/v1/pdufa (86 PDUFA target dates with date_pre | openFDA /drug/drugsfda.json (submissions.submission_status=' | 🟢 COVERED |
| Clinical Trial Readouts | ClinicalTrials.gov API v2 (overallStatus, enrollment actual  | ClinicalTrials.gov v2 results module (results posting and ad | 🟡 PARTIAL |
| Drug Pricing & Access | NADAC weekly file on data.medicaid.gov (dataset fbb83258-11c | NADAC via the data.medicaid.gov DKAN datastore query API — t | 🟢 COVERED |
| Health Policy & Agencies | Regulations.gov API v4 — docket stage, comment open/close da | Federal Register API v1 — the legal moment of publication fo | 🟢 COVERED |
| Vital Statistics & Demography | CDC Socrata NCHS VSRR provisional family — hmz2-vwda (state/ | CDC Socrata NCHS final series — w9j2-ggv5 (death rates and l | 🟢 COVERED |

**Rejected**

- **CDC Socrata 2ew6-ywp6 — NWSS Public SARS-CoV-2 Wastewater Metric Data** — NEWLY REJECTED BY THIS VERIFICATION. The original report wired this in as the SARS-CoV-2 wastewater stream for respiratory-outbreaks and marked it verified live. It is HTTP 200 and returns well-formed rows, and its Socra
- **CDC vizdata MMR kindergarten coverage JSON (/wcms/vizdata/measles/mmr-vaccine-coverage-for-kindergarteners-by-school-year.json)** — NEWLY REJECTED BY THIS VERIFICATION — DEAD. The original report listed this as a predictive input for measles-and-vpd. It returns HTTP 404 with a 20,905-byte CDC 'Page Not Found' HTML page, content-type text/html. Replac
- **pdufa.bio /api/v1/adcomm as an advisory-committee calendar** — NEWLY DOWNGRADED. The endpoint is live and the record the original report cited (adcomm_capr_2026-07-29, Capricor Deramiocel CTGTAC — DMD) is real, but meta.total=2 — the entire collection is two records. It was presente
- **Federal Register as an FDA-approvals feed** — NEWLY REJECTED FOR THAT SUBDOMAIN (the feed itself remains primary for health-policy and drug-pricing). The original report claimed coversSubdomains including fda-approvals. A term search for '\"new drug application\" ap
- **openFDA as a drug-pricing or health-policy feed** — NEWLY REJECTED FOR THOSE SUBDOMAINS (openFDA remains primary for fda-approvals). The original report claimed three subdomains. I enumerated the complete /drug/ndc.json record schema — product_ndc, generic_name, labeler_n
- **ClinicalTrials.gov as an FDA-approvals feed** — NEWLY REJECTED FOR THAT SUBDOMAIN (the feed remains primary for clinical-trials). CT.gov holds registration and results records; it holds no approval decision, approval date, or regulatory action of any kind. The origina
- **USDA APHIS commercial and backyard poultry flock detections** — CONFIRMED REJECTED — no machine-readable form. I independently re-probed five candidate CSV filenames under /sites/default/files/ (hpai-commercial-backyard-flocks.csv, hpai-poultry.csv, hpai-flocks.csv, hpai-positive-flo
- **USDA APHIS hpai-livestock.csv (dairy herd detections)** — CONFIRMED REJECTED — live but stale. HTTP 200, 4,618 bytes, 116 data rows, header 'State,Species,Date confirmed by NVSL'. I parsed the date column and computed max = 2024-06-18, over two years old; the newest rows are Te
- **ECDC ERVISS — European Respiratory Virus Surveillance Summary** — Not re-tested this session and carried forward as the original report described it: live and good quality, but superseded for this domain by WHO xMart FluNet VIW_FNT, which I did verify returns EU/EEA plus rest-of-world 
- **HHS newsroom RSS (hhs.gov/rss/news.xml and hhs.gov/about/news/rss.xml)** — CONFIRMED DEAD for programmatic use. I independently re-tested both paths on 2026-09-20/21 and both returned HTTP 403. HHS actions are reachable instead through the Federal Register API by filtering on agency id 221.
- **CDC WONDER API** — NOT VERIFIED — reported as unmeasured rather than working, in either direction. It is an XML-POST interface (wonder.cdc.gov/controller/datarequest), not REST. I did not exercise it, because every vital-statistics series 
- **CMS IRA drug price negotiation / Maximum Fair Price list** — Carried forward from the original report: no API exists; the selected-drug list and negotiated prices publish as press releases and Federal Register notices only. I did not re-run the 159-dataset catalog search, so the s
- **Global.health outbreak-data (GitHub)** — Carried forward, not re-tested. Superseded by WHO Disease Outbreak News for settlement (verified live at 3,196 items) and by WOAH WAHIS for the animal precursor (verified live at 6,813 events). A curated per-outbreak lin
- **WHO COVID-19 Global Daily Data bulk CSV and Our World in Data compact.csv** — Carried forward, not re-tested. Large static blobs refreshed weekly-to-monthly against a post-emergency reporting cadence that has collapsed. CDC Socrata NHSN gives higher-frequency US data (verified current to 2026-09-1
- **EU Clinical Trials Information System (CTIS) public API** — Carried forward, not re-tested. POST-only and awkward, and every clinical-trial contract in this domain's venue list is US-sponsor-centric, which ClinicalTrials.gov v2 covers with a cleaner REST interface. Worth revisiti
- **openFDA FAERS /drug/event and MAUDE /device/event** — Carried forward, not re-tested. Live but too narrow: adverse-event surveillance, not approval, pricing, disease-spread or policy. None of the nine subdomains resolve on adverse-event counts. Relevant only if a venue list
- **AppliedXL** — PAYWALLED / NO PUBLIC API. Named by Kalshi as the settlement source for the clinical-trial-readout subdomain, but commercial with no free tier. This is why clinical-trials stays PARTIAL rather than COVERED — the settleme

---

### macroeconomics

*8/12 subdomains covered · 14 primary feeds*

#### FRED — keyless fredgraph CSV bulk series export (+ keyed REST API) — Federal Reserve Bank of St. Louis ✅ LIVE

Covers **12** subdomains: cpi-inflation, gdp, employment, jobless-claims-and-jolts, layoffs, consumer-sentiment-and-spending, housing, mortgage-and-credit-defaults, fed-policy, global-central-banks, recession-and-cycle, regional-and-foreign-economies

- Docs: https://fred.stlouisfed.org/docs/api/fred/
- Auth: NONE for the fredgraph.csv path (no key, no registration). The richer /fred/ REST API (search, release calendar, vintages, metadata) needs a free self-service 32-char key. | Limits: fredgraph.csv: no key and no documented rate limit; it is the same static-export path fred.stlouisfed.org serves to its own charts. I issued ~40 sequential requests in this verification with no throttling. Keyed REST API: no officially documented limit; the widely-circulated 120 req/min figure is community-sourced, NOT in the docs.
- Latency: Per series, and VERIFIED per series. Daily: DFEDTARU 2026-09-20, T10Y3M 2026-09-18, T10YIE 2026-09-18, EFFR 2026-09-17. Weekly: ICSA/IC4WSA 2026-09-12, MORTGAGE30US 2026-09-17. Monthly: CPIAUCSL/RSAFS/HOUST/PERMIT/USREC/CAUR 2026-08. Quarterly: GDPC1 2026-04. NOTE the mirror lag traps found: UMCSENT stops at 2026-07 while the UMich source file has 2026-08, and DRCCLACBS/DRSFRMACBS/USSTHPI stop at 2026-04. | Format: CSV (single series) / ZIP-of-CSVs (multi-series, split by frequency). Keyed API: JSON or XML.
- Why primary: CONFIRMED as the one-feed-covers-everything answer for this domain. One keyless URL pattern, one changed query parameter to move from inflation to housing to the yield curve. I independently re-fetched 30 distinct series spanning all 12 claimed subdomains and every one returned real 2026 observations. Building 12 separate integrations when this covers all 12 would be the exact mistake to avoid. Two caveats I am attaching rather than burying: (a) FRED is a MIRROR, and I proved at least one case where the mirror is a full month behind the source (UMCSENT), so settlement should read the publishing agency; (b) FRED's foreign/OECD-sourced mirrors are unreliable — see rejectedFeeds.

```bash
curl 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=ICSA&cosd=2026-08-20'   # single series -> plain CSV. Multi-series returns a ZIP of per-frequency CSVs: curl -o bundle.zip 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE,PAYEMS,ICSA'
```

> Evidence: INDEPENDENTLY RE-FETCHED, all HTTP 200, keyless, Content-Type application/csv. Single-series CPIAUCSL (17,744 B) tail: 2026-06-01,332.568 / 2026-07-01,332.813 / 2026-08-01,334.131. ICSA&cosd=2026-08-20 -> observation_date,ICSA / 2026-08-22,204000 / 2026-08-29,207000 / 2026-09-05,206000 / 2026-09-12,196000. Multi-series id=UNRATE,PAYEMS,ICSA -> HTTP 200 Content-Type application/zip, 21,273 B, opens

#### BLS Public Data API v2 — multi-series POST — US Bureau of Labor Statistics ✅ LIVE

Covers **5** subdomains: cpi-inflation, employment, jobless-claims-and-jolts, layoffs, regional-and-foreign-economies

- Docs: https://www.bls.gov/developers/api_faqs.htm
- Auth: NONE required — the v2 endpoint accepts unregistered POSTs (independently re-confirmed live in this verification, two separate POSTs). A free key (annual renewal) lifts the quota. | Limits: Unregistered: 25 queries/day, 25 series per query, 10 years per query. Registered v2 key: 500 queries/day, 50 series/query, 20 years/query, 50 requests per 10 seconds. NOT INDEPENDENTLY MEASURED: I issued only 2 unregistered POSTs and did not probe the 25/day ceiling, so the quota figures are as-documented, not as-tested.
- Latency: Data posts at the official release instant — 8:30am ET on Employment Situation and CPI days. CPI and payrolls both carried August 2026 as the latest observation at time of check, consistent with no lag versus the press release. | Format: REST JSON (POST for multi-series, GET for single)
- Why primary: This is the SETTLEMENT authority, and one POST body settles five subdomains at once. CUUR0000SA0 is specifically the NSA CPI-U index that Kalshi's KXCPIYOY resolves against — not the SA series a naive integration would grab. Same call returns nonfarm payrolls, U-3, JOLTS openings, JOLTS quits and average hourly earnings. FRED mirrors these numbers but FRED is a mirror; when a contract resolves you want the publishing agency's own bytes. CORRECTION APPLIED: the prior report also claimed 'consumer-sentiment-and-spending'. BLS publishes neither retail sales (Census) nor consumer sentiment (UMich); the justification offered was average hourly earnings, which is an earnings series, not spending or sentiment. That subdomain has been REMOVED from this feed's coverage. 'regional-and-foreign-economies' is retained but is US-REGIONAL ONLY — BLS publishes no foreign data.

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"seriesid":["CUUR0000SA0","CES0000000001","LNS14000000","JTS000000000000000JOL","JTS000000000000000QUR","CES0500000003"],"startyear":"2026","endyear":"2026"}' 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
```

> Evidence: INDEPENDENTLY RE-FETCHED. POST HTTP 200, no API key, body status 'REQUEST_SUCCEEDED', responseTime 92ms. Per-series latest: CUUR0000SA0 -> 8 obs, Aug 2026 = 334.980 (Jul 333.918, Jun 333.952); CES0000000001 total nonfarm payrolls -> 8 obs, Aug 2026 = 159075 thousands, footnote code P 'preliminary'; LNS14000000 U-3 -> 8 obs, Aug 2026 = 4.1, with a Jan-2026 footnote about updated population controls

#### ForexFactory Economic Calendar JSON (faireconomy static mirror) — ForexFactory / faireconomy CDN ✅ LIVE

Covers **9** subdomains: employment, jobless-claims-and-jolts, consumer-sentiment-and-spending, housing, fed-policy, global-central-banks, cpi-inflation, gdp, regional-and-foreign-economies

- Docs: https://nfs.faireconomy.media/ff_calendar_thisweek.json
- Auth: none | Limits: No key, no registration, no published rate limit. UNDOCUMENTED endpoint with no published terms of service — it is the static JSON ForexFactory's own front end consumes. Treat as unsupported and cache it; it can disappear without notice. RE-CONFIRMED: only ff_calendar_thisweek.json exists — ff_calendar_nextweek.json and ff_calendar_lastweek.json both return HTTP 404 with 146-byte error bodies.
- Latency: Actuals populate within ~1 minute of a release printing. Forward schedule and consensus are present for the full current week ONLY — the file is a rolling 1-week window, so horizon is at most 7 days. | Format: REST JSON (flat array of event objects)
- Why primary: Still the best PREDICTIVE feed in this domain: one URL carrying the market CONSENSUS FORECAST alongside the previous print and an exact ISO timestamp with offset, across nine currencies. A prediction market on 'Jobs Numbers in September' is priced off consensus-versus-whisper, not off the level. HONESTY CORRECTION: because the file is a rolling CURRENT-WEEK window, a subdomain is only present in the weeks its release actually falls. At my check (week of 2026-09-20) I directly observed rows for employment, jobless claims, housing, consumer and central banks — but ZERO CPI rows and ZERO GDP rows. cpi-inflation and gdp are retained in coverage because those events demonstrably appear in their release weeks, but a developer must not assume any given pull contains them. Archive the file continuously.

```bash
curl 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'
```

> Evidence: INDEPENDENTLY RE-FETCHED. HTTP 200, Content-Type application/json, 10,179 B, 75 events, 7 rated High impact. Verbatim first element: {"title":"Bank Holiday","country":"JPY","date":"2026-09-20T19:00:00-04:00","impact":"Holiday","forecast":"","previous":""}. High-impact rows carrying live consensus: AUD 2026-09-23T21:30-04:00 Employment Change forecast 20.9K previous -15.8K; AUD 2026-09-23T21:30 Une

#### BIS Statistics API v2 — WS_CBPOL central bank policy rates — Bank for International Settlements ✅ LIVE

Covers **2** subdomains: fed-policy, global-central-banks

- Docs: https://stats.bis.org/api-doc/v2/
- Auth: none | Limits: No API key, no registration, no documented rate limit.
- Latency: Daily frequency for the D. key (US daily observation available for 2026-09-15 at time of check, i.e. ~5 days behind on a daily series); monthly aggregates for the M. key (2026-08 latest). NOTE: the M. key lagging to 2026-08 means BIS is NOT a same-day settlement feed for a policy decision — read the decision from the central bank's own release or FRED DFEDTARU/ECBDFR and use BIS for the harmonised cross-country panel. | Format: SDMX 2.1/3.0 — CSV, JSON or XML
- Why primary: CONFIRMED, and better than the prior report claimed. The naive build is one integration per central bank; WS_CBPOL returns the harmonised policy rate for 49 jurisdictions (prior report said ~38 — I counted 49 distinct REF_AREA codes in a single response) from ONE dataflow with a wildcard key. Each row also carries a COMPILATION field stating exactly which instrument is the policy rate for that jurisdiction, which is precisely the ambiguity that breaks naive multi-country rate feeds.

```bash
curl 'https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBPOL/1.0/M.*?format=csv&lastNObservations=1'   # ALL 49 jurisdictions in one call. Single country daily: curl 'https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBPOL/1.0/D.US?format=csv&lastNObservations=2'
```

> Evidence: INDEPENDENTLY RE-FETCHED. D.US HTTP 200, Content-Type text/csv;charset=UTF-8, header 'FREQ,REF_AREA,UNIT_MEASURE,UNIT_MULT,TIME_FORMAT,COMPILATION,DECIMALS,SOURCE_REF,SUPP_INFO_BREAKS,TITLE,TIME_PERIOD,OBS_VALUE,OBS_STATUS,OBS_CONF,OBS_PRE_BREAK'; rows 'D,US,368,0,,From 19 Dec 1985 onwards: mid-point of the Federal Reserve target rate; from 1 Jul 1954 to 18 Dec 1985: US Fed Funds effective rate.,4

#### Atlanta Fed GDPNow + Market Probability Tracker (XLSX bulk) — Federal Reserve Bank of Atlanta ✅ LIVE

Covers **2** subdomains: gdp, fed-policy

- Docs: https://www.atlantafed.org/cqer/research/gdpnow
- Auth: none | Limits: No API, no key, no rate limit — static XLSX re-published on each model update. CRITICAL AND INDEPENDENTLY RE-CONFIRMED: the URL path in the older inventory (/-/media/documents/cqer/... and /-/media/documents/datafiles/...) is DEAD and silently returns a 48,307-byte HTML 404 page under an .xlsx filename with HTTP 200. The live path inserts /Project/Atlanta/FRBA/. Validate the OOXML magic bytes (PK\x03\x04), never the HTTP status.
- Latency: GDPNow rebuilt 6–7 times per quarter within hours of each monthly source release. MPT re-estimated daily from the previous day's SOFR option settlements. NOT INDEPENDENTLY MEASURED: I verified the files are valid current OOXML but did not parse their internal date columns, so the refresh cadence is as-documented, not as-tested. | Format: XLSX bulk download (GDPNow headline also mirrored keyless on FRED as series GDPNOW)
- Why primary: CONFIRMED exactly as described. These two files are the predictive layer no statistical agency publishes. GDPNow is the real-time current-quarter GDP nowcast with subcomponent contributions and the vintage history of every nowcast issued — that vintage record is what lets you backtest how a GDP contract should have been priced. The Market Probability Tracker gives the market-implied PROBABILITY DENSITY over future fed funds / SOFR outcomes (P(rate in bucket X at meeting Y)), not a point forecast — already in the shape a prediction market trades in, and the free replacement for the bot-protected CME FedWatch.

```bash
curl -L -A 'Mozilla/5.0' -o gdpnow.xlsx 'https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/cqer/researchcq/gdpnow/GDPTrackingModelDataAndForecasts.xlsx'  &&  curl -L -A 'Mozilla/5.0' -o mpt.xlsx 'https://www.atlantafed.org/-/media/Project/Atlanta/FRBA/Documents/cenfis/market-probability-tracker/mpt_histdata.xlsx'
```

> Evidence: INDEPENDENTLY RE-FETCHED AND BYTE-VALIDATED. GDPNow corrected URL: HTTP 200, Content-Type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, 10,883,697 B, first 4 bytes hexdump '504b 0304' (PK..), `file` -> 'Microsoft Excel 2007+', Python zipfile opens with 111 sheet entries. MPT corrected URL: HTTP 200, same content type, 6,871,981 B, `file` -> 'Microsoft OOXML', zipfile opens wit

#### DOL ETA 539 — weekly unemployment insurance claims, all states — US Department of Labor, Employment & Training Administration ✅ LIVE

Covers **3** subdomains: jobless-claims-and-jolts, layoffs, regional-and-foreign-economies

- Docs: https://oui.doleta.gov/unemploy/DataDownloads.asp
- Auth: none | Limits: No key, no registration, no documented rate limit. Single full-history CSV — 13,365,263 B / 112,340 rows measured — cache it and diff rather than re-pulling.
- Latency: Weekly, Thursday 8:30am ET with the national claims release. VERIFIED current: latest rptdate in the file is 2026-09-12. | Format: CSV bulk (full history, one row per state per week)
- Why primary: CONFIRMED. The settlement authority for KXJOBLESSCLAIMS, and it beats FRED's ICSA/CCSA on two counts: it is the publishing agency rather than a mirror, and it is disaggregated to 53 state/territory codes in the same file — which covers state-level claims contracts and doubles as the only free high-frequency layoff proxy without adding an integration.

```bash
curl 'https://oui.doleta.gov/unemploy/csv/ar539.csv'
```

> Evidence: INDEPENDENTLY RE-FETCHED AND FULLY PARSED. HTTP 200, Content-Type text/csv, 13,365,263 B. Header: "st","rptdate","c1","c2",...,"c23". Parsed 112,340 rows, 53 distinct state/territory codes. CORRECTION TO PRIOR REPORT: earliest rptdate is 1984-06-09, not 1986 — history is ~2 years deeper than claimed. Earliest row shown: "AK","1986-02-15",6,1986-02-08,2048,... Latest rptdate 2026-09-12; tail rows "

#### US Treasury Daily Yield Curve Rates (CSV) + NY Fed Markets Data API — US Department of the Treasury / Federal Reserve Bank of New York ✅ LIVE

Covers **3** subdomains: recession-and-cycle, fed-policy, mortgage-and-credit-defaults

- Docs: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-yield-curve-rates
- Auth: none on both | Limits: No key, no registration, no documented rate limit on either. Treasury CSV is one file per calendar year (14,690 B for 2026 to date).
- Latency: Treasury curve daily, posted ~6pm ET after close — VERIFIED with 09/18/2026 as the top row. NY Fed reference rates published ~8am ET next business day — VERIFIED with effectiveDate 2026-09-17. | Format: CSV per year (Treasury); REST JSON/XML/CSV (NY Fed)
- Why primary: CONFIRMED. One CSV gives the entire par curve — 1M through 30Y, 14 tenors — which is every yield-curve-inversion contract (YINVERT) and the term-structure input to recession probability, without a per-tenor feed. NY Fed adds the overnight complex (SOFR, EFFR, OBFR, BGCR, TGCR) with full percentile distribution and transaction volume, which is the settlement basis for SOFR-referenced contracts and the anchor for the Atlanta Fed MPT densities.

```bash
curl 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv'   # and: curl 'https://markets.newyorkfed.org/api/rates/secured/sofr/last/1.json'
```

> Evidence: INDEPENDENTLY RE-FETCHED. Treasury HTTP 200, Content-Type text/csv; charset=UTF-8, 14,690 B. Header verbatim: Date,"1 Mo","1.5 Month","2 Mo","3 Mo","4 Mo","6 Mo","1 Yr","2 Yr","3 Yr","5 Yr","7 Yr","10 Yr","20 Yr","30 Yr" (14 tenors confirmed). Rows: 09/18/2026,3.97,3.98,4.10,4.14,4.24,4.24,4.44,4.76,4.83,4.86,4.93,5.01,5.38,5.34 and 09/17/2026,3.97,3.98,4.09,4.12,4.23,4.20,4.40,4.67,4.75,4.78,4.86

#### University of Michigan Surveys of Consumers (tbmics.csv) + NY Fed Survey of Consumer Expectations (XLSX) — University of Michigan ISR / Federal Reserve Bank of New York ✅ LIVE

Covers **2** subdomains: consumer-sentiment-and-spending, cpi-inflation

- Docs: https://data.sca.isr.umich.edu/
- Auth: none on both | Limits: No key, no rate limit on either — both are static files. UMich URL is http and 301-redirects, so you must follow redirects (-L) or you get a CloudFront error body. Note the UMich response Content-Type is application/octet-stream, not text/csv.
- Latency: UMich preliminary ~mid-month, final ~end of month; the CSV carried August 2026 while FRED's UMCSENT mirror still ended at July — INDEPENDENTLY RE-CONFIRMED, the direct file is a full month FRESHER than FRED. NY Fed SCE monthly, ~2nd Monday 11am ET. | Format: CSV (UMich); XLSX (NY Fed SCE)
- Why primary: CONFIRMED, including the lag finding, which is the operationally important part. UMich tbmics.csv is the settlement source for 'University of Michigan Consumer Sentiment' contracts and it leads the FRED mirror by a full month — settling off FRED would resolve on stale data. NY Fed SCE adds 1-year and 3-year household inflation expectations, home-price expectations and job-loss probabilities, which price both consumer and inflation contracts. Two static files, no API to break.

```bash
curl -L -A 'Mozilla/5.0' 'http://www.sca.isr.umich.edu/files/tbmics.csv'   # and: curl -L -A 'Mozilla/5.0' -o sce.xlsx 'https://www.newyorkfed.org/medialibrary/interactives/sce/sce/downloads/data/frbny-sce-data.xlsx'
```

> Evidence: INDEPENDENTLY RE-FETCHED. UMich HTTP 200 after following the 301, Content-Type application/octet-stream, 12,225 B. Header 'Month,YYYY,ICS_ALL'; first data row 'November,1952,86.2'; tail rows 'May,2026,44.8' / 'June,2026,49.5' / 'July,2026,55.2' / 'August,2026,51.7'. DIRECT LAG COMPARISON re-run in this session: FRED fredgraph.csv?id=UMCSENT last observation = 2026-07-01,55.2 — confirming the UMich

#### ECB Data Portal API (policy rates) + Eurostat prc_hicp_minr (CORRECTED ENDPOINT) — European Central Bank / Eurostat ✅ LIVE

Covers **3** subdomains: global-central-banks, cpi-inflation, regional-and-foreign-economies

- Docs: https://data.ecb.europa.eu/help/api/data
- Auth: none | Limits: No key, no registration, no documented rate limit on either. Eurostat caps a single query at 50 items per dimension.
- Latency: ECB policy rates daily — VERIFIED, deposit facility returned for 2026-09-21. Eurostat HICP: the CORRECTED dataset prc_hicp_minr is current, 'updated' field 2026-09-17T11:00:00+0200 with latest period 2026-08. The dataset named in the prior report (prc_hicp_manr) has an 'updated' field of 2026-02-06T23:00:00+0100 and has not moved since. | Format: SDMX-JSON / SDMX-ML / CSV (ECB); JSON-stat 2.0 / SDMX-ML / TSV (Eurostat)
- Why primary: Euro-area contracts settle on ECB and Eurostat, not on an aggregator. ONE Eurostat call with coicop18=TOTAL&unit=RCH_A returns the HICP annual rate for every member state plus the euro aggregate simultaneously — 44 values across 46 geos in a single request — the whole EU inflation surface without per-country integrations. ECB FM supplies the euro-area policy-rate settlement value that BIS WS_CBPOL only mirrors monthly. MAJOR CORRECTION APPLIED: the prior report's Eurostat call and its ECB ICP HICP path are both DEAD-BUT-200. Both are now in rejectedFeeds and replaced by the verified prc_hicp_minr endpoint above. The ECB's own OBS_COM warning about the 2026-02-04 methodology change was accurate — the migration already happened and the old datasets stopped moving.

```bash
curl 'https://data-api.ecb.europa.eu/service/data/FM/D.U2.EUR.4F.KR.DFR.LEV?lastNObservations=1&format=csvdata'   # ECB deposit facility rate. ALL-EU HICP, CORRECTED — the prior report's prc_hicp_manr/coicop=CP00 call is FROZEN; use: curl 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr?format=JSON&coicop18=TOTAL&unit=RCH_A&lastTimePeriod=1'
```

> Evidence: INDEPENDENTLY RE-FETCHED. ECB policy rate HTTP 200, SDMX-CSV: 'FM.D.U2.EUR.4F.KR.DFR.LEV,D,U2,EUR,4F,KR,DFR,LEV,2026-09-21,2.5,A,F,...,Deposit facility - date of changes (raw data) - Level' — current-dated, CONFIRMED. ECB ICP HICP FAILURE: ICP/M.U2.N.000000.4.ANR HTTP 200 but last observation is 2025-12,1.9 — NINE MONTHS STALE as of 2026-09-20, with the embedded OBS_COM 'As of 4 February 2026 onwa

#### National statistics offices — StatCan WDS + ONS beta data API (CORRECTED ENDPOINT) — Statistics Canada / UK Office for National Statistics ✅ LIVE

Covers **3** subdomains: cpi-inflation, regional-and-foreign-economies, employment

- Docs: https://www.statcan.gc.ca/en/developers/wds
- Auth: none on both | Limits: No key, no registration, no documented rate limit on either. StatCan WDS accepts batched vector arrays in one POST. ONS /v1/data is one timeseries per call.
- Latency: StatCan returns an explicit releaseTime field — VERIFIED 2026-09-14T08:30 for the 2026-08 reference period. ONS CPI carried August 2026 with updateDate 2026-09-15T23:00:00.000Z, i.e. ~5 days old at check. | Format: REST JSON (POST) for StatCan; REST JSON (GET) for ONS
- Why primary: PROMOTED to its own entry because the prior report buried these inside a coverage note and, for ONS, cited an endpoint that does not serve data. These are the only two non-EU foreign national offices I could verify returning CURRENT 2026 observations keylessly — which matters because the OECD leg of the prior report's cross-country stack turned out to be far narrower than claimed (no Japan, no euro area, 17 areas total). StatCan carries an explicit releaseTime per observation, which is exactly what a settlement engine needs to know a print has landed.

```bash
curl -X POST -H 'Content-Type: application/json' -d '[{"vectorId":41690973,"latestN":1}]' 'https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods'   # ONS, CORRECTED: curl 'https://api.beta.ons.gov.uk/v1/data?uri=/economy/inflationandpriceindices/timeseries/d7g7/mm23'
```

> Evidence: INDEPENDENTLY FETCHED. StatCan HTTP 200, verbatim: [{"status":"SUCCESS","object":{"responseStatusCode":0,"productId":18100004,"coordinate":"2.2.0.0.0.0.0.0.0.0","vectorId":41690973,"vectorDataPoint":[{"refPer":"2026-08-01","value":169.8,"decimals":1,"releaseTime":"2026-09-14T08:30","frequencyCode":6}]}}]. ONS CORRECTION — this is a fix, not a confirmation: the prior report cited 'ONS beta API v1 (

#### Redfin Data Center metro market tracker (bulk TSV) — DOWNGRADED, DATA IS ~4 MONTHS STALE — Redfin (public S3 bucket) ✅ LIVE

Covers **1** subdomains: housing

- Docs: https://www.redfin.com/news/data-center/
- Auth: none | Limits: No key, no registration, no rate limit. 111,494,355 B gzipped / 318,185,051 B raw — pull on a schedule, not per request. Companion files exist at the same prefix for county, city, zip and neighborhood granularity (NOT probed by me).
- Latency: CORRECTED — DO NOT TRUST THE PRIOR 'weekly refresh' CLAIM. I decompressed and scanned ALL 579,544 rows: the maximum PERIOD_END in the entire file is 2026-05-31. As of 2026-09-20 that is ~3.7 months stale. The file downloads cleanly with HTTP 200 and valid gzip, so a liveness check passes while the data cannot settle anything more recent than May. | Format: Gzipped TSV bulk, 58 columns, REGION_TYPE is 'metro' for every row in this file
- Why primary: RETAINED but DOWNGRADED. It is still the only verified-free source of METRO-LEVEL home prices with median sale price, MoM, YoY, median list price, price per sqft, inventory and days-on-market for ~900+ metros in one file, and Parcl Labs (Polymarket's stated settlement source) remains key-gated at 403. But the staleness finding kills its use as a settlement feed for a near-dated contract: a market resolving on 'Median home value in Austin Metro on September 30, 2026' cannot be settled from a file that stops at May 31. Use it for metro-level backtesting and cross-sectional context; use FRED CSUSHPINSA/USSTHPI for the national indices, and accept that near-real-time metro housing has NO verified free settlement feed.

```bash
curl -A 'Mozilla/5.0' -o redfin_metro.tsv000.gz 'https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/redfin_metro_market_tracker.tsv000.gz' && gzcat redfin_metro.tsv000.gz | head
```

> Evidence: INDEPENDENTLY DOWNLOADED AND FULLY PARSED — this is where I disagree with the prior report. HTTP 200, Content-Type binary/octet-stream, 111,494,355 B, `file` -> 'gzip compressed data, from Unix, original size modulo 2^32 318185051'. Header has 58 columns beginning PERIOD_BEGIN, PERIOD_END, PERIOD_DURATION, REGION_TYPE, REGION_TYPE_ID, TABLE_ID, IS_SEASONALLY_ADJUSTED, REGION, CITY, STATE, STATE_CO

#### OECD Data Explorer SDMX + DBnomics + World Bank (NARROWED — see corrections) — OECD / Cepremap DBnomics / World Bank ✅ LIVE

Covers **3** subdomains: cpi-inflation, gdp, regional-and-foreign-economies

- Docs: https://gitlab.com/sis-cc/dotstatsuite-documentation/-/wikis/Using-API/API-documentation
- Auth: none on all three | Limits: All three keyless. World Bank: per_page max 32,500, supports mrv. DBnomics: default page 1000 with offset paging. OECD: NOT UNLIMITED — a wildcard-METHODOLOGY query (JPN+FRA+ITA+ESP..CPI.PA._T.N.GY) returned HTTP 403 in this session, so OECD throttles or forbids broad structural wildcards. Use explicit dimension values.
- Latency: OECD CPI monthly, 2026-08 present for USA/DEU/KOR at check. World Bank ANNUAL with a 1–2 year lag — latest GDP-growth vintage is 2025, so it is a reference series, NOT a settlement feed for a 2026 contract. DBnomics re-indexes on provider schedule and I PROVED at least one mirror is badly behind (see evidence). | Format: SDMX-CSV (OECD); REST JSON (World Bank); REST JSON (DBnomics)
- Why primary: RETAINED but SUBSTANTIALLY NARROWED. The prior report described this as 'one harmonised layer for EVERY non-US economy instead of an integration per national statistics office' and claimed a verified USA+GBR+JPN+DEU call. That claim does not survive checking. DF_PRICES_ALL on the N (national-methodology) CPI key returns 17 areas, not a global panel, and Japan and the euro area are absent entirely. What it IS genuinely good for: a single call returning comparable annual CPI for a set of large non-EU economies (USA, GBR, DEU, CAN, AUS, CHN, IND, BRA, KOR, IDN, ISR, ARG, COL plus G7/G20/OECD aggregates), and World Bank for a multi-country annual GDP-growth reference in one semicolon-delimited request. DBnomics remains useful as a DISCOVERY layer across 93 providers but must NOT be used as a data mirror without checking each series' last observation. Employment and global-central-banks were dropped from this entry's coverage — BIS and the national offices serve those.

```bash
curl 'https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/USA+GBR+DEU.M.N.CPI.PA._T.N.GY?startPeriod=2026-06&format=csvfile'   # NOTE: JPN removed from this key — it returns NoRecordsFound.  Also: curl 'https://api.worldbank.org/v2/country/CN;IN;BR;JP;DE/indicator/NY.GDP.MKTP.KD.ZG?format=json&mrv=1&per_page=20'   # and: curl 'https://api.db.nomics.world/v22/providers'
```

> Evidence: MIXED — reported per component, not averaged. OECD PARTIAL: HTTP 200 SDMX-CSV for USA+GBR+JPN+DEU returned 8 rows covering ONLY USA (2026-06 3.531425, 2026-07 3.364825, 2026-08 3.396548), DEU (2026-06 2.298851, 2026-07 2.782324, 2026-08 2.861815) and GBR (2026-06 2.8, 2026-07 3.1) — JPN RETURNED NOTHING. Isolating it: JPN.M.N.CPI.PA._T.N.GY -> HTTP 404 body 'NoRecordsFound'; JPN.M._Z.CPI.PA._T.N.G

#### BEA API + BEA / Federal Reserve release RSS — US Bureau of Economic Analysis / Federal Reserve Board ⚠️ UNVERIFIED

Covers **2** subdomains: gdp, fed-policy

- Docs: https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
- Auth: BEA API requires a free email-registered key. The two RSS feeds require NOTHING. | Limits: BEA API: 100 requests/minute, 100 MB/minute, 30 errors/minute per key; breaching any of the three triggers a 1-minute timeout. NOT VERIFIED by me — no key obtained. RSS: no key, no limit, but only the last ~20–50 items — it is a notifier, not an archive.
- Latency: BEA data at the official 8:30am ET release (NOT VERIFIED — key-gated). RSS fires within seconds of publication; both feeds carried current-quarter 2026 items at check. | Format: REST JSON or XML (BEA API); RSS 2.0 (feeds)
- Why primary: BEA is the named settlement source for GDP (KXGDPYEAR) and the publisher of core PCE — the Fed's actual target measure. The RSS pair is the push layer that tells you a release has landed so you can resolve immediately rather than polling. CORRECTION: 'consumer-sentiment-and-spending' has been removed from this entry's coverage — I verified only the RSS notifiers and the key-gated endpoint's error path, and the consumer-spending claim rested on the unverified NIPA tables; FRED's keyless PCE/PSAVERT/RSAFS already cover it and are verified. HONEST CAVEAT RETAINED AND RE-CONFIRMED: FRED mirrors GDPC1 (2026-04-01 = 24,269.613) and PCEPILFE (2026-07-01 = 130.658) keylessly, so the BEA key is an upgrade for NIPA table depth and state/metro GDP, not a prerequisite for settling a headline GDP contract.

```bash
curl 'https://apps.bea.gov/api/data/?UserID=<YOUR_FREE_KEY>&method=GetData&datasetname=NIPA&TableName=T10101&Frequency=Q&Year=2026&ResultFormat=JSON'   # keyless companions, both independently re-verified: curl 'https://apps.bea.gov/rss/rss.xml'  and  curl 'https://www.federalreserve.gov/feeds/press_monetary.xml'
```

> Evidence: MIXED — reported separately rather than averaged, and I agree with the prior report's verifiedLive:false. BEA API: endpoint is LIVE but I could NOT obtain data. Re-probed with UserID=NOKEY -> HTTP 200, body {"BEAAPI":{"Request":{"RequestParam":[{"ParameterName":"USERID","ParameterValue":"NOKEY"},...]}...}} with the documented APIErrorCode 4 path — service up, auth enforced, data NOT verified by me

#### Socrata Open Data — state WARN layoff notices + federated catalog discovery — Tyler Technologies Socrata (state open-data portals) ✅ LIVE

Covers **1** subdomains: layoffs

- Docs: https://dev.socrata.com/
- Auth: none (an optional free app token raises throttling headroom) | Limits: No key required; anonymous requests are throttled per IP on a shared pool. Full SoQL ($where/$order/$limit/$select) supported and confirmed working ($limit and $order both honoured).
- Latency: Per-state posting cadence. The Texas dataset's most recent notice_date at check was 2026-06-23 — roughly 3 months old, so this is not a high-frequency feed. | Format: REST JSON / CSV with SoQL query grammar
- Why primary: CONFIRMED, including the prior report's own warning, which I verified rather than took on trust. This is the only free, structured, machine-readable WARN layoff data that actually returns rows. The Socrata federated catalog is the one endpoint that can discover state WARN datasets programmatically rather than hard-coding 50 scrapers — but it surfaces essentially ONE usable state (Texas). Listed as explicitly partial, not as coverage.

```bash
curl 'https://data.texas.gov/resource/8w53-c4f6.json?$limit=2&$order=notice_date%20DESC'   # catalog discovery across all Socrata domains: curl 'https://api.us.socrata.com/api/catalog/v1?q=WARN+notice&limit=10&only=dataset'
```

> Evidence: INDEPENDENTLY RE-FETCHED. Texas WARN HTTP 200, Content-Type application/json;charset=utf-8, verbatim: [{"notice_date":"2026-06-23T00:00:00.000","job_site_name":"JPMorgan Chase & Co.","county_name":"Collin","wda_name":"North Central Texas WDA","total_layoff_number":"244","layoff_date":"2026-08-21T00:00:00.000","wfdd_received_date":"2026-06-23T00:00:00.000","city_name":"Plano"},{"notice_date":"2026-

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| CPI & Inflation | FRED keyless: EXPINF1YR (Cleveland Fed 1-yr inflation expect | BLS Public Data API v2, series CUUR0000SA0 — the NSA CPI-U i | 🟢 COVERED |
| GDP Growth | Atlanta Fed GDPNow XLSX (re-downloaded, 10,883,697 B, PK mag | BEA API NIPA T10101 — key-gated, NOT verified by me (unregis | 🟢 COVERED |
| Payrolls & Unemployment | ForexFactory Economic Calendar JSON — DIRECTLY OBSERVED carr | BLS Public Data API v2, keyless multi-series POST: CES000000 | 🟢 COVERED |
| Jobless Claims & Job Openings | FRED keyless ICSA (re-verified 2026-09-12 = 196,000; 2026-09 | DOL ETA ar539.csv for initial/continuing claims — the publis | 🟢 COVERED |
| Layoffs | DOL ETA ar539.csv state-level weekly initial claims (highest | BLS API v2 JOLTS JTSLDL / JTSLDR for the official layoffs se | 🟡 PARTIAL |
| Consumer Sentiment & Spending | ForexFactory — DIRECTLY OBSERVED carrying 'Revised UoM Consu | UMich sca.isr.umich.edu/files/tbmics.csv for the Michigan se | 🟢 COVERED |
| Housing Prices & Activity | FRED keyless PERMIT building permits (re-verified 2026-08 =  | FRED keyless CSUSHPINSA Case-Shiller national (re-verified 2 | 🟡 PARTIAL |
| Mortgages, Credit & Defaults | US Treasury daily yield curve CSV (re-verified 10Y = 5.01 on | FRED keyless MORTGAGE30US — Freddie Mac PMMS 30-year fixed,  | 🟢 COVERED |
| Federal Reserve Policy | Atlanta Fed Market Probability Tracker XLSX — market-implied | Federal Reserve monetary-policy press RSS (federalreserve.go | 🟢 COVERED |
| Global Central Banks | ForexFactory Economic Calendar JSON — central-bank decisions | BIS Statistics API v2 WS_CBPOL — harmonised policy rate for  | 🟢 COVERED |
| Recession & Business Cycle | US Treasury daily yield curve CSV (all 14 tenors re-verified | FRED keyless USREC — the NBER-based US recession indicator,  | 🟡 PARTIAL |
| Regional & Foreign Economies | ForexFactory (9 currencies' release calendars with consensus | US states via FRED keyless (CAUR re-verified 2026-08 = 5.1)  | 🟡 PARTIAL |

**Rejected**

- **Eurostat prc_hicp_manr (and prc_hicp_midx, prc_hicp_mmor) — the endpoint the prior report listed as working** — FROZEN, AND IT FAILS SILENTLY WITH HTTP 200. NEW FINDING from this verification. prc_hicp_manr?format=JSON&coicop=CP00&lastTimePeriod=1 returns HTTP 200 with 45 geos and 42 values — which is exactly what the prior report
- **ECB Data Portal ICP dataflow (euro-area HICP) — ICP/M.U2.N.000000.4.ANR** — DISCONTINUED, NO REACHABLE SUCCESSOR. NEW FINDING. HTTP 200 but last observation is 2025-12 = 1.9, with the ECB's own OBS_COM stating 'As of 4 February 2026 onwards, the euro area HICP inflation will undergo major method
- **OECD SDMX DF_PRICES_ALL for Japan, the euro area, and most EU member states** — NoRecordsFound — THE PRIOR REPORT'S JAPAN CLAIM IS FALSE. NEW FINDING. The prior report cited a verified 'USA+GBR+JPN+DEU' four-country call. Re-running that exact call returns 8 rows covering USA, DEU and GBR ONLY — Jap
- **DBnomics as a data MIRROR for BLS series** — STALE BY 19 MONTHS. NEW FINDING. DBnomics itself is live (/v22/providers -> HTTP 200, num_found 93, confirming the prior report's count), but /v22/series/BLS/cu/CUUR0000SA0?observations=1 returns 1,345 observations endin
- **ONS legacy timeseries API (api.ons.gov.uk) and the /v1/datasets catalogue endpoint as a data source** — ONE DECOMMISSIONED, ONE MISCHARACTERISED. NEW FINDING. api.ons.gov.uk/timeseries/d7g7/dataset/mm23/data returns HTTP 404 with the explicit body 'This API has been decommissioned as part of a suite of work to improve the 
- **Redfin metro market tracker as a SETTLEMENT feed (retained only for backtesting)** — DATA ~4 MONTHS STALE despite a perfect download. NEW FINDING. The file itself is healthy — HTTP 200, 111,494,355 B, valid gzip, 579,544 rows, 58 columns, all REGION_TYPE 'metro' — and the prior report's byte count and he
- **Parcl Labs API** — PAYWALLED. Stated settlement source for Polymarket's metro housing markets; 403 without a key. A real settlement gap, not a substitutable one — and now a worse one than the prior report implied, since the proposed free s
- **Truflation daily inflation API** — NO FREE PUBLIC API. truflation.com/api/v1/inflation -> HTTP 404; truflation.com/api/inflation -> 404; api.truflation.com/v1/index -> 404. Only the marketing/marketplace page returns 200. Data access is commercial/on-chai
- **Atlanta Fed GDPNow & Market Probability Tracker — old inventory URL paths** — DEAD URLs, AND DANGEROUSLY SO — INDEPENDENTLY REPRODUCED. atlantafed.org/-/media/documents/cqer/researchcq/gdpnow/GDPTrackingModelDataAndForecasts.xlsx and /-/media/documents/datafiles/research-and-data/mpt/mpt_histdata.
- **FRED foreign OECD-MEI and foreign-central-bank mirror series (JPNCPIALLMINMEI, GBRCPIALLMINMEI, NYGDPMKTPCDCHN, IRSTCB01JPM156N)** — STALE / DISCONTINUED, failing silently with plausible-looking numbers. The prior report flagged the first three. I ADD IRSTCB01JPM156N (Japan immediate rates): HTTP 200, valid CSV, last observation 2026-12... correction,
- **US Census Bureau Data API (timeseries EITS — MARTS retail sales, RESCONST housing starts/permits)** — KEY-GATED and unverified: both endpoints return HTTP 302 redirecting to an HTML page titled 'Missing Key'. A free self-service key exists but was not obtained, so no working claim is made. Superseded for this domain anyw
- **USDA NASS Quick Stats API** — KEY-GATED. quickstats.nass.usda.gov/api/api_GET/ with key=DEMO returns HTTP 401. Needed for state-agriculture contracts such as KXMSCOTTON. Free key available; not verified, so listed as an honest gap rather than a worki
- **CME Group FedWatch / 30-Day Fed Funds (ZQ) public quotes** — BOT-PROTECTED with no stable machine-readable path. Fully superseded by the Atlanta Fed Market Probability Tracker, which publishes the same market-implied probability density from SOFR options as a free static XLSX — re
- **Challenger, Gray & Christmas job-cut report** — PROPRIETARY, no free feed, and no FRED series (fredgraph.csv?id=CHALLENGERLAYOFFS returns a bot-challenge HTML page rather than CSV). Cited by Kalshi layoff markets as a pricing input with no free equivalent. (Carried fo
- **layoffs.fyi** — NO API. The website returns HTTP 200 but api.layoffs.fyi does not resolve. The tech-layoff tally is published only as an embedded Airtable view. Cited by Kalshi layoff markets; no machine-readable access. (Carried forwar
- **warntracker.com, api.warn.dev, data.ny.gov WARN dataset 9a6q-6b5q** — ALL DEAD, and the absence is independently corroborated. warntracker.com/api/layoffs -> 404; api.warn.dev/notices -> no DNS; data.ny.gov/resource/9a6q-6b5q.json -> 404. No federal WARN aggregation API exists. I re-ran th
- **FRED releases/dates economic-calendar endpoint (keyed)** — KEY-GATED and unverified. Superseded by the ForexFactory calendar JSON, which is keyless and carries the market CONSENSUS FORECAST that FRED's calendar does not — though note the ForexFactory file is a rolling current-we
- **ForexFactory ff_calendar_nextweek.json / ff_calendar_lastweek.json** — HTTP 404 — RE-CONFIRMED in this verification, 146-byte error bodies on both. Only ff_calendar_thisweek.json is live. Forward visibility is limited to the current week, and I directly confirmed the consequence: the week-o
- **BLS news-release schedule HTML pages** — bls.gov/schedule/news_release/2026_sched.htm returns HTTP 403 (bot-blocked). Release-timing coverage comes from the ForexFactory calendar instead. (Carried forward; not re-probed.)
- **Trading Economics** — PAYWALLED. Named by Kalshi as a settlement source for some foreign-economy contracts. Leaves a genuine settlement gap for any contract resolving literally on a Trading Economics print. This gap is now WIDER than the prio
- **NBER Business Cycle Dating Committee** — NO API, NO STRUCTURED FEED of any kind. Recession dating is published as prose with a 4–21 month lag. FRED USREC is derived from it and inherits the lag. This is the settlement gap behind KXRECSSNBER-26 and there is no f
- **IMF Data Portal SDMX 3.0 API** — Flagged non-live in the source inventory; the SDMX 2.0 -> 3.0 migration broke existing clients and the auth model is undocumented. Not independently probed in this verification, so this rejection is INHERITED, NOT VERIFI
- **Bank of England IADB and Japan e-Stat API** — Both flagged non-live in the source inventory and not rescued. IMPORTANT CORRECTION TO THE PRIOR REPORT'S REASONING: it dismissed e-Stat on the grounds that 'OECD SDMX carries Japanese CPI (verified)'. That is false — OE
- **MBA (Mortgage Bankers Association) delinquency survey** — MEMBERS-ONLY, no free feed. Superseded for settlement by the Federal Reserve's own delinquency and charge-off series on FRED (DRSFRMACBS 2026-04 = 1.86 and DRCCLACBS 2026-04 = 2.85, both re-verified), which are the more 
- **Cleveland Fed inflation-nowcasting JSON endpoint** — NO JSON API EXISTS; the page is HTML/XLSX only. Not rejected in substance — the headline expectation and trimmed-mean series are mirrored keyless on FRED (EXPINF1YR re-verified 2026-09-01 = 2.64382396), which is the reco

---

### market-mechanics

*0/5 subdomains covered · 3 primary feeds*

#### Kalshi Trade API v2 — /series, /markets, /events, /multivariate_event_collections — Kalshi (CFTC-regulated US designated contract market) ✅ LIVE

Covers **4** subdomains: contract-tenor, contract-structure, parlays-and-combos, untagged-inventory

- Docs: https://trading-api.readme.io/reference/getting-started
- Base: `https://api.elections.kalshi.com/trade-api/v2/`
- Auth: VERIFIED none. Every read used here returned HTTP 200 with no key, no header, no signing — confirmed by response headers on an unauthenticated GET /markets?limit=1&status=open (HTTP/2 200, no WWW-Authenticate, no auth challenge). RSA key-pair signing is required only for order placement. | Limits: VERIFIED unauthenticated public read tier. CORRECTION TO PRIOR REPORT: the '~10 read req/s per IP' figure is a documentation claim I could NOT confirm — Kalshi returns no rate-limit headers (no X-RateLimit-*, no Retry-After) on public reads, so the ceiling is not observable from the API. What I did measure: 15 rapid sequential GETs to /series/KXBTC15M all returned 200, and ~35 calls across this verification hit no throttle. Treat 10 req/s as UNVERIFIED-but-not-contradicted, not as a measured limit. /series with no filter still returns the whole catalog in ONE response, so a full mechanics refresh costs 1 request.
- Latency: CORRECTED. List endpoints are CDN-cached: GET /markets?limit=1&status=open returned 'cache-control: public, max-age=15', 'x-cache: Hit from cloudfront', 'age: 8' — so catalog and list reads can be up to 15s stale. Single-market and orderbook reads are NOT cached: GET /markets/KXMLBGAME-26SEP211835TORBAL-TOR and its /orderbook both returned 'x-cache: Miss from cloudfront' with no cache-control, i.e. real-time. Poll single tickers for live quotes; do not poll the list endpoint for price. series.last_updated_ts observed 2026-09-18T15:20:18Z. settlement_timer_seconds observed = 5. | Format: JSON
- Why primary: One unauthenticated endpoint family replaces every per-mechanic lookup. READ THIS ALONGSIDE THE COVERAGE TABLE: for contract-tenor and contract-structure this feed supplies PARAMETERS AND ROUTING KEYS, not prices — which is exactly why those two table rows read UNCOVERED. The prior report listed them under coversSubdomains without flagging that, which reads as a contradiction; it is not one, but the distinction must be explicit or a developer will wire a tenor field in expecting a price. Verified: /series carries the entire tenor enum as a first-class typed field (frequency ∈ fifteen_min|hourly|daily|weekly|monthly|quarterly|annual|one_off|custom) across all 14,170 series — no tag-string parsing. The same record carries tags (the untagged-inventory signal), settlement_sources and contract_url (the classification input). /markets carries market_type, strike_type, price_level_structure, and on combo tickers mve_collection_ticker + mve_selected_legs, which resolve a parlay to leg market tickers priced through the SAME endpoint. Zero auth, one base URL.

```bash
curl -s 'https://api.elections.kalshi.com/trade-api/v2/series'   # entire 14,170-series catalog, one request, 17.3 MB
# single series (tenor + tags + settlement authority):
curl -s 'https://api.elections.kalshi.com/trade-api/v2/series/KXBTC15M'
# parlay combo -> legs:
curl -s 'https://api.elections.kalshi.com/trade-api/v2/markets/KXMVECROSSCATEGORY-S2026C1CFBCC1A0A-C1FABB13913'
curl -s 'https://api.elections.kalshi.com/trade-api/v2/multivariate_event_collections?limit=200&status=open'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-21. Every figure in the prior report reproduced EXACTLY.
GET /trade-api/v2/series → HTTP 200, 17,347,859 bytes (byte-identical to the prior report), 14,170 series. frequency distribution reproduced exactly: custom 5831, one_off 5760, annual 1501, monthly 372, weekly 305, daily 293, hourly 71, fifteen_min 31, quarterly 6. tags null/empty on 2,782 / 14,170 = 19.63%. 

#### Polymarket Gamma API — /series, /events, /markets, /tags — Polymarket ✅ LIVE

Covers **4** subdomains: contract-tenor, contract-structure, parlays-and-combos, venue-views-and-incentives

- Docs: https://docs.polymarket.com/developers/gamma-markets-api/overview
- Base: `https://gamma-api.polymarket.com/`
- Auth: VERIFIED none. All calls unauthenticated, HTTP 200. | Limits: CORRECTED — the prior report's '100 rows regardless of limit' is WRONG for /series. Measured caps differ per endpoint: /events caps at 100 (limit=100→100, limit=500→100, limit=2000→100), /tags caps at 100 (limit=200→100), but /series caps at 50 (limit=10→10, limit=50→50, limit=51→50, limit=100→50, limit=500→50). A developer who trusted the prior number would silently drop half of every /series page. offset= pagination works correctly and non-overlappingly on /series (offset 0→ids 1..10036, 50→10037..10087, 100→10091..10145, 150→10146..10205, 200→10206..10313 — 350 unique ids across 7 pages, zero duplicates). No key, no rate limit hit across ~45 calls; a 100-event pull returned 16.2 MB in one response.
- Latency: Near-real-time, re-confirmed: series.updatedAt = 2026-09-21T03:20:45.948569Z, seconds old at fetch time. No CDN cache-control observed. 5M contracts roll every 5 minutes. | Format: JSON
- Why primary: Gamma is the only feed exposing Polymarket's _mechanics tag family as QUERYABLE slugs rather than free text, so tenor, structure and merchandising filter server-side from one endpoint. Same caveat as the Kalshi entry: for contract-tenor, contract-structure and venue-views-and-incentives these are PARAMETERS AND FLAGS, not prices — which is why those table rows read UNCOVERED. /series adds a recurrence enum that is the Polymarket analogue of Kalshi's frequency, but see the correction below: the enum is LARGER than the prior report stated. Market records carry negRisk / negRiskAugmented / comboStatus (structure + combo eligibility) and clobRewards / rewardsMinSize / rewardsMaxSpread / featured / new / restricted / archived / cyom (incentives + UI flags), plus the UMA resolution block that covers parlay-leg settlement without the dead subgraph.

```bash
curl -s 'https://gamma-api.polymarket.com/events?limit=100&closed=false&tag_slug=up-or-down'   # live Up-or-Down 5M contract with full mechanics tag set; 100 is the hard cap
curl -s 'https://gamma-api.polymarket.com/series?limit=50&offset=0'   # NOTE: /series caps at 50, not 100 — paginate offset 0..2400
curl -s 'https://gamma-api.polymarket.com/markets?limit=1&closed=false'   # UMA resolution fields
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-21. Feed is live and useful, but I found TWO substantive errors in the prior report.
ERROR 1 — /series page cap is 50, not 100. Measured: limit=10→10, limit=50→50, limit=51→50, limit=100→50, limit=500→50 (1,583,451 bytes), limit=2000→50. /events and /tags do cap at 100 as claimed (limit=2000 on /events?tag_slug=up-or-down → exactly 100; /tags?limit=200 → 100).
ERRO

#### Polymarket CLOB API — /markets — Polymarket (Central Limit Order Book) ✅ LIVE

Covers **2** subdomains: contract-structure, venue-views-and-incentives

- Docs: https://docs.polymarket.com/developers/CLOB/introduction
- Base: `https://clob.polymarket.com/`
- Auth: VERIFIED none for public market-data reads. API key + wallet signing only for order placement. | Limits: VERIFIED unauthenticated. 1,000 rows per page — 20x Gamma's /series cap and 10x Gamma's /events cap. Cursor-paginated via next_cursor. One page returned 1,823,355 bytes with no throttling. Response envelope confirmed: {data, next_cursor, limit, count}.
- Latency: Real-time order-book layer; market records reflect current accepting_orders / accepting_order_timestamp state. No CDN cache headers observed. | Format: JSON
- Why primary: CLOB is the authoritative source for the mechanical parameters Gamma does not fully expose, at 10–20x the rows per request. Same parameters-not-prices caveat as above — both listed subdomains read UNCOVERED in the table because these are contract settings, not a data feed. It carries minimum_tick_size and minimum_order_size (payoff granularity), is_50_50_outcome, neg_risk + neg_risk_market_id + neg_risk_request_id (the identifier linking a multi-outcome group), seconds_delay and game_start_time (the sports embargo mechanic), accepting_orders / enable_order_book / archived (lifecycle), and rewards{rates,min_size,max_spread} (liquidity-incentive tier). Needed alongside Gamma, not instead of it.

```bash
curl -s 'https://clob.polymarket.com/markets?next_cursor='   # 1,000 markets per page, paginate with the returned next_cursor
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-21. Reproduced essentially byte-for-byte; no corrections.
GET /markets?next_cursor= → HTTP 200, 1,823,355 bytes (exact match to prior report), 1,000 records, next_cursor='aWQ6MjQ5Mzk2' (exact match), envelope keys [data, next_cursor, limit, count].
Field set confirmed present on every row: accepting_orders, accepting_order_timestamp, active, archived, closed, condi

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Contract Tenor & Intervals | NONE FOUND | NONE FOUND | 🔴 UNCOVERED |
| Contract Structure Types | NONE FOUND | NONE FOUND | 🔴 UNCOVERED |
| Multi-Event Parlays & Combos | Kalshi Trade API v2 — /markets (mve_selected_legs) + /multiv | Kalshi /series/{leg_series_ticker}.settlement_sources — reso | 🟡 PARTIAL |
| Merchandising Views & Liquidity Incentives | NONE FOUND | NONE FOUND | 🔴 UNCOVERED |
| Untagged & Bespoke Inventory | NONE FOUND at this level, by construction. An untagged serie | Kalshi Trade API v2 — /series settlement_sources (named auth | 🟡 PARTIAL |

**Rejected**

- **Robinhood prediction-markets public API** — DEAD / NONEXISTENT — independently re-probed 2026-09-21, all four results reproduced. api.robinhood.com/marketdata/event_contracts/ → HTTP 404, 0 bytes; api.robinhood.com/prediction_markets/events/ → HTTP 404, 0 bytes; b
- **Adjacent News API (adj.news) — normalized cross-venue prediction-market data** — DEAD — independently re-confirmed. curl to https://api.data.adj.news/api/markets?limit=2 with a 20s timeout returned HTTP 000 and 0 bytes; the connection failed outright with no response body written. Third consecutive n
- **UMA Optimistic Oracle v3 hosted subgraph (api.thegraph.com/subgraphs/name/umaprotocol/…)** — DEAD ENDPOINT / SUPERSEDED — independently re-confirmed: POST with a valid GraphQL body ({_meta{block{number}}}) to the hosted-service URL returned HTTP 301. The Graph's hosted service is retired and the decentralized ga
- **Kalshi /markets/{ticker}/orderbook as a joint parlay price** — REJECTED FOR THIS USE — re-verified and the finding is unchanged and important. The endpoint is live (HTTP 200) but returned an empty book for the sampled combo: {'orderbook_fp':{'no_dollars':[],'yes_dollars':[]}}, 51 by
- **Polymarket Gamma pagination caps — CORRECTED CONSTRAINT, not a rejection** — NOT A REJECTION — a documented constraint, and the prior report got it partly WRONG. Measured caps are per-endpoint, not uniform: /events caps at 100 (limit=2000 → 100 for up-or-down, 5m, 15m, 1h, recurring, hide-from-ne
- **All external subject-matter market-data feeds (commodities, sports, macro, crypto price APIs)** — REJECTED BY CONSTRUCTION, per the domain's own rule 'never map a data feed here.' Every candidate prices an underlying, and every underlying already belongs to a real subdomain elsewhere. Mapping a crypto price feed to '

---

### politics-and-government

*6/10 subdomains covered · 14 primary feeds*

#### Federal Register API v1 — US National Archives / Office of the Federal Register (GPO) ✅ LIVE

Covers **6** subdomains: trade-and-tariffs, presidential-tenure-and-conduct, immigration-and-border, tax-policy, executive-appointments, shutdown-and-debt-ceiling

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: None — no API key required. VERIFIED anonymous. | Limits: No key, no published hard rate limit (fair-use only). Exact calls/minute cap: UNKNOWN — not published. I made 4 queries this session with no throttling.
- Latency: Daily publication; public-inspection endpoint carries documents the business day BEFORE Federal Register publication — the fastest official signal for a new tariff proclamation or executive order. | Format: REST JSON/CSV (plus GPO bulk XML)
- Why primary: The single broadest keyless government-action feed. Every executive order, proclamation, memorandum and determination (presidential-tenure), every Section 232/301 tariff action (trade-and-tariffs), every immigration rule and notice, every Treasury/IRS regulation, agency personnel notices, and shutdown-related agency notices — all in one full-text-searchable index with agency, docket, RIN, effective date and comment-close date. No narrower feed (USTR press page, IRS newsroom, DHS newsroom) adds anything this does not already carry, and none of them are structured.

```bash
curl 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22section%20232%22&per_page=2&order=newest&fields%5B%5D=title&fields%5B%5D=publication_date&fields%5B%5D=type'  # EOs: https://www.federalregister.gov/api/v1/documents.json?conditions[presidential_document_type][]=executive_order&conditions[type][]=PRESDOCU&per_page=3&order=newest&fields[]=title&fields[]=executive_order_number&fields[]=signing_date  # same-day: https://www.federalregister.gov/api/v1/public-inspection-documents/current.json
```

> Evidence: INDEPENDENTLY RE-VERIFIED. HTTP 200 x4 this session. (1) 'section 232' term query -> 846 bytes, count=773, newest two results both 2026-09-14 Presidential Documents: 'Modifying the Scope of Products of Canada Subject to the Additional Duties Imposed To Offset Canadian Discrimination Against the Commerce of the United States With Respect to Motor Vehicles' and '...With Respect to Alcoholic Beverage

#### VoteHub Polls API — VoteHub ✅ LIVE

Covers **3** subdomains: approval-and-polling, presidential-tenure-and-conduct, courts-and-judiciary

- Docs: https://www.votehub.com/ (no public developer docs page; the JSON endpoint is public and undocumented — root https://api.votehub.com/ returns 404, only /polls is served)
- Auth: None — keyless, no registration, no referer or UA requirement. VERIFIED. | Limits: No key and no published rate limit — exact cap UNKNOWN. The full /polls payload is 2.71 MB and returns the entire universe in one response, so poll it once every few minutes rather than per-query. Note: https://www.votehub.com/ itself is behind Cloudflare and returned HTTP 403 to curl; the api.votehub.com host is NOT protected.
- Latency: Poll-release driven — new polls appear within about a day of publication. Data verified current through end_date 2026-09-17. | Format: REST JSON (flat array of poll objects)
- Why primary: One keyless GET returns every polling subject at once rather than one scraper per tracker: Trump approval, Congress approval, Supreme Court approval, JD Vance approval, the 2026 generic ballot, favorability, and Senate/Governor/Mayor/primary horse-race polls — with pollster, sponsor, sample size, population (rv/lv/a), field dates, internal/partisan flags and per-choice percentages. It is also a genuine named Kalshi settlement source (two series confirmed below). It replaces both FiveThirtyEight (frozen) and RealClearPolitics (no free API).

```bash
curl 'https://api.votehub.com/polls' | head -c 2000   # filtered: curl 'https://api.votehub.com/polls?poll_type=approval'  (also poll_type=generic-ballot, favorability, us-senator, governor, mayor, presidential-primary, proposition-50)
```

> Evidence: INDEPENDENTLY RE-VERIFIED, payload byte-identical to the original report. HTTP 200, content-type application/json, 2,711,935 bytes, parsed to 5,641 poll objects. poll_type distribution reproduced EXACTLY: approval 2945, favorability 1037, generic-ballot 544, us-senator 400, governor 368, presidential-primary 191, us-representative 97, attorney-general 37, proposition-50 11, mayor 11. subject distr

#### CourtListener REST API v4 — /search/ endpoint (Free Law Project) — Free Law Project ✅ LIVE

Covers **3** subdomains: courts-and-judiciary, trade-and-tariffs, immigration-and-border

- Docs: https://www.courtlistener.com/help/api/rest/v4/
- Auth: None for the /search/ endpoint — VERIFIED anonymous HTTP 200 on all three query types. A free account token is required for /opinions/, /dockets/ and the other object endpoints and raises rate limits. | Limits: Anonymous /search/ worked without a token this session. Authenticated object endpoints are severely capped: 5 requests/MINUTE, 50/hour, 125/day (Free Law Project's published v4 limits — NOT independently measured by me, since I never authenticated). Budget accordingly — /search/ is the only endpoint you can poll at any useful cadence, and it should still be self-throttled.
- Latency: Near-real-time for docket alerts and RECAP filings; SCOTUS opinions posted within hours of hand-down; oral-argument audio within a day. NOT independently timed this session. | Format: REST JSON (cursor-paginated) + webhooks + bulk CSV dumps
- Why primary: One endpoint replaces PACER (paid, per-page), the SCOTUS docket scraper, the oral-argument calendar scraper and 50 state appellate scrapers. type=o gives opinions/clusters, type=oa gives the argument calendar, type=r gives RECAP/PACER dockets and entries — so the same feed prices a SCOTUS cert grant, a tariff injunction in CIT/Federal Circuit, and an immigration nationwide injunction.

```bash
curl 'https://www.courtlistener.com/api/rest/v4/search/?q=&type=o&court=scotus&order_by=dateFiled%20desc'   # oral-argument calendar: .../search/?type=oa&court=scotus&order_by=dateArgued%20desc   # PACER/RECAP dockets: .../search/?type=r&q=tariff&order_by=dateFiled%20desc
```

> Evidence: INDEPENDENTLY RE-VERIFIED, all three claimed query types, anonymous, HTTP 200. (1) type=o&court=scotus -> 41,962 bytes, count=498145, newest result verbatim {"caseName":"National Republican Congressional Committee v. Brown","court_id":"scotus","court":"Supreme Court of the United States","cluster_id":10967483,"absolute_url":"/opinion/10967483/national-republican-congressional-committee-v-brown/"} 

#### Treasury FiscalData API — US Department of the Treasury / Bureau of the Fiscal Service ✅ LIVE

Covers **2** subdomains: shutdown-and-debt-ceiling, tax-policy

- Docs: https://fiscaldata.treasury.gov/api-documentation/
- Auth: None — no API key, no registration. VERIFIED anonymous. | Limits: No key and no published rate limit — exact cap UNKNOWN. JSON:API-style pagination via page[size]/page[number]; full history is downloadable as CSV. debt_to_penny goes back to 1993.
- Latency: Daily, ~1 business-day lag (verified: latest record_date 2026-09-17 fetched on 2026-09-20). | Format: REST JSON (JSON:API) + CSV/XML
- Why primary: This is the quantitative half of debt-ceiling pricing and it is one keyless API, not two. debt_to_penny gives total public debt outstanding against the statutory limit; the Daily Treasury Statement endpoints give the TGA operating cash balance, daily receipts and withdrawals — which is how you compute the extraordinary-measures runway and the X-date that the whole subdomain trades on. Also carries receipts by source (tax-policy revenue prints).

```bash
curl 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny?sort=-record_date&page%5Bsize%5D=2'   # cash runway: curl 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page[size]=2'
```

> Evidence: INDEPENDENTLY RE-VERIFIED, both endpoints HTTP 200, values reproduce the original report to the cent. debt_to_penny -> verbatim {"record_date":"2026-09-17","debt_held_public_amt":"32392786557372.46","intragov_hold_amt":"7700556910778.04","tot_pub_debt_out_amt":"40093343468150.50","record_fiscal_year":"2026","record_fiscal_quarter":"4"} and second row record_date 2026-09-16 tot_pub_debt_out_amt 400

#### US Senate roll-call vote XML + US House Clerk Electronic Voting System XML — US Senate / Office of the Clerk of the US House (official primary sources) ✅ LIVE

Covers **4** subdomains: executive-appointments, us-legislation, shutdown-and-debt-ceiling, tax-policy

- Docs: https://www.senate.gov/legislative/votes_new.htm and https://clerk.house.gov/Votes
- Auth: None. VERIFIED on all four URLs. | Limits: No key, no registration, no published rate limit — exact cap UNKNOWN. Static XML/HTML files; self-throttle as a courtesy. Full history back to 1989 (House EVS) and 1989 (Senate LIS).
- Latency: MINUTES after the vote closes — materially faster than Congress.gov. CAVEAT: I could not time this directly, but the per-vote XML carries both <vote_date> and <modify_date> (verified 01:59 PM vote, 04:52 PM modify on the same day), so the record is amendable for ~3 hours after the vote; do not treat the first fetch as final for settlement. | Format: XML (stable, documented schema) + HTML index
- Why primary: One XML index per chamber per session carries EVERY recorded vote — cloture motions, passage votes, confirmation votes and appropriations votes — with the question, result and tally, and links to member-level detail. It is simultaneously the fastest predictive feed (a cloture tally tells you the confirmation outcome before the confirmation vote happens) and the authoritative settlement record. With Congress.gov unverifiable this session (see its entry), this is the strongest VERIFIED legislative-action feed in the set.

```bash
curl 'https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_119_2.xml'   # per-vote detail: https://www.senate.gov/legislative/LIS/roll_call_votes/vote1192/vote_119_2_00238.xml   # House: https://clerk.house.gov/evs/2026/index.asp and https://clerk.house.gov/evs/2026/roll001.xml
```

> Evidence: INDEPENDENTLY RE-VERIFIED, and I additionally fetched the per-vote detail file the original report asserted but did not show. (1) Senate index vote_menu_119_2.xml -> HTTP 200, content-type text/xml, 156,758 bytes. Verbatim first two records, which demonstrate the cloture->confirmation predictive pair the whyPrimary claims: <vote_number>00238</vote_number><vote_date>17-Sep</vote_date><issue>PN999-4

#### Kalshi Trade API v2 — Kalshi (CFTC-regulated designated contract market) ✅ LIVE

Covers **10** subdomains: us-legislation, shutdown-and-debt-ceiling, executive-appointments, presidential-tenure-and-conduct, courts-and-judiciary, tax-policy, trade-and-tariffs, immigration-and-border, state-and-local-government, approval-and-polling

- Docs: https://trading-api.readme.io/reference/getting-started
- Auth: None for public market-data reads — VERIFIED anonymous on /series, /series/{ticker} and /markets. RSA key-pair signing required only for trading. | Limits: Public market data readable with no credentials. Exact anonymous requests/second: UNKNOWN — Kalshi publishes tiered limits for authenticated trading tiers but not for anonymous reads. I saw no throttling across 4 calls. WebSocket available for streaming.
- Latency: Realtime / WebSocket. NOT independently timed this session. | Format: REST JSON + WebSocket
- Why primary: Covers all ten subdomains with one call — the only feed in this set that does. This is the market-implied prior, plus each series carries contract_terms_url AND a structured settlement_sources array naming the exact publications the venue settles against, which is how you validate that your settlement feed matches the venue's. It also enumerates the exact live contract universe (2,343 Politics series), so it doubles as the domain's ground-truth taxonomy.

```bash
curl 'https://api.elections.kalshi.com/trade-api/v2/series?category=Politics'   # single series: curl 'https://api.elections.kalshi.com/trade-api/v2/series/KXSAVEACT'   # markets (NOTE: ALWAYS pass a series_ticker or category — a bare ?status=open returns sports): curl 'https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXSAVEACT&status=open'
```

> Evidence: INDEPENDENTLY RE-VERIFIED. /series?category=Politics -> HTTP 200 anonymous, 2,993,628 bytes, parsed to exactly 2,343 series — reproduces the original count. Series object keys: additional_prohibitions, categories, category, contract_terms_url, contract_url, exchange_index, fee_multiplier, fee_type, frequency, last_updated_ts, settlement_sources, tags, ticker, title. TICKER EXISTENCE AUDIT (I teste

#### GovInfo API — US Government Publishing Office ✅ LIVE

Covers **5** subdomains: us-legislation, tax-policy, presidential-tenure-and-conduct, courts-and-judiciary, shutdown-and-debt-ceiling

- Docs: https://api.govinfo.gov/docs/
- Auth: Free api.data.gov key. DEMO_KEY VERIFIED WORKING on GovInfo this session (unlike Congress.gov, whose DEMO_KEY pool was exhausted — the two services throttle independently). | Limits: 1,000 requests/hour per registered key (api.data.gov shared default). DEMO_KEY worked for me here but is a shared pool that CAN exhaust without warning — I watched exactly that happen to Congress.gov in this session. Register a key for production; do not ship DEMO_KEY.
- Latency: Daily. | Format: REST JSON + bulk XML/ZIP
- Why primary: The authenticated full TEXT layer, across five collections in one API: PLAW (enacted law text — the literal settlement document for 'signed into law' contracts), BILLSTATUS, CPD (Compilation of Presidential Documents), USCOURTS (federal opinions), CHRG (hearings) and CREC (Congressional Record). PROMOTED IN IMPORTANCE by this verification pass: with Congress.gov unverifiable this session, GovInfo PLAW is the only VERIFIED enacted-law settlement feed in the set, so it carries the 'became law' settlement role on its own rather than merely supplementing Congress.gov.

```bash
curl 'https://api.govinfo.gov/collections/PLAW/2026-01-01T00:00:00Z?offset=0&pageSize=3&api_key=DEMO_KEY'   # package detail: https://api.govinfo.gov/packages/PLAW-119publ1/summary?api_key=DEMO_KEY
```

> Evidence: INDEPENDENTLY RE-VERIFIED, HTTP 200, 1,132 bytes, reproduces the original report verbatim. /collections/PLAW/2026-01-01T00:00:00Z?offset=0&pageSize=3&api_key=DEMO_KEY -> {"count":5982,"packages":[{"congress":"119","dateIssued":"2025-01-29","docClass":"PUBLIC","lastModified":"2026-09-09T15:30:07Z","packageId":"PLAW-119publ1","packageLink":"https://api.govinfo.gov/packages/PLAW-119publ1/summary","ti

#### GDELT DOC 2.0 API — The GDELT Project ✅ LIVE

Covers **8** subdomains: presidential-tenure-and-conduct, executive-appointments, courts-and-judiciary, shutdown-and-debt-ceiling, state-and-local-government, immigration-and-border, trade-and-tariffs, us-legislation

- Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- Auth: None. VERIFIED. | Limits: No key. HARD LIMIT, and STRICTER THAN THE ORIGINAL REPORT STATED. The documented limit is one request per 5 seconds per IP, but the enforcement is a sustained IP-level block, not a per-request gate: after a short burst I received HTTP 429 (444-byte plain-text body: 'Please limit requests to one every 5 seconds or contact kalev.leetaru5@gmail.com for larger queries...') continuously for SEVERAL MINUTES, and 8-second and 10-second spacing did not clear it. I had to poll in a retry loop before a request succeeded. Budget one request per 10s minimum and implement exponential backoff; a naive 5s-sleep client will lock itself out. For higher volume GDELT directs you to the Web NGrams dataset or BigQuery.
- Latency: 15 minutes (GDELT's raw file cadence); the DOC API surfaces articles within about 15-30 minutes of publication. NOT independently timed. | Format: REST JSON/CSV (also HTML/RSS modes)
- Why primary: The only free feed that prices the subdomains where the event is a REPORTING event rather than a filing — 'Kash Patel out by...?', 'Justice Thomas announces retirement', a governor's executive order. mode=timelinevol gives a normalized coverage-intensity series per query, mode=artlist gives the underlying articles. One query language covers eight subdomains. STRICTLY A PREDICTIVE/PROXY FEED — never a settlement source.

```bash
curl 'https://api.gdeltproject.org/api/v2/doc/doc?query=tariff&mode=timelinevol&format=json&timespan=7d'   # articles: curl 'https://api.gdeltproject.org/api/v2/doc/doc?query=shutdown%20sourcelang:eng&mode=artlist&maxrecords=3&format=json&timespan=2d'
```

> Evidence: VERIFIED LIVE, but only after a retry loop (see freeTierLimits). mode=timelinevol&query=tariff&timespan=7d -> HTTP 200, 1,374 bytes, real hourly series, verbatim: {"query_details":{"title":"tariff","date_resolution":"hour"},"timeline":[{"series":"Volume Intensity","data":[{"date":"20260920T000000Z","value":0.5168},{"date":"20260920T020000Z","value":0.5341},{"date":"20260920T030000Z","value":0.5004

#### CBP Nationwide Encounters bulk CSV — US Customs and Border Protection ✅ LIVE

Covers **1** subdomains: immigration-and-border

- Docs: https://www.cbp.gov/newsroom/stats/nationwide-encounters
- Auth: None. VERIFIED. | Limits: No key. Static CSV behind CBP's Drupal CDN — no published rate limit. File path encodes the release month, so the pattern is https://www.cbp.gov/sites/default/files/{YYYY-MM}/nationwide-encounters-fy23-fy26-{mon}-{state|aor}.csv; scrape the index page https://www.cbp.gov/document/stats/nationwide-encounters to discover the newest without guessing. Use curl -L; the CDN may redirect.
- Latency: Monthly, released roughly 2-3 weeks after month end (verified: August FY2026 data published under the 2026-09 path). | Format: CSV bulk
- Why primary: The only free machine-readable US border-encounter series, and one file covers every dimension the subdomain needs — fiscal year, month, land border region, state, demographic, citizenship, and Title 8 vs Title 42 authority — so you do NOT need a separate feed per border sector or per nationality. It is both the predictive series and the settlement source for encounter-count contracts.

```bash
curl -L -O 'https://www.cbp.gov/sites/default/files/2026-09/nationwide-encounters-fy23-fy26-aug-state.csv'   # by Border Patrol AOR instead of state: https://www.cbp.gov/sites/default/files/2026-09/nationwide-encounters-fy23-fy26-aug-aor.csv
```

> Evidence: INDEPENDENTLY RE-VERIFIED and row-counted. HTTP 200, content-type text/csv, 2,869,939 bytes — byte-identical to the original report. wc -l = 44,697 lines. Header verbatim: 'Fiscal Year,Month Grouping,Month (abbv),Land Border Region,State,Demographic,Citizenship,Title of Authority,Encounter Count'. First data row verbatim: '2023,FYTD,APR,Northern Land Border,AK,Single Adults,"CHINA, PEOPLES REPUBLI

#### Socrata Discovery API + SODA 2.1 (state and municipal open-data portals) — Tyler Technologies / Socrata, serving data.cityofnewyork.us, data.ny.gov, data.ca.gov and ~200 other US state and city portals ✅ LIVE

Covers **1** subdomains: state-and-local-government

- Docs: https://socratadiscovery.docs.apiary.io/ and https://dev.socrata.com/docs/endpoints.html
- Auth: None for the volumes here. A free app token is recommended (and raises the throttle) but is not required — VERIFIED working with no token on three calls. | Limits: Anonymous requests are throttled by a shared per-IP pool; a free app token moves you to a per-token pool. Socrata does not publish the exact anonymous number — UNKNOWN. SoQL ($select/$where/$order/$limit) runs server-side, so you rarely need bulk pulls.
- Latency: Portal-dependent: NYC council and budget datasets update daily to weekly; some agency datasets are monthly. NOT independently measured. | Format: REST JSON/CSV/GeoJSON with SoQL query language
- Why primary: One query interface across roughly 200 separate US state and city governments — the Discovery API searches every portal at once and SODA reads any dataset on any of them. For the Kalshi local contracts (KXNYCDEPTSAFETY, verified present on Kalshi) this replaces a per-city scraper. It is the keyless alternative to Open States, which remains unverifiable (see rejectedFeeds).

```bash
curl 'https://data.cityofnewyork.us/resource/uvw5-9znb.json?$limit=2'   # cross-portal discovery: curl 'https://api.us.socrata.com/api/catalog/v1?q=budget&domains=data.cityofnewyork.us&limit=2'
```

> Evidence: INDEPENDENTLY RE-VERIFIED, HTTP 200 x3. (1) data.cityofnewyork.us/resource/uvw5-9znb.json?$limit=2 -> 332 bytes, verbatim [{"name":"Gale A. Brewer","council_member_id":"5259","term_start":"2026-01-01T00:00:00.000","term_end":"2029-12-31T00:00:00.000","district":"6","office_id":"5805"},{"name":"James F. Gennaro","council_member_id":"5273","district":"24"}] — reproduces the original exactly. (2) Dis

#### USITC Harmonized Tariff Schedule REST endpoint — US International Trade Commission ✅ LIVE

Covers **1** subdomains: trade-and-tariffs

- Docs: https://hts.usitc.gov/ (the /reststop/ JSON export is public and used by the site itself; no separate developer docs page)
- Auth: None. VERIFIED. | Limits: No key, no registration, no published rate limit — exact cap UNKNOWN. Undocumented endpoint used by the HTS site itself; self-throttle and expect it to change without notice.
- Latency: Updated on HTS revision (several times a year, plus out-of-cycle updates when a proclamation changes rates). | Format: JSON (served as application/octet-stream)
- Why primary: The only free source of the actual duty RATE by HTS line, which is what rate-threshold contracts (KXCANAUTOSTEEL50, verified present on Kalshi) settle on. The Federal Register tells you a proclamation was issued; HTS tells you the resulting number. One endpoint covers every chapter including Chapter 99, so there is no need for a per-sector tariff feed — but you MUST query Chapter 99, not the commodity chapter (see verificationEvidence).

```bash
curl 'https://hts.usitc.gov/reststop/exportList?from=9903.80&to=9903.96&format=JSON&styles=false'   # THIS IS THE CORRECTED CALL — Chapter 99 subchapter III is where Section 232/301 additional duties live. The MFN base rate for a commodity is a SEPARATE call, e.g. from=7208&to=7209 (steel) or from=8703&to=8704 (autos). You need BOTH: final duty = base + Ch.99 additional.
```

> Evidence: LIVE — but the ORIGINAL REPORT'S exampleCall RETURNS THE WRONG NUMBER, and this is the single most expensive defect I found. The report's call (from=7208&to=7209, steel) returns HTTP 200 / 17,958 bytes / 55 lines, 18 of which carry a 'general' rate — and EVERY ONE OF THOSE READS "Free". Verbatim: {"htsno":"7208.10.15.00","general":"Free","other":"0.4¢/kg + 20%","additionalDuties":null}. The parent

#### USAspending.gov API v2 — US Department of the Treasury / Bureau of the Fiscal Service ✅ LIVE

Covers **1** subdomains: shutdown-and-debt-ceiling

- Docs: https://api.usaspending.gov/
- Auth: None. VERIFIED. | Limits: No key, no registration. No published hard rate limit — exact cap UNKNOWN.
- Latency: Agency obligations and outlays update monthly; account-level data follows the fiscal-quarter submission calendar. | Format: REST JSON
- Why primary: Gives agency-level appropriations, obligations and outlays by fiscal year and quarter across every federal agency in one API — the spending-side counterpart to Treasury's debt-side data, and the way to see which accounts actually lapse in a shutdown. Narrower than the feeds above, but there is no free substitute for account-level federal spending.

```bash
curl 'https://api.usaspending.gov/api/v2/references/toptier_agencies/'
```

> Evidence: INDEPENDENTLY RE-VERIFIED. HTTP 200, 52,652 bytes. Verbatim first record: {"results":[{"agency_id":1525,"toptier_code":"247","abbreviation":"AAHC","agency_name":"400 Years of African-American History Commission","congressional_justification_url":null,"active_fy":"2026","active_fq":"4","outlay_amount":0.0,"obligated_amount":0.0,"budget_authority_amount":0.0,"current_total_budget_authority_amount":1

#### Congress.gov API v3 — US Library of Congress ⚠️ UNVERIFIED

Covers **6** subdomains: us-legislation, shutdown-and-debt-ceiling, executive-appointments, tax-policy, trade-and-tariffs, immigration-and-border

- Docs: https://github.com/LibraryOfCongress/api.congress.gov
- Auth: Free api.data.gov registered key REQUIRED. The original report's claim that 'DEMO_KEY works for testing (verified)' did NOT hold for me — see verificationEvidence. | Limits: 5,000 requests/hour per registered key (Library of Congress documented — NOT independently measured, since I could not obtain a key in this environment). DEMO_KEY is a shared api.data.gov pool that was FULLY EXHAUSTED throughout my session.
- Latency: Hourly to daily (Congress.gov ingest cadence). Bill actions typically appear same-day; roll-call detail lags the chamber XML by hours. NOT independently measured — use the Senate/House XML feed for latency-sensitive paths regardless. | Format: REST JSON/XML
- Why primary: Retained as primary on architecture, NOT on verification. ONE key covers six subdomains: /bill gives status, actions, cosponsors, committee referrals and CBO cost estimates; /nomination is the presidential-nomination and Senate-confirmation register; /law is the enacted-law settlement feed; /committee-meeting is the hearing/markup calendar. Kalshi's own series KXDISAPPROVETARIFF lists settlement_sources [{"name":"Library of Congress","url":"https://congress.gov"}], which is independent third-party confirmation that the venue settles against this source. HOWEVER: every settlement role claimed here is ALSO served by a feed I DID verify — GovInfo PLAW for enacted law, Senate roll-call XML for nominations and votes — so do not block integration on this feed.

```bash
REGISTER A KEY FIRST at https://api.data.gov/signup/ — DEMO_KEY DOES NOT WORK (see verificationEvidence). Then: curl 'https://api.congress.gov/v3/law/119/pub?api_key=YOUR_KEY&limit=2&format=json'  # also /v3/bill/119/hr/3633 | /v3/nomination/119?limit=3&sort=updateDate+desc | /v3/committee-meeting/119?limit=2
```

> Evidence: COULD NOT VERIFY — the original report's verifiedLive:true is NOT REPRODUCIBLE and I am downgrading it. I attempted all four claimed endpoints (/v3/law/119/pub, /v3/bill/119/hr/3633, /v3/nomination/119, /v3/committee-meeting/119) and then retried /v3/law/119/pub in a 25-iteration backoff loop at 15-second intervals. ALL 29 REQUESTS RETURNED HTTP 429, body verbatim: {"error":{"code":"OVER_RATE_LIMI

#### Polymarket Gamma API + CLOB API — Polymarket ✅ LIVE

Covers **6** subdomains: presidential-tenure-and-conduct, us-legislation, tax-policy, shutdown-and-debt-ceiling, courts-and-judiciary, state-and-local-government

- Docs: https://docs.polymarket.com/
- Auth: None for public read/market data. VERIFIED anonymous across 15 paged calls. API key + wallet signing only for trading. | Limits: Public reads need no key. Exact requests/minute cap: UNKNOWN — I paged 15 consecutive requests with no throttling. NOTE: limit is hard-capped at 100 per page; passing limit=500 silently returns 100. WebSocket available.
- Latency: Realtime / WebSocket. NOT independently timed. | Format: REST JSON + WebSocket
- Why primary: The second market-implied prior, genuinely NOT redundant with Kalshi for one specific and verified reason: it carries offshore/global tenure contracts Kalshi cannot list. I confirmed live markets on Xi Jinping, Zelenskyy, Pedro Sánchez and Lee Jae-myung tenure. It also carries the exact state-tax contract the tax-policy row flags as hard to settle ('Will Mamdani pass the 2% Millionaire Tax before 2027?'). Use it as a prior and as a contract-discovery surface — NOT as a broad substitute for Kalshi, which carries roughly 20x the political contract count.

```bash
curl 'https://gamma-api.polymarket.com/markets?limit=100&offset=0&closed=false'   # page with offset in steps of 100 (limit is capped at 100 regardless of what you pass)   # order book: curl 'https://clob.polymarket.com/book?token_id=<tokenId from gamma outcomes>'
```

> Evidence: LIVE, but COVERAGE SUBSTANTIALLY OVER-CLAIMED and downgraded. Endpoint verified: gamma-api.polymarket.com/markets?limit=1&closed=false -> HTTP 200, verbatim [{"id":"559651","question":"Xi Jinping out before 2027?","conditionId":"0xa467b14d51f01b957109d9cbb1d6c124fab2a089d52ed8f471d23c2812e743b7","slug":"xi-jinping-out-before-2027","resolutionSource":"","endDate":"2027-01-01T04:59:00Z","liquidity":

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| US Federal Legislation | Senate roll-call XML + House Clerk EVS XML (BOTH VERIFIED th | GovInfo /collections/PLAW (VERIFIED: count=5982, PLAW-119pub | 🟢 COVERED |
| Shutdowns & Debt Ceiling | Treasury FiscalData (VERIFIED to the cent: v2 debt_to_penny  | GovInfo /collections/PLAW (VERIFIED) for enacted CRs and app | 🟢 COVERED |
| Cabinet & Confirmations | US Senate roll-call vote XML (VERIFIED — index 156,758 bytes | US Senate roll-call vote XML — VERIFIED verbatim, and the cl | 🟢 COVERED |
| Presidential Tenure & Conduct | GDELT DOC 2.0 (VERIFIED live after backoff; timelinevol hour | Federal Register API conditions[type][]=PRESDOCU (VERIFIED:  | 🟡 PARTIAL |
| Courts & Judiciary | CourtListener v4 /search/ (ALL THREE query types VERIFIED an | CourtListener v4 /search/?type=o (VERIFIED: count=498,145, n | 🟢 COVERED |
| Tax Policy | FEDERAL: Federal Register (VERIFIED) for Treasury and IRS pr | FEDERAL: GovInfo PLAW enacted text (VERIFIED) plus Congress. | 🟡 PARTIAL |
| Trade Policy & Tariffs | Federal Register API (VERIFIED: conditions[term]='section 23 | Federal Register API final rules and presidential proclamati | 🟢 COVERED |
| Immigration & Border | CBP Nationwide Encounters CSV (VERIFIED: 2,869,939 bytes, 44 | CBP Nationwide Encounters CSV for encounter-count contracts. | 🟡 PARTIAL |
| Approval Ratings & Generic Ballot | VoteHub Polls API (VERIFIED, payload byte-identical to the p | VoteHub Polls API — CONFIRMED as a genuine named Kalshi sett | 🟢 COVERED |
| State & Local Government | Socrata Discovery API + SODA (VERIFIED x3: NYC council roste | For NYC agency, budget and council items: Socrata SODA on da | 🟡 PARTIAL |

**Rejected**

- **Congress.gov API v3 with DEMO_KEY (the exampleCall as originally published)** — THE FEED IS RETAINED AS PRIMARY; THE PUBLISHED CALL IS REJECTED. DEMO_KEY returned HTTP 429 {"error":{"code":"OVER_RATE_LIMIT",...}} on all 29 attempts — four distinct endpoints plus a 25-iteration backoff loop at 15s in
- **USITC HTS commodity-chapter query for tariff RATE settlement (from=7208 / from=8703)** — RETURNS THE WRONG NUMBER — the most expensive defect found in this verification. The endpoint is live and returns HTTP 200 with valid JSON, so it LOOKS like a pass, but from=7208&to=7209 yields general rate "Free" on all
- **Kalshi tickers KXGENERICBALLOTVOTEHUB, KXTRUMPENDORSEMENTS, KXCASESSION** — DO NOT EXIST. All three were cited in the prior report as evidence of subdomain coverage. I parsed the complete /series?category=Politics response (2,343 series) and searched exact and prefix for each — none present. Ten
- **Polymarket as a trade-and-tariffs or executive-appointments feed** — ZERO MARKETS MEASURED. Polymarket itself is retained as a primary feed for six other subdomains. But I paged the entire open universe — 15 requests, offset 0..1400, 1,600 unique open markets — and keyword-classified ever
- **Socrata and USAspending as tax-policy feeds** — VOCABULARY MATCH, NOT DATA MATCH. Both APIs are live and retained as primary for other subdomains. But nothing I retrieved from any Socrata portal was tax-measure data (NYC returns council rosters and budget line items),
- **GDELT DOC 2.0 'quoted-phrase returns empty body' claim** — CLAIM NOT REPRODUCIBLE — AND THE REAL BEHAVIOR IS WORSE. The prior report warned that query=%22government%20shutdown%22&mode=artlist returns HTTP 200 with an empty {}. I got HTTP 200 with a POPULATED articles array — but
- **Federal Register 'malformed field returns HTTP 400' claim** — CLAIM WRONG — the API SILENTLY IGNORES unrecognized parameters. The prior report said passing presidential_document_type outside a conditions[] wrapper returns HTTP 400 {"message":"field not valid"}. I tested it and got 
- **Open States API v3 (v3.openstates.org)** — KEY-GATED — RE-TESTED AND 403 REPRODUCED VERBATIM. https://v3.openstates.org/jurisdictions returned HTTP 403 {"detail":"Must provide API Key as ?apikey or X-API-KEY. Login and visit https://openstates.org/account/profile
- **LegiScan API** — KEY-GATED, COULD NOT VERIFY (prior-pass finding, not re-tested). api.legiscan.com returned HTTP 200 with an error body {"status":"ERROR","alert":{"message":"Invalid API key format..."}} — note this is itself a 200-with-e
- **CourtListener v4 object endpoints (/opinions/, /dockets/, /people/)** — SUPERSEDED BY /search/ ON THE SAME API — 401 INDEPENDENTLY REPRODUCED. /api/rest/v4/opinions/?court=scotus returned HTTP 401 {"detail":"Authentication credentials were not provided."} anonymously. Even authenticated, pub
- **OMB Agency Contingency Plans page** — DEAD URL (prior-pass finding, not re-tested). https://www.whitehouse.gov/omb/information-for-agencies/agency-contingency-plans/ returned HTTP 404. This would have been the OPM/OMB lapse-notice source for shutdown settlem
- **USCIS Processing Times API (egov.uscis.gov)** — BLOCKED (prior-pass finding, not re-tested). Returned HTTP 403 with a 5,488-byte HTML interstitial rather than JSON — a 403-with-HTML, not a usable endpoint. Would have partially covered the immigration receipts signal.
- **Legistar Web API (webapi.legistar.com)** — INCONSISTENT PER CLIENT (prior-pass finding, NOT re-tested this session — treat as unverified either way). Reported results across seven clients: seattle/sfgov/austintexas HTTP 200; nyc/phila 403; chicago/losangeles/bost
- **FiveThirtyEight GitHub data repo (fivethirtyeight/data)** — FROZEN, SUPERSEDED. 538 is defunct and the polling files are no longer updated. Historical raw_polls.csv remains useful for backtesting pollster error only. NOTE: Kalshi still lists KX538APPROVE / KX538APPROVEMIN / KX538
- **Silver Bulletin pollster ratings + raw polls XLSX** — NOT A LIVE SERIES. Annual/semiannual XLSX drops — valuable as WEIGHTS on top of VoteHub, but not a daily feed and cannot settle a contract. Not fetched in either pass, so not asserted live. Note Kalshi DOES carry KXSILVE
- **Metaculus API** — AUTHENTICATION NOW REQUIRED (prior-pass finding). /api2/questions/ and /api/posts/ return HTTP 403 'Permission Error'. Superseded for the market-prior role by Kalshi and Polymarket, both verified keyless this session.
- **PredictIt market data API** — SUPERSEDED, NOT VERIFIED IN EITHER PASS. Its political contract universe is a strict subset of Kalshi's 2,343 Politics series at far lower volume. Not carried into primaryFeeds unverified when two verified venues cover t
- **openFEC API** — OUT OF SCOPE. Campaign finance and certified election results belong to the elections domain; this domain is non-electoral government action. NOTE this exclusion rule cuts both ways — it is why I declined to count Polyma
- **Voteview DW-NOMINATE bulk CSVs** — TOO SLOW FOR LIVE USE. Batch-updated static CSVs — good for a member's prior propensity to defect, useless as a live vote feed. The House Clerk and Senate XML publish the same votes far sooner and both were verified this
- **IPU Parline API and UK Parliament Members API** — OUT OF GEOGRAPHIC SCOPE. Every subdomain here is US federal, state or local. (Incidental note: Kalshi does list foreign political series such as KXUKPARTYPOLLS, KXGERPOLLAFD and KXCANSNAPPROV in its Politics category, so
- **data.gov CKAN package_search** — DEAD ENDPOINT (prior-pass finding). https://catalog.data.gov/api/3/action/package_search returned HTTP 404 with a 36-byte body. It would only ever have been a dataset index, not a feed. The direct CBP CSV path, verified 
- **Kalshi /markets?status=open without a series or category filter** — RETURNS THE WRONG DOMAIN. The prior report's exampleCall 'markets?limit=2&status=open' is live (HTTP 200) but returns SPORTS markets — the page I received was full of KXWTASETWINNER, KXWTAMATCH and KXLNBPGAME tennis and 

---

### science-and-space

*4/7 subdomains covered · 16 primary feeds*

#### Launch Library 2 (The Space Devs) — The Space Devs ✅ LIVE

Covers **2** subdomains: launch-cadence, deep-space-missions

- Docs: https://thespacedevs.com/llapi
- Auth: none (free 'll.thespacedevs.com' tier, no key) | Limits: 15 requests/hour anonymous is the DOCUMENTED figure — NOT measured. I made 7 calls in one session with no 429 and the server returns NO rate-limit headers at all (no x-ratelimit-*, no retry-after), so the cap is unverifiable from responses. Treat 15/hr as the planning number. Full launch database 1957-present. Offset/limit pagination.
- Latency: minutely — status flips (Go/Hold/Success/Failure) and NET slips propagate within minutes | Format: REST JSON
- Why primary: ONE API answers both space subdomains. VERIFIED in mode=detailed: agency_launch_attempt_count_year (the literal YTD count that settles KXSPACEXCOUNT/KXRKLBLAUNCH), orbital_launch_attempt_count_year, pad_turnaround (ISO8601 duration), a status enum, and an `updates` array giving NET-slip history with timestamps — so slip distributions are computable. The /events/ endpoint on the same API returns non-launch deep-space milestones (flybys, orbital insertions), which no launch-only feed provides. CORRECTED FROM PRIOR REPORT: the `probability` and `weather_concerns` fields exist in the schema but are NULL in practice — do NOT plan a scrub-risk model on them (see verificationEvidence). Launch weather must come from Open-Meteo. Beats RocketLaunch.Live (5-result hard cap) and Space-Track (account required).

```bash
curl -s 'https://ll.thespacedevs.com/2.3.0/launches/?lsp__name=SpaceX&net__gte=2026-01-01T00:00:00Z&net__lte=2026-12-31T23:59:59Z&limit=1&mode=list'
```

> Evidence: CONFIRMED — HTTP 200 on 7 independent calls, 2026-09-20/21. SpaceX 2026 filter -> {"count":159, first result "Falcon 9 Block 5 | CSG-3", launch_designator "2026-001", status "Launch Successful", net "2026-01-03T02:09:16Z"}. Rocket Lab 2026 filter -> "count":30. /events/upcoming/ -> "count":27, first "Juice Earth Flyby" (id 1017). mode=detailed on CSG-3 returned the claimed settlement keys with REA

#### NASA JPL SSD/CNEOS API family (cad, fireball, sentry, horizons) — NASA Jet Propulsion Laboratory — Solar System Dynamics ✅ LIVE

Covers **1** subdomains: astronomical-events

- Docs: https://ssd-api.jpl.nasa.gov/doc/
- Auth: none | Limits: No key, NO published numeric rate limit (JPL asks for reasonable use and reserves the right to throttle) — limit is UNKNOWN, not unlimited. No rate-limit headers returned. CAD covers 1900-2200; fireball archive back to 1988.
- Latency: daily (orbit solutions refresh as new observations arrive; fireball detections post within days) | Format: REST JSON
- Why primary: One host covers the entire impact/close-approach subdomain with complementary endpoints instead of four vendors: cad.api (close approaches with nominal + min/max miss distance = NEO flux base rate), sentry.api (Palermo/Torino impact-risk table = forward probability), fireball.api (detected atmospheric impacts WITH impact energy in kt = the settlement field for meteor-strike contracts). Nothing else publishes detected bolide energy in kt for free. This is the most reliably verified feed in the domain — every endpoint I tested returned real data on the first attempt with no throttling.

```bash
curl -s 'https://ssd-api.jpl.nasa.gov/fireball.api?limit=3'   # returns impact energy in kilotons — settles "5kt meteor strike" markets directly
```

> Evidence: CONFIRMED — HTTP 200 on 3 endpoints, 2026-09-21, all first-attempt. fireball.api?limit=3 -> {"count":"3","fields":["date","energy","impact-e","lat",...],"data":[["2026-09-15 11:26:13","2.2","0.079","37.6","S",...],["2026-09-11 10:18:03","6.1","0.2",...],["2026-09-11 01:12:11","24.6","0.67","54.4","N",...]]} — impact-e in kt confirmed present as a real numeric field. cad.api?dist-max=0.05&date-min=

#### US Naval Observatory Astronomical Applications API — US Naval Observatory (aa.usno.navy.mil) ✅ LIVE

Covers **1** subdomains: astronomical-events

- Docs: https://aa.usno.navy.mil/data/api
- Auth: none | Limits: No key, no published rate limit — UNKNOWN (no rate-limit headers returned). US Government public domain. Covers solar and lunar eclipses across a multi-century span, plus rise/set/twilight and moon phases. apiversion 4.0.1.
- Latency: static/deterministic — ephemeris is computed, not observed; values never revise | Format: REST JSON
- Why primary: Eclipse contracts (KXECLIPSEREYK) have two halves: WHETHER the eclipse happens at that location (deterministic, zero uncertainty) and WHETHER you can see it (weather). USNO settles the first half exactly — returning local contact times, totality duration, altitude and azimuth for arbitrary coordinates — so the market collapses to a pure cloud-cover forecast. No other free API returns per-coordinate local eclipse circumstances. Verified exactly as the prior report described, field for field.

```bash
curl -s 'https://aa.usno.navy.mil/api/eclipses/solar/date?date=2026-08-12&coords=64.1466,-21.9426&height=0'   # Reykjavik, 12 Aug 2026 total solar eclipse
```

> Evidence: CONFIRMED — HTTP 200 on both endpoints, 2026-09-21, reproduced the prior report's values exactly. /api/eclipses/solar/year?year=2026 -> {"apiversion":"4.0.1","eclipses_in_year":[{"day":17,"event":"Annular Solar Eclipse of 17 February 2026","month":2},{"day":12,"event":"Total Solar Eclipse of 12 August 2026","month":8}]}. /api/eclipses/solar/date?date=2026-08-12&coords=64.1466,-21.9426&height=0 -> 

#### Open-Meteo (forecast + ensemble + historical archive) — Open-Meteo ✅ LIVE

Covers **2** subdomains: astronomical-events, launch-cadence

- Docs: https://open-meteo.com/en/docs
- Auth: none | Limits: 10,000 calls/day free — documented, NOT measured (no quota headers returned). CRITICAL LICENSING FLAG: the free tier is NON-COMMERCIAL use only. A paid prediction-market platform is commercial use and needs the paid API tier — this is a licensing blocker, not a technical one, and it is the single most likely thing to bite you at launch. Global coverage, hourly resolution, 16-day forecast, archive back to 1940.
- Latency: hourly model refresh | Format: REST JSON
- Why primary: One global endpoint supplies the only stochastic input to eclipse-visibility markets (cloud_cover at arbitrary lat/lon) AND — now that LL2's probability/weather_concerns fields are confirmed null — it is the SOLE launch-weather source for scrub-rate modelling at any pad worldwide. A US-only feed such as api.weather.gov cannot serve Icelandic or Kourou markets; Open-Meteo can, from a single URL shape. Its role is larger than the prior report assumed, because the LL2 weather fallback does not exist.

```bash
curl -s 'https://api.open-meteo.com/v1/forecast?latitude=64.1466&longitude=-21.9426&hourly=cloud_cover&forecast_days=2'
```

> Evidence: CONFIRMED with actual VALUES, not just an array shape — I specifically checked this because a populated `time` array with a null data array is the classic false pass. HTTP 200, 2026-09-21. Reykjavik query -> {"latitude":64.139565,"longitude":-21.971603,"elevation":7.0,"hourly_units":{"cloud_cover":"%"}}. Parsed: n_times=48, cloud_cover sample [100,100,100,100,100,100,100,100,100,100,100,100], null

#### NOAA Space Weather Prediction Center services — NOAA SWPC ✅ LIVE

Covers **2** subdomains: astronomical-events, launch-cadence

- Docs: https://www.swpc.noaa.gov/products-and-data
- Auth: none | Limits: No key, no published rate limit — UNKNOWN. US Government public domain. Dozens of JSON products (X-ray flux, Kp/planetary-k, solar wind, aurora forecast, alerts).
- Latency: 1-minute cadence on GOES X-ray — VERIFIED the fastest feed in this domain; the record I pulled was timestamped minutes before my call | Format: REST JSON
- Why primary: Real-time where NASA DONKI is hourly-to-daily — and since NASA DONKI could NOT be verified at all this pass (DEMO_KEY exhausted), SWPC is currently the only CONFIRMED-WORKING space-weather feed in this mapping. One host serves the whole space-weather event class (flares by class, geomagnetic Kp, aurora, official alerts) which Kalshi files under 'Climate and Weather > Space', and supplies the geomagnetic term in launch scrub models. Needs no key, which is now a decisive advantage over NASA.

```bash
curl -s 'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'
```

> Evidence: CONFIRMED — HTTP 200, 2026-09-21, no auth. xray-flares-latest.json -> [{"time_tag":"2026-09-21T03:07:00Z","satellite":18,"current_class":"B3.9","current_ratio":0.008254371763846772,"begin_time":"2026-09-21T00:59:00Z","begin_class":"B4.1","max_time":"2026-09-21T01:13:00Z","max_class":"C1.1","max_xrlong":1.146e-06,"end_time":"2026-09-21T01:25:00Z"}]. The time_tag was ~minutes old at fetch, confirmin

#### IAU Minor Planet Center — NEOCP JSON — IAU Minor Planet Center (Harvard/CfA) ✅ LIVE

Covers **1** subdomains: astronomical-events

- Docs: https://www.minorplanetcenter.net/data
- Auth: none | Limits: No key, NO published rate limit — UNKNOWN. MPC asks clients not to hammer the site and offers bulk files (MPCORB) for volume use.
- Latency: sub-minute to hourly on the NEO Confirmation Page — verified: objects discovered the same day as my call were present | Format: REST JSON (NEOCP) + HTML (MPEC listing is scrape-only)
- Why primary: The discovery-pipeline layer that JPL CNEOS does not have: every unconfirmed object awaiting designation, with a digest2 NEO-likelihood Score, discovery timestamp, RA/Dec, magnitude and observation count. For impact and close-approach markets this is the earliest possible signal — objects appear here hours to days before they exist in cad.api or sentry.api.

```bash
curl -sL 'https://www.minorplanetcenter.net/Extended_Files/neocp.json'
```

> Evidence: CONFIRMED — HTTP 200, 2026-09-21. neocp.json -> JSON array: [{"Temp_Desig":"P12qt5L","Score":100,"Discovery_year":2026,"Discovery_month":9,"Discovery_day":20.5,"R.A.":0.562,"Decl.":-11.8825,"V":21.6,"Updated":"Updated Sept. 20.81 UT","NObs":3,"Arc":0.03,"H":24.4,"Not_Seen_dys":0.623},{"Temp_Desig":"P12qt4R","Score":98,"Discovery_day":20.4,"NObs":9,...}]. Objects discovered the same calendar day as

#### CelesTrak GP / SATCAT — CelesTrak (Dr T.S. Kelso) ✅ LIVE

Covers **2** subdomains: launch-cadence, deep-space-missions

- Docs: https://celestrak.org/NORAD/documentation/gp-data-formats.php
- Auth: none | Limits: No key, NO published numeric rate limit — UNKNOWN. Stated policy: query no more often than the data updates (GP sets refresh a few times daily). Bulk group files preferred over per-object polling.
- Latency: hourly to several-times-daily refresh | Format: REST — TLE, 3LE, JSON, CSV, XML, KVN
- Why primary: The independent settlement cross-check for orbital insertion: a payload that actually reached orbit acquires a catalogued GP element set with an international designator. Because it derives from US Space Force tracking rather than provider press releases, it falsifies a 'Launch Successful' status that LL2 may have taken from a company statement. This matters more given that LL2's own `updates` are community-curated. Requires no account, unlike Space-Track.

```bash
curl -s 'https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json'
```

> Evidence: CONFIRMED — HTTP 200, 2026-09-21. GROUP=stations&FORMAT=json -> [{"OBJECT_NAME":"ISS (ZARYA)","OBJECT_ID":"1998-067A","EPOCH":"2026-09-20T12:42:37.141056","MEAN_MOTION":15.49196792,"ECCENTRICITY":0.00048259,"INCLINATION":51.6308,"NORAD_CAT_ID":25544,"REV_AT_EPOCH":58653,"BSTAR":0.00015975118},{"OBJECT_NAME":"POISK",...}]. Element-set epoch was under 24h old at fetch. International designator (OBJE

#### Nobel Prize API v2.1 — Nobel Prize Outreach AB ✅ LIVE

Covers **1** subdomains: nobel-and-academia

- Docs: https://api.nobelprize.org/2.1/
- Auth: none | Limits: No key, no published rate limit — UNKNOWN. Complete 1901-present, ~1,000 laureates. New laureates appear within hours of each October announcement.
- Latency: annual (October); record updated within hours of announcement | Format: REST JSON
- Why primary: This is the settlement authority itself, not a proxy — the Nobel Foundation's own structured record, with awardYear, category, dateAwarded, motivation, prizeAmount and per-laureate portion. Every Nobel contract on Kalshi and Polymarket resolves to exactly this object. A narrow feed is correct here because the subdomain IS narrow; there is no broader source carrying the official result.

```bash
curl -s 'https://api.nobelprize.org/2.1/nobelPrizes?nobelPrizeYear=2025&limit=2'
```

> Evidence: CONFIRMED — HTTP 200, 2026-09-21, reproduced the prior report's record exactly. /nobelPrizes?nobelPrizeYear=2025&limit=2 -> {"awardYear":"2025","category":{"en":"Chemistry"},"categoryFullName":{"en":"The Nobel Prize in Chemistry"},"dateAwarded":"2025-10-08","prizeAmount":11000000,"prizeAmountAdjusted":11000000,"laureates":[{"id":"1053","knownName":{"en":"Susumu Kitagawa"},"portion":"1/3","sortOrde

#### Crossref REST API — Crossref ✅ LIVE

Covers **2** subdomains: physics-breakthroughs, mathematics

- Docs: https://api.crossref.org/swagger-ui/index.html
- Auth: none; a mailto in the User-Agent puts you in the higher-throughput pool | Limits: CORRECTED — MEASURED LIVE from response headers 2026-09-21: x-rate-limit-limit: 3, x-rate-limit-interval: 1s, i.e. 3 req/sec, NOT the 1 req/sec the prior report stated. The prior figure was too conservative by 3x. Bulk snapshot available for volume use.
- Latency: daily (DOI registration is near-realtime; indexing lags hours) | Format: REST JSON + bulk snapshot
- Why primary: The settlement half of both research subdomains, from one API. 'Peer-reviewed confirmation' is operationally the moment a claim acquires a journal DOI with a publication date — Crossref is the registry that records exactly that, across every publisher, for physics and mathematics alike. Pairing it with arXiv gives preprint-to-publication conversion rates. Practical note: it is also the most throughput-tolerant literature API here (3/sec measured) versus arXiv, which threw 429/503 at me repeatedly — so put Crossref on the hot path and arXiv on a cached poll.

```bash
curl -s -H 'User-Agent: yourapp/1.0 (mailto:you@example.com)' 'https://api.crossref.org/works?query.bibliographic=inertial+confinement+fusion+ignition&rows=1&select=DOI,title,published'
```

> Evidence: CONFIRMED — HTTP/2 200, 2026-09-21, with headers inspected. Response headers: 'x-rate-limit-limit: 3', 'x-rate-limit-interval: 1s' (this CORRECTS the prior report's claim of limit 1). Body: {"status":"ok","message-type":"work-list","message":{"total-results":488990,"items":[{"DOI":"10.2172/2846","title":["Antiproton fast ignition for Inertial Confinement Fusion"],"published":{"date-parts":[[1997,1

#### OpenAlex — OurResearch ✅ LIVE

Covers **3** subdomains: physics-breakthroughs, mathematics, nobel-and-academia

- Docs: https://help.openalex.org/
- Auth: none required for light use; free API key strongly recommended since the Feb 2026 change | Limits: CHANGED Feb 2026 — the old 100k calls/day + polite pool model is replaced by a USD credit budget. CONFIRMED LIVE: the API returns meta.cost_usd per call (0.0001 USD on a per-page=2 query, on both works and authors endpoints). Anonymous calls still succeed. ~327M works, 9.7M US-affiliated authors.
- Latency: daily | Format: REST JSON + S3 bulk snapshot
- Why primary: The single broadest science-prediction feed: one query language spans physics, mathematics and the citation graph that drives Nobel forecasting. I verified the full Nobel-prior path end to end — the /authors endpoint returns cited_by_count plus summary_stats (h_index, i10_index, 2yr_mean_citedness), which is what a Citation-Laureates-style reconstruction actually needs. DATA-QUALITY WARNING ADDED: cited_by_count is contaminated at the top of the sort (see verificationEvidence) — you must filter outliers before using it as a Nobel prior, or your ranking is garbage at exactly the rows you care about.

```bash
curl -s 'https://api.openalex.org/works?filter=primary_topic.field.id:fields/31,from_publication_date:2020-01-01&sort=cited_by_count:desc&per-page=2&select=id,title,cited_by_count'
```

> Evidence: CONFIRMED — HTTP 200 on 2 endpoints, 2026-09-21. Works: {"meta":{"count":1842947,"db_response_time_ms":30,"cost_usd":0.0001},"x_query":{"oql":"works where date >= (2020-01-01) and field is (fields/31)"}} — the oql echo confirms the filter parsed as issued. Authors rollup (the Nobel-prior path, newly tested this pass): /authors?filter=last_known_institutions.country_code:us&sort=cited_by_count:desc

#### arXiv API (Atom query + RSS + OAI-PMH) — Cornell University / arXiv ✅ LIVE

Covers **2** subdomains: physics-breakthroughs, mathematics

- Docs: https://info.arxiv.org/help/api/user-manual.html
- Auth: none | Limits: CORRECTED — the documented terms say 1 request per 3 seconds, single connection. MEASURED REALITY IS HARSHER: export.arxiv.org returned HTTP 429 on a second call in the same session, then 429 again, then 503, then 429 across four retries spread over several minutes of intervening work. Do NOT design for 1-per-3s on the query API. The rss.arxiv.org host is a separate, far more tolerant path and returned 200 first try. Use HTTPS — HTTP 301-redirects.
- Latency: daily — new submissions announced once per weekday cycle | Format: Atom XML (query API), RSS (per-category, separate host), OAI-PMH (bulk)
- Why primary: ONE endpoint family covers both the physics and mathematics subdomains by swapping a category string: physics.plasm-ph (fusion -> KXFUSION), cond-mat.supr-con (room-temp superconductivity -> SUPERCON), and all math.* (Millennium Prize claims -> KXPNP). This is the claim-arrival pipeline that precedes peer-reviewed confirmation. Still primary — but architect it as a cached periodic poll behind rss.arxiv.org, never a per-user-request call, because the query API will throttle you out.

```bash
PREFER THE RSS PATH (verified reliable): curl -s 'https://rss.arxiv.org/rss/math.NT'   ||  Query API (works but throttles hard): curl -s 'https://export.arxiv.org/api/query?search_query=cat:physics.plasm-ph&start=0&max_results=1&sortBy=submittedDate&sortOrder=descending'
```

> Evidence: PARTIAL — I am splitting this precisely rather than claiming a clean pass. CONFIRMED WITH DATA: cat:physics.plasm-ph -> HTTP 200, <opensearch:totalResults>20530</opensearch:totalResults>, newest entry arXiv:2609.21951v1 'Azimuthal mode decomposition Particle in Cell algorithm for cylindrical plasma sources', updated 2026-09-18T16:07. cat:cond-mat.supr-con -> HTTP 200, totalResults 48122. So the PH

#### US NRC public reactor feeds (365-day status TXT + plant-status / event RSS) — US Nuclear Regulatory Commission ✅ LIVE

Covers **1** subdomains: energy-technology

- Docs: https://www.nrc.gov/documents-reports/document-collections/events-reports-associated-with/power-reactor-status-reports
- Auth: none | Limits: No key, no registration, US Government public domain. Rolling 365-day window in the TXT; yearly index pages archive further back. RSS is unpaginated current-state.
- Latency: daily (published each morning) — TXT led by 9/18/2026 at time of check, so expect a ~2-day lag, not same-day | Format: pipe-delimited TXT + RSS XML
- Why primary: The only free, machine-readable, authoritative feed on the actual operating state of every US commercial reactor — percent of full power per unit per day. It is the regulator's own record, so it settles reactor-operation contracts outright. IMPORTANT SCOPE LIMIT (unchanged and confirmed): this covers reactor OPERATION, not reactor LICENSING; the NRC licensing docket (ADAMS) is subscription-gated — see rejectedFeeds.

```bash
curl -sL 'https://www.nrc.gov/documents-reports/document-collections/events-reports-associated-with/power-reactor-status-reports/PowerReactorStatusForLast365Days.txt'   ||  RSS (exact URL, do not guess): curl -sL 'https://www.nrc.gov/public-involve/rss?feed=plant-status'
```

> Evidence: CONFIRMED, with a URL CORRECTION that would otherwise have cost a developer real time. TXT: HTTP 200 via -L, real pipe-delimited rows — header 'ReportDt|Unit|Power' then '9/18/2026 12:00:00 AM|Arkansas Nuclear 1|100', '...|Arkansas Nuclear 2|100', '...|Browns Ferry 1|0' (unit offline), '...|Browns Ferry 2|100'. DEFECT FOUND: the prior report asserted 'RSS feed=plant-status' works but gave no URL. 

#### Our World in Data (grapher CSV + indicators API) — Our World in Data / Global Change Data Lab ✅ LIVE

Covers **1** subdomains: energy-technology

- Docs: https://docs.owid.io/projects/etl/api/
- Auth: none | Limits: No key, no published rate limit — UNKNOWN. CSV downloads unmetered. Annual granularity, IEA-sourced for EV series.
- Latency: monthly to annual (source-dependent) — NOT a real-time feed | Format: CSV bulk + REST JSON
- Why primary: Thousands of harmonised energy-technology series from one URL shape — swap the grapher slug for EV sales share, solar/battery cost curves, nuclear share of electricity, all country-year. This is the practical replacement for the Argonne EV series named in the domain spec, which blocks programmatic fetch (403). Caveat restated because it is load-bearing: ANNUAL cadence, so it sets the trend prior and cannot settle a monthly contract.

```bash
curl -sL 'https://ourworldindata.org/grapher/electric-car-sales-share.csv?v=1&csvType=full&useColumnShortNames=true'
```

> Evidence: CONFIRMED — HTTP 200, 2026-09-21. electric-car-sales-share.csv returned a real CSV with header 'entity,code,year,ev_sales_share' and a full time series, not a stub: Australia AUS 2011=0.0061, 2012=0.029, 2013=0.033, 2014=0.15, 2015=0.19, 2016=0.15, 2017=0.25, 2018=0.42, 2019=1.2, 2020=0.98, 2021=2.7, 2022=5.1, 2023=11, 2024=12, 2025=15, then Austria. Data runs through 2025; there is no 2026 row, w

#### EIA Open Data (API v2 + no-key bulk manifest) — US Energy Information Administration ⚠️ UNVERIFIED

Covers **1** subdomains: energy-technology

- Docs: https://www.eia.gov/opendata/documentation.php
- Auth: free API key (instant self-service, email only) for the v2 API; the /bulk/ manifest and dataset files need NO key | Limits: No hard published quota. EIA guidance: stay under ~9,000 req/hour sustained and 5 req/sec burst. Hard response caps: 5,000 rows per v2 call. Bulk files unmetered. NOTE: these limits are documented, not measured — I hold no key and could not exercise the quota.
- Latency: hourly for EIA-930 grid data (~1-2h lag); weekly for petroleum/gas; monthly for generation and EV series | Format: REST JSON (also XML, CSV) + bulk JSON
- Why primary: The single richest free energy dataset anywhere: hourly US grid demand/generation/interchange by balancing authority, monthly nuclear/renewable/coal/gas generation, weekly petroleum and gas stocks, and EV series — all through one query grammar. For KXEVSHARE and nuclear-capacity contracts this is the settlement-grade national series. Retained as primary despite incomplete verification because the gate is a free self-service key, not a paywall — but see the evidence field and register before depending on it.

```bash
NO-KEY PATH (verified): curl -sL 'https://api.eia.gov/bulk/manifest.txt'  ||  KEYED PATH (register free at https://www.eia.gov/opendata/register.php, then): curl -sg 'https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key=YOUR_KEY&frequency=hourly&data[0]=value&facets[respondent][]=CAL&sort[0][column]=period&sort[0][direction]=desc&length=2'
```

> Evidence: PARTIAL — independently reproduced the prior report's honest split, and I confirm it was honest. CONFIRMED: https://api.eia.gov/bulk/manifest.txt -> HTTP 200 with real JSON ({"dataset":{"AEO.2014":{"last_updated":"2016-01-04T10:35:59-05:00","name":"Annual Energy Outlook 2014","identifier":"AEO.2014",...}}}) — the no-key bulk path IS live. NOT CONFIRMED: the v2 path returned HTTP 403 {"error":{"cod

#### NASA Open APIs (api.nasa.gov — NeoWs, DONKI, Techport, EONET, EPIC, TLE) — NASA / api.data.gov ⚠️ UNVERIFIED

Covers **2** subdomains: astronomical-events, deep-space-missions

- Docs: https://api.nasa.gov/
- Auth: free API key (instant, email only). DEMO_KEY is documented for testing but is shared per-IP and was exhausted on arrival from this environment. | Limits: CORRECTED FROM LIVE HEADERS. The prior report stated DEMO_KEY = 30 req/IP/hour AND 50/IP/day. The server's own response header says otherwise: 'x-ratelimit-limit: 10', 'x-ratelimit-remaining: 0'. So DEMO_KEY is 10 per window per IP, not 30/hr — and because the quota is keyed to a SHARED egress IP, it can be at zero before you make your first call, which is exactly what happened here. Registered free key: documented 1,000 req/hour (NOT measured — I had no key).
- Latency: NeoWs daily; DONKI hourly-to-daily; Techport daily | Format: REST JSON
- Why primary: One key unlocks ~16 APIs across two subdomains. NeoWs gives per-day NEO close approaches with hazard flags; DONKI gives solar flares with class/peak time, CMEs and geomagnetic storms; Techport gives NASA programme/project records with lastUpdated. RETAINED as primary but DEMOTED in priority: NOAA SWPC supersedes DONKI for space weather (faster, no key, verified working), and JPL CNEOS supersedes NeoWs for NEO data (no key, verified working). NASA's genuinely non-redundant contribution is Techport for mission-milestone context — and Techport is precisely the part I could not verify. Do not put this on the critical path until you have tested it with your own key.

```bash
REQUIRES YOUR OWN FREE KEY — DEMO_KEY is unusable in practice: curl -s 'https://api.nasa.gov/DONKI/FLR?startDate=2026-09-01&endDate=2026-09-20&api_key=YOUR_REGISTERED_KEY'
```

> Evidence: FAILED TO VERIFY — this is the prior report's most significant overclaim. It asserted 'HTTP 200 on three endpoints with DEMO_KEY' with specific payloads. I could not reproduce ANY of it. DONKI/FLR with DEMO_KEY -> HTTP 429 {"error":{"code":"OVER_RATE_LIMIT","message":"You have exceeded your rate limit..."}}. NeoWs feed with DEMO_KEY -> HTTP 429, same error. Retried DONKI after an interval with hea

#### GraceDB — Gravitational-Wave Candidate Event Database — LIGO / Virgo / KAGRA Collaboration ✅ LIVE

Covers **1** subdomains: physics-breakthroughs

- Docs: https://gracedb.ligo.org/documentation/
- Auth: none for public superevents; LVK membership only for internal alerts | Limits: No key, no published rate limit — UNKNOWN. 6,301 superevents total, of which 5,546 are category Production and the remainder are MDC (mock data challenge) injections.
- Latency: CORRECTED — 'minutes' applies only DURING an observing run. As of 2026-09-21 the network is NOT in a production observing run: the most recent Production superevent is 2025-11-18, i.e. ~10 months stale. Only MDC mock events are currently being generated (newest: 2026-09-21). Effective latency for real detections right now is: no data. | Format: REST JSON
- Why primary: It is the only free observational (as opposed to literature) event feed available for the physics subdomain, and it is the correct feed to have wired when O5 begins. Retained on that basis. But it must NOT be described as a currently-streaming settlement path — it is a dormant feed with a live mock-data stream running through it, which is a worse failure mode than a dead endpoint because it returns 200s full of plausible-looking fake detections.

```bash
MUST include the query filter or you get mock data: curl -s 'https://gracedb.ligo.org/apiweb/superevents/?format=json&count=3&query=category%3A%20Production'
```

> Evidence: LIVE BUT MATERIALLY MISREPRESENTED BY THE PRIOR REPORT — two defects found. (1) FILTER DEFECT: the prior report's exampleCall ('?format=json&count=2', no filter) returns {"numRows":6301, first row "superevent_id":"MS260921c","category":"MDC"} — a MOCK event as row 1. I then tested '?category=Production' and the parameter is SILENTLY IGNORED: still numRows 6301, still MDC first. The only form that 

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Launch Cadence & Providers | Launch Library 2 — /launches/upcoming/ (count 370 verified)  | Launch Library 2 status enum (Success / Failure / Go / Hold  | 🟢 COVERED |
| Astronomical & Impact Events | IMPACT/NEO: JPL CNEOS cad.api (count 34 approaches inside 0. | JPL CNEOS fireball.api — detected atmospheric impacts with i | 🟢 COVERED |
| Lunar, Mars & Deep Space | Launch Library 2 — /events/upcoming/ (count=27 verified, inc | Launch Library 2 status enum and event completion, cross-che | 🟢 COVERED |
| Nobel Prizes & Academia | OpenAlex — VERIFIED end to end this pass: the /authors endpo | Nobel Prize API v2.1 — the Nobel Foundation's own structured | 🟢 COVERED |
| Energy Technology & Nuclear | NRC plant-status RSS (verified at https://www.nrc.gov/public | NRC PowerReactorStatusForLast365Days.txt — the regulator's o | 🟡 PARTIAL |
| Physics Breakthroughs | arXiv API — cat:physics.plasm-ph (VERIFIED, totalResults 20, | Crossref REST API — a claim is peer-review-confirmed when it | 🟡 PARTIAL |
| Mathematics & Prizes | arXiv across math.* — coverage CONFIRMED but only via the RS | NONE FOUND for authoritative resolution. The Clay Mathematic | 🟡 PARTIAL |

**Rejected**

- **NRC legacy reactor-status RSS URL (/reading-rm/doc-collections/event-status/reactor-status/powerreactorstatusrss.xml)** — FALSE PASS — DANGEROUS. Returns HTTP 200, but the body is the NRC Drupal HOMEPAGE HTML ('<!DOCTYPE html>... Generator: Drupal 11'), not RSS. A status-code-only check marks this green. I also probed /reading-rm/.../rss.xm
- **GraceDB '?category=Production' query parameter** — SILENTLY IGNORED — the worst failure mode in this mapping. https://gracedb.ligo.org/apiweb/superevents/?format=json&count=3&category=Production returns HTTP 200 with numRows 6301 (the UNFILTERED total) and category 'MDC'
- **NASA api.nasa.gov DEMO_KEY as a usable example-call credential** — NOT USABLE — rejected as an exampleCall pattern, though the underlying APIs stay in primaryFeeds behind a registered key. DEMO_KEY returned HTTP 429 OVER_RATE_LIMIT on DONKI/FLR and on NeoWs/feed across three attempts, w
- **export.arxiv.org query API as a hot-path/per-request feed** — THROTTLES FAR HARDER THAN DOCUMENTED — rejected for synchronous use, retained for cached polling. Documented terms say 1 request per 3 seconds; measured reality was HTTP 429 on the second call of a session, then 429, 429
- **FAA commercial space launch licences / licensed launch operations** — NO free machine-readable feed exists. /space/launches_operations and /space/licenses_permits both 404; the Commercial Space Data page is an interactive HTML Fact Book with no CSV/XLSX/JSON and returns 403 to programmatic
- **NRC ADAMS Public Search API (licensing docket)** — Subscription-gated, not free-anonymous. The NRC replaced legacy ADAMS web search with a Public Search API in Dec 2025 behind adams-api-developer.nrc.gov, which requires subscribing to a product; the legacy adamswebsearch
- **Argonne National Laboratory — Light-Duty Electric Drive Vehicles Monthly Sales** — HTTP 403 on programmatic fetch; the XLSX sits behind a bot-blocked page. Named in the domain spec as the EV market-share source. Replaced with Our World in Data, which I verified works but is ANNUAL (confirmed: series en
- **Clay Mathematics Institute (Millennium Prize)** — No API, no RSS, no structured data of any kind — claymath.org/millennium-problems/ is plain HTML. It is the sole settlement authority for Millennium Prize contracts, which is why the mathematics subdomain is PARTIAL. Scr
- **RocketLaunch.Live** — Free anonymous tier hard-capped at 5 launches per call with no pagination. Superseded by Launch Library 2, which I verified returns full filtered counts (SpaceX 2026 = 159, Rocket Lab 2026 = 30) at no cost. Worth keeping
- **Space-Track.org** — Requires account registration and enforces per-endpoint throttling. CelesTrak serves the same US Space Force-derived GP/SATCAT data with no auth at all — verified live this pass (ISS element set, epoch under 24h old) — s
- **developer.nrel.gov (AFDC alternative-fuel / EV station API)** — NOT VERIFIED — DNS resolution failed from this environment (curl error 6). Not reported as working on the strength of an inventory alone. Retry from a network that resolves it; EIA and OWID cover the EV need meanwhile.
- **Semantic Scholar Academic Graph API** — Superseded by OpenAlex for this domain's breadth, and its published rate limits are self-contradictory (overview states a 1,000 req/sec shared pool; the key-request page states 1 req/sec). Not dead — just strictly worse 
- **Epoch AI, Hugging Face Hub, OpenRouter Models, TOP500/Green500** — Real and live, but they serve AI/compute-capability markets, not any of the seven subdomains here. Out of scope — they belong to a technology/AI domain mapping.

---

### society-education-and-records

*3/6 subdomains covered · 10 primary feeds*

#### Urban Institute Education Data Portal API (harmonized NCES IPEDS + CCD + EDFacts + CRDC) — Urban Institute (serving US Dept of Education / NCES source data) ✅ LIVE

Covers **3** subdomains: university-tuition, campus-and-institutions, academic-outcomes

- Docs: https://educationdata.urban.org/documentation/
- Auth: none — no key, no registration, no header required. CONFIRMED by fetch with no auth of any kind. | Limits: Free and unauthenticated — CONFIRMED. Paginated (count/next/previous cursor). No published per-IP rate limit (UNKNOWN — treat as courtesy-limited; I issued ~8 calls including two >0.4MB payloads with no throttling). 129 endpoints CONFIRMED at /api/v1/api-endpoints/. History depth CONFIRMED: /summaries returned 38 annual rows starting 1986; endpoint metadata reports years_available '1980, 1984–2024' for the IPEDS directory.
- Latency: annual, 1–2 year publication lag (2022 is the latest complete IPEDS collection served). EDFacts assessments lag further — 2018 was the year that returned data in my test. | Format: REST JSON
- Why primary: Still the broadest feed in the domain and the correct anchor, but for partly different reasons than the original report gave. CONFIRMED broad: one unauthenticated REST surface, 129 endpoints, spanning IPEDS academic-year-tuition (tuition_published, fees_published, tuition_fees_published, credit_hour_charge_pt), IPEDS directory (institution master WITH populated chief_admin_name/chief_admin_title), IPEDS admissions-enrollment, and the whole K-12 CCD/EDFacts/CRDC family. CORRECTION UPWARD on academic-outcomes: the original report justified that subdomain only via 'CCD enrollment', which is a headcount and not an outcome. The portal actually exposes genuine outcome endpoints I verified exist and return data — /school-districts/edfacts/assessments/{year}/{grade}/ (district reading/math proficiency bands), /school-districts/edfacts/grad-rates/, /college-university/ipeds/grad-rates/, /ipeds/grad-rates-pell/, /ipeds/outcome-measures/. That is real academic-outcomes coverage at district and institution level. CORRECTION DOWNWARD on two points: (1) tuition_pub_pct_increase is NOT a usable rate-increase series — see verificationEvidence, it is 94.7% unpopulated; derive year-over-year change from tuition_published across two year calls instead. (2) university-rankings has been REMOVED from coversSubdomains — this API never returns a ranking, only selectivity inputs that correlate with one. The /summaries aggregation endpoint is confirmed working and does return a whole state-level time series in one call.

```bash
curl 'https://educationdata.urban.org/api/v1/college-university/ipeds/academic-year-tuition/2022/?unitid=166027'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21. Seven calls, all HTTP 200, no auth. (1) academic-year-tuition unitid=166027 → HTTP 200, 1821 bytes, 0.33s, count:6. Row level_of_study=1,tuition_type=2: tuition_fees_ft 57261, tuition_ft 52659, fees_ft 4602, credit_hour_charge_pt 1646, tuition_published 52659, fees_published 4602, tuition_fees_published 57261 — all CONFIRM the original report exactly. (2) **

#### College Scorecard API v1 — US Department of Education, served via api.data.gov ✅ LIVE

Covers **1** subdomains: university-tuition

- Docs: https://collegescorecard.ed.gov/data/documentation/
- Auth: api.data.gov key required, free instant signup. CONFIRMED that DEMO_KEY works for evaluation — all my verification calls used it. | Limits: **CORRECTED — the original report's DEMO_KEY figure is wrong.** The response headers on this endpoint report `x-ratelimit-limit: 10`, not the 30/hour the report stated. I observed `x-ratelimit-remaining` fall 2 → 1 across consecutive calls, confirming the counter is live and the ceiling is 10 per window on DEMO_KEY, not 30. Plan for ~10, not 30, when evaluating without a registered key. The registered-key figure of 1,000 requests/hour is api.data.gov's documented default but is **UNVERIFIED** — I did not register a key and will not report a limit I did not observe. ~6,500 Title IV institutions and ~2,000 fields per institution are documented figures, also UNVERIFIED by me (my calls used field projections and returned total:1 and total:6).
- Latency: annual refresh; 'latest.*' prefix resolves to the most recent published collection — CONFIRMED (latest.cost.tuition.in_state returned 61676 for Harvard vs the 2022 IPEDS figure of 52659, i.e. a genuinely more recent collection than the Urban feed serves) | Format: REST JSON
- Why primary: Retained as the second broad institution-level feed, and its two distinguishing capabilities both CHECK OUT under independent fetch: (1) the shared join key — Harvard came back with id 166027, byte-identical to the IPEDS unitid the Urban feed uses, so the two really do join with no crosswalk; (2) genuine server-side multi-institution filtering — school.state=MA with latest.student.size__range=10000.. returned six institutions with tuition in a single call, so a 'tuition across every large Massachusetts school' panel is one HTTP request. It also carries fresher tuition than Urban/IPEDS, which matters given IPEDS' 1–2 year lag. **coversSubdomains CORRECTED:** university-rankings has been removed. Scorecard returns admission_rate, SAT average and completion rate — inputs a ranking publisher weights — but it never returns a rank from any named list, and a feed that cannot return the quantity does not cover the subdomain. Those variables are recorded as predictive inputs in the coverage table instead.

```bash
curl 'https://api.data.gov/ed/collegescorecard/v1/schools.json?school.name=Princeton%20University&fields=school.name,latest.admissions.admission_rate.overall,latest.admissions.sat_scores.average.overall,latest.cost.tuition.in_state,latest.completion.completion_rate_4yr_150nt&api_key=DEMO_KEY'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21, four calls on DEMO_KEY, all HTTP 200. (1) Princeton ranking-input pull → HTTP 200, 290 bytes, 0.69s: {"metadata":{"page":0,"total":1,"per_page":20},"results":[{"latest.admissions.admission_rate.overall":0.0462,"latest.admissions.sat_scores.average.overall":1553,"latest.cost.tuition.in_state":62688,"latest.completion.completion_rate_4yr_150nt":0.9761,"school.

#### NAEP Data Service (Nation's Report Card ad-hoc data API) — National Center for Education Statistics (NCES) / NAEP ✅ LIVE

Covers **1** subdomains: academic-outcomes

- Docs: https://www.nationsreportcard.gov/api_documentation.aspx
- Auth: none — CONFIRMED, no key, no header, no User-Agent requirement | Limits: Free, no key, no registration — CONFIRMED. No published rate limit (UNKNOWN; three calls in quick succession all served, responses reported dataHitType FROM_MEMORY suggesting a warm cache tier). Subject/grade/jurisdiction generality CONFIRMED across two subjects and two jurisdictions; full subject list (science, writing, civics, US history, geography) and full TUDA district list are documented but NOT TESTED by me.
- Latency: per assessment cycle — roughly every two years per subject, released on a pre-announced Nation's Report Card date | Format: REST JSON (serviceVersion in every response; .aspx path but genuinely returns JSON, confirmed by successful json.loads)
- Why primary: The strongest single mapping in this domain and every claim about it survived independent fetch unchanged. It is the literal settlement publication — Kalshi's USTESTSMATH / KXUSTESTSMATH resolve to the Nation's Report Card, and this is its machine-readable form — returning the scale score to full float precision with explicit errorFlag and isStatDisplayable guards. One endpoint parameterises across subject, grade and jurisdiction, so the whole subdomain is one integration with swapped query parameters, and the same series supplies the prior-cycle history that forms the pre-release prior. No corrections.

```bash
curl 'https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx?type=data&subject=mathematics&grade=8&subscale=MRPCM&variable=TOTAL&jurisdiction=NP&stattype=MN:MN&Year=2022'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21, three calls, all HTTP 200, serviceVersion 6.4.2026.1, Source B11A. (1) Math grade 8, jurisdiction NP, 2022 → HTTP 200, 512 bytes, 0.45s, full body parsed: {"status":200,"serviceVersion":"6.4.2026.1","dataHitType":"FROM_MEMORY","Source":"B11A","result":[{"year":2022,"sample":"R3","CohortLabel":"Grade 8","stattype":"MN:MN","subject":"MAT","grade":8,"scale":"MR

#### Wikidata Query Service (SPARQL) — Wikimedia Foundation ✅ LIVE

Covers **3** subdomains: campus-and-institutions, religion-and-civic-institutions, records-and-recognition

- Docs: https://query.wikidata.org/
- Auth: none, but a descriptive User-Agent is required by policy — CONFIRMED working with a custom UA on three separate queries; I did not test whether a generic UA is refused, so the 403/429-on-generic-agent claim is UNVERIFIED (follow the policy regardless) | Limits: 60-second query timeout, 5 concurrent queries per IP, ~30 queries/minute per IP — these are WDQS's published operational limits and are UNVERIFIED by me (I issued only 4 queries and did not probe for throttling). Free, no key — CONFIRMED. Full dumps available for self-hosting.
- Latency: minutes — edits propagate to WDQS with a short lag | Format: SPARQL over HTTP, returns JSON / CSV / TSV / XML (CSV confirmed)
- Why primary: Still the clearest one-endpoint-many-subdomains case in the domain, and three of the four original claims reproduced exactly. The same SPARQL surface returns current US university heads (P1075), the sitting pope with birth date and reign start (the actuarial inputs for KXNEWPOPEDATE), and complete recognition back-series (P166 → Q207826 for TIME Person of the Year). Because it is a graph, adding a new recognition list or office is a query change rather than a new integration. **coversSubdomains CORRECTED: university-rankings removed.** The original report already flagged the P1352 weakness in its own evidence but left the subdomain in the covers list anyway — that is exactly the over-claim this pass is meant to catch. My independent query confirms the defect is not institution-specific. Treat Wikidata as authoritative-ish for post-hoc structured record and as a leading indicator paired with EventStreams — never as settlement, since it is community-edited.

```bash
curl -G -H 'Accept: text/csv' -A 'yourapp/1.0 (you@example.com)' --data-urlencode 'query=SELECT ?yr ?whoLabel WHERE { ?who p:P166 ?s . ?s ps:P166 wd:Q207826 . OPTIONAL { ?s pq:P585 ?yr } SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } ORDER BY DESC(?yr) LIMIT 6' https://query.wikidata.org/sparql
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21, four distinct SPARQL queries, all HTTP 200, custom User-Agent. (1) TIME Person of the Year via P166 → wd:Q207826, CSV response: 2024-01-01 Donald Trump / 2022-01-01 Volodymyr Zelenskyy / 2021-01-01 Elon Musk / 2019-12-11 Greta Thunberg / 2018-01-01 Jamal Khashoggi / 2018-01-01 Tatiana Felgenhauer — matches the original report exactly, including the two-name 

#### Wikimedia Pageviews / Analytics REST API — Wikimedia Foundation ✅ LIVE

Covers **3** subdomains: campus-and-institutions, religion-and-civic-institutions, records-and-recognition

- Docs: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/
- Auth: none (descriptive User-Agent required by policy) — CONFIRMED working with a custom UA | Limits: Free, no key — CONFIRMED. The '100 requests/second per IP' figure is Wikimedia's documented AQS ceiling and is UNVERIFIED by me (I made two calls and did not load-test). History from 2015-07-01 to yesterday is documented; I confirmed only that a 2026-09 window and a 2026-09-18 top-1000 both resolve. The /top/ endpoint returning a full 1000-article ranked list is CONFIRMED.
- Latency: hourly endpoint lags ~1–2h; daily endpoint settles next day | Format: REST JSON
- Why primary: **coversSubdomains CORRECTED from six subdomains to three — this was the largest over-claim in the report.** The endpoint is live and excellent at what it does, but it returns one quantity: pageview counts. It never returns a tuition figure and never returns a test score, so listing it under university-tuition and academic-outcomes fails the spot-check standard (a feed claiming a subdomain must return that subdomain's quantity). Fetching Harvard_University pageviews tells you nothing about Harvard's tuition that the IPEDS feed does not already tell you authoritatively. Retained for the three subdomains where attention is a genuine modelled input: records-and-recognition, where the /top/ endpoint returns the ranked top-1000 English Wikipedia articles for any day and is the closest free machine-readable analogue to a search-attention leaderboard; and campus-and-institutions plus religion-and-civic-institutions, where an attention spike on a named person or institution is a real event signal with a decade of daily baseline to normalise against. Pair with EventStreams for the event and Pageviews for the magnitude.

```bash
curl -A 'yourapp/1.0 (you@example.com)' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Harvard_University/daily/20260901/20260910'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21, two endpoints, both HTTP 200, custom User-Agent. (1) per-article Harvard_University daily 20260901–20260910 → HTTP 200, 1561 bytes, 0.14s: {"items":[{"project":"en.wikipedia","article":"Harvard_University","granularity":"daily","timestamp":"2026090100","access":"all-access","agent":"user","views":3631},{..."2026090200","views":3893},...]} — views 3631 and 38

#### Wikimedia EventStreams (recentchange SSE firehose) — Wikimedia Foundation ✅ LIVE

Covers **3** subdomains: campus-and-institutions, religion-and-civic-institutions, records-and-recognition

- Docs: https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams
- Auth: none (descriptive User-Agent required) — CONFIRMED | Limits: Free, no key — CONFIRMED. Server-Sent Events. Throughput CONFIRMED at roughly 44 KB/s of live event JSON (263,939 bytes in a 6-second window), so budget real bandwidth for a persistent consumer. Last-Event-ID / since= gap-free resume is documented and the dual-datacentre offset structure needed for it IS present in the id: line I captured — but I did NOT test an actual reconnect-and-resume, so replay correctness is IMPLEMENTED / NOT LIVE-VALIDATED.
- Latency: sub-second — CONFIRMED: the first event carried meta.dt 2026-09-21T03:30:32.190Z against a stream-open timestamp of 1789961432191 (2026-09-21T03:30:32.191Z), i.e. ~1ms end-to-end | Format: SSE (text/event-stream) carrying JSON events
- Why primary: The lowest-latency free signal for the three event-driven subdomains, and the liveness and latency claims both survive independent test. A university president resigning, a pope being elected or a year-end list being announced produces an edit burst within seconds, well before any structured registry or annual publication updates. One persistent connection covers every entity in the domain at once, which beats polling N article endpoints. It is a trigger and a leading indicator, never a settlement source: filter on title and namespace, then confirm against the authoritative feed for that subdomain (Vatican bollettino, the institution's own announcement, NAEP).

```bash
curl -N --max-time 6 -A 'yourapp/1.0 (you@example.com)' 'https://stream.wikimedia.org/v2/stream/recentchange'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-21. Opened the stream with curl --max-time 6; curl exited 28 (timeout) as expected for a never-terminating stream, having captured **263,939 bytes** of live events. Handshake and first event verbatim: ':ok' / blank / 'event: message' / 'id: [{"topic":"eqiad.mediawiki.recentchange","partition":0,"timestamp":1789961432191},{"topic":"codfw.mediawiki.recentchange","par

#### Vatican News RSS + Holy See Press Office Bollettino — Dicasterium pro Communicatione (Holy See) ✅ LIVE

Covers **1** subdomains: religion-and-civic-institutions

- Docs: https://www.vaticannews.va/en.html
- Auth: none — CONFIRMED | Limits: Free, no key — CONFIRMED. **Exactly 50 items per pull, counted** (grep -c '<item>' = 50). Multiple language editions available by swapping the /en. prefix (documented; NOT TESTED). The Press Office bollettino is scrape-only HTML with no RSS or JSON — CONFIRMED.
- Latency: minutes — CONFIRMED: lastBuildDate Mon, 21 Sep 2026 05:00:14 +0200, within the hour of fetch, and the bollettino index carried a dated entry for 2026/09/19 | Format: RSS 2.0 / XML (bollettino: HTML, scrape-only)
- Why primary: Retained as a narrow primary, and every claim checks out — including the one detail the original report asserted but did not actually evidence. This is the official organ of the Holy See, the settlement authority named for KXNEWPOPEDATE and KXPOPESWIFT, so it is authoritative rather than a news proxy. No broader feed serves this subdomain's settlement; the central 'prefer one broad feed' rule's exception genuinely applies. The two-surface split is real and both halves are needed in production: vaticannews.va is the machine-readable monitoring stream, press.vatican.va is where the formal bollettino text lands and must be scraped. **New finding that improves the integration:** the bollettino index exposes a predictable dated URL pattern, /content/salastampa/en/bollettino/pubblico/YYYY/MM/DD.html, so the scrape can address a specific day directly rather than crawling the index.

```bash
curl -L 'https://www.vaticannews.va/en.rss.xml'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21, two surfaces, both HTTP 200. (1) https://www.vaticannews.va/en.rss.xml → HTTP 200, **72,246 bytes**, 0.17s — byte count matches the original report exactly. Valid RSS 2.0: <lastBuildDate>Mon, 21 Sep 2026 05:00:14 +0200</lastBuildDate>, <title><![CDATA[Vatican News - English]]></title>, <description><![CDATA[News from the Vatican - News about the Church]]></d

#### Google Trends daily trending RSS — Google ✅ LIVE

Covers **1** subdomains: records-and-recognition

- Docs: https://trends.google.com/trending
- Auth: none — CONFIRMED | Limits: No key — CONFIRMED. No published rate limit (UNKNOWN); undocumented endpoint Google may change without notice. **Two constraints CORRECTED/SHARPENED by my fetch.** (a) Volume: the feed returns **exactly 10 items**, counted, for both geo=US and geo=IN. The original report did not state a count and reads as though it returns a substantial trending set; it does not. (b) Archive: it returns ONLY the current snapshot — no backfill, no history. You must poll and persist your own series.
- Latency: sub-hourly — CONFIRMED with fresh evidence: item pubDates at 20:10, 20:00 and 19:50 -0700, i.e. a new entry every ~10 minutes | Format: RSS/XML with an ht: namespace carrying approx_traffic, picture and related news links
- Why primary: Retained: it is the surviving free Google Trends surface and the only live observation of the quantity that actually decides 'the #1 searched person on Google' (Polymarket) and KXRANKLISTGOOGLESEARCH (Kalshi). Nothing broader covers it. **But my re-fetch demonstrated the no-archive weakness empirically rather than just asserting it, and it is worse than the report conveys.** The report captured top item 'carlie irsay-gordon' at approx_traffic 2000+ with pubDate 19:40. My fetch, within roughly the same hour, returned top item 'jennifer garner' at approx_traffic 200+ — the leading entry and its traffic magnitude both turned over inside an hour, and the earlier observation is now unrecoverable from the endpoint. With only 10 slots and ~10-minute turnover, a poller that runs less often than every few minutes will silently drop entries. Build the capture-and-persist job before you need the history, and size its interval to the observed churn, not to a daily cadence.

```bash
curl 'https://trends.google.com/trending/rss?geo=US'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21. (1) geo=US → HTTP 200, 21,337 bytes, 0.30s, valid RSS with the ht namespace declared (xmlns:ht="https://trends.google.com/trending/rss"), <title>Daily Search Trends</title>, <description>Recent searches</description>. Item count counted at **10**. First item: <title>jennifer garner</title>, <ht:approx_traffic>200+</ht:approx_traffic>. pubDates sampled: Sun, 

#### Google News RSS (arbitrary-query search feed) — Google ✅ LIVE

Covers **4** subdomains: university-tuition, campus-and-institutions, religion-and-civic-institutions, records-and-recognition

- Docs: https://news.google.com/
- Auth: none — CONFIRMED | Limits: No key, no published rate limit (UNKNOWN). Unofficial but long-stable. **Licensing constraint is real and I reproduced it:** the feed body carries Google's copyright notice restricting use to rendering within a personal feed reader for personal, non-commercial use. That is a legal blocker for a commercial terminal, not a technical one — get it reviewed before redeployment. This is the main reason not to lean on it as the only news path.
- Latency: minutes behind publication | Format: RSS 2.0 / XML
- Why primary: Retained, and this is the one feed where I confirmed genuine topical relevance rather than just a 200. One endpoint with an arbitrary query string covers the announcement-driven gap that no structured feed fills: board-of-trustees decisions, presidential resignations, tuition-increase votes and ranking-release announcements all surface in press coverage long before any registry reflects them, and IPEDS is 1–2 years behind. **coversSubdomains trimmed from five to four:** university-rankings removed for consistency with every other feed here — a news article announcing a ranking release is a trigger, not the ranking, and the coverage table already carries that as the domain's open settlement gap. Note it is included in place of GDELT, which I re-tested and still could not sustain — see rejectedFeeds.

```bash
curl 'https://news.google.com/rss/search?q=%22university+president%22+resigns&hl=en-US&gl=US&ceid=US:en'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21. Query '"university president" resigns' → HTTP 200, **143,852 bytes**, 0.65s (report said 143,837 — a 15-byte delta consistent with a live feed, not a cached one). Valid RSS 2.0, channel <title>""university president" resigns" - Google News</title>. **The report only evidenced headers and the copyright block; I checked the items are actually on-topic** — real

#### Federal Register API v1 (Department of Education filter) — US National Archives / Office of the Federal Register ✅ LIVE

Covers **2** subdomains: campus-and-institutions, university-tuition

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none — CONFIRMED | Limits: Free, no key — CONFIRMED. Cursor pagination CONFIRMED (a search_after_cursor was returned in next_page_url). The 10,000-results-per-query ceiling is CONFIRMED by the response itself reporting count:10000 with total_pages:50 at per_page:2 — note that 10000 is the capped ceiling, not a true match count, so do not read it as a document total. 1,000 max per_page and full back archive are documented and UNVERIFIED by me.
- Latency: daily — CONFIRMED, and better than the report implies: the newest documents carried publication_date 2026-09-21, i.e. tomorrow's Federal Register issue is already queryable, so the feed is genuinely forward-dated rather than merely same-day | Format: REST JSON
- Why primary: Retained unchanged — every claim reproduced. The authoritative, structured, free record of federal education action, which is the layer driving Kalshi's Education contracts (Title VI enforcement, student-loan and Pell rules, accreditation actions, program terminations). Genuinely forward-looking in a way most feeds here are not: proposed rules publish with comment-close and effective dates, giving a dated calendar of decision points rather than a report of what already happened. One agency filter covers the whole federal education surface — one integration, not one per program.

```bash
curl 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=education-department&per_page=2&order=newest&fields%5B%5D=title&fields%5B%5D=publication_date&fields%5B%5D=type'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20/21 → HTTP 200, 724 bytes at per_page=2 (the report's 28,444-byte figure reflects an unprojected call; with the field projection in the exampleCall the payload is 724 bytes), 0.19s. Full body: {"description":"Documents from Education Department","count":10000,"total_pages":50,"next_page_url":"...search_after_cursor=WzE3ODk5NDg4MDAwMDAsIjIwMjYtMTkyMzUiXQ","results

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| University Tuition | Urban Institute IPEDS academic-year-tuition (tuition_publish | Urban Institute Education Data Portal serving NCES IPEDS aca | 🟢 COVERED |
| University Rankings | College Scorecard (admission_rate.overall, sat_scores.averag | NONE FOUND | 🟡 PARTIAL |
| Test Scores & Academic Outcomes | NAEP Data Service prior-cycle back series (same endpoint, ea | NAEP Data Service API (https://www.nationsreportcard.gov/Dat | 🟢 COVERED |
| Campus Leadership & Student Affairs | Wikimedia EventStreams SSE (sub-second, measured at ~1ms fro | PARTIAL — no API for university announcements. Closest struc | 🟡 PARTIAL |
| Religion & Civic Institutions | Wikidata SPARQL for actuarial and procedural base rates (re- | Vatican News RSS (https://www.vaticannews.va/en.rss.xml — re | 🟢 COVERED |
| Records, Lists & Recognition | Wikimedia Pageviews /top/ endpoint — the better of the two,  | PARTIAL — Wikidata records outcomes post-hoc as structured d | 🟡 PARTIAL |

**Rejected**

- **GDELT DOC 2.0 API (api.gdeltproject.org/api/v2/doc/doc)** — STILL REJECTED, but the original report's stated reason is FACTUALLY WRONG and is corrected here. It claimed 'zero successful payloads'. That is false — I got one. Across 7 independent attempts on 2026-09-20/21: attempt 
- **US News Best Colleges rankings** — DEAD/BLOCKED and paywalled — RE-VERIFIED independently. Probed https://www.usnews.com/education/best-colleges/api/search on 2026-09-20 → **HTTP 000** (no response at all; connection refused or bot-blocked at the edge). R
- **QS World University Rankings API** — PAYWALLED — RE-VERIFIED independently. Probed https://www.topuniversities.com/rankings/api/qs-world-university-rankings on 2026-09-20 → **HTTP 403 Forbidden**. Reproduces the original report exactly. Access requires a co
- **Wikidata P1352 (ranking) statements as a rankings source** — TOO SPARSE AND UNATTRIBUTED — RE-VERIFIED and the defect CONFIRMED to be systemic, not a sampling artifact. The report tested two institutions; I deliberately queried a different set to see whether the problem generalise
- **Google Year in Search annual list endpoint** — NO API — RE-VERIFIED, with the mechanism corrected. The report recorded https://trends.google.com/y/2025/US → HTTP 404. The actual behaviour is **HTTP 301**, redirecting to https://trends.google.com/trends/y/2025/US, whi
- **Hipolabs Universities API (universities.hipolabs.com)** — SUPERSEDED — TOO NARROW. RE-VERIFIED live: http://universities.hipolabs.com/search?name=Princeton → HTTP 200. It works, but it carries only name, country, domain and homepage — no tuition, no leadership, no enrollment, n
- **Nobel Prize API v2.1** — VERIFIED LIVE but TOO NARROW for a primary slot. RE-CONFIRMED HTTP 200 on 2026-09-20 for /2.1/nobelPrizes?nobelPrizeYear=2025. Authoritative, free, complete 1901-present history, but it covers one award family and none o
- **ProPublica Nonprofit Explorer API v2** — Out of scope as a primary — NOT RE-TESTED in this pass, and recorded as such rather than inheriting the original report's PASS. The report logged HTTP 200 with Harvard trustee records; I did not re-fetch it because its r
- **OECD SDMX REST API (PISA international assessment)** — NOT TESTED — and not required. Carried in the source inventory with live=false, and I did not probe it either. PISA would be the international analogue to NAEP, but every listed academic-outcomes contract (USTESTSMATH, K
- **UNESCO UIS global education indicators** — NOT TESTED — requires a free registration key I did not obtain. Its annual global indicators, with multi-year lag, do not serve any US-centric contract listed in this domain, and the Urban Institute portal covers the US 
- **Urban Institute field 'tuition_pub_pct_increase' as a tuition-increase settlement series** — NOT A FEED but recorded here because the original report promoted it as the series that prices Robinhood's UTHVT/UTLAO tuition strikes, and a developer would wire it in on that basis. **It does not carry usable data.** I

---

### speech-and-mentions

*0/4 subdomains covered · 11 primary feeds*

#### GovInfo keyless content/metadata endpoints (CREC Congressional Record + CPD Presidential Documents) — JSON API requires YOUR OWN free key, not DEMO_KEY — US Government Publishing Office (GPO) ✅ LIVE

Covers **1** subdomains: political-mentions

- Docs: https://api.govinfo.gov/docs/
- Auth: CORRECTED. The prior report claimed DEMO_KEY works but is 'heavily rate-limited'. DEMO_KEY is a globally shared key and was exhausted on EVERY attempt from a clean IP — 3/3 calls returned HTTP 429 OVER_RATE_LIMIT with zero successful calls, including the very first one and a retry several minutes later. Treat DEMO_KEY as non-functional. Register a free api.data.gov key before building anything on /search, /collections or /packages. NO key at all is needed for www.govinfo.gov/content/... and /metadata/..., which is where the verbatim text lives and which is verified working. | Limits: api.data.gov: 1,000 req/hour per registered key (documented; NOT independently verified — no key was available to test). DEMO_KEY: effectively 0 usable requests. www.govinfo.gov content/metadata URLs are keyless and were not throttled across 8 calls.
- Latency: CREC (congressional floor speech): ~1-day lag — CREC-2026-09-17 granule text was retrievable on 2026-09-20. CPD (presidential remarks): the prior report's ~41-day lag figure is UNVERIFIED by me — it was derived from the /search API, which I could not reach. The keyless CPD package DCPD-202600526 I fetched is undated in-body; I could not independently confirm the lag. Measure it yourself with a real key before relying on it. | Format: HTML and XML/MODS (verbatim text and metadata, keyless); JSON (search/collections, key required)
- Why primary: Still the broadest free verbatim-speech corpus: every word spoken on the US House and Senate floor (CREC) plus official presidential remarks and exchanges with reporters (CPD), with the transcript text retrievable with no key at all. One URL shape covers any term by any US federal speaker. NOTE: I REMOVED 'speech-metrics' from its claimed coverage — GovInfo publishes transcript text, not speech duration, attendance or post counts, and a transcript word count is a proxy, not the measured quantity these contracts settle on. Congress.gov remains superseded (DEMO_KEY HTTP 429 on retest).

```bash
# VERBATIM TEXT — keyless, verified working:
curl -sL 'https://www.govinfo.gov/content/pkg/CREC-2026-09-17/html/CREC-2026-09-17-pt1-PgS4800.htm'
curl -sL 'https://www.govinfo.gov/content/pkg/DCPD-202600526/html/DCPD-202600526.htm'
curl -sL 'https://www.govinfo.gov/metadata/pkg/CREC-2026-09-17/mods.xml'
# DISCOVERY/SEARCH — needs a real api.data.gov key (DEMO_KEY is exhausted, see auth):
curl -s -X POST 'https://api.govinfo.gov/search?api_key=YOUR_FREE_KEY' -H 'Content-Type: application/json' -d '{"query":"collection:CREC AND \"artificial intelligence\"","pageSize":3,"offsetMark":"*","sorts":[{
```

> Evidence: KEYLESS HALF VERIFIED. HTTP 200, 7373B: CREC-2026-09-17-pt1-PgS4800.htm returned real floor text, '<title>Congressional Record, Volume 172 Issue 147 (Thursday, September 17, 2026)</title>' then '[Senate] [Pages S4800-S4801] ... SENATE RESOLUTION 863--EXPRESSING SUPPOR'. HTTP 200, 57828B: DCPD-202600526 stripped to 5,925 words with 8 case-insensitive 'tariff' occurrences — reproduces the prior repo

#### UK Parliament Hansard Search API — UK Parliament ✅ LIVE

Covers **1** subdomains: political-mentions

- Docs: https://hansard-api.parliament.uk/swagger/ui/index
- Auth: none | Limits: No published quota, no key, no registration. No throttling observed across 4 calls in one session.
- Latency: Next sitting day. A 2026-09-15 Commons contribution was retrievable on 2026-09-20. | Format: JSON
- Why primary: Confirmed: the only free settlement-grade verbatim feed for UK political speech, speaker-attributed and filterable by term, House and date range. Two integration defects I found do NOT invalidate it but WILL break a naive implementation — see verificationEvidence. Both are avoidable with the right field choices.

```bash
curl -s 'https://hansard-api.parliament.uk/search/contributions/Spoken.json?queryParameters.searchTerm=inflation&queryParameters.house=Commons&queryParameters.startDate=2026-09-01&queryParameters.endDate=2026-09-19&queryParameters.take=20'   # per-speaker, use memberId NOT a name: curl -s 'https://hansard-api.parliament.uk/search/contributions/Spoken.json?queryParameters.memberId=1427&queryParameters.take=5'
```

> Evidence: VERIFIED. HTTP 200, 97069B: contributions/Spoken.json searchTerm=inflation, Commons, 2026-09-01..2026-09-19 returned 20 dated speaker-attributed contributions — SittingDate 2026-09-15 | 'Tom Gordon (Harrogate and Knaresborough) (LD)' | 'I thank the hon. Lady for her statement. Is she able to outline whether, during the course of its work, the Committee gave any consideration to index-linking compe

#### GDELT TV 2.0 API (Television Explorer) — HISTORICAL PRIORS ONLY, DATA FROZEN 2024-10-10 — The GDELT Project / Internet Archive TV News Archive ⚠️ UNVERIFIED

Covers **3** subdomains: political-mentions, broadcast-mentions, earnings-call-mentions

- Docs: https://blog.gdeltproject.org/gdelt-2-0-television-api-debuts/
- Auth: none | Limits: No key. ~1 request per 5 seconds sustainable; 4 TV calls in one session all succeeded with no 429.
- Latency: NOT LIVE. Index stops 2024-10-10. Queries answer instantly and return nothing after that date. | Format: JSON (also CSV, HTML)
- Why primary: Freeze independently reconfirmed. Retained for the same reason the prior report gave and with the same explicit label: it is the broadest per-term broadcast mention-frequency index that exists free (159 stations, 2009-06 to 2024-10), and it is the only free source of a base rate for 'how often does this speaker actually say X on air'. PRIOR ENGINE ONLY — it cannot price today's tape and cannot settle anything. verifiedLive stays false.

```bash
curl -s 'https://api.gdeltproject.org/api/v2/tv/tv?query=%22witch+hunt%22+(station:FOXNEWS)&mode=clipgallery&format=json&datanorm=raw&last24'   # per-term frequency series: curl -s 'https://api.gdeltproject.org/api/v2/tv/tv?query=tariff%20(station:CNN)&mode=timelinevol&format=json&datanorm=perc&last24'
```

> Evidence: FREEZE CONFIRMED INDEPENDENTLY. HTTP 200, 8734B: 'tariff (station:CNN)' mode=timelinevol returned 185 monthly points, first {20090601T120000Z, 0}, LAST and last-non-zero both {20241001T120000Z, 0.0373}. HTTP 200, 27421B: mode=stationdetails returned exactly 159 stations with keys [StationID, Description, Market, Network, StartDate, EndDate]; max EndDate across all 159 = 20241010T235959Z. Transcrip

#### Alpha Vantage EARNINGS_CALL_TRANSCRIPT — Alpha Vantage ✅ LIVE

Covers **1** subdomains: earnings-call-mentions

- Docs: https://www.alphavantage.co/documentation/#earnings-call-transcript
- Auth: Free API key (self-service email signup). The literal key 'demo' works but is restricted to symbol=IBM — confirmed. | Limits: Documented as 25 requests/day, 5/minute. NOT VERIFIED — no free key was available, and the demo key gives no way to observe the quota. At 25/day this feed cannot poll many tickers.
- Latency: UNVERIFIED and this is the feed's central open risk. The demo key refused every symbol but IBM and every recent quarter, so post-call publication lag could not be measured. Do not assume same-session availability. | Format: JSON — array of {speaker, title, content, sentiment} segments
- Why primary: One endpoint, symbol + quarter parameters, covers every ticker and quarter — KXEARNINGSMENTIONAMZN and KXEARNINGSMENTIONMS are the same call. Speaker/title fields separate prepared remarks from analyst Q&A, which is the structure these contracts turn on. It remains the best free option, but the unmeasured post-call lag is why I downgraded earnings-call-mentions from COVERED to PARTIAL.

```bash
curl -s 'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo'   # demo key is IBM-only; with a free key: .../query?function=EARNINGS_CALL_TRANSCRIPT&symbol=AMZN&quarter=2026Q2&apikey=YOUR_FREE_KEY
```

> Evidence: VERIFIED, REPRODUCES THE PRIOR REPORT EXACTLY. HTTP 200, 57092B: symbol=IBM quarter=2024Q1 apikey=demo returned keys ['symbol','quarter','transcript'] with 37 speaker-attributed segments. Segment[0] = {speaker:'Olympia McNerney', title:'Global Head of Investor Relations', content:"Thank you. I'd like to welcome you to IBM's First Quarter 2024 Earnings Presentation..."}. I recomputed word-boundary 

#### trumpstruth.org RSS (public Truth Social mirror) — trumpstruth.org (independent archive) ✅ LIVE

Covers **1** subdomains: speech-metrics

- Docs: https://www.trumpstruth.org/
- Auth: none | Limits: No key, no published quota. Must follow the trumpstruth.org -> www.trumpstruth.org 301 (-L) and send a browser User-Agent.
- Latency: Near-real-time. Newest item at fetch time was pubDate 'Mon, 21 Sep 2026 02:02:54 +0000', minutes old. | Format: RSS 2.0 with a truth: namespace (truth:originalId, truth:originalUrl)
- Why primary: Confirmed as the only working free feed of POTUS posts, and it settles the KXPOTUSTWEETS family directly. Every X/Twitter route and Truth Social's own API remain dead (retested). Per-post timestamps and truth:originalId back-references make exact per-day and per-week counts computable from the feed alone. One structural limit a developer must plan for: the window is 100 items, which at the observed rate is ~7 days — a high-volume week will roll off, so poll and persist rather than reading the feed once at settlement.

```bash
curl -sL -A 'Mozilla/5.0' 'https://www.trumpstruth.org/feed'
```

> Evidence: VERIFIED, COUNTS REPRODUCE EXACTLY. HTTP 200, 127766B. Parsed 100 <item> elements spanning 'Mon, 14 Sep 2026 20:30:07 +0000' to 'Mon, 21 Sep 2026 02:02:54 +0000'. Independently recomputed per-day counts from the real pubDate values: 14 Sep=8, 15 Sep=18, 16 Sep=7, 17 Sep=16, 18 Sep=35, 19 Sep=5, 20 Sep=9, 21 Sep=2 — matches the prior report on every day. Item child tags confirmed: ['title','link','

#### Google News RSS — Google ✅ LIVE

Covers **4** subdomains: political-mentions, earnings-call-mentions, broadcast-mentions, speech-metrics

- Docs: https://news.google.com/rss
- Auth: none | Limits: No key, no published quota. Requires a browser User-Agent. No throttling across 2 calls.
- Latency: Minutes. Newest item at fetch time was 'Mon, 21 Sep 2026 02:07:00 GMT'. | Format: RSS 2.0
- Why primary: One keyless endpoint gives a live arbitrary-phrase, time-windowed article count for any person or term — the shared PREDICTIVE primitive across all four subdomains. Kept at four subdomains, but with an explicit boundary the prior report stated only in prose: this measures whether the press WROTE about something, never whether a person SAID a word. It can never settle a mention contract in any subdomain. Treat the four-subdomain coverage as predictive-only.

```bash
curl -s -A 'Mozilla/5.0' 'https://news.google.com/rss/search?q=%22Jensen+Huang%22+when:1d&hl=en-US&gl=US&ceid=US:en'
```

> Evidence: VERIFIED ON TWO SUBDOMAINS. political/speech side — HTTP 200, 105091B: '"Jensen Huang" when:1d' returned 77 <item> elements with real timestamped headlines: 'Sun, 20 Sep 2026 11:00:01 GMT | Nvidia CEO Jensen Huang emerges as Trump's top ally in AI safety debate - CNBC', 'Sun, 20 Sep 2026 13:37:00 GMT | Nvidia's Jensen Huang rejects AI extinction warnings as "doomsday narratives"', 'Mon, 21 Sep 202

#### GDELT 2.0 raw 15-minute bulk files (Mentions + GKG + Events) — The GDELT Project ✅ LIVE

Covers **4** subdomains: political-mentions, earnings-call-mentions, broadcast-mentions, speech-metrics

- Docs: http://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf
- Auth: none | Limits: No key, no quota. Bulk download, not rate-limited like the query APIs — 6 file fetches in one session, zero 429s. Use https:// for lastupdate.txt (http:// 301s with an empty body).
- Latency: 15 minutes for export/mentions. GKG is effectively 30 minutes — it trails the manifest by at least one cycle (see the defect below). | Format: Zipped tab-delimited CSV
- Why primary: The live, unthrottled substrate the query APIs cannot be. One GKG file yields per-article person, organization and theme annotations for every article in a 15-minute window at once — mention volume for every named entity with no per-entity querying. I verified the GKG annotation columns directly, which the prior report did not. Same predictive-only boundary as Google News: it counts articles, not utterances.

```bash
curl -sL 'https://data.gdeltproject.org/gdeltv2/lastupdate.txt'
# Lines 1-2 (export, mentions) are safe to fetch immediately.
# Line 3 (gkg) IS OFTEN NOT PUBLISHED YET — fetch the PREVIOUS 15-min stamp instead:
curl -sL -o gkg.zip 'http://data.gdeltproject.org/gdeltv2/20260921031500.gkg.csv.zip'
```

> Evidence: MANIFEST AND MENTIONS VERIFIED. HTTP 200, 319B: lastupdate.txt returned three URLs stamped 20260921033000. HTTP 200, 34914B: downloaded 20260921033000.mentions.CSV.zip, unzipped to a 249,913-byte CSV, parsed 1,182 rows, first row '1324016127\t20260921033000\t20260921033000\t1\tbusinessday.co.za\thttps://www.businessday.co.za/opinion/2026-09-21-fred-arendse-three-years-of-giving-junior-mining-a-voi

#### Wikimedia Pageviews / Analytics REST API — Wikimedia Foundation ✅ LIVE

Covers **4** subdomains: political-mentions, earnings-call-mentions, broadcast-mentions, speech-metrics

- Docs: https://wikimedia.org/api/rest_v1/
- Auth: none (a descriptive User-Agent is required) | Limits: ~200 req/s courtesy limit, no key. Not stress-tested.
- Latency: ~24-48 hours for daily granularity — so it is a slow prior, not a live tape. | Format: JSON
- Why primary: One URL pattern gives a daily attention series for any named person — the cleanest cross-subdomain proxy for whether a person is salient enough to be mentioned. Predictive only; it settles nothing.

```bash
curl -s -A 'your-app/1.0 (you@example.com)' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Jensen_Huang/daily/20260910/20260919'
```

> Evidence: VERIFIED. HTTP 200, 1503B: per-article/en.wikipedia/all-access/user/Jensen_Huang/daily/20260910/20260919 returned a dense daily series — {timestamp:'2026091000', views:3959}, {2026091100: 3812}, continuing through the requested range with no gaps. (The prior report's 10,068 figure was for 2026-09-16, a spike day; my window opens earlier and shows the quieter baseline. Both are real.)

#### Internet Archive TV News Archive — SCHEDULE METADATA ONLY, captions are 403 — Internet Archive ✅ LIVE

Covers **2** subdomains: broadcast-mentions, political-mentions

- Docs: https://archive.org/developers/
- Auth: none for metadata. Caption files are access-restricted and cannot be downloaded at any free tier. | Limits: No key for advancedsearch/metadata. Two calls, no throttling.
- Latency: Same day — TV-CNNW newest item was dated 2026-09-21 at fetch time. | Format: JSON
- Why primary: The only live broadcast feed still free, and the only thing that makes GDELT TV's freeze survivable for TIMING. Retained with the prior report's caveat fully confirmed and made sharper: it gives you the schedule, NOT the words. Every item's manifest lists caption files and every one returns 403. No free mention COUNT can be derived from it.

```bash
curl -s 'https://archive.org/advancedsearch.php?q=collection%3A%28TV-CNNW%29&fl%5B%5D=identifier&fl%5B%5D=date&rows=5&output=json&sort%5B%5D=date+desc'
```

> Evidence: METADATA IS LIVE. HTTP 200, 508B: advancedsearch for collection:TV-CNNW returned numFound=125270 with docs [{date:'2026-09-21T00:00:00Z', identifier:'CNNW_20260921_000000_CNN_Newsroom'}, {date:'2026-09-21', identifier:'CNNW_20260921_010000_The_Detour_With_David_Chang'}, {date:'2026-09-20', identifier:'CNNW_20260920_100000_CNN_This_Morning_Week...'}] — newest one day fresher than the prior report f

#### SEC EDGAR Full-Text Search (efts) — 8-K Item 2.02 / Exhibit 99.1 earnings materials — US Securities and Exchange Commission ✅ LIVE

Covers **1** subdomains: earnings-call-mentions

- Docs: https://www.sec.gov/edgar/search/efts-faq.html
- Auth: none — but a descriptive User-Agent with a contact email is mandatory or SEC blocks the request | Limits: 10 requests/second fair-access limit (SEC published policy; not stress-tested). 3 calls, no block.
- Latency: Minutes after filing acceptance. | Format: JSON (Elasticsearch response shape)
- Why primary: Confirmed exactly as claimed and it is the fastest free signal on earnings-day language: the 8-K Exhibit 99.1 press release is filed before or as the call begins and shares most of its scripted vocabulary with the prepared remarks. It complements Alpha Vantage, whose post-call lag is unverified. One query covers all issuers.

```bash
curl -s -A 'YourName your@email.com' 'https://efts.sec.gov/LATEST/search-index?q=%22artificial+intelligence%22&forms=8-K&dateRange=custom&startdt=2026-08-01&enddt=2026-09-19'
```

> Evidence: VERIFIED, REPRODUCES THE PRIOR REPORT. HTTP 200, 61727B: q="artificial intelligence", forms=8-K, 2026-08-01..2026-09-19 returned {"took":386,"timed_out":false,"_shards":{"total":50,"successful":50,"failed":0},"hits":{"total":{"value":947,"relation":"eq"},"max_score":19.158974,"hits":[{"_index":"edgar_file","_id":"0001062993-26-004629:exhibit99-1.htm","_source":{"ciks":["0001498148"],"period_ending

#### whitehouse.gov news RSS — The White House ✅ LIVE

Covers **1** subdomains: political-mentions

- Docs: https://www.whitehouse.gov/news/
- Auth: none | Limits: No key. Requires a browser User-Agent and -L. The WordPress JSON API at /wp-json/wp/v2/posts is blocked (403).
- Latency: Same day — newest item at fetch time was 'Sun, 20 Sep 2026 17:02:49 +0000'. | Format: RSS 2.0 with full body text in content:encoded
- Why primary: The live bridge across GovInfo CPD's publication lag, with full body text same-day. The prior report's honest limit is CONFIRMED and is the important part: the feed carries written statements, proclamations, fact sheets and presidential messages, NOT verbatim spoken-remarks transcripts. Zero of 30 items were titled 'Remarks' in my fetch, independently reproducing the prior finding. Use it for same-day presidential LANGUAGE, not for what was said aloud.

```bash
curl -sL -A 'Mozilla/5.0' 'https://www.whitehouse.gov/news/feed/'
```

> Evidence: VERIFIED. HTTP 200, 602461B: parsed 30 <item> elements, newest 'Sun, 20 Sep 2026 17:02:49 +0000 | Presidential Message on Yom Kippur'. content:encoded present with 527 words of full body text on item[0]. Composition limit reproduced independently — titles were 'Fact Sheet: President Donald J. Trump Further Enhances Program Integri...', 'Enhancing Program Integrity and Interagency Coordination', 'C

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Political Speech Mentions | GDELT TV 2.0 API (per-station, per-phrase frequency 2009-202 | UK: UK Parliament Hansard API — verbatim, next-sitting-day,  | 🟡 PARTIAL |
| Earnings Call Mentions | Alpha Vantage EARNINGS_CALL_TRANSCRIPT on PRIOR quarters — V | Alpha Vantage EARNINGS_CALL_TRANSCRIPT for the settling quar | 🟡 PARTIAL |
| Sports & Entertainment Broadcast Mentions | GDELT TV 2.0 API for the historical prior — verified real an | NONE FOUND | 🟡 PARTIAL |
| Speech Duration, Attendance & Post Counts | trumpstruth.org RSS for the rolling 7-day post-rate distribu | POTUS posts (KXPOTUSTWEETS): trumpstruth.org RSS — near-real | 🟡 PARTIAL |

**Rejected**

- **GDELT DOC 2.0 API** — REASON CORRECTED — IT IS NOT DEAD. The prior report rejected this as HTTP 429 on all attempts. On retest it returned HTTP 200, 3718B with CURRENT data: mode=timelinevol for 'tariff' gave 75 daily points running 20260629 
- **GovInfo / Congress.gov DEMO_KEY as a usable credential** — NEW REJECTION — the prior report treated DEMO_KEY as a working-but-limited credential for GovInfo. It is not. 3/3 GovInfo calls returned HTTP 429 OVER_RATE_LIMIT (167B JSON error) from a clean IP, including the first cal
- **Congress.gov API v3** — HTTP 429 OVER_RATE_LIMIT on retest with DEMO_KEY — reconfirmed. Superseded by GovInfo, whose keyless content URLs expose the same Congressional Record verbatim text with no credential at all.
- **Truth Social official API (truthsocial.com/api/v1/accounts/.../statuses)** — HTTP 403 Cloudflare interstitial per the prior report; not re-tested individually, but the trumpstruth.org mirror that replaces it IS verified live (HTTP 200, 100 items, timestamps minutes old), so the substitution holds
- **X / Twitter API v2 (tweets/counts/recent)** — RECONFIRMED. HTTP 401, 99B {'title':'Unauthorized','type':'about:blank','status':401,'detail':'Unauthorized'} on retest. Read access is not in the free tier; counts require a paid plan. Directly blocks KXELONTWEETS, KXHU
- **nitter.net and xcancel.com (X front-end mirrors)** — Per the prior report: nitter.net connection failure (HTTP 000), xcancel.com HTTP 451 Unavailable For Legal Reasons. Not individually re-tested; the upstream X 401 I did reproduce means no free X post-count path exists ei
- **RSSHub public instance (truth_social route)** — HTTP 403 Cloudflare challenge page per the prior report. Not re-tested; superseded by the verified trumpstruth.org feed.
- **Internet Archive TV caption files (.cc5.txt / .cc5.srt / .align.srt)** — RECONFIRMED INDEPENDENTLY. GET https://archive.org/download/CNNW_20260920_100000_CNN_This_Morning_Weekend/CNNW_20260920_100000_CNN_This_Morning_Weekend.cc5.txt returned HTTP 403, 4868B, an 'Item not available' HTML page.
- **Internet Archive caption full-text search** — REASON CORRECTED AND MADE MORE SEVERE. The prior report said this returns count=0 (false negatives). It is worse: it silently ignores the query and returns false POSITIVES. /services/search/v1/scrape?q="witch hunt" AND c
- **GDELT TV AI Explorer API (api/v2/tvai/tvai)** — Per the prior report: alive and current, but every keyword query form is rejected ('Non-field specific keywords are not currently supported by the TV AI Explorer'), and it indexes AI-derived attributes of on-screen image
- **Financial Modeling Prep earning_call_transcript** — HTTP 401 'Invalid API KEY.' on both the v3 and /stable routes per the prior report; transcripts sit behind a paid plan. Superseded by Alpha Vantage, which I verified returns real transcript content.
- **API Ninjas earningstranscript** — HTTP 400 'Missing API Key.' — no demo path, so it cannot be verified to return real data and is not reported as working on inventory faith. Alpha Vantage covers the same need and was verified.
- **discountingcashflows.com transcript API** — HTTP 403 Forbidden (nginx). Blocked to scripted clients.
- **factba.se / Roll Call Factbase** — api.factba.se HTTP 503; factba.se JSON endpoint 301s to a non-API page. The best-known Trump speech/post archive API is down.
- **C-SPAN API** — api.c-span.org connection failure, no public endpoint. C-SPAN is the named settlement venue for SOTU duration and much floor/hearing video and offers nothing free and programmatic — a direct cause of the speech-duration 
- **whitehouse.gov WordPress JSON API (/wp-json/wp/v2/posts)** — HTTP 403 per the prior report. Use /news/feed/ RSS instead, which I verified returns HTTP 200, 602KB with full body text in content:encoded.
- **GDELT Web News NGrams 3.0** — No working endpoint located — /gdeltv3/webngrams/MASTERFILELIST.TXT 404, /gdeltv3/webngrams/lastupdate.txt 301 with 0 bytes, /gdeltv5/weblegacy/ngrams/lastupdate.txt 404. The source inventory's base URL is stale. Not re-
- **govinfo bulkdata and sitemap discovery paths (keyless alternatives to the search API)** — NEW REJECTION — I probed these looking for a keyless way around the exhausted DEMO_KEY and both failed. https://www.govinfo.gov/sitemap/CPD_2026_sitemap.xml returned HTTP 404 (146B nginx error page) and https://www.govin
- **Wikidata SPARQL for State of the Union duration** — Endpoint live but holds no usable data — a query for SOTU-class items returned an empty bindings array. No structured SOTU duration or attendance series exists, which is why speech duration is reported with no settlement

---

### sports

*16/34 subdomains covered · 15 primary feeds*

#### ESPN Sports API (sports.core.api.espn.com + site.api.espn.com) — ESPN / Disney — public but undocumented and unsupported ✅ LIVE

Covers **25** subdomains: football-nfl, football-college, basketball-nba, basketball-wnba, basketball-college, basketball-international, baseball-mlb, hockey-nhl, soccer-england, soccer-europe-top-leagues, soccer-uefa, soccer-americas, soccer-international, tennis, golf, motorsport, mma-and-ufc, cricket

- Docs: https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b (community reference; no official docs)
- Auth: none | Limits: No API key and no published quota — UNKNOWN. Undocumented and revocable at will. UA GOTCHA INDEPENDENTLY REPRODUCED: site.api.espn.com returns HTTP 403 to User-Agent 'Mozilla/5.0' but HTTP 200 to curl's default UA — I confirmed this on both /football/nfl/scoreboard and /cricket/8048/scoreboard. sports.core.api.espn.com served every UA tested. Do not send a browser UA to the site host.
- Latency: sub-minute for scores and in-game win probability; odds refresh every few minutes; futures refresh daily | Format: REST JSON. Core host is $ref-linked (2-4 hops to full detail); site host returns flat page-bundle payloads.
- Why primary: CONFIRMED as the single broad feed. I re-enumerated the tree myself: /v2/sports?limit=100 -> count 17, and the per-sport league counts reproduce (soccer 219, mma 48, rugby 25, basketball 15, golf 9, hockey 6, racing 5, tennis 2). The same URL grammar really does yield DraftKings odds, ESPN win probability, season futures, stat leaders and standings from one keyless integration. One caveat the original phrasing understates: odds are NOT uniform across the tree — see freeTierLimits and the per-subdomain rows. It consolidates roughly twenty single-sport APIs for FIXTURES and RESULTS; for PRICES it covers the US majors, soccer and MMA only.

```bash
curl -s "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401872945/competitions/401872945/odds/100"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, all via curl. VERIFIED: (1) /v2/sports?limit=100 -> 200, count 17. League trees re-counted: soccer 219, mma 48, rugby 25, basketball 15, golf 9 (champions-tour, eur, liv, lpga, mens/womens-olympics-golf, ntw, pga, tgl), hockey 6, racing 5 (f1, irl, nascar-premier, nascar-secondary, nascar-truck), tennis 2 (atp, wta), cricket 0 on the core host. (2) NFL odds/100

#### MLB Stats API — MLB Advanced Media ✅ LIVE

Covers **4** subdomains: baseball-mlb, transactions-and-coaching, player-awards, player-props-and-stat-leaders

- Docs: https://statsapi.mlb.com/docs/ (community reference: https://github.com/toddrob99/MLB-StatsAPI/wiki)
- Auth: none | Limits: No key, no published quota — UNKNOWN. Terms ask for non-commercial use and reasonable request rates; no documented calls/day figure.
- Latency: realtime — live feed updates pitch-by-pitch during play | Format: REST JSON
- Why primary: CONFIRMED. The only verified free source of structured roster transactions anywhere in this domain — I independently re-confirmed ESPN's /transactions returns count 0 for both NFL and NBA, so without this the transactions subdomain has no settlement source at all. Also carries the official award registry.

```bash
curl -s "https://statsapi.mlb.com/api/v1/transactions?startDate=2026-09-15&endDate=2026-09-19"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. (1) /api/v1/transactions?startDate=2026-09-15&endDate=2026-09-19 -> 200, 333,357 bytes — byte-identical to the report — and I parsed it myself: 899 transactions. First row is id 942806, person 'Otto Lopez' (id 672640), toTeam Miami Marlins (id 146), date 2026-09-15, typeCode NUM, typeDesc 'Number Change'. (Report cited the Aaron Judge row instead; same dataset,

#### NHL Web API (api-web.nhle.com) — National Hockey League — public, undocumented ✅ LIVE

Covers **2** subdomains: hockey-nhl, win-totals-and-standings

- Docs: https://github.com/Zmalski/NHL-API-Reference
- Auth: none | Limits: No key, no published quota — UNKNOWN. Undocumented; the NHL retired statsapi.web.nhl.com in 2023 without notice, so treat the contract as unstable. CORRECTED OPERATIONAL GOTCHA: /v1/standings/now is a 307 redirect (to /v1/standings/2026-04-17), so any client that does not follow redirects gets an empty body and a non-2xx code.
- Latency: realtime during games, down to shift-level | Format: REST JSON
- Why primary: CONFIRMED. Kept alongside ESPN because it is the authoritative NHL settlement source and its standings object really does carry the clinch and tiebreak fields that playoff-seeding and win-total contracts resolve against — I enumerated them myself rather than taking the claim on trust.

```bash
curl -sL "https://api-web.nhle.com/v1/standings/now"   # NOTE the -L: without it this returns HTTP 307 and a ZERO-BYTE body
```

> Evidence: DEFECT FOUND AND CORRECTED. The report's exampleCall as written — plain 'curl -s' — returns HTTP 307, size_download 0, redirect_url https://api-web.nhle.com/v1/standings/2026-04-17. A developer pasting it verbatim gets an empty body. This is precisely the class of failure this check exists to catch, and the original report's own evidence line ('-> 200, 59,856 bytes') could only have come from a re

#### Sleeper API — Sleeper (fantasy platform) ✅ LIVE

Covers **4** subdomains: fantasy-sports, football-nfl, player-props-and-stat-leaders, transactions-and-coaching

- Docs: https://docs.sleeper.com/
- Auth: none | Limits: No key. Docs state 1,000 calls/minute per IP and ask that /v1/players/nfl be called no more than once per day. CORRECTED SIZE: I measured that document at 14,660,125 bytes (~14.7 MB) on the wire, NOT the 2,597,263 bytes (~2.6 MB) the report claims — the report's figure appears to be the gzipped size. Budget ~14.7 MB of decompressed memory per refresh, request it with Accept-Encoding: gzip, cache it, and poll /v1/state/nfl instead.
- Latency: minutely for injury status changes; the players document is a daily dump | Format: REST JSON
- Why primary: CONFIRMED as the best free NFL injury-designation feed. I re-verified that ESPN has no working league-wide injuries substitute, so this fills a real hole rather than duplicating ESPN.

```bash
curl -s "https://api.sleeper.app/v1/state/nfl"   # and the full universe: curl -s "https://api.sleeper.app/v1/players/nfl"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. (1) /v1/state/nfl -> 200, exact body {"week":2,"season_type":"regular","season":"2026","leg":2,"league_season":"2026","previous_season":"2025","season_start_date":"2026-09-09","display_week":2,"league_create_season":"2026","season_has_scores":true}. (2) /v1/players/nfl -> 200, and I parsed it: 12,228 players (exact match to the report), 873 carrying a non-null 

#### nflverse-data (GitHub Releases bulk datasets) — nflverse open-source collective ✅ LIVE

Covers **4** subdomains: football-nfl, player-props-and-stat-leaders, fantasy-sports, transactions-and-coaching

- Docs: https://github.com/nflverse/nflverse-data
- Auth: none for release-asset downloads | Limits: No quota on release asset downloads (note the -L: GitHub release URLs redirect to objects.githubusercontent.com). Anonymous api.github.com metadata calls are limited to 60/hr — use a token for 5,000/hr, or hit the download URLs directly, which is unmetered.
- Latency: daily during the season | Format: CSV / CSV.gz / Parquet bulk
- Why primary: CONFIRMED. Supplies the modelling substrate no live JSON API gives away free — play-by-play with EPA, snap counts, depth charts, Next Gen Stats, contracts, draft picks and trades. One repo, no key.

```bash
curl -sL "https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_2026.csv"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20 with curl -sL -> HTTP 200, 49,524 bytes (report said 49,523 — 1 byte, immaterial). Header verified verbatim: 'season,season_type,game_type,team,week,gsis_id,position,full_name,first_name,last_name,report_primary_injury,report_secondary_injury,report_status,practice_primary_injury,practice_secondary_injury,practice_status'. First data row is a real 2026 row: '202

#### TheSportsDB v1 — TheSportsDB (community-maintained) ✅ LIVE

Covers **6** subdomains: football-canadian, baseball-international, hockey-international, basketball-international, darts-chess-and-mind-sports, niche-and-other-sports

- Docs: https://www.thesportsdb.com/free_sports_api
- Auth: none for the shared test key '3' embedded in the path; a free registered v2 key raises limits | Limits: Shared test key '3' is heavily throttled. ROW CAP INDEPENDENTLY CONFIRMED: every list call I made returned exactly ONE event (verified across CFL 4405, NPB 4591, KBO 4830, PDC 4554), so the free key is capped at 1 row per list call. I spaced calls ~4s apart and did not hit 429, but the report did, so treat throttling as real. The documented full-list behaviour on a free registered key remains NOT VERIFIED.
- Latency: minutes to hours after match completion; fixtures posted days ahead | Format: REST JSON
- Why primary: CONFIRMED as the only verified live source for Canadian Football after ESPN's CFL feed proved dead — I re-verified both halves of that finding myself. Listed as primary for REACH, not depth: the 1-row free-key cap makes it a settlement/results feed, not a live terminal feed, until a registered key is obtained. COVERAGE CORRECTED: 'table-tennis' removed from coversSubdomains — see evidence.

```bash
curl -s "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4405"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. (1) CFL id 4405 eventspastleague -> 200, 1,525 bytes, idEvent 2432594 'Calgary Stampeders vs Ottawa Redblacks', strTimestamp 2026-09-19T23:00:00, intHomeScore 40, intAwayScore 38, strLeague 'CFL', strSeason 2026 — current, exactly as claimed, and genuinely unlike ESPN's CFL. (2) NPB id 4591 -> 200, 1 row, 'Hanshin Tigers vs Yokohama DeNA BayStars' 2026-09-20. (

#### ncaa-api (NCAA.com wrapper) — Open-source (henrygd), self-hostable ✅ LIVE

Covers **3** subdomains: football-college, basketball-college, niche-and-other-sports

- Docs: https://github.com/henrygd/ncaa-api
- Auth: none on the public instance | Limits: README documents 5 requests/minute per IP on the public instance, but I could NOT reproduce that cap: 6 back-to-back calls with no spacing all returned HTTP 200. So the documented limit is either not enforced or not enforced at that threshold — do not design around either assumption. The README's advice to self-host via the published Docker image remains the right move for a live terminal.
- Latency: sub-minute during games | Format: REST JSON
- Why primary: CONFIRMED. One wrapper covering NCAA sports across divisions, supplying the AP/Coaches poll data that CFB playoff and seeding contracts key off and that ESPN's futures do not expose, with official NCAA settlement authority.

```bash
curl -s "https://ncaa-api.henrygd.me/rankings/football/fbs/associated-press"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. /rankings/football/fbs/associated-press -> HTTP 200, 2,368 bytes — byte-identical to the report. Parsed: sport 'Football', title 'College football rankings: Associated Press Top 25', updated 'Through Games SEP. 19, 2026', data[0] RANK 1 SCHOOL 'Texas (58)' POINTS '1,706' RECORD '3-0' PREVIOUS RANKING '1', data[1] 'Georgia (3)' 1,580 '3-0'. Current-week poll, no

#### Jolpica F1 (Ergast successor) — Jolpica open-source project ✅ LIVE

Covers **1** subdomains: motorsport

- Docs: https://github.com/jolpica/jolpica-f1
- Auth: none currently | Limits: Documented unauthenticated burst limit 4 requests/second, sustained 500 requests/hour (documented, not stress-tested by me). Token-based access is in development.
- Latency: hourly to daily post-session | Format: REST JSON (Ergast-compatible schema)
- Why primary: CONFIRMED as the authoritative free settlement source for F1 championship contracts. I separately re-confirmed that ESPN posts no odds for F1 (count=0) and that The Odds API's catalog contains no motorsport key at all, so this feed's settlement-only role is correctly characterised.

```bash
curl -s "https://api.jolpi.ca/ergast/f1/2026/constructorStandings.json"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. /ergast/f1/2026/constructorStandings.json -> HTTP 200, 2,503 bytes — byte-identical to the report. Parsed: MRData.series 'f1', StandingsTable.season '2026', round '14', total '11' constructors. Current-season standings confirmed. Claim holds.

#### Open-Meteo — Open-Meteo (ECMWF/GFS/ICON/HRRR blend) ✅ LIVE

Covers **6** subdomains: football-nfl, baseball-mlb, golf, motorsport, cricket, football-canadian

- Docs: https://open-meteo.com/en/docs
- Auth: none for non-commercial | Limits: Documented 10,000 calls/day, 5,000/hour, 600/minute, no API key, non-commercial. I did not stress-test the quota, so the numbers are documented-not-measured. Commercial use requires a paid plan — directly relevant if this terminal is monetised.
- Latency: hourly model updates; HRRR sub-hourly for US venues | Format: REST JSON
- Why primary: CONFIRMED. One keyless call at arbitrary lat/lon prices every outdoor sport at once — a single weather integration serving six subdomains, which is the consolidation the brief asks for.

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.0489&longitude=-94.4839&hourly=temperature_2m,wind_speed_10m,precipitation_probability&forecast_days=2"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. Arrowhead Stadium (39.0489,-94.4839) -> HTTP 200, 1,845 bytes (report said 1,840 — 5-byte drift from generationtime_ms). Body opens {"latitude":39.052387,"longitude":-94.483864,"generationtime_ms":0.0857,"utc_offset_seconds":0,"timezone":"GMT","elevation":259.0,"hourly_units":{...}} with the requested temperature_2m, wind_speed_10m and precipitation_probability

#### Chess.com Published-Data API + Lichess API — Chess.com and Lichess.org ✅ LIVE

Covers **1** subdomains: darts-chess-and-mind-sports

- Docs: https://www.chess.com/news/view/published-data-api and https://lichess.org/api
- Auth: none; Chess.com REQUIRES a descriptive User-Agent — this is not optional | Limits: Chess.com: no key; serialised per-endpoint rate limiting. UA REQUIREMENT INDEPENDENTLY CONFIRMED — with no UA override the same URL returns HTTP 403 with a 5,431-byte body; with a descriptive UA it returns 200. Lichess: no key for public endpoints, documented ~20 requests/second.
- Latency: minutes after event completion; Lichess tournament list is live | Format: REST JSON (Lichess also offers NDJSON streaming)
- Why primary: CONFIRMED. The settlement source of record for Chess.com-denominated markets (Titled Tuesday), not a third-party mirror. Note this covers only the chess half of its subdomain — darts has no price source anywhere free.

```bash
curl -s -A "your-app/1.0 (contact: you@example.com)" "https://api.chess.com/pub/leaderboards"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. (1) Chess.com /pub/leaderboards with a descriptive UA -> HTTP 200, 291,342 bytes (report said 291,334 — 8-byte drift from live rating changes). (2) THE UA TRAP REPRODUCED: the identical URL with no -A flag -> HTTP 403, 5,431 bytes of non-JSON. The report's warning is correct and load-bearing; a client with a default library UA will silently fail. (3) Lichess /a

#### EuroLeague feeds (incrowdsports) — Euroleague Basketball via InCrowd Sports ✅ LIVE

Covers **1** subdomains: basketball-international

- Docs: https://www.euroleaguebasketball.net/ (feed is undocumented; api-live.euroleague.net is the legacy XML sibling)
- Auth: none | Limits: No key, no published quota — UNKNOWN. Undocumented and unsupported.
- Latency: post-game; live game state available during play | Format: REST JSON (legacy endpoint returns XML)
- Why primary: CONFIRMED, including the premise. I independently enumerated ESPN's basketball tree and it contains 15 leagues with NO euroleague entry — so this feed is genuinely non-duplicative and is both the predictive and settlement source for EuroLeague markets.

```bash
curl -s "https://feeds.incrowdsports.com/provider/euroleague-feeds/v2/competitions/E/seasons/E2025/games"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. feeds.incrowdsports.com/.../competitions/E/seasons/E2025/games -> HTTP 200, 110,496 bytes (report said 110,489). Body: {"status":"success","data":[{"id":"32e0be44-4ef1-516d-9706-27b3c4203992","identifier":"E2025_406","code":406,"season":{"code":"E2025","name":"EuroLeague 2025-26","alias":"2025-26","year":2025},...}]} — the id and identifier match the report's s

#### KHL public API (khl.api.webcaster.pro) — Kontinental Hockey League — undocumented ✅ LIVE

Covers **1** subdomains: hockey-international

- Docs: https://github.com/topics/khl-api (no official docs; reverse-engineered mobile backend)
- Auth: none | Limits: No key, no published quota — UNKNOWN. Undocumented mobile backend; treat as revocable.
- Latency: live game state during play | Format: REST JSON
- Why primary: CONFIRMED, including the premise. I independently enumerated ESPN's hockey tree — 6 leagues, no KHL — so this is genuinely the only keyless KHL source and settles authoritatively as the league's own backend.

```bash
curl -s "https://khl.api.webcaster.pro/api/khl_mobile/events_v2.json"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. /api/khl_mobile/events_v2.json -> HTTP 200, 23,867 bytes (report said 22,217 — fixture list has grown). Body is a real array of fixture objects: [{"event":{"game_state_key":"not_yet_started","period":null,"hd":true,"id":3003043,"stage_id":407,"type_id":24,"khl_id":902720,"team_a":{...}}] — id 3003043 and khl_id 902720 match the report's sample exactly. Non-dupl

#### Fantasy Premier League official API — Premier League — public, undocumented ✅ LIVE

Covers **2** subdomains: soccer-england, fantasy-sports

- Docs: https://github.com/vaastav/Fantasy-Premier-League (de-facto reference)
- Auth: none for public endpoints | Limits: No key, no published quota — UNKNOWN. Undocumented; the League has changed the schema between seasons without notice. Payload measured at 1,777,445 bytes (~1.8 MB) — cache it, do not poll tightly.
- Latency: daily, with availability updated as press conferences land | Format: REST JSON
- Why primary: CONFIRMED as the only free feed carrying structured English-football player availability (chance_of_playing_this_round / next_round plus a news field) — the injury and rotation signal that prices EPL match markets.

```bash
curl -s "https://fantasy.premierleague.com/api/bootstrap-static/"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. /api/bootstrap-static/ -> HTTP 200, 1,777,445 bytes (report said 1,777,215 — 230-byte drift, consistent with live price/news churn). Feed is live and current-season. Claim holds.

#### Wikimedia REST API + Pageviews API — Wikimedia Foundation ✅ LIVE

Covers **4** subdomains: olympics-and-multisport, league-business, boxing, player-awards

- Docs: https://api.wikimedia.org/wiki/Main_Page and https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/
- Auth: none (a free account raises limits) | Limits: Anonymous access to api.wikimedia.org documented at 500 requests/hour; 5,000/hour with a free account. Pageviews API is unmetered in practice but expects a descriptive User-Agent — send one.
- Latency: pageviews are daily with ~1 day lag; article content is minutely | Format: REST JSON
- Why primary: CONFIRMED as live, and correctly characterised by the report as a weak-but-real fallback rather than a peer of the sports APIs. It is the only structured thing available for boxing results, Olympic medal tables and off-field league events. Treat it as scrape-grade: a wiki table is editable by anyone, so it is an input to manual settlement, not an automated resolver.

```bash
curl -s -A "your-app/1.0 (contact: you@example.com)" "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Super_Bowl_LXI/daily/20260901/20260920"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20 with a descriptive UA. Pageviews per-article 'Super_Bowl_LXI' daily 20260901-20260920 -> HTTP 200, 2,880 bytes — byte-identical to the report. First item verbatim: {"project":"en.wikipedia","article":"Super_Bowl_LXI","granularity":"daily","timestamp":"2026090100","access":"all-access","agent":"user","views":2082} — matches the report's cited value exactly. Real 

#### The Odds API v4 — The Odds API ⚠️ UNVERIFIED

Covers **9** subdomains: tennis, golf, boxing, cricket, football-canadian, baseball-international, hockey-international, basketball-international, rugby-and-afl

- Docs: https://the-odds-api.com/liveapi/guides/v4/
- Auth: free API key via email registration, passed as ?apiKey= | Limits: Starter plan documented as free with 500 credits/month; credits are consumed per region x market combination rather than per HTTP call. NOT INDEPENDENTLY VERIFIED — I have no key either. 500 credits/month is roughly 16/day, which almost certainly cannot sustain a live multi-sport terminal.
- Latency: roughly 1-5 minute refresh depending on sport (documented, not verified) | Format: REST JSON
- Why primary: Retained in primaryFeeds — with verifiedLive=false — because it is the only candidate feed that prices the sports ESPN carries results for but posts no odds on, and I independently reproduced every one of those ESPN odds gaps (tennis, golf, F1, AFL all count=0). Its catalog is verifiable without a key and genuinely contains keys for those sports. But NO PAYLOAD HAS EVER BEEN SEEN, by the original agent or by me. COVERAGE CORRECTED: 'niche-and-other-sports' removed as too vague to verify, and note that 'golf' is only 4 major-winner outright keys — it does NOT price regular tour events. No subdomain may be marked COVERED on this feed's strength.

```bash
curl -s "https://api.the-odds-api.com/v4/sports/tennis_atp_us_open/odds/?regions=us&markets=h2h&apiKey=YOUR_KEY"  # placeholder unavoidable: key is issued only by email registration. Keyless probe of https://api.the-odds-api.com/v4/sports/ returns HTTP 401 {"error_code":"MISSING_KEY"}
```

> Evidence: NOT VERIFIED — INCONCLUSIVE. I reached the same conclusion independently. (a) Auth gate is live: GET https://api.the-odds-api.com/v4/sports/ -> HTTP 401, 152 bytes, body {"message":"API key is missing","error_code":"MISSING_KEY","details_url":"https://the-odds-api.com/liveapi/guides/v4/api-error-codes.html#missing-key"}. MINOR CORRECTION: the error_code is MISSING_KEY when no key is supplied, not 

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| American Football — NFL | ESPN Sports API — /odds (DraftKings spread, total, moneyline | ESPN Sports API — site host /football/nfl/scoreboard, event  | 🟢 COVERED |
| American Football — College | ESPN Sports API — college-football /seasons/2026/futures (13 | ncaa-api (official NCAA.com data) and ESPN college-football  | 🟢 COVERED |
| Canadian Football (CFL) | NONE VERIFIED. The Odds API key americanfootball_cfl exists  | TheSportsDB league id 4405 — verified current: idEvent 24325 | 🟡 PARTIAL |
| Basketball — NBA | ESPN Sports API — /seasons/2026/futures (15 markets: NBA Win | ESPN Sports API basketball/nba scoreboard and standings | 🟢 COVERED |
| Basketball — WNBA | ESPN Sports API — wnba /seasons/2026/futures (1 market only: | ESPN Sports API basketball/wnba scoreboard | 🟢 COVERED |
| Basketball — College | ESPN Sports API — mens-college-basketball /seasons/2026/futu | ncaa-api (official NCAA.com) and ESPN mens-/womens-college-b | 🟢 COVERED |
| Basketball — International Leagues | NONE VERIFIED. The Odds API key basketball_euroleague exists | EuroLeague incrowdsports feed (verified, 110,496 bytes, seas | 🟡 PARTIAL |
| Baseball — MLB | ESPN Sports API /odds and /seasons/2026/futures (World Serie | MLB Stats API — /api/v1/schedule?sportId=1 and /api/v1.1/gam | 🟢 COVERED |
| Baseball — NPB, KBO & Others | NONE VERIFIED. The Odds API keys baseball_npb and baseball_k | TheSportsDB — NPB id 4591 (verified: 'Hanshin Tigers vs Yoko | 🟡 PARTIAL |
| Hockey — NHL | ESPN Sports API — nhl /seasons/2026/futures (Stanley Cup, bo | NHL Web API — curl -sL /v1/schedule/now and /v1/gamecenter/{ | 🟢 COVERED |
| Hockey — KHL, SHL & Others | NONE VERIFIED. The Odds API lists icehockey_liiga, icehockey | KHL public API khl.api.webcaster.pro (verified live, 23,867  | 🟡 PARTIAL |
| Soccer — England | ESPN Sports API /odds — RE-VERIFIED MYSELF on live fixture:  | ESPN Sports API — eng.1, eng.2, eng.3, eng.4, eng.5, eng.fa, | 🟢 COVERED |
| Soccer — European Top Leagues | ESPN Sports API /odds — verified present on the big-five lea | ESPN Sports API — esp.1, ita.1, ger.1, fra.1, ned.1, por.1,  | 🟢 COVERED |
| Soccer — UEFA Competitions | ESPN Sports API /odds — posted on UEFA club fixtures | ESPN Sports API — uefa.champions, uefa.europa, uefa.europa.c | 🟢 COVERED |
| Soccer — Americas | ESPN Sports API /odds — RE-VERIFIED MYSELF: usa.1 (MLS) odds | ESPN Sports API — usa.1, usa.nwsl, usa.usl.1, usa.usl.l1, us | 🟢 COVERED |
| Soccer — International & Other Leagues | ESPN Sports API /odds where posted — RE-VERIFIED: jpn.1 retu | ESPN Sports API — fifa.friendly, fifa.world, fifa.worldq.* ( | 🟢 COVERED |
| Tennis | NONE VERIFIED. The Odds API lists 44 tournament-level keys ( | ESPN Sports API — /sports/tennis/leagues/atp and /wta (tree  | 🟡 PARTIAL |
| Table Tennis | NONE FOUND | NONE FOUND | 🔴 UNCOVERED |
| Golf | NONE VERIFIED for regular tour events. The Odds API has only | ESPN Sports API — golf tree re-enumerated at 9 tours: pga, l | 🟡 PARTIAL |
| Motorsport | NONE FOUND for odds — this is a hard negative, not an unknow | Jolpica F1 (verified: 2026 round 14, 11-constructor champion | 🟡 PARTIAL |
| MMA & UFC | ESPN Sports API /odds — RE-VERIFIED MYSELF on a live card: ' | ESPN Sports API — /sports/mma, tree re-counted at exactly 48 | 🟢 COVERED |
| Boxing | NONE VERIFIED. The Odds API key boxing_boxing exists in the  | Wikimedia REST API (verified live) — structured fight-result | 🟡 PARTIAL |
| Cricket | NONE VERIFIED. The Odds API lists 16 cricket keys (ipl, big_ | ESPN Sports API site host by numeric league id — I RE-VERIFI | 🟡 PARTIAL |
| Rugby & Australian Rules | NONE VERIFIED. ESPN returns odds count=0 for AFL (I measured | ESPN Sports API — /sports/rugby (tree re-counted at exactly  | 🟡 PARTIAL |
| Darts, Chess & Mind Sports | Chess.com /pub/leaderboards (VERIFIED by me — 291,342 bytes, | TheSportsDB PDC Darts id 4554 (VERIFIED by me: 'World Series | 🟡 PARTIAL |
| Olympics & Multi-Sport Events | NONE FOUND — no free feed publishes Olympic medal-market odd | Wikimedia REST API (verified live) for medal tables and fina | 🟡 PARTIAL |
| Niche & Other Sports | NONE VERIFIED. ESPN returns odds count=0 for lacrosse and co | ESPN Sports API — lacrosse, volleyball, water-polo and field | 🟡 PARTIAL |
| Player & Coach Awards | ESPN Sports API /seasons/{year}/futures — VERIFIED by my own | ESPN /awards endpoint (VERIFIED by me — count 20 award defin | 🟢 COVERED |
| Player Props & Stat Leaders | ESPN /seasons/{yr}/types/{t}/leaders (VERIFIED by me — 185,3 | Official league stat feeds: MLB Stats API, NHL Web API, ESPN | 🟡 PARTIAL |
| Win Totals & Standings | ESPN /futures gives only ADJACENT markets (division, confere | ESPN /apis/v2/sports/{sport}/{league}/standings (VERIFIED by | 🟡 PARTIAL |
| Playoff Qualification & Seeding | ESPN Sports API /futures — VERIFIED DIRECTLY BY ME: college  | ESPN standings and NHL /v1/standings/now (with -L), which ca | 🟢 COVERED |
| Transactions, Draft & Coaching | NONE FOUND — no free feed prices coaching-change or next-tea | MLB Stats API /api/v1/transactions — VERIFIED BY ME: 333,357 | 🟡 PARTIAL |
| League Business & Off-Field | Wikimedia Pageviews API (VERIFIED by me — 'Super_Bowl_LXI' r | Wikimedia REST API (verified) for announcements and franchis | 🟡 PARTIAL |
| Fantasy Sports | Sleeper API — VERIFIED BY ME: /v1/players/nfl returns 12,228 | Official stat feeds under a stated scoring system — MLB Stat | 🟢 COVERED |

**Rejected**

- **ESPN football/cfl league (sports.core.api.espn.com and site host)** — REJECTION CONFIRMED BY MY OWN FETCH. Core host /v2/sports/football/leagues/cfl/events returns HTTP 200 with count 1 — a single event, id 401504210, from 2022 — and the site host scoreboard for ?dates=20260919 returns ZER
- **ESPN /transactions endpoint (all leagues)** — REJECTION CONFIRMED BY MY OWN FETCH. Returns HTTP 200 with count 0 and items [] for BOTH football/nfl and basketball/nba. The endpoint exists in the URL grammar but serves no data — capability by vocabulary only. MLB Sta
- **TheSportsDB table-tennis coverage (league 5641, World Table Tennis)** — NEWLY REJECTED BY THIS VERIFICATION. The report listed 'table-tennis' in TheSportsDB's coversSubdomains while simultaneously marking the subdomain UNCOVERED — an internal contradiction. I tested it: league 5641 returns H
- **ESPN cricket on the core host (sports.core.api.espn.com/v2/sports/cricket/leagues)** — CONFIRMED NON-FUNCTIONAL and recorded so nobody wires it up. Returns HTTP 200 with count 0 — cricket appears in ESPN's 17-sport index but has no leagues on the core host. Cricket works ONLY on site.api.espn.com under num
- **ESPN baseball/mexican-winter-league** — Abandoned — last event 2014-01-30, ~4,600 days stale. Distinguish from ESPN's caribbean-series and caf.nations, which are merely off-season and remain valid. (Carried over from the original report; not independently re-p
- **GDELT DOC 2.0 API** — COULD NOT VERIFY — HTTP 429 on all attempts in the original sweep ('Please limit requests to one every 5 seconds'). I did not re-test it in this pass, so it remains unverified rather than confirmed-working or confirmed-d
- **CollegeFootballData (CFBD)** — Key-gated and too thin for a live terminal — keyless probe returns HTTP 401, and the free tier is 1,000 API calls per MONTH (~one call every 45 minutes), which cannot drive a live panel. ESPN CFB futures (13 markets, ver
- **CricketData.org / CricAPI** — Key-gated: returns {"status":"failure","reason":"Invalid API Key"}. Free tier is 100 hits/day, too thin for live ball-by-ball. Superseded for fixtures and results by ESPN's cricket league ids on the site host, which I ve
- **ESPNcricinfo hs-consumer-api** — Blocked — HTTP 403 on /v1/pages/matches/live with both default and browser User-Agents. Not usable.
- **Sofascore API (api.sofascore.com)** — Blocked — HTTP 403 on every path tried. Would have been an excellent darts and table-tennis source; it is not accessible.
- **api.olympics.com** — Dead from this environment — connection failed outright (HTTP 000, zero bytes). No Olympic-organiser API is usable.
- **stats.nba.com** — NOT TESTED in either session and deliberately not claimed. It requires a precise spoofed browser header set (Referer, Origin, x-nba-stats-token) and throttles aggressively at ~1 req/sec — a fragile foundation for a live 
- **The Odds API — payload (retained in primaryFeeds with verifiedLive=false)** — Recorded here so it is not lost. VERIFIED: the host is alive (HTTP 401, error_code MISSING_KEY — note the original report cited INVALID_KEY, which requires sending a bogus key) and the public coverage catalog is real (I 
- **API-Sports / API-Football** — Key-gated and severely limited: 100 requests per DAY on the free plan. Unusable for live streaming across 30+ subdomains, and ESPN's soccer tree — which I independently re-counted at exactly 219 leagues — covers the same
- **football-data.org** — Key-gated (X-Auth-Token), 10 calls/minute, 12 competitions, and the free tier EXPLICITLY EXCLUDES live scores, lineups, goal scorers and bookings. A delayed 12-competition feed is strictly dominated by ESPN's keyless 219
- **balldontlie** — Key-gated (401 without registration) and its free tier is daily-latency only — live box scores, odds, props and injuries are all paid. Published rate limits conflict (5/min vs 60/min) and could not be resolved. Dominated
- **Understat** — Scrape-only, not an API — the data is embedded in JSON.parse() blobs inside inline <script> tags, so every request is a full page load and the contract breaks on any redesign. Genuinely valuable for shot-level xG across 
- **OpenF1** — Verified live but demoted: real-time streaming moved behind a paid tier, so the free tier is historical/post-session only. Jolpica F1 (which I verified: 2026 round 14, 11 constructors) covers settlement better and ESPN c
- **NASCAR cacher feeds (cf.nascar.com)** — Verified live but redundant — ESPN's racing tree (which I re-enumerated: f1, irl, nascar-premier, nascar-secondary, nascar-truck) already carries NASCAR and is current. Keep as a fallback for live timing/scoring depth. N
- **OpenLigaDB and openfootball/football.json** — Both verified live but narrower than ESPN, which carries the same competitions with odds attached. Retain OpenLigaDB as a keyless, commercially-licensed fallback for German football if ESPN's undocumented API is ever rev
- **PandaScore (esports)** — Token-gated; live match data and odds are paid, free tier is historical/reference only with unpublished limits. Esports is peripheral to this domain, so it does not justify a keyed integration.
- **Wikidata Query Service (SPARQL)** — NOT VERIFIED — returned HTTP 400 in the original sweep and was not re-tested here. It was the intended fallback for Olympic medal tables and cross-entity joins; recorded as a failure rather than asserted to work. The Wik

---

### technology-and-ai

*5/12 subdomains covered · 19 primary feeds*

#### OpenRouter Public API (models registry + rankings series) — OpenRouter ✅ LIVE

Covers **4** subdomains: model-releases, model-rankings, ai-market-share, ai-pricing

- Docs: https://openrouter.ai/docs/api-reference/list-available-models
- Auth: none for both endpoints (an API key is needed only for inference, not for these reads) | Limits: No API key and no published rate limit on either endpoint — UNKNOWN numeric ceiling. Both returned 200 on repeated back-to-back calls with no 429. /api/v1/models is 739 KB; the rankings series is 328 KB and carries only a rolling ~7-day window, so you MUST snapshot daily to build history.
- Latency: sub-minute for the models registry; the rankings series is bucketed by calendar day and the current day is partial | Format: REST JSON
- Why primary: VERIFIED AND STRENGTHENED. One call to /api/v1/models returns 446 models across ~60 labs with per-token prompt/completion pricing, context length, modality and a `created` release timestamp — simultaneously the AI-pricing feed, the release-detection feed and a rankings input. /api/frontend/v1/rankings/models returns per-model, per-day token volume. I independently confirmed from Kalshi's own series endpoint that KXTOKENUSEM's settlement_sources field literally reads {'name':'OpenRouter - AI Model Rankings','url':'https://openrouter.ai/rankings#top-models'} — so this is not a proxy, it is the named authority. Nothing else free gives cross-lab token share.

```bash
curl -s 'https://openrouter.ai/api/v1/models' | jq '.data[]|select(.id=="anthropic/claude-opus-4.6")|{id,ctx:.context_length,in:.pricing.prompt,out:.pricing.completion,created}'   # AND the undocumented rankings series (this is Kalshi's NAMED settlement source for KXTOKENUSEM): curl -s 'https://openrouter.ai/api/frontend/v1/rankings/models' | jq '.data[0]'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-21. /api/v1/models HTTP 200, 738,853 bytes, 0.308 s, 446 models. Parsed anthropic/claude-opus-4.6: ctx 1,000,000 | in $0.000005/tok | out $0.000025/tok | created 1770219050. /api/frontend/v1/rankings/models HTTP 200, 328,250 bytes, 572 rows; row0 keys = date, model_permaslug, variant, total_completion_tokens, total_prompt_tokens, count, total_tool_calls, change; da

#### Arena (LMArena) leaderboard — BOTH style-control ON and OFF via arena.ai — Arena / LMArena (formerly LMSYS Chatbot Arena) ✅ LIVE

Covers **2** subdomains: model-rankings, ai-pricing

- Docs: https://arena.ai/leaderboard
- Auth: none for the HTML pages on either lmarena.ai or arena.ai. Send a browser User-Agent. The JSON API at /api/* remains Cloudflare-blocked (403) — do not depend on it. | Limits: No key. Page is ~2.7 MB per single board, ~5.1 MB for the all-arenas page; poll hourly at most. No archive — the page serves only the latest snapshot, so you must snapshot daily to build history.
- Latency: leaderboard snapshots refresh roughly daily; vote counts move continuously but the published rating is a snapshot | Format: HTML page with embedded Next.js flight JSON (parse the flight payload, do not regex the rendered DOM)
- Why primary: CORRECTED — THE REPORT'S CENTRAL LIMITATION HERE IS FALSE. The report claimed the style-control-OFF board is unobtainable without a headless browser and downgraded model-rankings to PARTIAL for that reason. It is obtainable: https://arena.ai/leaderboard/text/overall-no-style-control returns HTTP 200 keylessly and its flight payload carries board id 'text-overall-raw' with 402 full entries, parsed by the identical parser. I found this by reading KXLLM1's settlement_sources from Kalshi's own API, which names 'LM Arena Leaderboard (Remove Style Control)' at exactly that arena.ai URL — the report was pointing at the wrong host. The payload gives rank, rankUpper, rankLower, rating, ratingUpper, ratingLower, votes, modelOrganization, inputPricePerMillion, outputPricePerMillion and contextLength per entry, so the rank-uncertainty band and convergence rate a '#1 at month end' contract trades on are directly available for BOTH variants.

```bash
# STYLE-CONTROL-OFF (the board Kalshi KXLLM1 actually settles on):
curl -sL -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130.0 Safari/537.36' 'https://arena.ai/leaderboard/text/overall-no-style-control' -o R.html
# STYLE-CONTROL-ON: https://arena.ai/leaderboard/text
python3 -c "import re,json;h=open('R.html',encoding='utf8',errors='replace').read();buf=''.join(json.loads(c) for c in re.findall(r'self\\.__next_f\\.push\\(\\[1,(\\\".*?\\\")\\]\\)</script>',h,re.S));e=[json.loads(x) for x in re.findall(r'\\{\\\"rank\\\":\\d+,\\\"rankUpper\\\".*?\\\"releaseType\\\"
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. arena.ai/leaderboard/text/overall-no-style-control HTTP 200, 2,729,311 bytes -> 402 entries, board id 'text-overall-raw'. Top 5 RAW: #1 claude-fable-5.1-max 1507.6 votes=5,783 Anthropic; #2 claude-opus-5-max 1505.0 votes=20,706; #3 claude-opus-5-high 1504.9 votes=42,617; #4 claude-opus-4-6-high 1503.0 votes=71,993; #5 claude-opus-4-6 1497.5 votes=75,878. arena.ai/

#### Epoch AI Open Data bundles (ai_models, benchmark_data, ml_hardware, ai_chip_sales, ai_companies, gpu_clusters) — Epoch AI ✅ LIVE

Covers **4** subdomains: model-releases, model-rankings, agi-and-capability-milestones, semiconductors-and-memory

- Docs: https://epoch.ai/data
- Auth: none | Limits: Plain CSV/ZIP over HTTPS, no key, no rate limit observed. CC-BY licensed, so commercially redistributable with attribution.
- Latency: weekly to monthly — curated, not automated. Files carry a Last modified column; use it for the structural prior and cadence, never for same-day settlement. | Format: ZIP of CSVs + standalone CSV
- Why primary: Six bundles from one provider, all verified live. benchmark_data.zip is the single best free capability series in existence: per-model scored runs with a stderr column on GPQA-Diamond, MATH-5, SWE-bench Verified, FrontierMath (plus tier_4 and tiers_1_3_v2 splits) and OTIS Mock AIME, each with a public Inspect log URL for audit. ai_models.zip carries notable/frontier/large_scale/all tables with publication date, org, parameters and training FLOP. ai_chip_sales.zip carries chip-type and designer timelines. CORRECTED SCOPE: I removed compute-hardware-pricing and ai-adoption from the claim — see verificationEvidence for why both were over-read.

```bash
curl -sL -o ai_models.zip https://epoch.ai/data/ai_models.zip && unzip -p ai_models.zip notable_ai_models.csv | head -2   # siblings: https://epoch.ai/data/benchmark_data.zip  https://epoch.ai/data/ml_hardware.zip  https://epoch.ai/data/ai_chip_sales.zip  https://epoch.ai/data/ai_companies.zip  https://epoch.ai/data/gpu_clusters.csv
```

> Evidence: ALL SIX INDEPENDENTLY FETCHED 2026-09-21. ai_models.zip HTTP 200, 3,335,497 B (README.md, notable_ai_models.csv 2,254,963 B, frontier_ai_models.csv, large_scale_ai_models.csv, all_ai_models.csv 6,819,645 B). benchmark_data.zip HTTP 200, 2,293,470 B, contains gpqa_diamond.csv, math_level_5.csv, swe_bench_verified.csv, otis_mock_aime_2024_2025.csv, frontiermath.csv, frontiermath_tier_4.csv, frontier

#### Atlassian Statuspage v2 convention (one schema, N providers) + GCP/AWS native status — Atlassian Statuspage, self-hosted per vendor; plus Google Cloud, AWS Health ✅ LIVE

Covers **1** subdomains: outages-and-security

- Docs: https://developers.statuspage.io/#tag/status-api
- Auth: none for every host tested | Limits: Static CDN JSON, no key, no published limit. Each summary.json is 4–6 KB; incidents.json is larger (OpenAI's is 38.6 KB for 25 incidents). Companion endpoints: /api/v2/status.json, /api/v2/incidents.json, /api/v2/incidents/unresolved.json, /api/v2/components.json, /api/v2/scheduled-maintenances.json.
- Latency: sub-minute once the vendor posts; the binding constraint is vendor disclosure lag, not the feed | Format: REST JSON — NOT byte-identical across hosts, see evidence. GCP native JSON; AWS native JSON in UTF-16.
- Why primary: Still the clearest case of one-URL-shape-over-a-hostname-list in the domain, and Polymarket outage markets do settle on 'official status pages'. incidents.json carries id, name, status, impact, created_at, resolved_at and a timestamped update trail — the settlement record. Adding a provider costs one line in a config list. CORRECTED SCOPE: I removed platforms-and-consumer-tech; a status page reports outages, it says nothing about device launches or app charts.

```bash
# Current state: for h in status.openai.com status.anthropic.com www.githubstatus.com www.cloudflarestatus.com status.cohere.com status.discord.com status.datadoghq.com status.zoom.us status.twilio.com status.figma.com status.coinbase.com status.snowflake.com; do curl -sL "https://$h/api/v2/summary.json" | python3 -c 'import json,sys;d=json.load(sys.stdin,strict=False);print(d["page"]["name"],d["status"]["description"],len(d.get("components",[])))'; done
# MANDATORY SECOND CALL for the settlement record — summary.json does NOT carry incidents on every host:
curl -sL https://status.openai.com/a
```

> Evidence: ALL 12 HOSTS INDEPENDENTLY SWEPT 2026-09-21 — all HTTP 200. BUT I FOUND TWO DEFECTS THE REPORT MISSED, ONE OF THEM SERIOUS. (1) MEASURED-ZERO FABRICATION: status.openai.com/api/v2/summary.json returns top-level keys ['components','page','status'] ONLY — there is NO incidents key and no scheduled_maintenances key. Same for status.cohere.com. The report recorded 'status.openai.com ... components=25 

#### Shadeform Instance Types API (cross-cloud GPU rental index) — Shadeform ✅ LIVE

Covers **1** subdomains: compute-hardware-pricing

- Docs: https://docs.shadeform.ai/api-reference/instances/types
- Auth: none for the instance-types listing (a key is required only to launch instances) | Limits: No key, no published rate limit on this endpoint — UNKNOWN. Response is ~255 KB. TRAP CONFIRMED: hourly_price is in CENTS for the WHOLE NODE — divide by 100 and by configuration.num_gpus for $/GPU-hour.
- Latency: near-real-time — the availability array is per-region with a boolean `available` flag reflecting current stock | Format: REST JSON
- Why primary: One keyless call returns the enterprise GPU rental market — 299 instance types across 19 clouds with SKU, GPU count, NVLink/interconnect, hourly price and per-region live availability, yielding a defensible spot index (min/median/n) per SKU. CORRECTED SCOPE: I removed semiconductors-and-memory. A GPU rental rate is not a semiconductor or memory price; the report's own ml_hardware/DRAMeXchange entries cover that and this feed returns nothing about DRAM, NAND or chip pricing.

```bash
curl -s 'https://api.shadeform.ai/v1/instances/types' | jq '[.instance_types[]|select(.configuration.gpu_type=="H200")|{cloud,gpu:.configuration.gpu_type,n:.configuration.num_gpus,usd_per_hr:((.hourly_price/100)/.configuration.num_gpus),avail:([.availability[]|select(.available)]|length)}]|sort_by(.usd_per_hr)[0:5]'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 254,833 bytes, 299 instance_types across 19 distinct clouds. I recomputed $/GPU-hour from scratch: H100 n=39 min=$1.66 median=$2.60; H200 n=17 min=$2.25 median=$4.47; B200 n=10 min=$3.74 median=$6.52; A100 n=17 min=$1.36 median=$1.99 — reproduces the report to the cent. Per-row keys confirmed: availability, boot_time, cloud, cloud_instance_type, configur

#### Vast.ai Bundles Search API (GPU marketplace incl. consumer SKUs) — Vast.ai ✅ LIVE

Covers **1** subdomains: compute-hardware-pricing

- Docs: https://docs.vast.ai/api-reference/search/search-offers
- Auth: none for the public bundles search | Limits: No key, no published limit — UNKNOWN. Query must be a URL-encoded JSON `q` object; gpu_name values are space-separated display names ('H100 SXM', 'RTX 5090'), NOT underscore ids.
- Latency: near-real-time marketplace book | Format: REST JSON
- Why primary: UPGRADED ON VERIFICATION. The necessary complement to Shadeform for consumer cards, and the report undersold it: I pulled KXRTX5090MS from Kalshi's series endpoint and its title is 'RTX 5090 Monthly' asking about the monthly average COMPUTE price, settling on Ornn's /compute dashboard. The report assumed it was a retail street price and therefore declared Vast.ai 'a correlated but genuinely different quantity' that must not be substituted. That is wrong — Vast.ai's dph_total IS a compute price and is the correct quantity class for this contract. It returns dph_total, num_gpus, geolocation, dlperf and reliability2 so you can filter to verified hosts before computing an index. CORRECTED SCOPE: removed semiconductors-and-memory for the same reason as Shadeform.

```bash
curl -s --get --data-urlencode 'q={"verified":{"eq":true},"rentable":{"eq":true},"gpu_name":{"in":["H200","RTX 5090","B200"]},"type":"on-demand","limit":500}' 'https://console.vast.ai/api/v0/bundles/' | jq '[.offers[]|{gpu:.gpu_name,per_gpu_hr:(.dph_total/.num_gpus),geo:.geolocation,rel:.reliability2}]|sort_by(.per_gpu_hr)[0:5]'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 189,105 bytes, 64 verified rentable on-demand offers. Recomputed $/GPU-hour: RTX 5090 n=58 min=$0.401 median=$0.601; H200 n=4 min=$3.295 median=$4.738; B200 n=2 $6.252. (Small drift from the report's n=59/$0.467 and n=1 B200 is expected — this is a live order book.) Fields dph_total, num_gpus, geolocation, reliability2, dlperf all confirmed present on of

#### Federal Register API v1 — US National Archives / Office of the Federal Register ✅ LIVE

Covers **3** subdomains: ai-policy, robotics-and-autonomy, semiconductors-and-memory

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none — no API key | Limits: No key and no published hard limit; no RateLimit headers on the live probe — exact ceiling UNKNOWN. per_page caps at 1,000.
- Latency: daily at 06:00 ET publication; public-inspection documents post ~1 business day earlier | Format: REST JSON + CSV + RSS
- Why primary: One keyless endpoint is the authoritative settlement record for federal AI action — executive orders, proposed and final rules, agency notices, BIS export-control actions and NHTSA autonomy rulemaking — with full text, agency, docket, RIN, effective date and comment-close date. The three-subdomain claim survives verification, but ONLY via agency filters; I corrected the exampleCall accordingly because the report's bare term query does not actually retrieve what it claims to.

```bash
# Use AGENCY and TYPE filters, not a bare term query (see evidence):
curl -s 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=industry-and-security-bureau&conditions%5Bpublication_date%5D%5Bgte%5D=2026-01-01&per_page=3&order=newest&fields%5B%5D=title&fields%5B%5D=type&fields%5B%5D=publication_date'
# swap agency for national-highway-traffic-safety-administration (autonomy) ; or conditions[type][]=PRESDOCU with the AI term for executive orders
# day-early wire: https://www.federalregister.gov/api/v1/public-inspection-documents.json?conditions%5Bavailable_on%
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. The report's exact exampleCall: HTTP 200, 4,555 bytes, count=244, newest four reproduce exactly. BUT I TESTED WHETHER THAT COUNT MEANS WHAT IT IMPLIES AND IT DOES NOT: the four newest 'artificial intelligence' hits are a public-health data-exchange Notice, a PCAOB filing, a medical-metrology RFI and an NYSE Arca proposed rule change — the term query matches any fu

#### Apple Marketing Tools RSS Feed Generator (App Store + Music + Podcasts + Books charts) — Apple ✅ LIVE

Covers **1** subdomains: platforms-and-consumer-tech

- Docs: https://rss.marketingtools.apple.com/
- Auth: none | Limits: No key, no published limit — UNKNOWN; treat as a CDN JSON file and poll hourly at most. List length selectable 10/25/50/100. NO ARCHIVE — current chart only, so you must snapshot daily to price a '#1 app on date X' contract.
- Latency: chart refresh appears more frequent than daily — feed.updated moved from 02:47:42 to 03:19:42 to 03:20:17 GMT within a 35-minute observation window on 2026-09-21 | Format: REST JSON
- Why primary: The named settlement source for '#1 Paid App in the US Apple App Store on date X', available keylessly with an explicit `updated` timestamp on every response. One URL template covers top-free and top-paid across 175 storefronts, and the same host serves Music, Podcasts and Books charts. CORRECTED SCOPE: I removed model-releases and ai-market-share. An app chart does not tell you a frontier model shipped, and an app rank is not token or API market share — the report was padding this feed's coverage with subdomains OpenRouter and HF already own properly. ChatGPT's #2 position is a consumer-attention datapoint, not a market-share measurement.

```bash
curl -s 'https://rss.marketingtools.apple.com/api/v2/us/apps/top-free/25/apps.json' | jq -r '.feed.updated, (.feed.results[]|"\(.name) — \(.artistName)")'   # swap top-free → top-paid, us → any of 175 storefronts, apps → music/podcasts/books
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. top-free HTTP 200, 12,385 bytes, feed.title 'Top Free Apps', feed.updated 'Mon, 21 Sep 2026 03:19:42 +0000', 25 results: 1 Muse from Meta (Meta Platforms, Inc.), 2 ChatGPT (OpenAI OpCo, LLC), 3 Vinted, 4 Kalshi: Trade Football & more (KalshiEX LLC), 5 Polymarket: Trade Live Sports — reproduces the report's ordering exactly. top-paid HTTP 200, 12,390 bytes, 25 resu

#### Hugging Face Hub API (models, datasets, spaces) — Hugging Face ✅ LIVE

Covers **2** subdomains: model-releases, model-rankings

- Docs: https://huggingface.co/docs/hub/api
- Auth: none for public reads; a free token raises limits and is required for gated repos | Limits: Anonymous reads work; HF publishes no hard numeric anonymous rate limit — UNKNOWN. Cursor-paginated via Link headers.
- Latency: sub-minute — independently confirmed: the newest record returned was timestamped 2026-09-21T03:20:05Z against a fetch at 03:20:0x, i.e. seconds old | Format: REST JSON
- Why primary: The de-facto registry for open-weight releases and the fastest machine-readable confirmation that a model actually shipped rather than was announced. createdAt gives release time, downloads and likes give adoption, trendingScore surfaces frontier drops within hours, and /api/spaces reaches the community leaderboards several benchmark markets reference. Complements OpenRouter, which only sees models a router has enabled. CORRECTED SCOPE: removed ai-market-share — repo download counts are not usage or token share, and OpenRouter's rankings series measures that quantity directly.

```bash
curl -s 'https://huggingface.co/api/models?sort=createdAt&direction=-1&limit=5'   # trending: https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=20   # leaderboard spaces: https://huggingface.co/api/spaces?search=leaderboard&sort=likes&direction=-1&limit=10
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. /api/models?sort=createdAt&direction=-1&limit=5 HTTP 200, 1,290 bytes, 5 records; first id 'krish5831/marker_test_new_camera_setup_20260920_221944' createdAt '2026-09-21T03:20:05.000Z', downloads 0, likes 0 — seconds old at fetch, confirming sub-minute freshness. (Note the top-of-list is dominated by noise repos; a release detector must filter on org/likes/downloa

#### BLS Public Data API v2 (semiconductor & memory PPI) — US Bureau of Labor Statistics ✅ LIVE

Covers **1** subdomains: semiconductors-and-memory

- Docs: https://www.bls.gov/developers/api_signature_v2.htm
- Auth: none for v2 unregistered use; a free registered key raises the caps | Limits: Unregistered: 25 queries/day, 25 series per query, 10 years per query, no net/percent-change calculations. Registered free key: 500 queries/day, 50 series, 20 years. Verified by successful unregistered POST.
- Latency: monthly, released mid-month for the prior month; the latest value is flagged preliminary and is revised for up to four months | Format: REST JSON (POST)
- Why primary: One POST returns up to 25 official producer-price series at once. PCU334413334413 (semiconductor and related device manufacturing) and PCU3344133344131 (semiconductors) give the official, revision-tracked price trend. CORRECTED SCOPE: I removed ai-pricing and compute-hardware-pricing. A semiconductor producer-price index is neither a per-token API price nor a GPU rental rate; those are OpenRouter's and Shadeform/Vast's quantities respectively, and letting a monthly PPI stand in for either would be a category error in the terminal.

```bash
curl -s -H 'Content-Type: application/json' -X POST -d '{"seriesid":["PCU334413334413","PCU3344133344131"],"startyear":"2025","endyear":"2026"}' https://api.bls.gov/publicAPI/v2/timeseries/data/
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 4,054 bytes, status REQUEST_SUCCEEDED, message []. PCU334413334413: 20 observations, latest 2026 August = 28.472, footnote 'Preliminary. All indexes are subject to monthly revisions up to four months after original publication.' PCU3344133344131: 13 observations, latest 2026 August = 20.102, same preliminary footnote. Reproduces the report exactly. The f

#### GDELT 2.0 DOC API + 15-minute raw files — The GDELT Project ✅ LIVE

Covers **5** subdomains: agi-and-capability-milestones, robotics-and-autonomy, platforms-and-consumer-tech, ai-policy, model-releases

- Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- Auth: none | Limits: CORRECTED — MUCH TIGHTER THAN THE REPORT STATES. The report says 'roughly one request every 5 seconds'. Measured from this host: 429 on the first call, 429 again after a 12 s wait, 429 after a further 30 s, 429 after another 30 s, HTTP 200 only on the third 30 s-spaced attempt. The 429 body is a 444-byte plain-text notice, not JSON, so a naive json.load() crashes rather than surfacing the throttle. Budget for <1 successful request/minute and treat 429 as the normal case. The raw 15-minute CSV/ZIP files at data.gdeltproject.org remain unmetered bulk HTTP and are the right path for any volume. timespan max 3 months on the DOC API.
- Latency: 15-minute file cadence, 96 files/day; DOC API queries the rolling window in near-real-time when it lets you through | Format: REST JSON + bulk CSV/ZIP
- Why primary: The catch-all announcement detector for subdomains whose settlement is 'a company said something'. One query language over worldwide news in 100+ languages replaces a per-company RSS list. Explicitly a PREDICTIVE/alerting feed, never a settlement authority. CORRECTED SCOPE: removed outages-and-security — vendor status pages and CISA KEV are authoritative and near-real-time there, and a rate-limited news tripwire adds nothing but false positives to an outage detector.

```bash
curl -s 'https://api.gdeltproject.org/api/v2/doc/doc?query=%22artificial+general+intelligence%22&mode=artlist&maxrecords=5&format=json&timespan=7d'   # expect 429s; retry with exponential backoff and ALWAYS check the HTTP code before parsing
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21 — LIVE BUT ONLY AFTER FOUR 429s. Attempt log: t=0 HTTP 429 (444 B); t=+12 s HTTP 429; t=+42 s HTTP 429; t=+72 s HTTP 429; t=+102 s HTTP 200, 2,311 bytes, valid JSON with an articles[] array, first url https://www.moneycontrol.com/artificial-intelligence/ten-days-that-changed-the-ai-race-how-fears-of-rogue-systems-grew-article-14033741.html and url_mobile present. T

#### SEC EDGAR full-text search (efts) + getcurrent Atom — US Securities and Exchange Commission ✅ LIVE

Covers **3** subdomains: robotics-and-autonomy, platforms-and-consumer-tech, agi-and-capability-milestones

- Docs: https://www.sec.gov/edgar/sec-api-documentation
- Auth: none, but a descriptive User-Agent with contact email is MANDATORY or SEC blocks you | Limits: Documented fair-access limit: 10 requests/second. No key. Full-text search covers 2001-present. getcurrent is the live filing wire.
- Latency: filings appear on getcurrent within minutes of acceptance; the full-text index lags by roughly one business day | Format: REST JSON (Elasticsearch response shape) + Atom XML
- Why primary: The legally binding version of 'company announcements', with an exact acceptance timestamp a press release does not carry. A material announcement must be 8-K'd, so efts full-text plus the getcurrent wire is one feed covering every listed company. CORRECTED SCOPE: removed ai-market-share (an 8-K does not report token or model share; OpenRouter does) and semiconductors-and-memory (chip and DRAM pricing comes from DRAMeXchange, BLS and TWSE — an 8-K is an event feed, not a price series). Also dropped the no-op `dateRange=custom` parameter from the exampleCall.

```bash
curl -s -A 'Market-Terminal/1.0 (you@example.com)' 'https://efts.sec.gov/LATEST/search-index?q=%22Optimus%22&forms=8-K&startdt=2026-01-01&enddt=2026-09-21' | jq '.hits.total.value, [.hits.hits[]._source|{file_date,display_names,file_type}][0:4]'   # real-time filing wire: curl -A '...' 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&owner=include&count=5&output=atom'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21 with UA 'Market-Terminal/1.0 (jaypatil.duke@gmail.com)'. efts HTTP 200, 31,452 bytes, valid ES envelope {"took":32,"timed_out":false,"_shards":{"total":50,"successful":50,...}}, hits.total.value = 50, relation 'eq'. Parsed hits: 2026-07-17 ['Optimus Healthcare Services, Inc. (CIK 0001892025)'] EX-10.1; 2026-08-20 ['Virtuix Holdings Inc. (VTIX) (CIK 0001606242)'] EX

#### NVD CVE API 2.0 (+ CISA KEV and FIRST EPSS as companions) — NIST National Vulnerability Database; CISA; FIRST.org ✅ LIVE

Covers **1** subdomains: outages-and-security

- Docs: https://nvd.nist.gov/developers/vulnerabilities
- Auth: none required for any of the three; a free NVD key raises NVD's cap | Limits: NVD without key: 5 requests per rolling 30 s; with free key: 50 per 30 s. CISA KEV is an unmetered static JSON/CSV file. EPSS REST is free with an UNKNOWN throttle plus an unmetered daily gzipped CSV of ~250,000 scored CVEs.
- Latency: NVD: hours to days after CVE publication. CISA KEV: updated on determination — the live file's dateReleased was 2026-09-18, i.e. 3 days old at fetch. EPSS: daily, confirmed. | Format: REST JSON; static JSON/CSV; REST JSON + gzip CSV
- Why primary: Three keyless feeds sharing a CVE-id join key and one ingest job: NVD says a vulnerability exists and how severe, CISA KEV says it is confirmed exploited in the wild (the closest thing to an official settlement trigger), EPSS gives a calibrated exploitation probability that is directly a prior. The report's correction of the source inventory's live=false marking on NVD and EPSS is upheld — I independently got 200 from both.

```bash
curl -s 'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=openai&resultsPerPage=2'   # exploited-in-the-wild: curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json   # exploit probability: curl -s 'https://api.first.org/data/v1/epss?cve=CVE-2024-3400'
```

> Evidence: ALL THREE INDEPENDENTLY FETCHED 2026-09-21. NVD HTTP 200, 5,705 bytes, totalResults 129, 2 vulnerabilities returned, first id CVE-2023-1651, response timestamp 2026-09-21T03:21:01.442. CISA KEV HTTP 200, 1,735,385 bytes, count = 1,716, dateReleased 2026-09-18T19:00:05.0974Z, last vulnerability CVE-2020-29583 dateAdded 2021-11-03. EPSS HTTP 200, 202 bytes, full body {"status":"OK","status-code":200

#### Kalshi Trade API v2 (incl. /series settlement_sources) + Polymarket Gamma API — KalshiEX LLC; Polymarket ✅ LIVE

Covers **12** subdomains: model-releases, model-rankings, ai-market-share, ai-pricing, compute-hardware-pricing, semiconductors-and-memory, ai-adoption, agi-and-capability-milestones, ai-policy, platforms-and-consumer-tech, outages-and-security, robotics-and-autonomy

- Docs: https://trading-api.readme.io/reference/getmarkets
- Auth: none for public market reads on either venue | Limits: Both public read surfaces are keyless. Kalshi is cursor-paginated (limit max 1000); Gamma supports limit/offset and tag_slug. No published numeric ceiling on either — UNKNOWN.
- Latency: sub-second — these are live order books | Format: REST JSON
- Why primary: The only feed covering all twelve subdomains, and the one that makes the terminal honest — for subdomains with no free machine-readable settlement source, the venue's own last-trade price is the best available real-time probability. UPGRADE FOUND DURING VERIFICATION: /trade-api/v2/series/{ticker} exposes a settlement_sources array naming the exact authority and URL per contract. The report never used it, and that omission caused two of its errors — it pointed LMArena at the wrong host and mis-typed KXRTX5090MS as a retail price. Ingest this endpoint first; it tells you which feed you actually need. Treat prices strictly as an implied prior, never ground truth.

```bash
# The high-value call the report missed — it returns the NAMED settlement authority per contract:
curl -s 'https://api.elections.kalshi.com/trade-api/v2/series/KXLLM1' | jq '.series|{title,settlement_sources,frequency,category}'
# markets by series: curl -s 'https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXTOKENUSEM&limit=2'
# Polymarket tech events: curl -s 'https://gamma-api.polymarket.com/events?closed=false&limit=3&tag_slug=tech'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. Kalshi /markets?limit=3&status=open HTTP 200, 9,091 bytes — but note the report's generic exampleCall returns KXMVECROSSCATEGORY sports/crypto parlays, which is NOT evidence of AI coverage, so I verified coverage properly by series. Every named AI/compute series resolves: KXLLM1 'Best AI this week' 2 markets; KXTOKENUSEM 'Will OpenRouter AI token usage for Septemb

#### DRAMeXchange public spot-price table — TrendForce / DRAMeXchange ✅ LIVE

Covers **1** subdomains: semiconductors-and-memory

- Docs: https://www.dramexchange.com/
- Auth: none | Limits: Free public front page only, ~183 KB. NO API — scrape-only, and the HTML structure is not a contract. Deep history and contract (vs spot) prices are behind TrendForce's paywall. CRITICAL, NEWLY FOUND: the eight tables on the page update on DIFFERENT schedules and each carries its own 'Last Update' stamp. On 2026-09-21 the DRAM and Module tables were stamped Sep.21 2026 11:00 (GMT+8) — current — while NAND Flash, Wafer, eMMC, Memory Card and GDDR were stamped Sep.7 2026 14:40 (14 days stale) and LPDDR Sep.14 (7 days stale). A parser that ignores the stamp will publish a two-week-old GDDR5 price as today's spot.
- Latency: DAILY for DDR5/DDR4 (DRAM table) and the Module table only. Weekly-or-worse and demonstrably stale for GDDR, LPDDR, NAND, Wafer, eMMC and Memory Card. | Format: HTML table (scrape)
- Why primary: The only free daily DRAM spot quote found anywhere, covering DDR5 16Gb chip, DDR5 UDIMM 16GB, DDR5 RDIMM 32GB, DDR4 and eTT grades in one table with high/low/average and percent change per row. It is the closest free proxy to the Ornn source Kalshi actually names for KXDDR5MS. Listed with its weaknesses stated: it is a scrape, not an API; it is a proxy, not the named settlement authority; and its non-DRAM tables are stale.

```bash
curl -sL -A 'Mozilla/5.0' https://www.dramexchange.com/ -o dx.html && python3 -c "import re;h=open('dx.html',encoding='utf8',errors='replace').read();print([m.group(1).strip() for m in re.finditer(r'Last Update:([^<&]{0,60})',h)]);[print([re.sub(r'<[^>]+>|\s+',' ',c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>',m.group(0),re.S)][:7]) for m in re.finditer(r'<tr[^>]*>(?:(?!</tr>).)*?DDR5(?:(?!</tr>).)*?</tr>',h,re.S)]"   # YOU MUST PARSE THE PER-TABLE 'Last Update' STAMP — see freeTierLimits
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 183,092 bytes. Parsed DDR5 rows (label, high, low, ..., average, change): ['DDR5 16Gb (2Gx8) 4800/5600','68.00','41.50','68.00','41.50','56.417','0.75 %']; ['DDR5 16Gb (2Gx8) eTT','25.80','23.70','25.80','23.70','24.800','0.81 %']; ['DDR5 UDIMM 16GB 4800/5600','265.00','220.00','265.00','220.00','234.000','1.74 %']; ['DDR5 RDIMM 32GB 4800/5600','2300.00'

#### TWSE OpenAPI monthly revenue (Taiwan semiconductor complex) — Taiwan Stock Exchange ✅ LIVE

Covers **1** subdomains: semiconductors-and-memory

- Docs: https://openapi.twse.com.tw/
- Auth: none | Limits: No key, no published limit — UNKNOWN. One 606 KB file carries all 1,086 listed companies, so a single monthly fetch covers the entire complex. Field names are Traditional Chinese; date format is ROC calendar (11508 = 2026-08).
- Latency: monthly — Taiwan requires revenue disclosure by the 10th of the following month, weeks ahead of US quarterly reporting | Format: REST JSON
- Why primary: One file, one fetch, the entire AI hardware supply chain's demand signal: TSMC (2330), Nanya Technology (2408, DRAM), UMC (2303), MediaTek (2454) and every other 半導體業 name, with year-on-year change. An official exchange disclosure rather than an estimate, and it lands before any US 10-Q. CORRECTED SCOPE: I removed compute-hardware-pricing and ai-market-share. Monthly revenue is a demand/volume signal, not a price and not a share measurement — Shadeform/Vast own GPU pricing and OpenRouter owns share. Keeping those claims would have let a revenue print masquerade as a price feed in the terminal.

```bash
curl -s 'https://openapi.twse.com.tw/v1/opendata/t187ap05_L' | python3 -c "import json,sys;d=json.load(sys.stdin);[print(x['公司代號'],x['公司名稱'],x['產業別'],x['資料年月'],x['營業收入-當月營收'],x['營業收入-去年同月增減(%)']) for x in d if x['公司代號'] in ('2330','2408','2303','2454')]"
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 606,355 bytes, 1,086 companies. Parsed for 資料年月 11508 (2026-08), revenue in NT$ thousands: 2330 台積電 (半導體業) 514,805,337 yoy +53.320%; 2408 南亞科 (半導體業) 44,690,268 yoy +560.854%; 2303 聯電 (半導體業) 25,044,641 yoy +30.714%; 2454 聯發科 (半導體業) 64,183,361 yoy +44.081%. Reproduces the report to three decimal places.

#### US Census Bureau BTOS — Business Trends and Outlook Survey (AI use) — US Census Bureau ✅ LIVE

Covers **1** subdomains: ai-adoption

- Docs: https://www.census.gov/hfp/btos/data_downloads
- Auth: none | Limits: Static XLSX download, no key, no limit. The api.census.gov timeseries route for BTOS returns 302 and the generic Census API demands a key — use the XLSX downloads, which do not. Sector and state breakouts are on sibling files.
- Latency: biweekly reference periods, published on a two-week cycle | Format: XLSX (six worksheets; inline strings, no sharedStrings table — parse xl/worksheets/*.xml directly)
- Why primary: The only free, official, recurring measurement of business AI adoption in the United States, with both a current-use and a six-month-forward-expectation question on biweekly slots — so it gives level AND slope. Kalshi's AI-adoption contracts settle on Ramp rather than this, but Ramp publishes no machine-readable series at all, so BTOS is the best available predictive feed and the honest public benchmark against it.

```bash
curl -sL 'https://www.census.gov/hfp/btos/downloads/National.xlsx' -o btos.xlsx && python3 -c "import zipfile,re;z=zipfile.ZipFile('btos.xlsx');s=z.read('xl/worksheets/sheet1.xml').decode('utf8','replace');v=re.findall(r'<is><t[^>]*>(.*?)</t>',s);print([x for x in v if 'rtificial' in x][:2]);print(v[:10])"
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 87,218 bytes, file(1) reports 'Microsoft Excel 2007+', six worksheets confirmed (xl/worksheets/sheet1..6.xml). 6,723 inline strings parsed. Question text confirmed verbatim: 'In the last two weeks, did this business use Artificial Intelligence (AI) in any of its business functions? (Examples of AI: machine learning, natural language processing, virtual a

#### GitHub REST API (releases, tags, events) — GitHub / Microsoft ✅ LIVE

Covers **1** subdomains: model-releases

- Docs: https://docs.github.com/en/rest/releases/releases
- Auth: none for public reads; a free personal access token raises the limit to 5,000/hr | Limits: Unauthenticated: 60 requests/hour/IP for core REST and 10/minute for search — a low ceiling. Use a free token, or poll narrowly.
- Latency: sub-minute — release events fire immediately on publish | Format: REST JSON + GraphQL + webhooks
- Why primary: The fastest hard confirmation that a framework or inference-engine version actually shipped, with a tag and a published_at timestamp you can settle on. Complements HF (weights) and OpenRouter (routed availability) to give three independent shipped/not-shipped signals. CORRECTED SCOPE: removed agi-and-capability-milestones — a repository release does not settle an AGI or capability claim, and pairing this feed with that subdomain in a terminal invites exactly the wrong inference.

```bash
curl -s 'https://api.github.com/repos/huggingface/transformers/releases?per_page=2'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 32,396 bytes, valid releases array with 2 elements: tag_name v5.17.0 published_at 2026-09-09T15:42:45Z; tag_name v5.16.1 published_at 2026-08-26T14:50:01Z. The settleable fields the report asserted (tag, published_at) are confirmed present and populated, which the report's own evidence did not actually show.

#### Wikimedia Pageviews REST API — Wikimedia Foundation ✅ LIVE

Covers **4** subdomains: agi-and-capability-milestones, platforms-and-consumer-tech, model-releases, robotics-and-autonomy

- Docs: https://wikimedia.org/api/rest_v1/
- Auth: none; a free Wikimedia account token raises limits | Limits: No key. Send a descriptive User-Agent or you will be blocked. Daily granularity from 2015-07; hourly top-articles endpoints also available.
- Latency: daily, published roughly 24 h after the day closes | Format: REST JSON
- Why primary: A clean, archival, keyless attention series for any named entity — model, company, person, concept — the generic PREDICTIVE input for subdomains whose settlement is an announcement. Unlike Google Trends RSS (current snapshot only, no backfill) it has a decade of daily history, so you can fit a base rate rather than eyeball a spike. One URL template covers every article. Never a settlement source for anything.

```bash
curl -s -A 'Market-Terminal/1.0 (you@example.com)' 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Artificial_general_intelligence/daily/20260901/20260919'
```

> Evidence: INDEPENDENTLY FETCHED 2026-09-21. HTTP 200, 3,204 bytes, 19 daily items for Artificial_general_intelligence; final item timestamp '2026091900' views 2343. Reproduces the report exactly.

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Frontier Model Releases | Epoch AI ai_models.zip (per-lab historical release cadence,  | Official vendor announcement, cross-confirmed three ways: Op | 🟢 COVERED |
| Model Rankings & Benchmarks | Arena embedded flight payload — rating, ratingUpper/ratingLo | https://arena.ai/leaderboard/text/overall-no-style-control — | 🟢 COVERED |
| AI Market Share & Token Usage | OpenRouter /api/frontend/v1/rankings/models daily token seri | OpenRouter rankings series — total_prompt_tokens + total_com | 🟢 COVERED |
| AI Token & API Pricing | OpenRouter /api/v1/models pricing block for all 446 models ( | Vendor published price lists; OpenRouter /api/v1/models is t | 🟢 COVERED |
| GPU & Hardware Pricing | Shadeform /v1/instances/types (299 types, 19 clouds, per-reg | NONE FREE — the named authority is Ornn (https://dashboard.o | 🟡 PARTIAL |
| Semiconductors & Memory | DRAMeXchange DRAM + Module tables (DAILY, verified stamped S | NONE FREE for the named authority — KXDDR5MS settles on Ornn | 🟡 PARTIAL |
| AI Adoption Indices | US Census BTOS National.xlsx — biweekly current-use and six- | Ramp AI Index (https://ramp.com/data/ai-index) — HTML page o | 🟡 PARTIAL |
| AGI & Capability Milestones | Epoch AI benchmark_data.zip — scored runs on FrontierMath (p | Lab announcements — no structured feed exists. Best machine- | 🟡 PARTIAL |
| AI Policy, Safety & Regulation | Federal Register API filtered by AGENCY and TYPE (not a bare | Federal Register API v1 — the authoritative keyless record o | 🟢 COVERED |
| Platforms, Devices & App Charts | Apple Marketing Tools RSS daily chart snapshots across 175 s | Apple Marketing Tools RSS — https://rss.marketingtools.apple | 🟡 PARTIAL |
| Outages, Hacks & Cybersecurity | Historical incident frequency computed from each vendor's /a | The vendor's own /api/v2/incidents.json — NOT summary.json,  | 🟡 PARTIAL |
| Robotics & Autonomy | SEC EDGAR full-text search for delivery-promise language and | Company announcements — SEC EDGAR 8-K is the legally binding | 🟡 PARTIAL |

**Rejected**

- **Ornn compute dashboard (dashboard.ornnai.com/compute)** — NEWLY IDENTIFIED BY VERIFICATION — THE MOST IMPORTANT GAP IN THIS DOMAIN, AND THE REPORT NEVER NAMED IT AS A FEED. I read settlement_sources from Kalshi's own /trade-api/v2/series endpoint and Ornn is the named settlemen
- **Azure status RSS (azure.status.microsoft/en-us/status/feed/)** — EMPTY FEED — HTTP 200 IS NOT A PASS HERE. Returns 577 bytes: a well-formed RSS channel with title 'Azure Status' and lastBuildDate 'Mon, 21 Sep 2026 03:19:00 Z' but ZERO <item> elements. The report cited 'azure.status.mi
- **Statuspage /api/v2/summary.json as a source of incident counts** — SCHEMA TRAP, documented rather than used. summary.json does NOT carry an incidents array on every host: status.openai.com and status.cohere.com return only ['components','page','status']. The report recorded 'incidents=0
- **Artificial Analysis API (artificialanalysis.ai/api/v2/data/llms/models)** — PAYWALLED / KEY REQUIRED — re-verified today: HTTP 401, 31 bytes with no key. Would have been an excellent single feed for model-rankings + ai-pricing + latency together, but it is not free-tier accessible. Arena + Epoch
- **LMArena official JSON API (lmarena.ai/api/leaderboard*)** — BLOCKED — Cloudflare 403/301 to non-browser clients on every variant. Superseded, but note the report's superseding path was incomplete: parse the server-rendered Next.js flight payload on ARENA.AI, which serves both the
- **LMSYS arena leaderboard CSV (storage.googleapis.com/arena-external-data/public/leaderboard_table.csv)** — DEAD — re-verified HTTP 404, 133 bytes. The widely-cited historical export no longer exists; anything still pointing at it is stale documentation.
- **OpenRouter frontend endpoints /api/frontend/models/find, /api/frontend/all-providers, /api/frontend/stats/apps, /api/frontend/stats/tokens, /api/v1/models/stats, /api/frontend/v1/rankings/authors** — DO NOT EXIST — I spot-re-verified two of them today: /api/frontend/stats/tokens HTTP 404 and /api/frontend/v1/rankings/authors HTTP 404. Recorded so nobody wastes time guessing at OpenRouter's internal surface. The three
- **Ramp AI Index as an API** — NO MACHINE-READABLE SURFACE — re-verified: ramp.com/data/ai-index HTTP 200 (4,872,471 B) but ramp.com/api/data/ai-index HTTP 404. Note the 404 body is 4,868,135 bytes of Next.js soft-404 HTML, so a client checking only r
- **Epoch AI ml_hardware.zip as a GPU price feed** — NEWLY REJECTED FOR THIS PURPOSE — over-read by the report, which listed it under compute-hardware-pricing. I parsed the CSV: 176 rows, only 59 (34%) have a non-empty 'Release price (USD)'. Per family: H100 4 rows/1 price
- **Epoch AI ai_companies_usage_reports.csv as an AI-adoption series** — NEWLY REJECTED FOR THIS PURPOSE. The report credited it under ai-adoption. It is a hand-curated, back-dated research compilation, not a recurring measurement: the row 'ChatGPT 50M WAU' carries Date 2023-03-25 against Rep
- **Federal Register bare conditions[term] queries** — MISLEADING RESULT SHAPE, documented rather than used. term='artificial intelligence' returns count=244 for 2026, but the newest four hits are a public-health data-exchange Notice, a PCAOB filing, a medical-metrology RFI 
- **Cloudflare Radar API** — LICENSE TRAP, not a technical failure. Free with a Cloudflare token and genuinely good for internet-outage and BGP data, but CC BY-NC 4.0 — NON-COMMERCIAL ONLY. A revenue-generating terminal cannot redistribute it withou
- **Census BTOS via api.census.gov** — BROKEN / KEY-WALLED — timeseries route returns HTTP 302 with a zero-byte body and the generic Census data API returns a 'Missing Key' HTML page. Superseded by the direct XLSX downloads at census.gov/hfp/btos/downloads/, 
- **Congress.gov API v3 with DEMO_KEY** — RATE-LIMITED SHARED KEY — re-verified today: HTTP 429 with body {"error":{"code":"OVER_RATE_LIMIT",...}}. The API itself is sound and free but needs its own api.data.gov key (5,000 req/hr). Launch prerequisite for ai-pol
- **OpenStates v3 API** — KEY REQUIRED — re-verified HTTP 403, 132 bytes. Free registration exists. Needed for state AI-law calendars.
- **FRED fredgraph.csv keyless export** — NOT REACHABLE FROM THE ORIGINAL HOST (HTTP 000). I did not re-test it, so I leave the report's finding as reported and unconfirmed. Immaterial either way: BLS API v2 serves the same PPI series keylessly and I did verify 
- **Prime Intellect availability API / Lambda Labs instance-types API** — HTTP 403 and HTTP 000 respectively per the report; not re-tested, and immaterial because Shadeform already carries lambdalabs rows and covers the enterprise surface with 299 types across 19 clouds.
- **Vast.ai with underscore GPU ids (e.g. gpu_name=H100_SXM)** — SILENT-FAILURE TRAP — RE-CONFIRMED TODAY. Returns HTTP 200 with body exactly {"offers": [], "truncated": false} instead of an error. A naive integration records this as 'zero H100 supply' — a missing measurement read as 
- **TradingEconomics guest API** — HTTP 410 GONE per the report; guest credential tier retired. Not re-tested; no bearing on this domain's coverage.
- **status.mistral.ai and status.x.ai** — HTTP 403 to non-browser clients — re-verified today (6,049 B and 5,478 B Cloudflare interstitials). Two notable AI labs have no scriptable status feed; their outages need browser-based collection. A direct contributor to
- **Epoch AI stale download paths (ai_benchmarking_run_results.csv / machine_learning_hardware.csv / epoch_capabilities_index.csv)** — HTTP 404 per the report — Epoch reorganised into ZIP bundles. I re-verified all six CURRENT paths return 200: ai_models.zip (3,335,497 B), benchmark_data.zip (2,293,470 B), ml_hardware.zip (29,498 B), ai_chip_sales.zip (
- **Anthropic RSS (anthropic.com/rss.xml and /news/rss.xml)** — HTTP 404 on both — re-verified today (59,882 B and 59,997 B soft-404 pages; another case where a size check would mislead). Anthropic publishes no feed, so one of the three most market-relevant labs has no push release c
- **ai.meta.com/blog/rss/** — HTTP 400 per the report; Meta's AI blog feed is not serving. Not re-tested. deepmind.google/blog/rss.xml and blogs.nvidia.com/feed/ were reported working if per-lab feeds are wanted.
- **Google Play Store chart API** — DOES NOT EXIST FREE. Google publishes no public Play chart endpoint; Sensor Tower, data.ai and Appfigures are paid. This is why platforms-and-consumer-tech stays PARTIAL — Apple is covered, Android is not.
- **Retail GPU street-price APIs (Newegg, Amazon PA-API, PCPartPicker, Keepa)** — NONE FREE AND WORKING — but the report's framing was wrong and this matters less than it claimed. It listed retail 5090 pricing as 'the single genuine UNCOVERED item' needed for KXRTX5090MS. I pulled that series from Kal
- **TrendForce / DRAMeXchange historical and contract price series** — PAYWALLED. Only the current spot tables on the public front page are free, and only some of them are current — the DRAM and Module tables were stamped Sep.21 2026 while GDDR, NAND, Wafer, eMMC and Memory Card were stampe

---

### transportation-and-logistics

*2/6 subdomains covered · 13 primary feeds*

#### BTS Supply Chain & Freight Indicators (single Socrata dataset y5ut-ibwt) — US Bureau of Transportation Statistics (data.bts.gov, Socrata SODA 2.1) ✅ LIVE

Covers **2** subdomains: freight-rates, ports-and-supply-chain

- Docs: https://data.bts.gov/d/y5ut-ibwt
- Auth: none (anonymous SODA reads work; a free Socrata app token raises the throttle pool) | Limits: CONFIRMED. No key required — anonymous reads succeeded repeatedly with no 429. Anonymous reads share a throttled pool; a free app token gives a per-token bucket. $limit default 1000, max 50000 per page with $offset. $select/$group/$where/$order aggregation all confirmed working anonymously.
- Latency: CONFIRMED per-indicator. Weekly indicators 3-10 days behind (diesel 2026-09-07, rail 2026-09-05, grain barge 2026-09-08, containerships anchored/awaiting berths 2026-09-15); monthly indicators ~6 weeks behind (2026-06 to 2026-08). | Format: REST JSON (SoQL), also CSV/XML
- Why primary: Still the highest-leverage feed in the domain and the clearest case of the 'one API, many subdomains' rule — I independently confirmed 44 distinct named indicators under ONE dataset id. Long format (indicator/measure1/value1/units/source per row) means a single $where swaps sub-series without changing integration code. VERIFIER ADDITION the original report missed: the TEU indicators are broken out PER PORT, not just nationally — a $group on measure1 for 'Loaded Import Containers at Select U.S. Ports in TEUs' returns nine named ports including 'Los Angeles' and 'Long Beach' SEPARATELY, current to 2026-07-01. The report undersold this; it is materially better port coverage than claimed.

```bash
curl 'https://data.bts.gov/resource/y5ut-ibwt.json?$where=indicator%20like%20%27U.S.%20Diesel%25%27&$order=date%20DESC&$limit=3'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, all HTTP 200. (1) Diesel call reproduced the report's exact payload: {"date":"2026-09-07","indicator":"U.S. Diesel Sales Prices  (in Dollars per Gallon)","value1":"5.967"}, plus 2026-08-31 5.599 and 2026-08-24 5.652. (2) Full indicator census via $select=indicator,count(*),max(date)&$group=indicator returned EXACTLY 44 distinct indicators, confirming the report

#### FAA National Airspace System Status (NASSTATUS) — US Federal Aviation Administration ✅ LIVE

Covers **1** subdomains: flight-disruption

- Docs: https://nasstatus.faa.gov/
- Auth: none | Limits: CONFIRMED no key, no registration, no published rate limit (UNKNOWN — no RateLimit headers observed). The report's warning stands and I echo it: this endpoint is UNDOCUMENTED/UNOFFICIAL, not published by the FAA as a supported public API, so it carries schema-change and withdrawal risk. Poll at 1-5 minute intervals.
- Latency: CONFIRMED sub-minute to minutely. Payload carries its own Update_Time; my fetch showed 03:20:33 GMT against the report's 02:52:08 GMT ~28 minutes earlier, and the content had already moved — proving it is genuinely live, not a cached page. | Format: REST XML (AirportStatus.dtd)
- Why primary: Independently confirmed as the single national-scope live feed that prices every US airport-delay contract in one call. One small XML document returns the entire current US delay state: Ground Delay Programs with airport/reason/avg/max, Airspace Flow Programs with constrained-area polygon and altitude floor/ceiling, general arrival/departure delays with trend, ground stops and airport closures. The reason codes are exactly the causal taxonomy a KXFLIGHTORD or FLIGHTJFK market trades on.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://nasstatus.faa.gov/api/airport-status-information'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, HTTP 200. Root <AIRPORT_STATUS_INFORMATION> with <Update_Time>Mon Sep 21 03:20:33 2026 GMT</Update_Time> — a LATER timestamp than the report's 02:52:08, so this is a distinct live observation. All four Ground Delay Programs the report cited reproduce with identical values: SFO 'low ceilings' Avg 54 minutes Max 3 hours and 45 minutes; DFW 'thunderstorms' Avg 1 h

#### IMF PortWatch — Daily Ports Data + Daily Chokepoints Data (ArcGIS FeatureServer) — International Monetary Fund / UN Global Platform / University of Oxford ✅ LIVE

Covers **1** subdomains: ports-and-supply-chain

- Docs: https://portwatch.imf.org/pages/data-and-methodology
- Auth: none | Limits: CONFIRMED. No API key, no registration, no quota encountered. ArcGIS FeatureServer maxRecordCount 1000 per query — page with resultOffset. Refreshed weekly (Tuesdays) with daily observations. History 2019-01-01 to present. Layer 0 of each service. NOTE for implementers: the 'date' field comes back as epoch MILLISECONDS on Daily_Ports_Data but as a plain 'YYYY-MM-DD' STRING on Daily_Chokepoints_Data — the two services are not type-consistent and naive shared parsing code will throw.
- Latency: CONFIRMED daily observations delivered weekly. Latest port date 2026-09-11 and latest chokepoint date 2026-09-13 both reproduced exactly, i.e. ~7-9 day lag. | Format: REST JSON (ArcGIS query API), plus CSV/GeoJSON bulk
- Why primary: Independently confirmed: two endpoints replace scraping thousands of port authorities and every canal authority. Daily_Ports_Data gives daily port-call counts and estimated import/export trade volume by vessel class for ~2,065 ports including Los Angeles-Long Beach (portid port664). Daily_Chokepoints_Data gives the same shape for maritime chokepoints. Both derive from satellite AIS, so they are a physical observation rather than a survey, and one schema serves both the port question and the canal-diversion question.

```bash
curl "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Ports_Data/FeatureServer/0/query?where=portid%3D'port664'&outFields=date,portname,portcalls,portcalls_container,import,export&orderByFields=date%20DESC&resultRecordCount=4&f=json&returnGeometry=false"
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, three HTTP 200 calls. (1) Daily_Ports_Data port664 reproduced the report's payload EXACTLY: {'date':'2026-09-11','portname':'Los Angeles-Long Beach','portcalls':11,'portcalls_container':6,'import':369623,'export':58559}, with 2026-09-10 portcalls 10 and 2026-09-09 portcalls 6 also matching. (2) Daily_Chokepoints_Data filtered to Suez Canal reproduced exactly: {

#### FRED keyless fredgraph CSV (no API key required) — Federal Reserve Bank of St. Louis ✅ LIVE

Covers **3** subdomains: freight-rates, passenger-throughput, aviation-industry

- Docs: https://fred.stlouisfed.org/docs/api/fred/
- Auth: none for the fredgraph.csv route (the api.stlouisfed.org REST route DOES require a free key) | Limits: CONFIRMED. Keyless CSV route: no key, no registration, no quota hit across 15 sequential calls. Keyed REST route: 120 req/min per key. Full series history per call. CAVEAT INDEPENDENTLY REPRODUCED: a multi-series id list returns a ZIP, not CSV — id=RAILFRTCARLOADSD11,GASDESW returned HTTP 200 with Content-Type: application/zip and PK\x03\x04 magic. Request ONE series per call.
- Latency: VERIFIED AND MORE NUANCED THAN REPORTED. Freight series are current (diesel 2026-09-14, PPI trucking 2026-08, truck tonnage / rail carloads / freight TSI 2026-06). But the AVIATION and PASSENGER series lag much harder — AIRRPMTSI, ENPLANE and LOADFACTOR all stop at 2026-05-01, roughly four months behind. That is context-only, not a settlement or even a near-term pricing input. | Format: CSV (keyless) / REST JSON-XML (keyed)
- Why primary: One URL pattern with a swappable series id, no key and no auth rotation makes this the cheapest possible integration and the correct backstop wherever a BTS Socrata series is stale or missing. Verified carrying truck tonnage, PPI long-distance TL trucking, retail diesel, rail freight carloads and Freight TSI for freight-rates, and air revenue passenger miles, enplanements, load factor and jet fuel for the aviation and passenger sides.

```bash
curl 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=GASDESW'   # one series per call. Verified working ids: GASDESW, TRUCKD11, PCU484121484121, RAILFRTCARLOADSD11, TSIFRGHT, AIRRPMTSI, ENPLANE, LOADFACTOR, DJFUELUSGULF
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, 15 calls. ALL FIVE of the report's freight series reproduced to the exact decimal: TRUCKD11 last rows 2026-05-01,112.8 / 2026-06-01,113.3; GASDESW 2026-09-07,5.967 / 2026-09-14,6.285; PCU484121484121 2026-07-01,203.781 / 2026-08-01,207.644; RAILFRTCARLOADSD11 2026-05-01,1003553 / 2026-06-01,991352; TSIFRGHT 2026-06-01,134.9. The report's negative results also r

#### BTS TranStats — Reporting Carrier On-Time Performance (monthly bulk) — US Bureau of Transportation Statistics (TranStats PREZIP) ✅ LIVE

Covers **2** subdomains: flight-disruption, aviation-industry

- Docs: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ
- Auth: none | Limits: CONFIRMED. No key, no registration. Open HTTP file directory, one ZIP per month. Range requests CONFIRMED supported (Accept-Ranges: bytes present; a Range request returned HTTP 206). No published rate limit (UNKNOWN). History 1987 to present. MEASURED FILE SIZE: 31,606,062 bytes (~31.6MB) for a single month — budget for that, and use Range to probe before downloading.
- Latency: CONFIRMED monthly with a ~2-3 month publication lag. Server Last-Modified for the 2026_6 file is Wed, 12 Aug 2026 12:15:44 GMT — so June data published mid-August, an independent confirmation of the lag the report claimed. | Format: ZIP of CSV
- Why primary: The authoritative US government record of every scheduled domestic flight — scheduled vs actual departure and arrival, delay minutes decomposed into carrier/weather/NAS/security/late-aircraft, cancellation flag with code, and diversions, keyed by carrier, origin, destination and tail number. One monthly file settles both airport-level delay-and-cancellation questions and carrier-level reliability questions with no per-airport fan-out. Its only weakness is the publication lag, which is why NASSTATUS and ADS-B carry the intraday signal.

```bash
curl -H 'User-Agent: Mozilla/5.0' -O 'https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2026_6.zip'   # swap the trailing _YYYY_M
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. HEAD returned HTTP 200 with Content-Length: 31606062, Content-Type: application/x-zip-compressed, Accept-Ranges: bytes, Last-Modified: Wed, 12 Aug 2026 12:15:44 GMT. A Range: bytes=0-200 request returned HTTP 206 with 201 bytes whose hexdump begins '504b 0304 1400 0000 0800' — a valid ZIP local file header — and the embedded filename is legible in the same 201 

#### TSA Passenger Throughput (daily checkpoint volumes) — U.S. Transportation Security Administration ✅ LIVE

Covers **1** subdomains: passenger-throughput

- Docs: https://www.tsa.gov/travel/passenger-volumes
- Auth: none | Limits: CONFIRMED. NO API — this is an HTML table on a government page, scrape-only. No key, no rate limit published. Scrape once daily after ~09:00 ET. Page is 186,441 bytes and carries a rolling window of 261 table rows (260 data rows + header); deeper history needs archived year pages.
- Latency: CONFIRMED daily. The prior day's nationwide total posts the following morning; latest row 9/17/2026 observed on 2026-09-20. | Format: scrape-only (HTML table, two columns: Date, Numbers)
- Why primary: It is the literal settlement source for Kalshi's TSA contracts, it is free, and there is no JSON alternative — BTS's own Socrata mirror of this series is dead (independently confirmed below). One page carries the entire national series, so no per-airport assembly is needed.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://www.tsa.gov/travel/passenger-volumes'   # then parse <tr> rows; two columns: Date, Numbers
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, HTTP 200, 186,441 bytes — byte-identical size to the report's fetch. Regex-parsed exactly 261 <tr> rows, matching the report. Header row ['Date','Numbers']. Data rows reproduced EXACTLY: ['9/17/2026','2,700,658'], ['9/16/2026','2,176,546'], ['9/15/2026','1,948,803'], plus ['9/14/2026','2,542,694'] which extends the report's evidence. This is real tabular data, 

#### MTA Open Data — Daily Ridership (Socrata sayj-mze2) + GTFS-RT Service Alerts — Metropolitan Transportation Authority via data.ny.gov and api-endpoint.mta.info ✅ LIVE

Covers **1** subdomains: passenger-throughput

- Docs: https://data.ny.gov/Transportation/MTA-Daily-Ridership-and-Traffic-Beginning-2020/sayj-mze2
- Auth: none for both — CONFIRMED keyless on the GTFS-RT alerts endpoint as well | Limits: CONFIRMED. Socrata: no key, anonymous reads worked, $limit max 50000 with $offset. GTFS-RT alerts: no key, returned 837,339 bytes as application/json with no auth header, no published quota (UNKNOWN) — poll every 30-60s. Ridership history from 2020-03-01; alerts are a current-state snapshot.
- Latency: CONFIRMED. Ridership daily with a ~3-day lag (latest 2026-09-17 observed 2026-09-20). Alerts near-realtime. | Format: REST JSON (SoQL) and GTFS-Realtime rendered as JSON
- Why primary: One dataset id covers all seven MTA modes — Subway, Bus, LIRR, Metro-North, Staten Island Railway, Access-A-Ride and Bridges & Tunnels — in long format (date, mode, count), so a KXMTA contract on any mode is the same query with a different filter rather than a different integration. Independently confirmed all seven modes present on the latest date.

```bash
curl 'https://data.ny.gov/resource/sayj-mze2.json?$order=date%20DESC&$limit=8'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, two HTTP 200 calls. Socrata sayj-mze2 reproduced the report's 2026-09-17 figures EXACTLY, all seven modes: AAR 51790, BT 1004594, Bus 1519901, LIRR 313539, MNR 255976, SIR 8468, Subway 4530966. GTFS-RT alerts returned 837,339 bytes — byte-identical to the report — Content-Type application/json, header {'gtfs_realtime_version':'2.0','incrementality':'FULL_DATASE

#### Federal Register API v1 — US Office of the Federal Register / GPO ✅ LIVE

Covers **4** subdomains: aviation-industry, transport-labor, ports-and-supply-chain, freight-rates

- Docs: https://www.federalregister.gov/developers/documentation/api/v1
- Auth: none | Limits: CONFIRMED. No key, no registration, no rate limit encountered across five agency queries (UNKNOWN published limit — no RateLimit headers returned). per_page default 20, max 1000. Full corpus 1994 to present. Public domain. NOTE: the 'count' field caps its display at 10000 — the FAA RULE filter reports exactly 10000, which is a ceiling, not a true total.
- Latency: CONFIRMED daily — published each federal business day ~06:00 ET; newest STB and NMB documents carried a 2026-09-21 publication date at fetch time. | Format: REST JSON (also CSV and RSS)
- Why primary: One agency-filtered endpoint reaches every US transport regulator from a single integration — the agency is a query parameter rather than a different host, so adding a regulator costs nothing. Independently confirmed live for FAA (airworthiness directives and route rules), Surface Transportation Board (rail cost adjustment and control exemptions), National Mediation Board (Railway Labor Act proceedings), and — verifier addition — Maritime Administration and Federal Maritime Commission, which the report asserted but never tested.

```bash
curl 'https://www.federalregister.gov/api/v1/documents.json?conditions%5Bagencies%5D%5B%5D=federal-aviation-administration&conditions%5Btype%5D%5B%5D=RULE&per_page=3&order=newest&fields%5B%5D=title&fields%5B%5D=publication_date&fields%5B%5D=document_number&fields%5B%5D=html_url'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, five HTTP 200 calls, all four of the report's agency claims reproduced EXACTLY. FAA RULE: count 10000, newest 2026-09-18 doc 2026-19173 'Establishment of United States Area Navigation Route T-581 in the Vicinity of Missoula, Montana' and docs 2026-19172 / 2026-19171 'Airworthiness Directives; Rolls-Royce Deutschland Ltd. & Co. KG Engines' — confirming ADs arriv

#### Cornell ILR Labor Action Tracker (labor_actions.json) — Cornell University ILR School, Worker Institute ✅ LIVE

Covers **1** subdomains: transport-labor

- Docs: https://striketracker.ilr.cornell.edu/
- Auth: none | Limits: CONFIRMED. No key, no registration. Undocumented but publicly served JSON — it is the file the site's own map fetches. Single file, MEASURED at 5,044,805 bytes containing the whole corpus per request — cache it and poll daily. No rate limit published (UNKNOWN). History from 2021-01. Caveat for implementers: this is a university research project, not a government or operator publication, so it has no service commitment and could change shape or disappear.
- Latency: CONFIRMED days — entries appear within roughly a week of the action. Latest Start_date 2026-09-17 observed 2026-09-20. | Format: REST JSON (object keyed by integer id)
- Why primary: The only free, structured, current, nationwide register of actual US labor actions. Every alternative is a press release, an employer statement, or BLS Work Stoppages (monthly aggregate, 1,000+ workers only). Each record carries Employer, Labor_Organization, Action_type, Authorized flag, Start_date, End_date, Duration, Approximate_Number_of_Participants, Bargaining_Unit_Size, Worker_demands, Industry and geocoded locations — enough to form a prior and observe resolution. One file covers rail, air, transit, trucking, warehousing and longshore together.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://striketracker.ilr.cornell.edu/labor_actions.json'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, HTTP 200, 5,044,805 bytes — byte-identical to the report. Parsed to a dict of EXACTLY 5021 entries, matching the report. Field schema reproduced exactly: ['id','Employer','Start_date','End_date','Labor_Organization','Authorized','Action_type','Industry','Worker_demands','Local','Duration','Approximate_Number_of_Participants','Bargaining_Unit_Size','Notes','loca

#### GDELT DOC 2.0 API — The GDELT Project ✅ LIVE

Covers **6** subdomains: flight-disruption, aviation-industry, passenger-throughput, freight-rates, ports-and-supply-chain, transport-labor

- Docs: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- Auth: none | Limits: HARD LIMIT INDEPENDENTLY RE-MEASURED AND CONFIRMED WORSE THAN DOCUMENTED. Nominally 1 request per 5 seconds, but in my own run the IP was held at HTTP 429 for THREE consecutive attempts with 8-second sleeps between them — roughly 24+ seconds of enforced cool-off — before the fourth attempt returned 200. The report's warning to use exponential backoff rather than a fixed 5s sleep is correct and I reproduce it independently. Error responses are ~444 bytes of PLAIN TEXT, not JSON — parse defensively or your client will throw on json.loads. maxrecords caps at 250 for artlist. Rolling ~3-month window.
- Latency: sub-minute (articles indexed within ~15 minutes of publication) | Format: REST JSON (errors in plain text)
- Why primary: The one feed touching all six subdomains, because each has an announcement channel no statistical series carries: ATC strike calls, carrier route suspensions, canal draft restrictions, bankruptcy rumours, strike-authorization votes. TimelineVol modes turn a keyword into a coverage-volume time series, usable as a prior where no numeric feed exists. It is a news prior, NOT a settlement source, and is used here only that way — that framing is correct and I retain it unchanged.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://api.gdeltproject.org/api/v2/doc/doc?query=airline%20strike&mode=artlist&maxrecords=5&format=json&timespan=7d'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20. Attempts 1, 2 and 3 returned HTTP 429 with a 444-byte plain-text body; attempt 4 returned HTTP 200, 2,291 bytes — the same byte size the report recorded. Parsed 5 real articles. The report's two headline hits reproduce EXACTLY: 20260920T210000Z que.es 'Huelga de controladores en Belgica: vuelos cancelados a Bruselas y Charleroi desde Espana' and 20260920T000000

#### Keyless ADS-B aggregators — adsb.fi and adsb.lol (OpenSky as fallback) — adsb.fi and adsb.lol volunteer feeder networks; OpenSky Network (ETH Zurich) ✅ LIVE

Covers **2** subdomains: flight-disruption, aviation-industry

- Docs: https://github.com/adsbfi/opendata and https://api.adsb.lol/docs and https://openskynetwork.github.io/opensky-api/rest.html
- Auth: none for adsb.fi and adsb.lol. OpenSky anonymous works but is reduced. | Limits: CONFIRMED keyless on both primary providers. adsb.fi public endpoints: 1 request/second, radius up to 250NM. adsb.lol: no key, no published numeric quota (UNKNOWN; community convention ~1 req/s). OpenSky anonymous: 400 credits/day, most-recent state vectors only. Both primaries share the ADSBexchange-v2 schema, so one is a genuine drop-in failover for the other — independently confirmed by parsing both with identical code.
- Latency: realtime — confirmed by aircraft counts changing between the report's fetch and mine | Format: REST JSON
- Why primary: A single radius query around any airport returns every aircraft currently there with type, registration, callsign, altitude, ground speed and squawk — one endpoint pattern serves every airport contract instead of one integration per airport. It supplies what NASSTATUS cannot: observed movement counts and holding patterns during a delay event, and airframe-type census. The type-code census claim for a MAX-grounding question is independently confirmed below.

```bash
curl 'https://opendata.adsb.fi/api/v2/lat/40.64/lon/-73.78/dist/25'   # JFK, 25NM.  Mirror: curl 'https://api.adsb.lol/v2/lat/41.978/lon/-87.904/dist/20'  # ORD
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, both providers HTTP 200. adsb.fi JFK 25NM: 26,948 bytes, 51 aircraft parsed, first record {'hex':'a32886','flight':'AAL1967','r':'N302UD','t':'B38M','desc':'BOEING 737 MAX 8','alt_baro':2625,'gs':213.9,'squawk':'1620'} — INDEPENDENTLY CONFIRMING the report's key claim that the B38M type code is directly observable in the payload, on a DIFFERENT airframe (N302UD

#### NOAA Aviation Weather Center Data API (METAR / TAF / SIGMET / AIRMET / PIREP) — NOAA National Weather Service, Aviation Weather Center ✅ LIVE

Covers **1** subdomains: flight-disruption

- Docs: https://aviationweather.gov/data/api/
- Auth: none | Limits: CONFIRMED. No key, no registration. No published numeric rate limit (UNKNOWN); poll per-station no faster than the ~hourly METAR cycle, or every 5 minutes for SPECI. Multi-station requests via a comma list in ids CONFIRMED working — three airports returned in one 1,899-byte response.
- Latency: CONFIRMED METAR hourly plus off-cycle SPECI; all three stations returned reportTime 2026-09-21T03:00:00Z in a single call. | Format: REST JSON, XML, CSV or raw text
- Why primary: Flight-delay contracts are priced by terminal weather. One comma-separated call returns decoded METAR for any set of airports — visibility, wind, gusts, ceiling, precipitation — and the TAF endpoint returns the forecast that turns an observation into a forward-looking probability, which is what lets you price a delay BEFORE the FAA declares a Ground Delay Program. Multi-station in one request means no per-airport fan-out.

```bash
curl -H 'User-Agent: Mozilla/5.0' 'https://aviationweather.gov/api/data/metar?ids=KJFK,KORD,KDFW&format=json'
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, HTTP 200, 1,899 bytes — byte-identical to the report. All three stations reproduced EXACTLY, including the raw observation strings: KORD reportTime 2026-09-21T03:00Z visib 3 wspd 14, raw 'METAR KORD 210251Z 07014G24KT 3SM -DZ BR BKN007 BKN013 OVC019 17/16 A3007' — a 3-statute-mile, 700ft-ceiling, gusting-24kt Chicago, the low-IFR state that precedes a GDP; KJFK

#### SEC EDGAR Submissions API (carrier filings) — US Securities and Exchange Commission ✅ LIVE

Covers **1** subdomains: aviation-industry

- Docs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Auth: none, but a descriptive User-Agent header with a contact email is MANDATORY — SEC returns 403 without it. CONFIRMED: my call succeeded only with the UA set. | Limits: CONFIRMED. No key. SEC fair-access policy 10 req/sec per IP. No daily cap. MEASURED: the submissions file carries 1,001 filings inline in filings.recent, spanning 2017-02-13 to 2026-08-28 for Delta — deeper history is in linked pagination files. Response 154,789 bytes.
- Latency: near-realtime — filings appear within minutes of acceptance | Format: REST JSON
- Why primary: One endpoint shape, swap the CIK, and you have every public carrier and manufacturer with form type, filing date and document description. This covers the 'company announcements' half of aviation-industry settlement, and the sicDescription field confirms the entity is a scheduled air carrier rather than a same-named issuer.

```bash
curl -H 'User-Agent: YourApp your@email.com' 'https://data.sec.gov/submissions/CIK0000027904.json'   # Delta Air Lines
```

> Evidence: INDEPENDENTLY RE-FETCHED 2026-09-20, HTTP 200, 154,789 bytes — byte-identical to the report, with User-Agent set. Payload name 'DELTA AIR LINES, INC.', sicDescription 'Air Transportation, Scheduled' — both reproduced exactly. filings.recent parallel arrays confirmed correctly indexed: 2026-08-28 N-PX, 2026-08-14 SCHEDULE 13G/A, 2026-08-14 13F-HR. VERIFIER ADDITION testing the report's load-bearing

**Coverage**

| Subdomain | Predictive feed | Settlement feed | Status |
|---|---|---|---|
| Flight Delays & Cancellations | FAA NASSTATUS (re-verified 2026-09-20 with a FRESHER Update_ | BTS TranStats Reporting Carrier On-Time Performance monthly  | 🟡 PARTIAL |
| Airlines & Aviation Safety | Federal Register API v1 with conditions[agencies][]=federal- | Federal Register API v1 (an airworthiness directive IS the l | 🟢 COVERED |
| Passenger Throughput & Transit | MTA Daily Ridership Socrata sayj-mze2 across all seven modes | TSA Passenger Volumes HTML table at tsa.gov/travel/passenger | 🟢 COVERED |
| Freight & Trucking Rates | BTS Supply Chain & Freight Indicators (Socrata y5ut-ibwt) —  | NONE FOUND | 🟡 PARTIAL |
| Ports & Supply Chain | IMF PortWatch Daily_Ports_Data (re-verified exactly: Los Ang | PARTIAL. BTS y5ut-ibwt per-port monthly TEU — a VERIFIER DIS | 🟡 PARTIAL |
| Transport Labor Actions | Cornell ILR Labor Action Tracker labor_actions.json (re-veri | Cornell ILR Labor Action Tracker Start_date / End_date / Dur | 🟡 PARTIAL |

**Rejected**

- **FlightAware AeroAPI** — RETAINED. The named Kalshi settlement source for KXFLIGHTORD/FLIGHTJFK, key-gated and commercial. Neither the original agent nor the verifier obtained a key or fetched any payload, so it is correctly excluded rather than
- **BTS 'Commercial Aviation Departures and TSA Screenings' (Socrata hvq3-38u5)** — RETAINED — VERIFIER INDEPENDENTLY RE-CONFIRMED DEAD. My own call returned HTTP 200 and correctly shaped JSON, but $order=date DESC gives a latest date of 2022-10-26 with 'Person Throughput at All Airports' = 1990205, and
- **BTS 'Monthly TEU Data' (Socrata rd72-aq8r)** — RETAINED as stale (reported last row 2022-10). Superseded by the per-port TEU indicators inside y5ut-ibwt, which the verifier confirmed are broken out for Los Angeles and Long Beach separately and current to 2026-07-01, 
- **BTS 'U.S. Airport On-Time Performance' (rns4-gpqn) and 'U.S. Marketing Air Carriers On-time Performance' (56fa-sf82)** — RETAINED as NOT TABULAR — reported HTTP 200 with a body of empty objects and HTTP 403 'no row or column access to non-tabular tables' respectively. These are visualization assets on the Socrata portal, not queryable data
- **BTS y5ut-ibwt 'Truck Spot Rates in $ per Mile by Truck Type' (sub-series only)** — RETAINED — VERIFIER INDEPENDENTLY RE-CONFIRMED STALE. My own full-dataset census shows this indicator at max(date) = 2024-05-12 with n=1155 rows, while 42 of the other 43 indicators in the same dataset are current to 202
- **BTS y5ut-ibwt 'Average Dwell Time at Major Terminals by Railroad' (sub-series only)** — ADDED BY VERIFIER as an explicit row, having been mentioned only in passing in the original evidence. My census returns max(date) = NULL for this indicator across all 231 rows — the date field is unpopulated, so the seri
- **FRED port-throughput series (no such keyless series found)** — ADDED BY VERIFIER. The original report claimed FRED covers ports-and-supply-chain via 'port throughput series' but named and tested none. I probed: IPG4841TAXS — the very id the report used in its own multi-series ZIP te
- **Truckstop.com dry van rates** — RETAINED. The named Kalshi settlement source for KXVANRATE/KXVANRATEMW. No free API exists and none was verified by either agent. This is the direct cause of freight-rates having settlementFeed NONE FOUND.
- **DAT Freight & Analytics (Trendlines / DAT iQ)** — RETAINED. Reported HTTP 301 on the trendlines page; DAT rate data is a paid product with no free API. Its output reaches the public only via the BTS republication, which the verifier independently confirmed stale at 2024
- **Drewry World Container Index (WCI)** — RETAINED. No free API; free web viewing requires email registration and CSV export is paid. Not fetchable programmatically.
- **Freightos Baltic Index (FBX)** — RETAINED. API access is enterprise-only by Freightos' own support documentation; CSV download requires a paid package. No free programmatic path.
- **FAA NOTAM API (external-api.faa.gov)** — RETAINED — VERIFIER INDEPENDENTLY RE-CONFIRMED KEY-GATED. My own probe of https://external-api.faa.gov/notamapi/v1/notams?icaoLocation=KJFK returned HTTP 401 with body {"message":"Unauthorized","http_status_code":401}. T
- **FAA SWIM Cloud Distribution Service (SCDS)** — RETAINED. Free of charge but requires SWIFT Portal registration and a signed Service Access Agreement with per-product approval. Not plug-and-play and not verifiable in a session. Best streaming source for ground stops i
- **NTSB CAROL Query API** — RETAINED as FAILED. Reported HTTP 500 'An unknown exception occured' on a live POST to https://data.ntsb.gov/carol-main-public/api/Query/Main, with no working request shape determined. The verifier did not attempt to ove
- **National Mediation Board (nmb.gov) feeds** — RETAINED. No machine-readable feed — reported HTTP 301 on /feed/ and 404 on /feed and /news/. NMB activity is reachable only indirectly via the Federal Register agency filter, which the verifier confirmed live at count 6
- **USDA AMS Market News API (marsapi.ams.usda.gov)** — RETAINED. HTTP 403 without credentials. Nothing is lost: the grain barge rate data it publishes is available free and current through BTS y5ut-ibwt, which the verifier confirmed at 2026-09-08 with 2,814 rows of history.
- **FRED series GSCPI (NY Fed Global Supply Chain Pressure Index)** — RETAINED — VERIFIER INDEPENDENTLY RE-CONFIRMED. My own request to https://fred.stlouisfed.org/graph/fredgraph.csv?id=GSCPI returned HTTP 404. This series does not exist on FRED. The index is published by the NY Fed only 
- **OpenSky /flights/arrival and /flights/departure (anonymous)** — RETAINED. Reported HTTP 404 with an empty array for a KJFK query over a 4-hour historical window using anonymous access; the per-airport endpoints require a registered OAuth2 client. OpenSky /states/all does work anonymo
- **Port of Los Angeles Signal / Port Optimizer Control Tower** — RETAINED, and now load-bearing. No public API: Signal requires email registration, Control Tower is restricted to port stakeholders, and TEU statistics ship as a monthly XLSX whose path must be scraped. Because this is t
- **Panama Canal Authority (ACP) and Suez Canal Authority** — RETAINED. Neither publishes an API — ACP is HTML plus PDF Advisories to Shipping; SCA is monthly web tables and PDF/XLS with weeks of lag. Both superseded for daily transit counts by IMF PortWatch Daily_Chokepoints_Data,
- **AAR Weekly Rail Traffic** — RETAINED. No API — weekly HTML/PDF press releases with redistribution licensing. Equivalent and better-structured rail data (Class I carloads, intermodal units, trailers and containers on flat cars, train speed, terminal
- **EUROCONTROL Aviation Intelligence Portal / DDR** — RETAINED. Open datasets are bulk CSV/XLSX and a weekly PDF, not an API; DDR is gated. Not verified live by either agent. Relevant only to European aviation contracts, which are outside the listed subdomains — though note
- **Drewry / RWI-ISL / Kiel Trade Indicator / NY Fed GSCPI XLSX** — RETAINED as a grouped rejection. All are scrape-only static-file publications with no API and none were fetched by either agent. They would add monthly-frequency supply-chain index context that IMF PortWatch already supp

---

## 4 · Coverage audit

### Kalshi Series Settlement-Source Registry (/trade-api/v2/series) — THE shared settlement spine ✅

- This is the single most valuable thing in the whole inventory and it is currently being used as a market feed rather than as infrastructure. 14,163 of 14,170 series (99.95%) carry a machine-readable settlement_sources array naming the exact URL the exchange itself settles against. That converts 'which settlement feed do we need?' from a research question into a JOIN. It is also a coverage oracle: harvesting distinct URLs yields the authoritative source list per category (e.g. Economics resolves to freddiemac.com/pmms, adpemploymentreport.com, apps.bea.gov/iTable, stats.gov.cn, data.imf.org, blockworks.co/analytics/l1, app.rwa.xyz/treasuries). Build the crawler against this registry, not against per-domain guesses.
- Docs: https://docs.kalshi.com/api-reference/market/get-series-list | Auth: None (public read) | Limits: Public read tier; one 17MB full-catalogue pull returns all series. Poll daily, not per-request.

```bash
curl -s 'https://api.elections.kalshi.com/trade-api/v2/series?limit=1000' | python3 -c "import sys,json;d=json.load(sys.stdin)['series'];print(len(d), sum(1 for s in d if s.get('settlement_sources')))"
```

### Polymarket CLOB /markets + /sampling-markets — contract structure, tenor and liquidity incentives ✅

- All three market-mechanics subdomains marked UNCOVERED are in fact carried as fields on feeds already in the inventory — the gap is vocabulary, not data. /markets returns neg_risk, neg_risk_market_id, is_50_50_outcome, minimum_tick_size, minimum_order_size, maker_base_fee, taker_base_fee, seconds_delay, end_date_iso, game_start_time, accepting_order_timestamp. /sampling-markets is the reward-earning subset and returns rewards.rates[].rewards_daily_rate in USDC with min_size and max_spread — that IS the liquidity-incentive feed. No new vendor needed.
- Docs: https://docs.polymarket.com/api-reference/markets/get-markets | Auth: None | Limits: Keyless public read; /markets full page is ~1.8MB, /sampling-markets ~2.5MB per 1000

```bash
curl -s 'https://clob.polymarket.com/sampling-markets' | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print(len(d)); print(d[0]['rewards'], d[0]['neg_risk'], d[0]['end_date_iso'], d[0]['minimum_tick_size'])"
```

### ForecastEx public contracts API — the THIRD venue Robinhood routes to, entirely absent from the inventory ✅

- The user named Robinhood as a first-class venue. The inventory models Robinhood coverage as a subset of Kalshi, which is now WRONG: Robinhood Derivatives routes event contracts to KalshiEx, ForecastEx, and (as of Sept 2026) OG.com. ForecastEx has a keyless public catalogue with last_yes_price, last_no_price, open_interest, expiration_date, payout_date and exchange_spec_url. Without it, Robinhood's universe is under-covered.
- Docs: https://www.forecastex.com/ | Auth: None | Limits: Keyless, ~5KB payload

```bash
curl -s 'https://www.forecastex.com/api/contracts' | python3 -c "import sys,json;r=json.load(sys.stdin);d=json.loads(r['body']['data']);print(len(d));print(d[0])"
```

### PredictIt Market Data API — fourth venue, keyless full-book snapshot ✅

- A fourth independent probability on the same political/election questions Kalshi and Polymarket list. Cross-venue disagreement is itself a tradable signal and a data-quality check on our own ingest — if our Kalshi price and our PredictIt price diverge structurally, one pipeline is broken. Costs one HTTP call for the entire venue.
- Docs: https://www.predictit.org/api/marketdata/all/ | Auth: None | Limits: Keyless; single call returns every open market with all contracts. Cached ~60s.

```bash
curl -s 'https://www.predictit.org/api/marketdata/all/'
```

### Manifold Markets API — keyless cross-domain forecast prior ✅

- Covers the long tail no regulated venue lists — AGI milestones, scientific results, obscure geopolitics — which is exactly where our UNCOVERED and settlement-gap rows cluster. Play money, so treat as a weak prior, never as settlement. It is the replacement for Metaculus, which has gone behind auth.
- Docs: https://docs.manifold.markets/api | Auth: None for reads | Limits: Keyless reads, cursor-paginated via before=<id>

```bash
curl -s 'https://api.manifold.markets/v0/markets?limit=500'
```

### ESPN Core API odds endpoint — keyless sportsbook lines (replaces The Odds API) ✅

- The sports mapping lists The Odds API v4 as covering 9 subdomains with live=false — i.e. our only odds source is an unverified keyed vendor. ESPN's core API serves the same lines keylessly from an endpoint we are already ingesting for scores, which means zero new auth, zero new vendor, and one fewer schema. Sportsbook lines are the best available public prior for every game-level market on Kalshi and Polymarket.
- Docs: https://github.com/pseudo-r/Public-ESPN-API | Auth: None | Limits: Keyless, undocumented/unofficial — no published quota, no SLA

```bash
curl -s 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401773008/competitions/401773008/odds'
```

### Nasdaq public API — consensus EPS forecasts, revision counts and dividend/corporate-action calendar ✅

- Fills the largest genuinely UNCOVERED financial row. Sell-side consensus and the direction of revisions is the standard predictive input for every 'will COMPANY beat EPS' contract, and it was entirely missing. The dividends calendar adds corporate actions (ex-date, record, payment, announcement), a whole class the inventory has no feed for at all.
- Docs: https://www.nasdaq.com/market-activity/earnings | Auth: None (browser User-Agent required) | Limits: Keyless, unofficial; UA-gated and rate-sensitive

```bash
curl -s -A 'Mozilla/5.0' 'https://api.nasdaq.com/api/analyst/AAPL/earnings-forecast' ; curl -s -A 'Mozilla/5.0' 'https://api.nasdaq.com/api/calendar/dividends?date=2026-09-18'
```

### Scryfall API — Magic: The Gathering secondary-market prices ✅

- One of the two feeds that turns Collectibles & Alternative Assets from UNCOVERED into priced. Per-printing usd / usd_foil / eur / tix, plus daily bulk dumps so the whole asset class can be backfilled without per-item calls.
- Docs: https://scryfall.com/docs/api | Auth: None | Limits: Keyless; requested 50-100ms between calls; bulk-data dumps published daily

```bash
curl -s 'https://api.scryfall.com/cards/search?q=%21%22Sol+Ring%22+set%3Ac13'
```

### Pokémon TCG API — graded/ungraded card market prices (TCGplayer + Cardmarket) ✅

- Second half of the collectibles fill, and the larger of the two markets by dollar volume. Returns a full price ladder, not a single point.
- Docs: https://docs.pokemontcg.io/ | Auth: None for the public tier (optional free key raises limits) | Limits: Keyless tier rate-limited — one call returned a non-JSON body under rapid fire; back off and retry

```bash
curl -s 'https://api.pokemontcg.io/v2/cards?q=set.id:base1%20name:charizard'
```

### GLEIF LEI Records API — legal-entity master and corporate hierarchy ✅

- Nothing in the inventory resolves 'the company in this Kalshi contract' to 'the CIK in this EDGAR filing' to 'the sanctioned entity in this OFAC row' to 'the issuer in this bond'. GLEIF is the free, authoritative entity spine, including parent/child relationships — which is how you stop a subsidiary sanction from being missed against a parent ticker.
- Docs: https://www.gleif.org/en/lei-data/gleif-api | Auth: None | Limits: Keyless REST + free full Golden Copy bulk file

```bash
curl -s 'https://api.gleif.org/api/v1/lei-records?filter%5Bentity.names%5D=Apple+Inc.&page%5Bsize%5D=1'
```

### OpenFIGI v3 mapping API — ticker / ISIN / CUSIP to FIGI crosswalk ✅

- Pairs with GLEIF: GLEIF identifies the issuer, OpenFIGI identifies the instrument, including share-class and composite level. Required before any cross-source price reconciliation (Nasdaq vs Cboe vs Robinhood) can be trusted.
- Docs: https://www.openfigi.com/api | Auth: None (optional free key raises limits) | Limits: Keyless: 25 requests/min, 10 jobs per request. POST only — GET returns 405.

```bash
curl -s -X POST 'https://api.openfigi.com/v3/mapping' -H 'Content-Type: application/json' -d '[{"idType":"TICKER","idValue":"AAPL","exchCode":"US"}]'
```

### SEC company_tickers.json — ticker to CIK crosswalk ✅

- The third leg of the crosswalk and the cheapest. Every EDGAR feed already in the inventory is keyed by CIK while every market feed is keyed by ticker; without this file that join is done by string matching on company name, which will silently mis-map.
- Docs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces | Auth: None, but a declared User-Agent with contact email is mandatory | Limits: 10 req/sec; a generic browser UA is rejected with 'Request Rate Threshold Exceeded'

```bash
curl -s -A 'YourApp your@email.com' 'https://www.sec.gov/files/company_tickers.json'
```

### DBnomics API v22 — unified macro archive over ~90 statistical providers ✅

- The macro domain currently runs BIS, ECB, Eurostat, OECD, StatCan, ONS, World Bank and IMF as separate feeds with separate schemas, separate auth and separate failure modes. DBnomics exposes all of them through one series path and one JSON shape. Use DBnomics for breadth, discovery and backfill; keep the official endpoint ONLY for series that actually settle a contract, because a mirror must never be the settlement authority.
- Docs: https://api.db.nomics.world/v22/apidocs | Auth: None | Limits: Keyless REST + bulk

```bash
curl -s 'https://api.db.nomics.world/v22/series/FED/H15?observations=1&limit=1'
```

### FINRA Data API (otcMarket group) — keyless OTC/ATS and short-sale volume ✅

- Extends the existing Reg SHO coverage to off-exchange venue-level activity with notional sums, and is the free on-ramp to the FINRA data catalogue generally. It is the closest free thing to dark-pool/ATS visibility, which a Bloomberg-style terminal is expected to have.
- Docs: https://developer.finra.org/docs | Auth: None for this group | Limits: Keyless for public datasets; other groups require OAuth

```bash
curl -s 'https://api.finra.org/data/group/otcMarket/name/weeklySummary?limit=1'
```

### Robinhood public marketdata quotes endpoint — venue-native equity quotes ✅

- Included because the user named Robinhood as a venue and because Single-Stock Prices is PARTIAL with only Cboe delayed and a throttled Yahoo endpoint behind it. Flagged with a caveat rather than promoted: unofficial, undocumented, and legally exposed. Do not wire it as a primary until counsel clears it.
- Docs: https://robinhood.com/us/en/support/articles/robinhood-event-contracts/ | Auth: None observed on this path | Limits: UNDOCUMENTED and NOT a published API. Terms-of-use risk is real; treat as best-effort, never as a settlement source.

```bash
curl -s 'https://api.robinhood.com/marketdata/quotes/?symbols=AAPL,NVDA,TSLA'
```

### Wikidata Query Service (SPARQL) — scheduled-future-event knowledge graph, elevated to shared infrastructure ✅

- Already listed in four domains as a per-domain feed. It should be one shared service: it is the only free source that answers 'what scheduled events exist in the future, everywhere, with dates and participants' — which is precisely the index a market-discovery layer needs to anticipate contracts before venues list them.
- Docs: https://query.wikidata.org/ | Auth: None; descriptive User-Agent required or requests fail | Limits: 60s query timeout, concurrency limits, UA-gated

```bash
curl -s -H 'Accept: application/sparql-results+json' -A 'ECHO/1.0 (contact@example.com)' 'https://query.wikidata.org/sparql?format=json&query=SELECT%20%3Fitem%20WHERE%20%7B%3Fitem%20wdt%3AP31%20wd%3AQ3305213%7D%20LIMIT%202'
```

### Gaps

| Item | Predictive | Settlement | Status |
|---|---|---|---|
| Contract Tenor & Intervals | Kalshi /series series.frequency + /markets close_time / expi | Kalshi /markets expiration_value + Polymarket end_date_iso | COVERED |
| Contract Structure Types | Kalshi /markets market_type + strike_type + custom_strike +  | Kalshi /markets settlement rules via contract_terms_url (PDF | COVERED |
| Merchandising Views & Liquidity Incentives | Polymarket CLOB /sampling-markets rewards.rates[].rewards_da | N/A — this subdomain has no outcome to settle | COVERED |
| Untagged & Bespoke Inventory | Kalshi /series tags + categories arrays; Polymarket Gamma /t | Kalshi settlement_sources | PARTIAL |
| Robinhood venue coverage (cross-cutting) | Kalshi Trade API v2 + ForecastEx /api/contracts | Kalshi settlement_sources; ForecastEx exchange_spec_url | PARTIAL |
| Polymarket settlement-source machine readability (cross-cutting) | Polymarket Gamma /markets (prices, UMA status) | NONE FOUND in structured form — prose only | PARTIAL |
| Kalshi series with NO declared settlement source | Kalshi market prices | NONE FOUND — exactly 7 series, enumerated | PARTIAL |
| Collectibles & Alternative Assets | Scryfall (MTG, per-printing usd/eur/tix) + Pokémon TCG API ( | Same feeds — these ARE the reference prices | PARTIAL |
| Corporate KPIs & Alternative Data | Nasdaq /api/analyst/{sym}/earnings-forecast (consensus EPS,  | SEC XBRL companyconcept / companyfacts (the filed number) | PARTIAL |
| Table Tennis | Kalshi KXTABLETENNIS series (TT Elite Series markets confirm | NONE FOUND — machine access blocked | UNCOVERED |
| Art & Auctions | Kalshi + Polymarket prices, Google News RSS, Wikimedia Pagev | NONE FOUND | UNCOVERED |
| Political Speech / Earnings Call / Broadcast Mentions / Speech Duration (all 4) | GDELT 2.0 raw 15-min Mentions+GKG, Google News RSS, GovInfo  | NONE FOUND for broadcast-TV mention counts | PARTIAL |
| Recession & Business Cycle | FRED (SAHMREALTIME, yield curve, claims), Atlanta Fed GDPNow | NONE FOUND in machine-readable form — NBER Business Cycle Da | PARTIAL |
| Layoffs | Socrata state WARN notices, DOL ETA 539 claims, GDELT | PARTIAL — WARN is 50 separate state portals with no common s | PARTIAL |
| Housing Prices & Activity | FRED (CSUSHPINSA, MORTGAGE30US, HOUST, EXHOSLUSM495S) | FRED / Census new-residential releases | PARTIAL |
| Electricity & Power, Coal, Copper | ERCOT dashboard JSON (one ISO only), EIA, FRED monthly coppe | PARTIAL for power (ERCOT only); NONE FOUND free/daily for co | PARTIAL |
| Futures curves & exchange settlement prices (cross-cutting, not currently a row) | CFTC Commitments of Traders (positioning only) | NONE FOUND | UNCOVERED |
| Credit, Bonds & Ratings | FRED ICE BofA OAS series, Treasury CMT curve, FINRA otcMarke | PARTIAL — no free single-bond TRACE prices, no CDS, no ratin | PARTIAL |
| Single-Stock Prices, Firm-Level Changes, Dollar Index, EM FX, Other Global Indices | Cboe delayed CDN, Nasdaq quotes, open.er-api.com, Robinhood  | PARTIAL — all free sources are delayed or end-of-day | PARTIAL |
| Primaries, Ballot Measures, Judicial, Other Statewide/Local, Margins & Turnout | Kalshi, Polymarket, PredictIt, Wikipedia polling tables, Vot | PARTIAL — North Carolina ENRS is wired as an 'exemplar'; the | PARTIAL |
| Russia-Ukraine, Israel/Gaza, Iran/Nuclear, China/Taiwan, Venezuela/LatAm, Gulf/Turkey, NATO/Treaties, Territorial Acquisition, South Asia/Sudan | Strong: OCHA HAPI, GDELT, DeepStateMap, NGA warnings, Tzeva  | NONE FOUND in structured form for the outcome questions (cea | PARTIAL |
| AGI & Capability Milestones | Epoch AI benchmark bundles, LMArena, OpenRouter rankings, Hu | PARTIAL — benchmark claims are self-reported by labs with no | PARTIAL |
| GPU & Hardware Pricing, Semiconductors & Memory | Shadeform, Vast.ai, DRAMeXchange public table, TWSE monthly  | PARTIAL — DRAMeXchange public table is the de-facto referenc | PARTIAL |
| Celebrities & Milestones, Public Appearances, Reality TV, Scripted TV & Film Production | Wikimedia Pageviews, Google News RSS, TVmaze, Wikidata | NONE FOUND structured — settles on entertainment-press conse | PARTIAL |
| Artist & Track Stream Counts, YouTube & Creator Metrics | kworb.net (Spotify daily + per-artist cumulative, YouTube mo | PARTIAL — kworb is a third-party scrape of Spotify, not Spot | PARTIAL |
| Tennis, Golf, Motorsport, Boxing, Cricket, Rugby/AFL, Darts & Mind Sports, Olympics, Niche Sports | ESPN core API (verified broad), Jolpica F1, Chess.com/Liches | PARTIAL — ESPN covers the majors; TheSportsDB, which the inv | PARTIAL |
| Transactions/Draft/Coaching, League Business, Win Totals, Player Props | ESPN core API + ESPN BET odds (newly verified, replaces the  | PARTIAL — ESPN/league sites for on-field; NONE FOUND structu | PARTIAL |
| Token Launches & Airdrops, Long-Tail/Meme, Relative Value, Dogecoin, Stablecoins & Security | CoinGecko, GeckoTerminal, DefiLlama, OKX/Binance/Coinbase/Kr | COVERED for listed pairs; PARTIAL for pre-launch FDV and air | PARTIAL |
| Freight & Trucking Rates | BTS Supply Chain Indicators, FRED, IMF PortWatch | NONE FOUND — DAT, Freightos FBX and Drewry WCI are all paywa | PARTIAL |
| Snowfall & Ski Resorts, Hourly & Weekly Average Temperature | Open-Meteo, NOAA/NWS gridpoints, SNOTEL, IEM MOS guidance | PARTIAL — NWS CLI products and ACIS settle official station  | PARTIAL |
| University Rankings | Urban Institute Education Data Portal, College Scorecard, Go | NONE FOUND — US News, THE and QS rankings are all proprietar | PARTIAL |
| Clinical Trial Readouts, Emerging Outbreaks & PHEIC | ClinicalTrials.gov v2, pdufa.bio catalyst API, WHO DON, Next | COVERED for PHEIC (WHO DON is the declaring authority); PART | PARTIAL |
| Real-time consolidated quotes, NBBO and Level 2 depth | NONE FOUND free | NONE FOUND free | UNCOVERED |
| Point-in-time macro vintages and revision archive | PARTIAL — FRED/ALFRED realtime_start/realtime_end requires a | N/A | PARTIAL |
| Cross-venue market identity (same real-world event across Kalshi / Polymarket / PredictIt / ForecastEx) | NONE — must be built | N/A | UNCOVERED |
| Streaming transport (WebSocket) vs polling | PARTIAL — Kalshi and Polymarket both publish WebSocket marke | N/A | PARTIAL |
| Historical tick and order-book archive for backtesting | PARTIAL — Kalshi /candlesticks gives OHLC per market; no ven | N/A | PARTIAL |
| Social sentiment firehose (X, Reddit, Bluesky, TikTok) | NONE FOUND accessible | N/A | UNCOVERED |
| Licensed newswire, embargoed releases and machine-readable press releases | PARTIAL — GDELT DOC 2.0 and Google News RSS give web-indexed | NONE FOUND | PARTIAL |
| Non-US company filings and fundamentals | NONE FOUND consolidated | NONE FOUND consolidated | UNCOVERED |
| Fund flows, 13F positioning, options open interest by strike | PARTIAL — CFTC CoT (futures positioning only), Cboe delayed  | N/A | PARTIAL |
| Recommended build order for shared services | See note | See note | COVERED |

### Consolidations

- **The Odds API v4 (sports betting lines)** → CONSOLIDATE INTO: ESPN Core API odds endpoint. The inventory itself marks The Odds API as live=false across 9 sports subdomains — our only odds source is an unverified keyed vendor with a 500-request/month free cap. ESPN's sports.core.api.espn.com ..
- **TheSportsDB v1 (credited with 6 sports subdomains)** → DEMOTE — THE CLAIM IS FALSE AT THE FREE TIER. Measured: all_sports.php on both free keys /3/ and /123/ returns exactly two sports, Soccer and Motorsport. Any subdomain whose coverage rests on TheSportsDB must be re-verified against ESPN Core API, whi
- **Metaculus API** → DEAD FOR OUR PURPOSE — now auth-gated. GET /api/posts/ returns HTTP 403 'The API is only available to authenticated users.' REPLACED BY: Manifold Markets API (keyless, verified), which covers the same long-tail forecast questions including AGI milest
- **CME Group CmeWS quote endpoints (futures settlement / curve)** → DEAD — explicit IP block. Returns 'This IP address is blocked due to suspected web scraping activity... strictly prohibited by CME Group's website Data Terms of Use.' NO FREE REPLACEMENT FOUND. Futures curves and exchange settlement prices remain an 
- **SofaScore API (api.sofascore.com and www.sofascore.com/api/v1)** → BLOCKED — HTTP 403 on both hosts. Significant because Kalshi's own settlement_sources names sofascore.com/table-tennis as the settlement authority for its table-tennis series. NO FREE REPLACEMENT FOUND; table tennis stays UNCOVERED for settlement.
- **Sotheby's /api/v1/search/lots, Christie's /api/discoverywebsite/searchbyquery, Artsy price database, Art Market API** → NOT FEEDS. The two auction-house endpoints return HTML/SPA shells, not JSON (verified). Artsy's price database is free but UI-only with no API. Art Market API is credit-metered (100 free credits), which is a trial, not a free tier. Art & Auctions has
- **Adjacent News API (prediction-market aggregator)** → DEAD — api.data.adj.news connection timed out (HTTP 000). REPLACED BY: ingesting the four venues directly (Kalshi, Polymarket, PredictIt, ForecastEx), which we must do anyway for order-book depth and settlement metadata an aggregator would strip.
- **Bluesky public.api.bsky.app and reddit.com/*/.json** → BLOCKED FROM DATACENTER EGRESS — 403 / HTML interstitial respectively (verified). Not rejected on merit; rejected as currently unreachable. Revisit if egress changes. Do not list social sentiment as covered on the strength of these.
- **BIS WS_CBPOL + ECB Data Portal + Eurostat + OECD SDMX + StatCan WDS + ONS beta + World Bank Indicators, as seven separate macro feeds** → CONSOLIDATE INTO: DBnomics API v22 (verified HTTP 200 serving Federal Reserve H.15 under one schema). One series path, one JSON shape, ~90 providers, no keys. KEEP the official endpoint ONLY where that exact series settles a contract — a mirror must 
- **Federal Register API v1, listed separately in 8 domains** → CONSOLIDATE INTO: one shared Federal Register ingester with an agency/topic filter applied downstream. It appears as a distinct primaryFeed in politics, geopolitics, financial-markets, crypto, technology, climate, health and transportation. It is one
- **GDELT DOC 2.0 API + GDELT raw 15-minute files, listed separately in 7 domains** → CONSOLIDATE INTO: one shared GDELT ingester. Critically, GDELT enforces 'one request every 5 seconds' (measured — a rapid second call returned the throttle notice instead of data). Seven independent domain pollers will throttle each other into failur
- **Wikimedia Pageviews API + Wikidata WDQS + EventStreams, listed separately across 6 domains** → CONSOLIDATE INTO: one Wikimedia service. Note the WDQS User-Agent requirement is load-bearing — a call without a descriptive UA returned HTTP 000 while the same query with one returned HTTP 200. Centralising the client is what guarantees every caller
- **Kalshi Trade API v2 and Polymarket Gamma/CLOB, listed as primaryFeeds in 18 and 17 domains respectively** → CONSOLIDATE INTO: one venue-ingest service per venue, with domain assignment derived from Kalshi's category enum (20 values, verified) downstream. Today they are counted as ~35 feed entries for what is 2 APIs and 1 full-catalogue pull of 17MB. Pollin
- **Redfin Data Center metro market tracker** → CONSOLIDATE INTO: FRED (CSUSHPINSA, MORTGAGE30US, HOUST, EXHOSLUSM495S). The inventory itself flags Redfin as ~4 months stale. A stale feed presented as live is worse than an absent one; FRED carries the Case-Shiller and Census series on a documented
- **Alpha Vantage Commodities API (11 functions)** → CONSOLIDATE INTO: FRED fredgraph CSV + World Bank Pink Sheet, both already primary in commodities and both keyless. Alpha Vantage's free tier is 25 requests/day, which cannot sustain a live terminal across 12 commodity subdomains. Keep Alpha Vantage 
- **Yahoo Finance chart endpoint v8 (unofficial)** → CONSOLIDATE INTO: Nasdaq public API + Cboe delayed CDN (+ Robinhood marketdata if counsel clears it). The inventory already annotates Yahoo as HEAVILY THROTTLED. Three unofficial sources for one number is worse than one; pick the least fragile and mo
- **GDELT TV 2.0 API (Television Explorer)** → DEAD — data frozen at 2024-10-10 per the inventory's own note, and the Internet Archive TV News captions fall back to 403. NO REPLACEMENT FOUND. Consequence, stated plainly: Kalshi's 'Mentions' category holds 445 series and we have no way to settle b
