CREATE USER app WITH PASSWORD 'put your password';

REVOKE CONNECT ON DATABASE bookverse FROM PUBLIC;
GRANT  CONNECT ON DATABASE bookverse  TO app;

REVOKE ALL     ON SCHEMA public FROM PUBLIC;
GRANT  USAGE   ON SCHEMA public  TO app;

create type rank as enum ('user', 'moderator', 'reviewer');

create table genres
(
    genre_id    smallserial not null
        constraint genres_pk
            primary key,
    genre_name  varchar(32),
    description text
);

alter table genres
    owner to postgres;

grant select, usage on sequence genres_genre_id_seq to app;

grant insert, select, update on genres to app;

create table series
(
    series_id   serial not null
        constraint series_pk
            primary key,
    series_name varchar(256),
    description text
);

alter table series
    owner to postgres;

grant select, usage on sequence series_series_id_seq to app;

grant insert, select, update on series to app;

create table books
(
    book_id      serial not null
        constraint books_pk
            primary key,
    series_id    integer
        constraint books_series_series_id_fk
            references series,
    book_name    varchar(128),
    rating_sum   integer check (rating_sum >=0),
    rating_num   integer check (rating_num >=0),
    publish_date date,
    preamble     text,
    cover_path   varchar(256)
);

alter table books
    owner to postgres;

grant select, usage on sequence books_book_id_seq to app;

grant insert, select, update on books to app;

create table genres_of_books
(
    book_id  integer  not null
        constraint genres_of_books_books_book_id_fk
            references books,
    genre_id smallint not null
        constraint genres_of_books_genres_genre_id_fk
            references genres,
    constraint genres_of_books_pk
        primary key (book_id, genre_id)
);

alter table genres_of_books
    owner to postgres;

grant insert, select, update on genres_of_books to app;

create table translators
(
    translator_id smallserial not null
        constraint translators_pk
            primary key,
    translator_name     varchar(48)
);

alter table translators
    owner to postgres;

grant select, usage on sequence translators_translator_id_seq to app;

grant insert, select, update on translators to app;

create unique index translators_translator_id_uindex
    on translators (translator_id);

create table translators_of_books
(
    book_id       integer  not null
        constraint translators_of_books_books_book_id_fk
            references books,
    translator_id smallint not null
        constraint translators_of_books_translators_translator_id_fk
            references translators,
    constraint translators_of_books_pk
        primary key (translator_id, book_id)
);

alter table translators_of_books
    owner to postgres;

grant insert, select, update on translators_of_books to app;

create table tags
(
    tag_id smallserial not null
        constraint tags_pk
            primary key,
    tag_name   varchar(32)
);

alter table tags
    owner to postgres;

grant select, usage on sequence tags_tag_id_seq to app;

grant insert, select, update on tags to app;

create unique index tags_tag_id_uindex
    on tags (tag_id);

create table tags_of_books
(
    book_id integer not null
        constraint tags_of_books_books_book_id_fk
            references books,
    tag_id  integer not null
        constraint tags_of_books_tags_tag_id_fk
            references tags,
    constraint tags_of_books_pk
        primary key (book_id, tag_id)
);

alter table tags_of_books
    owner to postgres;

grant insert, select, update on tags_of_books to app;

create table awards
(
    award_id    smallserial not null
        constraint awards_pk
            primary key,
    award_name        varchar(128),
    description text
);

alter table awards
    owner to postgres;

grant select, usage on sequence awards_award_id_seq to app;

grant insert, select, update on awards to app;

create unique index awards_award_id_uindex
    on awards (award_id);

create table awards_of_books
(
    book_id    integer  not null
        constraint awards_of_books_books_book_id_fk
            references books,
    award_id   smallint not null
        constraint awards_of_books_awards_award_id_fk
            references awards,
    award_date date,
    constraint awards_of_books_pk
        primary key (book_id, award_id)
);

alter table awards_of_books
    owner to postgres;

grant insert, select, update on awards_of_books to app;

create table authors
(
    author_id  serial not null
        constraint authors_pk
            primary key,
    author_name       varchar(48),
    bio        text,
    photo_path varchar(256)
);

alter table authors
    owner to postgres;

grant select, usage on sequence authors_author_id_seq to app;

grant insert, select, update on authors to app;

create unique index authors_author_id_uindex
    on authors (author_id);

create table authors_of_books
(
    book_id   integer not null
        constraint authors_of_books_books_book_id_fk
            references books,
    author_id integer not null
        constraint authors_of_books_authors_author_id_fk
            references authors,
    constraint authors_of_books_pk
        primary key (book_id, author_id)
);

alter table authors_of_books
    owner to postgres;

grant insert, select, update on authors_of_books to app;

create table stores
(
    store_id   smallserial not null
        constraint stores_pk
            primary key,
    store_name varchar(32),
    logo_path  varchar(256)
);

alter table stores
    owner to postgres;

grant select, usage on sequence stores_store_id_seq to app;

grant insert, select, update, delete on stores to app;

create unique index stores_store_id_uindex
    on stores (store_id);

create table stores_of_books
(
    book_id     integer  not null
        constraint stores_of_books_books_book_id_fk
            references books,
    store_id    smallint not null
        constraint stores_of_books_stores_store_id_fk
            references stores
            on delete cascade,
    price       money,
    product_url varchar(256),
    constraint stores_of_books_pk
        primary key (book_id, store_id)
);

alter table stores_of_books
    owner to postgres;

grant insert, select, update on stores_of_books to app;

create table users
(
    user_id     serial not null
        constraint users_pk
            primary key,
    login       varchar(32),
    email       varchar(96),
    password    varchar(60),
    karma       smallint,
    avatar_path varchar(32),
    rank        rank
);

alter table users
    owner to postgres;

grant select, usage on sequence users_user_id_seq to app;

grant insert, select, update on users to app;

create unique index users_user_id_uindex
    on users (user_id);

create table wishlists
(
    user_id integer not null
        constraint wishlists_users_user_id_fk
            references users,
    book_id integer not null
        constraint wishlists_books_book_id_fk
            references books,
    constraint wishlists_pk
        primary key (user_id, book_id)
);

alter table wishlists
    owner to postgres;

grant insert, select, update on wishlists to app;

create table favorites
(
    user_id integer not null
        constraint favorites_users_user_id_fk
            references users,
    book_id integer not null
        constraint favorites_books_book_id_fk
            references books,
    constraint favorites_pk
        primary key (user_id, book_id)
);

alter table favorites
    owner to postgres;

grant insert, select, update on favorites to app;

create table reviews
(
    user_id      integer not null
        constraint reviews_users_user_id_fk
            references users,
    book_id      integer not null
        constraint reviews_books_book_id_fk
            references books,
    is_special   boolean,
    publish_date date,
    review       text,
    constraint reviews_pk
        primary key (user_id, book_id)
);

alter table reviews
    owner to postgres;

grant insert, select, update on reviews to app;

create table ratings
(
    user_id integer not null
        constraint ratings_users_user_id_fk
            references users,
    book_id integer not null
        constraint ratings_books_book_id_fk
            references books,
    rating  smallint check (rating > 0 and rating <= 10),
    constraint ratings_pk
        primary key (user_id, book_id)
);

alter table ratings
    owner to postgres;

grant insert, select, update on ratings to app;

insert into stores (store_name) values ('Литрес');
