CREATE TABLE IF NOT EXISTS urls (
    id bigint NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) NOT NULL,
    created_at date NOT NULL
);

CREATE TABLE IF NOT EXISTS url_checks (
    id bigint NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint NOT NULL,
    status_code int,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at date NOT NULL
);
