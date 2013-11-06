create table if not exists entries(
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

create table if not exists pagetitles (
id integer primary key autoincrement,
rank integer default 0,
parent_id integer default 0,
mnemo text not null,
ptitle text not null,
added datetime not null,
in_use integer default 1
);
