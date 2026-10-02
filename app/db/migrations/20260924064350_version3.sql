-- migrate:up
create type event_type as enum('schedule', 'vote');

alter table tasks add column occurence_type event_type default 'vote';
 
drop table if exists user_meeting;

create table if not exists meeting_proposals(
    proposal_id UUID primary key default gen_random_uuid(),
    title varchar(255) not null,
    group_id UUID not null,
    foreign key (group_id)
    references groups(group_id)
);

create table if not exists options(
    option_id UUID primary key default gen_random_uuid(),
    proposal_id UUID not null,
    start_date date not null,
    start_time time not null,
    meeting_duration numeric(4, 2) not null,
    description varchar(255),
    foreign key (proposal_id)
    references meeting_proposals(proposal_id)
);

create table if not exists votes (
    vote_id UUID primary key default gen_random_uuid(),
    user_id UUID not null,
    option_id UUID not null,
    foreign key (user_id)
    references users(user_id),
    foreign key (option_id)
    references options(option_id)
);

-- migrate:down
drop table if exists votes;
drop table if exists options;
drop table if exists meeting_proposals;
alter table tasks
drop column if exists occurence_type;
drop type if exists event_type;
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

