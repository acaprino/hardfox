# Analisi Tecnica: Gap di Sincronizzazione (Sync Blind Spot)

## 1. Descrizione del Problema
È stata identificata una lacuna critica nel database delle impostazioni di Hardfox (`settings_metadata.py`). Attualmente, l'applicazione non mappa né gestisce le preferenze relative a **Firefox Sync** (chiavi `services.sync.*`).

Questo crea un "punto cieco" architetturale dove Hardfox può configurare correttamente il browser locale, ma le impostazioni possono essere sovrascritte silenziosamente dal cloud di Mozilla se la sincronizzazione è attiva per quelle specifiche preferenze.

## 2. Meccanismo del Conflitto
Firefox Sync opera su un livello di priorità che può confliggere con le modifiche apportate da Hardfox:

1. **Hardfox (Local)**: Scrive le preferenze in `user.js` (persistenti al riavvio) o `prefs.js`.
2. **Firefox Sync (Cloud)**: Quando il browser viene avviato e si connette a internet, confronta lo stato locale con lo stato salvato sul server.
3. **Sovrascrittura**: Se `services.sync.prefs.sync.privacy.sanitize.sanitizeOnShutdown` è impostato su `true` (default), Firefox Sync caricherà il valore presente sugli altri dispositivi dell'utente, ignorando potenzialmente la modifica locale di Hardfox (specialmente se Hardfox ha modificato `prefs.js` anziché bloccare il parametro via `user.js`).

### Casi d'uso critici:
- **Login persistente**: Se Hardfox imposta `sanitizeOnShutdown` a `false` per evitare la perdita dei cookie, ma un altro PC dell'utente ha `true`, la sincronizzazione riporterà il valore a `true` al prossimo riavvio, provocando nuovamente la perdita dei login.

## 3. Rischi Identificati
- **Inconsistenza della Privacy**: L'utente crede di essere protetto perché Hardfox conferma l'applicazione dei settaggi, ma il cloud "inietta" vecchi settaggi meno sicuri.
- **Difficoltà di Debugging**: Poiché Hardfox non vede queste chiavi, non può segnalare all'utente che il problema della perdita dei login è causato da un conflitto di sincronizzazione.
- **Mancanza di Controllo Granulare**: L'utente non può decidere, tramite Hardfox, quali settaggi di privacy devono restare locali e quali possono essere condivisi tra i dispositivi.

## 4. Proposta di Soluzione

### A. Estensione della Metadata
Aggiungere una nuova categoria `synchronization` in `settings_metadata.py` includendo:
- `services.sync.prefs.sync.[PREF_NAME]`: Toggle per decidere se sincronizzare una specifica impostazione.
- `services.sync.engine.prefs`: Toggle generale per la sincronizzazione di tutte le preferenze.

### B. Strategia di "Sync Lock"
Implementare una logica dell'IntentAnalyzer che, quando si scelgono profili "Strong" o "Maximum", imposti automaticamente a `false` la sincronizzazione delle preferenze critiche per evitare che dispositivi non protetti infettino la configurazione sicura.

## 5. Elenco Pref da Aggiungere (Esempi)
| Chiave | Tipo | Descrizione |
| :--- | :--- | :--- |
| `services.sync.prefs.sync.privacy.sanitize.sanitizeOnShutdown` | Toggle | Sincronizza lo stato della pulizia alla chiusura |
| `services.sync.prefs.sync.network.cookie.cookieBehavior` | Toggle | Sincronizza la gestione dei cookie |
| `services.sync.engine.passwords` | Toggle | Sincronizza le password salvate |

---
*Documento di analisi creato a seguito del bug report relativo alla perdita dei login in profili sincronizzati.*
