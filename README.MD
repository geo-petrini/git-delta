# GIT-Delta

Questo programma è stato creato per avere una panoramica delle modifiche avvenute durante il ciclo di vita di uno o più repository GIT.

## Funzionamento
La versione attuale si basa su repository clonati (locali).
Il programma legge un file di configurazione formattato nel modo seguente:

`config.json`
```json
{
    "repositories": [
        "/path/to/git/folder/1",
        "/path/to/git/folder/2",
        "."
    ]
}
```
Esso analizza tutti i commit del repository e produce un file html con un riassunto cronologico delle attività, quali:
- autore del commit
- messaggio
- timestamp
- files aggiunti
- files eliminati
- files modificati

Se i files sono testuali è possibile vederene il contenuto o le modifiche (diff).


## Roadmap
Non esiste una pianificazione dei prossimi sviluppi ma alcune aggiunte possibili sono:
- input di URL git per la clonazione del repository (invece che usare repo locali)
- formattazione del codice seguendo la sintassi corrispondente (es: https://highlightjs.org/)
- analisi del codice con un LLM per avere un riassunto testuale e cronologico delle modifiche attuate sui diversi commit
- analisi del codice per determinarne la qualità