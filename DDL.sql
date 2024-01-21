create table cafe_inventory.product
(
    id             int auto_increment
        primary key,
    user_id        int                     null,
    category       varchar(50)             null,
    price          varchar(10)             null,
    cost           varchar(10)             null,
    name           varchar(50)             null,
    description    varchar(100)            null,
    barcode        varchar(20)             null,
    expration_date datetime                null,
    size           enum ('small', 'large') null,
    constraint product_ibfk_1
        foreign key (user_id) references cafe_inventory.user (id)
)
    charset = utf8;

create index user_id
    on cafe_inventory.product (user_id);

create table cafe_inventory.user
(
    id       int auto_increment
        primary key,
    phone    varchar(11)  null,
    password varchar(128) null,
    name     varchar(10)  null
)
    charset = utf8;

create table cafe_inventory.token
(
    user_id      int auto_increment
        primary key,
    access_token varchar(255) not null,
    created_at   datetime     null
)
    charset = utf8;



