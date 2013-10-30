drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists pagetitles;
create table pagetitles (
id integer primary key autoincrement,
rank integer default 0,
parent_id integer default 0,
mnemo text not null,
ptitle text not null,
added datetime not null,
in_use integer default 1
);
