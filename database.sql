CREATE TABLE urls (
    id bigint NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) NOT NULL,
    created_at timestamp NOT NULL
);

