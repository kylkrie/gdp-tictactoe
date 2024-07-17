CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    -- I would normally make this an int or uuid but I'm not doing full auth
    user_id VARCHAR(255) NOT NULL,
    spaces BYTEA NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW()),
    updated_at TIMESTAMP NOT NULL DEFAULT (NOW())
);

CREATE TRIGGER update_boards_modtime
    BEFORE UPDATE ON boards
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();
