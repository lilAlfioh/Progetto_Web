# Event Registration API

Applicazione web sviluppata con FastAPI per la gestione di eventi, utenti e registrazioni.

## Funzionalità

- Creazione, modifica e cancellazione di eventi
- Creazione e cancellazione di utenti
- Registrazione di utenti a eventi
- Validazione dei dati (email, data evento)
- Documentazione automatica tramite Swagger all'indirizzo /docs

## API disponibili

### Eventi

- GET /events
- GET /events/{id}
- POST /events
- PUT /events/{id}
- DELETE /events/{id}
- DELETE /events
- POST /events/{id}/register
- POST /events/{id}/upload

### Utenti

- GET /users
- GET /users/{username}
- POST /users
- DELETE /users/{username}
- DELETE /users

### Registrazioni

- GET /registrations
- DELETE /registrations?username=...&event_id=...

## Avvio

1. Clonare il progetto
2. Creare un ambiente virtuale
3. Installare le dipendenze con:

pip install -r requirements.txt

4. Avviare il server con:

uvicorn app.main:app --reload

## Autore

Leonardo Alfieri