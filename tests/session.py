import droit

# Init database
db = droit.Database(multiSession=True)
db.loadPlugins()
db.parseScript("tests/test.dda")

# Load sessions
db.sessions.path = "tests/sessions.json"
db.sessions.loadSessions()
db.sessions.activateByUsername("Max Mustermann")

success = True

if not(db.simpleIO("Wer bin ich") == "Du bist Max Mustermann"):
    success = False

db.sessions.activateByUsername("Maxine Mustermann")

if not(db.simpleIO("Wer bin ich") == "Du bist Maxine Mustermann"):
    success = False

if success:
    print("test: 'session' successful")
else:
    print("test: 'session' failed")