create type rank as enum ('user', 'moderator', 'redactor', 'admin');

create table books
(
    book_id      serial not null
        constraint books_pk
            primary key,
    book_name    varchar(256),
    rating_sum   integer
        constraint books_rating_sum_check
            check (rating_sum >= 0),
    rating_num   integer
        constraint books_rating_num_check
            check (rating_num >= 0),
    publish_date date,
    preamble     text,
    cover_path   varchar(256)
);

create table genres
(
    genre_id    smallserial not null
        constraint genres_pk
            primary key,
    genre_name  varchar(64),
    description text,
    popularity  integer default 0
);

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

create table series
(
    series_id   serial not null
        constraint series_pk
            primary key,
    series_name varchar(256),
    description text
);

create table series_of_books
(
    book_id   integer not null
        constraint series_of_books_books_book_id_fk
            references books,
    series_id integer not null
        constraint series_of_books_series_series_id_fk
            references series,
    constraint series_of_books_pk
        primary key (book_id, series_id)
);

create table translators
(
    translator_id   smallserial not null
        constraint translators_pk
            primary key,
    translator_name varchar(48)
);

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

create table tags
(
    tag_id   smallserial not null
        constraint tags_pk
            primary key,
    tag_name   varchar(64)
);

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

create table awards
(
    award_id    smallserial not null
        constraint awards_pk
            primary key,
    award_name  varchar(128),
    description text
);

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

create table authors
(
    author_id   serial not null
        constraint authors_pk
            primary key,
    author_name varchar(48),
    bio         text,
    photo_path  varchar(256),
    popularity  integer default 0
);

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

create table stores
(
    store_id   smallserial not null
        constraint stores_pk
            primary key,
    store_name varchar(32),
    logo_path  varchar(256)
);

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

create table ratings
(
    user_id integer not null
        constraint ratings_users_user_id_fk
            references users,
    book_id integer not null
        constraint ratings_books_book_id_fk
            references books,
    rating  smallint
        constraint ratings_rating_check
            check ((rating > 0) AND (rating <= 10)),
    constraint ratings_pk
        primary key (user_id, book_id)
);

create table redactors_choice
(
    user_id    integer not null
        constraint redactors_choice_users_user_id_fk
            references users,
    book_id    integer not null
        constraint redactors_choice_books_book_id_fk
            references books,
    added_date date    not null,
    constraint redactors_choice_pk
        primary key (user_id, book_id)
);

insert into stores (store_name) values ('Литрес');
