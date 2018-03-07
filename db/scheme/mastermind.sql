CREATE TABLE IF NOT EXISTS games (
  id char(40) NOT NULL,
  code text NOT NULL,
  PRIMARY KEY (id)
) DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS history (
  game_id char(40) NOT NULL,
  guess text NOT NULL,
  result JSON NOT NULL,
  PRIMARY KEY (game_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE NO ACTION
) DEFAULT CHARSET=utf8;