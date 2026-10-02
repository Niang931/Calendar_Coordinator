-- migrate:up
create table if not exists users(
    user_id UUID primary key default gen_random_uuid(),
    username varchar(255) unique,
    hashed_password varchar(255) not null,
    email varchar(255) not null
);

create table if not exists tasks(
    user_id UUID not null,
    task_id UUID primary key default gen_random_uuid(),
    title varchar(255) not null,
    start_date date not null,
    start_time time not null,
    duration numeric(4, 2) not null,
    foreign key (user_id)
    references users(user_id)
);

create table association_table(
    task_id UUID not null,
    user_id UUID not null,
    role varchar(255) not null,
    foreign key (task_id)
    references tasks(task_id),
    foreign key (user_id)
    references users(user_id)
);

-- migrate:down
drop table if exists user_meeting;
drop table if exists user_schedule;
drop table if exists user_group;
drop table if EXISTS association_table;
drop table if exists groups;
drop table if EXISTS tasks;
drop table if EXISTS users;
