-- migrate:up
create table users(
    user_id UUID primary key default gen_random_uuid(),
    username varchar(255) unique,
    hashed_password varchar(255) not null,
    email varchar(255) not null
);

create table tasks(
    user_id UUID not null,
    task_id UUID default gen_random_uuid(),
    title varchar(255) not null,
    deadline date not null,
    duration numeric(4, 2) not null,
    foreign key (user_id)
    references users(user_id)
);


-- migrate:down
drop table if EXISTS tasks;
drop table if EXISTS users;
