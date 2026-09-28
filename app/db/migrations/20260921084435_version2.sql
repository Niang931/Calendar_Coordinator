-- migrate:up
-- drop table if EXISTS association_table;
-- drop table if exists tasks;
-- drop table if exists users;

create table if not exists users(
    user_id UUID primary key default gen_random_uuid(),
    username varchar(255) not null,
    hashed_password varchar(255) not null,
    email varchar(255) not null
);

create table if not exists groups(
    group_id UUID primary key default gen_random_uuid(),
    group_name varchar(255) not null,
    group_description varchar(255)
);

create table if not exists user_group(
    ug_id UUID primary key default gen_random_uuid(),
    user_id UUID not null,
    group_id UUID not null,
    added_at date default current_date,
    foreign key (user_id)
    references users(user_id),
    foreign key (group_id)
    references groups(group_id)
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

create table if not exists user_schedule(
    us_id UUID primary key default gen_random_uuid(),
    task_id UUID not null,
    user_id UUID not null,
    created_at date default current_date,
    foreign key (task_id)
    references tasks(task_id),
    foreign key (user_id)
    references users(user_id)
);

create table if not exists user_meeting(
    um_id UUID primary key default gen_random_uuid(),
    user_id UUID not null,
    task_id UUID not null default gen_random_uuid(),
    group_id UUID not null,
    options jsonb not null,
    resolved bool not null default false,
    foreign key (user_id)
    references users(user_id),
    foreign key (group_id)
    references groups(group_id)
);
-- migrate:down
drop table if exists user_meeting;
-- drop table if exists user_schedule;
-- drop table if exists user_group;
-- drop table if exists groups;
-- drop table if exists tasks;
-- drop table if exists users;

