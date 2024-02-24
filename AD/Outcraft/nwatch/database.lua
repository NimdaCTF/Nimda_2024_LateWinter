local DB = nil;

function initDB ()
  DB = sqlite3.open('nimda.sqlite3');
  DB:exec('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, value TEXT NULL, private BOOL DEFAULT false, added_at text not null, created_by text not null);');
  return true;
end

function addNoteDB(value, private, username)
  if not checkCName(value) then
    return false;
  end
  DB:exec(string.format('INSERT INTO notes (value, private, added_at, created_by) VALUES (\'%s\', %i, datetime(\'now\'), \'%s\');', value, private, username));
  return true;
end

function getNoteByIdDB(id)
  for row in DB:nrows(string.format('SELECT * FROM notes WHERE id=%i and private = false;', ID)) do
      return row;
  end
  return {};
end

function getNoteByValueDB(value, username)
  value = string.gsub(value, '_', ' ');
  for row in DB:nrows('SELECT * FROM notes WHERE value like \'%'.. value ..'%\' and (created_by = \''.. username ..'\' or private = false);') do
    return row;
  end
  return {};
end

