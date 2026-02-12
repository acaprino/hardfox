# Firefox `about:config` — Riferimento Completo delle Preferenze Documentate

> **Nota**: Non esiste un documento ufficiale Mozilla che elenchi tutte le preferenze di `about:config`. Questo documento compila le preferenze documentate da fonti ufficiali e comunitarie affidabili: MozillaZine Knowledge Base, MDN Web Docs, Firefox Source Code e ghacks user.js.
>
> **Versione di riferimento**: Firefox 130+ (febbraio 2026)
>
> **Legenda tipi**: `Boolean` (true/false), `Integer` (numero intero), `String` (testo)

---

## Sommario

1. [Accessibility.*](#accessibility)
2. [Alerts.*](#alerts)
3. [App.*](#app)
4. [Bidi.*](#bidi)
5. [Browser.*](#browser)
6. [Config.*](#config)
7. [Content.*](#content)
8. [DOM.*](#dom)
9. [Editor.*](#editor)
10. [Extensions.*](#extensions)
11. [Font.*](#font)
12. [General.*](#general)
13. [GFX.*](#gfx)
14. [Image.*](#image)
15. [Intl.*](#intl)
16. [Javascript.*](#javascript)
17. [Layout.*](#layout)
18. [Media.*](#media)
19. [Middlemouse.*](#middlemouse)
20. [Network.*](#network)
21. [Permissions.*](#permissions)
22. [Places.*](#places)
23. [Plugin.*](#plugin)
24. [Print.*](#print)
25. [Privacy.*](#privacy)
26. [Security.*](#security)
27. [Signon.*](#signon)
28. [Toolkit.*](#toolkit)
29. [UI.*](#ui)
30. [Preferenze Sperimentali (MDN)](#sperimentali)

---

## 1. Accessibility.* {#accessibility}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `accessibility.accesskeycausesactivation` | Boolean | `true` | true/false | `true`: premere un tasto di accesso attiva il controllo. `false`: il tasto di accesso sposta solo il focus. |
| `accessibility.blockautorefresh` | Boolean | `false` | true/false | `true`: blocca i meta refresh e redirect HTTP refresh. `false`: permette auto-refresh. |
| `accessibility.browsewithcaret` | Boolean | `false` | true/false | `true`: abilita la navigazione con cursore (caret browsing) nelle pagine web. `false`: disabilitata. Attivabile con F7. |
| `accessibility.tabfocus` | Integer | varia per OS | 1–7 (bitmask) | Controlla quali elementi ricevono focus tramite Tab. `1`: solo campi testo. `2`: tutti i form tranne campi testo. `4`: solo link. `7` (default Mac): tutti gli elementi. |
| `accessibility.typeaheadfind` | Boolean | `false` | true/false | `true`: abilita "Find As You Type" automaticamente quando si digita in una pagina. `false`: solo con `/` o `'`. |
| `accessibility.typeaheadfind.autostart` | Boolean | `true` | true/false | `true`: il typeahead find parte automaticamente alla digitazione. `false`: richiede attivazione manuale. |
| `accessibility.typeaheadfind.casesensitive` | Integer | `0` | 0/1/2 | `0`: case-insensitive. `1`: case-sensitive. `2`: auto-detect (sensibile se contiene maiuscole). |
| `accessibility.typeaheadfind.flashBar` | Integer | `1` | 0–n | Numero di volte che la barra di ricerca lampeggia quando si attiva il typeahead find. `0`: disabilita. |
| `accessibility.typeaheadfind.linksonly` | Boolean | `false` | true/false | `true`: il typeahead find cerca solo nei link. `false`: cerca in tutto il testo della pagina. |
| `accessibility.typeaheadfind.timeout` | Integer | `4000` | millisecondi | Tempo in ms prima che il typeahead find si disattivi automaticamente dopo l'ultima digitazione. |

---

## 2. Alerts.* {#alerts}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `alerts.slideIncrement` | Integer | `1` | pixel | Numero di pixel per incremento nell'animazione di scorrimento delle notifiche popup. |
| `alerts.slideIncrementTime` | Integer | `10` | millisecondi | Tempo in ms tra ogni incremento dell'animazione slide delle notifiche. |
| `alerts.totalOpenTime` | Integer | `4000` | millisecondi | Tempo totale in ms che una notifica popup resta visibile prima di chiudersi. |

---

## 3. App.* {#app}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `app.update.auto` | Boolean | `true` | true/false | `true`: scarica automaticamente gli aggiornamenti. `false`: solo notifica. |
| `app.update.enabled` | Boolean | `true` | true/false | `true`: abilita il controllo aggiornamenti. `false`: disabilita completamente. |
| `app.update.interval` | Integer | `86400` | secondi | Intervallo tra i controlli automatici per aggiornamenti (default: 24 ore). |
| `app.update.url` | String | URL Mozilla | URL | URL del server di aggiornamento. |
| `app.update.log` | Boolean | `false` | true/false | `true`: scrive log dettagliati degli aggiornamenti nella console. |

---

## 4. Bidi.* {#bidi}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `bidi.browser.ui` | Boolean | `false` | true/false | `true`: attiva interfaccia bidirezionale incondizionatamente. `false`: solo in locali bidi. |
| `bidi.characterset` | Integer | `1` | 1/2 | `1`: set di caratteri specificato dal documento. `2`: set di caratteri predefinito. |
| `bidi.controlstextmode` | Integer | `1` | 1/2/3 | `1`: logico. `2`: visuale. `3`: container. |
| `bidi.direction` | Integer | `1` | 1/2 | `1`: testo da sinistra a destra (LTR). `2`: testo da destra a sinistra (RTL). |
| `bidi.numeral` | Integer | `0` | 0–4 | `0`: numerali nominali. `1`: numerali contestuali regolari. `2`: numerali contestuali hindi. `3`: numerali arabi. `4`: numerali hindi. |
| `bidi.support` | Integer | `1` | 1/2/3 | `1`: supporto bidi Mozilla. `2`: supporto bidi OS. `3`: disabilita supporto bidi. |
| `bidi.texttype` | Integer | `1` | 1/2/3 | `1`: charset. `2`: logico. `3`: visuale. |
| `bidi.edit.caret_movement_style` | Integer | `0` | 0/1/2 | `0`: logico. `1`: visuale. `2`: numerico. Stile di movimento del cursore in testo bidirezionale. |

---

## 5. Browser.* {#browser}

### 5.1 Aspetto e colori

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.active_color` | String | `#EE0000` | codice hex | Colore predefinito per i link attivi (mentre si clicca). |
| `browser.anchor_color` | String | `#0000EE` | codice hex | Colore predefinito per i link non visitati. |
| `browser.visited_color` | String | `#551A8B` | codice hex | Colore predefinito per i link visitati. |
| `browser.display.background_color` | String | `#FFFFFF` | codice hex | Colore di sfondo predefinito per le pagine web. |
| `browser.display.foreground_color` | String | `#000000` | codice hex | Colore del testo predefinito per le pagine web. |
| `browser.display.focus_background_color` | String | `#117722` | codice hex | Colore di sfondo degli elementi con focus (richiede `use_focus_colors`). |
| `browser.display.focus_text_color` | String | `#FFFFFF` | codice hex | Colore del testo degli elementi con focus (richiede `use_focus_colors`). |
| `browser.display.use_focus_colors` | Boolean | `false` | true/false | `true`: usa colori personalizzati per gli elementi con focus. |
| `browser.display.focus_ring_on_anything` | Boolean | `false` | true/false | `true`: mostra l'anello di focus su qualsiasi elemento, non solo sui link. |
| `browser.display.focus_ring_width` | Integer | `1` | 0–n pixel | Larghezza dell'anello di focus in pixel. `0`: nasconde l'anello. |
| `browser.display.use_document_colors` | Boolean | `true` | true/false | `true`: permette ai documenti di specificare i propri colori. `false`: usa sempre i colori dell'utente. |
| `browser.display.use_document_fonts` | Integer | `1` | 0/1 | `0`: non usa mai i font del documento. `1`: permette ai documenti di specificare i font. |
| `browser.display.use_system_colors` | Boolean | `false` | true/false | `true`: usa i colori del sistema operativo per i documenti. |
| `browser.display.show_image_placeholders` | Boolean | `true` | true/false | `true`: mostra segnaposto durante il caricamento delle immagini. |
| `browser.display.force_inline_alttext` | Boolean | `false` | true/false | `true`: forza la visualizzazione inline del testo alt delle immagini non caricate. |

### 5.2 Navigazione e comportamento

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.backspace_action` | Integer | `2` | 0/1/2+ | `0`: il backspace torna indietro nella cronologia. `1`: agisce come Page Up. `2`+: nessuna azione. |
| `browser.link.open_newwindow` | Integer | `3` | 1/2/3 | `1`: apre nella finestra corrente. `2`: apre in una nuova finestra. `3`: apre in un nuovo tab. |
| `browser.link.open_newwindow.restriction` | Integer | `2` | 0/1/2 | `0`: applica `open_newwindow` a tutti i link. `1`: nessuna restrizione. `2`: applica solo ai link senza specifiche di dimensione finestra. |
| `browser.link.open_external` | Integer | `3` | 1/2/3 | Dove aprire link da applicazioni esterne. `1`: finestra corrente. `2`: nuova finestra. `3`: nuovo tab. |
| `browser.blink_allowed` | Boolean | `true` | true/false | `true`: permette l'effetto blink (testo lampeggiante). `false`: disabilita il blink. |
| `browser.frames.enabled` | Boolean | `true` | true/false | `true`: abilita la visualizzazione dei frame HTML. `false`: mostra il contenuto `<noframes>`. |
| `browser.enable_automatic_image_resizing` | Boolean | `true` | true/false | `true`: ridimensiona le immagini grandi per adattarle alla finestra quando visualizzate singolarmente. |
| `browser.send_pings` | Boolean | `false` | true/false | `true`: invia ping di tracciamento quando si cliccano link con attributo `ping`. `false`: blocca i ping. |
| `browser.send_pings.max_per_link` | Integer | `1` | 0–n | Numero massimo di URL a cui inviare ping per ogni click su un link. |

### 5.3 Ricerca e barra degli indirizzi

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.fixup.alternate.enabled` | Boolean | `true` | true/false | `true`: tenta di correggere URL incompleti (es. aggiunge www. e .com). |
| `browser.fixup.alternate.prefix` | String | `www.` | testo | Prefisso aggiunto quando si tenta di correggere un URL. |
| `browser.fixup.alternate.suffix` | String | `.com` | testo | Suffisso aggiunto quando si tenta di correggere un URL. |
| `browser.urlbar.trimHttps` | Boolean | varia | true/false | `true`: nasconde il prefisso `https://` nella barra degli indirizzi. |
| `browser.urlbar.autoFill` | Boolean | `true` | true/false | `true`: autocompletamento nella barra degli indirizzi basato su cronologia e segnalibri. |
| `browser.urlbar.suggest.searches` | Boolean | `true` | true/false | `true`: mostra suggerimenti di ricerca nella barra degli indirizzi. |
| `browser.urlbar.suggest.bookmark` | Boolean | `true` | true/false | `true`: mostra suggerimenti dai segnalibri. |
| `browser.urlbar.suggest.history` | Boolean | `true` | true/false | `true`: mostra suggerimenti dalla cronologia. |
| `browser.urlbar.suggest.openpage` | Boolean | `true` | true/false | `true`: mostra suggerimenti dalle schede aperte. |
| `browser.search.suggest.enabled` | Boolean | `true` | true/false | `true`: abilita i suggerimenti di ricerca dal motore predefinito. |
| `browser.search.openintab` | Boolean | `false` | true/false | `true`: apre i risultati di ricerca in un nuovo tab. |

### 5.4 Tab

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.tabs.closeWindowWithLastTab` | Boolean | `true` | true/false | `true`: chiude la finestra quando si chiude l'ultimo tab. `false`: mostra un tab vuoto. |
| `browser.tabs.insertRelatedAfterCurrent` | Boolean | `true` | true/false | `true`: apre nuovi tab correlati (es. link) accanto al tab corrente. `false`: in fondo. |
| `browser.tabs.insertAfterCurrent` | Boolean | `false` | true/false | `true`: tutti i nuovi tab si aprono dopo il tab corrente. |
| `browser.tabs.loadBookmarksInTabs` | Boolean | `false` | true/false | `true`: apre i segnalibri in nuovi tab. `false`: apre nel tab corrente. |
| `browser.tabs.loadDivertedInBackground` | Boolean | `false` | true/false | `true`: i link aperti da applicazioni esterne restano in background. |
| `browser.tabs.loadInBackground` | Boolean | `true` | true/false | `true`: i nuovi tab si aprono in background. `false`: il nuovo tab diventa attivo. |
| `browser.tabs.warnOnClose` | Boolean | `true` | true/false | `true`: avvisa quando si chiude una finestra con più tab. |
| `browser.tabs.warnOnOpen` | Boolean | `true` | true/false | `true`: avvisa quando si aprono molti tab contemporaneamente (es. da cartella segnalibri). |
| `browser.tabs.tabMinWidth` | Integer | `76` | pixel | Larghezza minima di un tab in pixel. |
| `browser.tabs.tabClipWidth` | Integer | `140` | pixel | Sotto questa larghezza, il pulsante di chiusura del tab viene nascosto. |

### 5.5 Cache

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.cache.check_doc_frequency` | Integer | `3` | 0/1/2/3 | `0`: controlla una volta per sessione. `1`: controlla ogni volta. `2`: non controlla mai (usa sempre la cache). `3`: controlla automaticamente quando la pagina è scaduta. |
| `browser.cache.disk.enable` | Boolean | `true` | true/false | `true`: abilita la cache su disco. |
| `browser.cache.disk.capacity` | Integer | `256000` | KB | Spazio massimo su disco per la cache, in kilobyte. |
| `browser.cache.disk.parent_directory` | String | (profilo) | percorso | Percorso della directory padre della cartella Cache. |
| `browser.cache.disk_cache_ssl` | Boolean | `false` | true/false | `true`: salva in cache contenuti ricevuti via SSL (rischio sicurezza). |
| `browser.cache.memory.enable` | Boolean | `true` | true/false | `true`: abilita la cache in memoria RAM. |
| `browser.cache.memory.capacity` | Integer | `-1` | -1/0/n KB | `-1`: dimensione automatica basata sulla RAM. `0`: disabilita. `n`: dimensione in KB. |
| `browser.cache.offline.enable` | Boolean | `true` | true/false | `true`: abilita la cache offline (per applicazioni web). |

### 5.6 Download

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.download.useDownloadDir` | Boolean | `true` | true/false | `true`: scarica direttamente nella cartella predefinita. `false`: chiede dove salvare. |
| `browser.download.folderList` | Integer | `1` | 0/1/2 | `0`: desktop. `1`: cartella Downloads. `2`: ultima cartella usata. |
| `browser.download.dir` | String | (vuoto) | percorso | Ultima directory usata per il salvataggio. |
| `browser.download.manager.retention` | Integer | `2` | 0/1/2 | `0`: rimuove al completamento. `1`: rimuove alla chiusura del browser. `2`: rimozione manuale. |

### 5.7 Favicon e icone

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.chrome.favicons` | Boolean | `true` | true/false | `true`: carica e mostra le favicon. |
| `browser.chrome.site_icons` | Boolean | `true` | true/false | `true`: carica icone specificate dall'elemento `<link>` nella pagina. |
| `browser.chrome.image_icons.max_size` | Integer | `1024` | pixel | Se un'immagine supera questa dimensione, non viene usata come thumbnail nel tab. |

### 5.8 Form e helper

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.formfill.enable` | Boolean | `true` | true/false | `true`: salva e autocompleta i dati inseriti nei form. |
| `browser.helperApps.alwaysAsk.force` | Boolean | `false` | true/false | `true`: chiede sempre cosa fare con tipi MIME sconosciuti e impedisce di ricordare la scelta. |
| `browser.helperApps.neverAsk.openFile` | String | (vuoto) | lista MIME | Lista separata da virgole di tipi MIME da aprire senza chiedere. |
| `browser.helperApps.neverAsk.saveToDisk` | String | (vuoto) | lista MIME | Lista separata da virgole di tipi MIME da salvare su disco senza chiedere. |

### 5.9 Sessione e avvio

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.startup.homepage` | String | about:home | URL | Homepage all'avvio del browser. |
| `browser.startup.page` | Integer | `1` | 0/1/2/3 | `0`: pagina vuota. `1`: homepage. `2`: ultima sessione. `3`: ripristina la sessione precedente. |
| `browser.sessionstore.resume_from_crash` | Boolean | `true` | true/false | `true`: offre il ripristino della sessione dopo un crash. |
| `browser.sessionstore.interval` | Integer | `15000` | millisecondi | Intervallo di salvataggio automatico della sessione (default: 15 secondi). |
| `browser.sessionstore.max_tabs_undo` | Integer | `25` | 0–n | Numero massimo di tab chiusi che possono essere ripristinati. |
| `browser.sessionstore.max_windows_undo` | Integer | `3` | 0–n | Numero massimo di finestre chiuse che possono essere ripristinate. |
| `browser.sessionstore.privacy_level` | Integer | `0` | 0/1/2 | `0`: memorizza dati di sessione per tutti i siti. `1`: solo per siti non-HTTPS. `2`: non memorizza mai dati di sessione extra. |

### 5.10 Safebrowsing

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `browser.safebrowsing.malware.enabled` | Boolean | `true` | true/false | `true`: abilita protezione contro malware (Google Safe Browsing). |
| `browser.safebrowsing.phishing.enabled` | Boolean | `true` | true/false | `true`: abilita protezione contro phishing. |
| `browser.safebrowsing.downloads.enabled` | Boolean | `true` | true/false | `true`: controlla i download per malware. |
| `browser.safebrowsing.downloads.remote.enabled` | Boolean | `true` | true/false | `true`: invia hash di file scaricati a Google per il controllo. |
| `browser.safebrowsing.provider.google4.dataSharing.enabled` | Boolean | `false` | true/false | `true`: condivide dati aggiuntivi con Google Safe Browsing. |

---

## 6. Config.* {#config}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `config.trim_on_minimize` | Boolean | `false` | true/false | Solo Windows. `true`: rilascia memoria quando Firefox è minimizzato. Può causare rallentamenti al ripristino. |

---

## 7. Content.* {#content}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `content.interrupt.parsing` | Boolean | `true` | true/false | `true`: permette l'interruzione del parsing per gestire eventi UI, migliorando la reattività. |
| `content.notify.interval` | Integer | `120000` | microsecondi | Intervallo minimo tra aggiornamenti di rendering durante il caricamento della pagina. |
| `content.notify.ontimer` | Boolean | `true` | true/false | `true`: aggiorna il rendering della pagina a intervalli regolari durante il caricamento. |
| `content.notify.backoffcount` | Integer | `-1` | -1/n | `-1`: nessun limite. `n`: numero massimo di aggiornamenti timer prima di smettere. |

---

## 8. DOM.* {#dom}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `dom.allow_scripts_to_close_windows` | Boolean | `false` | true/false | `true`: permette agli script di chiudere qualsiasi finestra. `false`: solo finestre aperte dagli script stessi. |
| `dom.disable_beforeunload` | Boolean | `false` | true/false | `true`: disabilita gli avvisi "beforeunload" quando si lascia una pagina. |
| `dom.disable_open_during_load` | Boolean | `false` | true/false | `true`: blocca i popup durante il caricamento della pagina. |
| `dom.disable_window_flip` | Boolean | `false` | true/false | `true`: impedisce agli script di portare finestre in primo piano (focus). |
| `dom.disable_window_move_resize` | Boolean | `false` | true/false | `true`: impedisce agli script di spostare o ridimensionare finestre. |
| `dom.disable_window_open_feature.close` | Boolean | `false` | true/false | `true`: forza il pulsante di chiusura nelle finestre popup. |
| `dom.disable_window_open_feature.location` | Boolean | `false` | true/false | `true`: forza la barra degli indirizzi nelle finestre popup. |
| `dom.disable_window_open_feature.menubar` | Boolean | `false` | true/false | `true`: forza la barra dei menu nelle finestre popup. |
| `dom.disable_window_open_feature.minimizable` | Boolean | `false` | true/false | `true`: forza la possibilità di minimizzare le finestre popup. |
| `dom.disable_window_open_feature.resizable` | Boolean | `true` | true/false | `true`: forza la ridimensionabilità delle finestre popup. |
| `dom.disable_window_open_feature.status` | Boolean | `true` | true/false | `true`: forza la barra di stato nelle finestre popup. |
| `dom.disable_window_open_feature.titlebar` | Boolean | `false` | true/false | `true`: forza la barra del titolo nelle finestre popup. |
| `dom.disable_window_open_feature.toolbar` | Boolean | `false` | true/false | `true`: forza la barra degli strumenti nelle finestre popup. |
| `dom.disable_window_status_change` | Boolean | `false` | true/false | `true`: impedisce agli script di modificare il testo nella barra di stato. |
| `dom.event.clipboardevents.enabled` | Boolean | `true` | true/false | `true`: permette ai siti di intercettare eventi copia/incolla. `false`: impedisce ai siti di sapere quando si copia/incolla. |
| `dom.event.contextmenu.enabled` | Boolean | `true` | true/false | `true`: permette ai siti di intercettare/disabilitare il menu contestuale (tasto destro). `false`: impedisce il blocco del click destro. |
| `dom.max_script_run_time` | Integer | `10` | secondi | Tempo massimo di esecuzione di uno script prima del dialogo "script non risponde". |
| `dom.popup_allowed_events` | String | `change click dblclick mouseup pointerup notificationclick reset submit touchend contextmenu` | lista eventi | Eventi che possono aprire popup senza essere bloccati. |
| `dom.popup_maximum` | Integer | `20` | 0–n | Numero massimo di popup che possono essere aperti da un singolo evento. |
| `dom.storage.enabled` | Boolean | `true` | true/false | `true`: abilita Web Storage (localStorage/sessionStorage). |
| `dom.webnotifications.enabled` | Boolean | `true` | true/false | `true`: abilita le notifiche web (Web Notifications API). |
| `dom.webnotifications.requireinteraction.enabled` | Boolean | varia | true/false | `true`: le notifiche restano visibili fino all'interazione dell'utente. |
| `dom.webnotifications.actions.enabled` | Boolean | `false` | true/false | `true`: abilita azioni sulle notifiche (sperimentale). |
| `dom.vr.enabled` | Boolean | `false` | true/false | `true`: abilita l'API WebVR (deprecata). |
| `dom.webgpu.enabled` | Boolean | varia | true/false | `true`: abilita l'API WebGPU. Abilitato per default su Windows e macOS Apple Silicon nelle release stabili. |
| `dom.payments.request.enabled` | Boolean | `false` | true/false | `true`: abilita la Payment Request API (sperimentale). |
| `dom.webshare.enabled` | Boolean | varia | true/false | `true`: abilita la Web Share API. Default `true` su Android. |
| `dom.screenorientation.allow-lock` | Boolean | `false` | true/false | `true`: permette il blocco dell'orientamento schermo. |
| `dom.reporting.enabled` | Boolean | `false` | true/false | `true`: abilita la Reporting API per violazioni CSP. |
| `dom.security.trusted_types.enabled` | Boolean | `false` | true/false | `true`: abilita la Trusted Types API (protezione XSS). |
| `dom.security.sanitizer.enabled` | Boolean | varia | true/false | `true`: abilita la HTML Sanitizer API. |
| `dom.closewatcher.enabled` | Boolean | varia | true/false | `true`: abilita l'interfaccia CloseWatcher per componenti UI chiudibili. |
| `dom.events.script_execute.enable` | Boolean | `true` | true/false | `true`: abilita gli eventi non-standard `beforescriptexecute`/`afterscriptexecute`. In rimozione. |
| `dom.forms.datetime.timepicker` | Boolean | `false` | true/false | `true`: abilita il selettore orario per input datetime-local. |
| `dom.navigation.webidl.enabled` | Boolean | `false` | true/false | `true`: abilita la Navigation API (sperimentale Nightly). |

---

## 9. Editor.* {#editor}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `editor.singleLine.pasteNewlines` | Integer | `1` | 0–4 | Comportamento incolla testo multilinea in campi a riga singola. `0`: incolla intatto. `1`: fino al primo a-capo. `2`: sostituisce a-capo con spazi. `3`: rimuove a-capo. `4`: sostituisce a-capo con virgole. |
| `editor.use_css` | Boolean | `true` | true/false | `true`: usa CSS per la formattazione nell'editor rich-text. `false`: usa metodi non-CSS. |
| `editor.use_custom_colors` | Boolean | `false` | true/false | `true`: usa colori personalizzati specificati nelle preferenze dell'editor. |

---

## 10. Extensions.* {#extensions}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `extensions.autoDisableScopes` | Integer | `15` | bitmask | Ambiti in cui le estensioni vengono disabilitate automaticamente dopo l'installazione. `0`: nessuno. `1`: profilo. `2`: utente. `4`: applicazione. `8`: sistema. `15`: tutti. |
| `extensions.blocklist.enabled` | Boolean | `true` | true/false | `true`: abilita la lista di blocco delle estensioni (malware/incompatibili). |
| `extensions.pocket.enabled` | Boolean | `true` | true/false | `true`: abilita l'integrazione Pocket. |
| `extensions.screenshots.disabled` | Boolean | `false` | true/false | `true`: disabilita la funzionalità screenshot integrata. |
| `extensions.update.autoUpdateDefault` | Boolean | `true` | true/false | `true`: le estensioni si aggiornano automaticamente. |
| `extensions.update.enabled` | Boolean | `true` | true/false | `true`: controlla gli aggiornamenti delle estensioni. |

---

## 11. Font.* {#font}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `font.default.x-western` | String | `serif` | serif/sans-serif | Font predefinito per i testi occidentali. |
| `font.minimum-size.x-western` | Integer | `0` | pixel | Dimensione minima del font per i testi occidentali. `0`: nessun minimo. |
| `font.name.serif.x-western` | String | `Times New Roman` | nome font | Font serif predefinito per i testi occidentali. |
| `font.name.sans-serif.x-western` | String | `Arial` | nome font | Font sans-serif predefinito per i testi occidentali. |
| `font.name.monospace.x-western` | String | `Courier New` | nome font | Font monospace predefinito per i testi occidentali. |
| `font.size.variable.x-western` | Integer | `16` | pixel | Dimensione predefinita per font proporzionali. |
| `font.size.monospace.x-western` | Integer | `13` | pixel | Dimensione predefinita per font monospace. |

---

## 12. General.* {#general}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `general.autoScroll` | Boolean | `true` (Win/Linux) | true/false | `true`: abilita lo scorrimento automatico con il click del tasto centrale del mouse. |
| `general.smoothScroll` | Boolean | `true` | true/false | `true`: abilita lo scorrimento fluido. `false`: scorrimento pixel-by-pixel. |
| `general.smoothScroll.lines.durationMaxMS` | Integer | `150` | millisecondi | Durata massima animazione smooth scroll per riga. |
| `general.smoothScroll.pages.durationMaxMS` | Integer | `150` | millisecondi | Durata massima animazione smooth scroll per pagina. |
| `general.useragent.override` | String | (non impostato) | stringa UA | Sovrascrive la stringa User-Agent del browser. Non impostare se non necessario. |
| `general.warnOnAboutConfig` | Boolean | `true` | true/false | `true`: mostra l'avviso di sicurezza quando si accede a about:config. (Versioni precedenti) |

---

## 13. GFX.* {#gfx}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `gfx.canvas.accelerated` | Boolean | varia | true/false | `true`: abilita l'accelerazione hardware per canvas 2D. |
| `gfx.webrender.all` | Boolean | varia | true/false | `true`: abilita WebRender per tutti gli utenti. |
| `gfx.font_rendering.cleartype_params.rendering_mode` | Integer | `-1` | -1 / 0–5 | `-1`: automatico. `0`–`5`: modalità di rendering ClearType specifiche (solo Windows). |

---

## 14. Image.* {#image}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `image.animation_mode` | String | `normal` | normal/once/none | `normal`: le GIF animate si ripetono normalmente. `once`: le GIF animate vengono riprodotte una sola volta. `none`: le GIF animate non vengono riprodotte. |
| `image.avif.compliance_strictness` | Integer | `1` | 0/1/2 | `0`: permissivo — accetta immagini AVIF con violazioni sia di raccomandazioni che di requisiti. `1`: misto — rifiuta violazioni di requisiti, accetta violazioni di raccomandazioni. `2`: rigoroso — rifiuta qualsiasi violazione. |
| `image.jxl.enabled` | Boolean | `false` | true/false | `true`: abilita il supporto JPEG XL. Disponibile solo su Nightly. |
| `image.mem.surfacecache.max_size_kb` | Integer | `2097152` | KB | Dimensione massima della cache delle superfici immagine in KB. |

---

## 15. Intl.* {#intl}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `intl.accept_languages` | String | `en-US, en` | lista lingue | Lingue preferite inviate nell'header HTTP Accept-Language, separate da virgole. |
| `intl.charset.detector` | String | (vuoto) | nome detector | Rilevatore automatico del set di caratteri. Valori comuni: vuoto (disabilitato), `ja_parallel_state_machine` (giapponese). |
| `intl.locale.requested` | String | (vuoto) | codice locale | Locale richiesto dall'utente (es. `it`, `en-US`). Vuoto = usa il locale del sistema. |

---

## 16. Javascript.* {#javascript}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `javascript.enabled` | Boolean | `true` | true/false | `true`: abilita JavaScript. `false`: disabilita JavaScript globalmente (sconsigliato). |
| `javascript.options.mem.high_water_mark` | Integer | `128` | MB | Soglia di memoria oltre la quale il GC è più aggressivo. |
| `javascript.options.mem.max` | Integer | `-1` | -1/n MB | Memoria massima per il motore JS. `-1`: nessun limite. |
| `javascript.options.wasm` | Boolean | `true` | true/false | `true`: abilita WebAssembly. |
| `javascript.options.shared_memory` | Boolean | `true` | true/false | `true`: abilita SharedArrayBuffer (richiede COOP/COEP). |

---

## 17. Layout.* {#layout}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `layout.css.devPixelsPerPx` | String | `-1.0` | -1.0 / float | `-1.0`: usa il DPI del sistema. Qualsiasi altro valore (es. `1.5`): sovrascrive il rapporto pixel, modificando lo zoom di tutta l'interfaccia. |
| `layout.css.dpi` | Integer | `-1` | -1/0/n | `-1`: DPI del sistema o 96, il maggiore. `0`: usa il DPI del sistema. `n`: DPI specifico. |
| `layout.word_select.eat_space_to_next_word` | Boolean | `true` (Win) | true/false | `true`: la selezione doppio-click include lo spazio dopo la parola. |
| `layout.spellcheckDefault` | Integer | `1` | 0/1/2 | `0`: disabilita il controllo ortografico. `1`: solo nei campi multilinea. `2`: anche nei campi a riga singola. |
| `layout.css.scroll-driven-animations.enabled` | Boolean | `false` (release) | true/false | `true`: abilita le animazioni guidate dallo scroll (scroll-driven animations). |
| `layout.css.control-characters.visible` | Boolean | `false` (release) | true/false | `true`: rende visibili i caratteri di controllo come box esagonali. |
| `layout.css.initial-letter.enabled` | Boolean | `false` | true/false | `true`: abilita la proprietà CSS `initial-letter` per capolettera decorativi. |
| `layout.css.fit-content-function.enabled` | Boolean | `false` | true/false | `true`: abilita la funzione CSS `fit-content()` per proprietà di dimensionamento. |
| `layout.css.prefers-reduced-transparency.enabled` | Boolean | `false` | true/false | `true`: abilita la media query `prefers-reduced-transparency`. |
| `layout.css.inverted-colors.enabled` | Boolean | `false` | true/false | `true`: abilita la media query `inverted-colors`. |
| `layout.css.basic-shape-shape.enabled` | Boolean | `false` (release) | true/false | `true`: abilita la funzione CSS `shape()` per clip-path e offset-path. |
| `layout.css.letter-spacing.model` | Boolean | `false` (release) | true/false | `true`: abilita la spaziatura simmetrica delle lettere. |
| `layout.css.relative-color-syntax.enabled` | Boolean | `false` (release) | true/false | `true`: abilita il supporto `calc()` per canali colore in colori relativi. |
| `layout.css.heading-selector.enabled` | Boolean | `false` | true/false | `true`: abilita le pseudo-classi CSS `:heading` e `:heading()`. |
| `layout.css.text-decoration-trim.enabled` | Boolean | `false` | true/false | `true`: abilita la proprietà CSS `text-decoration-trim`. |
| `layout.css.custom-media.enabled` | Boolean | `false` | true/false | `true`: abilita la regola at-rule `@custom-media`. |
| `layout.css.prefixes.transforms` | Boolean | `true` | true/false | `true`: abilita le proprietà CSS transform prefissate con `-moz-`. `false`: rimuove il supporto ai prefissi. |
| `layout.css.convertFromNode.enable` | Boolean | `false` (release) | true/false | `true`: abilita i metodi GeometryUtils `convertPointFromNode()`, `convertRectFromNode()`, `convertQuadFromNode()`. |
| `layout.css.getBoxQuads.enabled` | Boolean | `false` (release) | true/false | `true`: abilita il metodo GeometryUtils `getBoxQuads()`. |
| `layout.forms.input-type-search.enabled` | Boolean | `false` | true/false | `true`: abilita il layout aggiornato per `input type="search"` con icona di cancellazione. |
| `layout.forms.reveal-password-button.enabled` | Boolean | `false` | true/false | `true`: mostra un'icona "occhio" per rivelare/nascondere le password nei campi input. |

---

## 18. Media.* {#media}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `media.autoplay.default` | Integer | `1` | 0/1/5 | `0`: permette autoplay. `1`: blocca autoplay audio. `5`: blocca tutto l'autoplay (audio e video). |
| `media.autoplay.blocking_policy` | Integer | `0` | 0/1/2 | `0`: scelta dell'utente. `1`: blocca autoplay per tutti i siti. `2`: blocca solo in contesti con interazione dell'utente. |
| `media.eme.enabled` | Boolean | `true` | true/false | `true`: abilita Encrypted Media Extensions (per DRM come Widevine). |
| `media.gmp-widevinecdm.enabled` | Boolean | `true` | true/false | `true`: abilita il modulo CDM Widevine per contenuti DRM. |
| `media.mediasource.experimental.enabled` | Boolean | `false` | true/false | `true`: abilita metodi sperimentali su SourceBuffer (`appendBufferAsync()`, `removeAsync()`). |
| `media.peerconnection.enabled` | Boolean | `true` | true/false | `true`: abilita WebRTC. `false`: disabilita (migliora la privacy ma rompe videochiamate). |
| `media.peerconnection.ice.default_address_only` | Boolean | `false` | true/false | `true`: espone solo l'indirizzo IP predefinito tramite WebRTC ICE (protegge IP locale). |
| `media.peerconnection.ice.no_host` | Boolean | `false` | true/false | `true`: impedisce la divulgazione dell'IP host tramite WebRTC. |
| `media.track.enabled` | Boolean | `false` | true/false | `true`: abilita le proprietà `audioTracks` e `videoTracks` su HTMLMediaElement. |
| `media.navigator.enabled` | Boolean | `true` | true/false | `true`: abilita `navigator.mediaDevices` e `getUserMedia()`. `false`: impedisce ai siti di accedere a fotocamera/microfono. |
| `media.peerconnection.video.vp9_enabled` | Boolean | `true` | true/false | `true`: abilita il codec VP9 per WebRTC. |
| `media.webm.enabled` | Boolean | `true` | true/false | `true`: abilita la riproduzione di file WebM. |

---

## 19. Middlemouse.* {#middlemouse}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `middlemouse.contentLoadURL` | Boolean | `false` (Win/Mac), `true` (Linux) | true/false | `true`: un click con il tasto centrale sulla pagina carica l'URL contenuto negli appunti. |
| `middlemouse.paste` | Boolean | `false` (Win/Mac), `true` (Linux) | true/false | `true`: il tasto centrale incolla il contenuto degli appunti nei campi di testo. |
| `middlemouse.openNewWindow` | Boolean | `true` | true/false | `true`: un click con il tasto centrale su un link apre il link in un nuovo tab. |

---

## 20. Network.* {#network}

### 20.1 Connessione e protocollo

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `network.http.max-connections` | Integer | `900` | 1–n | Numero massimo di connessioni HTTP simultanee totali. |
| `network.http.max-persistent-connections-per-server` | Integer | `6` | 1–n | Numero massimo di connessioni persistenti per server. |
| `network.http.max-persistent-connections-per-proxy` | Integer | `32` | 1–n | Numero massimo di connessioni persistenti per proxy. |
| `network.http.pipelining` | Boolean | `false` | true/false | `true`: abilita HTTP pipelining (deprecato, rimosso nelle versioni recenti). |
| `network.http.version` | String | `1.1` | 1.0/1.1 | Versione massima del protocollo HTTP da usare. |
| `network.http.sendRefererHeader` | Integer | `2` | 0/1/2 | `0`: non invia mai l'header Referer. `1`: invia solo su click. `2`: invia sempre (anche per immagini ecc.). |
| `network.http.referer.XOriginPolicy` | Integer | `0` | 0/1/2 | `0`: invia sempre referer cross-origin. `1`: invia solo se i domini base corrispondono. `2`: invia solo se i host completi corrispondono. |
| `network.http.referer.XOriginTrimmingPolicy` | Integer | `0` | 0/1/2 | `0`: invia URL completo come referer cross-origin. `1`: invia URL senza query string. `2`: invia solo lo schema+host+porta. |
| `network.http.referer.trimmingPolicy` | Integer | `0` | 0/1/2 | Come sopra ma per referer same-origin. |
| `network.http.speculative-parallel-limit` | Integer | `6` | 0–n | Numero massimo di connessioni speculative parallele. `0`: disabilita connessioni speculative (migliora privacy). |
| `network.http.redirection-limit` | Integer | `20` | 0–n | Numero massimo di redirect HTTP da seguire prima di restituire un errore. |

### 20.2 DNS e prefetch

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `network.dns.disableIPv6` | Boolean | `false` | true/false | `true`: disabilita la risoluzione DNS IPv6 (AAAA). Utile se l'ISP non supporta IPv6. |
| `network.dns.disablePrefetch` | Boolean | `false` | true/false | `true`: disabilita il prefetch DNS. Migliora la privacy. |
| `network.dns.echconfig.enabled` | Boolean | `true` | true/false | `true`: abilita Encrypted Client Hello per DNS. |
| `network.dnsCacheEntries` | Integer | `400` | 0–n | Numero di voci nella cache DNS. `0`: disabilita la cache DNS. |
| `network.dnsCacheExpiration` | Integer | `60` | secondi | Tempo di vita delle voci nella cache DNS, in secondi. |
| `network.prefetch-next` | Boolean | `true` | true/false | `true`: abilita il link prefetching (precarica pagine suggerite dai siti). `false`: disabilita (migliora privacy). |
| `network.predictor.enabled` | Boolean | `true` | true/false | `true`: abilita il network predictor per precaricamento speculativo delle risorse. |

### 20.3 Proxy

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `network.proxy.type` | Integer | `5` | 0–5 | `0`: nessun proxy. `1`: configurazione manuale. `2`: auto-configurazione (PAC URL). `4`: auto-detect (WPAD). `5`: usa le impostazioni del sistema. |
| `network.proxy.http` | String | (vuoto) | hostname | Indirizzo del proxy HTTP. |
| `network.proxy.http_port` | Integer | `0` | 0–65535 | Porta del proxy HTTP. |
| `network.proxy.ssl` | String | (vuoto) | hostname | Indirizzo del proxy HTTPS. |
| `network.proxy.ssl_port` | Integer | `0` | 0–65535 | Porta del proxy HTTPS. |
| `network.proxy.socks` | String | (vuoto) | hostname | Indirizzo del proxy SOCKS. |
| `network.proxy.socks_port` | Integer | `0` | 0–65535 | Porta del proxy SOCKS. |
| `network.proxy.socks_version` | Integer | `5` | 4/5 | Versione del protocollo SOCKS. |
| `network.proxy.socks_remote_dns` | Boolean | `false` | true/false | `true`: risolve il DNS tramite il proxy SOCKS (essenziale con Tor). |
| `network.proxy.no_proxies_on` | String | `localhost, 127.0.0.1` | lista host | Host per i quali non usare il proxy. |

### 20.4 Cookie e sicurezza rete

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `network.cookie.cookieBehavior` | Integer | `5` | 0–5 | `0`: accetta tutti i cookie. `1`: solo dal sito originale (blocca terze parti). `2`: blocca tutti. `3`: usa la lista di blocco P3P (rimosso). `4`: blocca cookie traccianti. `5`: Total Cookie Protection (isolamento per sito). |
| `network.cookie.lifetimePolicy` | Integer | `0` | 0/2 | `0`: accetta normalmente. `2`: i cookie scadono alla chiusura del browser. |
| `network.cookie.thirdparty.sessionOnly` | Boolean | `false` | true/false | `true`: i cookie di terze parti scadono alla chiusura della sessione. |
| `network.IDN_show_punycode` | Boolean | `false` | true/false | `true`: mostra i nomi di dominio internazionalizzati in Punycode nella barra degli indirizzi. Protegge da attacchi omografici (es. аррӏе.com che sembra apple.com). |
| `network.cors_preflight.authorization_covered_by_wildcard` | Boolean | `true` | true/false | `true`: l'header Authorization è incluso nella risposta con `Access-Control-Allow-Headers: *`. |

### 20.5 TLS/SSL

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `network.http.spdy.enabled` | Boolean | `true` | true/false | `true`: abilita il protocollo SPDY. |
| `network.http.http2.enabled` | Boolean | `true` | true/false | `true`: abilita HTTP/2. |
| `network.http.http3.enabled` | Boolean | `true` | true/false | `true`: abilita HTTP/3 (QUIC). |
| `security.tls.version.min` | Integer | `3` | 1–4 | Versione TLS minima. `1`: TLS 1.0. `2`: TLS 1.1. `3`: TLS 1.2. `4`: TLS 1.3. |
| `security.tls.version.max` | Integer | `4` | 1–4 | Versione TLS massima. `4`: TLS 1.3. |

---

## 21. Permissions.* {#permissions}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `permissions.default.camera` | Integer | `0` | 0/1/2 | `0`: chiede sempre. `1`: permetti. `2`: blocca. |
| `permissions.default.microphone` | Integer | `0` | 0/1/2 | `0`: chiede sempre. `1`: permetti. `2`: blocca. |
| `permissions.default.desktop-notification` | Integer | `0` | 0/1/2 | `0`: chiede sempre. `1`: permetti. `2`: blocca le notifiche desktop. |
| `permissions.default.geo` | Integer | `0` | 0/1/2 | `0`: chiede sempre. `1`: permetti. `2`: blocca la geolocalizzazione. |

---

## 22. Places.* {#places}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `places.history.enabled` | Boolean | `true` | true/false | `true`: registra la cronologia dei siti visitati. `false`: disabilita la cronologia. |

---

## 23. Plugin.* {#plugin}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `plugin.default.state` | Integer | `1` | 0/1/2 | `0`: disabilitato. `1`: chiedi per attivare. `2`: sempre attivo. Stato predefinito per i plugin. |
| `plugins.click_to_play` | Boolean | `true` | true/false | `true`: i plugin richiedono un click per essere attivati (click-to-play). |

---

## 24. Print.* {#print}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `print.print_footerleft` | String | `&PT` | codici formato | Piè di pagina sinistro. `&PT`: numero pagina / totale. |
| `print.print_footerright` | String | `&D` | codici formato | Piè di pagina destro. `&D`: data. |
| `print.print_headerleft` | String | `&T` | codici formato | Intestazione sinistra. `&T`: titolo pagina. |
| `print.print_headerright` | String | `&U` | codici formato | Intestazione destra. `&U`: URL pagina. |
| `print.print_bgcolor` | Boolean | `false` | true/false | `true`: stampa i colori di sfondo. `false`: non stampa gli sfondi. |
| `print.print_bgimages` | Boolean | `false` | true/false | `true`: stampa le immagini di sfondo. |
| `print.shrink_to_fit` | Boolean | `true` | true/false | `true`: ridimensiona automaticamente il contenuto per adattarlo alla pagina stampata. |

---

## 25. Privacy.* {#privacy}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `privacy.donottrackheader.enabled` | Boolean | `false` | true/false | `true`: invia l'header "Do Not Track" (DNT: 1) ai siti web. |
| `privacy.globalprivacycontrol.enabled` | Boolean | `false` | true/false | `true`: invia il segnale Global Privacy Control (Sec-GPC: 1) ai siti. |
| `privacy.firstparty.isolate` | Boolean | `false` | true/false | `true`: isola cookie, cache e dati per dominio di primo livello (First Party Isolation). Può rompere alcuni siti. |
| `privacy.resistFingerprinting` | Boolean | `false` | true/false | `true`: abilita le contromisure anti-fingerprinting. Modifica molti comportamenti del browser (fuso orario, dimensione finestra, canvas, font, ecc.). Può impattare l'usabilità. |
| `privacy.trackingprotection.enabled` | Boolean | `false` | true/false | `true`: abilita la protezione dal tracciamento in modalità normale. |
| `privacy.trackingprotection.pbmode.enabled` | Boolean | `true` | true/false | `true`: abilita la protezione dal tracciamento in modalità privata. |
| `privacy.trackingprotection.socialtracking.enabled` | Boolean | `false` | true/false | `true`: blocca i tracker dei social network. |
| `privacy.trackingprotection.fingerprinting.enabled` | Boolean | `false` | true/false | `true`: blocca i fingerprinter noti. |
| `privacy.trackingprotection.cryptomining.enabled` | Boolean | `false` | true/false | `true`: blocca i script di cryptomining noti. |
| `privacy.sanitize.sanitizeOnShutdown` | Boolean | `false` | true/false | `true`: cancella i dati specificati alla chiusura del browser. |
| `privacy.clearOnShutdown.cache` | Boolean | `false` | true/false | `true`: cancella la cache alla chiusura. Richiede `sanitizeOnShutdown` = true. |
| `privacy.clearOnShutdown.cookies` | Boolean | `false` | true/false | `true`: cancella i cookie alla chiusura. |
| `privacy.clearOnShutdown.downloads` | Boolean | `false` | true/false | `true`: cancella la cronologia download alla chiusura. |
| `privacy.clearOnShutdown.formdata` | Boolean | `false` | true/false | `true`: cancella i dati dei form alla chiusura. |
| `privacy.clearOnShutdown.history` | Boolean | `false` | true/false | `true`: cancella la cronologia alla chiusura. |
| `privacy.clearOnShutdown.offlineApps` | Boolean | `false` | true/false | `true`: cancella i dati delle app offline alla chiusura. |
| `privacy.clearOnShutdown.sessions` | Boolean | `false` | true/false | `true`: cancella le sessioni attive alla chiusura. |
| `privacy.clearOnShutdown.siteSettings` | Boolean | `false` | true/false | `true`: cancella le impostazioni dei siti alla chiusura. |

---

## 26. Security.* {#security}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `security.ask_for_password` | Integer | `0` | 0/1/2 | `0`: non chiede mai la password principale. `1`: chiede una volta per sessione. `2`: chiede ogni N minuti (vedi `security.password_lifetime`). |
| `security.password_lifetime` | Integer | `30` | minuti | Tempo in minuti dopo il quale viene richiesta la password principale. Richiede `ask_for_password` = 2. |
| `security.OCSP.enabled` | Integer | `1` | 0/1/2 | `0`: disabilita OCSP. `1`: verifica OCSP per certificati che specificano un server OCSP. `2`: verifica OCSP per tutti i certificati. |
| `security.OCSP.require` | Boolean | `false` | true/false | `true`: rifiuta il certificato se il server OCSP non risponde (OCSP stapling rigoroso). |
| `security.cert_pinning.enforcement_level` | Integer | `1` | 0/1/2/3 | `0`: disabilitato. `1`: permette utenti di superare i pin per CA non built-in. `2`: rigoroso. `3`: forza test sui pin. |
| `security.mixed_content.block_active_content` | Boolean | `true` | true/false | `true`: blocca il contenuto misto attivo (script, CSS, iframe su pagine HTTPS). |
| `security.mixed_content.block_display_content` | Boolean | `false` | true/false | `true`: blocca anche il contenuto misto passivo (immagini, video su pagine HTTPS). |
| `security.insecure_connection_text.enabled` | Boolean | varia | true/false | `true`: mostra la dicitura "Non sicuro" nella barra degli indirizzi per pagine HTTP. |
| `security.insecure_connection_text.pbmode.enabled` | Boolean | varia | true/false | `true`: mostra la dicitura "Non sicuro" anche in modalità privata. |
| `security.ssl.require_safe_negotiation` | Boolean | `false` | true/false | `true`: richiede la rinegoziazione sicura SSL. Può impedire la connessione a server non aggiornati. |
| `security.ssl.treat_unsafe_negotiation_as_broken` | Boolean | `false` | true/false | `true`: mostra un avviso visivo per connessioni con rinegoziazione non sicura. |
| `security.pki.sha1_enforcement_level` | Integer | `1` | 0–4 | `0`: permette SHA-1 ovunque. `1`: proibisce per CA pubbliche. `2`: proibisce ovunque. `3`: solo per CA importate. `4`: solo per CA built-in. |
| `security.restrict_to_adults.always` | Boolean | `false` | true/false | `true`: blocca sempre i contenuti adulti marcati con `<meta name="rating">`. Sperimentale. |
| `security.restrict_to_adults.respect_platform` | Boolean | `false` | true/false | `true`: rispetta le impostazioni della piattaforma per i contenuti adulti. Sperimentale. |

---

## 27. Signon.* {#signon}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `signon.autofillForms` | Boolean | `true` | true/false | `true`: compila automaticamente i campi di login con le credenziali salvate. |
| `signon.rememberSignons` | Boolean | `true` | true/false | `true`: offre di salvare le password. `false`: non chiede mai di salvare password. |
| `signon.storeWhenAutocompleteOff` | Boolean | `true` | true/false | `true`: salva password anche per form con `autocomplete="off"`. |

---

## 28. Toolkit.* {#toolkit}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `toolkit.cosmeticAnimations.enabled` | Boolean | `true` | true/false | `true`: abilita le animazioni cosmetiche dell'interfaccia (apertura tab, transizioni). `false`: disabilita (utile su PC lenti). |
| `toolkit.legacyUserProfileCustomizations.stylesheets` | Boolean | `false` | true/false | `true`: abilita il caricamento di `userChrome.css` e `userContent.css` dal profilo per personalizzare l'interfaccia. |
| `toolkit.telemetry.enabled` | Boolean | varia | true/false | `true`: invia dati di telemetria a Mozilla. Default `true` su pre-release, `false` su release. |
| `toolkit.telemetry.unified` | Boolean | `true` | true/false | `true`: abilita il sistema di telemetria unificato. |

---

## 29. UI.* {#ui}

| Preferenza | Tipo | Default | Dominio valori | Descrizione |
|---|---|---|---|---|
| `ui.key.menuAccessKeyFocuses` | Boolean | `true` (Win/Linux) | true/false | `true`: premere e rilasciare Alt attiva il menu. |
| `ui.submenuDelay` | Integer | varia per OS | millisecondi | Ritardo in ms prima che un sottomenu si apra al passaggio del mouse. |
| `ui.prefersReducedMotion` | Integer | (non impostato) | 0/1 | `0`: preferisce le animazioni. `1`: preferisce il movimento ridotto. Sovrascrive le impostazioni del sistema. |
| `ui.systemUsesDarkTheme` | Integer | (non impostato) | 0/1 | `0`: forza tema chiaro. `1`: forza tema scuro. Sovrascrive le impostazioni del sistema. |

---

## 30. Preferenze Sperimentali (MDN Experimental Features) {#sperimentali}

Questa sezione elenca le preferenze che controllano feature sperimentali secondo la documentazione MDN. Sono tutte di tipo **Boolean**, con `true` per abilitare la feature.

| Preferenza | Categoria | Descrizione |
|---|---|---|
| `layout.forms.input-type-search.enabled` | HTML | Layout aggiornato per `input type="search"` con icona di cancellazione. |
| `layout.forms.reveal-password-button.enabled` | HTML | Pulsante "mostra password" nei campi password. |
| `dom.forms.datetime.timepicker` | HTML | Selettore orario per input `datetime-local`. |
| `layout.css.control-characters.visible` | CSS | Rende visibili i caratteri di controllo come hex box. |
| `layout.css.initial-letter.enabled` | CSS | Proprietà `initial-letter` per capolettera. |
| `layout.css.fit-content-function.enabled` | CSS | Funzione `fit-content()` per proprietà di dimensionamento. |
| `layout.css.scroll-driven-animations.enabled` | CSS | Animazioni guidate dallo scroll. |
| `layout.css.prefers-reduced-transparency.enabled` | CSS | Media query `prefers-reduced-transparency`. |
| `layout.css.inverted-colors.enabled` | CSS | Media query `inverted-colors`. |
| `layout.css.basic-shape-shape.enabled` | CSS | Funzione `shape()` per `clip-path` e `offset-path`. |
| `layout.css.letter-spacing.model` | CSS | Spaziatura simmetrica delle lettere. |
| `layout.css.relative-color-syntax.enabled` | CSS | Supporto `calc()` per canali colore relativi. |
| `layout.css.heading-selector.enabled` | CSS | Pseudo-classi `:heading` e `:heading()`. |
| `layout.css.text-decoration-trim.enabled` | CSS | Proprietà `text-decoration-trim`. |
| `layout.css.custom-media.enabled` | CSS | Regola at-rule `@custom-media`. |
| `layout.css.prefixes.transforms` | CSS | Proprietà transform prefissate `-moz-`. |
| `dom.closewatcher.enabled` | API | Interfaccia CloseWatcher. |
| `dom.security.trusted_types.enabled` | API | Trusted Types API (protezione XSS). |
| `dom.security.sanitizer.enabled` | API | HTML Sanitizer API. |
| `dom.events.script_execute.enable` | API | Eventi `beforescriptexecute`/`afterscriptexecute` (in rimozione). |
| `dom.webnotifications.actions.enabled` | API | Azioni sulle notifiche e proprietà `maxActions`. |
| `webgl.enable-draft-extensions` | API | Estensioni WebGL in draft. |
| `dom.webgpu.enabled` | API | WebGPU API. |
| `dom.webgpu.service-workers.enabled` | API | WebGPU nei service workers. |
| `dom.reporting.enabled` | API | Reporting API per violazioni CSP. |
| `media.mediasource.experimental.enabled` | API | SourceBuffer asincrono (`appendBufferAsync()`). |
| `image.avif.compliance_strictness` | API | Rigore conformità AVIF (Integer 0–2). |
| `image.jxl.enabled` | API | Supporto JPEG XL (solo Nightly). |
| `dom.vr.enabled` | API | WebVR API (deprecata). |
| `media.track.enabled` | API | Proprietà `audioTracks`/`videoTracks` su media. |
| `layout.css.convertFromNode.enable` | API | Metodi GeometryUtils `convertFromNode`. |
| `layout.css.getBoxQuads.enabled` | API | Metodo GeometryUtils `getBoxQuads()`. |
| `dom.payments.request.enabled` | API | Payment Request API. |
| `dom.payments.request.supportedRegions` | API | Regioni supportate per Payment Request (String, es. `US,CA`). |
| `dom.webshare.enabled` | API | Web Share API. |
| `dom.screenorientation.allow-lock` | API | ScreenOrientation.lock(). |
| `dom.webnotifications.requireinteraction.enabled` | API | Notifiche persistenti fino all'interazione. |
| `security.insecure_connection_text.enabled` | Sicurezza | Testo "Non sicuro" nella barra indirizzi (HTTP). |
| `security.insecure_connection_text.pbmode.enabled` | Sicurezza | Testo "Non sicuro" in navigazione privata. |
| `browser.urlbar.trimHttps` | Sicurezza | Nasconde il prefisso `https:` dalla barra indirizzi. |
| `security.restrict_to_adults.always` | Sicurezza | Restrizione contenuti adulti via `<meta name="rating">`. |
| `security.restrict_to_adults.respect_platform` | Sicurezza | Rispetta le impostazioni della piattaforma per contenuti adulti. |
| `dom.navigation.webidl.enabled` | API | Navigation API (solo Nightly). |
| `network.cors_preflight.authorization_covered_by_wildcard` | HTTP | Header Authorization coperto da wildcard CORS. |

---

## Note finali

### Fonti

- **MozillaZine Knowledge Base**: [kb.mozillazine.org/About:config_entries](http://kb.mozillazine.org/About:config_entries) e [Category:Preferences](http://kb.mozillazine.org/Category:Preferences) (~445 preferenze documentate, aggiornamento fino a ~2014)
- **MDN Web Docs**: [Experimental features in Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Experimental_features) (aggiornato regolarmente)
- **Firefox Source Code**: [searchfox.org - StaticPrefList.yaml](https://searchfox.org/mozilla-release/source/modules/libpref/init/StaticPrefList.yaml) e [all.js](https://searchfox.org/mozilla-release/source/modules/libpref/init/all.js)
- **ghacks user.js**: [github.com/0XDE57](https://gist.github.com/0XDE57/fbd302cef7693e62c769)
- **arkenfox user.js**: [github.com/arkenfox/user.js](https://github.com/arkenfox/user.js)

### Avvertenze

1. **Versione**: Alcune preferenze elencate qui potrebbero essere state rimosse, rinominate o sostituite nelle versioni più recenti di Firefox.
2. **Completezza**: Questo non è l'elenco completo di tutte le preferenze in `about:config` (oltre 3.000), ma di quelle per le quali esiste documentazione pubblica.
3. **Rischio**: Modificare preferenze in `about:config` può compromettere la stabilità, la sicurezza e le prestazioni del browser. Procedere con cautela.
4. **Reset**: Per ripristinare una preferenza al valore predefinito, fare click destro sulla riga e selezionare "Ripristina".
